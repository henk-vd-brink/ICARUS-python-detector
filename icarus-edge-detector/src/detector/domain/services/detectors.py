import abc
import logging
import torch
import numpy as np
import numba
import cv2
import pickle
import tensorrt as trt
import pycuda.autoinit
import pycuda.driver as cuda
import torchvision
import torchvision.transforms as transforms

logger = logging.getLogger(__name__)

class HostDeviceMem(object):
    def __init__(self, host_mem, device_mem):
        self.host = host_mem
        self.device = device_mem

    def __str__(self):
        return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

    def __repr__(self):
        return self.__str__()


class AbstractDetector(abc.ABC):
    pass


class FakeDetector(AbstractDetector):
    
    inference_results = [{"class": "person", "bounding_box": [0.1, 0.2, 0.3, 0.4], "confidence": 0.3}]

    def detect(self, data):
        data.inference_results = self.inference_results
        return data

    def __repr__(self):
        return "< FakeDetector >"

class YoloV5Detector(AbstractDetector):

    def __init__(self, config={}):

        self._ratio = config.get("ratio")
        self._confidence = config.get("confidence")
        self._labels = config.get("labels")

        self.logger = trt.Logger()

        self.max_batch_size = config.get("max_batch_size", 1)
        self.dtype = config.get("dtype", np.float16)
        self.image_size = config.get("image_size", (320, 320))
        self.n_classes = config.get("n_classes", 80)

        self.trt_runtime = trt.Runtime(self.logger)
        self.cfx = cuda.Device(0).make_context()

        self.engine = self._load_engine_from_path(self.trt_runtime, config.get("engine_path"))

        self.context = self.engine.create_execution_context()

        self.inputs, self.outputs, self.bindings, self.stream = self._allocate_buffers()

        if len(self.inputs) < 0:
            raise Exception("Error inputs TensorRT")

        if len(self.outputs) < 0:
            raise Exception("Error outputs TensorRT")

        if len(self.bindings) < 0:
            raise Exception("Error bindings TensorRT")

        self._warmup()


    def _load_engine_from_path(self, trt_runtime, engine_path):
        trt.init_libnvinfer_plugins(self.logger, "")

        with open(engine_path, 'rb') as f:
            engine_data = f.read()

        return trt_runtime.deserialize_cuda_engine(engine_data)

    def _allocate_buffers(self):        
        inputs = []
        outputs = []
        bindings = []
        stream = cuda.Stream()
        
        for binding in self.engine:
            size = trt.volume(self.engine.get_binding_shape(binding))
            dtype = trt.nptype(self.engine.get_binding_dtype(binding))
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)

            bindings.append(int(device_mem))

            if self.engine.binding_is_input(binding):
                inputs.append({"host": host_mem, "device": device_mem})
            else:
                outputs.append({"host": host_mem, "device": device_mem})

        return inputs, outputs, bindings, stream

    def _warmup(self):
        image = np.ones((1, 3, self.image_size[0], self.image_size[1]))
        image = np.ascontiguousarray(image, dtype=np.float32)
        [self._inference(image) for _ in range(2)]

    def _inference(self, image):
        self.inputs[0]["host"] = np.ravel(image)

        for input_ in self.inputs:
            cuda.memcpy_htod_async(input_["device"], input_["host"], self.stream)

        self.context.execute_async_v2(
            bindings=self.bindings, stream_handle=self.stream.handle
        )

        for output in self.outputs:
            cuda.memcpy_dtoh_async(output["host"], output["device"], self.stream)

        self.stream.synchronize()

        return list(map(lambda x: x["host"], self.outputs))
    
    def inference(self, image):
        try:
            return self._inference(image)
        except Exception as e:
            print(e)
            return []

    def detect(self, image):

        self.cfx.push()
        inference_results = self.inference(image)
        self.cfx.pop()

        if not inference_results:
            return []

        predictions = np.reshape(inference_results, (1, -1, int(5 + self.n_classes)))[0]
        detections = self._post_processing(predictions, ratio = self._ratio)
        return list(filter(lambda x: x.get("confidence") >= self._confidence, detections))

    def _post_processing(self, predictions, ratio):
        boxes = predictions[:, 0:4]
        confidences = predictions[:, 4:5]
        scores = confidences * predictions[:, 5:]
        
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = (boxes[:, 0] - boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2.0) * ratio[1]
        boxes_xyxy[:, 2] = (boxes[:, 0] + boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 3] = (boxes[:, 1] + boxes[:, 3] / 2.0) * ratio[1]

        detections = self.multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)

        get_reformatted_detections = lambda x: {"class": self._labels[int(x[5])], "bounding_box": [int(x[0]), int(x[1]), int(x[2]), int(x[3])], "confidence": x[4]}
        
        return list(map(get_reformatted_detections, detections))

    # @numba.njit
    def nms(self, boxes, scores, nms_thr):
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        indices = scores.argsort()[::-1]

        keep = []
        while indices.size > 0:
            i = indices[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[indices[1:]])
            yy1 = np.maximum(y1[i], y1[indices[1:]])
            xx2 = np.minimum(x2[i], x2[indices[1:]])
            yy2 = np.minimum(y2[i], y2[indices[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)

            inter = w * h
            ovr = inter / (areas[i] + areas[indices[1:]] - inter)

            inds = np.where(ovr <= nms_thr)[0]
            indices = indices[inds + 1]

        return keep

    # @numba.njit
    def multiclass_nms(self, boxes, scores, nms_thr, score_thr):
        """Multiclass NMS implemented in Numpy"""
        final_dets = []

        for cls_ind in range(scores.shape[1]):
            cls_scores = scores[:, cls_ind]
            valid_score_mask = cls_scores > score_thr
            
            if valid_score_mask.sum() == 0:
                continue

            valid_scores = cls_scores[valid_score_mask]
            valid_boxes = boxes[valid_score_mask]

            keep = self.nms(valid_boxes, valid_scores, nms_thr)

            if len(keep) > 0:
                cls_inds = np.ones((len(keep), 1)) * cls_ind
                
                dets = np.concatenate(
                    [valid_boxes[keep], valid_scores[keep, None], cls_inds], 1
                )
                
                final_dets.append(dets)

        if not final_dets:
            return []
            
        return np.concatenate(final_dets, 0)


    def __repr__(self):
        return "< YoloV5Detector >"

    def __del__(self):
        self.cfx.pop()

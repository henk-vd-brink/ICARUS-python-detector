import abc
import logging
import time
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda

logger = logging.getLogger(__name__)

from ...utils import timer


class AbstractDetector(abc.ABC):
    @abc.abstractmethod
    def detect(self, image):
        pass


class YoloV5Detector(AbstractDetector):
    def __init__(self, config={}):

        self._ratio = config.get("ratio")
        self._confidence = config.get("confidence")
        self._labels = config.get("labels")

        self._nms_config = config.get("nms_config", dict())

        self.logger = trt.Logger()

        self.max_batch_size = config.get("max_batch_size", 1)
        self.dtype = config.get("dtype", np.float16)
        self.image_size = config.get("image_size", (640, 640))
        self.n_classes = config.get("n_classes", 80)

        self.trt_runtime = trt.Runtime(self.logger)
        self.cfx = cuda.Device(0).make_context()

        self.engine = self._load_engine_from_path(
            self.trt_runtime, config.get("engine_path")
        )

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

        with open(engine_path, "rb") as f:
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
            host_memory = cuda.pagelocked_empty(size, dtype)
            device_memory = cuda.mem_alloc(host_memory.nbytes)

            bindings.append(int(device_memory))

            if self.engine.binding_is_input(binding):
                inputs.append({"host": host_memory, "device": device_memory})
            else:
                outputs.append({"host": host_memory, "device": device_memory})

        return inputs, outputs, bindings, stream

    def _warmup(self):
        image = np.ones((1, 3, *self.image_size))
        image = np.ascontiguousarray(image, dtype=np.float32)
        [self._inference(image) for _ in range(20)]

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

    @timer
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
        detections = self._post_processing(predictions, ratio=self._ratio)

        return list(
            filter(lambda x: x.get("confidence") >= self._confidence, detections)
        )

    def _get_reformatted_detection_from_detection(self, detection):
        return {
            "label": self._labels[int(detection[5])],
            "bounding_box": [
                int(detection[0]),
                int(detection[1]),
                int(detection[2]),
                int(detection[3]),
            ],
            "confidence": detection[4],
        }

    def _post_processing(self, predictions, ratio):
        boxes = predictions[:, 0:4]
        confidences = predictions[:, 4:5]
        scores = confidences * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = (boxes[:, 0] - boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2.0) * ratio[1]
        boxes_xyxy[:, 2] = (boxes[:, 0] + boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 3] = (boxes[:, 1] + boxes[:, 3] / 2.0) * ratio[1]

        detections = self.multiclass_nms(boxes_xyxy, scores)

        return list(map(self._get_reformatted_detection_from_detection, detections))

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

    def multiclass_nms(self, boxes, scores):
        """Multiclass NMS implemented in Numpy"""
        nms_threshold = self._nms_config.get("nms_threshold", 0.45)
        score_threshold = self._nms_config.get("score_threshold", 0.1)

        final_dets = []

        for label_index in range(scores.shape[1]):
            label_scores = scores[:, label_index]
            valid_score_mask = label_scores > score_threshold

            if valid_score_mask.sum() == 0:
                continue

            valid_scores = label_scores[valid_score_mask]
            valid_boxes = boxes[valid_score_mask]

            keep = self.nms(valid_boxes, valid_scores, nms_threshold)

            if len(keep) > 0:
                label_indexs = np.ones((len(keep), 1)) * label_index

                dets = np.concatenate(
                    [valid_boxes[keep], valid_scores[keep, None], label_indexs], 1
                )

                final_dets.append(dets)

        if not final_dets:
            return []

        return np.concatenate(final_dets, 0)

    def __repr__(self):
        return "< YoloV5Detector >"

    def __del__(self):
        self.cfx.pop()

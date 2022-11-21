import abc
import logging
import torch
import numpy as np
import cv2
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
        [self._inference(image) for _ in range(1)]

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

    def detect(self, data):
        image = data.image

        self.cfx.push()
        inference_results = self.inference(image)
        self.cfx.pop()

        predictions = np.reshape(inference_results, (1, -1, int(5 + self.n_classes)))[0]
        boxes, confidences, labels = self._post_processing(predictions)

        for i in range(len(labels)):
            try:

                label = labels[i]
                print(label)

                if label != 1:
                    continue

                box = boxes[i, :]
                x_1, y_1, x_2, y_2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                cv2.rectangle(data.raw_image, (x_1, y_1), (x_2, y_2), (255, 0, 0), 5)
            except Exception as e:

                pass

        cv2.imwrite("/home/docker_user/assets/joe.png", data.raw_image)
        return data

    def _post_processing(self, predictions, ratio = (1.796875, 1.09375)):
        boxes = predictions[:, 0:4] # x,y,w,h
        confidences = predictions[:, 4:5]
        
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = (boxes[:, 0] - boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2.0) * ratio[1]
        boxes_xyxy[:, 2] = (boxes[:, 0] + boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 3] = (boxes[:, 1] + boxes[:, 3] / 2.0) * ratio[1]

        labels = np.argmax(predictions[5:], axis=1)

        return boxes_xyxy, confidences, labels


    def __repr__(self):
        return "< YoloV5Detector >"

    def __del__(self):
        self.cfx.pop()

import logging
import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
from abc import ABC, abstractmethod

from .nms import multiclass_nms

logger = logging.getLogger(__name__)


class AbstractDetector(ABC):
    @abstractmethod
    def detect(self, image):
        pass


class YoloV5Detector(AbstractDetector):
    def __init__(
        self,
        ratio,
        confidence,
        labels,
        engine_path,
        max_batch_size=1,
        dtype=np.float16,
        image_size=(640, 640),
        n_classes=80,
    ):

        self._ratio = ratio
        self._confidence = confidence
        self._labels = labels

        self.logger = trt.Logger()

        self.max_batch_size = max_batch_size
        self.dtype = dtype
        self.image_size = image_size
        self.n_classes = n_classes

        engine_path = engine_path

        self.trt_runtime = trt.Runtime(self.logger)
        self.cfx = cuda.Device(0).make_context()

        self.engine = self._load_engine_from_path(self.trt_runtime, engine_path)

        self.context = self.engine.create_execution_context()

        self.inputs, self.outputs, self.bindings, self.stream = self._allocate_buffers()

        self._check_initialization()

        self._warmup()

    @classmethod
    def from_dict(cls, input_dict):
        ratio = input_dict.get("ratio")
        confidence = input_dict.get("confidence")
        labels = input_dict.get("labels")

        engine_path = input_dict.get("engine_path")
        return cls(
            ratio=ratio, confidence=confidence, labels=labels, engine_path=engine_path
        )

    def _load_engine_from_path(self, trt_runtime, engine_path):
        trt.init_libnvinfer_plugins(self.logger, "")

        with open(engine_path, "rb") as f:
            engine_data = f.read()

        return trt_runtime.deserialize_cuda_engine(engine_data)

    def _check_initialization(self):
        if len(self.inputs) < 0:
            raise Exception("Error inputs TensorRT")

        if len(self.outputs) < 0:
            raise Exception("Error outputs TensorRT")

        if len(self.bindings) < 0:
            raise Exception("Error bindings TensorRT")

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

    def _post_processing(self, predictions, ratio):
        boxes = predictions[:, 0:4]
        confidences = predictions[:, 4:5]
        scores = confidences * predictions[:, 5:]

        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = (boxes[:, 0] - boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 1] = (boxes[:, 1] - boxes[:, 3] / 2.0) * ratio[1]
        boxes_xyxy[:, 2] = (boxes[:, 0] + boxes[:, 2] / 2.0) * ratio[0]
        boxes_xyxy[:, 3] = (boxes[:, 1] + boxes[:, 3] / 2.0) * ratio[1]

        detections = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.1)

        get_reformatted_detections = lambda x: {
            "label": self._labels[int(x[5])],
            "bounding_box": [int(x[0]), int(x[1]), int(x[2]), int(x[3])],
            "confidence": x[4],
        }
        return list(map(get_reformatted_detections, detections))

    def __del__(self):
        self.cfx.pop()

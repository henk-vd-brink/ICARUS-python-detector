import abc
import logging
import torch

logger = logging.getLogger(__name__)

class AbstractDetector(abc.ABC):
    pass


class FakeDetector(AbstractDetector):
    
    inference_results = [{"class": "person", "bounding_box": [0.1, 0.2, 0.3, 0.4], "confidence": 0.67}]

    def detect(self, data):
        data.inference_results = self.inference_results
        return data

    def __repr__(self):
        return "< FakeDetector >"


class YoloV5Detector(AbstractDetector):

    def __init__(self):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

    def detect(self, data):
        results = model(data.image)
        results.print()

        return data

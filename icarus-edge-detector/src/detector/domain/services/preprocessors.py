import abc
import cv2
import logging

import numpy as np

logger = logging.getLogger(__name__)

class AbstractPreprocessor(abc.ABC):
    def __init__(self, config = {}):
        self._config = config

    def preprocess(self, data):
        logger.info("Preprocessing frame")
        return self._preprocess(data)

    @abc.abstractmethod
    def _preprocess(self, data):
        pass


class FakePreprocessor(AbstractPreprocessor):

    def _preprocess(self, data):
        print(frame)
        return frame


    def __repr__(self):
        return "< FakePreprocessor >"


class YoloV5Preprocessor(AbstractPreprocessor):
    def __init__(self, config={}):
        super().__init__(config)

        self._parse_config(config)
        
    def _parse_config(self, config):
        self._desired_image_width = config.get("desired_image_width", 416)
        self._desired_image_height = config.get("desired_image_height", 416)

    def _preprocess(self, data):
        data.image = data.raw_image
        return data

    def __repr__(self):
        return "< YoloV5Preprocessor >"
import abc
import cv2
import logging

import numpy as np

logger = logging.getLogger(__name__)


class AbstractPreprocessor(abc.ABC):
    def __init__(self, config={}):
        self._config = config

    def preprocess(self, data):
        return self._preprocess(data)

    @abc.abstractmethod
    def _preprocess(self, data):
        pass


class YoloV5Preprocessor(AbstractPreprocessor):
    def __init__(self, config={}):
        super().__init__(config)

        self._parse_config(config)

    def _parse_config(self, config):
        self._desired_image_width = config.get("desired_image_width", 640)
        self._desired_image_height = config.get("desired_image_height", 640)

    def _preprocess(self, image):
        new_image_resolution = (self._desired_image_width, self._desired_image_height)

        image = cv2.resize(
            image, new_image_resolution, interpolation=cv2.INTER_AREA
        ).astype(np.float32)

        image /= 255.0
        image = np.moveaxis(image, -1, 0)
        return image[np.newaxis]

    def __repr__(self):
        return "< YoloV5Preprocessor >"

import cv2
import logging
import numpy as np
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class Preprocessor(ABC):
    @abstractmethod
    def preprocess(self, image):
        return self._preprocess(image)


class YoloV5Preprocessor(Preprocessor):
    def __init__(self, desired_image_width=640, desired_image_height=640):
        self._desired_image_width = desired_image_width
        self._desired_image_height = desired_image_height

    def preprocess(self, image):
        new_image_resolution = (self._desired_image_width, self._desired_image_height)

        image = cv2.resize(
            image, new_image_resolution, interpolation=cv2.INTER_AREA
        ).astype(np.float32)

        image /= 255.0
        image = np.moveaxis(image, -1, 0)
        return image[np.newaxis]

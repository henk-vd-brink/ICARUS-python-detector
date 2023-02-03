import cv2
import numpy as np
from abc import ABC, abstractmethod


class Preprocessor(ABC):
    @abstractmethod
    def __call__(self, image: np.ndarray) -> np.ndarray:
        pass


class YoloV5Preprocessor(Preprocessor):
    def __init__(
        self, desired_image_width: int = 640, desired_image_height: int = 640
    ) -> None:
        self._desired_image_width = desired_image_width
        self._desired_image_height = desired_image_height

    def __call__(self, image: np.ndarray) -> np.ndarray:
        new_image_resolution = (self._desired_image_width, self._desired_image_height)

        image = cv2.resize(
            image, new_image_resolution, interpolation=cv2.INTER_AREA
        ).astype(np.float32)

        image /= 255.0
        image = np.moveaxis(image, -1, 0)
        return image[np.newaxis]

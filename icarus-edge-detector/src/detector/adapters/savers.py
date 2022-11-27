import abc
import os
import cv2
import logging
import numpy as np

logger = logging.getLogger(__name__)


class AbstractSaver(abc.ABC):
    def __init__(self, config={}):
        self._config = config


class FileSystemSaver(AbstractSaver):
    def __init__(self, config={}):
        super().__init__(config)

        self._parse_config(config)

    def _parse_config(self, config):
        self._base_path = config.get("base_path", "/dev/shm")

        if not os.path.exists(self._base_path):
            os.mkdir(self._base_path)

    def save_file(self, file_name, file_bytes):
        try:
            self._save_file(file_name, file_bytes)
        except Exception as e:
            logger.exception(e)

    def _save_file(self, file_name, file_bytes):
        with open(self._base_path + "/" + file_name, "wb") as file:
            file.write(file_bytes)

    @staticmethod
    def encode_image(image, encoding="jpg"):
        if not isinstance(image, np.ndarray):
            raise TypeError(f"Cannot encode image of type: {type(image)}")

        image_bytes = cv2.imencode("." + encoding, image)
        return image_bytes

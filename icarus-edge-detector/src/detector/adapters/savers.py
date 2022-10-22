import cv2
import numpy as np


class FileSystemSaver:
    def __init__(self, config = {}):
        self._config = config
        self._parse_config(config)

    def _parse_config(self, config):
        self._base_path = self._config.get("base_path", "/home/docker_user/data/")

    def save_file(self, file_name, file_bytes):
        try:
            self._save_file(file_name, file_bytes)
        except Exception:
            pass

    def _save_file(self, file_name, file_bytes):
        with open(self._base_path + file_name, "wb") as file:
            file.write(file_bytes)

    @staticmethod
    def encode_image(image, encoding="png"):
        if not isinstance(image, np.ndarray):
            raise TypeError(f"Cannot encode image of type: {type(image)}")

        image_bytes = cv2.imencode("." + encoding, image)
        return image_bytes
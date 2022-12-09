import abc
import os
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

    def save_image(self, image_uuid, image, encoding):
        try:
            if encoding == "npy":
                self._save_image_as_npy(image_uuid, image)
            else:
                raise Exception("wrong encoding")
        except Exception as e:
            logger.exception(e)

    def _save_image_as_npy(self, image_uuid, image):
        with open(self._base_path + "/" + image_uuid + ".npy", "wb") as file:
            np.save(file, image)

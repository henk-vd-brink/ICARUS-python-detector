import cv2
import uuid
import datetime
import numpy as np

from dataclasses import field, dataclass, asdict

@dataclass
class Data:
    raw_image: np.ndarray
    image: np.ndarray
    meta_data: dict
    inference_results: list = field(default_factory=lambda: [])

class Processor:
    def __init__(self, handlers):
        self._handlers = handlers

    def _get_timestamp(self):
        return datetime.datetime.now().isoformat()

    def _get_image_uuid(self):
        return str(uuid.uuid4())

    def _initialise_data_from_image(self, raw_image):
        meta_data = {
            "timestamp": self._get_timestamp(),
            "uuid": self._get_image_uuid()
        }

        return Data(raw_image=raw_image, image=raw_image.copy(), meta_data=meta_data)

    def handle_image(self, image):
        data = self._initialise_data_from_image(image)

        data = self._handlers.preprocess_data(data)
        data = self._handlers.detect(data)
        data = self._handlers.postprocess_data(data)

        self._handlers.store_image_on_file_system(data)
        self._handlers.send_stored_image_on_file_system_event_to_bus(data)
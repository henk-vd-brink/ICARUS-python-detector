import cv2
import uuid
import datetime
import time
import logging
import numpy as np

from dataclasses import field, dataclass, asdict

logger = logging.getLogger(__name__)

class Processor:
    def __init__(self, handlers):
        self._handlers = handlers

    def _get_meta_data(self):
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "uuid": str(uuid.uuid4())
        }

    def handle_image(self, image):
        meta_data = self._get_meta_data()        

        batch = self._handlers.preprocess_data(image)

        t_0 = time.perf_counter()
        detections = self._handlers.detect(batch)

        print("Number of dets: ", len(detections), " Detection time: ", time.perf_counter() - t_0)

        detections = list(filter(lambda x: x.get("class") == "person", detections))

        if not detections:
            return

        detection_results = dict(meta_data = meta_data, detections = detections)

        self._handlers.store_image_on_file_system(dict(meta_data=meta_data, image=image))
        self._handlers.send_stored_image_on_file_system_event_to_bus(detection_results)
import logging
from ..domain import models


class Flow:
    def __init__(self, handlers, config={}):
        self._handlers = handlers
        self._config = config

        self._logger = logging.getLogger("Flow")

    def _create_frame_from_image(self, image):
        return models.Frame.from_image(image)

    def handle_image(self, image):
        frame = self._create_frame_from_image(image)

        self._handlers.run_inference(frame)

        self._handlers.send_meta_data_to_remote(frame)

        self._handlers.send_image_to_remote(frame)

        self._logger.info("Detections: %s", frame.detections)
        
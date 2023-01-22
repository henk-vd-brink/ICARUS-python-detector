import logging

from ..domain import models

logger = logging.getLogger(__name__)


class Flow:
    def __init__(self, handlers, config={}):
        self._handlers = handlers
        self._config = config

    def _create_frame_from_image(self, image):
        return models.Frame.from_image(image)

    def handle_image(self, image):
        frame = self._create_frame_from_image(image)

        self._handlers.add_detections_to_frame(frame)

        self._handlers.send_meta_data_to_remote(frame)

        self._handlers.send_image_to_remote(frame)

import logging

from ..domain import models

logger = logging.getLogger(__name__)


class Flow:
    def __init__(self, handlers, filter_pipeline, config={}):
        self._handlers = handlers
        self._config = config
        self.filter_pipeline = filter_pipeline

    def _create_frame_from_image(self, image):
        return models.Frame.from_image(image)

    def _filter(self, frame):
        for filter in self.filter_pipeline:
            if filter.filter(frame):
                continue
            return False
        return True

    def handle_image(self, image):
        frame = self._create_frame_from_image(image)

        self._handlers.add_detections_to_frame(frame)

        self._handlers.send_meta_data_to_remote(frame)

        self._handlers.send_image_to_remote(frame)

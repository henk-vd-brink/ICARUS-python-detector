import datetime
import logging


class Processor:
    def __init__(self, handlers, config={}):
        self._handlers = handlers
        self._config = config

        self._logger = logging.getLogger(__name__)

    def _get_meta_data(self):
        timestamp = datetime.datetime.now()
        return {
            "timestamp": timestamp.isoformat(),
            "uuid": timestamp.strftime("%Y-%m-%d-%H-%M-%S-%f"),
        }

    def handle_image(self, image):
        meta_data = self._get_meta_data()

        batch = self._handlers.preprocess_data(image)

        detections = self._handlers.detect(batch)

        # detections = list(filter(lambda x: x.get("label") == "person", detections))

        if not detections:
            return

        detection_results = dict(meta_data=meta_data, detections=detections)

        self._handlers.store_image_on_file_system(
            dict(meta_data=meta_data, image=image)
        )

        self._handlers.send_stored_image_on_file_system_event_to_bus(detection_results)

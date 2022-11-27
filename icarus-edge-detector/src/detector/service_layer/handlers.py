import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


def preprocess_data(image, preprocessor):
    return preprocessor.preprocess(image)


def detect(image, detector):
    return detector.detect(image)


def store_image_on_file_system(input_dict, file_saver, encoding="jpg") -> None:
    file_name = input_dict["meta_data"].get("uuid") + "." + encoding
    image = input_dict["image"]

    _, file_bytes = file_saver.encode_image(image, encoding=encoding)
    file_saver.save_file(file_name, file_bytes)


def send_stored_image_on_file_system_event_to_bus(input_dict, mq_client) -> None:
    uuid = input_dict["meta_data"].get("uuid")
    timestamp = input_dict["meta_data"].get("timestamp")
    inference_results = input_dict["detections"]

    message = dict(
        timestamp=timestamp,
        uuid=uuid,
        file_name=uuid + ".jpg",
        inference_results=inference_results,
    )

    mq_client.publish("test", message)

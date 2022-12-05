import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


def preprocess_data(image, preprocessor):
    return preprocessor.preprocess(image)


def detect(image, detector):
    return detector.detect(image)


def store_image_on_file_system(input_dict, file_saver) -> None:
    image_uuid = input_dict["meta_data"].get("uuid")
    image = input_dict["image"]

    file_saver.save_image(image_uuid, image, encoding="npy")


def send_stored_image_on_file_system_event_to_bus(input_dict, mq_client) -> None:
    uuid = input_dict["meta_data"].get("uuid")
    timestamp = input_dict["meta_data"].get("timestamp")
    inference_results = input_dict["detections"]

    message = dict(
        timestamp=timestamp,
        uuid=uuid,
        file_name=uuid + ".npy",
        inference_results=inference_results,
    )

    mq_client.publish("test", message)

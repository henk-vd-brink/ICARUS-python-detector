import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

def preprocess_data(data, preprocessor):
    return preprocessor.preprocess(data)

def detect(data, detector):
    return detector.detect(data)

def postprocess_data(data, postprocessor):
    return postprocessor.postprocess(data)

def store_image_on_file_system(data, file_saver, encoding="png") -> None:
    file_name = data.meta_data.get("uuid") + "." + encoding

    _, file_bytes = file_saver.encode_image(data.raw_image)
    file_saver.save_file(file_name, file_bytes)

def send_stored_image_on_file_system_event_to_redis(data, mq_client) -> None:
    uuid = data.meta_data.get("uuid")

    message = dict(
        timestamp = data.meta_data.get("timestamp"),
        uuid = uuid,
        file_name = uuid + ".png",
        inference_results = data.inference_results
    )

    mq_client.publish("test", message)


import redis
import pathlib
import json
import requests
import io
import logging
import warnings
import numpy as np
import cv2

warnings.filterwarnings(action="ignore", message="Unverified HTTPS request")

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

from .. import bootstrap

mq_client = bootstrap.bootstrap()
mq_client.connect()

red = redis.StrictRedis(
    "icarus-edge-redis", 6379, charset="utf-8", decode_responses=True
)


def get_file_bytes_from_file_name(file_name):
    try:
        with open("/dev/shm/" + file_name, "rb") as file:
            file_bytes = np.load(file)
    except Exception as e:
        logger.warning("Could not retrieve file bytes")
        logger.exception(e)
        file_bytes = bytes()
    return file_bytes


def send_file_from_file_name(uuid, file_name):
    _, buffer = cv2.imencode(".jpg", get_file_bytes_from_file_name(file_name))

    image_as_jpg_bytes = io.BytesIO(buffer)

    file_name_as_jpg = uuid + ".jpg"
    files = {"file": (file_name_as_jpg, image_as_jpg_bytes)}
    logger.info(file_name_as_jpg)

    try:
        response = requests.post(
            "https://192.168.178.47:8443/files", files=files, verify=False
        )
    except requests.ConnectionError as e:
        logger.exception(e)
        return 599

    return response.status_code


def delete_file_from_file_name(file_name):
    pathlib.Path("/dev/shm/" + file_name).unlink()


def redis_consumer():
    while True:

        if red.llen("test") == 0:
            continue

        data_from_message_as_dict = json.loads(red.rpop("test"))

        file_name = data_from_message_as_dict.get("file_name")
        uuid = data_from_message_as_dict.get("uuid")

        send_file_from_file_name(uuid, file_name)
        delete_file_from_file_name(file_name)

        inference_results = data_from_message_as_dict["inference_results"]

        message = dict(image_uuid=uuid, meta_data=[])
        for inference_result in inference_results:
            message["meta_data"].append(
                dict(
                    label=inference_result.get("label"),
                    x_1=inference_result.get("bounding_box")[0],
                    y_1=inference_result.get("bounding_box")[1],
                    x_2=inference_result.get("bounding_box")[2],
                    y_2=inference_result.get("bounding_box")[3],
                    confidence=inference_result.get("confidence"),
                )
            )

        mq_client.publish(routing_key="DetectedObjects", body=message)


if __name__ == "__main__":
    redis_consumer()

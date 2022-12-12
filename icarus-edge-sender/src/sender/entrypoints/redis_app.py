import json
import requests
import io
import logging
import warnings
import cv2

warnings.filterwarnings(action="ignore", message="Unverified HTTPS request")

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

from .. import bootstrap

bootstrap_dict = bootstrap.bootstrap()

mq_client = bootstrap_dict["mq_client"]
file_system_adapter = bootstrap_dict["file_system_adapter"]
sender_adapter = bootstrap_dict["sender_adapter"]
redis_client = bootstrap_dict["redis_mq_client"]


def send_file_from_file_name(uuid, file_name):
    file_bytes = file_system_adapter.get_file_bytes_from_file_name(file_name)

    try:
        _, buffer = cv2.imencode(".jpg", file_bytes)
    except Exception as e:
        logger.warning(e)
        return 599

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


def redis_consumer():
    redis_client.connect()
    mq_client.connect()

    while True:

        if redis_client.connection.llen("test") == 0:
            continue

        message_as_json = redis_client.connection.rpop("test")
        message_as_dict = json.loads(message_as_json)

        file_name = message_as_dict.get("file_name")
        uuid = message_as_dict.get("uuid")

        send_file_from_file_name(uuid, file_name)
        file_system_adapter.delete_file_bytes_from_file_name(file_name)

        inference_results = message_as_dict["inference_results"]

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

        mq_client.publish(topic="DetectedObjects", body=message)


if __name__ == "__main__":
    redis_consumer()

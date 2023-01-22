import logging
import json
import cv2
import io
import asyncio

from ..domain import models

logger = logging.getLogger(__name__)


def run_inference(frame, detector):
    detections = detector.detect(frame.image)
    frame.detections = detections


def send_image_to_remote(frame, file_sender):
    image_uuid = frame.uuid
    image_as_numpy_array = frame.image

    _, buffer = cv2.imencode(".jpg", image_as_numpy_array)
    file_bytes = io.BytesIO(buffer)
    file_name = image_uuid + ".jpg"

    loop = asyncio.get_event_loop()
    loop.run_in_executor(
        None, file_sender.send, file_name, file_bytes
    )  # Fire and forget


def send_meta_data_to_remote(frame, rabbitmq_client):
    message = models.Message.from_frame(frame)

    if not rabbitmq_client.channel.is_open:
        rabbitmq_client.connect()

    rabbitmq_client.channel.basic_publish(
        exchange="DetectedObjects",
        routing_key="DetectedObjects",
        body=json.dumps(message.asdict()),
    )

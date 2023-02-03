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


def send_meta_data_to_remote(frame, meta_data_sender):
    message = models.Message.from_frame(frame)

    message_as_json = json.dumps(message.asdict())

    meta_data_sender.send_meta_data(message_as_json)

    logger.info(message_as_json)

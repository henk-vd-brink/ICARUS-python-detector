import logging
import json
import cv2
import io
import asyncio

logger = logging.getLogger(__name__)


def add_detections_to_frame(frame, preprocessor, detector):
    batch = preprocessor.preprocess(frame.image)
    detections = detector.detect(batch)

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
    uuid = frame.uuid
    inference_results = frame.detections

    message_meta_data = list()
    for inference_result in inference_results:
        label = inference_result.get("label")
        x_1, y_1, x_2, y_2 = inference_result.get("bounding_box")
        confidence = inference_result.get("confidence")

        message_meta_data.append(
            dict(
                label=label,
                x_1=x_1,
                y_1=y_1,
                x_2=x_2,
                y_2=y_2,
                confidence=confidence,
            )
        )

    message = dict(
        image_uuid=uuid,
        meta_data=message_meta_data,
    )

    with rabbitmq_client:
        rabbitmq_client.basic_publish(
            exchange="DetectedObjects",
            routing_key="DetectedObjects",
            body=json.dumps(message),
        )

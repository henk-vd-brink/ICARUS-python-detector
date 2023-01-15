import cv2
import os
import logging
import numpy as np


logging.basicConfig(level=logging.INFO)

VIDEO_HEIGHT = int(os.environ.get("VIDEO_OUTPUT_HEIGHT", 3496))
VIDEO_WIDTH = int(os.environ.get("VIDEO_OUTPUT_WIDTH", 4656))
VIDEO_FRAMERATE = int(os.environ.get("VIDEO_OUTPUT_FRAMERATE", 10))

DETECTOR_IMAGE_HEIGHT = int(os.environ.get("DETECTOR_IMAGE_HEIGHT", 640))
DETECTOR_IMAGE_WIDTH = int(os.environ.get("DETECTOR_IMAGE_WIDTH", 640))


def get_video_capture_config():
    input_caps = (
        "v4l2src device=/dev/video0 "
        f"! image/jpeg,height={VIDEO_HEIGHT},width={VIDEO_WIDTH},framerate={VIDEO_FRAMERATE}/1 "
        "! jpegparse "
        "! nvv4l2decoder mjpeg=1 "
        "! nvvidconv "
        "! video/x-raw,format=BGRx "
        "! videoconvert "
        "! video/x-raw,format=BGR "
        "! appsink drop=1"
    )
    return dict(input_caps=(input_caps, cv2.CAP_GSTREAMER))


def get_labels_from_txt_file(file_path):
    with open(file_path, "r") as f:
        labels = f.readlines()
    return [label.replace("\n", "") for label in labels]


def get_yolo_v5_detector_config():
    ratio = (VIDEO_WIDTH / DETECTOR_IMAGE_WIDTH, VIDEO_HEIGHT / DETECTOR_IMAGE_HEIGHT)
    labels = get_labels_from_txt_file("/home/docker_user/assets/coco_labels.txt")

    return dict(
        engine_path="/home/docker_user/assets/yolov5n.trt",
        max_batch_size=1,
        dtype=np.float16,
        confidence=0.6,
        image_size=(DETECTOR_IMAGE_WIDTH, DETECTOR_IMAGE_HEIGHT),
        n_classes=len(labels),
        ratio=ratio,
        labels=labels,
        nms_config=dict(nms_threshold=0.45, score_threshold=0.1),
    )


def get_rabbitmq_client_config():
    return dict(
        broker_ip_address=os.environ.get("REMOTE_IP_ADDRESS"),
        broker_port=os.environ.get("REMOTE_RABBITMQ_PORT"),
        broker_username=os.environ.get("REMOTE_RABBITMQ_USERNAME"),
        broker_password=os.environ.get("REMOTE_RABBITMQ_PASSWORD"),
    )


def get_file_sender_config():
    return dict(
        remote_ip_address=os.environ.get("REMOTE_IP_ADDRESS"),
        remote_port=os.environ.get("REMOTE_PORT"),
        auth=None,
    )

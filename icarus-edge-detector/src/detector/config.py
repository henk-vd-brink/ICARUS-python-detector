import cv2
import logging
import numpy as np

logger = logging.getLogger(__name__)

def get_video_capture_config():
    input_caps = (
        "v4l2src device=/dev/video0 io-mode=2 "
        "! image/jpeg,height=1080,width=1920 "
        "! nvv4l2decoder mjpeg=1 "
        "! nvvidconv "
        "! video/x-raw,format=BGRx "
        "! videoconvert "
        "! video/x-raw,format=BGR "
        "! appsink drop=1"
    )
    return dict(input_caps=(input_caps, cv2.CAP_GSTREAMER))


def get_labels_from_txt_file(file_path="/home/docker_user/assets/coco_labels.txt"):
    with open(file_path, "r") as f:
        labels = f.readlines()

    logger.info("Loaded labels, found %s labels", len(labels))

    return [l.replace("\n", "") for l in labels]


def get_mq_config():
    return dict(host="icarus-edge-redis")


def get_yolo_v5_detector_config():
    return {
        "engine_path": "/home/docker_user/assets/yolov5n.trt",
        "max_batch_size": 1,
        "dtype": np.float16,
        "confidence": 0.6,
        "image_size": (640, 640),
        "n_classes": 80,
        "ratio": (3, 1.6875),
        "labels": get_labels_from_txt_file(),
    }

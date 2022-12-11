import cv2
import os
import logging
import numpy as np

logger = logging.getLogger(__name__)


def get_desired_video_configuration():
    video_height = int(os.environ.get("VIDEO_OUTPUT_HEIGHT", 2160))
    video_width = int(os.environ.get("VIDEO_OUTPUT_WIDTH", 3840))
    video_framerate = int(os.environ.get("VIDEO_OUTPUT_FRAMERATE", 10))

    detector_image_height = int(os.environ.get("DETECTOR_IMAGE_HEIGHT", 640))
    detector_image_width = int(os.environ.get("DETECTOR_IMAGE_WIDTH", 640))

    ratio = (video_width / detector_image_width, video_height / detector_image_height)

    return (
        video_height,
        video_width,
        video_framerate,
        ratio,
        detector_image_height,
        detector_image_width,
    )


def get_video_capture_config():
    height, width, framerate, *_ = get_desired_video_configuration()

    input_caps = (
        "v4l2src device=/dev/video0 io-mode=2 "
        f"! image/jpeg,height={height},width={width},framerate={framerate}/1 "
        "! jpegparse "
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
    return [label.replace("\n", "") for label in labels]


def get_mq_config():
    return dict(host="icarus-edge-redis")


def get_yolo_v5_detector_config():
    (
        _,
        _,
        _,
        ratio,
        detector_image_height,
        detector_image_width,
    ) = get_desired_video_configuration()

    return dict(
        engine_path="/home/docker_user/assets/yolov5n.trt",
        max_batch_size=1,
        dtype=np.float16,
        confidence=0.6,
        image_size=(detector_image_width, detector_image_height),
        n_classes=80,
        ratio=ratio,
        labels=get_labels_from_txt_file(),
        nms_config=dict(nms_threshold=0.45, score_threshold=0.1),
    )

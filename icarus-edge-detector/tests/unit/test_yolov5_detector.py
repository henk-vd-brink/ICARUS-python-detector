import os
import cv2
import numpy as np
from detector.domain.services import detectors

def get_test_image(image_path="/home/docker_user/tests/assets/test_image.jpg"):
    image = cv2.imread(image_path, 0)
    resized_image = cv2.resize(image, (640, 640), interpolation = cv2.INTER_AREA)
    return np.ascontiguousarray(resized_image, dtype=np.float32)

yolo_v5_detector_config = {"engine_path": "/home/docker_user/assets/yolov5n.trt", 
"max_batch_size": 1, "dtype": np.float32, "confidence": 0.8, "image_size": (640, 640), "n_classes": 80}

def test_can_instantiate_yolo_v5_detector():
    detector = detectors.YoloV5Detector(config=yolo_v5_detector_config)
    
    assert isinstance(detector, detectors.AbstractDetector)

def test_can_get_image():
    assert isinstance(get_test_image(), np.ndarray)

def test_can_detect_anything_on_preprocessed_test_image():
    detector = detectors.YoloV5Detector(config=yolo_v5_detector_config)

    image = get_test_image()

    inference_results = detector.detect(image)
    assert False







import os
import cv2
import numpy as np
from detector.domain.services import detectors

class FakeData:
    pass

def get_test_image(image_path="/home/docker_user/tests/assets/test_image.jpg"):
    raw_image = cv2.imread(image_path)
    image = cv2.resize(raw_image.copy(), (640, 640), interpolation = cv2.INTER_AREA).astype(np.float16)
    image /= 255.0  
    image = np.moveaxis(image, -1, 0)        
    batch = image[np.newaxis]
    return raw_image, batch

yolo_v5_detector_config = {"engine_path": "/home/docker_user/assets/yolov5n.trt", 
"max_batch_size": 1, "dtype": np.float16, "confidence": 0.8, "image_size": (640, 640), "n_classes": 80}

# def test_can_instantiate_yolo_v5_detector():
#     detector = detectors.YoloV5Detector(config=yolo_v5_detector_config)
    
#     assert isinstance(detector, detectors.AbstractDetector)

def test_can_get_image():
    raw_image, image = get_test_image()

    assert isinstance(raw_image, np.ndarray)
    assert isinstance(image, np.ndarray)

def test_can_detect_anything_on_preprocessed_test_image():
    detector = detectors.YoloV5Detector(config=yolo_v5_detector_config)

    raw_image, image = get_test_image()

    fake_data = FakeData()
    fake_data.raw_image = raw_image
    fake_data.image = image


    inference_results = detector.detect(fake_data)
    assert False







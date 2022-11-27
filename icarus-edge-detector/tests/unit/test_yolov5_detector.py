import os
import cv2
import time
import pickle
import numpy as np
from detector.domain.services import detectors


class FakeData:
    pass


def get_labels_from_txt_file(file_path="/home/docker_user/assets/coco_labels.txt"):
    with open(file_path, "r") as f:
        labels = f.readlines()
    return labels


def get_test_image(image_path="/home/docker_user/tests/assets/test_image.jpg"):
    raw_image = cv2.imread(image_path)
    image = cv2.resize(
        raw_image.copy(), (640, 640), interpolation=cv2.INTER_AREA
    ).astype(np.float32)
    image /= 255.0
    image = np.moveaxis(image, -1, 0)
    batch = image[np.newaxis]
    return raw_image, batch


def load_pickled_numpy_object(file_path=""):
    with open(file_path, "rb") as f:
        numpy_object = pickle.load(f)
    return numpy_object


yolo_v5_detector_config = {
    "engine_path": "/home/docker_user/assets/yolov5n.trt",
    "max_batch_size": 1,
    "dtype": np.float16,
    "confidence": 0.8,
    "image_size": (640, 640),
    "n_classes": 80,
    "ratio": (1.796875, 1.09375),
    "labels": get_labels_from_txt_file(),
}

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

    t_0 = time.perf_counter()
    data = detector.detect(fake_data)
    print(time.perf_counter() - t_0)

    detections = data.inference_results

    for i in range(len(detections)):
        try:
            box = detections[i].get("bounding_box")
            cv2.rectangle(
                data.raw_image, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 5
            )
        except Exception as e:
            print(e)
            pass

        cv2.imwrite("/home/docker_user/assets/joe.png", data.raw_image)
    assert False


# def test_multiclass_nms():
#     detector = detectors.YoloV5Detector(config=yolo_v5_detector_config)

#     raw_image, image = get_test_image()

#     fake_data = FakeData()
#     fake_data.raw_image = raw_image
#     fake_data.image = image

#     boxes = load_pickled_numpy_object("/home/docker_user/assets/boxes_xyxy.pkl")
#     scores = load_pickled_numpy_object("/home/docker_user/assets/scores.pkl")

#     for _ in range(10):
#         t_0 = time.perf_counter()
#         detector.multiclass_nms(boxes, scores, nms_thr=0.45, score_thr=0.1 )
#         print(time.perf_counter() - t_0)

#     assert False

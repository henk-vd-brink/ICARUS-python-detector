import numpy as np


def get_input_caps():
    return 0

def get_labels_from_txt_file(file_path = "/home/docker_user/assets/coco_labels.txt"):
    with open(file_path, "r") as f:
        labels = f.readlines()
    return labels

def get_yolo_v5_detector_config():
    return {"engine_path": "/home/docker_user/assets/yolov5n.trt", 
"max_batch_size": 1, "dtype": np.float16, "confidence": 0.5, "image_size": (640, 640), "n_classes": 80, "ratio": (3, 1.6875), "labels": get_labels_from_txt_file()}
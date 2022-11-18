import numpy as np

def get_input_caps():
    return 0

def get_yolo_v5_detector_config():
    return {"engine_path": "/home/docker_user/assets/yolov5n.trt", 
"max_batch_size": 1, "dtype": np.float32, "confidence": 0.8, "image_size": (640, 640), "n_classes": 80}
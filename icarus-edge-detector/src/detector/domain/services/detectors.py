import abc
import logging
import torch
import numpy as np
import cv2
import torchvision
import torchvision.transforms as transforms

logger = logging.getLogger(__name__)

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

COLORS = np.random.uniform(0, 255, size=(len(COCO_INSTANCE_CATEGORY_NAMES), 3))

class AbstractDetector(abc.ABC):
    pass


class FakeDetector(AbstractDetector):
    
    inference_results = [{"class": "person", "bounding_box": [0.1, 0.2, 0.3, 0.4], "confidence": 0.67}]

    def detect(self, data):
        data.inference_results = self.inference_results
        return data

    def __repr__(self):
        return "< FakeDetector >"


class MobileNetV3Detector(AbstractDetector):

    def __init__(self):
        self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self._model = self._get_model(self._device)

        self._transform = transforms.Compose(
            [
                transforms.ToTensor(),
            ]
        )

    def _get_model(self, device):
        model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(pretrained=True)
        model = model.eval().to(device)
        return model

    def _draw_boxes_and_labels(self, boxes, classes, labels, image):
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
        for i, box in enumerate(boxes):
            color = COLORS[labels[i]]
            cv2.rectangle(
                image,
                (int(box[0]), int(box[1])),
                (int(box[2]), int(box[3])),
                color, 2
            )
            cv2.putText(image, classes[i], (int(box[0]), int(box[1]-5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, 
                        lineType=cv2.LINE_AA)
        return image

    def detect(self, data, detection_threshold=0.6):
        image = self._transform(data.image.copy()).to(self._device)
        image = image.unsqueeze(0)

        results = self._model(image)

        with torch.no_grad():
            outputs = self._model(image) 

        pred_scores = outputs[0]['scores'].detach().cpu().numpy()
        pred_bboxes = outputs[0]['boxes'].detach().cpu().numpy()

        boxes = pred_bboxes[pred_scores >= detection_threshold].astype(np.int32)
        labels = outputs[0]['labels'][:len(boxes)]

        pred_classes = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in labels.cpu().numpy()]
        
        image = self._draw_boxes_and_labels(boxes, pred_classes, labels, data.image)

        cv2.imwrite("/home/docker_user/assets/test.png", image)

        print(self._get_inference_results(boxes, pred_classes))

        return data

    def _get_inference_results(self, boxes, pred_classes):
        inference_results = []
        for i, box in enumerate(boxes):
            inference_result = {
                "class": pred_classes[i],
                "bounding_box": list(box)
            }
            inference_results.append(inference_result)
        return inference_results




    def __repr__(self):
        return "< MobileNetV3Detector >"

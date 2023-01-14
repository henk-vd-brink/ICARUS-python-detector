import cv2
from typing import Dict, Tuple, Any


class VideoCapture:
    def __init__(self, input_caps: Tuple[Any]) -> None:
        self._input_caps = input_caps

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> None:
        input_caps = input_dict["input_caps"]
        return cls(input_caps=input_caps)

    def __enter__(self) -> cv2.VideoCapture:
        self._cap = cv2.VideoCapture(*self._input_caps)
        return self._cap

    def __exit__(self, *_) -> None:
        self._cap.release()

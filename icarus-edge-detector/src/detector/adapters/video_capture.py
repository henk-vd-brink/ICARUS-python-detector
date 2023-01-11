import cv2


class VideoCapture:
    def __init__(self, input_caps):
        self._input_caps = input_caps

    @classmethod
    def from_dict(cls, input_dict):
        input_caps = input_dict.get("input_caps")
        return cls(input_caps=input_caps)

    def __enter__(self):
        self._cap = cv2.VideoCapture(*self._input_caps)
        return self._cap

    def __exit__(self, *_):
        self._cap.release()

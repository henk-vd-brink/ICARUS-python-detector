import cv2


class VideoCapture:
    def __init__(self, config={}):
        self._config = config

    def __enter__(self):
        input_caps = self._config.get("input_caps")
        self._cap = cv2.VideoCapture(*input_caps)
        return self._cap

    def __exit__(self, *args, **kwargs):
        self._cap.release()


class FakeVideoCapture:
    def __init__(self, path_to_image):
        self._image = cv2.imread(path_to_image)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def read(self):
        return True, self._image

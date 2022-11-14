import cv2

class VideoCapture():
    def __init__(self, config={}):
        self._config = config

    def __enter__(self):
        self._cap = cv2.VideoCapture(0)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
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


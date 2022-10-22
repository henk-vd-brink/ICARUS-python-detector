import cv2

class VideoCapture(cv2.VideoCapture):
    def __init__(self, *args, **kwargs):
        super(VideoCapture, self).__init__(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.release()


class FakeVideoCapture:
    def __init__(self, path_to_image="/home/docker_user/assets/test-livingroom.jpg"):
        self._image = cv2.imread(path_to_image)

    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs):
        pass

    def read(self):
        return True, self._image


import cv2

class VideoCapture(cv2.VideoCapture):
    def __init__(self, *args, **kwargs):
        super(VideoCapture, self).__init__(*args, **kwargs)

    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.release()
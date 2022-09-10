import cv2

class VideoCapture(cv2.VideoCapture):
    def __init__(self):
        super(VideoCapture, self).__init__(*args, **kwargs)      

    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.release()
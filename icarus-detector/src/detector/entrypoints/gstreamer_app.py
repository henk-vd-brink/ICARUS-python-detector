import cv2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .. import bootstrap

INPUT_CAPS = (
    """
    v4l2src device=/dev/video0 \
    ! video/x-raw, width=1920, height=1080 \
    ! decodebin \
    ! videoconvert \
    ! appsink sync=false \
    """,
    cv2.CAP_GSTREAMER
)


class VideoCapture(cv2.VideoCapture):
    def __init__(self, *args, **kwargs):
        super(VideoCapture, self).__init__(*args, **kwargs)      

    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.release()

bootstrap_dict = bootstrap.bootstrap()
bus = bootstrap_dict.get("bus")

def main():
    with VideoCapture(*INPUT_CAPS) as vc:
        while True:
            ret, image = vc.read()

            if not ret:
                break
            
            try:
                bus.handle_message("ReceivedImage", {"image": image})
            except Exception as e:
                logger.exception(e)

if __name__ == "__main__":
    main()
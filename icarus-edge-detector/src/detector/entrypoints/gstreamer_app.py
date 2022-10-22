import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .. import bootstrap

# INPUT_CAPS = (
#     "v4l2src device=/dev/video0"
#     "! video/x-raw, width=1920, height=1080"
#     "! decodebin"
#     "! videoconvert"
#     "! appsink sync=false",
#     cv2.CAP_GSTREAMER
# )



processor = bootstrap.bootstrap()

def main():
    frame = np.zeros((100,100,3))
    processor.handle_frame(frame)
    


if __name__ == "__main__":
    main()
import numpy as np
import logging
import time

from .. import bootstrap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

processor, video_capture = bootstrap.bootstrap()

def main():
    with video_capture as vc:
        while True:
            ret, image = vc.read()

            if not ret:
                break
                
            processor.handle_image(image)


if __name__ == "__main__":
    main()
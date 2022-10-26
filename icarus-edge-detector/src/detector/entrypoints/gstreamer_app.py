import numpy as np
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .. import bootstrap



processor, video_capture = bootstrap.bootstrap()

def main():
    
    with video_capture as vc:
        while True:
            ret, image = vc.read()

            if not ret:
                pass
                
            processor.handle_image(image)
        



if __name__ == "__main__":
    main()
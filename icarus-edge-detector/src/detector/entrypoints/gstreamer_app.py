import logging

from .. import bootstrap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

flow, video_capture = bootstrap.bootstrap()


def main(video_capture):
    while True:
        ret, image = video_capture.read()

        if not ret:
            logger.warning("Could not capture image, exiting..")
            break

        flow.handle_image(image)


if __name__ == "__main__":
    with video_capture as vc:
        main(vc)

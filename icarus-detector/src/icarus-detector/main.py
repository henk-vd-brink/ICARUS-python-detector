import cv2

from .core import pipeline_factory


def main(video_capture):
    process_pipeline_factory = pipeline_factory.PipelineFactory()
    process_pipeline = process_pipeline_factory.get_pipeline()

    process_pipeline.handle("joe!")

    # with video_capture as vc:
    #     while True:
    #         ret, frame = vc.read()
            
    #         if not ret:
    #             continue


if __name__ == "__main__":
    main(None)

import inspect
import queue
import logging

from . import config
from .adapters import video_capture as vc, savers, mq_clients
from .service_layer import handlers, processor
from .domain.services import preprocessors, detectors


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def inject_dependencies(function, dependencies):
    params = inspect.signature(function).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }

    return lambda input_params: function(input_params, **deps)


def inject_dependencies_into_handlers(handler_module, dependencies):
    functions = inspect.getmembers(handler_module, inspect.isfunction)

    for function in functions:
        function_name, function = function
        setattr(
            handler_module, function_name, inject_dependencies(function, dependencies)
        )


def bootstrap(
    preprocessor=preprocessors.YoloV5Preprocessor(),
    detector=detectors.YoloV5Detector(config.get_yolo_v5_detector_config()),
    video_capture=vc.VideoCapture(config.get_video_capture_config()),
    file_saver=savers.FileSystemSaver(),
    mq_client=mq_clients.RedisClient(config.get_mq_config()),
):

    mq_client.connect()

    logger.info(
        "Initialised APP \n --- \n"
        f"SELECTED preprocessor: {preprocessor}\n"
        f"SELECTED detector: {detector}\n"
        " ---"
    )

    dependencies = {
        "preprocessor": preprocessor,
        "detector": detector,
        "file_saver": file_saver,
        "mq_client": mq_client,
    }

    inject_dependencies_into_handlers(handlers, dependencies)

    return processor.Processor(handlers=handlers), video_capture

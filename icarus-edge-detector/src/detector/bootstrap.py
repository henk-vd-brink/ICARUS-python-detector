import inspect
import queue
import logging

from . import config
from .adapters import senders, video_capture as vc, savers, mq_clients
from .service_layer import handlers, processor
from .domain import services as domain_services

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
    injected_functions = {}

    for function in functions:
        function_name, function = function
        setattr(handler_module, function_name, inject_dependencies(function, dependencies))

def bootstrap(
    sender = senders.HttpSender(config={}),
    preprocessor = domain_services.preprocessors.MobileNetV3Preprocessor(),
    detector = domain_services.detectors.MobileNetV3Detector(),
    postprocessor = domain_services.postprocessors.MobileNetV3Postprocessor(),
    video_capture = vc.VideoCapture(),
    file_saver = savers.FileSystemSaver(),
    mq_client = mq_clients.RedisClient()
):   

    mq_client.connect()

    logger.info(
        "Initialised APP \n --- \n"
        f"SELECTED preprocessor: {preprocessor}\n"
        f"SELECTED detector: {detector}\n"
        f"SELECTED postprocessor: {postprocessor}\n"
        " ---"
    )

    dependencies = {
        "preprocessor": preprocessor,
        "postprocessor": postprocessor,
        "detector": detector,
        "sender": sender,
        "file_saver": file_saver,
        "mq_client": mq_client
    }

    inject_dependencies_into_handlers(handlers, dependencies)

    return processor.Processor(handlers=handlers), video_capture
    



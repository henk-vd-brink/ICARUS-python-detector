import inspect
import logging
from . import config
from .adapters import video_capture as vc, meta_data_senders as mds, file_senders as fs
from .service_layer import handlers, flow
from .domain.services import preprocessors, detectors


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
    video_capture=vc.VideoCapture.from_dict(config.get_video_capture_config()),
    file_sender=fs.HttpsFileSender.from_dict(config.get_file_sender_config()),
):
    selected_meta_data_sender = mds.SWITCHER.get(config.META_DATA_SENDER)

    meta_data_sender_config = config.get_meta_data_sender_config()

    meta_data_sender = (selected_meta_data_sender.from_dict(meta_data_sender_config),)

    detector_config = config.get_yolo_v5_detector_config()
    detector_config["preprocessor"] = preprocessors.YoloV5Preprocessor()

    detector = detectors.YoloV5Detector.from_dict(detector_config)

    dependencies = {
        "detector": detector,
        "meta_data_sender": meta_data_sender,
        "file_sender": file_sender,
    }

    inject_dependencies_into_handlers(handlers, dependencies)

    return flow.Flow(handlers=handlers), video_capture

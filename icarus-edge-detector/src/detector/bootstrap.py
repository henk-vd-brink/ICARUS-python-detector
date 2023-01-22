import inspect

from . import config
from .adapters import video_capture as vc, mq_clients as mc, file_senders as fs
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
    rabbitmq_client=mc.RabbitMqClient.from_dict(config.get_rabbitmq_client_config()),
    file_sender=fs.HttpsFileSender.from_dict(config.get_file_sender_config()),
    connect_to_rabbit_mq_broker=True,
):

    detector_config = config.get_yolo_v5_detector_config()
    detector_config["preprocessor"] = preprocessors.YoloV5Preprocessor()

    detector = detectors.YoloV5Detector.from_dict(detector_config)

    if connect_to_rabbit_mq_broker:
        rabbitmq_client.connect()
        rabbitmq_client.channel.exchange_declare("DetectedObjects")

    dependencies = {
        "detector": detector,
        "rabbitmq_client": rabbitmq_client,
        "file_sender": file_sender,
    }

    inject_dependencies_into_handlers(handlers, dependencies)

    return flow.Flow(handlers=handlers), video_capture

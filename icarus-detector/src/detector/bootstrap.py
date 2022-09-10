import inspect
import queue
import logging

from . import config
from .adapters import senders
from .service_layer import messagebus, handlers, event_collector as ec


def bootstrap(
    event_collector = ec.EventCollector(),
    sender = senders.HttpsSender()
):
    dependencies = {"event_collector": event_collector, "sender": sender}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return dict(
        bus=messagebus.MessageBus(
            command_handlers=injected_command_handlers,
            event_handlers=injected_event_handlers,
            event_collector=event_collector,
        ),
    )
    



def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters

    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)

import logging
import schema
from ..domain import commands, events

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self, command_handlers, event_handlers, event_collector):
        self._command_handlers = command_handlers
        self._event_handlers = event_handlers
        self.event_collector = event_collector

    def handle_message(self, name: str, body: dict):
        try:
            message_type = next(
                mt for mt in self._command_handlers if mt.__name__ == name
            )
            message = message_type.from_dict(body)
            self.handle(message)

        except StopIteration:
            raise KeyError(f"Unknown message with name {name}")

        except schema.SchemaError as e:
            logging.error(f"invalid message of type {name}\n" f"{body}\n" f"{e}")
            raise e

    def handle(self, message):
        self.queue = [message]

        while self.queue:
            message = self.queue.pop(0)

            if isinstance(message, events.Event):
                self._handle_event(message)
            elif isinstance(message, commands.Command):
                self._handle_command(message)
            else:
                raise Exception("Message was not an Event or Command.")

    def _handle_command(self, command):
        handler = self._command_handlers.get(type(command))

        if not handler:
            raise KeyError(f"Handler for command {type(command)} does not exist.")

        handler(command)
        self.queue.extend(self.event_collector.collect_new_events())

    def _handle_event(self, event):
        for handler in self._event_handlers[type(event)]:
            try:
                handler(event)
                self.queue.extend(self.event_collector.collect_new_events())
            except Exception as e:
                logging.warning(f"Error handling event: {type(event).__name__}")
                logging.exception(e)

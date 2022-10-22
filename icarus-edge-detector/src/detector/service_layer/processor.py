


class Processor:
    def __init__(self, handlers):
        self._handlers = handlers


    def handle_frame(self, frame):
        self._handlers.send_image_to_cloud("joe")
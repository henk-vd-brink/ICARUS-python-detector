import abc

class PipelineElement(abc.ABC):

    def handle(self, payload):
        if not self._can_handle(payload):
            raise Exception

        result = self._handle(payload)

        if not self.successor:
            return result
        
        return self.successor.handle(result)

    @abc.abstractmethod
    def _can_handle(self, payload):
        pass

    @abc.abstractmethod
    def _handle(self, payload):
        pass


class PreProcessing(PipelineElement):

    def __init__(self, *args, **kwargs):
        self.successor = None

    def _can_handle(self, payload):
        return True

    def _handle(self, payload):
        print("Preprocess")
        return payload


class Detection(PipelineElement):

    def __init__(self, *args, **kwargs):
        self.successor = None

    def _can_handle(self, payload):
        return True

    def _handle(self, payload):
        print("Detect")
        return payload


class PostProcessing(PipelineElement):

    def __init__(self, *args, **kwargs):
        self.successor = None

    def _can_handle(self, payload):
        return True

    def _handle(self, payload):
        print("Postprocess")
        return payload
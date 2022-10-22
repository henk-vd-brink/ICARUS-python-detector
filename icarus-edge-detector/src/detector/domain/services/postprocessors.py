import abc

class AbstractPostprocessor(abc.ABC):
    def __init__(self, config = {}):
        self._config = config

    def postprocess(self, frame, meta_data={}):
        self._postprocess(frame, meta_data)

    @abc.abstractmethod
    def _postprocess(self, frame, meta_data):
        pass


class FakePostprocessor(AbstractPostprocessor):

    def _postprocess(self, frame, meta_data):
        print(frame)
        return frame

    def __repr__(self):
        return "< FakePostprocessor >"
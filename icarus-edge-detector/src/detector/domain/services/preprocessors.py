import abc

class AbstractPreprocessor(abc.ABC):
    def __init__(self, config = {}):
        self._config = config

    def preprocess(self, frame, meta_data={}):
        self._preprocess(frame, meta_data)

    @abc.abstractmethod
    def _preprocess(self, frame, meta_data):
        pass


class FakePreprocessor(AbstractPreprocessor):

    def _preprocess(self, frame, meta_data):
        print(frame)
        return frame


    def __repr__(self):
        return "< FakePreprocessor >"
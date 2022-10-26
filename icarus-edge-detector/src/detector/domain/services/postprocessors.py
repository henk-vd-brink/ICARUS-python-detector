import abc
import logging

logger = logging.getLogger(__name__)

class AbstractPostprocessor(abc.ABC):
    def __init__(self, config = {}):
        self._config = config

    def postprocess(self, data):
        logger.info("Postprocessing frame")
        return self._postprocess(data)

    @abc.abstractmethod
    def _postprocess(self, data):
        pass


class FakePostprocessor(AbstractPostprocessor):

    def _postprocess(self, data):
        return data

    def __repr__(self):
        return "< FakePostprocessor >"


class MobileNetV3Postprocessor(AbstractPostprocessor):

    def _postprocess(self, data):
        return data

    def __repr__(self):
        return "< MobileNetV3Postprocessor >"

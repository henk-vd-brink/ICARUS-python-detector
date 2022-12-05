import abc
import asyncio
import logging

logger = logging.getLogger(__name__)


class AbstractSender(abc.ABC):
    def __init__(self, config={}):
        self._config = config

    def send_file(self, file_name, file_bytes):
        self._send_file(file_name, file_bytes)

    @abc.abstractmethod
    def _send_file(file_name, file_bytes):
        pass


class HttpSender(AbstractSender):
    def _send_file(self, file_name, file_bytes):
        logger.info("Sending file %s", file_name)

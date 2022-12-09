import abc
import requests
import logging

logger = logging.getLogger(__name__)


class Sender(abc.ABC):
    def __init__(self, config) -> None:
        self._config = config
        self._parse_config(config)

    @abc.abstractmethod
    def _parse_config(self, config):
        pass

    @abc.abstractmethod
    def send_file(self, file_name, file_bytes):
        pass


class ApiSender(Sender):
    def _parse_config(self, config):
        self._remote_host_ip_address = config["remote_host_ip_address"]
        self._remote_host_port = config["remote_host_port"]

    def send_file(self, file_name, file_bytes):
        url = f"https://{self._remote_host_ip_address}:{self._remote_host_port}/files"
        files = {"file": (file_name, file_bytes)}

        try:
            response = requests.post(url, files=files, verify=False)
        except requests.ConnectionError as e:
            logger.exception(e)
            return 599

        return response.status_code

import logging
import requests
import warnings
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

warnings.filterwarnings(action="ignore", message="Unverified HTTPS request")


class FileSender(ABC):
    @abstractmethod
    def send(self, file_name, file_bytes):
        pass


class HttpsFileSender(FileSender):
    def __init__(self, remote_ip_address, remote_port, auth=None):
        self._remote_ip_address = remote_ip_address
        self._remote_port = remote_port
        self._auth = auth

        self._remote_url = (
            f"https://{self._remote_ip_address}:{self._remote_port}/files"
        )

    @classmethod
    def from_dict(cls, input_dict):
        remote_ip_address = input_dict["remote_ip_address"]
        remote_port = input_dict["remote_port"]
        auth = input_dict["auth"]

        return cls(remote_ip_address, remote_port, auth)

    def send(self, file_name, file_bytes):
        files = {"file": (file_name, file_bytes)}

        try:
            requests.post(self._remote_url, files=files, verify=False)
        except requests.ConnectionError as e:
            self._logger.exception(e)

import logging
import requests
import warnings
from typing import Dict, Any
from abc import ABC, abstractmethod
from azure.storage.blob import BlobServiceClient


logger = logging.getLogger(__name__)

warnings.filterwarnings(action="ignore", message="Unverified HTTPS request")


class FileSender(ABC):
    @abstractmethod
    def send(self, file_name, file_bytes) -> None:
        pass


class HttpsFileSender(FileSender):
    def __init__(self, remote_ip_address: str, remote_port: int, auth=None) -> None:
        self._remote_ip_address = remote_ip_address
        self._remote_port = remote_port
        self._auth = auth

        self._remote_url = (
            f"https://{self._remote_ip_address}:{self._remote_port}/uploaded_images"
        )

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> FileSender:
        remote_ip_address = input_dict["remote_ip_address"]
        remote_port = input_dict["remote_port"]

        auth = input_dict.get("auth")

        return cls(remote_ip_address, remote_port, auth)

    def send(self, file_name: str, file_bytes: bytes) -> None:
        files = {"file": (file_name, file_bytes)}

        try:
            requests.post(self._remote_url, files=files, verify=False)
        except requests.ConnectionError as e:
            self._logger.exception(e)


class AzureBlobSender(FileSender):
    def __init__(
        self, remote_ip_address: str, remote_port: int, account_key: str
    ) -> None:
        self._remote_ip_address = remote_ip_address
        self._remote_port = remote_port
        self._account_key = account_key

        self._connection_string = (
            f"DefaultEndpointsProtocol=http;"
            f"BlobEndpoint=http://{remote_ip_address}:{remote_port}/icaruslocaldev1;"
            f"AccountName=icaruslocaldev1;AccountKey={account_key}"
        )

        self._blob_service_client = BlobServiceClient.from_connection_string(
            self._connection_string, "icaruslocaldev1"
        )

        self._container_client = self._blob_service_client.get_container_client(
            "icaruslocaldev1"
        )

        if not self._container_client.exists():
            self._container_client.create_container()

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> FileSender:
        remote_ip_address = input_dict["remote_ip_address"]
        remote_port = input_dict["remote_port"]
        account_key = input_dict["account_key"]

        return cls(remote_ip_address, remote_port, account_key)

    def send(self, file_name: str, file_bytes: bytes) -> None:
        blob_client = self._container_client.get_blob_client(file_name)
        blob_client.upload_blob(file_bytes, blob_type="BlockBlob", overwrite=True)


SWITCHER = {"blob": AzureBlobSender, "https": HttpsFileSender}

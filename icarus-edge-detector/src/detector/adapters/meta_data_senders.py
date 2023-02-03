import pika
import ssl
from azure.iot.device import IoTHubModuleClient
from typing import Dict, Any
from abc import ABC, abstractmethod


class AbstractMqClient(ABC):
    def connect(self) -> None:
        self._connect()

    @abstractmethod
    def send_meta_data(self, message):
        pass


class IoTEdgeClient(AbstractMqClient):
    def __init__(self):
        self._iot_edge_client = IoTHubModuleClient.create_from_edge_environment()

    @classmethod
    def from_dict(cls, _):
        return cls()

    def send_meta_data(self, message):
        self._iot_edge_client.send_message_to_output(message, "output_1")


class RabbitMqClient(AbstractMqClient):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        path_to_root_ca_cert: str = None,
        host_cn: str = None,
        connect_to_broker=True,
    ) -> None:
        self._path_to_root_ca_cert = path_to_root_ca_cert
        self._host_cn = host_cn

        self._ssl_options = None

        self._connection = None

        self.channel = None

        if self._path_to_root_ca_cert and self._host_cn:
            context = ssl.create_default_context(cafile=self._path_to_root_ca_cert)
            self._ssl_options = pika.SSLOptions(context, self._host_cn)

        self._parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username, password),
            ssl_options=self._ssl_options,
        )

        if connect_to_broker:
            self.connect()
            self.channel.exchange_declare("DetectedObjects")

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> AbstractMqClient:
        host = input_dict["host"]
        port = input_dict["port"]
        username = input_dict["username"]
        password = input_dict["password"]

        path_to_root_ca_cert = input_dict.get("path_to_root_ca_cert")
        host_cn = input_dict.get("host_cn")

        return cls(
            host=host,
            port=port,
            username=username,
            password=password,
            path_to_root_ca_cert=path_to_root_ca_cert,
            host_cn=host_cn,
        )

    def _connect(self) -> None:
        self._connection = pika.BlockingConnection(self._parameters)
        self.channel = self._connection.channel()

    def _disconnect(self) -> None:
        self._connection.close()

    def send_meta_data(self, message):
        if not self.channel.is_open:
            self._connect()

        self.channel.basic_publish(
            exchange="DetectedObjects", routing_key="jetson-nano0", body=message
        )


SWITCHER = {"rabbitmq": RabbitMqClient, "iot_edge": IoTEdgeClient}

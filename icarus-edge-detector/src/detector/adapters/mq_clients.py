import redis
import pika
import ssl
from typing import Dict, Any
from abc import ABC, abstractmethod


class AbstractMqClient(ABC):
    def connect(self) -> None:
        self._connect()

    @abstractmethod
    def _connect(self) -> None:
        pass

    @abstractmethod
    def _disconnect(self) -> None:
        pass


class RedisClient(AbstractMqClient):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> AbstractMqClient:
        host = input_dict["host"]
        port = input_dict["port"]
        return cls(host=host, port=port)

    def _connect(self) -> None:
        self._connection = redis.StrictRedis(
            host=self._host,
            port=self._port,
            db=0,
            charset="utf-8",
            decode_responses=True,
        )

    def _disconnect(self) -> None:
        self._connection.close()


class RabbitMqClient(AbstractMqClient):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        path_to_root_ca_cert: str = None,
        host_cn: str = None,
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

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> AbstractMqClient:
        host = input_dict["broker_ip_address"]
        port = input_dict["broker_port"]
        username = input_dict["broker_username"]
        password = input_dict["broker_password"]

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

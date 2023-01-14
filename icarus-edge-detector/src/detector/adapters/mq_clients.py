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
        host = input_dict.get("host")
        port = input_dict["port"]
        return cls(host=host, port=port)

    def _connect(self) -> None:
        self._connection = redis.StrictRedis(
            host=self._host,
            port=6379,
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
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._path_to_root_ca_cert = path_to_root_ca_cert
        self._host_cn = host_cn

        self._ssl_options = None

        self._connection = None
        self._channel = None

        if self._path_to_root_ca_cert and self._host_cn:
            context = ssl.create_default_context(cafile=self._path_to_root_ca_cert)
            self._ssl_options = pika.SSLOptions(context, self._host_cn)

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

    @property
    def channel(self) -> pika.channel.Channel:
        return self._channel

    def _connect(self) -> None:
        credentials = pika.PlainCredentials(self._username, self._password)

        parameters = pika.ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=credentials,
            ssl_options=self._ssl_options,
        )

        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def _disconnect(self) -> None:
        self._connection.close()

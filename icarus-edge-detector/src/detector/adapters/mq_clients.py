import redis
import pika
import ssl
from abc import ABC, abstractmethod


class AbstractMqClient(ABC):
    def connect(self):
        self._connect()

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def _disconnect(self):
        pass


class RedisClient(AbstractMqClient):
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port

    @classmethod
    def from_dict(cls, input_dict) -> AbstractMqClient:
        host = input_dict.get("host")
        port = input_dict.get("port")
        return cls(host=host, port=port)

    def _connect(self) -> None:
        self._connection = redis.StrictRedis(
            host=self._config.get("host"),
            port=6379,
            db=0,
            charset="utf-8",
            decode_responses=True,
        )

    def _disconnect(self) -> None:
        self._connection.close()

    def __enter__(self) -> redis.StrictRedis:
        self._connect()
        return self._connection

    def __exit__(self, *_) -> None:
        self._disconnect()


class RabbitMqClient(AbstractMqClient):
    def __init__(
        self, host, port, username, password, path_to_root_ca_cert, host_cn
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
    def from_dict(cls, input_dict) -> AbstractMqClient:
        host = input_dict.get("broker_ip_address")
        port = input_dict.get("broker_port")
        username = input_dict.get("broker_username")
        password = input_dict.get("broker_password")

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
    def channel(self):
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

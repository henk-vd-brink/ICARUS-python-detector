import pika
import json
import ssl
import redis
import abc


class MqClient(abc.ABC):
    def __init__(self, config) -> None:
        self._config = config
        self._parse_config(config)

    @abc.abstractmethod
    def _parse_config(self, config):
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def publish(self, topic, body):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *_):
        pass


class RedisMqClient(MqClient):
    def _parse_config(self, config):
        pass

    def connect(self):
        self.connection = redis.StrictRedis(
            "icarus-edge-redis", 6379, charset="utf-8", decode_responses=True
        )

    def publish(self, topic, body):
        pass


class RabbitMqClient(MqClient):
    def _parse_config(self, config):
        pass

    def connect(self):
        # context = ssl.create_default_context(cafile="/home/docker_user/certs/root_ca.crt")
        # ssl_options = pika.SSLOptions(context, "client-1")

        credentials = pika.PlainCredentials(
            self._config.get("broker_username"), self._config.get("broker_password")
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._config.get("broker_ip_address"),
                port=self._config.get("broker_port"),
                credentials=credentials,
            )
        )

        self._channel = connection.channel()

    def publish(self, topic, body):
        if isinstance(body, dict):
            body = json.dumps(body)

        exchange = self._config.get("exchange", "")

        self._channel.basic_publish(exchange=exchange, routing_key=topic, body=body)

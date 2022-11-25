import pika
import json
import abc

class AbstractMqClient(abc.ABC):

    def connect(self):
        self._connect()

    def publish(self, topic: str, data):
        self._publish(topic, data)

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def _publish(self, topic: str, data):
        pass

class RabbitMqClient(AbstractMqClient):
    def __init__(self, config = {}):
        self._config = config

    def _connect(self):
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

    def _publish(self, routing_key, body):
        if isinstance(body, dict):
            body = json.dumps(body)

        exchange = self._config.get("exchange")
        self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)

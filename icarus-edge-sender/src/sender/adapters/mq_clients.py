import pika
import json
import ssl

class RabbitMqClient:
    def __init__(self, config={}):
        self._config = config

    def connect(self):
        context = ssl.create_default_context(cafile="/home/docker_user/certs/root_ca.crt")
        ssl_options = pika.SSLOptions(context, "client-1")

        credentials = pika.PlainCredentials(
            self._config.get("broker_username"), self._config.get("broker_password")
        )

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._config.get("broker_ip_address"),
                port=self._config.get("broker_port"),
                credentials=credentials,
                ssl_options=ssl_options
            )
        )

        self._channel = connection.channel()

    def publish(self, routing_key, body):
        if isinstance(body, dict):
            body = json.dumps(body)

        exchange = self._config.get("exchange", "")

        self._channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=body
        )

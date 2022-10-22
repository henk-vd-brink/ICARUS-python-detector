import abc
import redis
import json


class AbstractMqClient(abc.Abc):

    def connect(self):
        self._connect()

    def publish(self, topic: str, data):
        self._publish(topic, data)

    def __enter__(self, *args, **kwargs):
        self._connect()
        return self
    
    def __exit__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def _publish(self, topic: str, data):
        pass

class RedisClient(AbstractMqClient):
    def __init__(self, config = {}):
        self._config = config

    def _connect(self):
        self._connection = redis.Redis(
            host = self._config.get("host", "localhost"),
            port = self._config.get("port", 6379),
            db = 0
        )

    def _publish(self, topic: str, data: dict):
        if isinstance(data, dict):
            data = json.dumps(data)

        self._connection.rpush(topic, data)
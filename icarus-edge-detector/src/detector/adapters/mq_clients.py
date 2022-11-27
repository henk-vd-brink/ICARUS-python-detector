import abc
import redis
import json


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


class RedisClient(AbstractMqClient):
    def __init__(self, config={}):
        self._config = config

    def _connect(self):
        self._connection = redis.StrictRedis(
            host=self._config.get("host"),
            port=6379,
            db=0,
            charset="utf-8",
            decode_responses=True,
        )

    def _publish(self, topic: str, message: dict):

        if isinstance(message, dict):
            message = json.dumps(message)

        self._connection.publish(topic, message)

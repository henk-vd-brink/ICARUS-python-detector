import redis

config = {"host": "localhost", "port": 6379}

class RedisAdapter:
    def __init__(self, config):
        self._config = config

    def connect(self):
        self._connection = redis.Redis(**config)
    
    def 


def test_connection_to_redis():
    redis_adapter = RedisAdapter(config=config)

if __name__ == "__main__":
    test_connection_to_redis()



    
import redis

red = redis.StrictRedis("localhost", 6379, charset="utf-8", decode_responses=True)


def redis_consumer():
    sub = red.pubsub()
    sub.subscribe("test")

    for message in sub.listen():
        print(message.get("data"))


if __name__ == "__main__":
    while True:
        redis_consumer()

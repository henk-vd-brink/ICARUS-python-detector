import redis
import pathlib
import json

red = redis.StrictRedis('icarus-edge-redis', 6379, charset="utf-8", decode_responses=True)

def redis_consumer():
    sub = red.pubsub()
    sub.subscribe("test")

    for message in sub.listen():

        data_from_message = message.get("data")

        if not isinstance(data_from_message, str):
            continue

        data_from_message_as_dict = json.loads(message.get("data"))

        file_name = data_from_message_as_dict.get("file_name")
        print(file_name)

        with open("/dev/shm/" + file_name, "rb") as f:
            f.read()
            print("read file ", file_name)
        
        pathlib.Path("/dev/shm/" + file_name).unlink()




if __name__ == "__main__":
    while True:
        redis_consumer()

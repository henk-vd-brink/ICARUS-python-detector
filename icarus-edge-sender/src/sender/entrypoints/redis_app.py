import redis
import pathlib
import json
import requests

from .. import bootstrap

mq_client = bootstrap.bootstrap()
mq_client.connect()

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
            file_bytes = f.read()
            print("read file ", file_name)

        files = {"file": (file_name, file_bytes)}
        requests.post("https://192.168.178.47:8443/files", files=files, verify=False)

        message = dict(
            image_uuid = 
            class = data_from_message_as_dict.get("class")
            x_1 = data_from_message_as_dict.get("bounding_box")[0],
            y_1 = data_from_message_as_dict.get("bounding_box")[0],
            x_2 = data_from_message_as_dict.get("bounding_box")[0],
            y_2 = data_from_message_as_dict.get("bounding_box")[0]
        )

        pathlib.Path("/dev/shm/" + file_name).unlink()




if __name__ == "__main__":
    while True:
        redis_consumer()

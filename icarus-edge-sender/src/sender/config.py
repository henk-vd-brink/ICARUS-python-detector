import os
import logging


def get_rabbit_mq_client_configuration():
    return dict(
        broker_ip_address=os.environ.get("REMOTE_IP_ADDRESS"),
        broker_port=os.environ.get("REMOTE_RABBITMQ_PORT"),
        broker_username=os.environ.get("REMOTE_RABBITMQ_USERNAME"),
        broker_password=os.environ.get("REMOTE_RABBITMQ_PASSWORD"),
    )


def get_redis_mq_client_configuration():
    return dict(redis_ip_address=os.environ.get("REDIS_IP_ADDRESS"), port=6379)


def get_remote_host_configuration():
    return dict(
        remote_host_ip_address=os.environ.get("REMOTE_IP_ADDRESS"),
        remote_host_port=os.environ.get("REMOTE_HOST_PORT"),
    )


def get_file_system_configuration():
    return dict(file_system_path="/dev/shm")

def get_rabbit_mq_client_configuration():
    return dict(
        broker_ip_address="192.168.178.47",
        broker_port=5672,
        broker_username="guest",
        broker_password="guest",
    )


def get_redis_mq_client_configuration():
    return dict(redis_ip_address="icarus-edge-redis", port=6379)


def get_remote_host_configuration():
    return dict(remote_host_ip_address="192.168.178.47", remote_host_port=8443)


def get_file_system_configuration():
    return dict(file_system_path="/dev/shm")

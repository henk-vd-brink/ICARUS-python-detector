import logging
import warnings

from . import config
from .adapters import mq_clients, file_system, senders

warnings.filterwarnings(action="ignore", message="Unverified HTTPS request")


def bootstrap(
    mq_client=mq_clients.RabbitMqClient(config.get_rabbit_mq_client_configuration()),
    file_system_adapter=file_system.FileSystem(config.get_file_system_configuration()),
    sender_adapter=senders.ApiSender(config.get_remote_host_configuration()),
    redis_mq_client=mq_clients.RedisMqClient(
        config.get_redis_mq_client_configuration()
    ),
):
    return dict(
        mq_client=mq_client,
        file_system_adapter=file_system_adapter,
        sender_adapter=sender_adapter,
        redis_mq_client=redis_mq_client,
    )

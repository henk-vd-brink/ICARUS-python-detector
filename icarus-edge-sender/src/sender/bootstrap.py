from . import config
from .adapters import mq_clients

def bootstrap():
    mq_client = mq_clients.RabbitMqClient(config.get_mq_client_configuration())

    return mq_client
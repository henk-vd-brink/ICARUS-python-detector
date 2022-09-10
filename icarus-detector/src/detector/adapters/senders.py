import abc
import asyncio
import aiohttp
import logging

logger = logging.getLogger(__name__)

class AbstractSender(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def send_file(self, url, file_name, file_bytes):
        pass


class HttpsSender(AbstractSender):
    async def _send_file(self, url, file_name, file_bytes):
        _, file_extension = file_name.split(".")
        data = aiohttp.FormData()
        data.add_field("file", file_bytes, filename=file_name, content_type=f"image/{file_extension}")
        
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data=data, verify_ssl=False)
        logger.info(response.status)

    def send_file(self, url, file_name, file_bytes):
        asyncio.run(self._send_file(url, file_name, file_bytes))
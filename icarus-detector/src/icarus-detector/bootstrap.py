import inspect
import queue
import logging

from . import config
from .adapters import (
    video_capture as vc
)


logging.basicConfig(level=logging.INFO)

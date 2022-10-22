import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

def preprocess_frame(frame, preprocessor):
    print(frame, preprocessor)

def send_image_to_cloud(frame, sender):
    sender.send_file("test.png", "bytes")


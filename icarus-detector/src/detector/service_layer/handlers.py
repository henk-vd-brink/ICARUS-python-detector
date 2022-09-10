import datetime
import uuid
import cv2
import logging
from ..domain import commands, events, model

logger = logging.getLogger(__name__)

def add_metadata_to_image(cmd, event_collector):
    timestamp = datetime.datetime.utcnow()
    image_uuid = str(uuid.uuid4())

    image = model.Image(
        image=cmd.image,
        timestamp=timestamp,
        uuid=image_uuid
    )

    event_collector.events.append(
        events.AddedMetadataToImage(image=image)
    )

def store_image_in_cloud(cmd, sender):
    image = cmd.image
    success, encoded_image = cv2.imencode('.png', image.image)
    image_bytes = encoded_image.tobytes()

    sender.send_file(
        url = "http://192.168.178.47:7000/files",
        file_name = image.uuid + ".png",
        file_bytes = image_bytes,
    )



COMMAND_HANDLERS = {
    commands.ReceivedImage: add_metadata_to_image
}

EVENT_HANDLERS = {
    events.AddedMetadataToImage: [store_image_in_cloud]
}

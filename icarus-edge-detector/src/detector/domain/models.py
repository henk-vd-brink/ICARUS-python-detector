import numpy as np
from dataclasses import dataclass, field, asdict
from datetime import datetime

from .. import config


@dataclass
class Frame:
    image: np.ndarray
    uuid: str
    timestamp: datetime
    detections: list = field(default_factory=lambda: [])

    @classmethod
    def from_image(cls, image):
        timestamp = datetime.now()
        timestamp_as_string = timestamp.strftime("%Y-%m-%d-%H-%M-%S-%f")
        image_uuid = f"{config.DEVICE_ID}-{timestamp_as_string}"
        return cls(image=image, uuid=image_uuid, timestamp=timestamp)


@dataclass
class MessageMetaData:
    label: str
    x_1: int
    y_1: int
    x_2: int
    y_2: int
    confidence: float

    @classmethod
    def from_detection(cls, detection):
        return cls(
            label=detection.get("label"),
            x_1=detection.get("bounding_box")[0],
            y_1=detection.get("bounding_box")[1],
            x_2=detection.get("bounding_box")[2],
            y_2=detection.get("bounding_box")[3],
            confidence=detection.get("confidence"),
        )


@dataclass
class Message:
    image_uuid: str
    timestamp: str
    meta_data: list = field(default_factory=lambda: [])

    @classmethod
    def from_frame(cls, frame):
        meta_data = list()
        for detection in frame.detections:
            meta_data.append(MessageMetaData.from_detection(detection))

        return cls(
            image_uuid=frame.uuid,
            timestamp=frame.timestamp.isoformat(),
            meta_data=meta_data,
        )

    def asdict(self):
        return asdict(self)

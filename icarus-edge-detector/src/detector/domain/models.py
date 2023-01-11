import uuid
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Frame:
    image: np.ndarray
    uuid: str
    timestamp: datetime
    detections: list = field(default_factory=lambda: [])

    @classmethod
    def from_image(cls, image):
        timestamp = datetime.now()
        image_uuid = timestamp.strftime("%Y-%m-%d-%H-%M-%S-%f")
        return cls(image=image, uuid=image_uuid, timestamp=timestamp)

import datetime
import numpy as np


class Image:
    def __init__(
        self,
        image: np.ndarray,
        timestamp: datetime.datetime,
        uuid: str
    ):
        self._image = image
        self.timestamp=timestamp
        self.uuid=uuid

    @property
    def image(self):
        return self._image

    def asdict(self):
        return dict(
            image=self._image,
            timestamp=self.timestamp,
            uuid=self.uuid
        )


class PreprocessStep:
    def __init__(self, config=None):
        self._config = config

    def process(self, input_image: Image):
        return input_image


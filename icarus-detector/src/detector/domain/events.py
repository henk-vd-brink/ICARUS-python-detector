from dataclasses import dataclass
from . import model

class Event:
    pass

@dataclass(unsafe_hash=True)
class AddedMetadataToImage(Event):
    image: model.Image
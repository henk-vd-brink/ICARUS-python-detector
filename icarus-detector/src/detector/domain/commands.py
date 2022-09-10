import numpy as np
from schema import Schema, Or
from dataclasses import make_dataclass


class Command:
    pass


def command_factory(name, **fields):
    schema = Schema(fields, ignore_extra_keys=True)
    cls = make_dataclass(name, fields.keys(), bases=(Command,))
    cls.from_dict = lambda s: cls(**schema.validate(s))
    return cls

ReceivedImage = command_factory(
    "ReceivedImage",
    image=np.ndarray,
)

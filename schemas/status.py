from dataclasses import dataclass


@dataclass
class Status:
    type: str
    message: str

from dataclasses import dataclass


@dataclass
class Epoch:
    current: int
    total: int

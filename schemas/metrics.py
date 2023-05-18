from dataclasses import dataclass


@dataclass
class Metrics:
    fps: float
    p: float
    r: float
    mAP_50: float
    mAP_95: float

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PCCParameters:
    """Operational PCC parameters for belief dynamics."""
    pressure: float = 1.0
    control: float = 1.0
    chaos: float = 0.0

    def __post_init__(self):
        if self.pressure < 0 or self.control < 0:
            raise ValueError("pressure and control must be nonnegative")
        if not 0 <= self.chaos <= 1:
            raise ValueError("chaos must lie in [0, 1]")


def corrupt_binary_observation(x: int, chaos: float, rng) -> int:
    """Flip a binary observation with probability `chaos`."""
    if x not in (0, 1):
        raise ValueError("binary observation must be 0 or 1")
    return 1 - x if rng.random() < chaos else x

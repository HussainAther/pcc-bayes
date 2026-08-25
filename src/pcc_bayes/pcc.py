from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, init=False)
class BeliefUpdateParameters:
    """Bayes-domain proxy parameters used by the synthetic update model.

    These parameters are *not* asserted to be the full cross-domain PCC constructs.

    pressure
        Evidence/likelihood gain in the generalized Bayesian update.
    control
        Memory/persistence gain on prior log-odds.
    observation_corruption
        Symmetric binary observation-channel flip probability. This is a noise
        parameter only; it must not be interpreted as the mature PCC Chaos construct.

    ``chaos=...`` remains accepted as a backwards-compatible keyword alias for
    ``observation_corruption`` so historical experiments stay reproducible.
    """

    pressure: float
    control: float
    observation_corruption: float

    def __init__(
        self,
        pressure: float = 1.0,
        control: float = 1.0,
        observation_corruption: float = 0.0,
        *,
        chaos: float | None = None,
    ):
        if chaos is not None:
            if observation_corruption != 0.0 and observation_corruption != chaos:
                raise ValueError(
                    "specify only one of observation_corruption or legacy chaos"
                )
            observation_corruption = chaos

        if pressure < 0 or control < 0:
            raise ValueError("pressure and control must be nonnegative")
        if not 0.0 <= observation_corruption <= 1.0:
            raise ValueError("observation_corruption must lie in [0, 1]")

        object.__setattr__(self, "pressure", float(pressure))
        object.__setattr__(self, "control", float(control))
        object.__setattr__(self, "observation_corruption", float(observation_corruption))

    @property
    def chaos(self) -> float:
        """Legacy alias for observation_corruption.

        Kept only for reproducibility of v0.1-v0.3 code and archived outputs.
        New code should use ``observation_corruption``.
        """
        return self.observation_corruption


# Backwards-compatible public name used by historical experiments.
PCCParameters = BeliefUpdateParameters


def corrupt_binary_observation(x: int, corruption_rate: float, rng) -> int:
    """Flip a binary observation with probability ``corruption_rate``."""
    if x not in (0, 1):
        raise ValueError("binary observation must be 0 or 1")
    if not 0.0 <= corruption_rate <= 1.0:
        raise ValueError("corruption_rate must lie in [0, 1]")
    return 1 - x if rng.random() < corruption_rate else x

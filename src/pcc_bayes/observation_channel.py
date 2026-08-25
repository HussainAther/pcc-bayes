from __future__ import annotations

import numpy as np


def _validate_corruption_rate(corruption_rate: float) -> None:
    if not 0.0 <= corruption_rate <= 1.0:
        raise ValueError("corruption_rate must lie in [0, 1]")


def binary_flip_probability(observed: int, latent: int, corruption_rate: float) -> float:
    """Probability of an observed bit after a symmetric flip channel."""
    if observed not in (0, 1) or latent not in (0, 1):
        raise ValueError("observed and latent must be binary")
    _validate_corruption_rate(corruption_rate)
    return (1.0 - corruption_rate) if observed == latent else corruption_rate


def seen_one_probability(raw_one_probability: float, corruption_rate: float) -> float:
    """Marginal P(Y=1) when X~Bernoulli(p) and Y flips with ``corruption_rate``."""
    if not 0.0 <= raw_one_probability <= 1.0:
        raise ValueError("raw_one_probability must lie in [0, 1]")
    _validate_corruption_rate(corruption_rate)
    return (
        raw_one_probability * (1.0 - corruption_rate)
        + (1.0 - raw_one_probability) * corruption_rate
    )


def seen_probability(observed: int, raw_one_probability: float, corruption_rate: float) -> float:
    """Marginal probability of a received binary observation under the flip channel."""
    q = seen_one_probability(raw_one_probability, corruption_rate)
    if observed == 1:
        return q
    if observed == 0:
        return 1.0 - q
    raise ValueError("observed must be binary")


def sample_observation_channel(
    raw: int, corruption_rate: float, rng: np.random.Generator
) -> int:
    """Sample Y|X from the symmetric binary flip channel."""
    if raw not in (0, 1):
        raise ValueError("raw must be binary")
    _validate_corruption_rate(corruption_rate)
    return 1 - raw if rng.random() < corruption_rate else raw

from __future__ import annotations

import numpy as np


def binary_flip_probability(observed: int, latent: int, chaos: float) -> float:
    """Probability of an observed bit after a symmetric flip channel."""
    if observed not in (0, 1) or latent not in (0, 1):
        raise ValueError("observed and latent must be binary")
    if not 0.0 <= chaos <= 1.0:
        raise ValueError("chaos must lie in [0, 1]")
    return (1.0 - chaos) if observed == latent else chaos


def seen_one_probability(raw_one_probability: float, chaos: float) -> float:
    """Marginal P(Y=1) when X~Bernoulli(p) and Y flips X with probability chaos."""
    if not 0.0 <= raw_one_probability <= 1.0:
        raise ValueError("raw_one_probability must lie in [0, 1]")
    if not 0.0 <= chaos <= 1.0:
        raise ValueError("chaos must lie in [0, 1]")
    return raw_one_probability * (1.0 - chaos) + (1.0 - raw_one_probability) * chaos


def seen_probability(observed: int, raw_one_probability: float, chaos: float) -> float:
    """Marginal probability of a received binary observation under the flip channel."""
    q = seen_one_probability(raw_one_probability, chaos)
    if observed == 1:
        return q
    if observed == 0:
        return 1.0 - q
    raise ValueError("observed must be binary")


def sample_observation_channel(raw: int, chaos: float, rng: np.random.Generator) -> int:
    """Sample Y|X from the symmetric binary flip channel."""
    if raw not in (0, 1):
        raise ValueError("raw must be binary")
    if not 0.0 <= chaos <= 1.0:
        raise ValueError("chaos must lie in [0, 1]")
    return 1 - raw if rng.random() < chaos else raw

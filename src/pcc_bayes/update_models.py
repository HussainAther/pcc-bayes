from __future__ import annotations

import numpy as np

from .bayes import bayes_update, tempered_update
from .belief_state import normalize


def update_belief(
    prior,
    likelihood,
    model: str,
    *,
    pressure: float = 1.0,
    control: float = 1.0,
    leak: float = 1.0,
    anchor_strength: float = 0.0,
    anchor=None,
):
    """Apply one member of the v0.3 candidate update-model family.

    Models
    ------
    bayes
        Ordinary Bayesian updating.
    leaky_bayes
        ``prior**leak * likelihood``. This is intentionally recognized as the
        ``pressure=1`` slice of the PCC family rather than treated as a wholly
        unrelated mechanism.
    anchored_bayes
        Perform a standard Bayes step, then convexly mix the result toward a
        fixed anchor distribution.
    pcc
        ``prior**control * likelihood**pressure``.
    """
    prior = normalize(prior)
    likelihood = np.asarray(likelihood, dtype=float)
    name = str(model).lower()

    if name == "bayes":
        return bayes_update(prior, likelihood)
    if name == "leaky_bayes":
        if not 0.0 <= leak:
            raise ValueError("leak must be nonnegative")
        return tempered_update(prior, likelihood, pressure=1.0, control=leak)
    if name == "pcc":
        return tempered_update(
            prior, likelihood, pressure=pressure, control=control
        )
    if name == "anchored_bayes":
        if not 0.0 <= anchor_strength <= 1.0:
            raise ValueError("anchor_strength must lie in [0, 1]")
        anchor = prior if anchor is None else normalize(anchor)
        updated = bayes_update(prior, likelihood)
        return normalize((1.0 - anchor_strength) * updated + anchor_strength * anchor)
    raise ValueError(f"unknown update model: {model}")


def replay_update_model(
    observations,
    world,
    model: str,
    *,
    prior=(0.5, 0.5),
    pressure: float = 1.0,
    control: float = 1.0,
    leak: float = 1.0,
    anchor_strength: float = 0.0,
    anchor=None,
):
    """Replay an observed evidence sequence under a candidate update model."""
    observations = np.asarray(observations, dtype=int)
    if np.any((observations != 0) & (observations != 1)):
        raise ValueError("observations must be binary")

    belief = normalize(prior)
    fixed_anchor = belief.copy() if anchor is None else normalize(anchor)
    history = [belief.copy()]
    for y in observations:
        belief = update_belief(
            belief,
            world.likelihood(int(y)),
            model,
            pressure=pressure,
            control=control,
            leak=leak,
            anchor_strength=anchor_strength,
            anchor=fixed_anchor,
        )
        history.append(belief.copy())
    return np.asarray(history)

from __future__ import annotations

import numpy as np


def markov_prediction_map(belief, switch_probability: float) -> np.ndarray:
    p = np.asarray(belief, dtype=float)
    if p.shape != (3,):
        raise ValueError("belief must have shape (3,)")
    if not np.isclose(np.sum(p), 1.0) or np.any(p < 0.0):
        raise ValueError("belief must be nonnegative and sum to one")
    if not 0.0 <= switch_probability <= 1.0:
        raise ValueError("switch_probability must lie in [0,1]")
    s = float(switch_probability)
    return (1.0 - 1.5 * s) * p + 0.5 * s


def observation_update_map(predicted_belief, observation: int, observation_accuracy: float) -> np.ndarray:
    q = np.asarray(predicted_belief, dtype=float)
    if q.shape != (3,):
        raise ValueError("predicted_belief must have shape (3,)")
    if observation not in (0, 1, 2):
        raise ValueError("observation must be in {0,1,2}")
    if not (1.0 / 3.0) < observation_accuracy < 1.0:
        raise ValueError("observation_accuracy must lie in (1/3,1)")
    miss = (1.0 - observation_accuracy) / 2.0
    likelihood = np.full(3, miss, dtype=float)
    likelihood[int(observation)] = observation_accuracy
    unnormalized = q * likelihood
    return unnormalized / float(np.sum(unnormalized))


def analytical_filter_step(belief, observation: int, switch_probability: float, observation_accuracy: float):
    predicted = markov_prediction_map(belief, switch_probability)
    posterior = observation_update_map(predicted, observation, observation_accuracy)
    return predicted, posterior


def prediction_gap_contraction_residual(belief, switch_probability: float) -> float:
    p = np.asarray(belief, dtype=float)
    q = markov_prediction_map(p, switch_probability)
    kappa = 1.0 - 1.5 * float(switch_probability)
    residuals = []
    for i in range(3):
        for j in range(i + 1, 3):
            residuals.append(abs((q[i] - q[j]) - kappa * (p[i] - p[j])))
    return float(max(residuals, default=0.0))

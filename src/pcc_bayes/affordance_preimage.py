from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class AffineAffordanceBoundary:
    """Affine pullback of p'_i - p'_j = delta onto the prior simplex."""

    coefficients: np.ndarray
    intercept: float
    top_action: int
    comparison_action: int
    observation: int
    delta: float

    def value(self, prior) -> float:
        p = np.asarray(prior, dtype=float)
        if p.shape != (3,):
            raise ValueError("prior must have shape (3,)")
        return float(np.dot(self.coefficients, p) + self.intercept)


def _validate_prior(prior) -> np.ndarray:
    p = np.asarray(prior, dtype=float)
    if p.shape != (3,):
        raise ValueError("prior must have shape (3,)")
    if np.any(p < 0.0) or not np.isclose(float(np.sum(p)), 1.0):
        raise ValueError("prior must be nonnegative and sum to one")
    return p


def observation_likelihood_vector(observation: int, observation_accuracy: float) -> np.ndarray:
    if observation not in (0, 1, 2):
        raise ValueError("observation must be in {0,1,2}")
    if not (1.0 / 3.0) < observation_accuracy < 1.0:
        raise ValueError("observation_accuracy must lie in (1/3,1)")
    miss = (1.0 - float(observation_accuracy)) / 2.0
    likelihood = np.full(3, miss, dtype=float)
    likelihood[int(observation)] = float(observation_accuracy)
    return likelihood


def unnormalized_update_scores(prior, observation: int, switch_probability: float, observation_accuracy: float) -> tuple[np.ndarray, float]:
    p = _validate_prior(prior)
    if not 0.0 <= switch_probability <= 1.0:
        raise ValueError("switch_probability must lie in [0,1]")
    kappa = 1.0 - 1.5 * float(switch_probability)
    predicted = kappa * p + 0.5 * float(switch_probability)
    likelihood = observation_likelihood_vector(observation, observation_accuracy)
    scores = predicted * likelihood
    return scores, float(np.sum(scores))


def affine_affordance_boundary(
    observation: int,
    top_action: int,
    comparison_action: int,
    switch_probability: float,
    observation_accuracy: float,
    delta: float = 0.15,
) -> AffineAffordanceBoundary:
    if top_action not in (0, 1, 2) or comparison_action not in (0, 1, 2):
        raise ValueError("action indices must be in {0,1,2}")
    if top_action == comparison_action:
        raise ValueError("top_action and comparison_action must differ")
    if delta <= 0.0:
        raise ValueError("delta must be positive")
    if not 0.0 <= switch_probability <= 1.0:
        raise ValueError("switch_probability must lie in [0,1]")

    likelihood = observation_likelihood_vector(observation, observation_accuracy)
    kappa = 1.0 - 1.5 * float(switch_probability)
    bias = 0.5 * float(switch_probability)
    e_i = np.zeros(3, dtype=float)
    e_j = np.zeros(3, dtype=float)
    e_i[top_action] = 1.0
    e_j[comparison_action] = 1.0
    coefficients = kappa * (
        likelihood[top_action] * e_i
        - likelihood[comparison_action] * e_j
        - float(delta) * likelihood
    )
    # sum(likelihood) == 1 for the symmetric categorical observation model.
    intercept = bias * (
        likelihood[top_action] - likelihood[comparison_action] - float(delta)
    )
    return AffineAffordanceBoundary(
        coefficients=coefficients,
        intercept=float(intercept),
        top_action=top_action,
        comparison_action=comparison_action,
        observation=observation,
        delta=float(delta),
    )


def score_boundary_value(prior, observation: int, top_action: int, comparison_action: int, switch_probability: float, observation_accuracy: float, delta: float = 0.15) -> float:
    scores, z = unnormalized_update_scores(prior, observation, switch_probability, observation_accuracy)
    return float(scores[top_action] - scores[comparison_action] - float(delta) * z)


def classify_affordance_preimage(prior, observation: int, switch_probability: float, observation_accuracy: float, delta: float = 0.15) -> int:
    scores, z = unnormalized_update_scores(prior, observation, switch_probability, observation_accuracy)
    top = int(np.argmax(scores))
    tol = 1e-15
    live = (scores[top] - scores) <= float(delta) * z + tol
    return int(np.sum(live))


def classify_affordance_preimages(priors, observations, switch_probability: float, observation_accuracy: float, delta: float = 0.15) -> np.ndarray:
    priors = np.asarray(priors, dtype=float)
    observations = np.asarray(observations, dtype=int)
    if priors.ndim != 2 or priors.shape[1] != 3:
        raise ValueError("priors must have shape (n,3)")
    if observations.shape != (len(priors),):
        raise ValueError("observations must have shape (n,)")
    out = np.empty(len(priors), dtype=int)
    for k, (p, y) in enumerate(zip(priors, observations)):
        out[k] = classify_affordance_preimage(
            p,
            int(y),
            switch_probability=switch_probability,
            observation_accuracy=observation_accuracy,
            delta=delta,
        )
    return out

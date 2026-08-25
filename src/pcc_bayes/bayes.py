from __future__ import annotations
import numpy as np
from .belief_state import normalize, EPS


def bayes_update(prior, likelihood):
    """Standard finite-hypothesis Bayesian update."""
    prior = normalize(prior)
    likelihood = np.asarray(likelihood, dtype=float)
    if likelihood.shape != prior.shape:
        raise ValueError("likelihood and prior must have identical shape")
    if np.any(likelihood < 0) or not np.all(np.isfinite(likelihood)):
        raise ValueError("likelihood must be finite and nonnegative")
    return normalize(prior * likelihood)


def tempered_update(prior, likelihood, pressure=1.0, control=1.0):
    """
    PCC-inspired generalized Bayesian update.

    posterior_i ∝ prior_i^control * likelihood_i^pressure

    pressure > 1 emphasizes incoming evidence; pressure < 1 weakens it.
    control > 1 increases persistence of the current belief; control < 1
    flattens prior influence. pressure=control=1 recovers Bayes.
    """
    prior = normalize(prior)
    likelihood = np.asarray(likelihood, dtype=float)
    if likelihood.shape != prior.shape:
        raise ValueError("likelihood and prior must have identical shape")
    if pressure < 0 or control < 0:
        raise ValueError("pressure and control must be nonnegative")
    lp = control * np.log(np.clip(prior, EPS, 1.0))
    ll = pressure * np.log(np.clip(likelihood, EPS, None))
    score = lp + ll
    score -= np.max(score)
    return normalize(np.exp(score))

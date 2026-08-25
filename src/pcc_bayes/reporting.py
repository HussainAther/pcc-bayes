from __future__ import annotations

import math
import numpy as np

from .belief_state import EPS, normalize


def binary_logit(belief) -> float:
    b = normalize(belief)
    p = float(np.clip(b[1], EPS, 1.0 - EPS))
    return float(np.log(p) - np.log1p(-p))


def probability_from_logit(z: float) -> float:
    if z >= 0:
        return float(1.0 / (1.0 + math.exp(-z)))
    ez = math.exp(z)
    return float(ez / (1.0 + ez))


def simulate_reported_beliefs(beliefs, sigma_logit=0.25, seed=0):
    """Generate noisy scalar reports of P(H1) from latent binary beliefs.

    Noise is Gaussian in log-odds space, which keeps reports inside (0, 1)
    after the inverse-logit transformation.
    """
    if sigma_logit < 0:
        raise ValueError("sigma_logit must be nonnegative")
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 2:
        raise ValueError("beliefs must have shape (T, 2)")
    rng = np.random.default_rng(seed)
    reports = []
    for belief in beliefs:
        z = binary_logit(belief)
        if sigma_logit > 0:
            z += float(rng.normal(0.0, sigma_logit))
        reports.append(probability_from_logit(z))
    return np.asarray(reports)


def report_loglik(reports, beliefs, sigma_logit=0.25) -> float:
    """Log-likelihood of noisy reported beliefs given latent beliefs."""
    if sigma_logit <= 0:
        raise ValueError("sigma_logit must be positive")
    reports = np.asarray(reports, dtype=float)
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 2 or len(reports) != len(beliefs):
        raise ValueError("reports and beliefs must have matching lengths")
    if np.any((reports <= 0.0) | (reports >= 1.0)):
        raise ValueError("reports must lie strictly inside (0, 1)")

    const = -math.log(sigma_logit) - 0.5 * math.log(2.0 * math.pi)
    total = 0.0
    for report, belief in zip(reports, beliefs):
        observed_z = math.log(float(report)) - math.log1p(-float(report))
        latent_z = binary_logit(belief)
        residual = (observed_z - latent_z) / sigma_logit
        total += const - 0.5 * residual * residual
    return float(total)


def action_one_probability(belief, beta=3.0, bias=0.0) -> float:
    """Soft decision policy P(action=1 | latent belief)."""
    if beta < 0:
        raise ValueError("beta must be nonnegative")
    return probability_from_logit(beta * binary_logit(belief) + bias)


def simulate_actions(beliefs, beta=3.0, bias=0.0, seed=0):
    """Sample binary actions from a soft log-odds decision policy."""
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 2:
        raise ValueError("beliefs must have shape (T, 2)")
    rng = np.random.default_rng(seed)
    probs = np.asarray([action_one_probability(b, beta, bias) for b in beliefs])
    return (rng.random(len(probs)) < probs).astype(int)


def action_loglik(actions, beliefs, beta=3.0, bias=0.0) -> float:
    """Bernoulli log-likelihood of actions given latent beliefs."""
    actions = np.asarray(actions, dtype=int)
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 2 or len(actions) != len(beliefs):
        raise ValueError("actions and beliefs must have matching lengths")
    if np.any((actions != 0) & (actions != 1)):
        raise ValueError("actions must be binary")

    total = 0.0
    for action, belief in zip(actions, beliefs):
        p = float(np.clip(action_one_probability(belief, beta, bias), EPS, 1.0 - EPS))
        total += math.log(p if action == 1 else 1.0 - p)
    return float(total)

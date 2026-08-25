from __future__ import annotations
import numpy as np

EPS = 1e-15


def normalize(p):
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or len(p) < 2:
        raise ValueError("belief vector must be one-dimensional with >=2 states")
    if np.any(p < 0) or not np.all(np.isfinite(p)):
        raise ValueError("beliefs must be finite and nonnegative")
    z = p.sum()
    if z <= 0:
        raise ValueError("belief vector must have positive mass")
    return p / z


def entropy(p):
    p = normalize(p)
    q = np.clip(p, EPS, 1.0)
    return float(-np.sum(q * np.log(q)))


def kl_divergence(p, q):
    p = normalize(p)
    q = normalize(q)
    pp = np.clip(p, EPS, 1.0)
    qq = np.clip(q, EPS, 1.0)
    return float(np.sum(pp * np.log(pp / qq)))


def js_divergence(p, q):
    p = normalize(p)
    q = normalize(q)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)


def log_odds_binary(p):
    p = normalize(p)
    if len(p) != 2:
        raise ValueError("log_odds_binary requires a two-state belief")
    a, b = np.clip(p, EPS, 1.0)
    return float(np.log(a / b))

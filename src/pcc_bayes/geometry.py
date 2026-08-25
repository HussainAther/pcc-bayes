from __future__ import annotations
import numpy as np
from .belief_state import normalize, kl_divergence


def fisher_quadratic_approx_binary(p_ref, p):
    """
    Local second-order KL approximation for Bernoulli distributions.
    For q = p_ref + delta: KL(Ber(q)||Ber(p_ref)) ≈ delta^2/[2 p_ref(1-p_ref)].
    """
    if not (0 < p_ref < 1 and 0 < p < 1):
        raise ValueError("probabilities must lie in (0,1)")
    d = p - p_ref
    return float(0.5 * d * d / (p_ref * (1.0 - p_ref)))


def exact_binary_kl(p_ref, p):
    return kl_divergence(normalize([p, 1-p]), normalize([p_ref, 1-p_ref]))

from __future__ import annotations
import numpy as np
from .belief_state import entropy, kl_divergence, js_divergence, normalize


def belief_observables(history, reference=None):
    """Compute uncertainty, revision, volatility, and optional reference divergence."""
    H = np.asarray([entropy(b) for b in history], dtype=float)
    revision_kl = np.zeros(len(history), dtype=float)
    revision_js = np.zeros(len(history), dtype=float)
    for t in range(1, len(history)):
        revision_kl[t] = kl_divergence(history[t], history[t - 1])
        revision_js[t] = js_divergence(history[t], history[t - 1])

    out = {
        "entropy": H,
        "revision_kl": revision_kl,
        "revision_js": revision_js,
        "cumulative_revision": np.cumsum(revision_js),
    }
    if reference is not None:
        ref = normalize(reference)
        out["kl_to_reference"] = np.asarray(
            [kl_divergence(b, ref) for b in history], dtype=float
        )
    return out


def rolling_volatility(values, window=10):
    values = np.asarray(values, dtype=float)
    if window < 2:
        raise ValueError("window must be >= 2")
    out = np.full(values.shape, np.nan, dtype=float)
    for i in range(window - 1, len(values)):
        out[i] = np.var(values[i - window + 1:i + 1])
    return out


def belief_reversals(history):
    """Count changes in the MAP hypothesis."""
    winners = np.argmax(np.asarray(history), axis=1)
    return int(np.sum(winners[1:] != winners[:-1]))


def time_to_confidence(history, threshold=0.9):
    maxima = np.max(np.asarray(history), axis=1)
    hits = np.flatnonzero(maxima >= threshold)
    return int(hits[0]) if len(hits) else None

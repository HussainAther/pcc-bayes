from __future__ import annotations

import itertools
import math
import numpy as np

from .reporting import action_loglik, report_loglik
from .update_models import replay_update_model


def _logsumexp(values) -> float:
    values = np.asarray(values, dtype=float)
    m = float(np.max(values))
    return m + float(np.log(np.exp(values - m).sum()))


def _parameter_grid(model: str, grids):
    name = model.lower()
    if name == "bayes":
        return [{}]
    if name == "leaky_bayes":
        return [{"leak": float(x)} for x in grids.get("leak", (0.5, 0.75, 1.0))]
    if name == "anchored_bayes":
        return [
            {"anchor_strength": float(x)}
            for x in grids.get("anchor_strength", (0.0, 0.1, 0.25, 0.5))
        ]
    if name == "pcc":
        ps = grids.get("pressure", (0.5, 1.0, 1.5))
        cs = grids.get("control", (0.5, 1.0, 1.5))
        return [
            {"pressure": float(p), "control": float(c)}
            for p, c in itertools.product(ps, cs)
        ]
    raise ValueError(f"unknown update model: {model}")


def compare_update_models(
    observations,
    world,
    *,
    reports=None,
    actions=None,
    models=("bayes", "leaky_bayes", "anchored_bayes", "pcc"),
    grids=None,
    prior=(0.5, 0.5),
    report_sigma_logit=0.25,
    action_beta=3.0,
    action_bias=0.0,
):
    """Likelihood-based comparison of latent update rules.

    Internal beliefs are never supplied to this function. Each candidate model
    reconstructs its own latent belief trajectory from the common received
    evidence sequence, and is scored only through noisy reports and/or actions.

    Uniform priors are used within each model's supplied parameter grid. The
    returned ``log_evidence`` is therefore the grid-averaged marginal
    likelihood, which penalizes a flexible model when only a small part of its
    parameter grid explains the data.
    """
    if reports is None and actions is None:
        raise ValueError("at least one of reports or actions must be supplied")
    observations = np.asarray(observations, dtype=int)
    grids = {} if grids is None else dict(grids)

    expected_len = len(observations) + 1
    if reports is not None and len(reports) != expected_len:
        raise ValueError("reports must include the initial state and every update")
    if actions is not None and len(actions) != expected_len:
        raise ValueError("actions must include the initial state and every update")

    model_rows = []
    for model in models:
        candidates = []
        for params in _parameter_grid(model, grids):
            beliefs = replay_update_model(
                observations, world, model, prior=prior, **params
            )
            ll = 0.0
            if reports is not None:
                ll += report_loglik(reports, beliefs, sigma_logit=report_sigma_logit)
            if actions is not None:
                ll += action_loglik(
                    actions, beliefs, beta=action_beta, bias=action_bias
                )
            candidates.append({"params": params, "loglik": float(ll)})

        loglikes = [row["loglik"] for row in candidates]
        log_evidence = _logsumexp(loglikes) - math.log(len(loglikes))
        best = max(candidates, key=lambda row: row["loglik"])
        model_rows.append({
            "model": model,
            "log_evidence": float(log_evidence),
            "best_loglik": float(best["loglik"]),
            "best_params": dict(best["params"]),
            "grid_points": len(candidates),
        })

    normalizer = _logsumexp([row["log_evidence"] for row in model_rows])
    for row in model_rows:
        row["posterior_model_probability"] = float(
            math.exp(row["log_evidence"] - normalizer)
        )
    model_rows.sort(key=lambda row: row["posterior_model_probability"], reverse=True)
    return model_rows

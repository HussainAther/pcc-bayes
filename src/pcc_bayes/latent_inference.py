from __future__ import annotations

import math
import numpy as np

from .bayes import tempered_update
from .belief_state import EPS, normalize
from .observation_channel import binary_flip_probability, seen_probability


def _binary_logit(belief) -> float:
    b = normalize(belief)
    p = float(np.clip(b[1], EPS, 1.0 - EPS))
    return float(np.log(p) - np.log1p(-p))


def _normal_logpdf(x: float, mean: float, sigma: float) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    z = (x - mean) / sigma
    return float(-0.5 * z * z - math.log(sigma) - 0.5 * math.log(2.0 * math.pi))


def _logsumexp(values) -> float:
    values = np.asarray(values, dtype=float)
    m = float(np.max(values))
    return m + float(np.log(np.exp(values - m).sum()))


def belief_transition_loglik(
    previous_belief,
    next_belief,
    received_observation: int,
    world,
    pressure: float,
    control: float,
    sigma_logit: float = 0.05,
) -> float:
    """Measurement likelihood for a single generalized-Bayes belief transition.

    The deterministic update is compared to the observed next belief in log-odds
    space with Gaussian measurement error. This makes the inverse model a proper
    likelihood while keeping the PCC update rule explicit.
    """
    predicted = tempered_update(
        previous_belief,
        world.likelihood(int(received_observation)),
        pressure=pressure,
        control=control,
    )
    return _normal_logpdf(
        _binary_logit(next_belief), _binary_logit(predicted), sigma_logit
    )


def observed_channel_loglik(
    beliefs,
    observations,
    world,
    pressure: float,
    control: float,
    observation_corruption: float,
    *,
    raw_observations=None,
    true_hypotheses=None,
    sigma_logit: float = 0.05,
) -> float:
    """Log-likelihood when received observations are known.

    If raw observations are supplied, observation corruption is identified through
    P(Y|X,q). Otherwise the raw channel is marginalized using the Bernoulli world model.
    Belief transitions contribute an independent logit-space measurement term.
    """
    beliefs = np.asarray(beliefs, dtype=float)
    observations = np.asarray(observations, dtype=int)
    if len(beliefs) != len(observations) + 1:
        raise ValueError("beliefs must contain one more row than observations")
    if raw_observations is not None and len(raw_observations) != len(observations):
        raise ValueError("raw_observations must match observations length")
    if true_hypotheses is not None and len(true_hypotheses) != len(observations):
        raise ValueError("true_hypotheses must match observations length")

    total = 0.0
    for t, y in enumerate(observations):
        total += belief_transition_loglik(
            beliefs[t], beliefs[t + 1], int(y), world, pressure, control, sigma_logit
        )
        if raw_observations is not None:
            prob = binary_flip_probability(int(y), int(raw_observations[t]), observation_corruption)
        else:
            h = world.true_hypothesis if true_hypotheses is None else int(true_hypotheses[t])
            p_raw = float(world.probs[h])
            prob = seen_probability(int(y), p_raw, observation_corruption)
        total += math.log(max(prob, EPS))
    return float(total)


def latent_channel_loglik(
    beliefs,
    world,
    pressure: float,
    control: float,
    observation_corruption: float,
    *,
    true_hypotheses=None,
    sigma_logit: float = 0.05,
) -> float:
    """Marginal log-likelihood when received observations are latent.

    For every transition, Y_t in {0,1} is analytically marginalized:

        p(b_{t+1}|b_t) = sum_y p(y|world,q) p(b_{t+1}|b_t,y,P,C).

    Conditioning each transition on the observed b_t makes this a scalable
    state-transition likelihood rather than an exponential enumeration of all
    latent observation paths.
    """
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 2 or len(beliefs) < 2:
        raise ValueError("beliefs must have shape (T+1, 2)")
    n = len(beliefs) - 1
    if true_hypotheses is not None and len(true_hypotheses) != n:
        raise ValueError("true_hypotheses must have one entry per transition")

    total = 0.0
    for t in range(n):
        h = world.true_hypothesis if true_hypotheses is None else int(true_hypotheses[t])
        p_raw = float(world.probs[h])
        terms = []
        for y in (0, 1):
            py = seen_probability(y, p_raw, observation_corruption)
            ll_b = belief_transition_loglik(
                beliefs[t], beliefs[t + 1], y, world, pressure, control, sigma_logit
            )
            terms.append(math.log(max(py, EPS)) + ll_b)
        total += _logsumexp(terms)
    return float(total)


def infer_latent_update_grid(
    beliefs,
    world,
    pressure_grid,
    control_grid,
    corruption_grid,
    *,
    observations=None,
    raw_observations=None,
    true_hypotheses=None,
    sigma_logit: float = 0.05,
):
    """Discrete Bayesian inference over Bayes-domain update/noise parameters.

    Uniform priors over supplied grid points are assumed. If observations are
    omitted, the received evidence is analytically marginalized. If observations
    are supplied, the observed-channel likelihood is used instead.
    """
    rows = []
    for p in pressure_grid:
        for c in control_grid:
            for ch in corruption_grid:
                if observations is None:
                    ll = latent_channel_loglik(
                        beliefs, world, p, c, ch,
                        true_hypotheses=true_hypotheses,
                        sigma_logit=sigma_logit,
                    )
                else:
                    ll = observed_channel_loglik(
                        beliefs, observations, world, p, c, ch,
                        raw_observations=raw_observations,
                        true_hypotheses=true_hypotheses,
                        sigma_logit=sigma_logit,
                    )
                rows.append({
                    "pressure": float(p),
                    "control": float(c),
                    "observation_corruption": float(ch),
                    "chaos": float(ch),  # legacy output alias
                    "log_likelihood": float(ll),
                })

    logw = np.array([r["log_likelihood"] for r in rows], dtype=float)
    logw -= np.max(logw)
    weights = np.exp(logw)
    weights /= weights.sum()
    for row, w in zip(rows, weights):
        row["posterior"] = float(w)
    rows.sort(key=lambda r: r["posterior"], reverse=True)
    return rows


def infer_latent_pcc_grid(
    beliefs,
    world,
    pressure_grid,
    control_grid,
    chaos_grid,
    **kwargs,
):
    """Backwards-compatible wrapper for v0.1-v0.3 experiments.

    New code should call :func:`infer_latent_update_grid` with
    ``corruption_grid=...``. The historical ``chaos_grid`` name is retained so
    archived experiments remain reproducible.
    """
    return infer_latent_update_grid(
        beliefs,
        world,
        pressure_grid,
        control_grid,
        corruption_grid=chaos_grid,
        **kwargs,
    )


def posterior_summary(rows):
    """Posterior means, MAP point, entropy, and effective support for a grid posterior."""
    if not rows:
        raise ValueError("rows must not be empty")
    w = np.asarray([r["posterior"] for r in rows], dtype=float)
    w = w / w.sum()
    keys = ("pressure", "control", "observation_corruption")
    means = {
        key: float(sum(float(r[key]) * wi for r, wi in zip(rows, w)))
        for key in keys
    }
    # Compatibility alias for consumers of archived result schemas.
    means["chaos"] = means["observation_corruption"]
    entropy = float(-np.sum(w * np.log(np.clip(w, EPS, None))))
    map_values = {k: rows[0][k] for k in keys}
    map_values["chaos"] = map_values["observation_corruption"]
    return {
        "map": map_values,
        "mean": means,
        "posterior_entropy": entropy,
        "effective_grid_points": float(np.exp(entropy)),
        "map_posterior": float(rows[0]["posterior"]),
    }


def posterior_marginal(rows, parameter: str):
    """Collapse a grid posterior to a normalized marginal for one parameter.

    ``chaos`` is accepted only as a backwards-compatible alias for
    ``observation_corruption``.
    """
    if parameter == "chaos":
        parameter = "observation_corruption"
    if parameter not in ("pressure", "control", "observation_corruption"):
        raise ValueError(
            "parameter must be pressure, control, or observation_corruption"
        )
    mass = {}
    for row in rows:
        value = float(row[parameter])
        mass[value] = mass.get(value, 0.0) + float(row["posterior"])
    z = sum(mass.values())
    return {k: v / z for k, v in sorted(mass.items())}

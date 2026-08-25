from __future__ import annotations
import numpy as np
from .simulation import simulate_binary_learning
from .pcc import PCCParameters


def trajectory_distance(a, b):
    """Mean squared distance between two belief trajectories."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    n = min(len(a), len(b))
    return float(np.mean((a[:n] - b[:n]) ** 2))


def infer_pcc_grid(observed_beliefs, pressure_grid, control_grid, chaos_grid,
                   simulator_kwargs=None, seeds=(0, 1, 2)):
    """
    Approximate inverse inference over PCC parameters by simulation matching.

    Converts trajectory mismatch to normalized pseudo-posterior weights via
    exp(-distance / temperature), making assumptions explicit rather than
    claiming an exact likelihood for latent cognitive parameters.
    """
    simulator_kwargs = dict(simulator_kwargs or {})
    rows = []
    for p in pressure_grid:
        for c in control_grid:
            for ch in chaos_grid:
                ds = []
                for seed in seeds:
                    sim = simulate_binary_learning(
                        pcc=PCCParameters(p, c, ch), seed=seed, **simulator_kwargs
                    )
                    ds.append(trajectory_distance(observed_beliefs, sim["beliefs"]))
                rows.append((p, c, ch, float(np.mean(ds))))
    distances = np.array([r[3] for r in rows])
    positive = distances[distances > 0]
    temperature = float(np.median(positive)) if len(positive) else 1.0
    weights = np.exp(-distances / max(temperature, 1e-12))
    weights /= weights.sum()
    return [
        {"pressure": r[0], "control": r[1], "chaos": r[2],
         "distance": r[3], "weight": float(w)}
        for r, w in zip(rows, weights)
    ]


def replay_beliefs_from_observations(observations, prior, world, pressure, control):
    """Replay a belief trajectory conditional on a realized observation sequence."""
    from .belief_state import normalize
    from .bayes import tempered_update
    b = normalize(prior)
    hist = [b.copy()]
    for y in observations:
        b = tempered_update(b, world.likelihood(int(y)), pressure=pressure, control=control)
        hist.append(b.copy())
    return np.asarray(hist)


def infer_pressure_control_grid(observed_beliefs, observations, world,
                                pressure_grid, control_grid, prior=(0.5, 0.5)):
    """
    Conditional inverse inference for Pressure and Control when the realized
    observation sequence is known. Returns normalized simulation-match weights.

    Observation corruption is intentionally absent: conditional on already-observed
    evidence, corruption probability belongs to the data-channel model rather than the
    deterministic belief replay.
    """
    rows = []
    for p in pressure_grid:
        for c in control_grid:
            pred = replay_beliefs_from_observations(observations, prior, world, p, c)
            d = trajectory_distance(observed_beliefs, pred)
            rows.append((p, c, d))
    distances = np.array([r[2] for r in rows], dtype=float)
    positive = distances[distances > 0]
    temperature = float(np.median(positive)) if len(positive) else 1.0
    weights = np.exp(-distances / max(temperature, 1e-12))
    weights /= weights.sum()
    return [
        {"pressure": p, "control": c, "distance": d, "weight": float(w)}
        for (p, c, d), w in zip(rows, weights)
    ]

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .belief_state import normalize
from .bayes import tempered_update
from .pcc import PCCParameters, corrupt_binary_observation


@dataclass(frozen=True)
class BinaryWorld:
    """Two candidate Bernoulli hypotheses."""
    p_h0: float = 0.3
    p_h1: float = 0.7
    true_hypothesis: int = 1

    def __post_init__(self):
        if not (0 < self.p_h0 < 1 and 0 < self.p_h1 < 1):
            raise ValueError("Bernoulli probabilities must lie in (0,1)")
        if self.true_hypothesis not in (0, 1):
            raise ValueError("true_hypothesis must be 0 or 1")

    @property
    def probs(self):
        return np.array([self.p_h0, self.p_h1], dtype=float)

    def sample(self, rng):
        p = self.probs[self.true_hypothesis]
        return int(rng.random() < p)

    def likelihood(self, observation):
        ps = self.probs
        return ps if observation == 1 else 1.0 - ps


def simulate_binary_learning(
    steps=200,
    prior=(0.5, 0.5),
    world=None,
    pcc=None,
    seed=0,
    switch_step=None,
):
    """Simulate sequential belief updates, optionally switching the true world."""
    world = world or BinaryWorld()
    pcc = pcc or PCCParameters()
    rng = np.random.default_rng(seed)
    belief = normalize(prior)
    history = [belief.copy()]
    raw_obs, seen_obs, truths = [], [], []

    for t in range(steps):
        if switch_step is not None and t == switch_step:
            world = BinaryWorld(world.p_h0, world.p_h1, 1 - world.true_hypothesis)
        truths.append(world.true_hypothesis)
        x = world.sample(rng)
        y = corrupt_binary_observation(x, pcc.observation_corruption, rng)
        likelihood = world.likelihood(y)
        belief = tempered_update(
            belief, likelihood, pressure=pcc.pressure, control=pcc.control
        )
        raw_obs.append(x)
        seen_obs.append(y)
        history.append(belief.copy())

    return {
        "beliefs": np.asarray(history),
        "raw_observations": np.asarray(raw_obs),
        "observations": np.asarray(seen_obs),
        "true_hypotheses": np.asarray(truths),
        "parameters": pcc,
    }

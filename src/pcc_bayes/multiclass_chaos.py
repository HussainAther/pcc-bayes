from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math

import numpy as np


@dataclass(frozen=True)
class ThreeStateTrackingConfig:
    steps: int = 400
    switch_probability: float = 0.10
    observation_accuracy: float = 0.65

    def __post_init__(self):
        if self.steps < 1:
            raise ValueError("steps must be positive")
        if not 0.0 <= self.switch_probability <= 1.0:
            raise ValueError("switch_probability must lie in [0, 1]")
        if not (1.0 / 3.0) < self.observation_accuracy < 1.0:
            raise ValueError("observation_accuracy must lie in (1/3, 1)")


def categorical_entropy_normalized(probabilities) -> float:
    p = np.asarray(probabilities, dtype=float)
    if p.shape != (3,):
        raise ValueError("probabilities must have shape (3,)")
    if np.any(p < 0.0) or not np.isclose(float(np.sum(p)), 1.0):
        raise ValueError("probabilities must be nonnegative and sum to one")
    positive = p[p > 0.0]
    h = -float(np.sum(positive * np.log2(positive)))
    return h / math.log2(3.0)


def generate_three_state_episode(config: ThreeStateTrackingConfig, seed: int):
    rng = np.random.default_rng(seed)
    states = np.empty(config.steps, dtype=int)
    observations = np.empty(config.steps, dtype=int)
    state = int(rng.integers(0, 3))
    wrong_choices = np.arange(3)
    for t in range(config.steps):
        if t > 0 and rng.random() < config.switch_probability:
            choices = wrong_choices[wrong_choices != state]
            state = int(rng.choice(choices))
        states[t] = state
        if rng.random() < config.observation_accuracy:
            observations[t] = state
        else:
            choices = wrong_choices[wrong_choices != state]
            observations[t] = int(rng.choice(choices))
    return states, observations


def filter_three_state_markov(
    observations,
    switch_probability: float = 0.10,
    observation_accuracy: float = 0.65,
):
    observations = np.asarray(observations, dtype=int)
    if np.any((observations < 0) | (observations > 2)):
        raise ValueError("observations must be in {0,1,2}")
    if not 0.0 <= switch_probability <= 1.0:
        raise ValueError("switch_probability must lie in [0,1]")
    if not (1.0 / 3.0) < observation_accuracy < 1.0:
        raise ValueError("observation_accuracy must lie in (1/3,1)")

    stay = 1.0 - switch_probability
    move = switch_probability / 2.0
    transition = np.full((3, 3), move, dtype=float)
    np.fill_diagonal(transition, stay)

    belief = np.full(3, 1.0 / 3.0, dtype=float)
    out = np.empty((len(observations), 3), dtype=float)
    error_prob = (1.0 - observation_accuracy) / 2.0
    for t, y in enumerate(observations):
        pred = belief @ transition
        likelihood = np.full(3, error_prob, dtype=float)
        likelihood[int(y)] = observation_accuracy
        post = pred * likelihood
        belief = post / np.sum(post)
        out[t] = belief
    return out


def deterministic_value_probabilities(belief) -> np.ndarray:
    belief = np.asarray(belief, dtype=float)
    probs = np.zeros(3, dtype=float)
    probs[int(np.argmax(belief))] = 1.0
    return probs


def utility_topset_chaos_probabilities(belief, utility_gap: float = 0.30) -> np.ndarray:
    if utility_gap <= 0.0:
        raise ValueError("utility_gap must be positive")
    belief = np.asarray(belief, dtype=float)
    if belief.shape != (3,):
        raise ValueError("belief must have shape (3,)")
    utilities = 2.0 * belief - 1.0
    best = int(np.argmax(utilities))
    viable = np.flatnonzero(np.max(utilities) - utilities <= utility_gap + 1e-15)
    probs = np.zeros(3, dtype=float)
    if len(viable) == 1:
        probs[best] = 1.0
        return probs
    probs[best] = 0.60
    others = viable[viable != best]
    probs[others] = 0.40 / len(others)
    return probs


_FROZEN_PERTURBATIONS = np.random.default_rng(8080).uniform(-0.18, 0.18, size=(129, 3))


def perturbed_utility_chaos_probabilities(belief) -> np.ndarray:
    belief = np.asarray(belief, dtype=float)
    if belief.shape != (3,):
        raise ValueError("belief must have shape (3,)")
    utilities = 2.0 * belief - 1.0
    winners = np.argmax(utilities[None, :] + _FROZEN_PERTURBATIONS, axis=1)
    counts = np.bincount(winners, minlength=3).astype(float)
    return counts / float(len(winners))


@lru_cache(maxsize=None)
def _cached_three_state_environment(config: ThreeStateTrackingConfig, seed: int):
    """Cache the environment/belief path shared by all policies for one frozen cell."""
    states, observations = generate_three_state_episode(config, seed)
    beliefs = filter_three_state_markov(
        observations,
        switch_probability=config.switch_probability,
        observation_accuracy=config.observation_accuracy,
    )
    states.setflags(write=False)
    observations.setflags(write=False)
    beliefs.setflags(write=False)
    return states, observations, beliefs


def simulate_three_action_policy_episode(
    policy: str,
    config: ThreeStateTrackingConfig,
    seed: int,
):
    states, observations, beliefs = _cached_three_state_environment(config, int(seed))
    offsets = {
        "deterministic_value": 80_001,
        "uniform_random": 80_002,
        "utility_topset_chaos": 80_003,
        "perturbed_utility_chaos": 80_004,
    }
    if policy not in offsets:
        raise ValueError(f"unknown three-action policy: {policy}")
    rng = np.random.default_rng(seed + offsets[policy])

    if policy == "deterministic_value":
        probs = np.asarray([deterministic_value_probabilities(b) for b in beliefs])
        actions = np.argmax(probs, axis=1).astype(int)
    elif policy == "uniform_random":
        probs = np.full((config.steps, 3), 1.0 / 3.0, dtype=float)
        actions = np.asarray([rng.choice(3, p=p) for p in probs], dtype=int)
    elif policy == "utility_topset_chaos":
        probs = np.asarray([utility_topset_chaos_probabilities(b) for b in beliefs])
        actions = np.asarray([rng.choice(3, p=p) for p in probs], dtype=int)
    else:
        probs = np.asarray([perturbed_utility_chaos_probabilities(b) for b in beliefs])
        utilities = 2.0 * beliefs - 1.0
        perturb = rng.uniform(-0.18, 0.18, size=(config.steps, 3))
        actions = np.argmax(utilities + perturb, axis=1).astype(int)

    correct = actions == states
    rewards = np.where(correct, 1.0, -1.0)
    entropies = np.asarray([categorical_entropy_normalized(p) for p in probs])
    support_sizes = np.sum(probs > 1e-12, axis=1)
    return {
        "states": states,
        "observations": observations,
        "beliefs": beliefs,
        "action_probabilities": probs,
        "actions": actions,
        "accuracy": float(np.mean(correct)),
        "mean_reward": float(np.mean(rewards)),
        "policy_entropy": float(np.mean(entropies)),
        "support_sizes": support_sizes,
    }


class OnlineSoftmaxExploiter:
    """Online three-class softmax regression over frozen public-context features."""

    def __init__(self, learning_rate=0.08, l2=0.001, calibration_passes=4):
        if learning_rate <= 0.0:
            raise ValueError("learning_rate must be positive")
        if l2 < 0.0:
            raise ValueError("l2 must be nonnegative")
        if calibration_passes < 1:
            raise ValueError("calibration_passes must be positive")
        self.learning_rate = float(learning_rate)
        self.l2 = float(l2)
        self.calibration_passes = int(calibration_passes)
        self.weights = np.zeros((3, 13), dtype=float)

    @staticmethod
    def _active_indices(observations, actions, t):
        if t < 2:
            return None
        return (
            0,
            1 + int(observations[t]),
            4 + int(observations[t - 1]),
            7 + int(actions[t - 1]),
            10 + int(actions[t - 2]),
        )

    @staticmethod
    def _features(observations, actions, t):
        idx = OnlineSoftmaxExploiter._active_indices(observations, actions, t)
        if idx is None:
            return None
        x = np.zeros(13, dtype=float)
        x[list(idx)] = 1.0
        return x

    @staticmethod
    def _softmax(logits):
        logits = logits - np.max(logits)
        e = np.exp(logits)
        return e / np.sum(e)

    def predict_proba_x(self, x):
        return self._softmax(self.weights @ x)

    def _predict_proba_indices(self, idx):
        return self._softmax(np.sum(self.weights[:, idx], axis=1))

    def predict_at(self, observations, actions, t) -> int:
        idx = self._active_indices(observations, actions, t)
        if idx is None:
            return 0
        return int(np.argmax(self._predict_proba_indices(idx)))

    def _update_indices(self, idx, action):
        probs = self._predict_proba_indices(idx)
        target = np.zeros(3, dtype=float)
        target[int(action)] = 1.0
        error = probs - target
        # Equivalent to dense SGD on gradient + L2 penalty, exploiting the
        # frozen one-hot feature structure for speed.
        self.weights *= 1.0 - self.learning_rate * self.l2
        for j in idx:
            self.weights[:, j] -= self.learning_rate * error

    def fit(self, episodes):
        for _ in range(self.calibration_passes):
            for ep in episodes:
                observations = np.asarray(ep["observations"], dtype=int)
                actions = np.asarray(ep["actions"], dtype=int)
                for t in range(2, len(actions)):
                    idx = self._active_indices(observations, actions, t)
                    self._update_indices(idx, actions[t])
        return self

    def prequential_accuracy(self, episodes, masks=None) -> float:
        correct = 0
        total = 0
        for i, ep in enumerate(episodes):
            observations = np.asarray(ep["observations"], dtype=int)
            actions = np.asarray(ep["actions"], dtype=int)
            mask = None if masks is None else np.asarray(masks[i], dtype=bool)
            for t in range(2, len(actions)):
                idx = self._active_indices(observations, actions, t)
                pred = int(np.argmax(self._predict_proba_indices(idx)))
                if mask is None or bool(mask[t]):
                    correct += int(pred == actions[t])
                    total += 1
                self._update_indices(idx, actions[t])
        return float(correct / total) if total else float("nan")

    def prequential_accuracies(self, episodes, masks_by_name):
        """Score several frozen masks in one identical predict-then-update pass."""
        names = tuple(masks_by_name)
        correct = {name: 0 for name in names}
        total = {name: 0 for name in names}
        for i, ep in enumerate(episodes):
            observations = np.asarray(ep["observations"], dtype=int)
            actions = np.asarray(ep["actions"], dtype=int)
            masks = {
                name: (None if masks_by_name[name] is None else np.asarray(masks_by_name[name][i], dtype=bool))
                for name in names
            }
            for t in range(2, len(actions)):
                idx = self._active_indices(observations, actions, t)
                pred = int(np.argmax(self._predict_proba_indices(idx)))
                hit = int(pred == actions[t])
                for name in names:
                    mask = masks[name]
                    if mask is None or bool(mask[t]):
                        correct[name] += hit
                        total[name] += 1
                self._update_indices(idx, actions[t])
        return {name: (float(correct[name] / total[name]) if total[name] else float("nan")) for name in names}

def _fit_and_score(policy, config, calibration_seeds, evaluation_seeds, masks=None):
    calibration = [simulate_three_action_policy_episode(policy, config, int(s)) for s in calibration_seeds]
    evaluation = [simulate_three_action_policy_episode(policy, config, int(s)) for s in evaluation_seeds]
    exploiter = OnlineSoftmaxExploiter().fit(calibration)
    score = exploiter.prequential_accuracy(evaluation, masks=masks)
    return evaluation, score


def evaluate_three_action_transfer(candidate, config, calibration_seeds, evaluation_seeds):
    if candidate not in {"utility_topset_chaos", "perturbed_utility_chaos"}:
        raise ValueError("candidate must be a frozen three-action Chaos policy")

    calibration_seeds = list(calibration_seeds)
    evaluation_seeds = list(evaluation_seeds)
    candidate_cal = [simulate_three_action_policy_episode(candidate, config, int(s)) for s in calibration_seeds]
    candidate_eval = [simulate_three_action_policy_episode(candidate, config, int(s)) for s in evaluation_seeds]
    baseline_cal = [simulate_three_action_policy_episode("deterministic_value", config, int(s)) for s in calibration_seeds]
    baseline_eval = [simulate_three_action_policy_episode("deterministic_value", config, int(s)) for s in evaluation_seeds]
    random_eval = [simulate_three_action_policy_episode("uniform_random", config, int(s)) for s in evaluation_seeds]

    branch_masks = [ep["support_sizes"] >= 2 for ep in candidate_eval]
    three_masks = [ep["support_sizes"] == 3 for ep in candidate_eval]
    score_masks = {"global": None, "branch": branch_masks, "three": three_masks}

    candidate_scores = OnlineSoftmaxExploiter().fit(candidate_cal).prequential_accuracies(candidate_eval, score_masks)
    # The matched baseline uses the same candidate-defined masks.
    baseline_scores = OnlineSoftmaxExploiter().fit(baseline_cal).prequential_accuracies(
        baseline_eval, {"global": None, "branch": branch_masks}
    )

    return {
        "candidate_policy": candidate,
        "candidate_mean_accuracy": float(np.mean([ep["accuracy"] for ep in candidate_eval])),
        "baseline_mean_accuracy": float(np.mean([ep["accuracy"] for ep in baseline_eval])),
        "candidate_mean_reward": float(np.mean([ep["mean_reward"] for ep in candidate_eval])),
        "baseline_mean_reward": float(np.mean([ep["mean_reward"] for ep in baseline_eval])),
        "random_mean_reward": float(np.mean([ep["mean_reward"] for ep in random_eval])),
        "candidate_policy_entropy": float(np.mean([ep["policy_entropy"] for ep in candidate_eval])),
        "baseline_policy_entropy": float(np.mean([ep["policy_entropy"] for ep in baseline_eval])),
        "candidate_global_softmax_accuracy": candidate_scores["global"],
        "baseline_global_softmax_accuracy": baseline_scores["global"],
        "candidate_branch_softmax_accuracy": candidate_scores["branch"],
        "baseline_branch_softmax_accuracy": baseline_scores["branch"],
        "candidate_three_way_softmax_accuracy": candidate_scores["three"],
        "opportunity_exploitability_reduction": baseline_scores["branch"] - candidate_scores["branch"],
        "branch_opportunity_fraction": float(np.mean([np.mean(m) for m in branch_masks])),
        "three_way_opportunity_fraction": float(np.mean([np.mean(m) for m in three_masks])),
        "mean_support_size": float(np.mean([np.mean(ep["support_sizes"]) for ep in candidate_eval])),
        "episodes": len(candidate_eval),
    }



def summarize_three_action_affordance(policy, config, evaluation_seeds):
    """Summarize fixed-policy branch affordances without fitting an exploiter."""
    if policy not in {"utility_topset_chaos", "perturbed_utility_chaos"}:
        raise ValueError("policy must be a frozen three-action Chaos policy")
    episodes = [
        simulate_three_action_policy_episode(policy, config, int(seed))
        for seed in evaluation_seeds
    ]
    branch = [ep["support_sizes"] >= 2 for ep in episodes]
    three = [ep["support_sizes"] == 3 for ep in episodes]
    return {
        "candidate_policy": policy,
        "observation_accuracy": float(config.observation_accuracy),
        "switch_probability": float(config.switch_probability),
        "branch_opportunity_fraction": float(np.mean([np.mean(mask) for mask in branch])),
        "three_way_opportunity_fraction": float(np.mean([np.mean(mask) for mask in three])),
        "mean_support_size": float(np.mean([np.mean(ep["support_sizes"]) for ep in episodes])),
        "policy_entropy": float(np.mean([ep["policy_entropy"] for ep in episodes])),
        "mean_reward": float(np.mean([ep["mean_reward"] for ep in episodes])),
        "mean_accuracy": float(np.mean([ep["accuracy"] for ep in episodes])),
        "episodes": len(episodes),
    }

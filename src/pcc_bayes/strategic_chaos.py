from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class TrackingConfig:
    steps: int = 400
    switch_probability: float = 0.08
    observation_accuracy: float = 0.75
    extra_corruption: float = 0.25

    def __post_init__(self):
        if self.steps < 1:
            raise ValueError("steps must be positive")
        if not 0.0 <= self.switch_probability <= 1.0:
            raise ValueError("switch_probability must lie in [0, 1]")
        if not 0.5 < self.observation_accuracy < 1.0:
            raise ValueError("observation_accuracy must lie in (0.5, 1)")
        if not 0.0 <= self.extra_corruption <= 0.5:
            raise ValueError("extra_corruption must lie in [0, 0.5]")


def binary_entropy(p: float) -> float:
    """Bernoulli entropy in bits, normalized to [0, 1]."""
    p = float(np.clip(p, 0.0, 1.0))
    if p in (0.0, 1.0):
        return 0.0
    return float(-(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p)))


def generate_tracking_episode(config: TrackingConfig, seed: int):
    """Generate hidden states and raw observations for the switching task."""
    rng = np.random.default_rng(seed)
    states = np.empty(config.steps, dtype=int)
    observations = np.empty(config.steps, dtype=int)
    state = int(rng.integers(0, 2))
    for t in range(config.steps):
        if t > 0 and rng.random() < config.switch_probability:
            state = 1 - state
        states[t] = state
        observations[t] = state if rng.random() < config.observation_accuracy else 1 - state
    return states, observations


def corrupt_observations(observations, rate: float, seed: int):
    observations = np.asarray(observations, dtype=int)
    if np.any((observations != 0) & (observations != 1)):
        raise ValueError("observations must be binary")
    if not 0.0 <= rate <= 0.5:
        raise ValueError("rate must lie in [0, 0.5]")
    rng = np.random.default_rng(seed)
    flips = rng.random(len(observations)) < rate
    return np.where(flips, 1 - observations, observations).astype(int)


def filter_binary_markov(observations, switch_probability=0.08, observation_accuracy=0.75):
    """Correct Bayesian filter for a symmetric binary hidden Markov state."""
    observations = np.asarray(observations, dtype=int)
    if np.any((observations != 0) & (observations != 1)):
        raise ValueError("observations must be binary")
    p1 = 0.5
    out = np.empty(len(observations), dtype=float)
    for i, y in enumerate(observations):
        # prediction under symmetric switching
        p1_pred = p1 * (1.0 - switch_probability) + (1.0 - p1) * switch_probability
        like1 = observation_accuracy if y == 1 else 1.0 - observation_accuracy
        like0 = observation_accuracy if y == 0 else 1.0 - observation_accuracy
        num = like1 * p1_pred
        den = num + like0 * (1.0 - p1_pred)
        p1 = num / den
        out[i] = p1
    return out


def predictable_value_prob(p1: float) -> float:
    return 1.0 if p1 >= 0.5 else 0.0


def structured_chaos_prob(p1: float) -> float:
    """Value-aware mixing: stochastic near indifference, greedy when confident."""
    confidence = abs(2.0 * float(p1) - 1.0)
    non_map = 0.45 * max(0.0, 1.0 - confidence / 0.60)
    if p1 >= 0.5:
        return 1.0 - non_map
    return non_map


def threshold_chaos_prob(p1: float, low: float = 0.25, high: float = 0.75) -> float:
    """Marginal action probability for a uniformly sampled decision threshold.

    A fresh threshold T ~ Uniform(low, high) is drawn and action 1 is selected
    iff p1 >= T. This is an independent policy architecture from
    ``structured_chaos_prob``: stochasticity enters through the criterion, not
    through an explicit non-MAP mixing weight.
    """
    if not 0.0 <= low < high <= 1.0:
        raise ValueError("threshold bounds must satisfy 0 <= low < high <= 1")
    p1 = float(p1)
    return float(np.clip((p1 - low) / (high - low), 0.0, 1.0))


def simulate_policy_episode(policy: str, config: TrackingConfig, seed: int):
    states, observations = generate_tracking_episode(config, seed)
    clean_beliefs = filter_binary_markov(
        observations, config.switch_probability, config.observation_accuracy
    )

    if policy == "corrupted_predictable":
        policy_observations = corrupt_observations(
            observations, config.extra_corruption, seed + 20_000
        )
        beliefs = filter_binary_markov(
            policy_observations, config.switch_probability, config.observation_accuracy
        )
    else:
        beliefs = clean_beliefs

    rng = np.random.default_rng(seed + {
        "predictable_value": 10_001,
        "uniform_random": 10_002,
        "corrupted_predictable": 10_003,
        "structured_chaos": 10_004,
        "threshold_chaos": 10_005,
    }[policy])

    if policy == "predictable_value" or policy == "corrupted_predictable":
        probs = np.asarray([predictable_value_prob(p) for p in beliefs], dtype=float)
    elif policy == "uniform_random":
        probs = np.full(config.steps, 0.5, dtype=float)
    elif policy == "structured_chaos":
        probs = np.asarray([structured_chaos_prob(p) for p in beliefs], dtype=float)
    elif policy == "threshold_chaos":
        # Preserve the marginal probabilities for entropy accounting, while the
        # realized action is generated below by an explicit sampled threshold.
        probs = np.asarray([threshold_chaos_prob(p) for p in beliefs], dtype=float)
    else:
        raise ValueError(f"unknown policy: {policy}")

    if policy == "threshold_chaos":
        thresholds = rng.uniform(0.25, 0.75, size=config.steps)
        actions = (beliefs >= thresholds).astype(int)
    else:
        actions = (rng.random(config.steps) < probs).astype(int)
    accuracy = float(np.mean(actions == states))
    entropy = float(np.mean([binary_entropy(p) for p in probs]))
    return {
        "states": states,
        "observations": observations,
        "beliefs": beliefs,
        "action_probabilities": probs,
        "actions": actions,
        "accuracy": accuracy,
        "policy_entropy": entropy,
    }


class HistoryExploiter:
    """Frozen n-gram predictor over public action history."""

    def __init__(self, order=3, alpha=1.0):
        if order < 1:
            raise ValueError("order must be positive")
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        self.order = int(order)
        self.alpha = float(alpha)
        self._counts = {}
        self._global = np.array([alpha, alpha], dtype=float)

    def fit(self, action_sequences):
        self._counts = {}
        self._global = np.array([self.alpha, self.alpha], dtype=float)
        for seq in action_sequences:
            seq = np.asarray(seq, dtype=int)
            for action in seq:
                self._global[action] += 1.0
            for t in range(self.order, len(seq)):
                key = tuple(int(x) for x in seq[t - self.order:t])
                if key not in self._counts:
                    self._counts[key] = np.array([self.alpha, self.alpha], dtype=float)
                self._counts[key][seq[t]] += 1.0
        return self

    def predict_one(self, history) -> int:
        history = np.asarray(history, dtype=int)
        if len(history) < self.order:
            counts = self._global
        else:
            key = tuple(int(x) for x in history[-self.order:])
            counts = self._counts.get(key, self._global)
        # deterministic tie-breaking is frozen to action 1
        return int(counts[1] >= counts[0])

    def accuracy(self, action_sequences) -> float:
        correct = 0
        total = 0
        for seq in action_sequences:
            seq = np.asarray(seq, dtype=int)
            for t in range(self.order, len(seq)):
                pred = self.predict_one(seq[:t])
                correct += int(pred == seq[t])
                total += 1
        return float(correct / total) if total else float("nan")


def evaluate_policy_family(policy: str, config: TrackingConfig, calibration_seeds, evaluation_seeds):
    calibration = [simulate_policy_episode(policy, config, int(seed)) for seed in calibration_seeds]
    evaluation = [simulate_policy_episode(policy, config, int(seed)) for seed in evaluation_seeds]

    exploiter = HistoryExploiter(order=3, alpha=1.0).fit([x["actions"] for x in calibration])
    exploit_accuracy = exploiter.accuracy([x["actions"] for x in evaluation])
    return {
        "policy": policy,
        "mean_accuracy": float(np.mean([x["accuracy"] for x in evaluation])),
        "mean_policy_entropy": float(np.mean([x["policy_entropy"] for x in evaluation])),
        "exploiter_accuracy": exploit_accuracy,
        "episodes": len(evaluation),
    }


class ContextExploiter:
    """Frozen lookup predictor using public evidence context and past actions."""

    def __init__(self, observation_order=2, action_order=2, alpha=1.0):
        if observation_order < 1 or action_order < 0:
            raise ValueError("invalid context orders")
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        self.observation_order = int(observation_order)
        self.action_order = int(action_order)
        self.alpha = float(alpha)
        self._counts = {}
        self._global = np.array([alpha, alpha], dtype=float)

    def _key(self, observations, actions, t):
        if t + 1 < self.observation_order or t < self.action_order:
            return None
        obs = tuple(int(x) for x in observations[t + 1 - self.observation_order:t + 1])
        acts = tuple(int(x) for x in actions[t - self.action_order:t]) if self.action_order else ()
        return obs + acts

    def fit(self, episodes):
        self._counts = {}
        self._global = np.array([self.alpha, self.alpha], dtype=float)
        for episode in episodes:
            observations = np.asarray(episode["observations"], dtype=int)
            actions = np.asarray(episode["actions"], dtype=int)
            for action in actions:
                self._global[action] += 1.0
            for t in range(len(actions)):
                key = self._key(observations, actions, t)
                if key is None:
                    continue
                if key not in self._counts:
                    self._counts[key] = np.array([self.alpha, self.alpha], dtype=float)
                self._counts[key][actions[t]] += 1.0
        return self

    def predict_at(self, observations, actions, t) -> int:
        key = self._key(observations, actions, t)
        counts = self._global if key is None else self._counts.get(key, self._global)
        return int(counts[1] >= counts[0])

    def accuracy(self, episodes, mask_fn=None) -> float:
        correct = 0
        total = 0
        for episode in episodes:
            observations = np.asarray(episode["observations"], dtype=int)
            actions = np.asarray(episode["actions"], dtype=int)
            for t in range(len(actions)):
                if self._key(observations, actions, t) is None:
                    continue
                if mask_fn is not None and not mask_fn(episode, t):
                    continue
                pred = self.predict_at(observations, actions, t)
                correct += int(pred == actions[t])
                total += 1
        return float(correct / total) if total else float("nan")


def evaluate_context_exploitability(policy: str, config: TrackingConfig, calibration_seeds, evaluation_seeds):
    calibration = [simulate_policy_episode(policy, config, int(seed)) for seed in calibration_seeds]
    evaluation = [simulate_policy_episode(policy, config, int(seed)) for seed in evaluation_seeds]
    exploiter = ContextExploiter(observation_order=2, action_order=2, alpha=1.0).fit(calibration)

    def mixing_opportunity(episode, t):
        p = float(episode["action_probabilities"][t])
        return 0.0 < p < 1.0

    return {
        "policy": policy,
        "context_exploiter_accuracy": exploiter.accuracy(evaluation),
        "mixing_opportunity_exploiter_accuracy": exploiter.accuracy(evaluation, mask_fn=mixing_opportunity),
        "mixing_opportunity_fraction": float(np.mean([
            np.mean((ep["action_probabilities"] > 0.0) & (ep["action_probabilities"] < 1.0))
            for ep in evaluation
        ])),
    }


class AdaptiveContextExploiter(ContextExploiter):
    """Context exploiter that updates after every revealed evaluation action."""

    def update_at(self, observations, actions, t):
        observations = np.asarray(observations, dtype=int)
        actions = np.asarray(actions, dtype=int)
        action = int(actions[t])
        self._global[action] += 1.0
        key = self._key(observations, actions, t)
        if key is not None:
            if key not in self._counts:
                self._counts[key] = np.array([self.alpha, self.alpha], dtype=float)
            self._counts[key][action] += 1.0

    def prequential_accuracy(self, episodes, mask_fn=None) -> float:
        """Predict then update online, retaining learned counts across episodes."""
        correct = 0
        total = 0
        for episode in episodes:
            observations = np.asarray(episode["observations"], dtype=int)
            actions = np.asarray(episode["actions"], dtype=int)
            for t in range(len(actions)):
                key = self._key(observations, actions, t)
                if key is None:
                    continue
                use = mask_fn is None or mask_fn(episode, t)
                if use:
                    pred = self.predict_at(observations, actions, t)
                    correct += int(pred == actions[t])
                    total += 1
                self.update_at(observations, actions, t)
        return float(correct / total) if total else float("nan")


def evaluate_adaptive_exploitability(policy: str, config: TrackingConfig, calibration_seeds, evaluation_seeds):
    calibration = [simulate_policy_episode(policy, config, int(seed)) for seed in calibration_seeds]
    evaluation = [simulate_policy_episode(policy, config, int(seed)) for seed in evaluation_seeds]
    exploiter = AdaptiveContextExploiter(observation_order=2, action_order=2, alpha=1.0).fit(calibration)

    def mixing_opportunity(episode, t):
        p = float(episode["action_probabilities"][t])
        return 0.0 < p < 1.0

    adaptive_accuracy = exploiter.prequential_accuracy(evaluation)

    # Use a fresh copy so the subset diagnostic sees the same frozen initial
    # condition rather than a twice-adapted exploiter.
    subset_exploiter = AdaptiveContextExploiter(observation_order=2, action_order=2, alpha=1.0).fit(calibration)
    mixing_accuracy = subset_exploiter.prequential_accuracy(evaluation, mask_fn=mixing_opportunity)

    return {
        "policy": policy,
        "mean_accuracy": float(np.mean([x["accuracy"] for x in evaluation])),
        "mean_policy_entropy": float(np.mean([x["policy_entropy"] for x in evaluation])),
        "adaptive_exploiter_accuracy": adaptive_accuracy,
        "mixing_opportunity_adaptive_accuracy": mixing_accuracy,
        "mixing_opportunity_fraction": float(np.mean([
            np.mean((ep["action_probabilities"] > 0.0) & (ep["action_probabilities"] < 1.0))
            for ep in evaluation
        ])),
        "episodes": len(evaluation),
    }


@dataclass(frozen=True)
class AsymmetricPayoffs:
    reward_state0_action0: float = 1.0
    reward_state0_action1: float = -2.0
    reward_state1_action0: float = -0.5
    reward_state1_action1: float = 1.0

    def expected_rewards(self, p1: float):
        p1 = float(p1)
        p0 = 1.0 - p1
        u0 = p0 * self.reward_state0_action0 + p1 * self.reward_state1_action0
        u1 = p0 * self.reward_state0_action1 + p1 * self.reward_state1_action1
        return float(u0), float(u1)

    @property
    def indifference_threshold(self) -> float:
        # Solve U(action 0) = U(action 1) for p=P(state=1).
        a0 = self.reward_state0_action0
        b0 = self.reward_state1_action0 - self.reward_state0_action0
        a1 = self.reward_state0_action1
        b1 = self.reward_state1_action1 - self.reward_state0_action1
        den = b1 - b0
        if den == 0:
            raise ValueError("payoff matrix has no unique posterior indifference threshold")
        threshold = (a0 - a1) / den
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("payoff indifference lies outside [0, 1]")
        return float(threshold)

    def realized_reward(self, state: int, action: int) -> float:
        if state == 0 and action == 0:
            return float(self.reward_state0_action0)
        if state == 0 and action == 1:
            return float(self.reward_state0_action1)
        if state == 1 and action == 0:
            return float(self.reward_state1_action0)
        if state == 1 and action == 1:
            return float(self.reward_state1_action1)
        raise ValueError("state and action must be binary")


def predictable_utility_prob(p1: float, payoffs: AsymmetricPayoffs | None = None) -> float:
    payoffs = payoffs or AsymmetricPayoffs()
    return 1.0 if float(p1) >= payoffs.indifference_threshold else 0.0


def utility_structured_chaos_prob(
    p1: float,
    payoffs: AsymmetricPayoffs | None = None,
    mixing_width: float = 0.18,
    max_non_greedy: float = 0.45,
) -> float:
    """Value-aware mixing around the payoff indifference point."""
    if mixing_width <= 0:
        raise ValueError("mixing_width must be positive")
    if not 0.0 <= max_non_greedy <= 0.5:
        raise ValueError("max_non_greedy must lie in [0, 0.5]")
    payoffs = payoffs or AsymmetricPayoffs()
    threshold = payoffs.indifference_threshold
    distance = abs(float(p1) - threshold)
    non_greedy = max_non_greedy * max(0.0, 1.0 - distance / mixing_width)
    greedy_action1 = predictable_utility_prob(p1, payoffs) == 1.0
    return float(1.0 - non_greedy if greedy_action1 else non_greedy)


def utility_threshold_chaos_prob(
    p1: float,
    payoffs: AsymmetricPayoffs | None = None,
    half_width: float = 0.20,
) -> float:
    """Marginal action-1 probability from a sampled utility decision threshold."""
    if half_width <= 0:
        raise ValueError("half_width must be positive")
    payoffs = payoffs or AsymmetricPayoffs()
    center = payoffs.indifference_threshold
    low = center - half_width
    high = center + half_width
    if low < 0.0 or high > 1.0:
        raise ValueError("threshold interval must remain inside [0, 1]")
    return float(np.clip((float(p1) - low) / (high - low), 0.0, 1.0))


def simulate_asymmetric_policy_episode(
    policy: str,
    config: TrackingConfig,
    seed: int,
    payoffs: AsymmetricPayoffs | None = None,
):
    payoffs = payoffs or AsymmetricPayoffs()
    states, observations = generate_tracking_episode(config, seed)
    beliefs = filter_binary_markov(
        observations, config.switch_probability, config.observation_accuracy
    )
    offsets = {
        "predictable_utility": 30_001,
        "uniform_random": 30_002,
        "utility_structured_chaos": 30_003,
        "utility_threshold_chaos": 30_004,
    }
    if policy not in offsets:
        raise ValueError(f"unknown asymmetric policy: {policy}")
    rng = np.random.default_rng(seed + offsets[policy])

    if policy == "predictable_utility":
        probs = np.asarray([predictable_utility_prob(p, payoffs) for p in beliefs], dtype=float)
        actions = probs.astype(int)
    elif policy == "uniform_random":
        probs = np.full(config.steps, 0.5, dtype=float)
        actions = (rng.random(config.steps) < probs).astype(int)
    elif policy == "utility_structured_chaos":
        probs = np.asarray([utility_structured_chaos_prob(p, payoffs) for p in beliefs], dtype=float)
        actions = (rng.random(config.steps) < probs).astype(int)
    else:
        probs = np.asarray([utility_threshold_chaos_prob(p, payoffs) for p in beliefs], dtype=float)
        center = payoffs.indifference_threshold
        thresholds = rng.uniform(center - 0.20, center + 0.20, size=config.steps)
        actions = (beliefs >= thresholds).astype(int)

    rewards = np.asarray(
        [payoffs.realized_reward(int(s), int(a)) for s, a in zip(states, actions)],
        dtype=float,
    )
    return {
        "states": states,
        "observations": observations,
        "beliefs": beliefs,
        "action_probabilities": probs,
        "actions": actions,
        "rewards": rewards,
        "mean_reward": float(np.mean(rewards)),
        "accuracy": float(np.mean(actions == states)),
        "policy_entropy": float(np.mean([binary_entropy(p) for p in probs])),
    }


class OnlineLogisticExploiter:
    """Online logistic action predictor over public context features."""

    def __init__(self, learning_rate=0.05, l2=0.001, calibration_passes=5):
        if learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if l2 < 0:
            raise ValueError("l2 must be nonnegative")
        if calibration_passes < 1:
            raise ValueError("calibration_passes must be positive")
        self.learning_rate = float(learning_rate)
        self.l2 = float(l2)
        self.calibration_passes = int(calibration_passes)
        self.weights = np.zeros(7, dtype=float)

    @staticmethod
    def _sigmoid(z: float) -> float:
        if z >= 0:
            return float(1.0 / (1.0 + math.exp(-z)))
        ez = math.exp(z)
        return float(ez / (1.0 + ez))

    def _features(self, observations, actions, t):
        observations = np.asarray(observations, dtype=int)
        actions = np.asarray(actions, dtype=int)
        if t < 2:
            return None
        cur_obs = float(observations[t])
        prev_obs = float(observations[t - 1])
        prev_action = float(actions[t - 1])
        prev2_action = float(actions[t - 2])
        return np.asarray(
            [
                1.0,
                cur_obs,
                prev_obs,
                prev_action,
                prev2_action,
                cur_obs * prev_action,
                prev_obs * prev_action,
            ],
            dtype=float,
        )

    def predict_probability(self, observations, actions, t) -> float:
        x = self._features(observations, actions, t)
        if x is None:
            return 0.5
        return self._sigmoid(float(np.dot(self.weights, x)))

    def predict_at(self, observations, actions, t) -> int:
        return int(self.predict_probability(observations, actions, t) >= 0.5)

    def update_at(self, observations, actions, t):
        x = self._features(observations, actions, t)
        if x is None:
            return
        y = float(np.asarray(actions, dtype=int)[t])
        p = self._sigmoid(float(np.dot(self.weights, x)))
        grad = (p - y) * x + self.l2 * self.weights
        self.weights -= self.learning_rate * grad

    def fit(self, episodes):
        self.weights = np.zeros(7, dtype=float)
        for _ in range(self.calibration_passes):
            for episode in episodes:
                observations = np.asarray(episode["observations"], dtype=int)
                actions = np.asarray(episode["actions"], dtype=int)
                for t in range(len(actions)):
                    self.update_at(observations, actions, t)
        return self

    def prequential_accuracy(self, episodes, mask_fn=None) -> float:
        correct = 0
        total = 0
        for episode in episodes:
            observations = np.asarray(episode["observations"], dtype=int)
            actions = np.asarray(episode["actions"], dtype=int)
            for t in range(len(actions)):
                if self._features(observations, actions, t) is None:
                    continue
                use = mask_fn is None or mask_fn(episode, t)
                if use:
                    pred = self.predict_at(observations, actions, t)
                    correct += int(pred == actions[t])
                    total += 1
                self.update_at(observations, actions, t)
        return float(correct / total) if total else float("nan")


def evaluate_asymmetric_logistic_exploitability(
    policy: str,
    config: TrackingConfig,
    calibration_seeds,
    evaluation_seeds,
    payoffs: AsymmetricPayoffs | None = None,
):
    payoffs = payoffs or AsymmetricPayoffs()
    calibration = [
        simulate_asymmetric_policy_episode(policy, config, int(seed), payoffs)
        for seed in calibration_seeds
    ]
    evaluation = [
        simulate_asymmetric_policy_episode(policy, config, int(seed), payoffs)
        for seed in evaluation_seeds
    ]

    exploiter = OnlineLogisticExploiter(
        learning_rate=0.05, l2=0.001, calibration_passes=5
    ).fit(calibration)

    def mixing_opportunity(episode, t):
        p = float(episode["action_probabilities"][t])
        return 0.0 < p < 1.0

    exploit_accuracy = exploiter.prequential_accuracy(evaluation)
    subset_exploiter = OnlineLogisticExploiter(
        learning_rate=0.05, l2=0.001, calibration_passes=5
    ).fit(calibration)
    mixing_accuracy = subset_exploiter.prequential_accuracy(
        evaluation, mask_fn=mixing_opportunity
    )

    return {
        "policy": policy,
        "mean_reward": float(np.mean([ep["mean_reward"] for ep in evaluation])),
        "mean_accuracy": float(np.mean([ep["accuracy"] for ep in evaluation])),
        "mean_policy_entropy": float(np.mean([ep["policy_entropy"] for ep in evaluation])),
        "logistic_exploiter_accuracy": exploit_accuracy,
        "mixing_opportunity_logistic_accuracy": mixing_accuracy,
        "mixing_opportunity_fraction": float(np.mean([
            np.mean((ep["action_probabilities"] > 0.0) & (ep["action_probabilities"] < 1.0))
            for ep in evaluation
        ])),
        "episodes": len(evaluation),
    }

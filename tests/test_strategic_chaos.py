import numpy as np

from pcc_bayes.strategic_chaos import (
    HistoryExploiter,
    TrackingConfig,
    binary_entropy,
    filter_binary_markov,
    simulate_policy_episode,
    structured_chaos_prob,
)


def test_binary_entropy_endpoints_and_half():
    assert binary_entropy(0.0) == 0.0
    assert binary_entropy(1.0) == 0.0
    assert np.isclose(binary_entropy(0.5), 1.0)


def test_filter_moves_toward_observation():
    beliefs = filter_binary_markov([1, 1, 1], switch_probability=0.08, observation_accuracy=0.75)
    assert beliefs[0] > 0.5
    assert beliefs[-1] > beliefs[0]


def test_structured_chaos_randomizes_near_indifference_only():
    assert np.isclose(structured_chaos_prob(0.5), 0.55)
    assert structured_chaos_prob(0.95) == 1.0
    assert structured_chaos_prob(0.05) == 0.0


def test_policy_episode_is_reproducible():
    config = TrackingConfig(steps=80)
    a = simulate_policy_episode("structured_chaos", config, seed=4)
    b = simulate_policy_episode("structured_chaos", config, seed=4)
    assert np.array_equal(a["actions"], b["actions"])
    assert np.array_equal(a["states"], b["states"])


def test_history_exploiter_learns_constant_sequence():
    exploiter = HistoryExploiter(order=3).fit([np.ones(30, dtype=int)])
    assert exploiter.accuracy([np.ones(30, dtype=int)]) == 1.0


def test_context_exploiter_learns_observation_action_mapping():
    from pcc_bayes.strategic_chaos import ContextExploiter
    episodes = []
    for _ in range(3):
        observations = np.tile([0, 1], 20)
        actions = observations.copy()
        episodes.append({
            "observations": observations,
            "actions": actions,
            "action_probabilities": actions.astype(float),
        })
    exploiter = ContextExploiter(observation_order=1, action_order=0).fit(episodes)
    assert exploiter.accuracy(episodes) == 1.0


def test_threshold_chaos_probability_has_frozen_bounds():
    from pcc_bayes.strategic_chaos import threshold_chaos_prob
    assert threshold_chaos_prob(0.20) == 0.0
    assert np.isclose(threshold_chaos_prob(0.50), 0.5)
    assert threshold_chaos_prob(0.80) == 1.0


def test_threshold_chaos_episode_is_reproducible():
    config = TrackingConfig(steps=80)
    a = simulate_policy_episode("threshold_chaos", config, seed=9)
    b = simulate_policy_episode("threshold_chaos", config, seed=9)
    assert np.array_equal(a["actions"], b["actions"])
    assert 0.0 < a["policy_entropy"] < 1.0


def test_adaptive_exploiter_updates_online():
    from pcc_bayes.strategic_chaos import AdaptiveContextExploiter
    observations = np.tile([0, 1], 30)
    actions = observations.copy()
    episode = {"observations": observations, "actions": actions, "action_probabilities": actions.astype(float)}
    exploiter = AdaptiveContextExploiter(observation_order=1, action_order=0).fit([])
    acc = exploiter.prequential_accuracy([episode])
    assert acc > 0.9

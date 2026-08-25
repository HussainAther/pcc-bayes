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


def test_asymmetric_payoff_threshold_is_two_thirds():
    from pcc_bayes.strategic_chaos import AsymmetricPayoffs
    payoffs = AsymmetricPayoffs()
    assert np.isclose(payoffs.indifference_threshold, 2.0 / 3.0)


def test_utility_policy_uses_asymmetric_threshold():
    from pcc_bayes.strategic_chaos import predictable_utility_prob
    assert predictable_utility_prob(0.60) == 0.0
    assert predictable_utility_prob(0.70) == 1.0


def test_utility_structured_chaos_mixes_at_value_indifference():
    from pcc_bayes.strategic_chaos import utility_structured_chaos_prob
    p = 2.0 / 3.0
    assert np.isclose(utility_structured_chaos_prob(p), 0.55)
    assert utility_structured_chaos_prob(0.20) == 0.0


def test_online_logistic_exploiter_learns_simple_mapping():
    from pcc_bayes.strategic_chaos import OnlineLogisticExploiter
    observations = np.tile([0, 1], 60)
    actions = observations.copy()
    episode = {
        "observations": observations,
        "actions": actions,
        "action_probabilities": actions.astype(float),
    }
    exploiter = OnlineLogisticExploiter(calibration_passes=5).fit([episode])
    acc = exploiter.prequential_accuracy([episode])
    assert acc > 0.95


def test_false_negative_costly_threshold_is_one_third():
    from pcc_bayes.strategic_chaos import AsymmetricPayoffs
    payoffs = AsymmetricPayoffs(
        reward_state0_action0=1.0,
        reward_state0_action1=-0.5,
        reward_state1_action0=-2.0,
        reward_state1_action1=1.0,
    )
    assert np.isclose(payoffs.indifference_threshold, 1.0 / 3.0)


def test_matched_opportunity_evaluation_uses_candidate_mask():
    from pcc_bayes.strategic_chaos import (
        AsymmetricPayoffs,
        TrackingConfig,
        evaluate_matched_opportunity_exploitability,
    )
    row = evaluate_matched_opportunity_exploitability(
        "utility_structured_chaos",
        TrackingConfig(steps=80),
        calibration_seeds=range(2),
        evaluation_seeds=range(10, 13),
        payoffs=AsymmetricPayoffs(),
    )
    assert 0.0 < row["opportunity_fraction"] < 1.0
    assert 0.0 <= row["candidate_opportunity_logistic_accuracy"] <= 1.0
    assert 0.0 <= row["baseline_opportunity_logistic_accuracy"] <= 1.0


def test_three_state_filter_rows_sum_to_one():
    from pcc_bayes.multiclass_chaos import filter_three_state_markov
    beliefs = filter_three_state_markov([0, 1, 2, 2, 1])
    assert beliefs.shape == (5, 3)
    assert np.allclose(np.sum(beliefs, axis=1), 1.0)


def test_topset_chaos_can_keep_three_actions_live():
    from pcc_bayes.multiclass_chaos import utility_topset_chaos_probabilities
    probs = utility_topset_chaos_probabilities(np.array([0.36, 0.34, 0.30]))
    assert np.count_nonzero(probs > 0.0) == 3
    assert np.isclose(np.sum(probs), 1.0)
    assert np.isclose(np.max(probs), 0.60)


def test_perturbed_utility_marginal_is_reproducible():
    from pcc_bayes.multiclass_chaos import perturbed_utility_chaos_probabilities
    belief = np.array([0.38, 0.34, 0.28])
    a = perturbed_utility_chaos_probabilities(belief)
    b = perturbed_utility_chaos_probabilities(belief)
    assert np.array_equal(a, b)
    assert np.isclose(np.sum(a), 1.0)


def test_three_action_episode_reproducible():
    from pcc_bayes.multiclass_chaos import ThreeStateTrackingConfig, simulate_three_action_policy_episode
    config = ThreeStateTrackingConfig(steps=80)
    a = simulate_three_action_policy_episode("utility_topset_chaos", config, 12)
    b = simulate_three_action_policy_episode("utility_topset_chaos", config, 12)
    assert np.array_equal(a["states"], b["states"])
    assert np.array_equal(a["actions"], b["actions"])


def test_online_softmax_exploiter_learns_current_observation_mapping():
    from pcc_bayes.multiclass_chaos import OnlineSoftmaxExploiter
    observations = np.tile([0, 1, 2], 80)
    actions = observations.copy()
    episode = {"observations": observations, "actions": actions}
    exploiter = OnlineSoftmaxExploiter(calibration_passes=5).fit([episode])
    assert exploiter.prequential_accuracy([episode]) > 0.95

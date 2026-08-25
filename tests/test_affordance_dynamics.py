import numpy as np

from pcc_bayes.affordance_dynamics import (
    analytical_filter_step,
    markov_prediction_map,
    observation_update_map,
    prediction_gap_contraction_residual,
)


def test_markov_prediction_contracts_pairwise_gaps():
    p = np.array([0.7, 0.2, 0.1])
    s = 0.30
    q = markov_prediction_map(p, s)
    assert np.isclose(q.sum(), 1.0)
    assert prediction_gap_contraction_residual(p, s) <= 1e-15
    assert np.isclose((q[0] - q[1]) / (p[0] - p[1]), 1.0 - 1.5 * s)


def test_observation_update_matches_direct_bayes():
    q = np.array([0.4, 0.35, 0.25])
    post = observation_update_map(q, observation=1, observation_accuracy=0.55)
    likelihood = np.array([0.225, 0.55, 0.225])
    expected = q * likelihood
    expected = expected / expected.sum()
    assert np.allclose(post, expected)


def test_analytical_step_is_normalized():
    _, post = analytical_filter_step(np.full(3, 1 / 3), 2, 0.1, 0.65)
    assert np.isclose(post.sum(), 1.0)
    assert np.all(post >= 0.0)

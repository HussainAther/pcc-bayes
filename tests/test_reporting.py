import numpy as np

from pcc_bayes.reporting import (
    action_loglik,
    action_one_probability,
    report_loglik,
    simulate_actions,
    simulate_reported_beliefs,
)


def test_report_simulation_stays_inside_unit_interval():
    beliefs = np.array([[0.5, 0.5], [0.2, 0.8], [0.9, 0.1]])
    reports = simulate_reported_beliefs(beliefs, sigma_logit=0.4, seed=2)
    assert np.all((reports > 0.0) & (reports < 1.0))


def test_exact_latent_reports_score_better_than_wrong_beliefs():
    beliefs = np.array([[0.5, 0.5], [0.25, 0.75], [0.1, 0.9]])
    wrong = beliefs[:, ::-1]
    reports = beliefs[:, 1]
    assert report_loglik(reports, beliefs, 0.2) > report_loglik(reports, wrong, 0.2)


def test_action_policy_and_likelihood_are_finite():
    beliefs = np.array([[0.5, 0.5], [0.2, 0.8], [0.8, 0.2]])
    actions = simulate_actions(beliefs, beta=2.0, seed=4)
    assert 0.0 < action_one_probability([0.2, 0.8], beta=2.0) < 1.0
    assert np.isfinite(action_loglik(actions, beliefs, beta=2.0))

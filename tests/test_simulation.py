import numpy as np
from pcc_bayes.simulation import simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.observables import belief_observables


def test_history_normalized():
    sim = simulate_binary_learning(steps=20, seed=1)
    assert np.allclose(sim["beliefs"].sum(axis=1), 1.0)


def test_standard_bayes_learns_in_expectation_long_run():
    sim = simulate_binary_learning(steps=1000, pcc=PCCParameters(1,1,0), seed=3)
    assert sim["beliefs"][-1, 1] > 0.99


def test_observable_lengths():
    sim = simulate_binary_learning(steps=10)
    obs = belief_observables(sim["beliefs"])
    assert len(obs["entropy"]) == 11
    assert len(obs["revision_js"]) == 11


def test_switch_records_both_true_states():
    sim = simulate_binary_learning(steps=20, switch_step=10, seed=2)
    assert set(sim["true_hypotheses"]) == {0, 1}

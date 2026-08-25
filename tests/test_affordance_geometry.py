import numpy as np

from pcc_bayes.affordance_geometry import (
    TopsetAffordanceGeometry,
    classify_topset_supports,
    support_fraction_summary,
)
from pcc_bayes.multiclass_chaos import utility_topset_chaos_probabilities


def test_frozen_topset_boundaries():
    g = TopsetAffordanceGeometry(utility_gap=0.30)
    assert np.isclose(g.posterior_gap, 0.15)
    assert g.support_size([0.60, 0.25, 0.15]) == 1
    assert g.support_size([0.50, 0.36, 0.14]) == 2
    assert g.support_size([0.40, 0.35, 0.25]) == 3
    # Equality at the 0.15 boundary remains viable.
    assert g.support_size([0.50, 0.35, 0.15]) == 2
    assert g.support_size([0.40, 0.35, 0.25]) == 3


def test_analytical_support_matches_policy_on_random_simplex():
    rng = np.random.default_rng(1010)
    beliefs = rng.dirichlet(np.ones(3), size=2000)
    predicted = classify_topset_supports(beliefs)
    implemented = np.asarray([
        np.sum(utility_topset_chaos_probabilities(b) > 1e-12) for b in beliefs
    ])
    assert np.array_equal(predicted, implemented)


def test_support_fraction_summary_partitions_probability():
    summary = support_fraction_summary([1, 1, 2, 3])
    assert np.isclose(summary["one_action_fraction"], 0.5)
    assert np.isclose(summary["two_action_fraction"], 0.25)
    assert np.isclose(summary["three_action_fraction"], 0.25)
    assert np.isclose(summary["branch_fraction"], 0.5)

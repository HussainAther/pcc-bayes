import numpy as np

from pcc_bayes.affordance_dynamics import analytical_filter_step
from pcc_bayes.affordance_geometry import TopsetAffordanceGeometry
from pcc_bayes.affordance_preimage import (
    affine_affordance_boundary,
    classify_affordance_preimage,
    score_boundary_value,
    unnormalized_update_scores,
)


def test_affine_boundary_equals_score_form():
    p = np.array([0.52, 0.31, 0.17])
    boundary = affine_affordance_boundary(1, 1, 0, 0.30, 0.55)
    expected = score_boundary_value(p, 1, 1, 0, 0.30, 0.55)
    assert abs(boundary.value(p) - expected) < 1e-15


def test_boundary_identity_matches_normalized_posterior_gap():
    p = np.array([0.21, 0.49, 0.30])
    y = 2
    s = 0.10
    a = 0.65
    delta = 0.15
    scores, z = unnormalized_update_scores(p, y, s, a)
    _, post = analytical_filter_step(p, y, s, a)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            f = score_boundary_value(p, y, i, j, s, a, delta)
            rhs = z * (post[i] - post[j] - delta)
            assert abs(f - rhs) < 1e-15


def test_preimage_classifier_matches_post_update_geometry():
    geometry = TopsetAffordanceGeometry(utility_gap=0.30)
    priors = [
        np.array([1/3, 1/3, 1/3]),
        np.array([0.70, 0.20, 0.10]),
        np.array([0.40, 0.35, 0.25]),
    ]
    for p in priors:
        for y in range(3):
            for s in (0.03, 0.30):
                for a in (0.45, 0.65):
                    _, post = analytical_filter_step(p, y, s, a)
                    predicted = classify_affordance_preimage(p, y, s, a)
                    assert predicted == geometry.support_size(post)

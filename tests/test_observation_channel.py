import numpy as np
from pcc_bayes.observation_channel import (
    binary_flip_probability, seen_one_probability, seen_probability,
)


def test_flip_channel_normalizes():
    for x in (0, 1):
        assert np.isclose(sum(binary_flip_probability(y, x, 0.2) for y in (0, 1)), 1.0)


def test_marginal_seen_probability():
    assert np.isclose(seen_one_probability(0.7, 0.1), 0.66)
    assert np.isclose(seen_probability(0, 0.7, 0.1), 0.34)

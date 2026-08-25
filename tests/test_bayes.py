import numpy as np
from pcc_bayes.bayes import bayes_update, tempered_update


def test_tempered_recovers_bayes():
    prior = [0.4, 0.6]
    like = [0.2, 0.8]
    assert np.allclose(bayes_update(prior, like), tempered_update(prior, like, 1, 1))


def test_pressure_zero_ignores_likelihood():
    post = tempered_update([0.4, 0.6], [0.01, 0.99], pressure=0, control=1)
    assert np.allclose(post, [0.4, 0.6])

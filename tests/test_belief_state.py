import numpy as np
from pcc_bayes.belief_state import normalize, entropy, kl_divergence, js_divergence


def test_normalize():
    assert np.allclose(normalize([2, 2]), [0.5, 0.5])


def test_entropy_uniform_binary():
    assert np.isclose(entropy([0.5, 0.5]), np.log(2))


def test_kl_identity_zero():
    assert np.isclose(kl_divergence([0.2, 0.8], [0.2, 0.8]), 0.0)


def test_js_symmetric():
    a = js_divergence([0.2,0.8], [0.7,0.3])
    b = js_divergence([0.7,0.3], [0.2,0.8])
    assert np.isclose(a, b)

from pcc_bayes.geometry import exact_binary_kl, fisher_quadratic_approx_binary


def test_local_kl_approximation():
    exact = exact_binary_kl(0.5, 0.5001)
    approx = fisher_quadratic_approx_binary(0.5, 0.5001)
    assert abs(exact - approx) / exact < 1e-4

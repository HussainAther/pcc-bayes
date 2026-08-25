from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.meta_inference import infer_pressure_control_grid


def test_conditional_grid_recovers_exact_generator():
    world = BinaryWorld()
    sim = simulate_binary_learning(steps=40, world=world,
                                   pcc=PCCParameters(1.5, 1.2, 0.1), seed=8)
    rows = infer_pressure_control_grid(
        sim["beliefs"], sim["observations"], world,
        pressure_grid=(1.0, 1.5, 2.0), control_grid=(1.0, 1.2, 1.4)
    )
    best = min(rows, key=lambda r: r["distance"])
    assert best["pressure"] == 1.5
    assert best["control"] == 1.2
    assert best["distance"] < 1e-20

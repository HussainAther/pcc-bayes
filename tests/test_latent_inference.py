from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.latent_inference import infer_latent_pcc_grid, posterior_summary


def test_observed_raw_channel_recovers_generator_grid_point():
    world = BinaryWorld()
    sim = simulate_binary_learning(
        steps=80, world=world, pcc=PCCParameters(1.5, 1.2, 0.15), seed=11
    )
    rows = infer_latent_pcc_grid(
        sim["beliefs"], world,
        pressure_grid=(1.0, 1.5, 2.0),
        control_grid=(1.0, 1.2, 1.4),
        chaos_grid=(0.05, 0.15, 0.25),
        observations=sim["observations"],
        raw_observations=sim["raw_observations"],
        true_hypotheses=sim["true_hypotheses"],
        sigma_logit=0.03,
    )
    assert rows[0]["pressure"] == 1.5
    assert rows[0]["control"] == 1.2
    flip_rate = float((sim["observations"] != sim["raw_observations"]).mean())
    expected_grid_chaos = min((0.05, 0.15, 0.25), key=lambda x: abs(x - flip_rate))
    assert rows[0]["chaos"] == expected_grid_chaos


def test_latent_channel_returns_normalized_posterior():
    world = BinaryWorld()
    sim = simulate_binary_learning(
        steps=30, world=world, pcc=PCCParameters(1.5, 1.2, 0.15), seed=4
    )
    rows = infer_latent_pcc_grid(
        sim["beliefs"], world,
        pressure_grid=(1.0, 1.5),
        control_grid=(1.0, 1.2),
        chaos_grid=(0.05, 0.15, 0.25),
        true_hypotheses=sim["true_hypotheses"],
        sigma_logit=0.03,
    )
    assert abs(sum(r["posterior"] for r in rows) - 1.0) < 1e-12
    summary = posterior_summary(rows)
    assert summary["effective_grid_points"] >= 1.0


def test_posterior_marginal_normalizes():
    from pcc_bayes.latent_inference import posterior_marginal
    world = BinaryWorld()
    sim = simulate_binary_learning(steps=8, world=world, seed=2)
    rows = infer_latent_pcc_grid(
        sim["beliefs"], world,
        pressure_grid=(1.0,), control_grid=(1.0,), chaos_grid=(0.0, 0.1, 0.2),
        observations=sim["observations"], raw_observations=sim["raw_observations"]
    )
    m = posterior_marginal(rows, "chaos")
    assert abs(sum(m.values()) - 1.0) < 1e-12


def test_canonical_corruption_grid_api_and_legacy_output_alias_agree():
    from pcc_bayes.latent_inference import infer_latent_update_grid, posterior_marginal
    world = BinaryWorld()
    sim = simulate_binary_learning(steps=8, world=world, seed=2)
    rows = infer_latent_update_grid(
        sim["beliefs"], world,
        pressure_grid=(1.0,), control_grid=(1.0,), corruption_grid=(0.0, 0.1),
        observations=sim["observations"], raw_observations=sim["raw_observations"]
    )
    assert all(r["observation_corruption"] == r["chaos"] for r in rows)
    assert posterior_marginal(rows, "observation_corruption") == posterior_marginal(rows, "chaos")

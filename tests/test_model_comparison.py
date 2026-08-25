from pcc_bayes.model_comparison import compare_update_models
from pcc_bayes.reporting import simulate_reported_beliefs
from pcc_bayes.simulation import BinaryWorld
from pcc_bayes.update_models import replay_update_model


def test_model_probabilities_normalize():
    world = BinaryWorld()
    observations = [1, 0, 1, 1, 0, 1]
    latent = replay_update_model(observations, world, "bayes")
    reports = simulate_reported_beliefs(latent, sigma_logit=0.15, seed=1)
    rows = compare_update_models(
        observations,
        world,
        reports=reports,
        models=("bayes", "pcc"),
        grids={"pressure": (0.5, 1.0, 1.5), "control": (0.5, 1.0, 1.5)},
        report_sigma_logit=0.15,
    )
    assert abs(sum(r["posterior_model_probability"] for r in rows) - 1.0) < 1e-12


def test_distinct_pcc_generator_is_recovered_from_noisy_reports():
    world = BinaryWorld()
    observations = [1, 1, 0, 1, 0, 0, 1, 1, 1, 0] * 4
    latent = replay_update_model(
        observations, world, "pcc", pressure=1.5, control=0.6
    )
    reports = simulate_reported_beliefs(latent, sigma_logit=0.08, seed=7)
    rows = compare_update_models(
        observations,
        world,
        reports=reports,
        models=("bayes", "leaky_bayes", "anchored_bayes", "pcc"),
        grids={
            "leak": (0.4, 0.6, 0.8, 1.0),
            "anchor_strength": (0.0, 0.1, 0.25, 0.5),
            "pressure": (0.75, 1.0, 1.5),
            "control": (0.4, 0.6, 0.8, 1.0),
        },
        report_sigma_logit=0.08,
    )
    assert rows[0]["model"] == "pcc"
    assert rows[0]["best_params"] == {"pressure": 1.5, "control": 0.6}

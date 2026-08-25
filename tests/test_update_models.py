import numpy as np

from pcc_bayes.simulation import BinaryWorld
from pcc_bayes.update_models import replay_update_model


def test_leaky_bayes_is_pressure_one_pcc_slice():
    world = BinaryWorld()
    obs = [1, 0, 1, 1, 0]
    leak = replay_update_model(obs, world, "leaky_bayes", leak=0.7)
    pcc = replay_update_model(obs, world, "pcc", pressure=1.0, control=0.7)
    assert np.allclose(leak, pcc)


def test_anchor_zero_recovers_standard_bayes():
    world = BinaryWorld()
    obs = [1, 1, 0, 1]
    bayes = replay_update_model(obs, world, "bayes")
    anchored = replay_update_model(obs, world, "anchored_bayes", anchor_strength=0.0)
    assert np.allclose(bayes, anchored)

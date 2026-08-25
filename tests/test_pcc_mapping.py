import pytest

from pcc_bayes.pcc import BeliefUpdateParameters, PCCParameters


def test_observation_corruption_is_canonical_name():
    params = BeliefUpdateParameters(pressure=1.5, control=0.6, observation_corruption=0.2)
    assert params.observation_corruption == 0.2
    assert params.chaos == 0.2  # legacy compatibility only


def test_legacy_chaos_keyword_remains_reproducible():
    params = PCCParameters(pressure=1.5, control=0.6, chaos=0.2)
    assert params.observation_corruption == 0.2


def test_conflicting_corruption_names_are_rejected():
    with pytest.raises(ValueError):
        PCCParameters(observation_corruption=0.2, chaos=0.1)

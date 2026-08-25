"""PCC-Bayes: dynamical analysis of Bayesian belief trajectories."""

from .belief_state import normalize, entropy, kl_divergence, js_divergence
from .bayes import bayes_update, tempered_update
from .simulation import BinaryWorld, simulate_binary_learning
from .observables import belief_observables

__all__ = [
    "normalize", "entropy", "kl_divergence", "js_divergence",
    "bayes_update", "tempered_update", "BinaryWorld",
    "simulate_binary_learning", "belief_observables",
]

__version__ = "0.1.0"

"""PCC-Bayes: dynamical analysis of Bayesian belief trajectories."""

from .belief_state import normalize, entropy, kl_divergence, js_divergence
from .bayes import bayes_update, tempered_update
from .simulation import BinaryWorld, simulate_binary_learning
from .observables import belief_observables
from .latent_inference import infer_latent_update_grid, infer_latent_pcc_grid, posterior_summary
from .model_comparison import compare_update_models
from .reporting import simulate_reported_beliefs, simulate_actions

__all__ = [
    "normalize", "entropy", "kl_divergence", "js_divergence",
    "bayes_update", "tempered_update", "BinaryWorld",
    "simulate_binary_learning", "belief_observables",
    "infer_latent_update_grid", "infer_latent_pcc_grid", "posterior_summary",
    "compare_update_models", "simulate_reported_beliefs", "simulate_actions",
]

__version__ = "0.12.0"

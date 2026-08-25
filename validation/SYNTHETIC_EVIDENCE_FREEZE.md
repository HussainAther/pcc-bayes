# Synthetic evidence freeze — v0.1.0

This file records baseline outputs that should not silently change as models evolve.

## Environment

- Python 3.10+
- NumPy
- deterministic seeds specified in scripts

## Frozen checks

1. `pytest -q` passes all tests.
2. `experiments/04_same_endpoint_different_paths.py` ends both paths at `P(H1)=0.70` while producing strongly separated cumulative JS revision and reversal counts.
3. `experiments/05_information_geometry.py` demonstrates convergence of exact Bernoulli KL to the Fisher quadratic approximation as perturbation size decreases.
4. `experiments/06_infer_update_rule.py` conditions on the observed sequence and should rank the generating Pressure/Control pair at or near the optimum on a grid containing the true values.
5. `experiments/07_latent_chaos_identifiability.py` is retained as a negative/identifiability test and is *not* expected to recover the generating Chaos value reliably.

If these outcomes change, record why in the research status rather than updating this file without explanation.

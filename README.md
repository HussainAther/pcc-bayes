# PCC-Bayes

**Pressure–Chaos–Control and entropy-based instability dynamics for Bayesian belief trajectories.**

PCC-Bayes extends the PCC / EBID research program from dynamical state variables to **belief distributions**. The central object is not only what an agent believes, but how its posterior distribution moves through probability space under evidence, inertia, and noise.

## Core question

> Can the structure of an inferential process be recovered from the dynamics of its beliefs, rather than only from its final belief state?

Two agents may end at the same posterior while taking radically different routes: smooth convergence, oscillatory revision, dogmatic persistence, or noise-driven volatility. PCC-Bayes makes those trajectories measurable.

## PCC mapping in belief space

| PCC term | Operational interpretation |
|---|---|
| Pressure | strength of incoming evidence / likelihood influence |
| Control | persistence or concentration of the current belief |
| Chaos | corruption, unreliability, or stochastic distortion of observations |

A generalized update is used for controlled experiments:

`posterior_i ∝ prior_i^control * likelihood_i^pressure`

With `pressure=1`, `control=1`, and `chaos=0`, this reduces to ordinary finite-hypothesis Bayes.

## EBID-style observables

The repo tracks:

- Shannon entropy: current uncertainty
- KL / Jensen-Shannon revision: belief change per observation
- cumulative revision: total trajectory movement
- KL to a reference belief: displacement in information space
- belief reversals: changes in MAP hypothesis
- time to confidence
- rolling revision volatility

Near a reference distribution, KL divergence is locally quadratic in belief perturbations. This gives a direct information-geometric bridge to the EBID observation that quadratic entropy-like deficits can grow at twice the local perturbation exponent.

## What is deliberately *not* claimed

This repository does **not** assume that human cognition is exactly Bayesian, that PCC is universal, or that the generalized update is a psychological law. The first goal is narrower: build a falsifiable computational framework for classifying and inferring belief dynamics.

## Repository layout

```text
pcc-bayes/
├── src/pcc_bayes/
│   ├── bayes.py             # ordinary + tempered Bayesian updates
│   ├── belief_state.py      # entropy / KL / JS utilities
│   ├── geometry.py          # local Fisher/KL geometry
│   ├── latent_inference.py  # likelihood-based hidden-channel inference
│   ├── meta_inference.py    # simulation-matching baselines
│   ├── model_comparison.py  # latent-rule model evidence
│   ├── observation_channel.py # explicit evidence-corruption model
│   ├── observables.py       # EBID-style trajectory observables
│   ├── reporting.py         # noisy reports + binary action models
│   ├── pcc.py               # PCC parameterization + noise operator
│   ├── update_models.py     # Bayes/leaky/anchored/PCC candidates
│   └── simulation.py        # sequential binary belief model
├── experiments/
│   ├── 01_coin_learning.py
│   ├── 02_regime_sweep.py
│   ├── 03_world_switch.py
│   ├── 04_same_endpoint_different_paths.py
│   ├── 05_information_geometry.py
│   ├── 06_infer_update_rule.py
│   ├── 07_latent_chaos_identifiability.py
│   ├── 08_latent_observation_channel.py
│   ├── 09_identifiability_by_sequence_length.py
│   └── 10_report_action_model_comparison.py
├── docs/
│   ├── THEORY.md
│   ├── HYPOTHESES.md
│   ├── FALSIFICATION_PLAN.md
│   └── ROADMAP.md
└── tests/
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

## Run tests

```bash
pytest -q
```

## Run experiments

```bash
python experiments/01_coin_learning.py
python experiments/02_regime_sweep.py
python experiments/03_world_switch.py
python experiments/04_same_endpoint_different_paths.py
python experiments/05_information_geometry.py
python experiments/06_infer_update_rule.py
python experiments/07_latent_chaos_identifiability.py
python experiments/08_latent_observation_channel.py
python experiments/09_identifiability_by_sequence_length.py
python experiments/10_report_action_model_comparison.py
```

Outputs are written to `results/`.

## First research targets

1. **Belief-regime map** — identify where inference is prior-dominated, evidence-responsive, volatile, or noise-limited.
2. **Plasticity vs rigidity** — after the latent world switches, measure adaptation delay as a function of control and pressure.
3. **Path dependence** — construct trajectories with similar endpoints but different revision volatility.
4. **Information geometry** — test the local quadratic KL approximation and the predicted doubled growth exponent in controlled perturbation experiments.
5. **Meta-inference** — infer latent PCC update parameters from observed belief trajectories.
6. **Observation-channel identifiability** — separate raw evidence, corrupted evidence, and beliefs and quantify which PCC parameters remain recoverable as variables are hidden.
7. **Latent-belief model comparison** — compare candidate update rules using only noisy probability reports and/or actions rather than direct access to internal beliefs.

## Relationship to PCC / EBID

The parent PCC / EBID project studies structured instability under Pressure, Chaos, and Control and uses entropy-like quantities as observables of dynamical departure. PCC-Bayes asks whether the same mathematical language is useful when the dynamical state is itself a probability distribution.

The connection is a hypothesis to test, not an assumed equivalence.

## Status

Version 0.3 adds a latent-belief observation layer and likelihood-based model comparison among Bayes, leaky Bayes, anchored Bayes, and PCC-tempered updates. In the frozen synthetic baseline, noisy probability reports recover the PCC generator cleanly while binary actions alone leave substantial ambiguity with leaky Bayes. The v0.2 Chaos-saturation ceiling remains an important earlier boundary result. APIs and theory remain research-grade and are expected to evolve.

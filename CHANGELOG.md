# Changelog

## 0.1.0 — 2026-08-25

- initial PCC-Bayes research package
- binary sequential inference model
- Pressure/Control generalized Bayesian update
- Chaos observation corruption model
- EBID-style information observables
- Fisher/KL local geometry experiment
- regime, switching, trajectory, and inverse-inference experiments
- falsification plan and synthetic evidence freeze

## 0.2.0 — 2026-08-25

- explicit raw-evidence -> corruption-channel -> received-evidence -> belief model
- proper transition likelihood in binary log-odds space
- analytic marginalization of latent received binary observations
- discrete Bayesian grid posterior for Pressure, Control, and Chaos
- posterior summaries and parameter marginals
- observation-access identifiability experiment
- sequence-length Chaos recovery experiment
- documented belief-saturation information ceiling
- v0.2 synthetic evidence freeze

## 0.3.0 — 2026-08-25

- latent internal-belief observation layer
- Gaussian log-odds model for noisy reported probabilities
- stochastic binary action model with soft log-odds policy
- common replay interface for Bayes, leaky Bayes, anchored Bayes, and PCC-tempered updates
- explicit test and documentation of leaky Bayes as the `Pressure=1` PCC slice
- grid-averaged marginal model evidence for update-rule comparison
- report-only, action-only, and joint observation experiment
- documented action-only identifiability ambiguity
- v0.3 synthetic evidence freeze

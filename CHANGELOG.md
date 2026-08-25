# Changelog

## 0.6.0 - Asymmetric value and logistic-exploiter falsification

- prospectively froze asymmetric decision payoffs that shift the Bayes-optimal action threshold to 2/3
- added value-aware structured and stochastic-threshold Chaos policies centered on utility indifference
- added a distinct online logistic exploiter model class with fixed public-context features and prequential SGD updates
- both Chaos candidates preserved asymmetric reward and outperformed uniform random play
- both failed the frozen >=0.05 global logistic-exploitability reduction gate, achieving reductions of 0.0270 and 0.0326
- mixing-opportunity prediction accuracy fell much further (0.6312 and 0.6612), identifying a conditional/local effect without retroactively passing the global gate
- added Experiment 15, a frozen result document, and regression tests

## 0.5.0 - Adaptive exploiter and independent Chaos replication

- prospectively froze an online adaptive-exploiter replication before confirmatory evaluation
- added `threshold_chaos`, an independently specified stochastic decision-threshold architecture
- added an online context-aware exploiter that predicts then updates after every revealed action
- retained the v0.4.1 structured-Chaos policy and all environment parameters unchanged
- both Chaos candidates passed frozen unpredictability, adequacy, value-preservation, and adaptive-exploitability gates
- structured Chaos reduced adaptive exploiter accuracy from 0.9835 to 0.9002
- threshold Chaos reduced adaptive exploiter accuracy from 0.9835 to 0.9122
- added Experiment 14, frozen result documentation, and regression tests

## 0.4.1 - Mature Chaos and context-conditioned exploitability

- added a switching-state Bayesian tracking environment for strategic-policy tests
- prospectively froze and ran the first mature PCC Chaos experiment
- separated unpredictability, strategic adequacy, and exploitability resistance
- preserved a preregistered negative result: action-history exploitability reduction missed its gate
- added a prospectively frozen context-aware exploiter diagnostic without retuning the policy
- found an 8.33-point held-out reduction in context-conditioned exploitability for structured Chaos
- retained uniform randomness and observation corruption as explicit anti-definition baselines
- added Experiment 12/13 result tables and regression tests

## 0.3.2 - PCC construct reconciliation

- separated mature cross-domain PCC constructs from Bayes-domain scalar proxies
- renamed the canonical binary noise parameter to `observation_corruption`
- retained `chaos` as a backwards-compatible API alias for archived experiments
- documented that observation corruption is **not** sufficient for PCC Chaos
- added prospective requirements for stronger Bayesian Pressure, Control, and Chaos mappings
- added compatibility/terminology tests

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

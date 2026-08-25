# Roadmap

## Phase 1 — Synthetic baseline

- binary hypothesis model
- PCC parameter sweeps
- world-switch adaptation
- entropy / revision observables
- information-geometric validation
- simulation-based inverse inference

## Phase 2 — Better inference models

Completed in v0.2 baseline:

- explicit raw -> corrupted -> belief observation channel
- likelihood-based discrete posterior over Pressure, Control, and Chaos
- analytic marginalization of latent binary received observations
- observation-access and sequence-length identifiability experiments

Next:

- categorical and continuous hypotheses
- Beta-Bernoulli and Dirichlet-multinomial conjugate models
- explicit source reliability
- misspecified likelihoods
- hierarchical priors
- sequential Monte Carlo for latent belief states

## Phase 3 — Agents and reported beliefs

Completed in v0.3 baseline:

- noisy reported probabilities in log-odds space
- binary soft-decision action observation model
- latent-belief replay under Bayes, leaky Bayes, anchored Bayes, and PCC-tempered updates
- grid-averaged model evidence with within-model complexity penalty
- explicit documentation that leaky Bayes is the `Pressure=1` slice of PCC
- report-only, action-only, and joint model-identifiability experiment

Next:

- jointly infer decision-policy parameters rather than fixing them
- richer action tasks with varying payoffs
- allow received evidence and internal belief to be latent simultaneously
- compare against additional genuinely distinct update families
- repeated-seed calibration of model probabilities and recovery rates

## Phase 4 — EBID tests

- local perturbation growth experiments
- Fisher metric for multinomial simplex
- detectability limits for entropy/KL early-warning signals
- distinguish true instability from stochastic posterior movement

## Phase 5 — Cross-domain applications

Potential targets only after synthetic falsification work:

- multi-agent forecasting
- scientific belief revision
- adversarial information environments
- adaptive control / active inference
- market expectations

No human-domain interpretation should precede a clear observation model and appropriate validation.

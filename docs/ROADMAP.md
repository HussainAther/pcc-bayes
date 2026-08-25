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
- likelihood-based discrete posterior over evidence pressure, belief control, and observation corruption
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
- repeated-seed calibration of model probabilities and recovery rates (20-seed pilot complete; 100-seed frozen confirmation pending)

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


## v0.4.1 completed: mature Chaos probe

- separated Chaos into unpredictability, adequacy, and exploitability resistance
- retained a failed history-only exploitability gate
- passed a prospectively frozen context-conditioned exploitation diagnostic

## v0.5.0 completed: adaptive Chaos replication

- added an online-updating context-aware exploiter
- retained the original structured-Chaos policy unchanged
- added an independently specified stochastic-threshold Chaos architecture
- both candidates passed frozen unpredictability, adequacy, value-preservation, and adaptive-exploitability gates
- next: vary exploiter model class and environmental payoff/asymmetry before claiming broader portability

## v0.6.0 completed: asymmetric-value / logistic falsification

- introduced a fixed asymmetric payoff matrix and utility-optimal posterior threshold of 2/3
- replaced the count-table opponent with a distinct online logistic exploiter
- both Chaos candidates preserved utility but failed the frozen 5-point global exploitability-reduction gate
- the exploitability reduction was concentrated on the 25--29% of decisions where mixing was strategically live
- next: prospectively separate **global exploitability** from **opportunity-conditioned exploitability**, and test whether the latter replicates across payoff matrices without retuning policy coefficients

## Phase 5 — Opportunity-conditioned Chaos robustness

Completed in v0.7.0:

- prospectively separated global exploitability from opportunity-conditioned exploitability;
- introduced matched-context scoring against deterministic utility play;
- preserved the two existing Chaos policy architectures without coefficient retuning;
- replicated the local conditional exploitability effect across payoff thresholds 1/3, 1/2, and 2/3;
- retained the earlier v0.6 global failure unchanged.

Next: keep the v0.7 opportunity definition fixed and attempt falsification under a new opponent model class and/or altered environment dynamics before making any broader cross-domain claim.

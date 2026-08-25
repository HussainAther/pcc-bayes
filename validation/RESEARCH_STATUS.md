# Research status

Date: 2026-08-25

## Implemented

- finite binary Bayesian belief dynamics
- generalized Pressure/Control update
- stochastic observation-channel Chaos
- entropy, KL, JS, reversal, confidence, and volatility observables
- environmental switch experiments
- local Fisher/KL geometry check
- conditional inverse inference for Pressure/Control
- latent-channel simulation-matching baseline for `(P,C,Ch)`
- explicit hidden observation-channel likelihood
- analytic marginalization of latent received binary evidence
- discrete likelihood-based posterior over `(P,C,Ch)`
- sequence-length identifiability diagnostics
- automated unit tests

## Current synthetic evidence

### Endpoint insufficiency

A smooth and a volatile trajectory were constructed with the same endpoint `P(H1)=0.70`. The smooth trajectory has cumulative JS revision about `0.00091` and zero MAP reversals; the volatile trajectory has cumulative JS revision about `1.137` and ten MAP reversals. This validates the basic claim that an endpoint posterior need not summarize belief dynamics.

### Local geometry

For a Bernoulli reference probability of `0.5`, the Fisher quadratic approximation to KL reaches relative error around `3e-11` at perturbation `1e-6`, numerically validating the expected local second-order geometry.

### Parameter identifiability

Conditional on the realized observations, Pressure and Control can be replayed and compared directly. Chaos is not identifiable from that deterministic replay because it parameterizes how latent/raw observations become observed evidence.

Version 0.2 supplies the missing generative observation model. In a 120-step synthetic run, exact belief transitions recover Pressure=1.5 and Control=1.2, while Chaos posterior concentration depends strongly on observation access. With raw and received evidence both observed, effective posterior support is about 2.83 grid points; with beliefs only it is about 6.20.

Across 20 seeds, increasing sequence length from 20 to 160 reduces mean effective Chaos-grid support from about 4.85 to 2.28 when raw and received evidence are available. Beliefs-only support remains near 6.69 after saturation. This establishes an information ceiling in the current binary setup: longer belief trajectories need not make the corruption channel identifiable.

## Not yet established

- a universal PCC structure for Bayesian inference
- calibrated Bayesian posterior inference over PCC parameters
- human cognitive validity
- entropy as a universal early-warning signal for belief instability
- cross-domain generalization

## Next scientific milestone

Add a reported-belief/action observation layer and likelihood-based model comparison among standard Bayes, leaky Bayes, recency weighting, anchoring, and PCC-tempered updates. The key next question is whether model class and update parameters remain distinguishable when internal beliefs are not directly observed.

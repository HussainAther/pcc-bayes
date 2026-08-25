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
- automated unit tests

## Current synthetic evidence

### Endpoint insufficiency

A smooth and a volatile trajectory were constructed with the same endpoint `P(H1)=0.70`. The smooth trajectory has cumulative JS revision about `0.00091` and zero MAP reversals; the volatile trajectory has cumulative JS revision about `1.137` and ten MAP reversals. This validates the basic claim that an endpoint posterior need not summarize belief dynamics.

### Local geometry

For a Bernoulli reference probability of `0.5`, the Fisher quadratic approximation to KL reaches relative error around `3e-11` at perturbation `1e-6`, numerically validating the expected local second-order geometry.

### Parameter identifiability

Conditional on the realized observations, Pressure and Control can be replayed and compared directly. Chaos is not identifiable from that deterministic replay because it parameterizes how latent/raw observations become observed evidence.

When all three are inferred only by stochastic trajectory matching, the current baseline can favor a zero-chaos model even when data were generated with nonzero chaos. This is a useful negative result: a proper generative observation model or additional observed variables are required before interpreting weights over Chaos as posterior beliefs.

## Not yet established

- a universal PCC structure for Bayesian inference
- calibrated Bayesian posterior inference over PCC parameters
- human cognitive validity
- entropy as a universal early-warning signal for belief instability
- cross-domain generalization

## Next scientific milestone

Implement an explicit hidden-observation state-space model where raw evidence, corrupted evidence, and reported beliefs are separately represented. Compare PCC-Bayes against standard Bayes, leaky Bayes, recency weighting, and anchoring using likelihood-based model comparison.

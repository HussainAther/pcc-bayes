# Falsification plan

PCC-Bayes should be treated as an empirical modeling program rather than protected terminology.

## Baselines

Every PCC-inspired experiment should be compared against:

- ordinary Bayes (`P=1, C=1, Ch=0`)
- noise-only Bayes (`P=1, C=1, Ch>0`)
- likelihood tempering without PCC interpretation
- forgetting / leaky Bayes where appropriate

If conventional language explains the observations completely, PCC terminology should not be claimed to add predictive content.

## Predeclared observables

Use endpoint accuracy, log score, entropy, JS revision, cumulative revision, reversal count, and adaptation delay before introducing custom metrics.

## Robustness checks

- repeat across random seeds
- sweep prior asymmetry
- reverse which hypothesis is true
- vary separation between candidate likelihoods
- test both abrupt and gradual environmental change
- avoid interpreting simplex-boundary numerical artifacts as instability

## Geometry claim

The Fisher/KL result is local. Test progressively smaller perturbations and report approximation error. Do not extrapolate doubled-exponent behavior beyond the interval where the quadratic approximation is quantitatively accurate.

## Meta-inference claim

The baseline inverse routine produces simulation-matching weights, not a calibrated posterior. Label it accordingly until a generative likelihood over observed reports/actions is introduced.

## Negative results worth preserving

Keep experiments where:

- PCC parameters are not identifiable
- entropy fails as an early-warning signal
- high volatility does not imply poor accuracy
- ordinary Bayes outperforms all generalized rules
- mature PCC definitions fail prospective mechanistic tests, or Bayes-domain proxies disagree with them

Those are scientifically informative boundaries of the framework.

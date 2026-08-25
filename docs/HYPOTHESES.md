# Testable hypotheses

Terminology note: `pressure` and `control` below are Bayes-domain proxy parameters. The stochastic evidence channel is called **observation corruption**, not PCC Chaos. See `PCC_CONSTRUCT_MAPPING.md`.

## H1 — Evidence pressure accelerates revision

Holding control and observation corruption fixed, increasing pressure should initially increase per-step belief revision and reduce time to confidence when the model is correctly specified.

**Failure condition:** revision or confidence is non-monotonic across the full sweep without an interpretable saturation or boundary effect.

## H2 — Belief control creates a robustness/plasticity tradeoff

Higher control should reduce short-run response to noisy observations but increase adaptation delay after the latent generating hypothesis changes.

**Failure condition:** control does not measurably alter both noise robustness and switch adaptation in the predicted directions.

## H3 — Observation corruption can maintain uncertainty or induce false confidence

At moderate parameter settings, increasing observation corruption should reduce calibration and increase trajectory volatility. Under strong control/pressure, corrupted evidence may instead produce confidently wrong states.

**Failure condition:** observation corruption has negligible effect on calibration or trajectory statistics.

This hypothesis concerns a noise channel only. Passing H3 would **not** establish PCC Chaos.

## H4 — Endpoint belief is insufficient to identify dynamics

Trajectories with similar final posterior probabilities can differ strongly in cumulative JS revision, volatility, or reversal count.

**Failure condition:** these observables collapse to endpoint belief in the tested systems.

## H5 — Local KL growth follows quadratic geometry

For sufficiently small perturbations around an interior reference belief, exact KL divergence should match its Fisher quadratic approximation and inherit a doubled exponent from exponentially growing perturbations.

**Failure condition:** the approximation or slope relation fails in the expected local regime after numerical error is excluded.

## H6 — Update parameters are partially identifiable from trajectories

Observed belief trajectories should contain enough information to recover at least coarse regions of `(pressure, control, observation_corruption)` parameter space under known world dynamics.

**Failure condition:** materially different parameter triples remain indistinguishable even with long, informative trajectories.

## H7 — Mature PCC constructs require stronger intervention tests

Likelihood gain, memory gain, and observation corruption should not by themselves be sufficient to claim mature PCC Pressure, Control, or Chaos.

**Failure condition:** a prospectively specified mechanistic mapping demonstrates that one of these scalar proxies alone satisfies all stages of the corresponding mature construct across independent implementations.

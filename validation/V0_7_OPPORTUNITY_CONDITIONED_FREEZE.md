# v0.7 Opportunity-conditioned Chaos robustness freeze

Date frozen: 2026-08-25

## Question

Does the local exploitability effect observed diagnostically in v0.6 survive prospectively across multiple payoff geometries when **opportunity-conditioned exploitability** is made the primary endpoint, without retuning either Chaos policy?

This specification is frozen before the v0.7 confirmatory results are inspected.

## Environment

Reuse the binary Markov tracking process and logistic opponent protocol from v0.6:

- steps per episode: 400
- hidden-state switch probability: 0.08
- observation accuracy: 0.75
- calibration seeds: 0--49
- evaluation seeds: 1000--1099
- online logistic exploiter features, learning rate, L2 coefficient, calibration passes, prequential update order, and classification threshold are unchanged from v0.6

The hidden state remains unavailable to the exploiter. Public observations and prior public actions remain available.

## Frozen payoff geometries

Three payoff matrices are tested prospectively.

### A. Symmetric classification value

| hidden state | action 0 | action 1 |
|---|---:|---:|
| 0 | +1.0 | -1.0 |
| 1 | -1.0 | +1.0 |

Utility indifference threshold: `p=0.5`.

### B. False-positive-costly value

| hidden state | action 0 | action 1 |
|---|---:|---:|
| 0 | +1.0 | -2.0 |
| 1 | -0.5 | +1.0 |

Utility indifference threshold: `p=2/3`.

This is the v0.6 payoff geometry and is included unchanged.

### C. False-negative-costly value

| hidden state | action 0 | action 1 |
|---|---:|---:|
| 0 | +1.0 | -0.5 |
| 1 | -2.0 | +1.0 |

Utility indifference threshold: `p=1/3`.

No payoff matrix is fit to the confirmatory result.

## Policies

The policies and coefficients are unchanged from v0.6:

1. `predictable_utility`: deterministic expected-utility maximizing baseline.
2. `uniform_random`: 50/50 anti-definition baseline.
3. `utility_structured_chaos`: `mixing_width=0.18`, `max_non_greedy=0.45`.
4. `utility_threshold_chaos`: threshold half-width `0.20`.

The only payoff-dependent quantity is the analytically implied utility-indifference threshold already used by the policy definitions. No coefficient is retuned across payoff matrices.

## Opportunity definition

For each Chaos candidate separately, an **opportunity** is a decision step where that candidate's frozen marginal action probability satisfies

`0 < P(action 1 | belief, payoff geometry) < 1`.

This mask is determined solely by the candidate's policy and posterior, before observing whether the candidate or exploiter prediction is correct.

For each candidate/payoff pair, the same candidate-defined opportunity mask is applied to:

- that candidate's evaluation trajectory, and
- the deterministic `predictable_utility` trajectory generated from the same evaluation seed and therefore the same hidden/public environment trajectory.

Each policy is predicted by a separately calibrated online logistic exploiter of the frozen v0.6 model class. This compares conditional predictability on matched public contexts rather than comparing different subsets.

## Primary exploitability endpoint

For candidate `c`, define

`Delta_opp(c) = Accuracy_exploiter(predictable_utility | c-opportunities) - Accuracy_exploiter(c | c-opportunities)`.

The primary exploitability gate is:

`Delta_opp(c) >= 0.10`.

This 10-percentage-point gate is frozen prospectively. The v0.6 diagnostic did not compute the matched deterministic opportunity-conditioned comparator, so this threshold is not selected from that unobserved contrast.

## Candidate gates per payoff geometry

Each Chaos candidate must independently satisfy all four gates within each payoff geometry:

1. **Opportunity prevalence:** candidate opportunity fraction >= 0.10 and <= 0.60.
2. **Unpredictability:** mean normalized policy entropy >= predictable-utility entropy + 0.10.
3. **Value preservation:** candidate mean reward >= predictable-utility mean reward - 0.12.
4. **Opportunity-conditioned exploitability resistance:** `Delta_opp >= 0.10`.

Uniform random is retained as an anti-definition/value reference but is not used in the primary opportunity-conditioned contrast because every step is a mixing step under that policy.

## Cross-payoff robustness criterion

v0.7 passes only if **both** independently implemented Chaos candidates pass all four gates in **all three** frozen payoff geometries (6 candidate/payoff cells total).

A partial result is retained if only some cells pass. No payoff matrix, seed, policy coefficient, exploiter hyperparameter, opportunity definition, or gate may be modified after result inspection.

## Secondary outputs

Report, without additional pass/fail gates:

- global online logistic exploiter accuracy;
- opportunity-conditioned exploiter accuracy for candidate and matched deterministic baseline;
- mean reward;
- classification accuracy;
- normalized policy entropy;
- opportunity fraction.

## Interpretation boundaries

Passing would support the narrow claim that value-aware PCC Chaos is a **local conditional property of strategically viable option sets** across several payoff geometries in this synthetic Bayesian tracking substrate.

It would not establish universal PCC Chaos, optimal mixed strategy, human cognition, equilibrium behavior, fighting-game validity, or cross-domain universality.

Failure is retained without post-hoc retuning.

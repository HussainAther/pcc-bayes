# v0.8 Three-action Chaos transfer result

Date: 2026-08-25

Status: **FAIL (frozen confirmatory test)**

The v0.8 design was frozen before confirmatory result inspection in `V0_8_THREE_ACTION_FREEZE.md`. No policy coefficient, environment parameter, seed, opportunity definition, exploiter hyperparameter, or gate was changed after inspection.

## Result summary

| Candidate | Reward | Branch fraction | Three-way fraction | Entropy | Candidate branch exploiter | Matched deterministic branch exploiter | Reduction | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| utility-topset Chaos | 0.4668 | 0.1142 | 0.0226 | 0.0756 | 0.4983 | 0.7018 | 0.2035 | FAIL |
| perturbed-utility Chaos | 0.4738 | 0.1252 | 0.0230 | 0.0429 | 0.6575 | 0.7103 | 0.0528 | FAIL |

Deterministic baseline reward was `0.4775`; uniform-random reward was `-0.3304`.

## Frozen gates

### Utility-topset Chaos

Passed:

- value preservation;
- opportunity-conditioned exploitability resistance (`0.2035 >= 0.10`);
- non-random adequacy.

Failed:

- branch prevalence (`0.1142 < 0.15`);
- genuine three-way branching (`0.0226 < 0.05`);
- normalized entropy (`0.0756 < 0.10`).

### Perturbed-utility Chaos

Passed:

- value preservation;
- non-random adequacy.

Failed:

- branch prevalence (`0.1252 < 0.15`);
- genuine three-way branching (`0.0230 < 0.05`);
- normalized entropy (`0.0429 < 0.10`);
- opportunity-conditioned exploitability resistance (`0.0528 < 0.10`).

## Interpretation

The richer three-action environment did **not** produce enough strategically live branching under the frozen policies and environment to satisfy the prospective transfer claim. The Bayesian posterior was usually decisive enough that both candidate policies collapsed to a single supported action. Mean support size was only `1.137` for utility-topset Chaos and `1.148` for perturbed-utility Chaos.

The utility-topset result is nevertheless diagnostically informative: on the relatively rare candidate-defined branch opportunities, the multiclass exploiter's accuracy fell from `0.7018` for matched deterministic play to `0.4983` for the Chaos candidate, a `20.35` percentage-point reduction, while reward remained within `0.011` of deterministic play. This local effect is not sufficient to pass v0.8 because the branch opportunities themselves were too rare and true three-way opportunities were only about `2.3%` of steps.

The perturbed-utility architecture provided a stronger falsification: even conditional on its branch opportunities, the matched exploitability reduction was only `5.28` percentage points, below the frozen `10`-point criterion.

## Constraint added to the theory

v0.7's binary opportunity-conditioned result cannot be assumed to transfer merely by increasing the action count. A mature multi-option Chaos claim requires both:

1. an environment/policy combination that actually sustains a nontrivial multi-action viable set; and
2. conditional resistance to exploitation within that viable set.

The first requirement failed prospectively here, and the second was architecture-dependent.

No post-hoc widening of the viable set, increase in perturbation amplitude, reduction in observation accuracy, or gate relaxation is counted as v0.8 evidence.

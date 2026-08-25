# v0.10 Analytical Affordance Geometry Freeze

Status: frozen before confirmatory comparison.

## Purpose

v0.9 showed that branch prevalence and three-way branch prevalence respond differently to information structure. v0.10 asks whether the support cardinality of the fixed v0.8 utility-topset Chaos policy can be predicted analytically from posterior geometry, without inspecting action samples or tuning thresholds.

## Frozen policy

The policy remains unchanged from v0.8/v0.9:

- three hidden states / three actions;
- state-matching utility `u_i = 2 p_i - 1`;
- `utility_gap = 0.30`;
- all actions whose utility is within `0.30` of the maximum are viable;
- if multiple actions are viable, the highest-utility action receives probability 0.60 and the remaining probability is split among the other viable actions.

No policy coefficients may be changed in this experiment.

## Analytical prediction

Let posterior probabilities be sorted as

`p_(1) >= p_(2) >= p_(3)`.

Because

`max(u) - u_i = 2 (p_(1) - p_i)`,

the frozen utility gap `g = 0.30` induces a posterior gap

`delta = g / 2 = 0.15`.

Therefore the predicted support cardinality is:

1. exactly one viable action iff `p_(1) - p_(2) > 0.15`;
2. exactly two viable actions iff `p_(1) - p_(2) <= 0.15` and `p_(1) - p_(3) > 0.15`;
3. exactly three viable actions iff `p_(1) - p_(3) <= 0.15`.

Boundary equality is included in the viable set, matching the frozen implementation.

## Confirmatory data

Use exactly the v0.9 information-structure grid:

- observation accuracy: `{0.45, 0.55, 0.65, 0.80}`;
- state-switch probability: `{0.03, 0.10, 0.30}`;
- 100 evaluation seeds: `1000..1099`;
- 400 steps per seed.

Only the fixed `utility_topset_chaos` policy is confirmatory for the exact analytical boundary test. The perturbation-based policy is not claimed to share these simple polyhedral boundaries.

## Frozen tests

For every posterior step in all 12 cells:

1. analytical support cardinality must exactly equal the implemented policy support cardinality;
2. cell-level predicted one-, two-, and three-action fractions must equal empirical support fractions to numerical tolerance `1e-12`;
3. the v0.9 historical branch fraction must equal predicted `(two + three)` fraction to `1e-12`;
4. the v0.9 historical three-way fraction must equal the predicted three-action fraction to `1e-12`.

Any mismatch is a failure of the claimed analytical mapping or its implementation.

## Interpretation rule

A pass establishes only an exact geometric characterization of this frozen policy's viable-set affordance in posterior space. It does not establish a universal PCC boundary, nor does it explain how often the Bayesian filter visits each region. The latter remains an environment/filter-dynamics question.

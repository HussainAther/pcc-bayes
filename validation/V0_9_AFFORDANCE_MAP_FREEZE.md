# v0.9 Information-structure affordance map freeze

Date frozen: 2026-08-25

## Question

Does the failure of v0.8 to sustain multi-option branch points arise from the environment's information structure rather than from post-hoc retuning of the Chaos policies?

This specification is frozen before v0.9 confirmatory results are inspected.

## Fixed policies

The two v0.8 three-action policies are carried forward unchanged:

- `utility_topset_chaos` with utility gap `0.30` and 0.60/0.40 viable-set allocation;
- `perturbed_utility_chaos` with per-action perturbations `Uniform(-0.18,+0.18)` and the frozen 129-point marginal-probability grid from seed `8080`.

No policy coefficient may vary across cells.

## Environment grid

The hidden state, three-action reward structure, Bayesian filter, and episode length remain those of v0.8. Only two environmental parameters vary:

- observation accuracy: `{0.45, 0.55, 0.65, 0.80}`;
- state-switch probability: `{0.03, 0.10, 0.30}`.

This gives 12 prospectively specified environment cells. Conditional on a state switch, either alternative state remains equally likely. Conditional on observation error, either wrong symbol remains equally likely.

Evaluation seeds for affordance metrics: `1000--1099` in every cell.

## Affordance metrics

For each candidate policy and environment cell, measure:

- branch-opportunity fraction: support size `K_t >= 2`;
- genuine three-way fraction: support size `K_t = 3`;
- mean support size;
- normalized policy entropy;
- mean reward.

These are properties of the fixed policy interacting with the environment; no exploiter is needed to define them.

## Frozen directional predictions

For **each** candidate architecture:

1. At switch probability `0.10`, branch prevalence at observation accuracy `0.45` must exceed branch prevalence at `0.80`.
2. At switch probability `0.10`, three-way prevalence at observation accuracy `0.45` must exceed three-way prevalence at `0.80`.
3. At observation accuracy `0.55`, branch prevalence at switch probability `0.30` must exceed branch prevalence at `0.03`.
4. At observation accuracy `0.55`, three-way prevalence at switch probability `0.30` must exceed three-way prevalence at `0.03`.

These endpoint predictions test whether less informative observations and less persistent states expand the live option set.

## High-affordance anchor cell

The cell `(observation_accuracy=0.45, switch_probability=0.30)` is designated **in advance** as the high-uncertainty anchor. It is not selected from the observed grid.

For both candidate architectures, the anchor must satisfy the same prevalence requirements that v0.8 failed:

- branch-opportunity fraction `>= 0.15`;
- three-way-opportunity fraction `>= 0.05`.

## Local Chaos replication at the anchor

Only at the prespecified anchor cell, rerun the unchanged v0.8 online multiclass softmax exploiter protocol:

- calibration seeds `0--49`;
- evaluation seeds `1000--1099`;
- learning rate `0.08`;
- L2 `0.001`;
- 4 calibration passes;
- same public-context features and matched candidate-defined branch masks.

Each candidate must satisfy:

- opportunity-conditioned exploitability reduction `>= 0.10`;
- candidate reward >= deterministic reward - `0.15`;
- candidate reward >= uniform-random reward + `0.20`.

## Overall v0.9 decision

v0.9 passes only if:

- all four directional predictions hold for both candidate architectures;
- both anchor prevalence gates hold for both architectures; and
- both candidates pass all three local-Chaos anchor gates.

A partial pattern is retained as partial evidence, not promoted to a pass.

## Interpretation boundaries

Passing would support the antecedent claim that multi-option PCC-Chaos-like behavior depends on environmental affordances: information structure can create or remove strategically live alternative sets even when the decision policies are held fixed.

It would not establish that low information or high volatility is universally beneficial, that these two parameters exhaust environmental affordances, or that the result transfers to humans or fighting games.

Failure is retained without widening the viable set, changing perturbation amplitude, altering seeds, or selecting a different anchor after result inspection.

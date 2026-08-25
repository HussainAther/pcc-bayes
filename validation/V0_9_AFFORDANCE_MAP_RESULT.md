# v0.9 Information-structure affordance map result

Date: 2026-08-25

Status: **FAIL overall; strong partial support for environmental affordance**

The design in `V0_9_AFFORDANCE_MAP_FREEZE.md` was frozen before confirmatory inspection. The two v0.8 Chaos policies, seeds, policy coefficients, environment grid, anchor cell, and all gates were retained unchanged.

## Main result

Reducing observation reliability strongly expanded the live option set for both fixed policy architectures. The prespecified low-information/high-volatility anchor (`observation_accuracy=0.45`, `switch_probability=0.30`) converted the rare-branch v0.8 setting into a branch-rich environment without changing either policy.

| Candidate | Branch fraction | Three-way fraction | Mean support | Reward | Candidate branch exploiter | Matched deterministic | Reduction |
|---|---:|---:|---:|---:|---:|---:|---:|
| utility-topset Chaos | 0.5727 | 0.2642 | 1.837 | -0.1306 | 0.5388 | 0.8958 | 0.3569 |
| perturbed-utility Chaos | 0.5982 | 0.2235 | 1.822 | -0.1053 | 0.7480 | 0.9001 | 0.1521 |

Both candidates passed all prespecified anchor gates, including branch prevalence, genuine three-way prevalence, value preservation relative to deterministic play, nonrandom adequacy, and at least a 0.10 matched opportunity-conditioned exploitability reduction.

## Directional predictions

For both policy architectures:

Passed:

- lower observation reliability (`0.45` versus `0.80` at switch `0.10`) increased branch prevalence;
- lower observation reliability increased genuine three-way prevalence;
- higher state switching (`0.30` versus `0.03` at observation accuracy `0.55`) increased overall branch prevalence.

Failed:

- higher state switching did **not** increase three-way prevalence at observation accuracy `0.55`.

The overall v0.9 decision is therefore **FAIL**, because the freeze required all four directional predictions for both architectures.

## Why the failed prediction matters

The grid shows that state volatility and observation uncertainty are not interchangeable forms of "more uncertainty." At observation accuracy `0.55`, increasing switching from `0.03` to `0.30` raised overall branching but reduced or eliminated true three-way support:

- utility-topset: branch `0.1023 -> 0.3039`, three-way `0.0116 -> 0.0000`;
- perturbed-utility: branch `0.1099 -> 0.3396`, three-way `0.0115 -> 0.0105`.

Thus a more volatile hidden state can create **more frequent two-option ambiguity** without creating a broader three-option viable set. Affordance geometry depends on the interaction between transition dynamics, observation likelihoods, and the policy's fixed utility/decision geometry rather than on a single scalar "uncertainty" level.

## Constraint added to the theory

The v0.8 failure was not simply a consequence of using three actions. Environmental information structure can strongly alter whether a fixed policy has strategically live alternatives. However, multi-option affordance is multidimensional:

1. observation informativeness strongly controls branch-set prevalence in this substrate;
2. state volatility can increase branching without monotonically increasing branch **cardinality**;
3. once a branch-rich environment is present, both fixed v0.8 architectures can preserve value and reduce matched local exploitability;
4. therefore "affordance" should be modeled as a structured property of the environment-policy interaction, not a one-dimensional uncertainty knob.

The negative directional result is retained. No alternate anchor, policy widening, perturbation change, or gate relaxation is counted as v0.9 evidence.

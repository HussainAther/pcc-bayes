# v0.4 mature PCC Chaos result

Date: 2026-08-25

## Confirmatory Experiment 12

The prospectively frozen structured-Chaos policy produced:

| Policy | U: policy entropy | A: task accuracy | action-history exploiter accuracy |
|---|---:|---:|---:|
| predictable_value | 0.0000 | 0.8059 | 0.8198 |
| uniform_random | 1.0000 | 0.5013 | 0.4986 |
| corrupted_predictable | 0.0000 | 0.6689 | 0.7468 |
| structured_chaos | 0.2879 | 0.7856 | 0.7981 |

Structured Chaos passed the frozen unpredictability, adequacy-vs-random, and
value-preservation gates. It failed the action-history-only exploitability gate:
exploiter accuracy fell by only 0.0217, below the preregistered 0.05 reduction.
The overall mature-Chaos claim therefore did **not** pass Experiment 12 as frozen.

Both anti-definitions behaved correctly: uniform random failed strategic adequacy,
and the observation-corruption baseline failed the mature-Chaos conjunction.

## Prospective diagnostic: Experiment 13

A new diagnostic was frozen before execution. It replaced the history-only
exploiter with a stronger context-aware exploiter that observes the current/previous
public evidence and previous two public actions. No agent parameters, seeds, or
v0.4 acceptance thresholds were changed.

Held-out context-aware exploiter accuracy was:

| Policy | context exploiter accuracy | mixing-opportunity accuracy | mixing-opportunity fraction |
|---|---:|---:|---:|
| predictable_value | 0.9835 | n/a | 0.0000 |
| uniform_random | 0.4998 | 0.4998 | 1.0000 |
| corrupted_predictable | 0.8089 | n/a | 0.0000 |
| structured_chaos | 0.9002 | 0.7651 | 0.4263 |

The predictable-minus-structured reduction was 0.0833, passing the prospectively
frozen >=0.05 diagnostic criterion. On steps where the structured policy actually
mixed, the exploiter reached only 0.7651 accuracy.

## Interpretation

The evidence does not support the claim that structured Chaos is uniformly hard to
predict from action history. Instead it supports a narrower, strategically more
meaningful claim: when public context is accounted for, value-aware mixing makes the
agent materially harder to exploit than a deterministic value policy while retaining
most task performance.

This is consistent with the mature PCC anti-definition `Chaos != randomness`:
uniform random behavior maximizes unpredictability and resistance to prediction but
sacrifices task value. Observation corruption can degrade predictability but does not
supply deliberate behavioral mixing and fails the conjunction of mature-Chaos gates.

This remains a synthetic Bayesian tracking result, not evidence for universal PCC or
human strategic cognition.

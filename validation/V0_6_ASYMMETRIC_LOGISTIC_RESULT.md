# v0.6 Asymmetric-value and logistic-exploiter result

Date: 2026-08-25

Status: **frozen replication criterion failed**.

## Frozen design

The confirmatory design is specified in `V0_6_ASYMMETRIC_LOGISTIC_FREEZE.md`. No seeds, payoff entries, policy coefficients, logistic features, optimizer settings, or pass/fail thresholds were changed after inspecting the result.

The asymmetric payoff matrix makes false positives costly and shifts the Bayes-optimal action-1 threshold to `p=2/3`. Mature-Chaos candidates therefore mix around strategic value indifference rather than raw posterior uncertainty.

## Confirmatory results

| policy | policy entropy | mean reward | classification accuracy | online logistic exploiter accuracy | mixing-opportunity exploiter accuracy | mixing fraction |
|---|---:|---:|---:|---:|---:|---:|
| predictable utility | 0.0000 | 0.5978 | 0.7862 | 0.9328 | n/a | 0.0000 |
| uniform random | 1.0000 | -0.1187 | 0.5004 | 0.5006 | 0.5006 | 1.0000 |
| utility structured Chaos | 0.1848 | 0.5836 | 0.7765 | 0.9058 | 0.6312 | 0.2537 |
| utility threshold Chaos | 0.2115 | 0.5803 | 0.7749 | 0.9002 | 0.6612 | 0.2927 |

## Frozen gates

Both candidates passed:

- unpredictability;
- adequacy relative to uniform random play;
- asymmetric value preservation.

Both candidates failed the frozen **>=0.05 overall reduction in logistic exploiter accuracy** requirement.

- utility structured Chaos: reduction `0.9328 - 0.9058 = 0.0270`;
- utility threshold Chaos: reduction `0.9328 - 0.9002 = 0.0326`.

Therefore the v0.6 replication criterion is **FAIL**.

## Diagnostic interpretation

The failure is not a value-collapse result. Both candidates preserved nearly all deterministic expected utility under the asymmetric payoff matrix while uniform random play had negative mean reward.

The exploitability effect is concentrated on the states where the candidate actually mixes. On those subsets, online logistic prediction accuracy falls to 0.6312 for utility structured Chaos and 0.6612 for utility threshold Chaos. Those mixing opportunities occupy only about 25% and 29% of decisions respectively, so the global accuracy reduction is diluted by the majority of states in which the value-aware policy remains deterministic.

This suggests a narrower hypothesis for future testing: mature Chaos may be a **local/conditional property of strategically viable option sets**, not a requirement that the full policy be globally unpredictable.

That interpretation is diagnostic, not a retroactive pass. The preregistered overall exploitability gate remains failed.

## Boundary established

v0.5 showed robustness across two stochastic policy architectures against an adaptive count-table exploiter under symmetric classification value. v0.6 shows that this result does not automatically survive a simultaneous change in payoff geometry and exploiter model class under the same global 5-point criterion.

The next falsification work should distinguish global exploitability from opportunity-conditioned exploitability prospectively rather than moving the v0.6 gate.

# v0.7 Opportunity-conditioned Chaos robustness result

Date: 2026-08-25

Status: **cross-payoff robustness criterion passed**.

## Frozen design

The confirmatory design is specified in `V0_7_OPPORTUNITY_CONDITIONED_FREEZE.md`. The opportunity definition, three payoff matrices, seeds, two Chaos policy architectures and coefficients, online logistic exploiter, and all pass/fail gates were fixed before confirmatory results were inspected.

The v0.6 global exploitability failure remains unchanged. v0.7 tests a different, prospectively frozen claim: exploitability on matched contexts where the candidate policy's frozen rule makes more than one action strategically live.

## Confirmatory results

| payoff geometry | candidate | opportunity fraction | candidate reward | deterministic reward | candidate exploiter accuracy on opportunities | deterministic exploiter accuracy on same opportunities | reduction |
|---|---|---:|---:|---:|---:|---:|---:|
| symmetric | structured Chaos | 0.2293 | 0.5986 | 0.6118 | 0.7598 | 0.9279 | **0.1681** |
| symmetric | threshold Chaos | 0.2714 | 0.5910 | 0.6118 | 0.7615 | 0.9392 | **0.1777** |
| false-positive costly | structured Chaos | 0.2537 | 0.5836 | 0.5978 | 0.6312 | 0.7347 | **0.1035** |
| false-positive costly | threshold Chaos | 0.2927 | 0.5803 | 0.5978 | 0.6612 | 0.7703 | **0.1091** |
| false-negative costly | structured Chaos | 0.2552 | 0.5867 | 0.6029 | 0.6370 | 0.7503 | **0.1132** |
| false-negative costly | threshold Chaos | 0.2945 | 0.5730 | 0.6029 | 0.6577 | 0.7838 | **0.1261** |

All six candidate/payoff cells passed all four frozen gates:

- opportunity prevalence between 0.10 and 0.60;
- normalized policy entropy at least 0.10 above deterministic utility play;
- mean reward within 0.12 of deterministic utility play;
- matched opportunity-conditioned exploiter-accuracy reduction at least 0.10.

Therefore the v0.7 cross-payoff robustness criterion is **PASS**.

## Why this does not erase v0.6

The global online-logistic criterion from v0.6 remains failed. In the same false-positive-costly geometry, global exploiter-accuracy reductions were only 0.0270 and 0.0326, below the frozen 0.05 requirement.

v0.7 does not relabel those outcomes. Instead it prospectively tests the narrower hypothesis suggested by that failed experiment: Chaos-like resistance may be concentrated at strategic branch points rather than distributed uniformly across all actions.

The matched comparison is important. The deterministic baseline is scored only on the exact public-context steps selected by each candidate's frozen opportunity rule. Thus the reduction is not explained merely by comparing an ambiguous subset for Chaos with an easy full trajectory for deterministic play.

## Interpretation

Within this binary Bayesian tracking substrate, two independently structured value-aware stochastic policies show reduced online logistic predictability specifically where their own policy rules preserve multiple live actions. The effect survives three payoff geometries with utility-indifference thresholds at 1/3, 1/2, and 2/3 while retaining most deterministic reward.

The strongest supported statement is therefore local and conditional:

> mature PCC Chaos is consistent with preserving strategically viable alternatives at branch points while reducing an opponent's ability to collapse those same contexts into a reliably predicted action.

This is stronger than a one-payoff diagnostic but remains substrate-specific. It does not establish a universal PCC law, an equilibrium solution, human strategic validity, or transfer to fighting games.

## Boundary and next test

The narrowest passing cell is the false-positive-costly structured-Chaos condition (`Delta_opp = 0.1035`) against a 0.10 gate. Robustness should therefore not be overstated.

A stronger next falsification should hold the v0.7 opportunity definition fixed while changing the **opponent model class again** and/or the **environmental dynamics**, rather than adding more payoff matrices or tuning policy widths.

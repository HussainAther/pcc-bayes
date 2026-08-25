# v0.5 adaptive-exploiter and independent-architecture result

Date: 2026-08-25
Status: **PASS** under the frozen v0.5 criteria

See `validation/V0_5_ADAPTIVE_CHAOS_REPLICATION_FREEZE.md` for the prespecified design.

## Confirmatory summary

The deterministic value baseline achieved mean task accuracy 0.8059 and adaptive context-exploiter accuracy 0.9835. Uniform random play achieved task accuracy 0.5013 and adaptive exploiter accuracy 0.5001.

The unchanged v0.4.1 `structured_chaos` policy achieved:

- normalized policy entropy: 0.2879
- task accuracy: 0.7856
- adaptive exploiter accuracy: 0.9002
- adaptive exploiter accuracy on mixing opportunities: 0.7651
- mixing-opportunity fraction: 0.4263

Relative to deterministic value play, adaptive exploitability fell by 0.0833 while task accuracy fell by only 0.0203. All four frozen candidate gates passed.

The independently specified `threshold_chaos` policy achieved:

- normalized policy entropy: 0.2499
- task accuracy: 0.7895
- adaptive exploiter accuracy: 0.9122
- adaptive exploiter accuracy on mixing opportunities: 0.7643
- mixing-opportunity fraction: 0.3715

Relative to deterministic value play, adaptive exploitability fell by 0.0713 while task accuracy fell by only 0.0164. All four frozen candidate gates passed.

## Gate table

| Candidate | Unpredictability | Adequacy vs random | Value preservation | Adaptive exploitability resistance | All |
|---|---|---|---|---|---|
| structured_chaos | PASS | PASS | PASS | PASS | PASS |
| threshold_chaos | PASS | PASS | PASS | PASS | PASS |

The independent-architecture replication therefore passes.

## Interpretation

The result strengthens the narrow synthetic claim developed in v0.4.1. The effect is not tied to one confidence-to-mixing function and does not disappear when the exploiter updates online. Two different value-aware stochastic mechanisms preserve most tracking accuracy while making behavior less conditionally predictable from the same public context.

The important object remains **conditional exploitability among viable alternatives**, not global randomness. Uniform random play is much harder to predict but loses substantial task value, so unpredictability alone remains insufficient for mature PCC Chaos.

## Boundaries

This is still one binary Bayesian tracking substrate, one public-context representation, and one family of count-based adaptive exploiters. The result does not establish universality, equilibrium optimality, human behavioral validity, or transfer to competitive games. A stronger next step would vary exploiter model class and environmental payoff/asymmetry rather than retune either passing Chaos policy.

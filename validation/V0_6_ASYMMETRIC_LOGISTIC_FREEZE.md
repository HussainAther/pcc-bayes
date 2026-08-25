# v0.6 Asymmetric-value and logistic-exploiter falsification freeze

Date frozen: 2026-08-25

## Question

Does the mature PCC Chaos result survive when (a) strategic adequacy is defined by an asymmetric payoff geometry rather than binary classification accuracy and (b) exploitability is measured by a different online opponent model class: logistic prediction rather than a context-count table?

This specification is frozen before the v0.6 confirmatory result is inspected.

## Environment

Reuse the binary Markov tracking process:

- steps per episode: 400
- hidden-state switch probability: 0.08
- observation accuracy: 0.75
- calibration seeds: 0--49
- evaluation seeds: 1000--1099

The hidden state is unavailable to the exploiter. Public observations and prior public actions are available.

## Asymmetric payoff geometry

Rewards are frozen as:

| hidden state | action 0 | action 1 |
|---|---:|---:|
| 0 | +1.0 | -2.0 |
| 1 | -0.5 | +1.0 |

Thus a false positive (action 1 when state=0) is substantially more costly than a miss. Under posterior `p=P(state=1)`, action 1 is Bayes-optimal only when `p >= 2/3`.

The primary value quantity is mean realized reward per decision, not classification accuracy.

## Policies

1. `predictable_utility`: deterministic expected-utility maximizing baseline using the frozen payoff matrix.
2. `uniform_random`: 50/50 anti-definition baseline.
3. `utility_structured_chaos`: confidence/value-aware mixing centered on the utility-indifference threshold. It permits up to 0.45 non-greedy probability at exact indifference and linearly removes mixing over a posterior-width of 0.18 on either side.
4. `utility_threshold_chaos`: independent architecture. A fresh posterior decision threshold is sampled uniformly from `[2/3 - 0.20, 2/3 + 0.20]` at every decision; action 1 is selected iff posterior exceeds the sampled threshold.

No policy coefficient is fit to v0.6 confirmatory outcomes.

## Online logistic exploiter

Use a logistic action predictor with public features:

- bias
- current observation
- previous observation
- previous action
- second previous action
- current-observation x previous-action interaction
- previous-observation x previous-action interaction

Training/evaluation protocol:

- calibration: 5 fixed online passes through the 50 calibration episodes
- learning rate: 0.05
- L2 coefficient: 0.001
- evaluation: prequential prediction followed immediately by one SGD update on the revealed action
- learned weights persist across evaluation episodes in frozen seed order
- classification threshold: 0.5

This model class is intentionally different from the v0.5 count-table exploiter and cannot memorize discrete context cells directly.

## Candidate gates

Each candidate (`utility_structured_chaos`, `utility_threshold_chaos`) must independently satisfy all four:

1. **Unpredictability**: mean normalized policy entropy >= predictable-utility entropy + 0.10.
2. **Adequacy vs random**: mean reward >= uniform-random mean reward + 0.20.
3. **Value preservation**: mean reward >= predictable-utility mean reward - 0.12.
4. **Logistic exploitability resistance**: online logistic exploiter accuracy <= predictable-utility exploiter accuracy - 0.05.

## Replication criterion

v0.6 passes only if both independently implemented Chaos candidates pass all four gates.

## Value-indifference diagnostic

Report exploiter accuracy on decisions where the candidate's action probability lies strictly between zero and one. This is diagnostic only and is not an additional pass/fail gate.

## Anti-definitions

- Random action remains insufficient for Chaos even if difficult to predict.
- Posterior uncertainty alone is insufficient; mixing must be conditioned on strategic value geometry.
- Observation corruption remains a noise construct, not mature Chaos.

## Interpretation boundaries

Passing would support a narrow robustness claim: value-aware conditional unpredictability can preserve asymmetric decision utility and reduce online exploitability across two policy architectures and two exploiter model classes in this synthetic Bayesian tracking substrate.

It would not establish universal PCC Chaos, equilibrium optimality, human validity, or transfer to fighting games or other competitive domains.

Failure is retained without changing seeds, payoff matrix, policy coefficients, feature set, optimizer hyperparameters, or gates.

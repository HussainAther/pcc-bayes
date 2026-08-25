# v0.4 Mature PCC Chaos synthetic evidence freeze

Status: **frozen before confirmatory execution**

## Question

Can a Bayesian decision agent exhibit the mature PCC Chaos structure —
**unpredictability + strategic adequacy + resistance to exploitation** — without
identifying Chaos with random action or observation corruption?

This experiment is deliberately narrower than a claim of universal PCC. It tests
whether the cross-domain Chaos anti-definition can be instantiated prospectively in
a sequential Bayesian tracking task.

## Environment

A hidden binary state follows a two-state Markov process with switch probability
`0.08` per step. The agent receives a binary observation that matches the hidden
state with probability `0.75`. A correctly specified Bayesian filter tracks the
posterior state probability. Each episode contains `400` decisions.

Task value is action accuracy: reward 1 when the binary action equals the current
hidden state and 0 otherwise.

## Frozen policy families

1. **predictable_value** — deterministic MAP action from the clean posterior.
2. **uniform_random** — action 0/1 with equal probability, independent of belief.
3. **corrupted_predictable** — deterministic MAP action after an additional
   symmetric observation flip channel with rate `0.25`. This is the legacy
   observation-corruption/noise proxy and is explicitly *not* called Chaos.
4. **structured_chaos** — uses the clean posterior and randomizes only when the
   posterior makes both actions strategically viable. Let
   `confidence = abs(2*p1 - 1)`. The probability of taking the non-MAP action is
   `0.45 * max(0, 1 - confidence / 0.60)`. At high confidence it is deterministic;
   near indifference it mixes substantially.

No policy parameter is tuned after confirmatory results are observed.

## Measures

### U — behavioral unpredictability

Mean normalized Bernoulli entropy of the policy's action distribution. For
deterministic policies this is 0; for uniform random it is 1.

### A — strategic adequacy

Held-out mean task accuracy.

### E — resistance to exploitation

A frozen action-history exploiter predicts the next action using Laplace-smoothed
lookup tables over the previous three public actions. The exploiter is calibrated
on independent episodes and then frozen. Lower held-out prediction accuracy means
greater resistance to this exploiter.

## Seeds

- calibration episodes: seeds `0..49`
- held-out evaluation episodes: seeds `1000..1099`

Agent stochasticity uses a deterministic seed derived from episode seed and policy,
so comparisons are reproducible.

## Prospectively frozen gates

The **structured_chaos** family counts as a successful mature-Chaos instantiation
only if all of the following hold on held-out episodes:

1. **Unpredictability:** `U_structured >= U_predictable + 0.10`.
2. **Adequacy vs randomness:** `A_structured >= A_random + 0.15`.
3. **Value preservation:** `A_structured >= A_predictable - 0.08`.
4. **Exploitability resistance:** exploiter accuracy against structured Chaos is at
   least `0.05` lower than against predictable-value play.
5. **Noise anti-definition:** the observation-corruption baseline does not satisfy
   all four mature-Chaos gates when substituted for structured Chaos.
6. **Randomness anti-definition:** uniform random fails at least one adequacy/value
   gate despite high unpredictability/exploitation resistance.

Failure of any required gate is retained as a negative result. Thresholds are not
moved after execution.

## Scope

Passing supports only this claim: a prospectively specified Bayesian decision
policy can instantiate the current mature PCC Chaos structure in this synthetic
tracking environment. It does not establish human validity, cross-domain
universality, or that this is the unique operationalization of Chaos.

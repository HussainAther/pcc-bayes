# PCC construct mapping for Bayesian belief dynamics

## Why this document exists

PCC-Bayes began with a deliberately simple three-parameter analogy: evidence weighting was called Pressure, prior persistence was called Control, and observation corruption was called Chaos. The broader PCC research program has since developed more demanding mechanistic definitions. This document freezes the distinction so the Bayesian repository does not overclaim.

## Mature cross-domain PCC constructs

The current comparative PCC program treats the constructs as functional mechanisms rather than permanent strategy types:

- **Pressure:** consequential threat or commitment -> constriction/redistribution of viable responses -> strategic consequence.
- **Control:** relevant information -> contextual interpretation -> allocation among strategically viable responses.
- **Chaos:** unpredictability + strategic adequacy + resistance to exploitation. **Chaos is not randomness.**

These definitions come from the comparative synthetic PCC program and are intentionally stricter than a one-number label.

## What PCC-Bayes currently implements

| Repository quantity | Mathematical role | Relationship to mature PCC |
|---|---|---|
| `pressure` | likelihood/evidence exponent `P` | **Pressure-like proxy only.** It measures evidence gain, not threat, response constriction, or consequence. |
| `control` | prior/log-odds memory exponent `C` | **Control-like proxy only.** It measures persistence/forgetting, not information-context-allocation as a full mechanism. |
| `observation_corruption` | binary evidence flip probability | **Not PCC Chaos.** It is a stochastic observation-channel corruption parameter. |

Historical code and archived outputs used the key `chaos` for observation corruption. Version 0.3.2 retains that name only as a backwards-compatible alias. New code and prose should use `observation_corruption` or `corruption_rate`.

## Consequence for interpretation

The generalized binary update remains useful:

`logit(b_{t+1}) = C logit(b_t) + P log(L_1/L_0)`.

But `P` and `C` should be read as **Bayes-domain control parameters**, not as complete operational definitions of cross-domain Pressure and Control. Likewise, observation corruption can create stochastic or misleading evidence without satisfying the mature Chaos requirements.

Therefore the current scientific claim is narrow:

> PCC-Bayes studies whether belief-update dynamics contain pressure-like evidence amplification, control-like memory/persistence, and identifiable observation-channel corruption, while keeping the mature PCC constructs conceptually separate.

## What a genuine PCC-Bayes mapping would require

A stronger future mapping should be intervention-based.

### Pressure candidate

A Bayesian Pressure mechanism would need more than large likelihood gain. A candidate experiment should establish a sequence such as:

1. an information source or commitment changes the decision environment;
2. the set or value distribution of viable posterior-contingent actions is measurably constricted;
3. that constriction has downstream consequence.

### Control candidate

A Bayesian Control mechanism should test whether information is actually used contextually:

1. relevant evidence is available;
2. the same evidence is interpreted differently under different decision contexts;
3. action/report allocation changes among viable alternatives in a value-sensitive way.

Memory gain `C` may contribute to such a mechanism, but it is not sufficient by itself.

### Chaos candidate

A Bayesian Chaos mechanism must not be defined by evidence noise or posterior entropy alone. A candidate should require:

1. unpredictability of reports/actions or update timing;
2. preservation of inferential or decision value;
3. resistance to exploitation by an observer/adversary attempting to predict or manipulate the agent.

This suggests a future adversarial-observer experiment rather than another corruption sweep.

## Research discipline

Until those experiments are prospectively specified and passed, PCC-Bayes should report:

- **evidence pressure** or **likelihood gain** for `P`;
- **belief persistence / memory gain** for `C`;
- **observation corruption** for the flip channel;
- **PCC Pressure/Control/Chaos** only when discussing the broader theory or explicitly labeling these quantities as proxies.

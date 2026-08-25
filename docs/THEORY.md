# Theory

## 1. Beliefs as dynamical states

Let `b_t(theta)` denote a normalized distribution over a finite hypothesis set after observations through time `t`. Sequential inference creates a trajectory on the probability simplex.

Standard Bayes is

`b_{t+1}(theta) ∝ b_t(theta) L(x_{t+1} | theta)`.

PCC-Bayes introduces an experimental two-exponent family:

`b_{t+1}(theta) ∝ b_t(theta)^C L(x_{t+1} | theta)^P`,

where `P` is evidence pressure and `C` is belief control. Observation chaos is implemented separately as corruption of the data channel.

This parameterization is intentionally minimal. It provides knobs that can be swept and inferred without claiming that these knobs uniquely represent cognition.

For a binary belief, the update has a particularly transparent log-odds form:

`logit(b_{t+1}) = C logit(b_t) + P log(L_1/L_0)`.

Thus `C=1` gives ordinary accumulation of past log evidence, `C<1` gives exponential forgetting of accumulated log-odds, and `C>1` amplifies existing conviction. A conventional leaky-Bayes recursion is therefore nested inside PCC as the `P=1` slice, rather than constituting an independent model family.

## 2. Interpretation of the parameters

### Pressure

Pressure controls how strongly each observation moves the posterior. High pressure creates sharper likelihood-driven updates; low pressure discounts evidence.

### Control

Control controls persistence of the current belief. Values above one can produce rigidity and escalating concentration; values below one weaken memory of prior concentration.

### Chaos

Chaos alters the evidence channel rather than the posterior directly. In the binary baseline, observations are flipped with probability `Ch`. More realistic extensions can include missingness, source mixtures, adversarial evidence, and model misspecification.

## 3. Observables

For belief vector `b_t`:

- uncertainty: `H_t = -sum_i b_t(i) log b_t(i)`
- directed revision: `KL(b_t || b_{t-1})`
- symmetric bounded revision: `JS(b_t, b_{t-1})`
- displacement from reference: `KL(b_t || b*)`
- MAP reversals: count of changes in `argmax_i b_t(i)`
- confidence time: first time `max_i b_t(i)` exceeds a threshold

A belief can therefore be high-confidence but dynamically unstable, or uncertain but dynamically stable.

## 4. Information-geometric bridge to EBID

For a nearby distribution `b = b* + delta`, KL divergence has a local second-order expansion governed by the Fisher information metric:

`KL(b || b*) ≈ 1/2 delta^T F(b*) delta`.

If a perturbation magnitude grows locally as `exp(lambda t)`, a quadratic divergence should grow as `exp(2 lambda t)` while the local approximation remains valid. This is the belief-space counterpart of the entropy-deficit doubling mechanism explored in EBID.

Crucially, this is a *local geometric prediction*. It can fail outside the local regime, near simplex boundaries, under saturation, or when the chosen observable is not quadratic in the unstable mode.

## 5. Meta-inference

Let `phi = (P, C, Ch)` parameterize an update process. Given an observed belief trajectory `B`, the inverse problem is

`p(phi | B) ∝ p(B | phi) p(phi)`.

The v0.1 baseline used simulation distance and normalized pseudo-posterior weights. Version 0.2 adds an explicit binary observation channel and a likelihood-based grid posterior. When received evidence is hidden, the binary observation is marginalized analytically at each transition. The model still remains synthetic and conditional on the specified update family; it is not a calibrated cognitive model.

A key v0.2 result is an identifiability ceiling near simplex boundaries: once beliefs saturate, additional belief observations can carry little information about the hidden corruption process. See `OBSERVATION_MODEL.md`.

## 6. Core distinction

PCC-Bayes separates three levels:

1. **Bayesian inference**: beliefs about a world state.
2. **Belief dynamics**: trajectories produced by repeated updates.
3. **Meta-inference**: inference about the rule that generated those trajectories.

The research value lies mainly in levels 2 and 3.

## 7. Latent reports, actions, and model comparison

Version 0.3 treats internal belief as latent at the measurement stage. Given a common received-evidence sequence, each candidate update rule generates its own latent belief trajectory. Observable data are then generated from that trajectory through either noisy probability reports, a stochastic binary action policy, or both.

Reported probabilities use additive Gaussian noise in binary log-odds space. Actions use a soft log-odds policy. Model comparison integrates likelihood over a supplied discrete parameter grid with a uniform within-model prior. This grid-averaged evidence prevents a flexible model from being judged only by its single best-fitting parameter point.

The first synthetic result shows a measurement-channel boundary: noisy reports can distinguish a non-Bayesian PCC generator cleanly in the tested setup, whereas binary actions alone discard enough information to leave PCC and leaky Bayes substantially confounded.

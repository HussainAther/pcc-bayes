# Research status

Date: 2026-08-25

## Implemented

- finite binary Bayesian belief dynamics
- generalized Pressure/Control update
- stochastic observation-channel corruption (historically labeled Chaos)
- entropy, KL, JS, reversal, confidence, and volatility observables
- environmental switch experiments
- local Fisher/KL geometry check
- conditional inverse inference for Pressure/Control
- latent-channel simulation-matching baseline for `(P,C,q)`
- explicit hidden observation-channel likelihood
- analytic marginalization of latent received binary evidence
- discrete likelihood-based posterior over `(P,C,q)`
- sequence-length identifiability diagnostics
- latent reported-belief likelihood in log-odds space
- stochastic binary action observation model
- model evidence over Bayes, leaky Bayes, anchored Bayes, and PCC update families
- explicit leaky-Bayes/PCC nesting test
- automated unit tests

## Current synthetic evidence

### Endpoint insufficiency

A smooth and a volatile trajectory were constructed with the same endpoint `P(H1)=0.70`. The smooth trajectory has cumulative JS revision about `0.00091` and zero MAP reversals; the volatile trajectory has cumulative JS revision about `1.137` and ten MAP reversals. This validates the basic claim that an endpoint posterior need not summarize belief dynamics.

### Local geometry

For a Bernoulli reference probability of `0.5`, the Fisher quadratic approximation to KL reaches relative error around `3e-11` at perturbation `1e-6`, numerically validating the expected local second-order geometry.

### Parameter identifiability

Conditional on the realized observations, Pressure and Control can be replayed and compared directly. Observation corruption is not identifiable from that deterministic replay because it parameterizes how latent/raw observations become observed evidence.

Version 0.2 supplies the missing generative observation model. In a 120-step synthetic run, exact belief transitions recover Pressure=1.5 and Control=1.2, while observation-corruption posterior concentration depends strongly on observation access. With raw and received evidence both observed, effective posterior support is about 2.83 grid points; with beliefs only it is about 6.20.

Across 20 seeds, increasing sequence length from 20 to 160 reduces mean effective corruption-grid support from about 4.85 to 2.28 when raw and received evidence are available. Beliefs-only support remains near 6.69 after saturation. This establishes an information ceiling in the current binary setup: longer belief trajectories need not make the corruption channel identifiable. This result concerns observation noise and is not evidence for or against the mature PCC Chaos construct.

### Latent report/action model comparison

Version 0.3 adds a latent-belief measurement layer. In the frozen 80-step PCC-generated synthetic run (`P=1.5`, `C=0.6`), noisy probability reports recover PCC decisively and select the exact generating grid point. Binary actions alone are much less informative: PCC receives model probability about 0.56 and leaky Bayes about 0.40. Combining reports and actions again recovers the generating PCC model and grid point.

This establishes a second information-loss boundary: coarse decisions can obscure distinctions that remain visible in probabilistic reports. Leaky Bayes is also formally recognized as the `P=1` slice of PCC in binary log-odds space.

## PCC construct reconciliation (v0.3.2)

The broader comparative PCC program now defines Pressure, Control, and Chaos as mechanistic structures rather than scalar labels. PCC-Bayes therefore freezes the following terminology: `pressure` is an evidence-gain proxy, `control` is a belief-memory proxy, and the binary flip probability is `observation_corruption`. The historical `chaos` API name remains only as a compatibility alias. Observation corruption must not be reported as PCC Chaos without a separate prospective test of unpredictability, value/adequacy, and exploitability resistance. See `docs/PCC_CONSTRUCT_MAPPING.md`.

## Mature PCC Chaos in Bayesian tracking (v0.4.1)

A prospectively frozen four-policy test compared deterministic value play, uniform random play, observation-corrupted deterministic play, and a structured value-aware mixing policy. Structured Chaos achieved normalized policy entropy 0.2879 and task accuracy 0.7856 versus 0.8059 for deterministic value play and 0.5013 for uniform random. It therefore passed unpredictability, adequacy-vs-random, and value-preservation gates.

The original action-history-only exploitability gate failed: frozen exploiter accuracy fell only from 0.8198 to 0.7981, a 0.0217 reduction versus the preregistered 0.05 requirement. This failure is retained.

A separately frozen context-aware diagnostic then exposed the current/previous public evidence plus recent actions to the exploiter, without changing the policy or seeds. Exploiter accuracy was 0.9835 on predictable-value play and 0.9002 on structured Chaos, an 0.0833 reduction that passed the frozen diagnostic gate. On the 42.63% of steps where the structured policy actually mixed, exploiter accuracy was 0.7651.

The current supported interpretation is therefore conditional: Bayesian structured Chaos is not globally unpredictable, but value-aware mixing can reduce exploitability **given the same public context** while preserving most decision value. Uniform randomness remains maximally unpredictable but strategically inadequate, and observation corruption remains a noise baseline rather than PCC Chaos. See `validation/V0_4_CHAOS_RESULT.md`.


## Adaptive-exploiter and independent-architecture replication (v0.5.0)

A prospectively frozen replication tested the unchanged structured-Chaos policy and a second stochastic-threshold architecture against a context-aware exploiter that updates after every revealed action. Deterministic value play remained highly predictable to this opponent (0.9835 accuracy). Structured Chaos reduced adaptive prediction accuracy to 0.9002 while preserving task accuracy at 0.7856 versus 0.8059 for deterministic play. The independent threshold-Chaos policy reduced adaptive prediction accuracy to 0.9122 while retaining 0.7895 task accuracy.

Both candidates passed all four frozen gates: increased policy entropy, adequacy relative to uniform random play, value preservation relative to deterministic play, and at least a 0.05 reduction in adaptive exploiter accuracy. On mixing opportunities, adaptive prediction accuracy was about 0.765 for both architectures. This supports implementation replication of the narrow context-conditioned Chaos claim within the current Bayesian tracking substrate. It does not yet establish robustness to different exploiter model classes or payoff structures. See `validation/V0_5_ADAPTIVE_CHAOS_REPLICATION_RESULT.md`.


## Asymmetric-value and logistic-exploiter falsification (v0.6.0)

A prospectively frozen test simultaneously changed strategic value geometry and the exploiter model class. False positives were assigned reward -2.0 while misses received -0.5, shifting the Bayes-optimal action-1 threshold from 0.5 to 2/3. Two Chaos architectures were re-expressed around this utility-indifference point without fitting to confirmatory outcomes. Exploitability was measured by an online logistic predictor with fixed public-context features and prequential SGD updates.

Both candidates preserved asymmetric reward: deterministic utility play achieved mean reward 0.5978, utility structured Chaos 0.5836, utility threshold Chaos 0.5803, and uniform random play -0.1187. Both candidates therefore passed unpredictability, adequacy-vs-random, and value-preservation gates. However, the frozen global exploitability gate failed for both. Logistic prediction accuracy fell from 0.9328 on deterministic play to 0.9058 and 0.9002, reductions of only 0.0270 and 0.0326 versus the required 0.05.

The failure is retained. A prespecified diagnostic shows the effect is concentrated where mixing is active: exploiter accuracy on mixing opportunities was 0.6312 and 0.6612, covering about 25% and 29% of decisions. This motivates a future prospective distinction between global policy unpredictability and local conditional exploitability over strategically viable alternatives. See `validation/V0_6_ASYMMETRIC_LOGISTIC_RESULT.md`.

## Not yet established

- a universal PCC structure for Bayesian inference
- calibrated Bayesian posterior inference over PCC parameters
- human cognitive validity
- entropy as a universal early-warning signal for belief instability
- cross-domain generalization

## Next scientific milestone

For the mature-Chaos branch, prospectively distinguish **global exploitability** from **opportunity-conditioned exploitability** and test the conditional claim across multiple frozen payoff matrices and opponent model classes without retuning policy coefficients. The v0.6 global logistic gate remains failed. In parallel, the inference branch still has a frozen 100-seed model-recovery confirmation pending.


## v0.3.1 repeated-seed recovery pilot

A prospectively frozen 100-seed model-recovery calibration has been specified. A
20-seed computational pilot, using the first frozen seeds without changing the grid or
measurement model, shows near-perfect recovery from noisy reported probabilities but
substantial degradation from binary actions alone. For the true PCC generator,
action-only top-1 recovery was 13/20, with five leaky-Bayes and two anchored-Bayes
confusions. Reports and joint reports+actions recovered PCC in 20/20 pilot seeds.

The full 100-seed frozen run remains pending and should be treated as confirmatory.

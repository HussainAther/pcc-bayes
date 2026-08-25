# Changelog

## 0.10.0 - Analytical affordance geometry

- Derived exact posterior-simplex boundaries for one-, two-, and three-action support under the frozen utility-topset Chaos policy.
- Added `affordance_geometry.py` with analytical support classification and region summaries.
- Prospectively validated the boundaries across all 480,000 posterior states in the frozen v0.9 grid with zero mismatches.
- Reproduced every historical v0.9 branch and three-way occupancy fraction from posterior geometry alone.
- Showed geometrically that higher volatility can move posterior mass into two-action bands without increasing occupancy of the central three-action region.

## 0.9.0 - 2026-08-25

- prospectively mapped three-action viable-set affordance over a 12-cell observation-reliability x state-persistence grid while holding both v0.8 Chaos policies fixed
- added an exploiter-free affordance summary for branch prevalence, three-way prevalence, support size, entropy, and reward
- prespecified a low-information/high-volatility anchor before inspection
- found 57--60% branch prevalence and 22--26% genuine three-way prevalence at the anchor, versus ~11--13% and ~2.3% in v0.8
- both fixed policies passed anchor value, nonrandom-adequacy, and matched opportunity-conditioned exploitability gates; reductions were 35.69 and 15.21 percentage points
- retained an overall frozen failure because higher state switching increased branch frequency but did not monotonically increase three-way branch prevalence at fixed observation accuracy
- added Experiment 18, frozen affordance-map result documentation, caching of shared environment/belief paths, and regression tests

## 0.8.0 - 2026-08-25

- prospectively transferred opportunity-conditioned Chaos from binary decisions to a three-state, three-action Bayesian tracking task
- added a correct categorical Markov filter, normalized ternary policy entropy, and two independent three-action Chaos architectures
- added an online adaptive three-class softmax exploiter with public observation/action context
- froze explicit branch-prevalence and genuine three-way-opportunity gates before confirmatory inspection
- retained a negative result: branch opportunities occurred on only 11.4--12.5% of steps and three-way opportunities on about 2.3%, below the frozen gates
- utility-topset Chaos preserved value and reduced matched branch-point exploiter accuracy by 20.35 points, but still failed the full transfer criterion because branching was too rare
- perturbed-utility Chaos preserved value but reduced matched branch-point exploitability by only 5.28 points, below the frozen 10-point gate
- added Experiment 17, frozen result documentation, and multiclass regression tests

## 0.6.0 - Asymmetric value and logistic-exploiter falsification

- prospectively froze asymmetric decision payoffs that shift the Bayes-optimal action threshold to 2/3
- added value-aware structured and stochastic-threshold Chaos policies centered on utility indifference
- added a distinct online logistic exploiter model class with fixed public-context features and prequential SGD updates
- both Chaos candidates preserved asymmetric reward and outperformed uniform random play
- both failed the frozen >=0.05 global logistic-exploitability reduction gate, achieving reductions of 0.0270 and 0.0326
- mixing-opportunity prediction accuracy fell much further (0.6312 and 0.6612), identifying a conditional/local effect without retroactively passing the global gate
- added Experiment 15, a frozen result document, and regression tests

## 0.5.0 - Adaptive exploiter and independent Chaos replication

- prospectively froze an online adaptive-exploiter replication before confirmatory evaluation
- added `threshold_chaos`, an independently specified stochastic decision-threshold architecture
- added an online context-aware exploiter that predicts then updates after every revealed action
- retained the v0.4.1 structured-Chaos policy and all environment parameters unchanged
- both Chaos candidates passed frozen unpredictability, adequacy, value-preservation, and adaptive-exploitability gates
- structured Chaos reduced adaptive exploiter accuracy from 0.9835 to 0.9002
- threshold Chaos reduced adaptive exploiter accuracy from 0.9835 to 0.9122
- added Experiment 14, frozen result documentation, and regression tests

## 0.4.1 - Mature Chaos and context-conditioned exploitability

- added a switching-state Bayesian tracking environment for strategic-policy tests
- prospectively froze and ran the first mature PCC Chaos experiment
- separated unpredictability, strategic adequacy, and exploitability resistance
- preserved a preregistered negative result: action-history exploitability reduction missed its gate
- added a prospectively frozen context-aware exploiter diagnostic without retuning the policy
- found an 8.33-point held-out reduction in context-conditioned exploitability for structured Chaos
- retained uniform randomness and observation corruption as explicit anti-definition baselines
- added Experiment 12/13 result tables and regression tests

## 0.3.2 - PCC construct reconciliation

- separated mature cross-domain PCC constructs from Bayes-domain scalar proxies
- renamed the canonical binary noise parameter to `observation_corruption`
- retained `chaos` as a backwards-compatible API alias for archived experiments
- documented that observation corruption is **not** sufficient for PCC Chaos
- added prospective requirements for stronger Bayesian Pressure, Control, and Chaos mappings
- added compatibility/terminology tests

## 0.1.0 — 2026-08-25

- initial PCC-Bayes research package
- binary sequential inference model
- Pressure/Control generalized Bayesian update
- Chaos observation corruption model
- EBID-style information observables
- Fisher/KL local geometry experiment
- regime, switching, trajectory, and inverse-inference experiments
- falsification plan and synthetic evidence freeze

## 0.2.0 — 2026-08-25

- explicit raw-evidence -> corruption-channel -> received-evidence -> belief model
- proper transition likelihood in binary log-odds space
- analytic marginalization of latent received binary observations
- discrete Bayesian grid posterior for Pressure, Control, and Chaos
- posterior summaries and parameter marginals
- observation-access identifiability experiment
- sequence-length Chaos recovery experiment
- documented belief-saturation information ceiling
- v0.2 synthetic evidence freeze

## 0.3.0 — 2026-08-25

- latent internal-belief observation layer
- Gaussian log-odds model for noisy reported probabilities
- stochastic binary action model with soft log-odds policy
- common replay interface for Bayes, leaky Bayes, anchored Bayes, and PCC-tempered updates
- explicit test and documentation of leaky Bayes as the `Pressure=1` PCC slice
- grid-averaged marginal model evidence for update-rule comparison
- report-only, action-only, and joint observation experiment
- documented action-only identifiability ambiguity
- v0.3 synthetic evidence freeze

## 0.7.0 - 2026-08-25

- Prospectively froze opportunity-conditioned exploitability as a distinct primary endpoint after the retained v0.6 global failure.
- Added matched-context scoring so deterministic utility play and each Chaos candidate are evaluated on the exact same candidate-defined strategic opportunity steps.
- Tested unchanged structured- and threshold-Chaos policies across symmetric, false-positive-costly, and false-negative-costly payoff geometries.
- Both architectures passed all frozen opportunity prevalence, unpredictability, value-preservation, and >=0.10 opportunity-conditioned exploitability-resistance gates in all three payoff geometries.
- Retained the v0.6 global logistic exploitability failure; v0.7 supports a narrower local/conditional claim rather than retroactively changing the earlier criterion.

## 0.11.0 - 2026-08-25

- Added exact three-state simplex prediction and observation update maps.
- Prospectively validated affordance-transition dynamics over all 480,000 frozen v0.9 posterior updates.
- Verified the Markov prediction gap-contraction identity and exact 1/2/3-action transition matrices.
- Showed dynamically that the obs=0.55, switch=0.30 regime routes mass into two-action bands without entering the three-action region.

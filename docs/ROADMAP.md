# Roadmap

## Phase 1 — Synthetic baseline

- binary hypothesis model
- PCC parameter sweeps
- world-switch adaptation
- entropy / revision observables
- information-geometric validation
- simulation-based inverse inference

## Phase 2 — Better inference models

Completed in v0.2 baseline:

- explicit raw -> corrupted -> belief observation channel
- likelihood-based discrete posterior over evidence pressure, belief control, and observation corruption
- analytic marginalization of latent binary received observations
- observation-access and sequence-length identifiability experiments

Next:

- categorical and continuous hypotheses
- Beta-Bernoulli and Dirichlet-multinomial conjugate models
- explicit source reliability
- misspecified likelihoods
- hierarchical priors
- sequential Monte Carlo for latent belief states

## Phase 3 — Agents and reported beliefs

Completed in v0.3 baseline:

- noisy reported probabilities in log-odds space
- binary soft-decision action observation model
- latent-belief replay under Bayes, leaky Bayes, anchored Bayes, and PCC-tempered updates
- grid-averaged model evidence with within-model complexity penalty
- explicit documentation that leaky Bayes is the `Pressure=1` slice of PCC
- report-only, action-only, and joint model-identifiability experiment

Next:

- jointly infer decision-policy parameters rather than fixing them
- richer action tasks with varying payoffs
- allow received evidence and internal belief to be latent simultaneously
- compare against additional genuinely distinct update families
- repeated-seed calibration of model probabilities and recovery rates (20-seed pilot complete; 100-seed frozen confirmation pending)

## Phase 4 — EBID tests

- local perturbation growth experiments
- Fisher metric for multinomial simplex
- detectability limits for entropy/KL early-warning signals
- distinguish true instability from stochastic posterior movement

## Phase 5 — Cross-domain applications

Potential targets only after synthetic falsification work:

- multi-agent forecasting
- scientific belief revision
- adversarial information environments
- adaptive control / active inference
- market expectations

No human-domain interpretation should precede a clear observation model and appropriate validation.


## v0.4.1 completed: mature Chaos probe

- separated Chaos into unpredictability, adequacy, and exploitability resistance
- retained a failed history-only exploitability gate
- passed a prospectively frozen context-conditioned exploitation diagnostic

## v0.5.0 completed: adaptive Chaos replication

- added an online-updating context-aware exploiter
- retained the original structured-Chaos policy unchanged
- added an independently specified stochastic-threshold Chaos architecture
- both candidates passed frozen unpredictability, adequacy, value-preservation, and adaptive-exploitability gates
- next: vary exploiter model class and environmental payoff/asymmetry before claiming broader portability

## v0.6.0 completed: asymmetric-value / logistic falsification

- introduced a fixed asymmetric payoff matrix and utility-optimal posterior threshold of 2/3
- replaced the count-table opponent with a distinct online logistic exploiter
- both Chaos candidates preserved utility but failed the frozen 5-point global exploitability-reduction gate
- the exploitability reduction was concentrated on the 25--29% of decisions where mixing was strategically live
- next: prospectively separate **global exploitability** from **opportunity-conditioned exploitability**, and test whether the latter replicates across payoff matrices without retuning policy coefficients

## Phase 5 — Opportunity-conditioned Chaos robustness

Completed in v0.7.0:

- prospectively separated global exploitability from opportunity-conditioned exploitability;
- introduced matched-context scoring against deterministic utility play;
- preserved the two existing Chaos policy architectures without coefficient retuning;
- replicated the local conditional exploitability effect across payoff thresholds 1/3, 1/2, and 2/3;
- retained the earlier v0.6 global failure unchanged.

Next: keep the v0.7 opportunity definition fixed and attempt falsification under a new opponent model class and/or altered environment dynamics before making any broader cross-domain claim.


## Phase 6 — Multi-option Chaos transfer

v0.8 completed as a retained negative result:

- three-state / three-action Bayesian tracking substrate;
- categorical filtering and normalized ternary policy entropy;
- two independent multi-action Chaos architectures;
- online multiclass softmax exploiter;
- explicit branch-opportunity and three-way-opportunity masks;
- full frozen transfer gate failed because the environment rarely sustained multi-action viable sets;
- exploitability resistance was architecture-dependent.

Next:

- do **not** retune v0.8 policies post hoc;
- prospectively vary environmental information structure (observation quality, transition persistence, or payoff geometry) as blocked conditions while keeping the v0.8 policy definitions fixed;
- test the antecedent hypothesis that mature multi-option Chaos requires sufficient viable-set affordance before asking about exploitability;
- only after that, consider continuous or larger action spaces.


## Phase 7 — Environmental affordance mapping

v0.9 completed as a retained partial failure:

- held the two v0.8 multi-action Chaos policies fixed;
- prospectively varied observation reliability and state-switch probability over a 12-cell grid;
- demonstrated that low observation reliability can turn a rare-branch environment into one with frequent two- and three-option branch sets;
- both candidates passed all local Chaos gates at the prespecified low-information/high-volatility anchor;
- retained failure of the frozen monotonic-volatility prediction: more state switching increased branch frequency without necessarily increasing three-way branch cardinality.

Next:

- treat environmental affordance as an interaction surface rather than a scalar uncertainty axis;
- prospectively test whether branch **cardinality** can be predicted from posterior/utility geometry before simulation;
- distinguish two-option ambiguity from genuine multi-option ambiguity analytically;
- do not choose a new passing environment cell post hoc.

## v0.10 complete: analytical affordance geometry

The one/two/three-action decision regions of the frozen utility-topset policy are now analytically characterized and prospectively validated. Next: derive/test how the Markov transition and observation update transport posterior mass across these fixed simplex regions.

## v0.11 completed: affordance-transition dynamics

The one-step three-state Bayesian map and the frozen utility-topset affordance geometry now jointly predict exact transitions among 1-, 2-, and 3-action regions. Next: derive observation-specific preimages of each affordance region so transition probabilities can be characterized from prior-belief geometry before simulation.

## v0.12 completed: observation-specific transition preimages

The one-step preimages of the frozen one-, two-, and three-action affordance regions are now explicit affine partitions of the prior probability simplex for each observation. All frozen validation gates passed across 480,000 updates.

Next: use these preimage regions together with the observation probabilities to derive **conditional transition probabilities** between affordance classes from a prior belief, rather than only deterministic destinations conditional on a realized observation. This would turn the geometric transition surfaces into a stochastic affordance-transition kernel.

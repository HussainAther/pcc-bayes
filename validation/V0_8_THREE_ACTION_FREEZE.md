# v0.8 Three-action Chaos transfer freeze

Date frozen: 2026-08-25

## Question

Does the prospectively defined v0.7 opportunity-conditioned PCC Chaos signature survive transfer from a binary decision problem to a genuinely three-state, three-action Bayesian tracking task with branch points that can keep all three actions strategically live?

This specification is frozen before the v0.8 confirmatory results are inspected.

## Environment

A hidden state `s_t in {0,1,2}` follows a symmetric Markov process:

- steps per episode: 400
- state-switch probability: 0.10 per step
- conditional on switching, the next state is chosen uniformly from the other two states
- public observation `y_t in {0,1,2}`
- observation accuracy: 0.65
- conditional on an observation error, either incorrect symbol is emitted with equal probability
- prior: uniform over three states
- calibration seeds: 0--49
- evaluation seeds: 1000--1099

The agent uses the correct three-state Bayesian filter. The exploiter sees public observations and prior public actions, but not the hidden state or the agent's posterior.

## Payoffs

Actions are state guesses. Reward is:

- correct action: `+1.0`
- incorrect action: `-1.0`

The deterministic baseline chooses the action with maximal posterior probability, with ties broken toward the lowest action index.

No payoff parameter is fit to the confirmatory result.

## Frozen Chaos architectures

Two independently structured three-action policies are tested.

### A. Utility-topset Chaos

Let `u_a = 2 p(s=a) - 1` be expected reward for action `a`, and `u_max=max_a u_a`.

An action is viable when `u_max - u_a <= 0.30`.

- if one action is viable, choose it deterministically;
- if `m>=2` actions are viable, assign probability `0.60` to the best action and distribute `0.40` uniformly among the other viable actions;
- non-viable actions receive probability zero.

### B. Perturbed-utility Chaos

On every decision, draw independent `epsilon_a ~ Uniform(-0.18, +0.18)` and choose

`argmax_a (u_a + epsilon_a)`.

For opportunity masks and entropy accounting, the marginal action probabilities are estimated deterministically from a frozen 129-point per-action perturbation grid generated from seed `8080`. The realized action uses fresh seeded perturbations per episode.

This architecture injects stochasticity through the decision criterion rather than through an explicit viable-set mixture.

No Chaos coefficient is retuned after result inspection.

## Multiclass exploiter

Use an online three-class softmax-regression exploiter with frozen features:

- intercept;
- one-hot current observation (3);
- one-hot previous observation (3);
- one-hot previous action (3);
- one-hot action two steps back (3).

Training protocol:

- learning rate: 0.08
- L2 coefficient: 0.001
- calibration passes: 4
- online prequential evaluation: predict, score, then update after each revealed action
- ties in predicted class probability break toward the lowest action index

Separate exploiters are calibrated for each policy.

## Opportunity definitions

For each Chaos candidate and each decision step, define support size

`K_t = number of actions with marginal policy probability > 1e-12`.

A **branch opportunity** has `K_t >= 2`.

A **three-way opportunity** has `K_t = 3`.

The candidate's frozen marginal policy defines these masks before exploiter correctness is observed.

For matched contrasts, the same candidate-defined branch-opportunity mask is applied to the deterministic baseline trajectory generated from the same seed and therefore the same hidden/public environment trajectory.

## Primary exploitability endpoint

For candidate `c`, define

`Delta_opp(c) = Accuracy_exploiter(deterministic | c-branch opportunities) - Accuracy_exploiter(c | c-branch opportunities)`.

Frozen primary gate:

`Delta_opp(c) >= 0.10`.

## Gates per candidate

Each Chaos architecture must independently satisfy all six gates:

1. **Branch prevalence:** branch-opportunity fraction between `0.15` and `0.70`.
2. **Genuine three-way branching:** three-way-opportunity fraction at least `0.05`.
3. **Unpredictability:** mean normalized policy entropy at least deterministic entropy + `0.10`, where entropy is normalized by `log2(3)`.
4. **Value preservation:** candidate mean reward at least deterministic mean reward - `0.15`.
5. **Opportunity-conditioned exploitability resistance:** `Delta_opp >= 0.10`.
6. **Non-random adequacy:** candidate mean reward at least uniform-random mean reward + `0.20`.

v0.8 passes only if both candidate architectures pass all six gates.

## Secondary outputs

Report without additional pass/fail gates:

- global multiclass exploiter accuracy;
- branch-opportunity exploiter accuracy for candidate and matched deterministic baseline;
- three-way-opportunity exploiter accuracy;
- classification accuracy;
- mean reward;
- normalized policy entropy;
- branch-opportunity fraction;
- three-way-opportunity fraction;
- mean support size.

## Interpretation boundaries

Passing would support transfer of the v0.7 local PCC Chaos signature to a richer three-option Bayesian decision substrate: strategically adequate policies can preserve multiple live alternatives at matched decision branch points while reducing conditional exploitability.

It would not establish universal PCC Chaos, equilibrium optimality, human cognition, fighting-game validity, or cross-domain universality.

Failure is retained without post-hoc retuning.

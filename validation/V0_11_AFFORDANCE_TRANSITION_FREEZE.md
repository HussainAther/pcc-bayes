# v0.11 Affordance-Transition Freeze

Status: prospective freeze, written before the v0.11 confirmatory run.

## Question
Can the motion of posterior mass between the frozen 1-, 2-, and 3-action affordance regions be predicted exactly from the one-step Bayesian map on the three-state probability simplex?

## Frozen setting
Reuse the full v0.9 environment grid without changing any policy coefficient:

- observation accuracy: 0.45, 0.55, 0.65, 0.80
- switch probability: 0.03, 0.10, 0.30
- 100 evaluation seeds per cell
- 400 steps per seed
- utility-topset gap: 0.30, equivalent to posterior gap 0.15

## Analytical map
For switch probability s, define the symmetric transition matrix with stay probability 1-s and each off-diagonal transition s/2.

For a posterior p before prediction, the predictive belief q is

    q = p T.

For every pair i,j,

    q_i - q_j = (1 - 3s/2) (p_i - p_j).

Thus the prediction step contracts every pairwise simplex gap by the exact factor

    kappa(s) = 1 - 3s/2.

Given observation y and observation accuracy a, define

    l_y(i) = a                  if i = y
             (1-a)/2           otherwise.

The posterior update is

    p'_i = q_i l_y(i) / sum_j q_j l_y(j).

No fitted parameters enter this map.

## Affordance regions
Using the already frozen v0.10 utility-topset geometry, with sorted posterior coordinates p_(1) >= p_(2) >= p_(3):

- 1 action: p_(1) - p_(2) > 0.15
- 2 actions: p_(1) - p_(2) <= 0.15 and p_(1) - p_(3) > 0.15
- 3 actions: p_(1) - p_(3) <= 0.15

## Confirmatory predictions / gates
Across all 480,000 frozen posterior updates:

1. The analytical one-step map must reproduce the implemented Markov-filter posterior with maximum absolute coordinate error <= 1e-12.
2. The analytical map must reproduce the implemented post-update affordance class with zero mismatches.
3. The full 3x3 affordance transition-count matrix (1/2/3 actions before update -> 1/2/3 actions after update) must match an independently classified implementation matrix exactly in every grid cell.
4. The prediction-only gap contraction identity must hold numerically with maximum absolute pairwise-gap residual <= 1e-12.
5. The v0.10/v0.9 occupancy fractions recovered from the dynamically generated posteriors must match the frozen historical branch and three-action fractions to <= 1e-12.

Failure of any gate is retained. No changes to the region threshold, environment grid, seeds, or likelihood model are permitted after inspection.

## Interpretation constraint
Passing these gates establishes an exact dynamical account for this finite symmetric three-state Bayesian substrate. It does not establish universal PCC dynamics or a general law for arbitrary decision geometries.

# v0.12 Observation-Specific Affordance-Preimage Freeze

Status: prospective freeze, written before the v0.12 confirmatory run.

## Question
For each possible observation in the frozen three-state Bayesian substrate, can the exact subset of the *prior* probability simplex that maps into the one-, two-, or three-action affordance regions be characterized by affine transition surfaces, before simulating the posterior?

## Frozen setting
Reuse the full v0.9/v0.11 environment grid without changing any decision-policy coefficient:

- observation accuracy: 0.45, 0.55, 0.65, 0.80
- switch probability: 0.03, 0.10, 0.30
- observations: y in {0,1,2}
- 100 evaluation seeds per cell
- 400 updates per seed
- utility-topset gap: 0.30, hence posterior affordance gap delta = 0.15

## Preimage derivation
For prior belief p, switch probability s, and observation y,

    kappa = 1 - 3s/2
    q_i = kappa p_i + s/2

Let l_i be the frozen categorical observation likelihood:

    l_i = a                  if i = y
          (1-a)/2           otherwise.

Define unnormalized posterior scores

    r_i = l_i q_i
    Z = sum_h r_h.

The posterior is p'_i = r_i / Z. Therefore every oriented posterior affordance boundary

    p'_i - p'_j = delta

pulls back exactly to

    F_ij(p) = r_i - r_j - delta Z = 0.

Because each r_i is affine in p, each F_ij is an affine line on the prior simplex. With e_i the ith coordinate vector and l the likelihood vector,

    F_ij(p) = A_ij dot p + c_ij,

where

    A_ij = kappa (l_i e_i - l_j e_j - delta l)
    c_ij = (s/2) (l_i - l_j - delta).

No fitted parameters enter these surfaces.

## Preimage classification
Let t be the index with largest unnormalized score r_t. An action j is live after the update iff

    r_t - r_j <= delta Z

using the same 1e-15 numerical boundary tolerance as the frozen utility-topset implementation.

Thus the number of live actions can be classified directly in prior coordinates plus the observation, without forming the normalized posterior.

## Confirmatory predictions / gates
Across all 480,000 frozen updates:

1. The affine boundary identity must hold with maximum residual

       |F_ij(p) - Z (p'_i - p'_j - delta)| <= 1e-12

   over every ordered pair i != j.
2. Direct preimage classification from r_t - r_j <= delta Z must match the implemented posterior affordance class with zero mismatches.
3. For every grid cell, the full 3x3 before->after affordance transition matrix obtained from the preimage classifier must match the frozen v0.11 transition matrix exactly.
4. Observation-specific post-update class counts produced by the preimage classifier must sum exactly to the implemented counts for each y in {0,1,2}.
5. All generated affine surfaces must be finite and must reproduce the score-form boundary value to <= 1e-12 on the tested priors.

Failure of any gate is retained. No adjustment to delta, utility gap, likelihoods, seeds, grid, or numerical gate is permitted after inspection.

## Interpretation constraint
Passing establishes exact observation-specific preimages for this finite symmetric three-state Bayesian model and frozen utility-topset geometry. It does not imply that arbitrary Bayesian models, utility functions, or PCC systems have affine affordance preimages.

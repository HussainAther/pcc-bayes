# v0.11 Affordance-Transition Result

Status: PASS.

The prospectively frozen analytical one-step Bayesian map reproduced the existing three-state Markov-filter implementation across the complete frozen v0.9 grid.

## Confirmatory totals

- 12 environment cells
- 100 seeds per cell
- 400 updates per seed
- 480,000 posterior updates total
- maximum posterior coordinate error: 5.551e-16
- maximum prediction-gap contraction residual: 2.220e-16
- affordance-class mismatches: 0
- all 3x3 affordance transition matrices matched exactly
- all historical v0.9/v0.10 occupancy fractions matched to the frozen tolerance

All frozen gates passed.

## Dynamical interpretation

The Markov prediction step has the exact form

    q_i = (1 - 3s/2) p_i + s/2,

so every pairwise posterior gap contracts by

    kappa(s) = 1 - 3s/2.

The observation step then reweights the predicted belief by a likelihood vector that privileges the observed state and renormalizes. Thus transition volatility and evidence act as geometrically distinct operators: the former contracts posterior gaps toward the simplex center, while the latter repolarizes belief toward an observation-dependent direction.

The previously surprising v0.9 cell at observation accuracy 0.55 and switch probability 0.30 is especially diagnostic. Across 40,000 updates it produced:

- 11,368 direct 1-action -> 2-action transitions;
- 0 direct 1-action -> 3-action transitions;
- 0 direct 2-action -> 3-action transitions;
- 0 three-action posterior occupancy.

Hence increased volatility did not merely create generic uncertainty. Under this likelihood geometry, posterior transport was repeatedly routed into the two-action affordance bands without entering the central three-action region.

By contrast, the lower-information cell at observation accuracy 0.45 and switch probability 0.30 exhibited substantial transport into the three-action region, including 4,245 direct 1 -> 3 transitions and 3,929 direct 2 -> 3 transitions.

## Claim discipline

This result establishes an exact affordance-transition account for the finite symmetric three-state Bayesian substrate and the frozen utility-topset decision geometry. It does not establish a universal PCC transition law. The natural next test is to derive transition-boundary preimages: for each observation symbol, characterize analytically which prior-belief regions map into the 1-, 2-, and 3-action affordance regions after one full Bayesian step.

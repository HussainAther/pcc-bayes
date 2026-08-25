# v0.10 Analytical Affordance Geometry Result

Status: **PASS** against the prospectively frozen analytical boundary test.

## Result

The frozen utility-topset policy has an exact posterior-simplex characterization.
With state-matching utility

`u_i = 2 p_i - 1`

and frozen utility gap `g = 0.30`, the equivalent posterior gap is

`delta = g / 2 = 0.15`.

For sorted posterior coordinates `p_(1) >= p_(2) >= p_(3)`:

- one action is viable when `p_(1) - p_(2) > 0.15`;
- two actions are viable when `p_(1) - p_(2) <= 0.15` and `p_(1) - p_(3) > 0.15`;
- three actions are viable when `p_(1) - p_(3) <= 0.15`.

The implementation uses its pre-existing `1e-15` numerical tolerance at equality; the analytical classifier mirrors that implementation convention without changing the scientific boundary.

## Confirmatory comparison

The comparison covered the complete frozen v0.9 grid:

- 4 observation-accuracy values;
- 3 state-switch probabilities;
- 100 evaluation seeds per cell;
- 400 posterior states per seed;
- 480,000 posterior states total.

Observed outcomes:

- analytical/implemented support-cardinality mismatches: **0 / 480,000**;
- all 12 cell-level one/two/three support fractions matched exactly to the frozen tolerance;
- all 12 analytical branch fractions matched the historical v0.9 branch fractions;
- all 12 analytical three-action fractions matched the historical v0.9 three-way fractions.

The prospective v0.10 test therefore passes.

## Geometry clarifies the v0.9 negative result

The analytical partition separates branch prevalence from branch cardinality.
For example, at observation accuracy `0.55` and switch probability `0.30`:

- one-action region occupancy: `0.6961`;
- two-action region occupancy: `0.3039`;
- three-action region occupancy: `0.0000`.

Thus the increased state volatility did create substantially more branch states, but it moved posterior mass into the two-action bands rather than the central three-action region. This explains why the frozen v0.9 prediction that higher switching would increase three-way branching failed.

At the prespecified low-information/high-volatility anchor (`0.45`, `0.30`), the corresponding occupancies were:

- one action: `0.4273`;
- two actions: `0.3085`;
- three actions: `0.2642`.

The high three-way affordance at that anchor is therefore directly interpretable as posterior occupancy of the simplex region satisfying `p_(1) - p_(3) <= 0.15`.

## Interpretation

This result is exact for the frozen utility-topset policy. It establishes that the policy's viable-set cardinality is a piecewise-polyhedral function of posterior belief geometry.

It does **not** establish a universal PCC boundary. It also does not by itself predict how frequently a given environment will visit each region. That occupancy depends on the Bayesian filtering dynamics induced by transition and observation structure.

The next theoretical problem is therefore no longer to characterize the decision regions; it is to characterize the **transport of posterior mass through those regions** as environmental information and volatility change.

# v0.12 Observation-Specific Affordance-Preimage Result

Status: **PASS**.

The frozen v0.12 test evaluated the exact prior-simplex preimages of the one-, two-, and three-action affordance regions under each possible observation in the three-state Bayesian tracking model.

## Confirmatory result

Across the frozen v0.9/v0.11 grid:

- 12 environment cells
- 3 possible observations
- 100 seeds per cell
- 400 updates per seed
- 480,000 updates total
- 216 observation/cell/oriented-pair affine boundary surfaces

All frozen gates passed.

- maximum posterior-coordinate reconstruction error: `4.441e-16`
- maximum affine-score identity residual: `3.331e-16`
- maximum normalized boundary identity residual: `4.441e-16`
- preimage affordance-class mismatches: `0 / 480000`
- every preimage-derived 3x3 affordance transition matrix matched the frozen v0.11 matrix exactly
- every observation-specific class count matched the implemented posterior classification exactly

## Exact boundary form

For prior belief `p`, switch probability `s`, observation `y`, observation accuracy `a`, and frozen posterior affordance gap `delta=0.15`, define

    kappa = 1 - 3s/2
    q_i = kappa p_i + s/2
    r_i = l_y(i) q_i
    Z = sum_i r_i

The pullback of the posterior boundary

    p'_i - p'_j = delta

is the affine prior-space surface

    F_ij(p) = r_i - r_j - delta Z = 0.

Equivalently,

    F_ij(p) = A_ij dot p + c_ij,

with coefficients fixed analytically by `(s,a,y,i,j,delta)`.

## Concrete example

At observation accuracy `0.55`, switch probability `0.30`, and observation `y=0`, one oriented boundary (`action 0` versus `action 1`) is

    0.257125 p0 - 0.1423125 p1 - 0.0185625 p2 + 0.02625 = 0.

The corresponding action-0 versus action-2 boundary is obtained by the expected permutation of `p1` and `p2`.

These lines partition the prior simplex into observation-specific regions whose points are guaranteed to land in the frozen one-, two-, or three-action affordance regions after the Bayesian update.

## Interpretation

v0.10 solved the static posterior affordance geometry. v0.11 solved the forward one-step transport map. v0.12 solves the inverse geometric question for one step: before seeing the normalized posterior, the prior simplex can be partitioned into exact observation-conditioned preimages of each affordance class.

This establishes an exact result for the finite symmetric three-state Bayesian model and frozen utility-topset decision rule. It does not imply affine preimages for arbitrary likelihoods, nonlinear decision utilities, continuous state spaces, or general PCC systems.

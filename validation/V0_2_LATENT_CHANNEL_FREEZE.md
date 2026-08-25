# v0.2 latent-channel synthetic evidence freeze

Date: 2026-08-25

## Frozen question

Under a known binary world model, how does access to raw evidence, received evidence, or beliefs alone affect recovery of the synthetic PCC observation/update parameters?

## Generating parameters

- Pressure: `1.5`
- Control: `1.2`
- Chaos: `0.15`
- binary hypotheses: Bernoulli `0.3` versus `0.7`

## Experiment 08: one-run observation-access comparison

For a 120-step run with seed 21:

- realized corruption rate: `0.175`
- raw + received evidence + beliefs: posterior mean Chaos `0.1803`, effective support `2.83` grid points
- received evidence + beliefs: posterior mean Chaos `0.1009`, effective support `5.91` grid points
- beliefs only: posterior mean Chaos `0.1981`, effective support `6.20` grid points

All three conditions recover the generating Pressure and Control grid point in this deterministic synthetic trajectory. Chaos remains substantially more weakly identified when the raw channel is hidden.

## Experiment 09: sequence-length identifiability

This experiment conditions on the known generating Pressure and Control values and isolates Chaos recovery across 20 synthetic seeds.

At sequence length 20, Chaos posterior-mean RMSE is approximately:

- raw + received evidence + beliefs: `0.0425`
- received evidence + beliefs: `0.0382`
- beliefs only: `0.0309`

At sequence length 160:

- raw + received evidence + beliefs: `0.0299`
- received evidence + beliefs: `0.0494`
- beliefs only: `0.0297`

RMSE alone is not the key identifiability statistic. Posterior concentration distinguishes the conditions. Mean effective grid support changes from about `4.85 -> 2.28` for raw + received evidence as length increases from 20 to 160, while beliefs-only support remains near `6.69` after saturation. Thus the beliefs-only posterior does not accumulate useful Chaos information indefinitely.

## Interpretation

The v0.2 result is a boundary result:

1. Pressure and Control are directly identified from exact synthetic belief transitions when the generating update family is correctly specified.
2. Chaos is best localized when the pre-corruption and post-corruption evidence streams are both available.
3. Hiding the raw channel broadens the posterior over Chaos.
4. Belief-only inference can hit an information ceiling because posterior saturation destroys observation-level distinguishability.

No claim of human cognitive validity is made.

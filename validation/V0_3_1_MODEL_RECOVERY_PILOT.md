# v0.3.1 Repeated-Seed Model-Recovery Pilot

This is a computational pilot of the prospectively frozen design in
`V0_3_1_MODEL_RECOVERY_FREEZE.md`. It uses the first 20 frozen seeds rather than the
full 100-seed confirmatory set. The confirmatory design is unchanged.

## Pilot configuration

- seeds: 0..19
- sequence length: 80 updates
- report noise: sigma_logit = 0.25
- action beta: 2.0
- candidate generators and inference grids: exactly as frozen

## Top-1 model-family recovery

| true generator | reports | actions | reports + actions |
| --- | ---: | ---: | ---: |
| Bayes | 1.00 | 1.00 | 1.00 |
| leaky Bayes | 1.00 | 0.80 | 1.00 |
| anchored Bayes | 0.95 | 0.85 | 1.00 |
| PCC | 1.00 | 0.65 | 1.00 |

For a true PCC generator, the action-only winners were:

- PCC: 13/20
- leaky Bayes: 5/20
- anchored Bayes: 2/20
- Bayes: 0/20

The mean posterior probability assigned to the true PCC model was approximately
1.000 for reports, 0.594 for actions, and 1.000 for reports + actions.

## Parameter recovery

Exact-grid parameter recovery across all trials was perfect for the report condition
for Bayes, leaky Bayes, and PCC, and 0.95 for anchored Bayes. Under actions only,
exact recovery declined to 0.70 for leaky Bayes, 0.75 for anchored Bayes, and 0.55
for PCC. Joint reports + actions recovered the exact frozen grid point in all 20 pilot
seeds for every generator.

## Interpretation

The pilot supports all frozen directional hypotheses without requiring a post-hoc
grid or threshold change. Binary actions discard substantial information about belief
magnitude, producing family and parameter confounding that is much weaker under
reported probabilities. PCC-versus-leaky confusion is especially visible in the
action-only condition, consistent with the nesting of leaky Bayes inside the PCC
family when Pressure = 1.

This result is a measurement-channel and model-identifiability result. It does not
establish PCC as a cognitive law, and it should not be promoted to a 100-seed
confirmatory result until the full frozen seed set is executed.

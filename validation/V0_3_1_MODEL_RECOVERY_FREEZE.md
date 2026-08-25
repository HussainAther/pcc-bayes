# v0.3.1 Repeated-Seed Model-Recovery Freeze

Status: frozen before confirmatory execution.

## Question

When internal beliefs are latent, how reliably can the measurement layer recover the
update-rule family from noisy reports, binary actions, or both across independent
synthetic realizations?

This experiment tests measurement and identifiability. It does **not** establish that
PCC parameters are universal cognitive constructs.

## Candidate generators

Four prespecified generators are used:

- `bayes`: ordinary Bayes.
- `leaky_bayes`: leak = 0.60.
- `anchored_bayes`: anchor strength = 0.25.
- `pcc`: Pressure = 1.50, Control = 0.60.

The received evidence sequence is observed by the analyst in this experiment. Chaos
in the upstream observation channel is therefore not inferred here; it belongs to the
separate latent-channel experiments.

## Candidate inference grid

- leak: {0.40, 0.60, 0.80, 1.00}
- anchor strength: {0.00, 0.10, 0.25, 0.50}
- Pressure: {0.75, 1.00, 1.25, 1.50}
- Control: {0.40, 0.60, 0.80, 1.00}

Bayes has no free grid parameter. The PCC family intentionally contains ordinary
Bayes and leaky-Bayes-like slices; grid-averaged evidence is retained to penalize
unused flexibility.

## Confirmatory calibration

- seeds: 0..99
- sequence length: 80 updates
- binary world: p(x=1|H0)=0.30, p(x=1|H1)=0.70, true H=1
- prior: (0.5, 0.5)
- report noise: sigma_logit = 0.25
- action policy: beta = 2.0, bias = 0

For each generator and seed, generate one evidence sequence, reconstruct the latent
trajectory under the true generator, then generate reports and actions from that same
latent trajectory. Compare all four candidate update families using only the received
evidence plus the designated measurement channel.

Measurement conditions:

1. reports only
2. actions only
3. reports + actions

## Primary outcomes

For each true generator x measurement condition:

- top-1 recovery rate;
- mean posterior probability assigned to the true model;
- full true-model x inferred-model confusion counts.

For parameterized true generators, record exact recovery of the prespecified true
grid point when the correct family is top-ranked.

## Frozen directional hypotheses

H1. Report-based observations will recover update-rule family more reliably than
binary actions alone.

H2. Joint reports + actions will be at least as informative as actions alone and will
not systematically degrade report-based recovery.

H3. Action-only data will show greater confusion between `pcc` and `leaky_bayes`
than report-based data because the binary decision channel compresses belief
magnitude.

H4. Recovery will be non-uniform across model families because the candidate models
are nested or partially overlapping; this is treated as an identifiability result, not
repaired by post-hoc threshold or grid changes.

## Interpretation rule

No acceptance threshold will be tuned after observing the confirmatory output. Any
poorly recovered family or measurement condition remains a retained negative or
boundary result. Follow-up changes require a new prospective experiment.

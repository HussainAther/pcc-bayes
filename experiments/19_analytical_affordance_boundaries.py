from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from pcc_bayes.affordance_geometry import classify_topset_supports, support_fraction_summary
from pcc_bayes.multiclass_chaos import (
    ThreeStateTrackingConfig,
    filter_three_state_markov,
    generate_three_state_episode,
    utility_topset_chaos_probabilities,
)

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "results" / "18_information_affordance_map.csv"
OUT = ROOT / "results" / "19_analytical_affordance_boundaries.csv"

OBSERVATION_ACCURACIES = (0.45, 0.55, 0.65, 0.80)
SWITCH_PROBABILITIES = (0.03, 0.10, 0.30)
EVALUATION_SEEDS = tuple(range(1000, 1100))
TOL = 1e-12


def load_historical():
    with HISTORICAL.open(newline="") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for row in rows:
        if row["candidate_policy"] != "utility_topset_chaos":
            continue
        key = (float(row["observation_accuracy"]), float(row["switch_probability"]))
        out[key] = row
    return out


def main():
    historical = load_historical()
    rows = []
    total_states = 0
    total_mismatches = 0

    for switch_probability in SWITCH_PROBABILITIES:
        for observation_accuracy in OBSERVATION_ACCURACIES:
            config = ThreeStateTrackingConfig(
                steps=400,
                switch_probability=switch_probability,
                observation_accuracy=observation_accuracy,
            )
            predicted_parts = []
            implemented_parts = []
            for seed in EVALUATION_SEEDS:
                _, observations = generate_three_state_episode(config, seed)
                beliefs = filter_three_state_markov(
                    observations,
                    switch_probability=switch_probability,
                    observation_accuracy=observation_accuracy,
                )
                predicted = classify_topset_supports(beliefs, utility_gap=0.30)
                implemented = np.asarray([
                    np.sum(utility_topset_chaos_probabilities(b, utility_gap=0.30) > 1e-12)
                    for b in beliefs
                ], dtype=int)
                predicted_parts.append(predicted)
                implemented_parts.append(implemented)

            predicted = np.concatenate(predicted_parts)
            implemented = np.concatenate(implemented_parts)
            mismatch_count = int(np.sum(predicted != implemented))
            summary = support_fraction_summary(predicted)
            implemented_summary = support_fraction_summary(implemented)
            hist = historical[(observation_accuracy, switch_probability)]
            hist_branch = float(hist["branch_opportunity_fraction"])
            hist_three = float(hist["three_way_opportunity_fraction"])

            row = {
                "observation_accuracy": observation_accuracy,
                "switch_probability": switch_probability,
                "states": len(predicted),
                "mismatch_count": mismatch_count,
                **{f"predicted_{k}": v for k, v in summary.items()},
                **{f"implemented_{k}": v for k, v in implemented_summary.items()},
                "historical_branch_fraction": hist_branch,
                "historical_three_action_fraction": hist_three,
                "gate_exact_state_classification": mismatch_count == 0,
                "gate_cell_fraction_match": all(
                    abs(summary[k] - implemented_summary[k]) <= TOL
                    for k in summary
                ),
                "gate_historical_branch_match": abs(summary["branch_fraction"] - hist_branch) <= TOL,
                "gate_historical_three_match": abs(summary["three_action_fraction"] - hist_three) <= TOL,
            }
            row["cell_pass"] = all(
                value for key, value in row.items() if key.startswith("gate_")
            )
            rows.append(row)
            total_states += len(predicted)
            total_mismatches += mismatch_count

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"tested posterior states: {total_states}")
    print(f"analytical/implementation mismatches: {total_mismatches}")
    print()
    for row in rows:
        print(
            f"obs={row['observation_accuracy']:.2f} switch={row['switch_probability']:.2f} "
            f"one={row['predicted_one_action_fraction']:.4f} "
            f"two={row['predicted_two_action_fraction']:.4f} "
            f"three={row['predicted_three_action_fraction']:.4f} "
            f"branch={row['predicted_branch_fraction']:.4f} "
            f"{'PASS' if row['cell_pass'] else 'FAIL'}"
        )
    overall = all(row["cell_pass"] for row in rows)
    print(f"\nv0.10 analytical affordance geometry: {'PASS' if overall else 'FAIL'}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

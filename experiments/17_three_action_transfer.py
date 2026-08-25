from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.multiclass_chaos import (
    ThreeStateTrackingConfig,
    evaluate_three_action_transfer,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "17_three_action_transfer.csv"
CANDIDATES = ("utility_topset_chaos", "perturbed_utility_chaos")


def gates(row):
    return {
        "branch_prevalence": 0.15 <= row["branch_opportunity_fraction"] <= 0.70,
        "three_way_branching": row["three_way_opportunity_fraction"] >= 0.05,
        "unpredictability": row["candidate_policy_entropy"] >= row["baseline_policy_entropy"] + 0.10,
        "value_preservation": row["candidate_mean_reward"] >= row["baseline_mean_reward"] - 0.15,
        "opportunity_exploitability_resistance": row["opportunity_exploitability_reduction"] >= 0.10,
        "nonrandom_adequacy": row["candidate_mean_reward"] >= row["random_mean_reward"] + 0.20,
    }


def main():
    config = ThreeStateTrackingConfig(
        steps=400,
        switch_probability=0.10,
        observation_accuracy=0.65,
    )
    calibration_seeds = range(0, 50)
    evaluation_seeds = range(1000, 1100)

    rows = []
    all_pass = True
    for candidate in CANDIDATES:
        row = evaluate_three_action_transfer(
            candidate,
            config,
            calibration_seeds,
            evaluation_seeds,
        )
        cell_gates = gates(row)
        row.update({f"gate_{k}": v for k, v in cell_gates.items()})
        row["cell_pass"] = all(cell_gates.values())
        all_pass = all_pass and row["cell_pass"]
        rows.append(row)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"{row['candidate_policy']:27s} "
            f"reward={row['candidate_mean_reward']:.4f}/{row['baseline_mean_reward']:.4f} "
            f"random={row['random_mean_reward']:.4f} "
            f"H={row['candidate_policy_entropy']:.4f} "
            f"global={row['candidate_global_softmax_accuracy']:.4f}/{row['baseline_global_softmax_accuracy']:.4f} "
            f"branch={row['candidate_branch_softmax_accuracy']:.4f}/{row['baseline_branch_softmax_accuracy']:.4f} "
            f"delta={row['opportunity_exploitability_reduction']:.4f} "
            f"three={row['candidate_three_way_softmax_accuracy']:.4f} "
            f"branchfrac={row['branch_opportunity_fraction']:.4f} "
            f"threefrac={row['three_way_opportunity_fraction']:.4f} "
            f"support={row['mean_support_size']:.3f} "
            f"{'PASS' if row['cell_pass'] else 'FAIL'}"
        )
        failed = [k.removeprefix("gate_") for k, v in row.items() if k.startswith("gate_") and not v]
        if failed:
            print("  failed gates: " + ", ".join(failed))

    print(f"\nv0.8 three-action transfer: {'PASS' if all_pass else 'FAIL'}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.strategic_chaos import (
    AsymmetricPayoffs,
    TrackingConfig,
    evaluate_matched_opportunity_exploitability,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "16_opportunity_conditioned_robustness.csv"
CANDIDATES = ("utility_structured_chaos", "utility_threshold_chaos")

PAYOFFS = {
    "symmetric": AsymmetricPayoffs(
        reward_state0_action0=1.0,
        reward_state0_action1=-1.0,
        reward_state1_action0=-1.0,
        reward_state1_action1=1.0,
    ),
    "false_positive_costly": AsymmetricPayoffs(
        reward_state0_action0=1.0,
        reward_state0_action1=-2.0,
        reward_state1_action0=-0.5,
        reward_state1_action1=1.0,
    ),
    "false_negative_costly": AsymmetricPayoffs(
        reward_state0_action0=1.0,
        reward_state0_action1=-0.5,
        reward_state1_action0=-2.0,
        reward_state1_action1=1.0,
    ),
}


def gates(row):
    return {
        "opportunity_prevalence": 0.10 <= row["opportunity_fraction"] <= 0.60,
        "unpredictability": row["candidate_policy_entropy"] >= row["baseline_policy_entropy"] + 0.10,
        "value_preservation": row["candidate_mean_reward"] >= row["baseline_mean_reward"] - 0.12,
        "opportunity_exploitability_resistance": row["opportunity_exploitability_reduction"] >= 0.10,
    }


def main():
    config = TrackingConfig(
        steps=400,
        switch_probability=0.08,
        observation_accuracy=0.75,
        extra_corruption=0.25,
    )
    calibration_seeds = range(0, 50)
    evaluation_seeds = range(1000, 1100)

    rows = []
    all_pass = True
    for payoff_name, payoffs in PAYOFFS.items():
        for candidate in CANDIDATES:
            row = evaluate_matched_opportunity_exploitability(
                candidate,
                config,
                calibration_seeds,
                evaluation_seeds,
                payoffs,
            )
            row = {"payoff_geometry": payoff_name, **row}
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
            f"{row['payoff_geometry']:23s} {row['candidate_policy']:27s} "
            f"thr={row['indifference_threshold']:.3f} "
            f"reward={row['candidate_mean_reward']:.4f}/{row['baseline_mean_reward']:.4f} "
            f"H={row['candidate_policy_entropy']:.4f} "
            f"global={row['candidate_global_logistic_accuracy']:.4f}/{row['baseline_global_logistic_accuracy']:.4f} "
            f"opp={row['candidate_opportunity_logistic_accuracy']:.4f}/{row['baseline_opportunity_logistic_accuracy']:.4f} "
            f"delta={row['opportunity_exploitability_reduction']:.4f} "
            f"frac={row['opportunity_fraction']:.4f} "
            f"{'PASS' if row['cell_pass'] else 'FAIL'}"
        )
        failed = [k.removeprefix('gate_') for k, v in row.items() if k.startswith('gate_') and not v]
        if failed:
            print(f"  failed gates: {', '.join(failed)}")

    print(f"\nv0.7 cross-payoff robustness: {'PASS' if all_pass else 'FAIL'}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.strategic_chaos import TrackingConfig, evaluate_policy_family


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "12_mature_chaos.csv"
POLICIES = (
    "predictable_value",
    "uniform_random",
    "corrupted_predictable",
    "structured_chaos",
)


def passes_structured_gates(rows_by_policy):
    p = rows_by_policy["predictable_value"]
    r = rows_by_policy["uniform_random"]
    s = rows_by_policy["structured_chaos"]
    return {
        "unpredictability": s["mean_policy_entropy"] >= p["mean_policy_entropy"] + 0.10,
        "adequacy_vs_random": s["mean_accuracy"] >= r["mean_accuracy"] + 0.15,
        "value_preservation": s["mean_accuracy"] >= p["mean_accuracy"] - 0.08,
        "exploitability_resistance": s["exploiter_accuracy"] <= p["exploiter_accuracy"] - 0.05,
    }


def substituted_candidate_passes(candidate, rows_by_policy):
    p = rows_by_policy["predictable_value"]
    r = rows_by_policy["uniform_random"]
    c = rows_by_policy[candidate]
    return (
        c["mean_policy_entropy"] >= p["mean_policy_entropy"] + 0.10
        and c["mean_accuracy"] >= r["mean_accuracy"] + 0.15
        and c["mean_accuracy"] >= p["mean_accuracy"] - 0.08
        and c["exploiter_accuracy"] <= p["exploiter_accuracy"] - 0.05
    )


def main():
    config = TrackingConfig(
        steps=400,
        switch_probability=0.08,
        observation_accuracy=0.75,
        extra_corruption=0.25,
    )
    calibration_seeds = range(0, 50)
    evaluation_seeds = range(1000, 1100)

    rows = [
        evaluate_policy_family(policy, config, calibration_seeds, evaluation_seeds)
        for policy in POLICIES
    ]
    by_policy = {row["policy"]: row for row in rows}
    gates = passes_structured_gates(by_policy)
    noise_passes = substituted_candidate_passes("corrupted_predictable", by_policy)
    random_passes = substituted_candidate_passes("uniform_random", by_policy)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"{row['policy']:24s} "
            f"U={row['mean_policy_entropy']:.4f} "
            f"A={row['mean_accuracy']:.4f} "
            f"exploit_acc={row['exploiter_accuracy']:.4f}"
        )
    print("\nstructured_chaos gates")
    for name, passed in gates.items():
        print(f"  {name:28s}: {'PASS' if passed else 'FAIL'}")
    print(f"  all_structured_gates          : {'PASS' if all(gates.values()) else 'FAIL'}")
    print(f"  corruption_baseline_all_gates: {'FAIL anti-definition' if noise_passes else 'PASS anti-definition'}")
    print(f"  random_baseline_all_gates    : {'FAIL anti-definition' if random_passes else 'PASS anti-definition'}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()

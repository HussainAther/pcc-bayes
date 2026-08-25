from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.strategic_chaos import (
    AsymmetricPayoffs,
    TrackingConfig,
    evaluate_asymmetric_logistic_exploitability,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "15_asymmetric_logistic_falsification.csv"
POLICIES = (
    "predictable_utility",
    "uniform_random",
    "utility_structured_chaos",
    "utility_threshold_chaos",
)
CANDIDATES = ("utility_structured_chaos", "utility_threshold_chaos")


def candidate_gates(candidate, by_policy):
    p = by_policy["predictable_utility"]
    r = by_policy["uniform_random"]
    c = by_policy[candidate]
    return {
        "unpredictability": c["mean_policy_entropy"] >= p["mean_policy_entropy"] + 0.10,
        "adequacy_vs_random": c["mean_reward"] >= r["mean_reward"] + 0.20,
        "value_preservation": c["mean_reward"] >= p["mean_reward"] - 0.12,
        "logistic_exploitability_resistance": (
            c["logistic_exploiter_accuracy"] <= p["logistic_exploiter_accuracy"] - 0.05
        ),
    }


def main():
    config = TrackingConfig(
        steps=400,
        switch_probability=0.08,
        observation_accuracy=0.75,
        extra_corruption=0.25,
    )
    payoffs = AsymmetricPayoffs(
        reward_state0_action0=1.0,
        reward_state0_action1=-2.0,
        reward_state1_action0=-0.5,
        reward_state1_action1=1.0,
    )
    calibration_seeds = range(0, 50)
    evaluation_seeds = range(1000, 1100)
    rows = [
        evaluate_asymmetric_logistic_exploitability(
            policy, config, calibration_seeds, evaluation_seeds, payoffs
        )
        for policy in POLICIES
    ]
    by_policy = {row["policy"]: row for row in rows}
    gates = {candidate: candidate_gates(candidate, by_policy) for candidate in CANDIDATES}

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"utility indifference threshold={payoffs.indifference_threshold:.6f}")
    for row in rows:
        print(
            f"{row['policy']:26s} "
            f"U={row['mean_policy_entropy']:.4f} "
            f"reward={row['mean_reward']:.4f} "
            f"acc={row['mean_accuracy']:.4f} "
            f"logistic={row['logistic_exploiter_accuracy']:.4f} "
            f"mix={row['mixing_opportunity_logistic_accuracy']:.4f} "
            f"mix_frac={row['mixing_opportunity_fraction']:.4f}"
        )

    print("\nFrozen candidate gates")
    for candidate in CANDIDATES:
        print(f"  {candidate}")
        for name, passed in gates[candidate].items():
            print(f"    {name:36s}: {'PASS' if passed else 'FAIL'}")
        print(f"    all                                 : {'PASS' if all(gates[candidate].values()) else 'FAIL'}")
    replication = all(all(gates[c].values()) for c in CANDIDATES)
    print(f"\nv0.6 asymmetric/logistic replication: {'PASS' if replication else 'FAIL'}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

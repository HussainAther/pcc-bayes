from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.multiclass_chaos import (
    ThreeStateTrackingConfig,
    evaluate_three_action_transfer,
    summarize_three_action_affordance,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "18_information_affordance_map.csv"
ANCHOR_OUT = ROOT / "results" / "18_information_affordance_anchor.csv"

CANDIDATES = ("utility_topset_chaos", "perturbed_utility_chaos")
OBSERVATION_ACCURACIES = (0.45, 0.55, 0.65, 0.80)
SWITCH_PROBABILITIES = (0.03, 0.10, 0.30)
EVALUATION_SEEDS = tuple(range(1000, 1100))
CALIBRATION_SEEDS = tuple(range(0, 50))
ANCHOR = (0.45, 0.30)


def _lookup(rows, candidate, observation_accuracy, switch_probability):
    for row in rows:
        if (
            row["candidate_policy"] == candidate
            and row["observation_accuracy"] == observation_accuracy
            and row["switch_probability"] == switch_probability
        ):
            return row
    raise KeyError((candidate, observation_accuracy, switch_probability))


def directional_gates(rows, candidate):
    low_info = _lookup(rows, candidate, 0.45, 0.10)
    high_info = _lookup(rows, candidate, 0.80, 0.10)
    high_switch = _lookup(rows, candidate, 0.55, 0.30)
    low_switch = _lookup(rows, candidate, 0.55, 0.03)
    return {
        "lower_information_increases_branching": (
            low_info["branch_opportunity_fraction"] > high_info["branch_opportunity_fraction"]
        ),
        "lower_information_increases_three_way": (
            low_info["three_way_opportunity_fraction"] > high_info["three_way_opportunity_fraction"]
        ),
        "higher_switching_increases_branching": (
            high_switch["branch_opportunity_fraction"] > low_switch["branch_opportunity_fraction"]
        ),
        "higher_switching_increases_three_way": (
            high_switch["three_way_opportunity_fraction"] > low_switch["three_way_opportunity_fraction"]
        ),
    }


def anchor_gates(row):
    return {
        "branch_prevalence": row["branch_opportunity_fraction"] >= 0.15,
        "three_way_prevalence": row["three_way_opportunity_fraction"] >= 0.05,
        "opportunity_exploitability_resistance": row["opportunity_exploitability_reduction"] >= 0.10,
        "value_preservation": row["candidate_mean_reward"] >= row["baseline_mean_reward"] - 0.15,
        "nonrandom_adequacy": row["candidate_mean_reward"] >= row["random_mean_reward"] + 0.20,
    }


def main():
    rows = []
    for candidate in CANDIDATES:
        for switch_probability in SWITCH_PROBABILITIES:
            for observation_accuracy in OBSERVATION_ACCURACIES:
                config = ThreeStateTrackingConfig(
                    steps=400,
                    switch_probability=switch_probability,
                    observation_accuracy=observation_accuracy,
                )
                rows.append(
                    summarize_three_action_affordance(candidate, config, EVALUATION_SEEDS)
                )

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    direction = {candidate: directional_gates(rows, candidate) for candidate in CANDIDATES}

    anchor_rows = []
    for candidate in CANDIDATES:
        config = ThreeStateTrackingConfig(
            steps=400,
            observation_accuracy=ANCHOR[0],
            switch_probability=ANCHOR[1],
        )
        row = evaluate_three_action_transfer(
            candidate,
            config,
            CALIBRATION_SEEDS,
            EVALUATION_SEEDS,
        )
        row["observation_accuracy"] = ANCHOR[0]
        row["switch_probability"] = ANCHOR[1]
        gates = anchor_gates(row)
        row.update({f"gate_{name}": value for name, value in gates.items()})
        row["cell_pass"] = all(gates.values())
        anchor_rows.append(row)

    with ANCHOR_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=anchor_rows[0].keys())
        writer.writeheader()
        writer.writerows(anchor_rows)

    all_pass = True
    for candidate in CANDIDATES:
        print(f"\n{candidate}")
        for name, passed in direction[candidate].items():
            print(f"  {name}: {'PASS' if passed else 'FAIL'}")
        all_pass = all_pass and all(direction[candidate].values())

        anchor = next(r for r in anchor_rows if r["candidate_policy"] == candidate)
        print(
            "  anchor: "
            f"branch={anchor['branch_opportunity_fraction']:.4f} "
            f"three={anchor['three_way_opportunity_fraction']:.4f} "
            f"support={anchor['mean_support_size']:.3f} "
            f"reward={anchor['candidate_mean_reward']:.4f}/{anchor['baseline_mean_reward']:.4f} "
            f"branch_expl={anchor['candidate_branch_softmax_accuracy']:.4f}/"
            f"{anchor['baseline_branch_softmax_accuracy']:.4f} "
            f"delta={anchor['opportunity_exploitability_reduction']:.4f} "
            f"{'PASS' if anchor['cell_pass'] else 'FAIL'}"
        )
        failed = [
            key.removeprefix("gate_")
            for key, value in anchor.items()
            if key.startswith("gate_") and not value
        ]
        if failed:
            print("    failed anchor gates: " + ", ".join(failed))
        all_pass = all_pass and anchor["cell_pass"]

    print(f"\nv0.9 information-structure affordance map: {'PASS' if all_pass else 'FAIL'}")
    print(f"wrote {OUT}")
    print(f"wrote {ANCHOR_OUT}")


if __name__ == "__main__":
    main()

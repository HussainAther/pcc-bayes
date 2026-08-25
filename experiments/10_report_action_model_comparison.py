from __future__ import annotations

import csv
from pathlib import Path

from pcc_bayes.model_comparison import compare_update_models
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.reporting import simulate_actions, simulate_reported_beliefs
from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning


OUT = Path(__file__).resolve().parents[1] / "results" / "10_report_action_model_comparison.csv"


def main():
    world = BinaryWorld()
    generator = PCCParameters(pressure=1.5, control=0.6, chaos=0.10)
    sim = simulate_binary_learning(steps=80, world=world, pcc=generator, seed=31)

    reports = simulate_reported_beliefs(sim["beliefs"], sigma_logit=0.15, seed=32)
    actions = simulate_actions(sim["beliefs"], beta=2.0, seed=33)

    grids = {
        "leak": (0.4, 0.6, 0.8, 1.0),
        "anchor_strength": (0.0, 0.1, 0.25, 0.5),
        "pressure": (0.75, 1.0, 1.25, 1.5),
        "control": (0.4, 0.6, 0.8, 1.0),
    }
    conditions = {
        "reports": {"reports": reports},
        "actions": {"actions": actions},
        "reports+actions": {"reports": reports, "actions": actions},
    }

    rows_out = []
    for condition, observed in conditions.items():
        rows = compare_update_models(
            sim["observations"],
            world,
            grids=grids,
            report_sigma_logit=0.15,
            action_beta=2.0,
            **observed,
        )
        for rank, row in enumerate(rows, start=1):
            rows_out.append({
                "condition": condition,
                "rank": rank,
                "model": row["model"],
                "posterior_model_probability": row["posterior_model_probability"],
                "log_evidence": row["log_evidence"],
                "best_loglik": row["best_loglik"],
                "best_params": repr(row["best_params"]),
                "grid_points": row["grid_points"],
            })

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows_out[0].keys())
        writer.writeheader()
        writer.writerows(rows_out)

    for condition in conditions:
        print(f"\n{condition}")
        for row in [r for r in rows_out if r["condition"] == condition]:
            print(
                f"{row['rank']}. {row['model']}: "
                f"P(model|data)={row['posterior_model_probability']:.6f}, "
                f"best={row['best_params']}"
            )
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()

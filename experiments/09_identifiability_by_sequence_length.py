"""v0.2: recovery error and posterior concentration as sequence length grows."""
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt

from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.latent_inference import infer_latent_pcc_grid, posterior_summary

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

world = BinaryWorld()
truth = PCCParameters(1.5, 1.2, 0.15)
pressure_grid = (truth.pressure,)
control_grid = (truth.control,)
chaos_grid = (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)
lengths = (20, 40, 80, 160)
seeds = tuple(range(20))
condition_names = ("raw+received+beliefs", "received+beliefs", "beliefs-only")

records = []
for steps in lengths:
    for seed in seeds:
        sim = simulate_binary_learning(steps=steps, world=world, pcc=truth, seed=seed)
        extras = {
            "raw+received+beliefs": dict(
                observations=sim["observations"], raw_observations=sim["raw_observations"]
            ),
            "received+beliefs": dict(observations=sim["observations"]),
            "beliefs-only": dict(),
        }
        for condition in condition_names:
            rows = infer_latent_pcc_grid(
                sim["beliefs"], world, pressure_grid, control_grid, chaos_grid,
                true_hypotheses=sim["true_hypotheses"], sigma_logit=0.03,
                **extras[condition],
            )
            s = posterior_summary(rows)
            records.append({
                "steps": steps,
                "seed": seed,
                "condition": condition,
                "map_pressure": s["map"]["pressure"],
                "map_control": s["map"]["control"],
                "map_chaos": s["map"]["chaos"],
                "mean_pressure": s["mean"]["pressure"],
                "mean_control": s["mean"]["control"],
                "mean_chaos": s["mean"]["chaos"],
                "effective_grid_points": s["effective_grid_points"],
                "flip_rate": float((sim["observations"] != sim["raw_observations"]).mean()),
            })

with (OUT / "09_identifiability_by_sequence_length.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

summary_rows = []
for steps in lengths:
    for condition in condition_names:
        subset = [r for r in records if r["steps"] == steps and r["condition"] == condition]
        row = {"steps": steps, "condition": condition}
        for parameter, true_value in (
            ("pressure", truth.pressure), ("control", truth.control), ("chaos", truth.chaos)
        ):
            estimates = np.asarray([r[f"mean_{parameter}"] for r in subset])
            row[f"rmse_{parameter}"] = float(np.sqrt(np.mean((estimates - true_value) ** 2)))
            row[f"bias_{parameter}"] = float(np.mean(estimates - true_value))
        row["mean_effective_grid_points"] = float(
            np.mean([r["effective_grid_points"] for r in subset])
        )
        summary_rows.append(row)

with (OUT / "09_identifiability_summary.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
    writer.writeheader()
    writer.writerows(summary_rows)

fig, ax = plt.subplots(figsize=(7.5, 4.5))
for condition in condition_names:
    subset = [r for r in summary_rows if r["condition"] == condition]
    ax.plot(
        [r["steps"] for r in subset], [r["rmse_chaos"] for r in subset],
        marker="o", label=condition,
    )
ax.set_xscale("log", base=2)
ax.set_xlabel("sequence length")
ax.set_ylabel("Chaos posterior-mean RMSE")
ax.set_title("Chaos identifiability improves unevenly with observation access")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "09_identifiability_by_sequence_length.png", dpi=180)

for row in summary_rows:
    print(row)

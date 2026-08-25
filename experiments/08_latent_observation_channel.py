"""v0.2: compare PCC parameter inference under progressively hidden evidence."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt

from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.latent_inference import (
    infer_latent_pcc_grid, posterior_summary, posterior_marginal,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)

world = BinaryWorld()
truth = PCCParameters(pressure=1.5, control=1.2, chaos=0.15)
sim = simulate_binary_learning(steps=120, world=world, pcc=truth, seed=21)

pressure_grid = (1.0, 1.25, 1.5, 1.75, 2.0)
control_grid = (0.9, 1.0, 1.1, 1.2, 1.3)
chaos_grid = (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)

conditions = {
    "raw+received+beliefs": dict(
        observations=sim["observations"], raw_observations=sim["raw_observations"]
    ),
    "received+beliefs": dict(observations=sim["observations"]),
    "beliefs-only": dict(),
}

all_rows = []
posteriors = {}
for name, extra in conditions.items():
    rows = infer_latent_pcc_grid(
        sim["beliefs"], world, pressure_grid, control_grid, chaos_grid,
        true_hypotheses=sim["true_hypotheses"], sigma_logit=0.03, **extra,
    )
    posteriors[name] = rows
    summary = posterior_summary(rows)
    all_rows.append({
        "condition": name,
        "map_pressure": summary["map"]["pressure"],
        "map_control": summary["map"]["control"],
        "map_chaos": summary["map"]["chaos"],
        "mean_pressure": summary["mean"]["pressure"],
        "mean_control": summary["mean"]["control"],
        "mean_chaos": summary["mean"]["chaos"],
        "map_posterior": summary["map_posterior"],
        "effective_grid_points": summary["effective_grid_points"],
    })

with (OUT / "08_latent_observation_channel.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
for ax, parameter, true_value in zip(
    axes, ("pressure", "control", "chaos"),
    (truth.pressure, truth.control, truth.chaos),
):
    for name, rows in posteriors.items():
        marginal = posterior_marginal(rows, parameter)
        ax.plot(list(marginal.keys()), list(marginal.values()), marker="o", label=name)
    ax.axvline(true_value, linestyle="--", linewidth=1)
    ax.set_title(parameter.capitalize())
    ax.set_xlabel("grid value")
    ax.set_ylabel("posterior mass")
axes[0].legend(fontsize=8)
fig.suptitle("Parameter identifiability under progressively hidden evidence")
fig.tight_layout()
fig.savefig(OUT / "08_latent_observation_channel.png", dpi=180)

print("true:", truth)
print("realized flip rate:", (sim["observations"] != sim["raw_observations"]).mean())
for row in all_rows:
    print(row)

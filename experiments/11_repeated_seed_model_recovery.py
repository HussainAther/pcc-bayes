from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from pcc_bayes.model_comparison import _logsumexp, _parameter_grid
from pcc_bayes.reporting import (
    action_loglik,
    report_loglik,
    simulate_actions,
    simulate_reported_beliefs,
)
from pcc_bayes.simulation import BinaryWorld
from pcc_bayes.update_models import replay_update_model


ROOT = Path(__file__).resolve().parents[1]
TRIALS_OUT = ROOT / "results" / "11_model_recovery_trials.csv"
SUMMARY_OUT = ROOT / "results" / "11_model_recovery_summary.csv"
CONFUSION_OUT = ROOT / "results" / "11_model_recovery_confusion.csv"

GENERATORS = {
    "bayes": {},
    "leaky_bayes": {"leak": 0.60},
    "anchored_bayes": {"anchor_strength": 0.25},
    "pcc": {"pressure": 1.50, "control": 0.60},
}

GRIDS = {
    "leak": (0.40, 0.60, 0.80, 1.00),
    "anchor_strength": (0.00, 0.10, 0.25, 0.50),
    "pressure": (0.75, 1.00, 1.25, 1.50),
    "control": (0.40, 0.60, 0.80, 1.00),
}

MODEL_ORDER = ("bayes", "leaky_bayes", "anchored_bayes", "pcc")


def sample_observations(world: BinaryWorld, steps: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.asarray([world.sample(rng) for _ in range(steps)], dtype=int)


def params_match(model: str, inferred: dict, true_params: dict) -> bool:
    if model == "bayes":
        return True
    if set(inferred) != set(true_params):
        return False
    return all(np.isclose(inferred[k], true_params[k]) for k in true_params)


def compare_all_channels(observations, world, reports, actions, sigma, beta):
    by_condition = {"reports": [], "actions": [], "reports+actions": []}
    for model in MODEL_ORDER:
        candidates = []
        for params in _parameter_grid(model, GRIDS):
            beliefs = replay_update_model(observations, world, model, **params)
            ll_reports = report_loglik(reports, beliefs, sigma_logit=sigma)
            ll_actions = action_loglik(actions, beliefs, beta=beta)
            candidates.append((params, ll_reports, ll_actions))

        for condition, idxs in {
            "reports": (1,),
            "actions": (2,),
            "reports+actions": (1, 2),
        }.items():
            vals = [sum(candidate[i] for i in idxs) for candidate in candidates]
            log_evidence = _logsumexp(vals) - np.log(len(vals))
            best_idx = int(np.argmax(vals))
            by_condition[condition].append({
                "model": model,
                "log_evidence": float(log_evidence),
                "best_loglik": float(vals[best_idx]),
                "best_params": dict(candidates[best_idx][0]),
            })

    for rows in by_condition.values():
        normalizer = _logsumexp([row["log_evidence"] for row in rows])
        for row in rows:
            row["posterior_model_probability"] = float(
                np.exp(row["log_evidence"] - normalizer)
            )
        rows.sort(key=lambda row: row["posterior_model_probability"], reverse=True)
    return by_condition


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-seeds", type=int, default=100)
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()

    world = BinaryWorld()
    steps = 80
    sigma = 0.25
    beta = 2.0
    seeds = range(args.n_seeds)

    trials_out = TRIALS_OUT
    summary_out = SUMMARY_OUT
    confusion_out = CONFUSION_OUT
    if args.pilot:
        trials_out = ROOT / "results" / "11_model_recovery_pilot_trials.csv"
        summary_out = ROOT / "results" / "11_model_recovery_pilot_summary.csv"
        confusion_out = ROOT / "results" / "11_model_recovery_pilot_confusion.csv"

    trial_rows = []
    confusion = defaultdict(Counter)

    for true_model, true_params in GENERATORS.items():
        for seed in seeds:
            observations = sample_observations(world, steps, seed)
            beliefs = replay_update_model(
                observations,
                world,
                true_model,
                **true_params,
            )
            reports = simulate_reported_beliefs(
                beliefs, sigma_logit=sigma, seed=10_000 + seed
            )
            actions = simulate_actions(
                beliefs, beta=beta, seed=20_000 + seed
            )

            conditions = compare_all_channels(
                observations, world, reports, actions, sigma, beta
            )

            for condition, rows in conditions.items():
                winner = rows[0]
                true_row = next(row for row in rows if row["model"] == true_model)
                recovered = winner["model"] == true_model
                exact_params = recovered and params_match(
                    true_model, winner["best_params"], true_params
                )
                confusion[(condition, true_model)][winner["model"]] += 1
                trial_rows.append({
                    "condition": condition,
                    "true_model": true_model,
                    "seed": seed,
                    "inferred_model": winner["model"],
                    "recovered": int(recovered),
                    "true_model_probability": true_row["posterior_model_probability"],
                    "winner_probability": winner["posterior_model_probability"],
                    "best_params": repr(winner["best_params"]),
                    "exact_true_params_if_recovered": int(exact_params),
                })

    trials_out.parent.mkdir(exist_ok=True)
    with trials_out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=trial_rows[0].keys())
        writer.writeheader()
        writer.writerows(trial_rows)

    summary_rows = []
    for condition in ("reports", "actions", "reports+actions"):
        for true_model in MODEL_ORDER:
            rows = [
                row for row in trial_rows
                if row["condition"] == condition and row["true_model"] == true_model
            ]
            recovered = np.asarray([row["recovered"] for row in rows], dtype=float)
            probs = np.asarray(
                [row["true_model_probability"] for row in rows], dtype=float
            )
            exact = np.asarray(
                [row["exact_true_params_if_recovered"] for row in rows], dtype=float
            )
            n_recovered = int(recovered.sum())
            summary_rows.append({
                "condition": condition,
                "true_model": true_model,
                "n": len(rows),
                "top1_recovery_rate": float(recovered.mean()),
                "mean_true_model_probability": float(probs.mean()),
                "exact_parameter_recovery_rate_all_trials": float(exact.mean()),
                "exact_parameter_recovery_rate_given_model_recovered": (
                    float(exact.sum() / n_recovered) if n_recovered else float("nan")
                ),
            })

    with summary_out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    confusion_rows = []
    for condition in ("reports", "actions", "reports+actions"):
        for true_model in MODEL_ORDER:
            counts = confusion[(condition, true_model)]
            for inferred_model in MODEL_ORDER:
                confusion_rows.append({
                    "condition": condition,
                    "true_model": true_model,
                    "inferred_model": inferred_model,
                    "count": counts[inferred_model],
                    "rate": counts[inferred_model] / float(args.n_seeds),
                })

    with confusion_out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=confusion_rows[0].keys())
        writer.writeheader()
        writer.writerows(confusion_rows)

    label = "PILOT" if args.pilot else "CONFIRMATORY"
    print(f"{label} repeated-seed model recovery ({args.n_seeds} seeds, T=80)")
    for condition in ("reports", "actions", "reports+actions"):
        print(f"\n{condition}")
        for row in [r for r in summary_rows if r["condition"] == condition]:
            print(
                f"  true={row['true_model']:<15} "
                f"top1={row['top1_recovery_rate']:.3f} "
                f"mean_Ptrue={row['mean_true_model_probability']:.3f} "
                f"exact_params={row['exact_parameter_recovery_rate_all_trials']:.3f}"
            )
        pcc_counts = confusion[(condition, "pcc")]
        print("  PCC winner counts:", dict(pcc_counts))

    print(f"\nwrote {trials_out}")
    print(f"wrote {summary_out}")
    print(f"wrote {confusion_out}")


if __name__ == "__main__":
    main()

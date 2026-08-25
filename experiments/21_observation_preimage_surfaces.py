from __future__ import annotations

import csv
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from pcc_bayes.affordance_geometry import classify_topset_supports
from pcc_bayes.affordance_preimage import affine_affordance_boundary
from pcc_bayes.multiclass_chaos import ThreeStateTrackingConfig, filter_three_state_markov, generate_three_state_episode

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "results" / "20_affordance_transition_dynamics.csv"
OUT = ROOT / "results" / "21_observation_preimage_validation.csv"
SURFACES = ROOT / "results" / "21_observation_preimage_surfaces.csv"
OBSERVATION_ACCURACIES = (0.45, 0.55, 0.65, 0.80)
SWITCH_PROBABILITIES = (0.03, 0.10, 0.30)
EVALUATION_SEEDS = tuple(range(1000, 1100))
DELTA = 0.15
TOL = 1e-12
BOUNDARY_TOL = 1e-15


def load_historical():
    with HISTORICAL.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return {(float(r["observation_accuracy"]), float(r["switch_probability"])): r for r in rows}


def transition_matrix(before, after):
    m = np.zeros((3, 3), dtype=int)
    np.add.at(m, (before - 1, after - 1), 1)
    return m


def vectorized_preimage(priors, observations, s, a):
    kappa = 1.0 - 1.5 * s
    predicted = kappa * priors + 0.5 * s
    miss = (1.0 - a) / 2.0
    likelihoods = np.full_like(predicted, miss)
    likelihoods[np.arange(len(observations)), observations] = a
    scores = predicted * likelihoods
    z = scores.sum(axis=1)
    top = np.argmax(scores, axis=1)
    top_scores = scores[np.arange(len(scores)), top]
    live = (top_scores[:, None] - scores) <= (DELTA * z[:, None] + BOUNDARY_TOL)
    classes = live.sum(axis=1).astype(int)
    posterior = scores / z[:, None]
    return classes, scores, z, posterior


def run_cell(args):
    s, a, historical = args
    priors_all = []
    obs_all = []
    posts_all = []
    before_classes_all = []
    after_classes_all = []
    config = ThreeStateTrackingConfig(steps=400, switch_probability=s, observation_accuracy=a)
    for seed in EVALUATION_SEEDS:
        _, observations = generate_three_state_episode(config, seed)
        impl = filter_three_state_markov(observations, switch_probability=s, observation_accuracy=a)
        priors = np.vstack([np.full((1, 3), 1.0 / 3.0), impl[:-1]])
        priors_all.append(priors)
        obs_all.append(observations)
        posts_all.append(impl)
        before_classes_all.append(classify_topset_supports(priors, utility_gap=0.30))
        after_classes_all.append(classify_topset_supports(impl, utility_gap=0.30))

    priors = np.vstack(priors_all)
    observations = np.concatenate(obs_all).astype(int)
    implemented_posts = np.vstack(posts_all)
    before_classes = np.concatenate(before_classes_all)
    implemented_after = np.concatenate(after_classes_all)

    preimage_classes, scores, z, preimage_posts = vectorized_preimage(priors, observations, s, a)
    class_mismatches = int(np.sum(preimage_classes != implemented_after))
    posterior_error = float(np.max(np.abs(preimage_posts - implemented_posts)))

    max_boundary_identity_residual = 0.0
    max_affine_score_residual = 0.0
    for y in range(3):
        mask = observations == y
        p = priors[mask]
        if not np.any(mask):
            continue
        score_y = scores[mask]
        z_y = z[mask]
        post_y = implemented_posts[mask]
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                boundary = affine_affordance_boundary(y, i, j, s, a, DELTA)
                affine_value = p @ boundary.coefficients + boundary.intercept
                score_value = score_y[:, i] - score_y[:, j] - DELTA * z_y
                normalized_value = z_y * (post_y[:, i] - post_y[:, j] - DELTA)
                max_affine_score_residual = max(
                    max_affine_score_residual,
                    float(np.max(np.abs(affine_value - score_value))),
                )
                max_boundary_identity_residual = max(
                    max_boundary_identity_residual,
                    float(np.max(np.abs(affine_value - normalized_value))),
                )

    preimage_matrix = transition_matrix(before_classes, preimage_classes)
    hist = historical[(a, s)]
    historical_matrix = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            historical_matrix[i, j] = int(hist[f"transition_{i+1}_to_{j+1}"])

    observation_count_match = True
    obs_counts = {}
    for y in range(3):
        mask = observations == y
        for cls in range(1, 4):
            predicted_count = int(np.sum(preimage_classes[mask] == cls))
            implemented_count = int(np.sum(implemented_after[mask] == cls))
            obs_counts[f"obs{y}_class{cls}_count"] = predicted_count
            obs_counts[f"implemented_obs{y}_class{cls}_count"] = implemented_count
            observation_count_match &= predicted_count == implemented_count

    row = {
        "observation_accuracy": a,
        "switch_probability": s,
        "updates": len(observations),
        "max_posterior_error": posterior_error,
        "max_boundary_identity_residual": max_boundary_identity_residual,
        "max_affine_score_residual": max_affine_score_residual,
        "class_mismatch_count": class_mismatches,
    }
    row.update(obs_counts)
    for i in range(3):
        for j in range(3):
            row[f"transition_{i+1}_to_{j+1}"] = int(preimage_matrix[i, j])
            row[f"historical_transition_{i+1}_to_{j+1}"] = int(historical_matrix[i, j])
    row.update({
        "gate_boundary_identity": max_boundary_identity_residual <= TOL,
        "gate_affine_score_identity": max_affine_score_residual <= TOL,
        "gate_zero_class_mismatch": class_mismatches == 0,
        "gate_transition_matrix_match": bool(np.array_equal(preimage_matrix, historical_matrix)),
        "gate_observation_specific_counts": bool(observation_count_match),
    })
    row["cell_pass"] = all(v for k, v in row.items() if k.startswith("gate_"))
    return row


def surface_rows():
    rows = []
    for s in SWITCH_PROBABILITIES:
        for a in OBSERVATION_ACCURACIES:
            for y in range(3):
                for i in range(3):
                    for j in range(3):
                        if i == j:
                            continue
                        boundary = affine_affordance_boundary(y, i, j, s, a, DELTA)
                        rows.append({
                            "observation_accuracy": a,
                            "switch_probability": s,
                            "observation": y,
                            "top_action": i,
                            "comparison_action": j,
                            "coefficient_p0": float(boundary.coefficients[0]),
                            "coefficient_p1": float(boundary.coefficients[1]),
                            "coefficient_p2": float(boundary.coefficients[2]),
                            "intercept": float(boundary.intercept),
                            "delta": DELTA,
                        })
    return rows


def main():
    historical = load_historical()
    args = [(s, a, historical) for s in SWITCH_PROBABILITIES for a in OBSERVATION_ACCURACIES]
    with Pool(processes=12) as pool:
        rows = pool.map(run_cell, args)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    surfaces = surface_rows()
    with SURFACES.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=surfaces[0].keys())
        writer.writeheader()
        writer.writerows(surfaces)

    total_updates = sum(int(r["updates"]) for r in rows)
    total_mismatches = sum(int(r["class_mismatch_count"]) for r in rows)
    max_boundary = max(float(r["max_boundary_identity_residual"]) for r in rows)
    max_affine = max(float(r["max_affine_score_residual"]) for r in rows)
    max_post = max(float(r["max_posterior_error"]) for r in rows)
    print(f"tested updates: {total_updates}")
    print(f"generated affine surfaces: {len(surfaces)}")
    print(f"max posterior error: {max_post:.3e}")
    print(f"max affine-score residual: {max_affine:.3e}")
    print(f"max boundary identity residual: {max_boundary:.3e}")
    print(f"preimage class mismatches: {total_mismatches}")
    for r in rows:
        print(
            f"obs_acc={r['observation_accuracy']:.2f} switch={r['switch_probability']:.2f} "
            f"mismatch={r['class_mismatch_count']} boundary={r['max_boundary_identity_residual']:.2e} "
            f"{'PASS' if r['cell_pass'] else 'FAIL'}"
        )
    overall = all(r["cell_pass"] for r in rows)
    print(f"\nv0.12 observation-specific preimage surfaces: {'PASS' if overall else 'FAIL'}")
    print(f"wrote {OUT}")
    print(f"wrote {SURFACES}")


if __name__ == "__main__":
    main()

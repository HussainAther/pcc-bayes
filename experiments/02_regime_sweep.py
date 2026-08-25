from pathlib import Path
import csv, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from pcc_bayes.simulation import simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.observables import belief_observables, belief_reversals, time_to_confidence

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)
rows = []
for p in (0.5, 1.0, 2.0):
    for c in (0.7, 1.0, 1.3):
        for ch in (0.0, 0.1, 0.25):
            for seed in range(10):
                sim = simulate_binary_learning(steps=150, pcc=PCCParameters(p, c, ch), seed=seed)
                b = sim["beliefs"]
                o = belief_observables(b)
                rows.append({
                    "pressure": p, "control": c, "chaos": ch, "seed": seed,
                    "final_true_prob": b[-1, 1],
                    "final_entropy": o["entropy"][-1],
                    "mean_revision_js": np.mean(o["revision_js"][1:]),
                    "cumulative_revision": o["cumulative_revision"][-1],
                    "reversals": belief_reversals(b),
                    "time_to_confidence": time_to_confidence(b) or -1,
                })

path = OUT / "02_regime_sweep.csv"
with path.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print("saved", path, "rows=", len(rows))

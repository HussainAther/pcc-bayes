from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import matplotlib.pyplot as plt
from pcc_bayes.geometry import exact_binary_kl, fisher_quadratic_approx_binary

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

p0 = 0.5
deltas = np.logspace(-6, -1, 80)
exact = np.array([exact_binary_kl(p0, p0+d) for d in deltas])
approx = np.array([fisher_quadratic_approx_binary(p0, p0+d) for d in deltas])
rel = np.abs(exact - approx) / exact

plt.figure(figsize=(7,4))
plt.loglog(deltas, rel)
plt.xlabel("perturbation |delta|")
plt.ylabel("relative KL approximation error")
plt.tight_layout()
plt.savefig(OUT / "05_information_geometry.png", dpi=160)
print("smallest-delta relative error:", rel[0])
print("saved", OUT / "05_information_geometry.png")

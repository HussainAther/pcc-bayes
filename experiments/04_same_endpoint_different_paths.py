from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import matplotlib.pyplot as plt
from pcc_bayes.observables import belief_observables, belief_reversals

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

smooth = np.linspace(0.52, 0.70, 20)
volatile = np.array([0.90,0.31,0.82,0.42,0.91,0.38,0.80,0.44,0.77,0.49,
                     0.75,0.53,0.73,0.57,0.72,0.60,0.71,0.64,0.70,0.70])
A = np.c_[1-smooth, smooth]
B = np.c_[1-volatile, volatile]
for name, hist in (("smooth", A), ("volatile", B)):
    o = belief_observables(hist)
    print(name, "endpoint=", hist[-1,1], "cum_JS=", o["cumulative_revision"][-1],
          "reversals=", belief_reversals(hist))

plt.figure(figsize=(8,4))
plt.plot(smooth, label="smooth")
plt.plot(volatile, label="volatile")
plt.ylabel("P(H1)"); plt.xlabel("step"); plt.legend(); plt.tight_layout()
plt.savefig(OUT / "04_same_endpoint_different_paths.png", dpi=160)
print("saved", OUT / "04_same_endpoint_different_paths.png")

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib.pyplot as plt
from pcc_bayes.simulation import simulate_binary_learning
from pcc_bayes.pcc import PCCParameters

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

plt.figure(figsize=(8, 4))
for c in (0.7, 1.0, 1.3):
    sim = simulate_binary_learning(steps=180, switch_step=90,
                                   pcc=PCCParameters(1.0, c, 0.05), seed=3)
    plt.plot(sim["beliefs"][:, 1], label=f"control={c}")
plt.axvline(90, linestyle="--")
plt.xlabel("update")
plt.ylabel("P(H1)")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "03_world_switch.png", dpi=160)
print("saved", OUT / "03_world_switch.png")

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib.pyplot as plt
from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.observables import belief_observables

OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

sim = simulate_binary_learning(
    steps=120,
    prior=(0.5, 0.5),
    world=BinaryWorld(0.3, 0.7, 1),
    pcc=PCCParameters(1.0, 1.0, 0.0),
    seed=7,
)
obs = belief_observables(sim["beliefs"])

plt.figure(figsize=(8, 4))
plt.plot(sim["beliefs"][:, 1], label="P(H1)")
plt.plot(obs["entropy"], label="entropy")
plt.xlabel("update")
plt.legend()
plt.tight_layout()
plt.savefig(OUT / "01_coin_learning.png", dpi=160)
print("final belief:", sim["beliefs"][-1])
print("saved", OUT / "01_coin_learning.png")

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pcc_bayes.simulation import simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.meta_inference import infer_pcc_grid

truth = PCCParameters(1.5, 1.0, 0.1)
observed = simulate_binary_learning(steps=80, pcc=truth, seed=11)["beliefs"]
rows = infer_pcc_grid(
    observed,
    pressure_grid=(0.5, 1.0, 1.5, 2.0),
    control_grid=(0.8, 1.0, 1.2),
    chaos_grid=(0.0, 0.1, 0.2),
    simulator_kwargs={"steps": 80},
    seeds=(9,10,11,12,13),
)
rows = sorted(rows, key=lambda r: r["weight"], reverse=True)
print("true parameters:", truth)
print("top latent-channel simulation matches:")
for r in rows[:8]:
    print(r)
print("This baseline is intentionally retained as an identifiability stress test.")

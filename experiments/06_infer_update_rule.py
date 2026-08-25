from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pcc_bayes.simulation import BinaryWorld, simulate_binary_learning
from pcc_bayes.pcc import PCCParameters
from pcc_bayes.meta_inference import infer_pressure_control_grid

world = BinaryWorld(0.3, 0.7, 1)
truth = PCCParameters(1.5, 1.2, 0.1)
sim = simulate_binary_learning(steps=80, world=world, pcc=truth, seed=11)
rows = infer_pressure_control_grid(
    sim["beliefs"], sim["observations"], world,
    pressure_grid=(0.5, 1.0, 1.5, 2.0),
    control_grid=(0.8, 1.0, 1.2, 1.4),
)
rows = sorted(rows, key=lambda r: r["weight"], reverse=True)
print("true pressure/control:", truth.pressure, truth.control)
print("top candidates conditional on realized observations:")
for r in rows[:8]:
    print(r)
print("note: chaos is not inferred here because the realized evidence is conditioned upon")

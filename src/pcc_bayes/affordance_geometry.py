from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TopsetAffordanceGeometry:
    """Exact posterior-simplex geometry for the frozen utility-topset policy."""

    utility_gap: float = 0.30

    def __post_init__(self):
        if self.utility_gap <= 0.0:
            raise ValueError("utility_gap must be positive")

    @property
    def posterior_gap(self) -> float:
        # u_i = 2 p_i - 1, hence utility difference = 2 * posterior difference.
        return self.utility_gap / 2.0

    def ordered_probabilities(self, belief) -> np.ndarray:
        p = np.asarray(belief, dtype=float)
        if p.shape != (3,):
            raise ValueError("belief must have shape (3,)")
        if np.any(p < 0.0) or not np.isclose(float(np.sum(p)), 1.0):
            raise ValueError("belief must be nonnegative and sum to one")
        return np.sort(p)[::-1]

    def margins(self, belief) -> tuple[float, float]:
        p1, p2, p3 = self.ordered_probabilities(belief)
        return float(p1 - p2), float(p1 - p3)

    def support_size(self, belief) -> int:
        gap12, gap13 = self.margins(belief)
        delta = self.posterior_gap
        tol = 1e-15
        if gap12 > delta + tol:
            return 1
        if gap13 > delta + tol:
            return 2
        return 3

    def region(self, belief) -> str:
        return {1: "one_action", 2: "two_action", 3: "three_action"}[self.support_size(belief)]


def classify_topset_supports(beliefs, utility_gap: float = 0.30) -> np.ndarray:
    geometry = TopsetAffordanceGeometry(utility_gap=utility_gap)
    beliefs = np.asarray(beliefs, dtype=float)
    if beliefs.ndim != 2 or beliefs.shape[1] != 3:
        raise ValueError("beliefs must have shape (n, 3)")
    ordered = np.sort(beliefs, axis=1)[:, ::-1]
    gap12 = ordered[:, 0] - ordered[:, 1]
    gap13 = ordered[:, 0] - ordered[:, 2]
    delta = geometry.posterior_gap
    out = np.full(len(beliefs), 3, dtype=int)
    tol = 1e-15
    out[gap13 > delta + tol] = 2
    out[gap12 > delta + tol] = 1
    return out


def support_fraction_summary(support_sizes) -> dict[str, float]:
    support = np.asarray(support_sizes, dtype=int)
    if support.ndim != 1 or np.any((support < 1) | (support > 3)):
        raise ValueError("support_sizes must be a one-dimensional array in {1,2,3}")
    return {
        "one_action_fraction": float(np.mean(support == 1)),
        "two_action_fraction": float(np.mean(support == 2)),
        "three_action_fraction": float(np.mean(support == 3)),
        "branch_fraction": float(np.mean(support >= 2)),
    }

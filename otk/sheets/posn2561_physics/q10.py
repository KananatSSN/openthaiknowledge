"""MC10 figure: uniform door weight90N,width1m, hinges1.5m apart, upper reaction magnitude50N. Torque fixes horizontal reaction30N; upper vertical can be +40 or -40. Source assumes +40, giving bottom sqrt3400N (~58N); -40 gives sqrt17800N. Adaptation explicitly requires upward vertical support from BOTH hinges. solve returns positive-upward branch."""

from math import sqrt, hypot


def solve(weight=90, width=1, separation=1.5, upper=50):
    horizontal = weight * width / (2 * separation)
    vertical = sqrt(upper**2 - horizontal**2)
    if not 0 < vertical < weight:
        raise ValueError("both hinges must support upward")
    return hypot(horizontal, weight - vertical)


def check(weight=90, width=1, separation=1.5, upper=50):
    # Search lower vertical reaction from the upper magnitude constraint.
    horizontal = weight * (width / 2) / separation
    lo, hi = 0.0, float(weight)
    for _ in range(100):
        lower_vertical = (lo + hi) / 2
        upper_squared = horizontal**2 + (weight - lower_vertical) ** 2
        if upper_squared > upper**2:
            lo = lower_vertical
        else:
            hi = lower_vertical
    return hypot(horizontal, (lo + hi) / 2)


PARAMS = {"weight": 90, "width": 1, "separation": 1.5, "upper": 50}
VARIANTS = [{"weight": 180, "upper": 100}, {"width": 0.5}, {"upper": 60}]
ANSWER = 58.309518948453004

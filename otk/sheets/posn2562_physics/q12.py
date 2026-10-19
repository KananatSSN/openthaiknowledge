"""MC12 figure: symmetric heavy rope of totalweight W between equal-height supports. At supports theta is measured from VERTICAL. Lowest-point tension is horizontal W tan(theta)/2, source answer3. Flexible rope; no horizontal distributed load."""

from math import tan, radians, atan2


def solve(weight=100, theta=30):
    return weight * tan(radians(theta)) / 2


def check(weight=100, theta=30):
    # Build half-rope vertical tensions by accumulating discrete weights.
    lo, hi = 0.0, 10 * weight
    for _ in range(100):
        horizontal = (lo + hi) / 2
        vertical = 0.0
        for _ in range(100):
            vertical += weight / 200
        angle_to_vertical = atan2(horizontal, vertical)
        if angle_to_vertical < radians(theta):
            lo = horizontal
        else:
            hi = horizontal
    return (lo + hi) / 2


PARAMS = {"weight": 100, "theta": 30}
VARIANTS = [{"weight": 200}, {"theta": 45}, {"theta": 60}]
ANSWER = 28.867513459481287

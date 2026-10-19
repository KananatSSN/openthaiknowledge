"""MC16: equal free-surface height. Heavy bottom1100kg/m³, left900kg/m³ depthB12cm, right800kg/m³ depthA8cm. Figure A<B identifies which unlabeled light fluid is on each side. Adaptation explicitly labels them."""

from fractions import Fraction


def solve(left=900, right=800, heavy=1100, height_b=12):
    return Fraction(height_b * (heavy - left), heavy - right)


def check(left=900, right=800, heavy=1100, height_b=12):
    depth = height_b + 1
    pressure_left = left * height_b + heavy * (depth - height_b)
    lo, hi = 0.0, float(height_b)
    for _ in range(100):
        height_a = (lo + hi) / 2
        pressure_right = right * height_a + heavy * (depth - height_a)
        if pressure_right > pressure_left:
            lo = height_a
        else:
            hi = height_a
    return (lo + hi) / 2


PARAMS = {"left": 900, "right": 800, "heavy": 1100, "height_b": 12}
VARIANTS = [{"height_b": 18}, {"left": 1000}, {"right": 700}]
ANSWER = Fraction(8, 1)

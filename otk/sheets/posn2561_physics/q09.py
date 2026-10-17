"""MC9: conical pendulums share support, mA/mB2, LB/LA1.5, periodA/periodB2. TA/TB=(mA/mB)(LA/LB)(periodB/periodA)²=1/3. These ratios are physically feasible; unequal cone angles are essential."""

from fractions import Fraction
from math import pi, sqrt


def solve(mass_ratio=2, len_a=2, len_b=3, period_ratio=2):
    return Fraction(mass_ratio * len_a, len_b * period_ratio**2)


def check(mass_ratio=2, len_a=2, len_b=3, period_ratio=2):
    # Construct actual equilibria with g1 and mB1, then vertical force balance.
    cos_b = min(0.25, 0.5 * len_a / (period_ratio**2 * len_b))
    period_b = 2 * pi * sqrt(len_b * cos_b)
    period_a = period_b * period_ratio
    cos_a = period_a**2 / (4 * pi * pi * len_a)
    assert 0 < cos_a < 1 and 0 < cos_b < 1
    tension_a = mass_ratio / cos_a
    tension_b = 1 / cos_b
    return tension_a / tension_b


PARAMS = {"mass_ratio": 2, "len_a": 2, "len_b": 3, "period_ratio": 2}
VARIANTS = [{"mass_ratio": 3}, {"len_b": 4}, {"period_ratio": 3}]
ANSWER = Fraction(1, 3)

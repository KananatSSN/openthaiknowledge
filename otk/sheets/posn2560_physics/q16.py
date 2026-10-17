"""Part 1,16: first sphere above water fraction1/4 (pi a³/3); second submerged fraction2/3 (8pi b³/9). Ratio rho1/rho2=9/8, independent radii."""

from fractions import Fraction
from math import pi


def solve(above_num=1, above_den=4, sub_num=2, sub_den=3):
    return (1 - Fraction(above_num, above_den)) / Fraction(sub_num, sub_den)


def check(above_num=1, above_den=4, sub_num=2, sub_den=3):
    # Distinct actual spheres, infer mass from displaced water then density.
    v1, v2 = 4 * pi * 0.3**3 / 3, 4 * pi * 0.7**3 / 3
    m1 = 1000 * (v1 - v1 * above_num / above_den)
    m2 = 1000 * v2 * sub_num / sub_den
    return (m1 / v1) / (m2 / v2)


PARAMS = {"above_num": 1, "above_den": 4, "sub_num": 2, "sub_den": 3}
VARIANTS = [{"above_num": 1, "above_den": 3}, {"sub_num": 1, "sub_den": 2}, {"above_den": 5}]
ANSWER = Fraction(9, 8)

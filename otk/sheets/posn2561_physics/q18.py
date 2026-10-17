"""MC18 figure: two initially equal strips length20pi cm heat by80K and form concentric complete circles whose radii differ.20mm. Circumference difference=2pi delta_r gives coefficient difference2.5e-5/K. Treat ideal free linear expansions as source model."""

from fractions import Fraction
from math import pi


def solve(length_pi_cm=20, gap_mm=0.2, delta_t=80):
    return Fraction(str(gap_mm)) / (5 * length_pi_cm * delta_t)


def check(length_pi_cm=20, gap_mm=0.2, delta_t=80):
    length_mm = length_pi_cm * pi * 10
    base_alpha = 1e-5
    inner_radius = length_mm * (1 + base_alpha * delta_t) / (2 * pi)
    lo, hi = 0.0, 0.01
    for _ in range(100):
        delta_alpha = (lo + hi) / 2
        outer_radius = length_mm * (1 + (base_alpha + delta_alpha) * delta_t) / (2 * pi)
        if outer_radius - inner_radius < gap_mm:
            lo = delta_alpha
        else:
            hi = delta_alpha
    return (lo + hi) / 2


PARAMS = {"length_pi_cm": 20, "gap_mm": 0.2, "delta_t": 80}
VARIANTS = [{"gap_mm": 0.1}, {"delta_t": 40}, {"length_pi_cm": 10}]
ANSWER = Fraction(1, 40000)

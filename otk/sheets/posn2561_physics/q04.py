"""MC4 figure: left3kg, right2kg joined by massless spring scale. BOTH external forces point RIGHT:5N on left,15N on right. Acceleration4m/s², scale reads tension7N, not net20N."""

from fractions import Fraction
import numpy as np


def solve(left_mass=3, right_mass=2, left_force=5, right_force=15):
    return Fraction(left_mass * right_force - right_mass * left_force, left_mass + right_mass)


def check(left_mass=3, right_mass=2, left_force=5, right_force=15):
    # Independent block-by-block force equations, unknown a,T.
    acceleration, tension = np.linalg.solve(
        [[left_mass, -1], [right_mass, 1]], [left_force, right_force]
    )
    assert tension > 0 and acceleration > 0
    return float(tension)


PARAMS = {"left_mass": 3, "right_mass": 2, "left_force": 5, "right_force": 15}
VARIANTS = [{"left_force": 2}, {"right_force": 25}, {"left_mass": 4}]
ANSWER = Fraction(7, 1)

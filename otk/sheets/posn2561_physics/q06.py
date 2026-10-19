"""MC6: one-dimensional elastic neutron collision with initially stationary deuteron of mass ratio2. Neutron KE fraction1/9. Generalize positive target/projectile mass ratio."""

from fractions import Fraction
import numpy as np


def solve(ratio=2):
    return Fraction((1 - ratio) ** 2, (1 + ratio) ** 2)


def check(ratio=2):
    # Set initial projectile mass and speed to1; eliminate target velocity
    # by momentum and independently solve quadratic energy conservation.
    roots = np.roots([ratio + 1, -2, 1 - ratio])
    velocity = next(float(v) for v in roots if abs(v - 1) > 1e-8)
    target_velocity = (1 - velocity) / ratio
    assert abs(velocity + ratio * target_velocity - 1) < 1e-9
    assert abs(velocity**2 + ratio * target_velocity**2 - 1) < 1e-9
    return velocity**2


PARAMS = {"ratio": 2}
VARIANTS = [{"ratio": 3}, {"ratio": 4}, {"ratio": 1}]
ANSWER = Fraction(1, 9)

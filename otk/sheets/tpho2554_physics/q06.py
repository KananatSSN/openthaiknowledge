"""Theory 2.1 figure: m2 is tied at the midpoint of a string of length L, m1 at its end on the far side of the axis; the centre of mass is x = (L/2) sin(alpha) - (m1/(m1 + m2))(L/2) sin(beta) from the axis. Adapted: masses, L and the angles (degrees) vary; metres."""

from math import radians, sin


def solve(m1=2.0, m2=1.0, length=1.0, alpha=30.0, beta=38.3):
    return length / 2 * sin(radians(alpha)) - m1 / (m1 + m2) * length / 2 * sin(radians(beta))


def check(m1=2.0, m2=1.0, length=1.0, alpha=30.0, beta=38.3):
    # Signed horizontal positions of the two masses, then their weighted mean.
    x2 = length / 2 * sin(radians(alpha))
    x1 = x2 - length / 2 * sin(radians(beta))
    return (m1 * x1 + m2 * x2) / (m1 + m2)


PARAMS = {"m1": 2.0, "m2": 1.0, "length": 1.0, "alpha": 30.0, "beta": 38.3}
VARIANTS = [{"m1": 3.0, "beta": 35.5}, {"length": 1.6, "alpha": 20.0, "beta": 24.9}, {"m2": 2.0, "beta": 48.3}]
ANSWER = 0.043406989401619966
TOL = 1e-12

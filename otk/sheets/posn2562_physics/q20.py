"""Short20 figure: forceF pullsblockM upwardatangle theta on horizontalfloor, limitingstaticfrictionmu N. Min F=mu Mg/sqrt(1+mu^2), achievedtheta=atanmu. Contactmaintained atoptimum. Generator explicitly uses staticcoefficient."""

from math import sqrt, sin, cos, pi


def solve(mass=2, g=10, mu=0.75):
    return mu * mass * g / sqrt(1 + mu * mu)


def check(mass=2, g=10, mu=0.75):
    # At each candidateangle solve horizontal limitingequilibrium and verticalN.
    def required(theta):
        force = mu * mass * g / (cos(theta) + mu * sin(theta))
        normal = mass * g - force * sin(theta)
        assert normal >= 0
        return force

    lo, hi = 0.0, pi / 2
    for _ in range(120):
        a, b = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if required(a) > required(b):
            lo = a
        else:
            hi = b
    return required((lo + hi) / 2)


PARAMS = {"mass": 2, "g": 10, "mu": 0.75}
VARIANTS = [{"mu": 0.5}, {"mass": 5}, {"mu": 1}]
ANSWER = 12.0

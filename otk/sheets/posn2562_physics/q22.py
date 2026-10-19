"""Short22 figure: spoolouterradiusR2, innerhubR1<R2, thread unwinds fromLOWERhubtangent andpulledrightupattheta. Given equations a=OmegaR2, Ma=Fcostheta-fr, I Omega=frR2-FR1 imply rightwarda iff cos(theta)>R1/R2. Returncriticalangledegrees."""

from math import acos, cos, radians, pi
import numpy as np


def solve(inner=1, outer=2):
    return acos(inner / outer) * 180 / pi


def check(inner=1, outer=2):
    # Full coupled Newton/Euler/noslip system; searchsignchange in acceleration.
    mass, force, inertia = 3.0, 2.0, 5.0
    lo, hi = 0.0, 90.0
    for _ in range(100):
        theta = (lo + hi) / 2
        acceleration, omega, friction = np.linalg.solve(
            [[1, -outer, 0], [mass, 0, 1], [0, inertia, -outer]],
            [0, force * cos(radians(theta)), -force * inner],
        )
        assert abs(acceleration - omega * outer) < 1e-10
        if acceleration > 0:
            lo = theta
        else:
            hi = theta
    return (lo + hi) / 2


PARAMS = {"inner": 1, "outer": 2}
VARIANTS = [{"inner": 1, "outer": 3}, {"inner": 2, "outer": 3}, {"inner": 3, "outer": 5}]
ANSWER = 60.00000000000001

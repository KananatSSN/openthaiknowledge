"""Short24 figure: twopendulums equallengthl, massesm<M, initiallytouchatbottom; releaseleftm, no sticking. Sourceintendedcollisioninterval pi sqrt(l/g) requiresSMALLANGLES, omittedinsource. Generator statesSHM andELASTICimpact; massesdropoutbecausebothfrequenciessame. Returntimeinseconds."""

from math import pi, sqrt, sin


def solve(length=1, g=10, light=1, heavy=2):
    return pi * sqrt(length / g)


def check(length=1, g=10, light=1, heavy=2):
    # Simulate analytic SHM trajectories after an elastic collision, then
    # find their FIRST positive meeting by bracketing the signed separation.
    frequency = sqrt(g / length)
    incoming = 1.0
    vlight = (light - heavy) / (light + heavy) * incoming
    vheavy = 2 * light / (light + heavy) * incoming
    assert vlight < 0 < vheavy

    def gap(time):
        return (vheavy - vlight) / frequency * sin(frequency * time)

    step = 0.01 / frequency
    last = step
    for i in range(2, 1000):
        time = i * step
        if gap(time) <= 0:
            break
        last = time
    else:
        raise AssertionError("no secondcollision")
    lo, hi = last, time
    for _ in range(100):
        mid = (lo + hi) / 2
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"length": 1, "g": 10, "light": 1, "heavy": 2}
VARIANTS = [{"length": 4}, {"heavy": 5}, {"light": 2, "heavy": 3}]
ANSWER = 0.9934588265796102

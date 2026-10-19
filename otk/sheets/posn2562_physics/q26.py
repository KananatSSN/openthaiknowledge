"""Worked26 figure: identicalsmoothdiscsB,C resttouching. IdenticalA approachesalongtheirperpendicularbisector withspeedu; simultaneoussymmetricelasticcollision. B,C departat±30deg toincomingdirection. A rebounds v=u/5; eachB,Cspeedw=2sqrt3u/5. Bothspeedsverified, notjustone subpart."""

from math import sqrt


def solve(speed=5):
    return speed / 5, 2 * sqrt(3) * speed / 5


def check(speed=5):
    # Independent collision impulse/restition equations with contactnormal
    # n=(sqrt3/2,±1/2), normalizedmass1, equalimpulsesJ.
    cosine = sqrt(3) / 2
    impulse = 2 * speed * cosine / (1 + 2 * cosine * cosine)
    ax = speed - 2 * impulse * cosine
    b = (impulse * cosine, impulse / 2)
    c = (impulse * cosine, -impulse / 2)
    assert abs(ax + b[0] + c[0] - speed) < 1e-9
    assert abs(ax * ax + sum(v * v for v in b) + sum(v * v for v in c) - speed * speed) < 1e-8
    assert ax < 0
    return -ax, sqrt(sum(v * v for v in b))


PARAMS = {"speed": 5}
VARIANTS = [{"speed": 10}, {"speed": 3}, {"speed": 8}]
ANSWER = (1.0, 3.4641016151377544)

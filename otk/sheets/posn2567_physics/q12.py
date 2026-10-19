"""Short12 figure: a ray enters a spherical drop at incidence i, refracts to theta, reflects once inside, and leaves. The angle between the incoming and outgoing rays is phi = 4 theta - 2 i. Degrees."""

from math import atan2, cos, degrees, radians, sin


def solve(incidence=60, refraction=40):
    return 4 * refraction - 2 * incidence


def check(incidence=60, refraction=40):
    # Rotate a direction vector through the three events: refract at entry
    # (turn by i - theta), reflect (turn by 180 - 2 theta), refract at exit
    # (turn by i - theta), all the same way; then the angle to the reversed
    # input direction.
    i, t = radians(incidence), radians(refraction)
    turn = (i - t) + (radians(180) - 2 * t) + (i - t)
    out = (cos(turn), sin(turn))
    reversed_in = (-1.0, 0.0)
    angle = atan2(out[0] * reversed_in[1] - out[1] * reversed_in[0], out[0] * reversed_in[0] + out[1] * reversed_in[1])
    return abs(degrees(angle))


PARAMS = {"incidence": 60, "refraction": 40}
VARIANTS = [{"incidence": 50, "refraction": 35}, {"incidence": 70, "refraction": 45}, {"incidence": 40, "refraction": 30}]
ANSWER = 40

"""Theory 1.2 e): a thin tube m' with a loose half cylinder m inside (frictionless contact, oscillations damped out) rolls down at a = ((m' + m)/(2m' + m)) g sin(theta): only the tube turns. Adapted: both masses (kg) and theta (degrees) vary; returns m/s^2 with g = 9.81."""

from math import radians, sin


def solve(tube=1.0, half=0.5, incline=30.0):
    return (tube + half) / (2 * tube + half) * 9.81 * sin(radians(incline))


def check(tube=1.0, half=0.5, incline=30.0, run=2.0):
    # energy: after rolling a distance l, tube K = m' v^2, half K = m v^2/2
    drop = (tube + half) * 9.81 * run * sin(radians(incline))
    speed2 = drop / (tube + half / 2)
    return speed2 / (2 * run)


PARAMS = {"tube": 1.0, "half": 0.5, "incline": 30.0}
VARIANTS = [{"half": 2.0}, {"incline": 20.0}, {"tube": 0.3}]
ANSWER = 2.9429999999999996
TOL = 1e-9

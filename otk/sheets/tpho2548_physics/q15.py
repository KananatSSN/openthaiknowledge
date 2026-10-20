"""Theory 3.4: under the tube the air turns from straight down to sideways, pushing the lower disc down with the momentum flux rho pi a^2 v0^2. Adapted: numbers; newtons."""

from math import pi


def solve(density=1.2, tube=0.01, speed=20):
    return density * pi * tube**2 * speed**2


def check(density=1.2, tube=0.01, speed=20):
    # Mass per second times the vertical velocity it loses.
    mass_rate = density * pi * tube**2 * speed
    return mass_rate * (speed - 0)


PARAMS = {"density": 1.2, "tube": 0.01, "speed": 20}
VARIANTS = [{"speed": 5}, {"tube": 0.02}, {"density": 1.0, "speed": 40}]
ANSWER = 0.15079644737231007
TOL = 1e-12

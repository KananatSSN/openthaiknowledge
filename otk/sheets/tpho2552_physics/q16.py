"""Lab 2 figure 1: a solid rod (length 2L, radius R) swinging about O, x from end A, has T = (2 pi/sqrt g) sqrt((L^2/3 + R^2/4)/(L - x) + (L - x)), so g = (4 pi^2/T^2)[(L^2/3 + R^2/4)/(L - x) + (L - x)]. Adapted: synthetic L, R, x (cm) and T (s); m/s^2."""

from math import pi, sqrt


def solve(half=40.0, radius=0.6, pivot=10.0, period=1.42):
    arm = (half - pivot) / 100
    inertia = ((half / 100) ** 2 / 3 + (radius / 100) ** 2 / 4) / arm + arm
    return 4 * pi**2 * inertia / period**2


def check(half=40.0, radius=0.6, pivot=10.0, period=1.42):
    # Bisect on g: the compound pendulum's period from I_O and M g d.
    L, R, d = half / 100, radius / 100, (half - pivot) / 100
    inertia = L * L / 3 + R * R / 4 + d * d    # per unit mass, about O

    lo, hi = 0.1, 100.0
    for _ in range(200):
        g = (lo + hi) / 2
        lo, hi = (g, hi) if 2 * pi * sqrt(inertia / (g * d)) > period else (lo, g)
    return lo


PARAMS = {"half": 40.0, "radius": 0.6, "pivot": 10.0, "period": 1.42}
VARIANTS = [{"pivot": 25.0, "period": 1.6}, {"half": 50.0, "period": 1.5}, {"radius": 1.0}]
ANSWER = 9.354837822714307
TOL = 1e-9

"""Theory 3 (a)-(c): the flux through a circle of radius r is pi r^2 B0 cos(omega t), so the emf round it is pi r^2 B0 omega sin(omega t), peaking at pi r^2 omega B0. Adapted: r (cm), B0 (T) and omega vary; returns the peak emf in mV."""

from math import pi


def solve(radius=5.0, field=0.2, omega=100.0):
    return pi * (radius * 1e-2) ** 2 * field * omega * 1e3


def check(radius=5.0, field=0.2, omega=100.0):
    # Largest -d(flux)/dt over one period, by central differences.
    from math import cos

    area = pi * (radius * 1e-2) ** 2
    period = 2 * pi / omega
    h = period * 1e-7
    best = 0.0
    for i in range(4001):
        t = period * i / 4000
        rate = -(area * field * cos(omega * (t + h)) - area * field * cos(omega * (t - h))) / (2 * h)
        best = max(best, rate)
    return best * 1e3


PARAMS = {"radius": 5.0, "field": 0.2, "omega": 100.0}
VARIANTS = [{"radius": 10.0}, {"field": 0.5, "omega": 50.0}, {"omega": 314.0}]
ANSWER = 157.0796326794897
TOL = 1e-6

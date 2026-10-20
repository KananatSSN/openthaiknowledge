"""Lab 2, part 2.1 figure 2.2: the cube hangs on two strings of length l, d apart, and twists about the vertical with T^2 = (16 pi^2 I/(m0 g d^2)) l, so I = m0 g d^2 T^2/(16 pi^2 l). Adapted: synthetic m0, d, l, T in grams, centimetres and seconds with g = 978 cm/s^2; returns I in g cm^2."""

from math import pi, sin, sqrt


def solve(mass=500, separation=4, length=30, period=0.9, g=978):
    return mass * g * separation**2 * period**2 / (16 * pi**2 * length)


def check(mass=500, separation=4, length=30, period=0.9, g=978):
    # Exact bifilar geometry: twisting by phi moves each lower end d sin(phi/2)
    # sideways and raises the cube; the torsion constant is U''(0).
    def energy(phi):
        shift = separation * sin(phi / 2)
        return mass * g * (length - sqrt(length * length - shift * shift))

    h = 1e-3
    kappa = (energy(h) - 2 * energy(0) + energy(-h)) / (h * h)
    return kappa * period**2 / (4 * pi**2)


PARAMS = {"mass": 500, "separation": 4, "length": 30, "period": 0.9, "g": 978}
VARIANTS = [{"period": 1.5}, {"separation": 6, "length": 50}, {"mass": 250}]
ANSWER = 1337.7435876297857
TOL = 1e-5

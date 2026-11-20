"""Theory 3.5: building a uniform sphere shell by shell, each shell dm meets G m(r) dm/r, which sums to P.E. = -(3/5) G M^2/R (A = 3/5); for the Sun (2.0e30 kg, 7.0e8 m) it is -2.29e41 J. Adapted: the mass (1e30 kg) and radius (1e8 m) vary; returns joules."""


def solve(mass=2.0, radius=7.0):
    from otk.sheets.tpho2562_physics._shared import G

    return -0.6 * G * (mass * 1e30) ** 2 / (radius * 1e8)


def check(mass=2.0, radius=7.0, shells=20000):
    from otk.sheets.tpho2562_physics._shared import G

    m, r = mass * 1e30, radius * 1e8
    total, dr = 0.0, r / shells
    for i in range(shells):
        x = (i + 0.5) * dr
        inside = m * (x / r) ** 3
        dm = 3 * m * x * x * dr / r**3
        total -= G * inside * dm / x
    return total


PARAMS = {"mass": 2.0, "radius": 7.0}
VARIANTS = [{"mass": 1.0}, {"radius": 3.0}, {"mass": 4.0, "radius": 10.0}]
ANSWER = -2.286857142857143e+41
TOL = 1e-6

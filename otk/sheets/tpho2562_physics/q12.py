"""Theory 3.2-3.4: two masses m circling their centre of mass at radius r obey m v^2/r = G m^2/(2r)^2, so the kinetic energy is G m^2/(4r), the potential energy -G m^2/(2r), and P.E. = -2 K.E. (b = 2). Adapted: the mass (1e30 kg) and the orbit radius (1e11 m) vary; returns the kinetic energy in joules."""


def solve(mass=1.0, radius=1.0):
    from otk.sheets.tpho2562_physics._shared import G

    m, r = mass * 1e30, radius * 1e11
    return G * m**2 / (4 * r)


def check(mass=1.0, radius=1.0):
    from math import sqrt

    from otk.sheets.tpho2562_physics._shared import G

    m, r = mass * 1e30, radius * 1e11
    potential = -G * m * m / (2 * r)
    v = sqrt(G * m / (4 * r))  # from the centripetal force
    kinetic = 2 * 0.5 * m * v**2
    assert abs(potential + 2 * kinetic) < 1e-9 * kinetic
    return kinetic


PARAMS = {"mass": 1.0, "radius": 1.0}
VARIANTS = [{"mass": 2.0}, {"radius": 0.5}, {"mass": 0.4, "radius": 3.0}]
ANSWER = 1.6675000000000001e+38
TOL = 1e-9

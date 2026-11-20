"""Theory 3.6: by the virial theorem the kinetic energy of the hydrogen cloud is half of A G M^2/R, and (3/2)(M/m_p) k_B T = (3/10) G M^2/R gives T = G M m_p/(5 R k_B) = 4.61e6 K for the Sun. Adapted: the mass (1e30 kg) and radius (1e8 m) vary; returns kelvin."""


def solve(mass=2.0, radius=7.0):
    from otk.sheets.tpho2562_physics._shared import G, K_B, M_P

    return 0.6 * G * mass * 1e30 * M_P / (3 * radius * 1e8 * K_B)


def check(mass=2.0, radius=7.0):
    from otk.sheets.tpho2562_physics import q13
    from otk.sheets.tpho2562_physics._shared import K_B, M_P

    kinetic = -q13.check(mass=mass, radius=radius) / 2
    atoms = mass * 1e30 / M_P
    return kinetic / (1.5 * atoms * K_B)


PARAMS = {"mass": 2.0, "radius": 7.0}
VARIANTS = [{"mass": 1.0}, {"radius": 3.0}, {"mass": 4.0, "radius": 10.0}]
ANSWER = 4612380.952380953
TOL = 1e-6

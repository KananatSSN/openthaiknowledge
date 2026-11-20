"""Theory 3.7: the virial theorem makes the total energy E = -K.E. = -(3/2)(M/m_p) k_B T, so dE/dT = -(3/2)(M/m_p) k_B = -2.48e34 J/K for 2.0e30 kg of hydrogen. Adapted: the mass (1e30 kg) varies; returns J/K."""


def solve(mass=2.0):
    from otk.sheets.tpho2562_physics._shared import K_B, M_P

    return -1.5 * mass * 1e30 / M_P * K_B


def check(mass=2.0, radius=7.0):
    from otk.sheets.tpho2562_physics import q14
    from otk.sheets.tpho2562_physics._shared import G

    # E = -(3/10) G M^2/R at two radii, against their virial temperatures
    def state(r):
        return -0.3 * G * (mass * 1e30) ** 2 / (r * 1e8), q14.solve(mass=mass, radius=r)

    (e1, t1), (e2, t2) = state(radius), state(radius * 1.01)
    return (e2 - e1) / (t2 - t1)


PARAMS = {"mass": 2.0}
VARIANTS = [{"mass": 1.0}, {"mass": 0.3}, {"mass": 10.0}]
ANSWER = -2.479041916167665e+34
TOL = 1e-9

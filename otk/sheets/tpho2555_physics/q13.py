"""Theory 3 (e): every proton reaches the axis after r/v_r = m u/(e E), covering u times that, while the outside field E also speeds it along the axis by (1/2)(eE/m)(mu/(eE))^2; the beam focuses at s = 3 m u^2/(2 e E) = 3 m epsilon0 u^2/(2 e sigma). Adapted: sigma (microcoulombs per square metre) and u (km/s) vary; returns s in mm."""

EPS0, E_CHARGE, M_PROTON = 8.85e-12, 1.6e-19, 1.67e-27


def solve(density=1.0, speed=100.0):
    return 3 * M_PROTON * EPS0 * (speed * 1e3) ** 2 / (2 * E_CHARGE * density * 1e-6) * 1e3


def check(density=1.0, speed=100.0, radius=0.5):
    # Leave the hole with v_r = e r E/(m u), drift inward at constant v_r
    # while the axial field accelerates the proton; time-step to the axis.
    field = density * 1e-6 / EPS0
    u = speed * 1e3
    r = radius * 1e-3
    vr = E_CHARGE * r * field / (M_PROTON * u)
    t_axis = r / vr
    n = 2000
    dt = t_axis / n
    z, vz = 0.0, u
    a = E_CHARGE * field / M_PROTON
    for _ in range(n):
        z += vz * dt + 0.5 * a * dt * dt
        vz += a * dt
    return z * 1e3


PARAMS = {"density": 1.0, "speed": 100.0}
VARIANTS = [{"density": 5.0}, {"speed": 300.0}, {"density": 0.5, "speed": 50.0}]
ANSWER = 1.3855781250000003
TOL = 1e-9

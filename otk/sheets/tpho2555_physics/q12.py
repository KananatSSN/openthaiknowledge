"""Theory 3 (c)-(d): a proton crosses the hole in d/u while the radial field e r E/d pushes it toward the axis, an impulse e r E/u, so it leaves with v_r = e r E/(m u) = e r sigma/(epsilon0 m u). Adapted: sigma (microcoulombs per square metre), u (km/s) and r (mm) vary; returns v_r in m/s."""

EPS0, E_CHARGE, M_PROTON = 8.85e-12, 1.6e-19, 1.67e-27


def solve(density=1.0, speed=100.0, radius=0.5):
    field = density * 1e-6 / EPS0
    return E_CHARGE * radius * 1e-3 * field / (M_PROTON * speed * 1e3)


def check(density=1.0, speed=100.0, radius=0.5, thickness=1.0):
    # Step a proton through the hole (the radial shift during the crossing
    # is negligible), accumulating the radial push.
    field = density * 1e-6 / EPS0
    d, u, r = thickness * 1e-3, speed * 1e3, radius * 1e-3
    n = 1000
    dt = d / u / n
    v = 0.0
    for _ in range(n):
        v += E_CHARGE * (r / d) * field / M_PROTON * dt
    return v


PARAMS = {"density": 1.0, "speed": 100.0, "radius": 0.5}
VARIANTS = [{"density": 5.0}, {"speed": 400.0}, {"radius": 2.0}]
ANSWER = 54129.03007544232
TOL = 1e-9

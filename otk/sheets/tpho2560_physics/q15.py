"""Theory 3 B.2: with z = vt, r = r0 + beta z^2 gives a radial acceleration 2 beta v^2, so beta = a0/(2 v^2) = 5.94e-7 per metre for 10^6 protons at 4.0 MeV, r0 = 1.0 mm, l = 30 cm. Adapted: n (millions), the energy (MeV), r0 (mm) and l (cm) vary; returns beta in units of 1e-7 per metre."""

from math import sqrt


def solve(count=1.0, energy=4.0, radius=1.0, length=30.0):
    from otk.sheets.tpho2560_physics import q14

    v = sqrt(2 * energy * 1e6 * 1.6e-19 / 1.67e-27)
    return q14.solve(count, energy, radius, length) * 1e8 / (2 * v * v) * 1e7


def check(count=1.0, energy=4.0, radius=1.0, length=30.0):
    # Step the edge radius in z with constant acceleration a0 over a short
    # distance and fit r - r0 = beta z^2.
    from otk.sheets.tpho2560_physics import q14

    v = sqrt(2 * energy * 1e6 * 1.6e-19 / 1.67e-27)
    a0 = q14.solve(count, energy, radius, length) * 1e8
    z_end, steps = 1e-3, 1000
    dt = z_end / v / steps
    r, vr = 0.0, 0.0
    for _ in range(steps):
        r += vr * dt + 0.5 * a0 * dt * dt
        vr += a0 * dt
    return r / z_end**2 * 1e7


PARAMS = {"count": 1.0, "energy": 4.0, "radius": 1.0, "length": 30.0}
VARIANTS = [{"count": 3.0}, {"radius": 0.5}, {"energy": 10.0, "length": 20.0}]
ANSWER = 5.943438658580359
TOL = 1e-9

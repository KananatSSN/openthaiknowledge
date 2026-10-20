"""Shared event simulation for problem 2: m resting on M, both dropped from h on a smooth vertical rod between the floor and a ceiling at H."""


def first_bounce(ratio, drop, g=10.0):
    """(v, V): speeds of m and M just after M rebounds off the floor and meets m."""
    v0 = (2 * g * drop) ** 0.5
    # M rebounds with +v0 into m falling at -v0; elastic collision.
    m, big = ratio, 1.0
    u_m, u_M = -v0, v0
    v = ((m - big) * u_m + 2 * big * u_M) / (m + big)
    V = ((big - m) * u_M + 2 * m * u_m) / (m + big)
    return v, V


def second_collision(ratio, drop, ceiling, g=10.0, dt=1e-6):
    """(time after the first collision, height) of the next meeting."""
    v, V = first_bounce(ratio, drop, g)
    t, ym, vm, yM, vM = 0.0, 0.0, v, 0.0, V
    while True:
        ym += vm * dt
        vm -= g * dt
        yM += vM * dt
        vM -= g * dt
        t += dt
        if ym >= ceiling and vm > 0:
            vm, ym = -vm, ceiling
        if yM <= 0 and vM < 0:
            vM, yM = -vM, 0.0
        if t > 1e-3 and ym <= yM:
            return t, ym

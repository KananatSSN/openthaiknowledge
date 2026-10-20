"""Lab part 2: twisting alone, the paired disc magnets (total mass m, radius R, thickness d) have I = mR^2/4 + md^2/12 and f = (1/2 pi) sqrt(mu B_h/I), so mu = I (2 pi f)^2/B_h; 50 swings in 33.97 s give f = 1.47 Hz, I = 1.435e-6 kg m^2 and mu = 3.0 A m^2 with B_h = 0.41 G. Adapted: the time for 50 swings and B_h (G) vary; returns mu in A m^2."""

from math import pi


def solve(time50=33.97, field=0.41, mass=27.6, radius=14.0, thickness=6.0):
    m, R, d = mass * 1e-3, radius * 1e-3, thickness * 1e-3
    inertia = m * R * R / 4 + m * d * d / 12
    f = 50 / time50
    return inertia * (2 * pi * f) ** 2 / (field * 1e-4)


def check(time50=33.97, field=0.41, mass=27.6, radius=14.0, thickness=6.0):
    # Bisect mu until a simulated small twist (torque -mu B sin phi) takes
    # the measured time for one swing.
    from math import sin

    m, R, d = mass * 1e-3, radius * 1e-3, thickness * 1e-3
    inertia = m * (R * R / 4 + d * d / 12)
    target = time50 / 50
    B = field * 1e-4

    def period(mu):
        phi, w, t, dt = 1e-3, 0.0, 0.0, target / 20000
        crossings = []
        prev = phi
        while len(crossings) < 2:
            a = -mu * B * sin(phi) / inertia
            w += a * dt
            phi += w * dt
            t += dt
            if prev > 0 >= phi or prev < 0 <= phi:
                crossings.append(t - dt * phi / (phi - prev))
            prev = phi
        return 2 * (crossings[1] - crossings[0])

    lo, hi = 0.01, 100.0
    for _ in range(60):
        mid = (lo * hi) ** 0.5
        if period(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo * hi) ** 0.5


PARAMS = {"time50": 33.97, "field": 0.41, "mass": 27.6, "radius": 14.0, "thickness": 6.0}
VARIANTS = [{"time50": 40.0}, {"field": 0.35}, {"time50": 28.5, "field": 0.45}]
ANSWER = 2.993899519904359
TOL = 1e-4

"""Short6: the spinning ring's current I = Q omega/(2 pi) gives B = mu0 I/(2R) = mu0 Q omega/(4 pi R) at O. Tesla for Q in microcoulombs, R in m."""

from math import cos, pi, sin

MU0 = 4e-7 * pi


def solve(charge=4, omega=10, radius=0.5):
    return MU0 * charge * 1e-6 * omega / (4 * pi * radius)


def check(charge=4, omega=10, radius=0.5, n=4000):
    # Moving point charges: B = mu0/(4 pi) q v x r_hat / r^2 summed round the ring.
    q = charge * 1e-6 / n
    v = omega * radius
    bz = 0.0
    for k in range(n):
        p = 2 * pi * k / n
        vel = (-v * sin(p), v * cos(p))
        r = (-radius * cos(p), -radius * sin(p))
        bz += MU0 / (4 * pi) * q * (vel[0] * r[1] - vel[1] * r[0]) / radius**3
    return bz


PARAMS = {"charge": 4, "omega": 10, "radius": 0.5}
VARIANTS = [{"radius": 2}, {"charge": 10, "omega": 50}, {"omega": 1, "radius": 0.1}]
ANSWER = 8e-12

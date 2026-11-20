"""Theory 1.2.1-1.2.2 figure: light enters a drop (index n) at incidence phi, refracts to alpha = asin(sin(phi)/n), reflects once inside and leaves; the deviation is delta = pi - 4 alpha + 2 phi (shown as the angle between incoming and outgoing rays). Adapted: n and phi given; degrees."""

from math import asin, degrees, radians, sin


def solve(index=4 / 3, incidence=60):
    alpha = degrees(asin(sin(radians(incidence)) / index))
    return 180 - 4 * alpha + 2 * incidence


def check(index=4 / 3, incidence=60):
    # Trace the ray as vectors in the plane: refract, reflect, refract; the
    # deviation (below 180 degrees here) is the angle between the input and
    # output directions.
    from math import acos, cos, sqrt

    def refract(d, n_hat, ratio):
        cos_i = -(d[0] * n_hat[0] + d[1] * n_hat[1])
        k = 1 - ratio**2 * (1 - cos_i**2)
        t = ratio * cos_i - sqrt(k)
        return (ratio * d[0] + t * n_hat[0], ratio * d[1] + t * n_hat[1])

    def reflect(d, n_hat):
        dot = d[0] * n_hat[0] + d[1] * n_hat[1]
        return (d[0] - 2 * dot * n_hat[0], d[1] - 2 * dot * n_hat[1])

    phi = radians(incidence)
    # Unit circle drop; ray travels +x and hits the point at polar angle pi - phi.
    p = (cos(3.141592653589793 - phi), sin(3.141592653589793 - phi))
    d = (1.0, 0.0)
    d = refract(d, p, 1 / index)                     # outward normal is p
    # next hit on the circle: p + t d, |.| = 1
    t = -2 * (p[0] * d[0] + p[1] * d[1])
    q = (p[0] + t * d[0], p[1] + t * d[1])
    d = reflect(d, (-q[0], -q[1]))
    t = -2 * (q[0] * d[0] + q[1] * d[1])
    r = (q[0] + t * d[0], q[1] + t * d[1])
    d = refract(d, (-r[0], -r[1]), index)
    return degrees(acos(max(-1.0, min(1.0, d[0]))))


PARAMS = {"index": 4 / 3, "incidence": 60}
VARIANTS = [{"incidence": 40}, {"index": 1.5, "incidence": 50}, {"incidence": 75}]
ANSWER = 137.9785986903256
TOL = 1e-9

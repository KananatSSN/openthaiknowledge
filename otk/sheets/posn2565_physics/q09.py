"""MC9 figure: equal smooth spheres; B at rest with its lowest point on the line of A's centre, so the centres are offset by b = R. At contact the line of centres makes alpha with u, sin alpha = b/(2R) = 1/2, and B leaves at u cos alpha = (sqrt3/2) u (answer 3). Adapted: offset b, radius R, speed u (m/s)."""

from math import sqrt


def solve(offset=5, radius=5, speed=10):
    s = offset / (2 * radius)
    return speed * sqrt(1 - s * s)


def check(offset=5, radius=5, speed=10):
    # Find the contact by bisection on A's position, then apply an elastic
    # impulse along the line of centres for equal masses and check energy.
    lo, hi = -10 * radius, 0.0
    for _ in range(200):
        x = (lo + hi) / 2
        if sqrt(x * x + offset * offset) > 2 * radius:
            lo = x
        else:
            hi = x
    x = (lo + hi) / 2
    nx, ny = -x / (2 * radius), offset / (2 * radius)
    j = speed * nx  # equal masses, elastic: B gets the normal component
    a = (speed - j * nx, -j * ny)
    b = (j * nx, j * ny)
    assert abs(sum(c * c for c in a) + sum(c * c for c in b) - speed * speed) < 1e-6
    return sqrt(b[0] ** 2 + b[1] ** 2)


PARAMS = {"offset": 5, "radius": 5, "speed": 10}
VARIANTS = [{"offset": 6}, {"offset": 8, "speed": 5}, {"offset": 2, "radius": 13}]
TOL = 1e-9
ANSWER = 8.660254037844386

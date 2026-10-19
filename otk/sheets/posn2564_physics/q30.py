"""Short30 figure: projectile from A at speed u and elevation theta strikes a vertical wall a distance L away, perpendicularly, at height H. Hitting at right angles means the apex: tan theta = 2H/L and u^2 = g(L^2 + 4H^2)/(2H). Returns (tan theta, u^2)."""

from math import cos, sin, sqrt


def solve(width=40, height=15, g=10):
    return 2 * height / width, g * (width**2 + 4 * height**2) / (2 * height)


def check(width=40, height=15, g=10):
    # Bisect on the launch angle so the apex sits at x = L, take u^2 from the
    # apex height, then confirm the path passes (L, H) moving horizontally.
    def apex_x(theta):
        u2 = 2 * g * height / sin(theta) ** 2
        return u2 * sin(theta) * cos(theta) / g

    lo, hi = 1e-6, 1.5707
    for _ in range(200):
        mid = (lo + hi) / 2
        if apex_x(mid) > width:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    u2 = 2 * g * height / sin(theta) ** 2
    u = sqrt(u2)
    t = width / (u * cos(theta))
    assert abs(u * sin(theta) * t - g * t * t / 2 - height) < 1e-6
    assert abs(u * sin(theta) - g * t) < 1e-6
    return (sin(theta) / cos(theta), u2)


PARAMS = {"width": 40, "height": 15, "g": 10}
VARIANTS = [{"width": 30, "height": 20}, {"width": 12, "height": 3}, {"width": 50, "height": 5}]
ANSWER = (0.75, 833.3333333333334)

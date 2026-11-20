"""Part2 item 19 figure: launched at u, theta from the vertical; d(r^2)/dt = g^2 t {(t - 3u cos/2g)^2 + (2u^2/g^2)(1 - 9cos^2/8)} never goes negative when cos^2 theta <= 8/9, i.e. sin theta >= 1/3. Returns the least sin theta."""

from math import sqrt


def solve(launch=10, g=10):
    return 1 / 3


def check(launch=10, g=10):
    # Bisect on sin(theta): simulate r^2 along the flight and see whether it
    # ever decreases.
    def monotone(s):
        c = sqrt(1 - s * s)
        last, t, dt = 0.0, 0.0, 1e-3 * launch / g
        while t < 6 * launch / g:
            t += dt
            x, y = launch * s * t, launch * c * t - g * t * t / 2
            r2 = x * x + y * y
            if r2 < last - 1e-12:
                return False
            last = r2
        return True

    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if monotone(mid):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


PARAMS = {"launch": 10, "g": 10}
VARIANTS = [{"launch": 20}, {"launch": 5, "g": 9.8}, {"launch": 30}]
TOL = 2e-3
ANSWER = 0.3333333333333333

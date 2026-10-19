"""Part2 item 17 figure: a boat sails at u parallel to a cliff L away; the horn sounds at A, the echo is heard at B after T. The sound path A-C-B (isosceles) has length vT while AB = uT: L = (T/2) sqrt(v^2 - u^2)."""

from math import sqrt


def solve(time=4, sound=5, boat=3):
    return time / 2 * sqrt(sound * sound - boat * boat)


def check(time=4, sound=5, boat=3):
    # Bisect on L: the echo returns to the moving boat after path / v.
    def echo_time(dist):
        lo, hi = 0.0, 1e6
        for _ in range(200):
            t = (lo + hi) / 2
            path = 2 * sqrt(dist * dist + (boat * t / 2) ** 2)
            if path > sound * t:
                lo = t
            else:
                hi = t
        return (lo + hi) / 2

    lo, hi = 0.0, 1e5
    for _ in range(200):
        mid = (lo + hi) / 2
        if echo_time(mid) < time:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"time": 4, "sound": 5, "boat": 3}
VARIANTS = [{"time": 2, "sound": 13, "boat": 5}, {"time": 10}, {"sound": 340, "boat": 20, "time": 6}]
TOL = 1e-7
ANSWER = 8.0

"""Theory 2.1 figure: a smooth vertical cylinder open at both ends, a large piston (area A) above a small one (area a), joined by a rigid rod, total mass M, enclosing gas, outside pressure Pa: (P0 - Pa)(A - a) = Mg, so P0 = Pa + Mg/(A - a). Adapted: numbers; pascals with g = 9.8."""


def solve(outside=1.0e5, mass=20, big=0.05, small=0.01, g=9.8):
    return outside + mass * g / (big - small)


def check(outside=1.0e5, mass=20, big=0.05, small=0.01, g=9.8):
    # Bisect on the gas pressure for zero net force on the piston pair
    # (upward: gas under A and outside air under a; downward: air on A, gas
    # on a, and the weight).
    def net(p):
        return p * big + outside * small - outside * big - p * small - mass * g

    lo, hi = 0.0, 1e8
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if net(mid) < 0 else (lo, mid)
    return lo


PARAMS = {"outside": 1.0e5, "mass": 20, "big": 0.05, "small": 0.01, "g": 9.8}
VARIANTS = [{"mass": 5}, {"big": 0.02, "small": 0.015}, {"outside": 9.0e4}]
ANSWER = 104900.0
TOL = 1e-9

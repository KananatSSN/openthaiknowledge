"""Theory 3.8: a second -q' at Q with r = r0 is in equilibrium when rho r0/(3 eps0) = q'/(4 pi eps0 (2 r0)^2): r0^3 = 3q'/(16 pi rho). Adapted: q' as the charge of a ball of radius s at density rho, so r0 = s/4^(1/3); metres."""


def solve(size=0.5):
    return size / 4 ** (1 / 3)


def check(size=0.5):
    # Bisect the net outward force on the charge at Q: the ball's field
    # pushes it in, the charge at P pushes it out (rho = eps0 = 1).
    from math import pi

    q = 4 / 3 * pi * size**3

    def net(r):
        return -r / 3 * q + q * q / (4 * pi * (2 * r) ** 2)

    lo, hi = 1e-6, 10 * size
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if net(mid) > 0 else (lo, mid)
    return lo


PARAMS = {"size": 0.5}
VARIANTS = [{"size": 1.0}, {"size": 0.12}, {"size": 3.0}]
ANSWER = 0.3149802624737183
TOL = 1e-9

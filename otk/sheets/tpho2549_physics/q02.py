"""Theory 1.2 figure: a solid cylinder rolls from rest down a slope at theta without slipping when mu >= tan(theta)/3; in general mu >= tan(theta) k/(1 + k) with I = k m R^2. Adapted: tan theta and k (1/2 cylinder, 2/5 sphere, 1 hoop) given."""


def solve(slope=0.75, shape=0.5):
    return slope * shape / (1 + shape)


def check(slope=0.75, shape=0.5):
    # Bisect on mu: with friction mu N, does the contact point slip?
    from math import atan, cos, sin

    theta = atan(slope)

    def slips(mu):
        f = mu * cos(theta)                 # per unit m g
        a = sin(theta) - f                  # linear acceleration / g
        alpha_r = f / shape                 # R * angular acceleration / g
        return a > alpha_r + 1e-15

    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if slips(mid) else (lo, mid)
    return hi


PARAMS = {"slope": 0.75, "shape": 0.5}
VARIANTS = [{"shape": 0.4}, {"shape": 1.0, "slope": 1.0}, {"slope": 0.25}]
ANSWER = 0.25
TOL = 1e-9

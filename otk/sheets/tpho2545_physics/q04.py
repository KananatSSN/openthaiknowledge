"""Theory I.3 figure: object at a (inside f) gives a virtual image the same size as the real image of the object at b (beyond f): f/(f - a) = f/(b - f), so f = (a + b)/2. cm."""


def solve(near=6, far=14):
    return (near + far) / 2


def check(near=6, far=14):
    # Bisect on f between the two distances for equal magnifications.
    mag = lambda u, f: abs(f / (f - u))
    lo, hi = near + 1e-9, far - 1e-9
    for _ in range(200):
        f = (lo + hi) / 2
        if mag(near, f) > mag(far, f):
            lo = f
        else:
            hi = f
    return (lo + hi) / 2


PARAMS = {"near": 6, "far": 14}
VARIANTS = [{"near": 10, "far": 30}, {"near": 3, "far": 5}, {"near": 8, "far": 40}]
ANSWER = 10.0

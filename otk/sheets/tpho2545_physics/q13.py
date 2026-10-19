"""Theory III.b: the force I a B over the tube's section a b supports a level difference h: D g h a b = I a B, h = I B/(D g b). Metres."""


def solve(current=1.2, field=1.0, density=1200, width=0.01, g=9.8):
    return current * field / (density * g * width)


def check(current=1.2, field=1.0, density=1200, width=0.01, g=9.8, depth=0.01):
    # Bisect on h for the pressure balance across the plates' region.
    push = current * depth * field / (depth * width)
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if density * g * mid < push:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"current": 1.2, "field": 1.0, "density": 1200, "width": 0.01, "g": 9.8}
VARIANTS = [{"current": 3}, {"field": 0.5, "width": 0.02}, {"density": 1000, "g": 10}]
ANSWER = 0.01020408163265306

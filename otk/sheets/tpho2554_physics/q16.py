"""Theory 3.7: a cylinder piece of radius R and length L becomes a sphere of radius r with the same volume (pi R^2 L = 4 pi r^3/3) and, by energy, the same side area (2 pi R L = 4 pi r^2), so L = 9R/2, about half of Plateau and Rayleigh's 9.1R, and r = 3R/2. Adapted: the jet radius R (mm) varies; returns r in mm."""


def solve(radius=1.33):
    return 1.5 * radius


def check(radius=1.33):
    # Eliminate L with the volume condition and bisect the area condition
    # 2 pi R (4 r^3/(3 R^2)) = 4 pi r^2 for its nonzero root.
    from math import pi

    def residual(r):
        length = 4 * r**3 / (3 * radius**2)
        return 2 * pi * radius * length - 4 * pi * r * r

    lo, hi = 0.1 * radius, 10 * radius
    for _ in range(200):
        mid = (lo + hi) / 2
        if residual(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"radius": 1.33}
VARIANTS = [{"radius": 0.5}, {"radius": 2.0}, {"radius": 0.9}]
ANSWER = 1.995
TOL = 1e-9

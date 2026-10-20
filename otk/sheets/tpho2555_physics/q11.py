"""Theory 3 (b) figures 2-3: a Gaussian cylinder of radius r and length d in the hole has flux 2 pi r^2 E out of its ends, so 2 pi r d E_r + 2 pi r^2 E = 0 and E_r = -(r/d) E, toward the axis. Adapted: r and d (mm) vary; returns |E_r|/E."""


def solve(radius=0.5, thickness=1.0):
    return radius / thickness


def check(radius=0.5, thickness=1.0):
    # E_z runs linearly from -E to +E across the hole; div E = 0 in
    # cylindrical form, (1/r) d(r E_r)/dr = -dE_z/dz, integrated outward.
    n = 2000
    slope = 2.0 / thickness
    flux = 0.0
    for i in range(n):
        r = (i + 0.5) * radius / n
        flux += -slope * r * radius / n
    return abs(flux / radius)


PARAMS = {"radius": 0.5, "thickness": 1.0}
VARIANTS = [{"radius": 2.0}, {"thickness": 0.4}, {"radius": 1.5, "thickness": 3.0}]
ANSWER = 0.5
TOL = 1e-9

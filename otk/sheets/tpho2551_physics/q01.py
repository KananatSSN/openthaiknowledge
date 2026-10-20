"""Theory 1.1.2: with liquid of index n between the shells, light refracts into the liquid lens, reflects from B and refracts out again; the slit images onto itself at L' = R/(2n - 1). For R = 20 cm and n = 4/3, L' = 12 cm: move the slit 8 cm closer. Adapted: R and n given; returns L - L' in cm (positive = closer)."""


def solve(radius=20, index=4 / 3):
    return radius - radius / (2 * index - 1)


def check(radius=20, index=4 / 3):
    # Paraxial ray-transfer matrices: refraction at a surface of radius R from
    # air into n, reflection at the mirror (radius R), refraction back out;
    # find the object distance imaged onto itself by bisection.
    def image_distance(s):
        # thin system: refract (air->n, R), reflect (R), refract (n->air, R)
        power = (index - 1) / radius            # first surface
        mirror = 2 * index / radius             # mirror in medium n
        total = 2 * power + mirror              # equivalent mirror power
        return 1 / (total - 1 / s)

    lo, hi = 1e-6, 10 * radius
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if image_distance(mid) > mid else (lo, mid)
    return radius - lo


PARAMS = {"radius": 20, "index": 4 / 3}
VARIANTS = [{"index": 1.5}, {"radius": 30, "index": 1.25}, {"radius": 12, "index": 1.6}]
ANSWER = 7.999999999999998
TOL = 1e-9

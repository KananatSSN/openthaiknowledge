"""Theory 1.2: light reflected inside the lens from the curved face (a concave mirror of focal length R/2 seen from inside) converges R/2 - t inside the flat face and leaves it appearing (R/2 - t)/n from it: x = 1.0 cm for R = 5 cm, t = 1 cm, n = 1.5. Adapted: numbers for n, t, D (R from D); cm."""


def solve(index=1.5, thickness=1.0, focus=11.0):
    radius = (index - 1) * (focus - thickness)
    return (radius / 2 - thickness) / index


def check(index=1.5, thickness=1.0, focus=11.0):
    # Trace a paraxial ray: reflect off the spherical face (exact geometry at a
    # small height), carry it to the flat face, refract with Snell, and find
    # where it meets the axis outside.
    from math import asin, sin, tan

    radius = (index - 1) * (focus - thickness)
    h = 1e-5
    # Mirror normal angle at height h; incoming ray parallel to the axis.
    phi = asin(h / radius)
    out = 2 * phi                       # reflected ray angle toward the axis
    sag = radius - (radius**2 - h * h) ** 0.5
    # Travel back from the mirror (at depth thickness - sag) to the flat face.
    height = h - (thickness - sag) * tan(out)
    inside = out
    outside = asin(index * sin(inside))
    return height / tan(outside) if outside else float("inf")


PARAMS = {"index": 1.5, "thickness": 1.0, "focus": 11.0}
VARIANTS = [{"index": 1.6, "focus": 15}, {"thickness": 0.5, "focus": 21}, {"index": 1.4, "focus": 16}]
ANSWER = 1.0
TOL = 1e-4

"""Theory 1.2 figure 1.2: a plano-convex lens (centre thickness t, index n), light entering the flat face, focuses D behind the flat face; only the curved face refracts, so its focus is D - t beyond the vertex and R = (n - 1)(D - t). With t = 1.0 cm, n = 1.5, D = 11.0 cm, R = 5 cm. Adapted: numbers for n, t, D; cm."""


def solve(index=1.5, thickness=1.0, focus=11.0):
    return (index - 1) * (focus - thickness)


def check(index=1.5, thickness=1.0, focus=11.0):
    # Paraxial ray from height h through the curved face (exact Snell at a
    # tiny height), then where it crosses the axis.
    from math import asin, sin, tan

    def crossing(radius, h=1e-4):
        a1 = asin(h / radius)          # incidence on the curved face inside glass
        a2 = asin(index * sin(a1))     # refracted angle in air
        bend = a2 - a1                 # ray angle below the axis
        sag = radius - (radius**2 - h * h) ** 0.5
        return thickness - sag + h / tan(bend)

    lo, hi = 1e-3, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if crossing(mid) < focus else (lo, mid)
    return lo


PARAMS = {"index": 1.5, "thickness": 1.0, "focus": 11.0}
VARIANTS = [{"index": 1.6}, {"thickness": 0.5, "focus": 21}, {"index": 1.4, "focus": 16}]
ANSWER = 5.0
TOL = 1e-5

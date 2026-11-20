"""Lab part 1: the lower magnet drops when the hanging mass M satisfies Mg = b r^n, so log M against log r is a line of slope n; the solution's 13 readings give n = -3.9. Adapted with synthetic distances (mm) and masses (g); returns n."""

from math import log10


def solve(distances=(26.05, 27.72, 29.81, 31.49, 34.41, 37.55, 41.10), masses=(63.8, 51.6, 41.1, 27.6, 21.5, 14.8, 10.9)):
    xs = [log10(r) for r in distances]
    ys = [log10(m) for m in masses]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def check(distances=(26.05, 27.72, 29.81, 31.49, 34.41, 37.55, 41.10), masses=(63.8, 51.6, 41.1, 27.6, 21.5, 14.8, 10.9)):
    from math import log

    from otk.sheets.tpho2560_physics._shared import line

    return line([log(r) for r in distances], [log(m) for m in masses])[0]


PARAMS = {"distances": (26.05, 27.72, 29.81, 31.49, 34.41, 37.55, 41.10), "masses": (63.8, 51.6, 41.1, 27.6, 21.5, 14.8, 10.9)}
VARIANTS = [{"masses": (60.0, 48.0, 37.0, 30.0, 21.0, 15.0, 11.0)}, {"distances": (25.0, 27.0, 29.0, 31.0, 34.0, 37.0, 40.0)}, {"masses": (70.0, 55.0, 42.0, 34.0, 25.0, 18.0, 13.5)}]
ANSWER = -3.972585034495673
TOL = 1e-9

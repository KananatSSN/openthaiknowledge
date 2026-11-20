"""Lab part 1: the illuminance falls as 1/x^2 so log R = -2 gamma log x + c2, and the slope of log R against log x gives gamma = -slope/2; the solution's 1.2531 gives gamma = -0.63. Adapted with synthetic distances (cm) and resistances (ohm); returns gamma."""

from math import log10


def solve(distances=(21, 25, 31, 41, 55, 73), resistances=(846, 1009, 1334, 1866, 2743, 4140)):
    xs = [log10(x) for x in distances]
    ys = [log10(r) for r in resistances]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return -slope / 2


def check(distances=(21, 25, 31, 41, 55, 73), resistances=(846, 1009, 1334, 1866, 2743, 4140)):
    # Fit in natural logarithms instead (the slope does not depend on the base).
    from math import log

    from otk.sheets.tpho2559_physics._shared import line

    slope, _ = line([log(x) for x in distances], [log(r) for r in resistances])
    return -slope / 2


PARAMS = {"distances": (21, 25, 31, 41, 55, 73), "resistances": (846, 1009, 1334, 1866, 2743, 4140)}
VARIANTS = [{"resistances": (900, 1100, 1450, 2100, 3100, 4800)}, {"distances": (20, 24, 30, 40, 54, 72)}, {"resistances": (700, 800, 960, 1200, 1500, 1900)}]
ANSWER = -0.6373558363854258
TOL = 1e-9

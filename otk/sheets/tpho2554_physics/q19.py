"""Lab 2 part 1 figure 1: the box starts to slide when the hanging clips' weight reaches mu_s N, so mu_s is the slope of the clips' mass at slipping against the box's mass (least squares). Adapted with synthetic readings (box mass in g, clips needed) and the mass of one clip (g); returns mu_s."""


def solve(clip=1.5, loads=(100, 150, 200, 250, 300), counts=(27, 40, 53, 67, 80)):
    xs, ys = list(loads), [n * clip for n in counts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def check(clip=1.5, loads=(100, 150, 200, 250, 300), counts=(27, 40, 53, 67, 80)):
    # Normal equations solved by Cramer's rule.
    xs, ys = list(loads), [n * clip for n in counts]
    n, sx, sy = len(xs), sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


PARAMS = {"clip": 1.5, "loads": (100, 150, 200, 250, 300), "counts": (27, 40, 53, 67, 80)}
VARIANTS = [{"clip": 2.0, "counts": (20, 30, 40, 50, 60)}, {"loads": (80, 120, 160, 200, 240)}, {"counts": (25, 41, 52, 68, 79)}]
ANSWER = 0.399
TOL = 1e-12

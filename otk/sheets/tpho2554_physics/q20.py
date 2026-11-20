"""Lab 2 part 2 figure 2: the ruler starts to move when mu_k N_B = mu_s N_A, and N_B/N_A = x_A/x_B, so the slope of x_A against x_B is mu_s/mu_k and mu_k = mu_s/slope. Adapted with synthetic distances (cm) from the centre of mass and mu_s from part 1; returns mu_k."""


def solve(static=0.40, near=(4.0, 6.0, 8.0, 10.0, 12.0), far=(3.1, 4.6, 6.2, 7.7, 9.2)):
    n = len(near)
    mx, my = sum(far) / n, sum(near) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(far, near)) / sum((x - mx) ** 2 for x in far)
    return static / slope


def check(static=0.40, near=(4.0, 6.0, 8.0, 10.0, 12.0), far=(3.1, 4.6, 6.2, 7.7, 9.2)):
    # Normal equations solved by Cramer's rule.
    xs, ys = list(far), list(near)
    n, sx, sy = len(xs), sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    return static * (n * sxx - sx * sx) / (n * sxy - sx * sy)


PARAMS = {"static": 0.40, "near": (4.0, 6.0, 8.0, 10.0, 12.0), "far": (3.1, 4.6, 6.2, 7.7, 9.2)}
VARIANTS = [{"static": 0.55}, {"far": (2.8, 4.2, 5.6, 7.0, 8.4)}, {"near": (5.0, 7.5, 10.0, 12.5, 15.0)}]
ANSWER = 0.3060392156862745
TOL = 1e-12

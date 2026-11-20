"""Lab 2 item 3: omega^2 = k/(M + beta1 m) makes T^2 = (4 pi^2/k) M + 4 pi^2 beta1 m/k a straight line in M, so beta1 = intercept/(slope m). Adapted with synthetic periods (grams, seconds) and the spring's mass m (g); returns beta1."""


def solve(spring=40.0, masses=(20.0, 40.0, 60.0, 80.0, 100.0), periods=(0.376, 0.467, 0.544, 0.612, 0.673)):
    xs, ys = list(masses), [t * t for t in periods]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return (my - slope * mx) / (slope * spring)


def check(spring=40.0, masses=(20.0, 40.0, 60.0, 80.0, 100.0), periods=(0.376, 0.467, 0.544, 0.612, 0.673)):
    from otk.sheets.tpho2555_physics._fit import line

    slope, intercept = line(list(masses), [t * t for t in periods])
    # The intercept over the slope is the effective mass beta1 m.
    return intercept / slope / spring


PARAMS = {"spring": 40.0, "masses": (20.0, 40.0, 60.0, 80.0, 100.0), "periods": (0.376, 0.467, 0.544, 0.612, 0.673)}
VARIANTS = [{"spring": 30.0}, {"periods": (0.40, 0.49, 0.565, 0.632, 0.693)}, {"masses": (30.0, 50.0, 70.0, 90.0, 110.0)}]
ANSWER = 0.40219110499370797
TOL = 1e-12

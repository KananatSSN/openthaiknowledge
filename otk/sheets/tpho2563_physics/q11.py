"""Theory 2.8: moist air obeys T2 - T1 = -alpha(z2 - z1) - (alpha L_v/g)[beta(T2) - beta(T1)]; reading beta off the paper's graph gives T2 = -1.7 C. Here beta(T) is the straight line beta(T1) + s(T - T1) through the solution's beta(T1) = 6.0e-3 at 5.95 C with s = 0.349e-3 per C (the slope its answer implies), so T2 = T1 - alpha(z2 - z1)/(1 + alpha L_v s/g). Adapted: T1 (C), both heights (m) and s (1e-3 per C) vary; returns Celsius."""


def solve(lower=5.95, start=1440.0, top=2900.0, slope=0.349):
    alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)
    gain = alpha * 2.5e6 / 9.81 * slope * 1e-3
    return lower - alpha * (top - start) / (1 + gain)


def check(lower=5.95, start=1440.0, top=2900.0, slope=0.349):
    from otk.sheets.tpho2563_physics._shared import bisect

    alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)

    def beta(t):
        return 6.0e-3 + slope * 1e-3 * (t - lower)

    def miss(t):
        return t - (lower - alpha * (top - start) - alpha * 2.5e6 / 9.81 * (beta(t) - beta(lower)))

    return bisect(miss, lower - 60, lower)


PARAMS = {"lower": 5.95, "start": 1440.0, "top": 2900.0, "slope": 0.349}
VARIANTS = [{"slope": 0.2}, {"top": 3500.0}, {"lower": 12.0}]
ANSWER = -1.6869643760055162
TOL = 1e-9

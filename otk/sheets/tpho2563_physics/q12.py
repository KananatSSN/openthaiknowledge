"""Theory 2.9: the mean moist lapse rate from S1 to S2 is (T2 - T1)/(z2 - z1) = -5.2 C/km, about half the dry rate, with T2 from 2.8. Adapted as in 2.8 (beta a straight line of slope s); returns C/km."""


def solve(lower=5.95, start=1440.0, top=2900.0, slope=0.349):
    from otk.sheets.tpho2563_physics import q11

    return (q11.solve(lower=lower, start=start, top=top, slope=slope) - lower) / (top - start) * 1e3


def check(lower=5.95, start=1440.0, top=2900.0, slope=0.349):
    from otk.sheets.tpho2563_physics import q11

    # step the moist ascent in metres, condensing as beta falls
    alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)
    gain = alpha * 2.5e6 / 9.81 * slope * 1e-3
    t, steps = lower, 10000
    dz = (top - start) / steps
    for _ in range(steps):
        t += -alpha * dz / (1 + gain)
    assert abs(t - q11.check(lower=lower, start=start, top=top, slope=slope)) < 1e-6
    return (t - lower) / (top - start) * 1e3


PARAMS = {"lower": 5.95, "start": 1440.0, "top": 2900.0, "slope": 0.349}
VARIANTS = [{"slope": 0.2}, {"top": 3500.0}, {"slope": 0.5}]
ANSWER = -5.230797517811998
TOL = 1e-6

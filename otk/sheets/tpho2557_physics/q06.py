"""Theory 2 (b): the table stays upright while the wheel's normal force N2 = Mg - N1 is positive, i.e. a < wg/(2h), which with a = wg mu/(2(w - mu h)) means mu < w/(2h). Adapted: w and h vary; returns the largest mu."""


def solve(width=1.0, height=0.6):
    return width / (2 * height)


def check(width=1.0, height=0.6):
    # Bisect the friction coefficient at which the wheel's normal force vanishes.
    from otk.sheets.tpho2557_physics._shared import bisect, table

    return bisect(lambda mu: table(width, height, mu, True)[2], 1e-6, width / height * 0.999)


PARAMS = {"width": 1.0, "height": 0.6}
VARIANTS = [{"width": 0.8}, {"height": 1.2}, {"width": 1.5, "height": 0.4}]
ANSWER = 0.8333333333333334
TOL = 1e-9

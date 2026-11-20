"""Theory 2 (c): with the wheel in front, torque balance gives a2 = w g mu/(2(w + mu h)); from the same u, s2/s1 = a1/a2 = (w + mu h)/(w - mu h) = n, so mu = w(n - 1)/(h(n + 1)). Adapted: n, w and h vary; returns mu."""


def solve(ratio=1.5, width=1.0, height=0.6):
    return width * (ratio - 1) / (height * (ratio + 1))


def check(ratio=1.5, width=1.0, height=0.6):
    # Bisect mu until the two stopping distances (from the force equations
    # in each direction) are in the given ratio.
    from otk.sheets.tpho2557_physics._shared import bisect, table

    def gap(mu):
        forward = table(width, height, mu, True)[0]
        backward = table(width, height, mu, False)[0]
        return forward / backward - ratio

    return bisect(gap, 1e-6, width / (2 * height) * 0.999)


PARAMS = {"ratio": 1.5, "width": 1.0, "height": 0.6}
VARIANTS = [{"ratio": 2.0}, {"width": 0.8, "height": 0.5}, {"ratio": 1.2}]
ANSWER = 0.3333333333333333
TOL = 1e-9

"""Theory 1.1 figure 1: M slides at V0 into a resting m (M > m) on a smooth floor; elastic collision gives V1 = (M - m)V0/(M + m) and v1 = 2M V0/(M + m). Adapted: masses and V0 vary; returns v1 in m/s."""


def solve(big=5, small=1, speed=3):
    return 2 * big * speed / (big + small)


def check(big=5, small=1, speed=3):
    from otk.sheets.tpho2553_physics._wall import collisions

    _, _, v = next(collisions(big, small, speed, 1.0))
    return v


PARAMS = {"big": 5, "small": 1, "speed": 3}
VARIANTS = [{"big": 2}, {"small": 3, "big": 7}, {"speed": 10}]
ANSWER = 5.0
TOL = 1e-12

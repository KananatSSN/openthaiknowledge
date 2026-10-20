"""Theory 1.2 figure 2: m runs to the wall l0 away and back while M follows at V1; together they cover 2 l0, so the second collision is l1 = l0 (v1 - V1)/(v1 + V1) = l0 (M + m)/(3M - m) from the wall. Adapted: masses and l0 vary; metres."""


def solve(big=5, small=1, gap=1.4):
    return gap * (big + small) / (3 * big - small)


def check(big=5, small=1, gap=1.4):
    from otk.sheets.tpho2553_physics._wall import collisions

    meetings = collisions(big, small, 2.0, gap, count=2)
    next(meetings)
    distance, _, _ = next(meetings)
    return distance


PARAMS = {"big": 5, "small": 1, "gap": 1.4}
VARIANTS = [{"big": 2}, {"small": 3, "big": 7}, {"gap": 0.6}]
ANSWER = 0.5999999999999999
TOL = 1e-12

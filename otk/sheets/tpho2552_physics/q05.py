"""Theory 2.1 figure: m sits on M, both dropped from h; M rebounds elastically from the floor and meets m, so m leaves at v = ((3 - m/M)/(1 + m/M)) v0 and rises to ((3 - m/M)/(1 + m/M))^2 times the release height: 9 times when M >> m. Adapted: m/M given (0 for M >> m); returns the height multiple (no ceiling)."""


def solve(ratio=0.0):
    return ((3 - ratio) / (1 + ratio)) ** 2


def check(ratio=0.0):
    from otk.sheets.tpho2552_physics._balls import first_bounce

    v, _ = first_bounce(ratio, 1.0)
    return v * v / (2 * 10.0)


PARAMS = {"ratio": 0.0}
VARIANTS = [{"ratio": 1 / 6}, {"ratio": 0.5}, {"ratio": 0.25}]
ANSWER = 9.0
TOL = 1e-12

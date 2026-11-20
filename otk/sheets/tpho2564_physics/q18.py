"""Theory 3.1 g): by the first law the heat the lung air takes from the body is Q = dU + w = 22.1 + 2.7 = 24.8 J. Adapted: the volume (L), alpha (L) and k (1e-3 /Pa) vary; returns joules."""


def solve(volume=3.31, alpha=3.58, k=0.964):
    from otk.sheets.tpho2564_physics import q15, q17

    return q17.solve(volume=volume, alpha=alpha, k=k) + q15.solve(volume=volume, alpha=alpha, k=k)


def check(volume=3.31, alpha=3.58, k=0.964):
    from otk.sheets.tpho2564_physics import q15, q17

    return q17.check(volume=volume, alpha=alpha, k=k) + q15.check(volume=volume, alpha=alpha, k=k)


PARAMS = {"volume": 3.31, "alpha": 3.58, "k": 0.964}
VARIANTS = [{"volume": 3.0}, {"alpha": 3.6}, {"k": 1.2}]
ANSWER = 24.896776393955346
TOL = 1e-6

"""Theory 3.1 f): to keep its pressure as the chest pressure falls by p_D, the diatomic air filling V_f must gain internal energy (5/2) p_D V_f = 22.1 J (p_D = 2668 Pa, V_f = 3.31 L). Adapted: the volume (L), alpha (L) and k (1e-3 /Pa) vary, p_D from 3.1 c); returns joules."""


def solve(volume=3.31, alpha=3.58, k=0.964):
    from otk.sheets.tpho2564_physics import q14

    return 2.5 * q14.solve(volume=volume, alpha=alpha, k=k) * volume * 1e-3


def check(volume=3.31, alpha=3.58, k=0.964):
    from otk.sheets.tpho2564_physics import q14

    # U = (5/2) p V before and after, at the same volume
    p0 = 101325.0
    p_d = q14.check(volume=volume, alpha=alpha, k=k)
    return 2.5 * p0 * volume * 1e-3 - 2.5 * (p0 - p_d) * volume * 1e-3


PARAMS = {"volume": 3.31, "alpha": 3.58, "k": 0.964}
VARIANTS = [{"volume": 3.0}, {"alpha": 3.6}, {"k": 1.2}]
ANSWER = 22.18709584676346
TOL = 1e-9

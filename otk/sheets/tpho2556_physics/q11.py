"""Theory 2 (c)-(d): the moved gas filled V_B T_A/T_B in A at pressure mg/a, so the weight did W_A = (mg/a) V_B T_A/T_B on it; with V_B = mga/k and T_B/T_A = 2 gamma/(gamma + 1), W_A = m^2 g^2 (gamma + 1)/(2 gamma k). Adapted: m (kg), k and gamma vary; returns W_A in joules with g = 9.8."""


def solve(mass=5.0, spring=2000.0, gamma=1.4, g=9.8):
    return (mass * g) ** 2 * (gamma + 1) / (2 * gamma * spring)


def check(mass=5.0, spring=2000.0, gamma=1.4, g=9.8):
    from otk.sheets.tpho2556_physics._valve import transfer

    return transfer(mass, 50e-4, spring, gamma, 300.0, g)[3]


PARAMS = {"mass": 5.0, "spring": 2000.0, "gamma": 1.4, "g": 9.8}
VARIANTS = [{"gamma": 5 / 3}, {"mass": 2.0}, {"spring": 500.0, "gamma": 1.3}]
ANSWER = 1.029
TOL = 1e-6

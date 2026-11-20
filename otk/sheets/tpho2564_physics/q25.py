"""Lab part 1 d): with no load the free end sags dy = 3 mu g L^4/(2 E b h^3), so E = 3 mu g L^4/(2 b h^3 dy): an aluminium strip 2.5 cm by 1.75 mm of 0.122 kg/m sagging 2.9 cm over 60 cm gives 60 GPa. Adapted: the length (cm) and sag (cm) vary; returns GPa."""

STRIP = {"mu": 0.122, "b": 0.025, "h": 1.75e-3}


def solve(length=60.0, sag=2.9):
    L, dy = length * 1e-2, sag * 1e-2
    return 3 * STRIP["mu"] * 9.81 * L**4 / (2 * STRIP["b"] * STRIP["h"] ** 3 * dy) / 1e9


def check(length=60.0, sag=2.9):
    from otk.sheets.tpho2564_physics._shared import bisect

    # the modulus for which equation (2) with m = 0 predicts the sag
    L = length * 1e-2

    def miss(modulus):
        return L**3 / (2 * modulus * STRIP["b"] * STRIP["h"] ** 3) * 3 * STRIP["mu"] * L * 9.81 - sag * 1e-2

    return bisect(miss, 1e9, 1e12) / 1e9


PARAMS = {"length": 60.0, "sag": 2.9}
VARIANTS = [{"length": 90.0, "sag": 13.5}, {"sag": 3.3}, {"length": 75.0, "sag": 7.0}]
ANSWER = 59.87878038403539
TOL = 1e-6

"""Theory 1.5: with energy per unit volume (1/2) rho v^2 + (1/2) rho g h (the layer's centre of mass at h/2), the loss across the jump is (1/4) rho g (h2 - h1)(h2^2 + h1^2)/(h1 h2), so k = 1/4. Adapted: the depth before (cm) and the speed (m/s) vary, h2 from 1.4; returns the loss in J/m^3."""


def solve(depth=2.0, speed=3.0):
    from otk.sheets.tpho2562_physics import q03

    h1, h2 = depth * 1e-2, q03.solve(depth=depth, speed=speed) * 1e-2
    return 0.25 * 1000 * 9.8 * (h2 - h1) * (h2**2 + h1**2) / (h1 * h2)


def check(depth=2.0, speed=3.0):
    from otk.sheets.tpho2562_physics import q03

    h1, h2 = depth * 1e-2, q03.check(depth=depth, speed=speed) * 1e-2
    v2 = speed * h1 / h2
    before = 0.5 * 1000 * speed**2 + 0.5 * 1000 * 9.8 * h1
    after = 0.5 * 1000 * v2**2 + 0.5 * 1000 * 9.8 * h2
    return before - after


PARAMS = {"depth": 2.0, "speed": 3.0}
VARIANTS = [{"depth": 1.0}, {"speed": 5.0}, {"depth": 4.0, "speed": 2.0}]
ANSWER = 3652.187157974252
TOL = 1e-6

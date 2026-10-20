"""Theory 2 f): at high temperature M = chi B with chi = N mu^2/(k_B T). Adapted: the number of moments (1e23) and T (K) vary; returns J/T^2."""


def solve(count=1.0, temperature=300.0):
    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    return count * 1e23 * BOHR**2 / (BOLTZMANN * temperature)


def check(count=1.0, temperature=300.0):
    from otk.sheets.tpho2565_physics import q06
    from otk.sheets.tpho2565_physics._shared import BOHR

    # the slope of M = N mu tanh(mu B/k_B T) at small B
    h = 1e-3
    return count * 1e23 * BOHR * (q06.check(field=h, temperature=temperature) - q06.check(field=-h, temperature=temperature)) / (2 * h)


PARAMS = {"count": 1.0, "temperature": 300.0}
VARIANTS = [{"temperature": 77.0}, {"count": 6.02}, {"temperature": 4.2}]
ANSWER = 0.002077465603864734
TOL = 1e-6

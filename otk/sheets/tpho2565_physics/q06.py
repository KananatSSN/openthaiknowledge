"""Theory 2 b), d), g): two-level moments in B at T split as N_up/N = 1/(exp(-2x) + 1), x = mu B/(k_B T), so M/(N mu) = tanh x = 0.6 at 1 T and 1 K. Adapted: B (T) and T (K) vary."""

from math import tanh


def solve(field=1.0, temperature=1.0):
    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    return tanh(BOHR * field / (BOLTZMANN * temperature))


def check(field=1.0, temperature=1.0):
    from math import exp

    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    x = BOHR * field / (BOLTZMANN * temperature)
    up, down = exp(x), exp(-x)  # Boltzmann weights of the two states
    return (up - down) / (up + down)


PARAMS = {"field": 1.0, "temperature": 1.0}
VARIANTS = [{"field": 0.3}, {"temperature": 4.2}, {"field": 5.0, "temperature": 2.0}]
ANSWER = 0.5863129624957659
TOL = 1e-9

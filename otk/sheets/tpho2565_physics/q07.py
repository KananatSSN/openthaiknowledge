"""Theory 2 e), g): the entropy per particle is S/(N k_B) = ln(exp(-2x) + 1)/(exp(-2x) + 1) + ln(exp(2x) + 1)/(exp(2x) + 1), x = mu B/(k_B T): ln 2 = 0.69 at B = 0 and 0.51 at 1 T and 1 K. Adapted: B (T) and T (K) vary."""

from math import exp, log


def solve(field=1.0, temperature=1.0):
    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    x = BOHR * field / (BOLTZMANN * temperature)
    a, b = exp(-2 * x) + 1, exp(2 * x) + 1
    return log(a) / a + log(b) / b


def check(field=1.0, temperature=1.0, count=10**6):
    from math import lgamma

    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    # count the arrangements: S = k_B ln(N!/(N_up! N_down!)) for a large N
    x = BOHR * field / (BOLTZMANN * temperature)
    up = count / (exp(-2 * x) + 1)
    return (lgamma(count + 1) - lgamma(up + 1) - lgamma(count - up + 1)) / count


PARAMS = {"field": 1.0, "temperature": 1.0}
VARIANTS = [{"field": 0.0}, {"temperature": 4.2}, {"field": 3.0}]
ANSWER = 0.5097444287639611
TOL = 1e-4

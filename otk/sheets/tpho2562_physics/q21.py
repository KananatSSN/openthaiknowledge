"""Lab part 1.3: at high current I = I0 exp(e(V - I R_s)/(nkT)), so a reading (V, I) off the straight line gives R_s = [V - (nkT/e) ln(I/I0)]/I. Synthetic data: n = 3.0, I0 = 4e-17 A and 0.200 A at 3.00 V give 0.970 ohm. Adapted: the high-current reading and the fitted n and I0 vary; returns ohms at T = 300 K."""

from math import log


def solve(volts=3.0, amps=0.2, ideality=3.0, saturation=4e-17):
    from otk.sheets.tpho2562_physics._shared import E, K_B

    return (volts - ideality * K_B * 300 / E * log(amps / saturation)) / amps


def check(volts=3.0, amps=0.2, ideality=3.0, saturation=4e-17):
    from math import exp

    from otk.sheets.tpho2562_physics._shared import E, K_B, bisect

    # the R_s for which equation (2) returns the measured current
    def gap(rs):
        return saturation * exp(E * (volts - amps * rs) / (ideality * K_B * 300)) - amps

    return bisect(gap, -10.0, 1e3)


PARAMS = {"volts": 3.0, "amps": 0.2, "ideality": 3.0, "saturation": 4e-17}
VARIANTS = [{"volts": 3.2}, {"amps": 0.3}, {"ideality": 2.8}]
ANSWER = 0.969974321961804
TOL = 1e-6

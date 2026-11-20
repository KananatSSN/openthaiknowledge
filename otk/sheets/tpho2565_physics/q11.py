"""Theory 2 k): only the isothermal magnetisation at T_i exchanges heat, Q/N = T_i [S(B_L) - S(B_H)]/N: 2.5e-24 J at 1 K for B_L = 1.85 mT and B_H = 1 T (the solution rounds to 3e-24 J). Adapted: T_i (K), B_H (T) and B_L (mT) vary; returns 1e-24 J."""


def solve(start=1.0, high=1.0, low=1.855):
    from otk.sheets.tpho2565_physics import q07
    from otk.sheets.tpho2565_physics._shared import BOLTZMANN

    drop = q07.solve(field=low * 1e-3, temperature=start) - q07.solve(field=high, temperature=start)
    return start * BOLTZMANN * drop * 1e24


def check(start=1.0, high=1.0, low=1.855, steps=4000):
    from math import tanh

    from otk.sheets.tpho2565_physics._shared import BOHR, BOLTZMANN

    # at fixed T the heat released as the field rises is the integral of B dM
    q, db = 0.0, (high - low * 1e-3) / steps
    for i in range(steps):
        b0 = low * 1e-3 + i * db
        b1 = b0 + db
        m0 = BOHR * tanh(BOHR * b0 / (BOLTZMANN * start))
        m1 = BOHR * tanh(BOHR * b1 / (BOLTZMANN * start))
        q += (b0 + b1) / 2 * (m1 - m0)
    return q * 1e24


PARAMS = {"start": 1.0, "high": 1.0, "low": 1.855}
VARIANTS = [{"start": 0.5}, {"high": 2.0}, {"low": 10.0}]
ANSWER = 2.5309472518762943
TOL = 1e-4

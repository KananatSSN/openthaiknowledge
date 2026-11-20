"""Theory 1.2.4: with V_B = x V_A, e = (x - 1)(Delta p)/(5 p_A (x - 1) + 3 Delta p) rises toward Delta p/(5 p_A) = (1 - T_min/T_A)/5 = 5% as x grows. Adapted: T_A and T_min vary; returns the limiting efficiency in percent."""


def solve(hot=400.0, cold=300.0):
    return 100 * (1 - cold / hot) / 5


def check(hot=400.0, cold=300.0):
    # Integrate the cycle for ever larger B and extrapolate e(x) = e_inf - c/x.
    from otk.sheets.tpho2560_physics._shared import cycle

    w1, q1 = cycle(10.0, 0.4, 1e3, hot, cold, steps=4000)
    w2, q2 = cycle(10.0, 0.4, 2e3, hot, cold, steps=4000)
    e1, e2 = w1 / q1, w2 / q2
    return 100 * (2 * e2 - e1)


PARAMS = {"hot": 400.0, "cold": 300.0}
VARIANTS = [{"cold": 200.0}, {"hot": 600.0}, {"cold": 350.0}]
ANSWER = 5.0
TOL = 1e-5

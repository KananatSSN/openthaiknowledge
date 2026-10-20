"""Theory 3.10: balancing P_grav = alpha G M rho/R against n k_B T + K n^(5/3) (K = 2.4e-38) gives k_B T = C n^(1/3) - K n^(2/3) for a cloud of mass M; the lightest cloud that reaches 1e7 K does so where P_deg = P_ideal, at n = (k_B T/K)^(3/2) = 4.36e32 m^-3. Adapted: the ignition temperature (1e6 K) varies; returns atoms per cubic metre."""


def solve(temperature=10.0):
    from otk.sheets.tpho2562_physics._shared import K_B

    return (K_B * temperature * 1e6 / 2.4e-38) ** 1.5


def check(temperature=10.0):
    from math import exp, log

    from otk.sheets.tpho2562_physics._shared import K_B, golden_min

    # the mass needed grows as (k_B T n^(-1/3) + K n^(1/3))^(3/2): minimise over n
    kt = K_B * temperature * 1e6

    def need(log_n):
        n = exp(log_n)
        return kt * n ** (-1 / 3) + 2.4e-38 * n ** (1 / 3)

    return exp(golden_min(need, log(1e20), log(1e40)))


PARAMS = {"temperature": 10.0}
VARIANTS = [{"temperature": 5.0}, {"temperature": 20.0}, {"temperature": 15.0}]
ANSWER = 4.360153380329642e+32
TOL = 1e-6

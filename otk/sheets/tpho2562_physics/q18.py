"""Theory 3.11: with rho = n m_p and R = (3M/(4 pi n m_p))^(1/3), P_grav = alpha G (4 pi/3)^(1/3) m_p^(4/3) M^(2/3) n^(4/3); the cloud just reaches T when its highest temperature, C^2/(4K) at n^(1/3) = C/(2K), equals T, so alpha G (4 pi/3)^(1/3) m_p^(4/3) M^(2/3) = 2 sqrt(K k_B T) and M = 2.0e29 kg (about 0.1 solar mass) for 1e7 K and alpha = 1/2. Adapted: the ignition temperature (1e6 K) and alpha vary; returns kilograms."""

from math import pi, sqrt


def solve(temperature=10.0, alpha=0.5):
    from otk.sheets.tpho2562_physics._shared import G, K_B, M_P

    c = 2 * sqrt(2.4e-38 * K_B * temperature * 1e6)
    return (c / (alpha * G * (4 * pi / 3) ** (1 / 3) * M_P ** (4 / 3))) ** 1.5


def check(temperature=10.0, alpha=0.5):
    from math import exp, log

    from otk.sheets.tpho2562_physics._shared import G, K_B, M_P, bisect, golden_min

    def hottest(mass):
        # the cloud's highest k_B T as it contracts (n rising), found numerically
        c = alpha * G * (4 * pi / 3) ** (1 / 3) * M_P ** (4 / 3) * mass ** (2 / 3)

        def cold(log_n):
            n = exp(log_n)
            return -(c * n ** (1 / 3) - 2.4e-38 * n ** (2 / 3))

        return -cold(golden_min(cold, log(1e20), log(1e40))) / K_B

    log_m = bisect(lambda x: hottest(exp(x)) - temperature * 1e6, log(1e26), log(1e33), n=100)
    return exp(log_m)


PARAMS = {"temperature": 10.0, "alpha": 0.5}
VARIANTS = [{"temperature": 5.0}, {"alpha": 0.6}, {"temperature": 20.0}]
ANSWER = 1.9975227546680846e+29
TOL = 1e-6

"""Short11: resistors of 1, 2, ..., 100 kilo-ohm in parallel: 1/R = H_100 per kilo-ohm, and with H_n ~ ln n + 0.577 and ln 10 ~ 2.303, R ~ 1000 / 5.183 ~ 193 ohm. Adapted: N = 10^k resistors; returns ohms by that estimate."""


def solve(power=2):
    harmonic = power * 2.303 + 0.577
    return 1000 / harmonic


def check(power=2):
    # Exact harmonic sum against the estimate: they agree to 3 significant
    # figures, which is what the question asks for; return the estimate's
    # value after confirming that.
    n = 10**power
    exact = 1000 / sum(1 / k for k in range(1, n + 1))
    estimate = 1000 / (power * 2.303 + 0.577)
    assert abs(exact - estimate) / exact < 5e-3
    return estimate


PARAMS = {"power": 2}
VARIANTS = [{"power": 3}, {"power": 4}, {"power": 5}]
ANSWER = 192.9384526336099

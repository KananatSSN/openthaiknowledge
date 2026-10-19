"""MC8: simple pendulum wire expands by fraction alpha*deltaT; small-angle period ratio sqrt(1+alpha deltaT), source answer3. Use exact linear-expansion model, not first-order period approximation."""

from math import sqrt, pi


def solve(alpha=0.00002, delta_t=80):
    return sqrt(1 + alpha * delta_t)


def check(alpha=0.00002, delta_t=80):
    # Construct two SHM initial-value solutions and locate each first zero.
    length, g = 2.0, 10.0
    periods = []
    for actual_length in (length, length + length * alpha * delta_t):
        from math import cos

        lo, hi = 0.0, pi
        for _ in range(100):
            time = (lo + hi) / 2
            displacement = cos(sqrt(g / actual_length) * time)
            if displacement > 0:
                lo = time
            else:
                hi = time
        periods.append(4 * (lo + hi) / 2)
    return periods[1] / periods[0]


PARAMS = {"alpha": 2e-05, "delta_t": 80}
VARIANTS = [{"delta_t": 40}, {"alpha": 1e-05}, {"delta_t": 100}]
ANSWER = 1.0007996802557444

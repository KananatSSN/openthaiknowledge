"""Theory 1.3 (b): when T >> T0, I^2 R = sigma A T^q with R = lambda T^p; eliminating T and R = V/I gives I proportional to V^n with n = (q - p)/(q + p), 0.6 for radiation (q = 4) and R proportional to T (p = 1). Adapted: the exponent p of R(T) varies; returns n."""


def solve(power=1.0, radiation=4.0):
    return (radiation - power) / (radiation + power)


def check(power=1.0, radiation=4.0):
    # Two hot steady states: compute V and I for each, then the log slope.
    from math import log

    def state(T):
        R = T**power
        P = T**radiation
        current = (P / R) ** 0.5
        return current * R, current

    v1, i1 = state(1000.0)
    v2, i2 = state(4000.0)
    return log(i2 / i1) / log(v2 / v1)


PARAMS = {"power": 1.0, "radiation": 4.0}
VARIANTS = [{"power": 1.2}, {"power": 1.5}, {"power": 0.8}]
ANSWER = 0.6
TOL = 1e-9

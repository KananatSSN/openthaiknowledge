"""Theory 1.3 figure 1.3: a frictionless piston M in vacuum rests on air (P0 = Mg/A); M' is dropped on it and the pair sinks adiabatically (gamma = 1.4, U = (5/2)nRT) until the volume is halved at the lowest point: (M + M')g h = (5/2)nR(T - T0) with T/T0 = 2^0.4 gives M'/M = 5(2^0.4 - 1) - 1 = 0.6. Adapted: lowest volume V0/k; M'/M = 5(k^0.4 - 1)/(2(1 - 1/k)) - 1."""


def solve(ratio=2.0):
    return 5 * (ratio**0.4 - 1) / (2 * (1 - 1 / ratio)) - 1


def check(ratio=2.0):
    # Work done on the gas along the adiabat, integral of P dV, equals the
    # pistons' loss of potential energy (they stop at the lowest point).
    # Units: P0 = 1, V0 = 1, A = 1 so M g = 1 and x = 1.
    n = 200000
    work = 0.0
    for i in range(n):
        v = 1 - (1 - 1 / ratio) * (i + 0.5) / n
        work += v ** (-1.4) * (1 - 1 / ratio) / n
    drop = 1 - 1 / ratio
    return work / drop - 1


PARAMS = {"ratio": 2.0}
VARIANTS = [{"ratio": 1.5}, {"ratio": 3.0}, {"ratio": 4.0}]
ANSWER = 0.597539553864471
TOL = 1e-6

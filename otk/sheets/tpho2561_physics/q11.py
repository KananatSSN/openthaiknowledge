"""Theory 2.6: matching V = kg m^2 s^-3 A^-1 against f^a h^b e^c with h in kg m^2/s and e in A s gives a = 1, b = 1, c = -1, so V = A f h/e. Adapted: the dimensionless constant A and f (GHz) vary; returns V in microvolts."""

H, E = 6.626069e-34, 1.602177e-19


def solve(factor=0.5, frequency=70.0):
    return factor * frequency * 1e9 * H / E * 1e6


def check(factor=0.5, frequency=70.0):
    # Solve the exponent equations (kg: b = 1; m: 2b = 2; s: -a - b + c = -3;
    # A: c = -1) by substitution, then evaluate.
    b = 1
    c = -1
    a = 3 - b + c
    return factor * (frequency * 1e9) ** a * H**b * E**c * 1e6


PARAMS = {"factor": 0.5, "frequency": 70.0}
VARIANTS = [{"frequency": 10.0}, {"factor": 1.0}, {"factor": 0.25, "frequency": 90.0}]
ANSWER = 144.74831120406796
TOL = 1e-12

"""Lab 1, part 1.1 figure 1.1(a): C and R in series with an AC source of amplitude E0 and angular frequency w; the rms voltage across C is V_C = E0/(sqrt 2 sqrt(1 + w^2 R^2 C^2)). Adapted: numbers for E0, w, R, C; volts rms."""

from math import sqrt


def solve(amplitude=12, omega=1000, resistance=750, capacitance=1e-6):
    x = omega * resistance * capacitance
    return amplitude / sqrt(2) / sqrt(1 + x * x)


def check(amplitude=12, omega=1000, resistance=750, capacitance=1e-6):
    # Complex impedances: the capacitor's share of the source phasor.
    zc = 1 / (1j * omega * capacitance)
    return abs(amplitude * zc / (resistance + zc)) / sqrt(2)


PARAMS = {"amplitude": 12, "omega": 1000, "resistance": 750, "capacitance": 1e-6}
VARIANTS = [{"resistance": 0}, {"omega": 314.159, "resistance": 3300}, {"amplitude": 20, "capacitance": 2.2e-6}]
ANSWER = 6.788225099390855
TOL = 1e-9

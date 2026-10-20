"""Lab 2, part 2.1 figure 2.1: a coil (L, internal r) in series with R across an AC source; the same current flows through both, so V_R/V_L = R/sqrt((omega L)^2 + r^2). Adapted: numbers for R, r, omega, L."""

from math import sqrt


def solve(resistor=150, coil=30, omega=1000, inductance=0.04):
    return resistor / sqrt((omega * inductance) ** 2 + coil**2)


def check(resistor=150, coil=30, omega=1000, inductance=0.04):
    # Phasors: the ratio of the voltage magnitudes across R and across the coil.
    current = 1 / complex(resistor + coil, omega * inductance)
    return abs(current * resistor) / abs(current * complex(coil, omega * inductance))


PARAMS = {"resistor": 150, "coil": 30, "omega": 1000, "inductance": 0.04}
VARIANTS = [{"coil": 0}, {"resistor": 560, "coil": 38, "omega": 314.159, "inductance": 1.2}, {"inductance": 0.5}]
ANSWER = 3.0
TOL = 1e-9

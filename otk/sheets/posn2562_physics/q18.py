"""Short18 circuit: currentE/r downward through idealL andseriesr initiallyDC; switchdisconnectsbattery andconnects topA toR toground. Inductorcurrentcontinuous down E/r, forcing returncurrent UP throughR, so VA=-ER/r relativeground. Plus mark by inductor indicates initial reference only, not fixed post-switchvoltage."""

from fractions import Fraction
import numpy as np


def solve(emf=12, resistor=6, internal=3):
    return -Fraction(emf * resistor, internal)


def check(emf=12, resistor=6, internal=3):
    # UnknowntopA, coilbottomB, voltageacrossL. Frozen inductorcurrent andKCL.
    current = emf / internal
    va, vb, vl = np.linalg.solve(
        [[1 / resistor, 0, 0], [0, 1 / internal, 0], [1, -1, -1]], [-current, current, 0]
    )
    assert abs(va - vb - vl) < 1e-9
    return float(va)


PARAMS = {"emf": 12, "resistor": 6, "internal": 3}
VARIANTS = [{"resistor": 3}, {"emf": 9}, {"internal": 6}]
ANSWER = Fraction(-24, 1)

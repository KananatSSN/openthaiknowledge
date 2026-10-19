"""Part 1,14: (3ohm||6ohm) in series with resistive branch(2.5+1.5)ohm. Across latter: series1uF and4uF, parallel2uF. At steady DC, charge on4uF=6.4uC; parallel cap irrelevant."""

import numpy as np


def solve(voltage=12, r1=3, r2=6, ra=2.5, rb=1.5, c1=1, c2=4, cp=2):
    rp = r1 * r2 / (r1 + r2)
    vc = voltage * (ra + rb) / (rp + ra + rb)
    return c1 * c2 / (c1 + c2) * vc


def check(voltage=12, r1=3, r2=6, ra=2.5, rb=1.5, c1=1, c2=4, cp=2):
    # Nodal KCL in resistors and neutrality of isolated capacitor midpoint.
    # Unknown nodes: upper capacitors, resistor midpoint, capacitor midpoint.
    mat = [[1 / r1 + 1 / r2 + 1 / ra, -1 / ra, 0], [-1 / ra, 1 / ra + 1 / rb, 0], [-c1, 0, c1 + c2]]
    rhs = [voltage / r1 + voltage / r2, 0, 0]
    _, _, midpoint = np.linalg.solve(mat, rhs)
    return float(c2 * midpoint)


PARAMS = {"voltage": 12, "r1": 3, "r2": 6, "ra": 2.5, "rb": 1.5, "c1": 1, "c2": 4, "cp": 2}
VARIANTS = [{"voltage": 24}, {"c1": 2}, {"cp": 10}]
ANSWER = 6.4

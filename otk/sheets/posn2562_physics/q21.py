"""Short21 circuitfigure: C1series(C2||C), requestedC suchthatnetcapacitanceAB equalsC itself. Positive solution C=(-C2+sqrt(C2^2+4C1C2))/2; negativequadraticroot unphysical. All capacitances positive, sameunits."""

from math import sqrt
import numpy as np


def solve(c1=6, c2=3):
    return (sqrt(c2 * c2 + 4 * c1 * c2) - c2) / 2


def check(c1=6, c2=3):
    # Apply1V, solve floatingmidpointneutrality, and requireinputcharge=C.
    lo, hi = 0.0, float(c1)
    for _ in range(100):
        cap = (lo + hi) / 2
        node = float(np.linalg.solve([[c1 + c2 + cap]], [c1])[0])
        charge = c1 * (1 - node)
        if charge > cap:
            lo = cap
        else:
            hi = cap
    return (lo + hi) / 2


PARAMS = {"c1": 6, "c2": 3}
VARIANTS = [{"c1": 10}, {"c2": 6}, {"c1": 12, "c2": 4}]
ANSWER = 3.0

"""Written7 circuit:50V supply series15ohm then10ohm branch containing ideal ammeter. Closing switch adds20ohm||20ohm in parallel with10ohm. Ammeter2A->1.25A. Return signed change after-before=-.75A."""

from fractions import Fraction
import numpy as np


def solve(voltage=50, series=15, branch=10, added=(20, 20)):
    equivalent = 1 / (1 / Fraction(branch) + sum(1 / Fraction(r) for r in added))
    before = Fraction(voltage, series + branch)
    after = voltage * equivalent / (series + equivalent) / branch
    return after - before


def check(voltage=50, series=15, branch=10, added=(20, 20)):
    currents = []
    for resistors in ((branch,), (branch, *added)):
        # Unknown intermediate potential and source current, with KCL.
        node, current = np.linalg.solve(
            [[sum(1 / r for r in resistors), -1], [1, series]], [0, voltage]
        )
        assert current > 0
        currents.append(node / branch)
    return float(currents[1] - currents[0])


PARAMS = {"voltage": 50, "series": 15, "branch": 10, "added": (20, 20)}
VARIANTS = [{"voltage": 100}, {"series": 10}, {"added": (10, 20)}]
ANSWER = Fraction(-3, 4)

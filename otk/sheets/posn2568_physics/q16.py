"""Short16 figure: charging C through R from emf E; i^2 R + (q/C) i = E i, the power the source delivers. Adapted: given R, C, q and i, the emf E = i R + q/C (volts; microfarad and microcoulomb)."""


def solve(resistance=10, capacitance=4, charge=20, current=0.5):
    return current * resistance + charge / capacitance


def check(resistance=10, capacitance=4, charge=20, current=0.5):
    # Power balance: E = (i^2 R + (q/C) i) / i.
    return (current**2 * resistance + charge / capacitance * current) / current


PARAMS = {"resistance": 10, "capacitance": 4, "charge": 20, "current": 0.5}
VARIANTS = [{"current": 2}, {"charge": 0}, {"resistance": 3, "capacitance": 1, "charge": 7, "current": 1}]
ANSWER = 10.0

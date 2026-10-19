"""MC14 circuit figure: C initially acrossR2 of DC dividerE-R1-R2 untilsteady. Switch disconnects divider and puts C across separateR. Initial I_R=E R2/[R(R1+R2)], source answer4; capacitor voltagecontinuous, capacitanceaffects laterdecay but notinitialcurrent."""

from fractions import Fraction
import numpy as np


def solve(emf=12, r1=2, r2=4, load=8, cap=1):
    return Fraction(emf * r2, load * (r1 + r2))


def check(emf=12, r1=2, r2=4, load=8, cap=1):
    # First solve the DC network, then carry stored charge across switching.
    node, current = np.linalg.solve([[1, r1], [1, -r2]], [emf, 0])
    charge = cap * node
    initial_voltage = charge / cap
    assert current > 0
    return float(initial_voltage / load)


PARAMS = {"emf": 12, "r1": 2, "r2": 4, "load": 8, "cap": 1}
VARIANTS = [{"r1": 4}, {"load": 4}, {"cap": 3}]
ANSWER = Fraction(1, 1)

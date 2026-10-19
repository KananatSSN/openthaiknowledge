"""MC13 circuit figure: leftbattery positiveatTOP, rightbattery positiveatBOTTOM. Eachouterbranch has equal resistorR, middle branchr. Equal EMFs yieldzero middle current by symmetry; varying left/right EMFs gives downward current(EL-ER)/(R+2r). The sources drive opposite middle currents, not parallel aiding supplies."""

from fractions import Fraction
import numpy as np


def solve(left_emf=10, right_emf=10, outer=5, middle=2):
    return Fraction(left_emf - right_emf, outer + 2 * middle)


def check(left_emf=10, right_emf=10, outer=5, middle=2):
    # Full node/branch system: nodeV, currentleft, currentmiddle,currentright.
    matrix = [[1, outer, 0, 0], [1, 0, 0, outer], [1, 0, -middle, 0], [0, 1, -1, 1]]
    voltage, il, im, ir = np.linalg.solve(matrix, [left_emf, -right_emf, 0, 0])
    assert abs(il + ir - im) < 1e-10
    return float(im)


PARAMS = {"left_emf": 10, "right_emf": 10, "outer": 5, "middle": 2}
VARIANTS = [{"left_emf": 20}, {"right_emf": 15}, {"left_emf": 12, "right_emf": 6, "outer": 10}]
ANSWER = Fraction(0, 1)

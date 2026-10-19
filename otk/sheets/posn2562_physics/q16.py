"""Short16 figure: monatomic idealgas, frictionless massless piston, constant external atmosphericpressure, laterally insulatedcylinder. Slow heatQ produces isobaric expansion: deltaT=2Q/(5nR). Original symbolic constants represented by a numerical instance."""

from fractions import Fraction
import numpy as np


def solve(heat=100, moles=2, gas_constant=5):
    return Fraction(2 * heat, 5 * moles * gas_constant)


def check(heat=100, moles=2, gas_constant=5):
    # Independently solve first law and PV=nRT at fixed external pressure.
    pressure = 100.0
    dt, dv = np.linalg.solve(
        [[1.5 * moles * gas_constant, pressure], [-moles * gas_constant, pressure]], [heat, 0]
    )
    assert dv > 0
    return float(dt)


PARAMS = {"heat": 100, "moles": 2, "gas_constant": 5}
VARIANTS = [{"heat": 200}, {"moles": 1}, {"gas_constant": 8}]
ANSWER = Fraction(4, 1)

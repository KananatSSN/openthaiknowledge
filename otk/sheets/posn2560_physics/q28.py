"""Part2,8: open cylinder radius1m, outgoing volume rate8pi/100 m³/s; surface speed8cm/s downward. qcoef denotes coefficient of pi in flow in m³/s."""

from fractions import Fraction
from math import pi


def solve(q_num=8, q_den=100, radius=1):
    return Fraction(100 * q_num, q_den * radius**2)


def check(q_num=8, q_den=100, radius=1):
    dt = 0.125
    initial_height = 2.0
    volume = pi * radius * radius * initial_height
    volume -= q_num / q_den * pi * dt
    final_height = volume / (pi * radius * radius)
    return (initial_height - final_height) / dt * 100


PARAMS = {"q_num": 8, "q_den": 100, "radius": 1}
VARIANTS = [{"radius": 2}, {"q_num": 4}, {"q_den": 200}]
ANSWER = Fraction(8, 1)

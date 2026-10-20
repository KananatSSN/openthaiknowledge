"""Theory 3.2.1 figure: string cut, wedge A (with C, M = m_A + m_C) free on the smooth floor: a_A = m g sin(theta) cos(theta)/(M + m sin^2(theta)) = 1.40 m/s^2 for the paper's masses. Adapted: masses vary; g = 9.80."""

from math import sqrt


def solve(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    c = sqrt(1 - sine * sine)
    big = wedge + pulley
    return block * g * sine * c / (big + block * sine * sine)


def check(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    from otk.sheets.tpho2551_physics._wedge import lagrange

    return lagrange(wedge + pulley, block, 0.0, sine, g)[0]


PARAMS = {"wedge": 10.0, "block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"wedge": 4.0}, {"block": 8.0, "pulley": 1.0}, {"sine": 0.8}]
ANSWER = 1.4
TOL = 1e-12

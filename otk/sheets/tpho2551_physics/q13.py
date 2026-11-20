"""Theory 3.3.4: string intact and wedge free; the normal force between B and A is N = m (g cos(theta) - a_A sin(theta)) = 28.8 N for the paper's masses. Adapted: masses vary; newtons with g = 9.80."""

from math import sqrt


def solve(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    from otk.sheets.tpho2551_physics._newton import intact

    return intact(wedge, block, pulley, sine, g)[3]


def check(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    # Normal force from the block's perpendicular equation with the
    # Lagrangian's wedge acceleration.
    from otk.sheets.tpho2551_physics._wedge import lagrange

    a_wedge = lagrange(wedge + pulley, block, pulley / 2, sine, g)[0]
    return block * (g * sqrt(1 - sine * sine) - a_wedge * sine)


PARAMS = {"wedge": 10.0, "block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"wedge": 4.0}, {"block": 8.0, "pulley": 1.0}, {"sine": 0.8}]
ANSWER = 28.77064220183487
TOL = 1e-9

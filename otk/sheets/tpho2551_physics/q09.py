"""Theory 3.1.1: with the wedge held, the string tension is T = (m_C/2) a = 4.70 N for the paper's masses. Adapted: masses vary; newtons with g = 9.80."""


def solve(block=4.0, pulley=2.0, sine=0.6, g=9.8):
    return pulley / 2 * block * g * sine / (block + pulley / 2)


def check(block=4.0, pulley=2.0, sine=0.6, g=9.8):
    # The block's own equation: T = m_B (g sin(theta) - a), with a from energy.
    v2 = 2 * block * g * sine / (block + 0.5 * pulley)
    return block * (g * sine - v2 / 2)


PARAMS = {"block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"pulley": 6.0}, {"block": 1.5}, {"sine": 0.8}]
ANSWER = 4.704
TOL = 1e-12

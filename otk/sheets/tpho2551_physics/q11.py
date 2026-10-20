"""Theory 3.2.2: string cut, the block's acceleration seen from A is (M + m) g sin(theta)/(M + m sin^2(theta)) = 7.00 m/s^2 for the paper's masses (M = m_A + m_C). Adapted: masses vary; g = 9.80."""


def solve(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    big = wedge + pulley
    return (big + block) * g * sine / (big + block * sine * sine)


def check(wedge=10.0, block=4.0, pulley=2.0, sine=0.6, g=9.8):
    from otk.sheets.tpho2551_physics._wedge import lagrange

    return lagrange(wedge + pulley, block, 0.0, sine, g)[1]


PARAMS = {"wedge": 10.0, "block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"wedge": 4.0}, {"block": 8.0, "pulley": 1.0}, {"sine": 0.8}]
ANSWER = 7.0
TOL = 1e-12

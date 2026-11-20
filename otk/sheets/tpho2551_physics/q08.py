"""Theory 3.1.2 figure: wedge A held still; block B (m_B) slides down the smooth face (sin theta = 0.600) pulling a string wound on pulley C (disc, mass m_C): m_B g sin(theta) - T = m_B a, T = (m_C/2) a, so a = m_B g sin(theta)/(m_B + m_C/2) = 4.70 m/s^2 for m_B = 4.00 kg, m_C = 2.00 kg. Adapted: masses vary; g = 9.80."""


def solve(block=4.0, pulley=2.0, sine=0.6, g=9.8):
    return block * g * sine / (block + pulley / 2)


def check(block=4.0, pulley=2.0, sine=0.6, g=9.8):
    # Energy: after B slides s, (1/2)(m_B + I/R^2) v^2 = m_B g s sin(theta),
    # and a = v^2/(2s).
    s = 1.0
    v2 = 2 * block * g * s * sine / (block + 0.5 * pulley)
    return v2 / (2 * s)


PARAMS = {"block": 4.0, "pulley": 2.0, "sine": 0.6, "g": 9.8}
VARIANTS = [{"pulley": 6.0}, {"block": 1.5}, {"sine": 0.8}]
ANSWER = 4.704
TOL = 1e-12

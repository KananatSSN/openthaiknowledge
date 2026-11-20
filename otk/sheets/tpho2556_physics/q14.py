"""Theory 2 (g): with U = PV/(gamma - 1), energy balance gives P V_B/(gamma - 1)(1 - T_A/T_B) = P V_B (T_A/T_B - 1/2), so T_B/T_A = 2 gamma/(gamma + 1); 7/6 for gamma = 1.4. Adapted: T_A (K) and gamma vary; returns T_B in kelvin."""


def solve(temp=300.0, gamma=1.4):
    return temp * 2 * gamma / (gamma + 1)


def check(temp=300.0, gamma=1.4):
    from otk.sheets.tpho2556_physics._valve import transfer

    return transfer(5.0, 50e-4, 2000.0, gamma, temp)[2]


PARAMS = {"temp": 300.0, "gamma": 1.4}
VARIANTS = [{"gamma": 5 / 3}, {"temp": 450.0}, {"gamma": 1.3, "temp": 250.0}]
ANSWER = 350.0
TOL = 1e-6

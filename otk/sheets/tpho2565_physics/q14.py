"""Theory 3 e): adiabatically P is proportional to T^(gamma/(gamma - 1)), so P1 = P0 [1 + (gamma - 1) M^2/2]^(-gamma/(gamma - 1)). Adapted: P0 (kPa), M and gamma vary; returns kPa."""


def solve(pressure=200.0, mach=0.8, gamma=1.4):
    return pressure * (1 + (gamma - 1) * mach**2 / 2) ** (-gamma / (gamma - 1))


def check(pressure=200.0, mach=0.8, gamma=1.4):
    from otk.sheets.tpho2565_physics import q13

    # P/rho^gamma constant with P proportional to rho T: P1/P0 = (rho1/rho0)(T1/T0)
    ratio = q13.check(start=300.0, mach=mach, gamma=gamma) / 300.0
    return pressure * ratio ** (1 / (gamma - 1)) * ratio


PARAMS = {"pressure": 200.0, "mach": 0.8, "gamma": 1.4}
VARIANTS = [{"mach": 1.0}, {"gamma": 5 / 3}, {"mach": 0.5, "pressure": 120.0}]
ANSWER = 131.20432367179498
TOL = 1e-9

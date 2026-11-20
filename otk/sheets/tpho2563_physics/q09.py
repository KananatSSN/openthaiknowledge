"""Theory 2.3: with T proportional to p^(2/7), dT/dz = (2T/7p) dp/dz and dp/dz = -rho g = -p mu g/(RT), so the dry lapse rate is alpha = 2 g mu/(7R) = 9.78 K/km for air (mu = 29.0 g/mol). Adapted: the molar mass (g/mol) and g vary; returns K/km with R = 8.31."""


def solve(molar=29.0, gravity=9.81):
    return 2 * gravity * molar * 1e-3 / (7 * 8.31) * 1e3


def check(molar=29.0, gravity=9.81):
    from otk.sheets.tpho2563_physics._shared import adiabatic_climb

    z, t = adiabatic_climb(293.15, 100.0, 80.0, mu=molar * 1e-3, g=gravity)
    return (293.15 - t) / z * 1e3


PARAMS = {"molar": 29.0, "gravity": 9.81}
VARIANTS = [{"molar": 44.0}, {"gravity": 3.71}, {"molar": 28.0, "gravity": 9.78}]
ANSWER = 9.781330582774627
TOL = 1e-6

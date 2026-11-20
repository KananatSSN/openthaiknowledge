"""Theory 2.1-2.3 figure: relative humidity h% means P_vapor = h P_sat/100, and the nitrogen carries the rest of the atmospheric pressure; after cooling to 25 C at 50% the nitrogen's partial pressure is 1.01325e5 - 1.5845e3 = 0.9974e5 Pa. Adapted: the humidity and saturation pressure after cooling vary; returns P'_N2 in kPa."""


def solve(dry=50.0, sat_cool=3.169, atm=101325.0):
    return (atm - dry / 100 * sat_cool * 1e3) / 1e3


def check(dry=50.0, sat_cool=3.169, atm=101325.0):
    # Mass ratio route: the vapour's mass is h% of the saturated mass in the
    # same volume and temperature; convert to a pressure, then subtract.
    R, T, V = 8.31447, 298.15, 1.0
    saturated_moles = sat_cool * 1e3 * V / (R * T)
    vapour_moles = dry / 100 * saturated_moles
    return (atm - vapour_moles * R * T / V) / 1e3


PARAMS = {"dry": 50.0, "sat_cool": 3.169, "atm": 101325.0}
VARIANTS = [{"dry": 40.0}, {"sat_cool": 2.339, "dry": 60.0}, {"dry": 55.0}]
ANSWER = 99.7405
TOL = 1e-9

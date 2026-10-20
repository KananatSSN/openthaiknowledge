"""Theory 2.6 (a): the vapour's moles drop from P_vap V/(RT) = 91.14 to P'_vap V'/(RT') = 47.94, so 43.20 mol = 777.6 g of water condenses (18 g/mol). Adapted: the room volume and both humidities vary; returns the mass in grams."""


def solve(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0, R=8.31447):
    T, Tp = warm + 273.15, cool + 273.15
    pv, pv2 = humid / 100 * sat_warm * 1e3, dry / 100 * sat_cool * 1e3
    volume = (atm - pv2) * T * room / ((atm - pv) * Tp)
    return (pv * volume / (R * T) - pv2 * room / (R * Tp)) * 18.0


def check(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0, R=8.31447):
    from otk.sheets.tpho2559_physics._aircon import balance

    return balance(room, warm, cool, humid, dry, sat_warm, sat_cool, atm=atm)["condensed"]


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "warm": 30.0, "cool": 25.0, "sat_warm": 4.244, "sat_cool": 3.169, "atm": 101325.0, "R": 8.31447}
VARIANTS = [{"room": 60.0}, {"humid": 80.0}, {"dry": 40.0, "room": 90.0}]
ANSWER = 777.7594732158931
TOL = 1e-9

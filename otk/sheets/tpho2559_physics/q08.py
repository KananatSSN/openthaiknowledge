"""Theory 2.4-2.5 (a): the nitrogen's moles are unchanged, P_N2 V/T = P'_N2 V'/T', so the air that ends up filling the 75 m^3 room at 25 C occupied V = P'_N2 T V'/(P_N2 T') = 77.33 m^3 before. Adapted: the room volume and both humidities vary; returns V in m^3."""


def solve(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    pn = atm - humid / 100 * sat_warm * 1e3
    pn2 = atm - dry / 100 * sat_cool * 1e3
    return pn2 * (warm + 273.15) * room / (pn * (cool + 273.15))


def check(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    from otk.sheets.tpho2559_physics._aircon import balance

    return balance(room, warm, cool, humid, dry, sat_warm, sat_cool, atm=atm)["volume"]


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "warm": 30.0, "cool": 25.0, "sat_warm": 4.244, "sat_cool": 3.169, "atm": 101325.0}
VARIANTS = [{"room": 60.0}, {"humid": 80.0}, {"dry": 40.0, "room": 90.0}]
ANSWER = 77.33260733731981
TOL = 1e-9

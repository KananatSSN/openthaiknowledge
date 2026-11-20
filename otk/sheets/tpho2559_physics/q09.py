"""Theory 2.5 (b): the atmosphere pushes the extra air into the room, doing work P_atm (V - V') = 1.01325e5 (77.33 - 75) = 236.1 kJ. Adapted: the room volume and both humidities vary; returns the work in kJ."""


def solve(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    pn = atm - humid / 100 * sat_warm * 1e3
    pn2 = atm - dry / 100 * sat_cool * 1e3
    volume = pn2 * (warm + 273.15) * room / (pn * (cool + 273.15))
    return atm * (volume - room) / 1e3


def check(room=75.0, humid=70.0, dry=50.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    from otk.sheets.tpho2559_physics._aircon import balance

    return balance(room, warm, cool, humid, dry, sat_warm, sat_cool, atm=atm)["work"] / 1e3


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "warm": 30.0, "cool": 25.0, "sat_warm": 4.244, "sat_cool": 3.169, "atm": 101325.0}
VARIANTS = [{"room": 60.0}, {"humid": 80.0}, {"dry": 40.0, "room": 90.0}]
ANSWER = 236.35143845393017
TOL = 1e-9

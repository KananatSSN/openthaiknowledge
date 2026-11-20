"""Theory 2.6 (b): condensing at the 10 C coil releases H(283.15 K) = 57.075 - 0.0439(283.15) = 44.645 kJ/mol, so 43.20 mol give 1929 kJ. Adapted: the room volume, both humidities and the coil temperature vary; returns the heat in kJ."""


def solve(room=75.0, humid=70.0, dry=50.0, coil=10.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0, R=8.31447):
    T, Tp = warm + 273.15, cool + 273.15
    pv, pv2 = humid / 100 * sat_warm * 1e3, dry / 100 * sat_cool * 1e3
    volume = (atm - pv2) * T * room / ((atm - pv) * Tp)
    moles = pv * volume / (R * T) - pv2 * room / (R * Tp)
    return moles * (57.075 - 0.0439 * (coil + 273.15))


def check(room=75.0, humid=70.0, dry=50.0, coil=10.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0, R=8.31447):
    from otk.sheets.tpho2559_physics._aircon import balance

    return balance(room, warm, cool, humid, dry, sat_warm, sat_cool, coil, atm)["latent"] / 1e3


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "coil": 10.0, "warm": 30.0, "cool": 25.0, "sat_warm": 4.244, "sat_cool": 3.169, "atm": 101325.0, "R": 8.31447}
VARIANTS = [{"room": 60.0}, {"coil": 5.0}, {"dry": 40.0, "humid": 80.0}]
ANSWER = 1929.047223348538
TOL = 1e-9

"""Theory 2.7: the heat removed is the cooling of all gas 30 to 25 C (3nR dT for vapour, 5/2 nR dT for nitrogen: 325.0 kJ), of the condensing vapour 25 to 10 C (16.2 kJ), the atmosphere's work (236.1 kJ) and the condensation (1929 kJ): 2506 kJ. Adapted: the room volume and both humidities vary; returns the total in kJ (R = 8.31 in the energies)."""


def solve(room=75.0, humid=70.0, dry=50.0, coil=10.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    R = 8.31447
    T, Tp, Tc = warm + 273.15, cool + 273.15, coil + 273.15
    pv, pv2 = humid / 100 * sat_warm * 1e3, dry / 100 * sat_cool * 1e3
    pn, pn2 = atm - pv, atm - pv2
    volume = pn2 * T * room / (pn * Tp)
    nv, nv2 = pv * volume / (R * T), pv2 * room / (R * Tp)
    nn = pn * volume / (8.31 * T)
    condensed = nv - nv2
    cooling = (3 * nv + 2.5 * nn) * 8.31 * (T - Tp) + 3 * condensed * 8.31 * (Tp - Tc)
    return (cooling + atm * (volume - room) + condensed * (57.075e3 - 43.9 * Tc)) / 1e3


def check(room=75.0, humid=70.0, dry=50.0, coil=10.0, warm=30.0, cool=25.0, sat_warm=4.244, sat_cool=3.169, atm=101325.0):
    from otk.sheets.tpho2559_physics._aircon import balance

    return balance(room, warm, cool, humid, dry, sat_warm, sat_cool, coil, atm)["total"] / 1e3


PARAMS = {"room": 75.0, "humid": 70.0, "dry": 50.0, "coil": 10.0, "warm": 30.0, "cool": 25.0, "sat_warm": 4.244, "sat_cool": 3.169, "atm": 101325.0}
VARIANTS = [{"room": 60.0}, {"coil": 5.0}, {"dry": 40.0, "humid": 80.0}]
ANSWER = 2506.5412002978733
TOL = 5e-3

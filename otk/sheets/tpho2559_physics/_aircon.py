"""Shared mole-counting model for problem 2: a room of volume V' at total pressure P_atm cooled from T (humidity h) to T' (humidity h'); nitrogen keeps its moles, vapour condenses on a coil at T_c. Counts moles directly rather than using the solution's ratios."""

R = 8.31447


def kelvin(celsius):
    return celsius + 273.15


def balance(room=75.0, warm=30.0, cool=25.0, humid=70.0, dry=50.0, sat_warm=4.244, sat_cool=3.169, coil=10.0, atm=101325.0):
    """Dictionary of every quantity the problem asks for, in SI units."""
    T, Tp, Tc = kelvin(warm), kelvin(cool), kelvin(coil)
    vap, vap2 = humid / 100 * sat_warm * 1e3, dry / 100 * sat_cool * 1e3
    nitrogen_after = (atm - vap2) * room / (R * Tp)
    volume = nitrogen_after * R * T / (atm - vap)
    vapour_before = vap * volume / (R * T)
    vapour_after = vap2 * room / (R * Tp)
    condensed = vapour_before - vapour_after
    work = atm * (volume - room)
    latent = (57.075 - 0.0439 * Tc) * 1e3
    q_condense = condensed * latent
    # internal energies: 3 nRT for vapour, 5/2 nRT for nitrogen (R = 8.31 as in the solution)
    r = 8.31
    cool_all = 3 * vapour_before * r * (Tp - T) + 2.5 * nitrogen_after * r * (Tp - T)
    cool_condensed = 3 * condensed * r * (Tc - Tp)
    total = -(cool_all + cool_condensed - work - q_condense)
    return {
        "vapour": (vap, vap2), "nitrogen": (atm - vap, atm - vap2), "volume": volume,
        "work": work, "condensed": condensed * 18.0, "latent": q_condense, "total": total,
    }

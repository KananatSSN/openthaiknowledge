"""Part 1,19: ideal N2 gas, .25*.60*.50 m³, .05atm,27C. Source constants use T=300K, atmosphere101300Pa, R8.31,NA6.02e23. Return actual molecule count, about9.17e22 (nearest offered10^23)."""


def solve(volume=0.075, pressure_atm=0.05, celsius=27):
    return pressure_atm * 101300 * volume / (8.31 * (celsius + 273)) * 6.02e23


def check(volume=0.075, pressure_atm=0.05, celsius=27):
    # Invert ideal-gas pressure in terms of k_B, using a dimensionless count.
    boltzmann = 8.31 / 6.02e23
    lo, hi = 0.0, 1e4
    for _ in range(120):
        scaled = (lo + hi) / 2
        p = scaled * 1e23 * boltzmann * (celsius + 273) / volume
        if p < pressure_atm * 101300:
            lo = scaled
        else:
            hi = scaled
    return (lo + hi) / 2 * 1e23


PARAMS = {"volume": 0.075, "pressure_atm": 0.05, "celsius": 27}
VARIANTS = [{"volume": 0.15}, {"pressure_atm": 0.1}, {"celsius": 127}]
ANSWER = 9.173074608904933e22

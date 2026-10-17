"""Part 1,18: insulated water-oil mixture; final Celsius temperature is factor times original oil Celsius temperature. Ignore vessel heat capacity. Source gives25C."""


def solve(oil_mass=0.075, water_mass=0.250, water_temp=80, oil_c=1400, water_c=4200, factor=3):
    cw = water_mass * water_c
    co = oil_mass * oil_c
    return cw * water_temp / (factor * cw + (factor - 1) * co)


def check(oil_mass=0.075, water_mass=0.250, water_temp=80, oil_c=1400, water_c=4200, factor=3):
    lo, hi = 0.0, water_temp / factor
    for _ in range(100):
        start = (lo + hi) / 2
        final = factor * start
        lost = water_mass * water_c * (water_temp - final)
        gained = oil_mass * oil_c * (final - start)
        if lost > gained:
            lo = start
        else:
            hi = start
    return (lo + hi) / 2


PARAMS = {
    "oil_mass": 0.075,
    "water_mass": 0.25,
    "water_temp": 80,
    "oil_c": 1400,
    "water_c": 4200,
    "factor": 3,
}
VARIANTS = [{"water_temp": 60}, {"factor": 2}, {"oil_mass": 0.15}]
ANSWER = 25.0

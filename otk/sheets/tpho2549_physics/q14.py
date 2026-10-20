"""Lab 2(c): a stone weighs W in air, W_w in water and W_l in the liquid; Archimedes gives the liquid's specific gravity (W - W_l)/(W - W_w). Adapted: synthetic steelyard readings in grams."""


def solve(air=80, water=50, liquid=56):
    return (air - liquid) / (air - water)


def check(air=80, water=50, liquid=56):
    # Stone volume from the water loss, then the liquid's density from its loss.
    volume = (air - water) / 1.0       # cm^3 at 1 g/cm^3
    return (air - liquid) / volume / 1.0


PARAMS = {"air": 80, "water": 50, "liquid": 56}
VARIANTS = [{"liquid": 45}, {"air": 120, "water": 70, "liquid": 80}, {"liquid": 50}]
ANSWER = 0.8
TOL = 1e-12

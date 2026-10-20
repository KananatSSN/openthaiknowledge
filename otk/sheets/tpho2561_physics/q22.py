"""Lab part 4: filling the gaps of a known volume of rice with water from a syringe, the packing density is phi = 1 - V_water/V_rice. Adapted: the rice volume and the water used (ml) vary; returns phi."""


def solve(rice=20.0, water=8.4):
    return 1 - water / rice


def check(rice=20.0, water=8.4):
    # Grain volume by displacement: rice plus the water poured in occupies
    # the bottle's rice mark exactly; the grains fill the rest.
    grains = rice - water
    return grains / rice


PARAMS = {"rice": 20.0, "water": 8.4}
VARIANTS = [{"water": 7.0}, {"rice": 30.0, "water": 12.5}, {"water": 9.5}]
ANSWER = 0.58
TOL = 1e-12

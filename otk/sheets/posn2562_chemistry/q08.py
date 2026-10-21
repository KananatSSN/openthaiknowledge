"""Source MC8: the jump after IE₂ reveals a group-2 metal and MO oxide."""


def solve(ies=(590, 1150, 4920, 6480, 8150, 10500)):
    ratios = [b / a for a, b in zip(ies, ies[1:])]
    valence = ratios.index(max(ratios)) + 1
    assert valence == 2
    # Four source claims: nonconductor, gaseous halide, MO oxide, negative states.
    claims = (False, False, valence == 2, False)
    return claims.index(True)


def check(ies=(590, 1150, 4920, 6480, 8150, 10500)):
    jumps = [b - a for a, b in zip(ies, ies[1:])]
    assert jumps.index(max(jumps)) == 1
    # After losing two electrons, the third comes from a core shell.
    metal_charge = 2
    oxygen_charge = -2
    oxide_ratio = (abs(oxygen_charge), metal_charge)
    return 2 if oxide_ratio == (2, 2) else None


PARAMS = {"ies": (590, 1150, 4920, 6480, 8150, 10500)}
VARIANTS = [
    {"ies": (738, 1451, 7733, 10543, 13630, 18020)},
    {"ies": (550, 1060, 4600, 5900, 7500, 9400)},
    {"ies": (620, 1200, 5000, 6600, 8300, 10700)},
]
ANSWER = solve(**PARAMS)

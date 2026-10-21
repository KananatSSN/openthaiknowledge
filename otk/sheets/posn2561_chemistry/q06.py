"""Source p3, MC6: K < Ca is the one false second-ionization comparison.

IE2 (eV), NIST ASD singly ionized species: Ca 11.871719, Se 21.196,
Br 21.591, Rb 27.28954, K 31.62500. The close Se–Br order is measured,
not inferred from a simplified periodic trend.
"""


IE2_EV = {19: 31.62500, 20: 11.871719, 34: 21.196,
          35: 21.591, 37: 27.28954}


def solve(elements=(19, 20, 34, 35, 37)):
    assert set(elements) == set(IE2_EV)
    false = [index for index in range(4)
             if not IE2_EV[elements[index]] < IE2_EV[elements[index + 1]]]
    assert len(false) == 1
    return false[0]


def check(elements=(19, 20, 34, 35, 37)):
    # Independently use the experimentally established ordering instead of
    # floating-point values: Ca < Se < Br < Rb < K.
    ordered = (20, 34, 35, 37, 19)
    positions = {z: i for i, z in enumerate(ordered)}
    false = [i for i, (left, right) in enumerate(zip(elements, elements[1:]))
             if positions[left] >= positions[right]]
    assert len(false) == 1
    return false[0]


PARAMS = {"elements": (19, 20, 34, 35, 37)}
VARIANTS = [
    {"elements": (20, 19, 34, 35, 37)},
    {"elements": (20, 34, 19, 35, 37)},
    {"elements": (20, 34, 35, 19, 37)},
]
ANSWER = 0

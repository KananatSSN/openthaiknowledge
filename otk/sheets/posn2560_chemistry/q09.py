"""Source p5, MC9: underlines are S in sulfate, Cl in HClO4, and Au in
Na[Au(CN)2], giving (+6,+7,+1), source choice ง. The extracted text loses
the underlines, so this reading comes from the rendered page.

The first sulfate is inside [Co(NH3)4SO4]Cl; its central sulfur oxidation
state depends on SO4 charge, independently of the cobalt oxidation state.
"""


def solve(oxo_oxygen=4, oxo_charge=-2, acid_oxygen=4,
          cyanide_count=2, complex_charge=-1):
    if oxo_oxygen < 1 or acid_oxygen < 1 or cyanide_count < 1:
        raise ValueError("positive ligand counts required")
    first = oxo_charge + 2 * oxo_oxygen
    second = 2 * acid_oxygen - 1
    third = complex_charge + cyanide_count
    return first, second, third


def check(oxo_oxygen=4, oxo_charge=-2, acid_oxygen=4,
          cyanide_count=2, complex_charge=-1):
    # Enumerate integer oxidation states and apply charge conservation to
    # each complete ion or molecule; no closed-form expression is reused.
    def find(total_charge, known_sum):
        matches = [state for state in range(-10, 11)
                   if state + known_sum == total_charge]
        assert len(matches) == 1
        return matches[0]

    return (find(oxo_charge, sum([-2] * oxo_oxygen)),
            find(0, 1 + sum([-2] * acid_oxygen)),
            find(complex_charge, sum([-1] * cyanide_count)))


PARAMS = {"oxo_oxygen": 4, "oxo_charge": -2, "acid_oxygen": 4,
          "cyanide_count": 2, "complex_charge": -1}
VARIANTS = [
    {"oxo_oxygen": 3, "oxo_charge": -1, "acid_oxygen": 3,
     "cyanide_count": 2, "complex_charge": -1},
    {"oxo_oxygen": 4, "oxo_charge": -3, "acid_oxygen": 4,
     "cyanide_count": 6, "complex_charge": -3},
    {"oxo_oxygen": 4, "oxo_charge": -2, "acid_oxygen": 3,
     "cyanide_count": 4, "complex_charge": -2},
]
ANSWER = (6, 7, 1)

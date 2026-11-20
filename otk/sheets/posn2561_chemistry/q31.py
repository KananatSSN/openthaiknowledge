"""Source p8, MC31: both substances must have permanent dipole attractions."""


PAIRS = (
    ("PCl₃", "CO₂"),
    ("NH₃", "O₂"),
    ("CH₄", "SiH₄"),
    ("PH₃", "H₂S"),
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    polar = {"PCl₃", "NH₃", "PH₃", "H₂S"}
    matches = [i for i, option in enumerate(options)
               if all(species in polar for species in PAIRS[option])]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independent geometry/dipole route: CO2, O2, CH4, SiH4 have zero
    # permanent dipole. PH3 and H2S have measured nonzero dipoles.
    dipole_debye = {"PCl₃": 0.97, "CO₂": 0.0, "NH₃": 1.47, "O₂": 0.0,
                    "CH₄": 0.0, "SiH₄": 0.0, "PH₃": 0.58, "H₂S": 0.97}
    possible = [i for i, option in enumerate(options)
                if min(dipole_debye[name] for name in PAIRS[option]) > 0]
    assert len(possible) == 1
    return possible[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3

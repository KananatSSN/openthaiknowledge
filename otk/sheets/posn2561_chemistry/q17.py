"""Source p6, MC17: helium-3 plus deuterium is the fusion reaction."""


REACTIONS = (
    "¹⁰¹₄₃Tc → ¹⁰¹₄₄Ru + ⁰₋₁e",
    "¹⁴₇N + ¹₀n → ¹⁴₆C + ¹₁H",
    "³₂He + ²₁H → ⁴₂He + ¹₁H",
    "²³⁵₉₂U + ¹₀n → ⁹⁰₃₆Kr + ¹⁴⁴₅₆Ba + 2¹₀n",
)
LEFT = (
    ((43, 101),),
    ((7, 14), (0, 1)),
    ((2, 3), (1, 2)),
    ((92, 235), (0, 1)),
)
RIGHT = (
    ((44, 101), (-1, 0)),
    ((6, 14), (1, 1)),
    ((2, 4), (1, 1)),
    ((36, 90), (56, 144), (0, 1), (0, 1)),
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    fusion = []
    for i, option in enumerate(options):
        reactants = LEFT[option]
        products = RIGHT[option]
        if (len(reactants) == 2 and all(0 < z < 5 for z, _ in reactants)
                and any(a > max(mass for _, mass in reactants)
                        for z, a in products if z > 0)):
            fusion.append(i)
    assert len(fusion) == 1
    return fusion[0]


def check(options=(0, 1, 2, 3)):
    # Independently identify the only reaction combining two light charged
    # nuclei; the others are beta decay, neutron exchange and fission.
    candidates = []
    for i, option in enumerate(options):
        reactants = LEFT[option]
        if (len(reactants) == 2 and all(z >= 1 for z, _ in reactants)
                and sum(mass for _, mass in reactants) <= 5):
            candidates.append(i)
    assert len(candidates) == 1
    return candidates[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 2

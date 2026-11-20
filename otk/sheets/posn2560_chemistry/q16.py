"""Source p7, MC16: neutron, deuteron, Ra-226 (choice ก)."""

_PARTICLES = {(1, 0): "n", (1, 1): "p", (2, 1): "d", (4, 2): "alpha"}


def solve(co_mass=59, mn_mass=56, te_mass=130, iodine_mass=130, rn_mass=222):
    # Co(Z=27)+A -> Mn(Z=25)+alpha(Z=2)
    a = _PARTICLES[(mn_mass + 4 - co_mass, 25 + 2 - 27)]
    # Te(Z=52)+B -> I(Z=53)+2n
    b = _PARTICLES[(iodine_mass + 2 - te_mass, 53 - 52)]
    # Rn(Z=86)+alpha -> C+gamma
    return a, b, (rn_mass + 4, 88)


def check(co_mass=59, mn_mass=56, te_mass=130, iodine_mass=130, rn_mass=222):
    particles = (("n", 1, 0), ("p", 1, 1), ("d", 2, 1), ("alpha", 4, 2))
    first = [name for name, mass, charge in particles
             if co_mass + mass == mn_mass + 4 and 27 + charge == 25 + 2]
    second = [name for name, mass, charge in particles
              if te_mass + mass == iodine_mass + 2 and 52 + charge == 53]
    products = [(mass, atomic) for mass in range(210, 231)
                for atomic in (86, 87, 88, 89)
                if rn_mass + 4 == mass and 86 + 2 == atomic]
    assert len(first) == len(second) == len(products) == 1
    return first[0], second[0], products[0]


PARAMS = {"co_mass": 59, "mn_mass": 56, "te_mass": 130,
          "iodine_mass": 130, "rn_mass": 222}
VARIANTS = [
    {"co_mass": 60, "mn_mass": 57, "te_mass": 128,
     "iodine_mass": 128, "rn_mass": 220},
    {"co_mass": 58, "mn_mass": 55, "te_mass": 132,
     "iodine_mass": 132, "rn_mass": 224},
    {"co_mass": 61, "mn_mass": 58, "te_mass": 129,
     "iodine_mass": 129, "rn_mass": 222},
]
ANSWER = ("n", "d", (226, 88))

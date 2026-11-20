"""Acetic acid solution: 900 g acid and 600 g water; acid mole fraction ~31%."""


def solve(molarity=15, volume_l=1, density_g_ml=1.5, order=(0, 1, 2, 3)):
    acid_mol = molarity * volume_l
    total = density_g_ml * volume_l * 1000
    acid_g = acid_mol * 60
    water = total - acid_g
    claims = (
        water == 600,
        round(acid_g / total * 100) == 60,
        round(acid_mol / (water / 1000)) == 25,
        round(acid_mol / (acid_mol + water / 18) * 100) == 69,
    )
    return order.index(claims.index(False))


def check(molarity=15, volume_l=1, density_g_ml=1.5, order=(0, 1, 2, 3)):
    water_g = volume_l * (density_g_ml * 1000 - molarity * 60)
    acid_g = volume_l * molarity * 60
    mol_fraction = (acid_g / 60) / ((acid_g / 60) + (water_g / 18))
    false = (
        water_g != 600,
        acid_g / (water_g + acid_g) != 0.6,
        (acid_g / 60) / (water_g / 1000) != 25,
        abs(mol_fraction - 0.69) > 0.01,
    )
    assert false == (False, False, False, True)
    return order.index(3)


PARAMS = {"molarity": 15, "volume_l": 1, "density_g_ml": 1.5, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"molarity": 15, "volume_l": 1, "density_g_ml": 1.5, "order": (1, 0, 2, 3)},
    {"molarity": 15, "volume_l": 1, "density_g_ml": 1.5, "order": (2, 3, 0, 1)},
    {"molarity": 15, "volume_l": 1, "density_g_ml": 1.5, "order": (3, 1, 2, 0)},
]

ANSWER = solve(**PARAMS)

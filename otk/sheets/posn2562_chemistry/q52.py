"""Convert saturated salt to free base, then divide by base solubility."""


def solve(salt_sol_g_l=1892, sample_l=0.05, base_molar=200, salt_molar=236.5, base_sol_g_l=2.5):
    return round(salt_sol_g_l * sample_l / salt_molar * base_molar / base_sol_g_l, 2)


def check(salt_sol_g_l=1892, sample_l=0.05, base_molar=200, salt_molar=236.5, base_sol_g_l=2.5):
    salt_mass = salt_sol_g_l * sample_l
    molecules = salt_mass / salt_molar
    base_mass = molecules * base_molar
    return round(base_mass / base_sol_g_l, 2)


PARAMS = {
    "salt_sol_g_l": 1892,
    "sample_l": 0.05,
    "base_molar": 200,
    "salt_molar": 236.5,
    "base_sol_g_l": 2.5,
}
VARIANTS = [
    {
        "salt_sol_g_l": 946,
        "sample_l": 0.05,
        "base_molar": 200,
        "salt_molar": 236.5,
        "base_sol_g_l": 2.5,
    },
    {
        "salt_sol_g_l": 1892,
        "sample_l": 0.1,
        "base_molar": 200,
        "salt_molar": 236.5,
        "base_sol_g_l": 2.5,
    },
    {
        "salt_sol_g_l": 1892,
        "sample_l": 0.05,
        "base_molar": 200,
        "salt_molar": 236.5,
        "base_sol_g_l": 5.0,
    },
]

ANSWER = solve(**PARAMS)

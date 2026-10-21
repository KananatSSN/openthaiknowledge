"""Equal freezing depression means equal molality for non-electrolytes."""


def solve(eg_g=124, eg_molar=62, eg_water_g=1500, glucose_water_g=3000, glucose_molar=180):
    return round(
        (eg_g / eg_molar) / (eg_water_g / 1000) * (glucose_water_g / 1000) * glucose_molar, 2
    )


def check(eg_g=124, eg_molar=62, eg_water_g=1500, glucose_water_g=3000, glucose_molar=180):
    target_m = (eg_g / eg_molar) * glucose_water_g / eg_water_g
    return round(target_m * glucose_molar, 2)


PARAMS = {
    "eg_g": 124,
    "eg_molar": 62,
    "eg_water_g": 1500,
    "glucose_water_g": 3000,
    "glucose_molar": 180,
}
VARIANTS = [
    {"eg_g": 62, "eg_molar": 62, "eg_water_g": 1500, "glucose_water_g": 3000, "glucose_molar": 180},
    {
        "eg_g": 186,
        "eg_molar": 62,
        "eg_water_g": 1500,
        "glucose_water_g": 3000,
        "glucose_molar": 180,
    },
    {
        "eg_g": 124,
        "eg_molar": 62,
        "eg_water_g": 3000,
        "glucose_water_g": 3000,
        "glucose_molar": 180,
    },
]

ANSWER = solve(**PARAMS)

"""Source p18, written 6: both formations release heat; |X-Y|=190 kJ."""


def solve(hh=435, oo=500, oh=460, nn=945, nh=390):
    # Enthalpy per mole H2O and per mole NH3 from broken minus formed bonds.
    water = hh + oo / 2 - 2 * oh
    ammonia = nn / 2 + 1.5 * hh - 3 * nh
    water_type = "คายพลังงาน" if water < 0 else "ดูดพลังงาน"
    ammonia_type = "คายพลังงาน" if ammonia < 0 else "ดูดพลังงาน"
    return water_type, ammonia_type, round(abs(water - ammonia), 1)


def check(hh=435, oo=500, oh=460, nn=945, nh=390):
    # Balance to two product moles first: 2H2+O2->2H2O;
    # N2+3H2->2NH3. Divide each reaction enthalpy by two.
    water_pair = 2 * hh + oo - 4 * oh
    ammonia_pair = nn + 3 * hh - 6 * nh
    water = water_pair / 2
    ammonia = ammonia_pair / 2
    return ("คายพลังงาน" if water_pair < 0 else "ดูดพลังงาน",
            "คายพลังงาน" if ammonia_pair < 0 else "ดูดพลังงาน",
            round(abs(water - ammonia), 1))


PARAMS = {"hh": 435, "oo": 500, "oh": 460, "nn": 945, "nh": 390}
VARIANTS = [
    {"hh": 440, "oo": 498, "oh": 463, "nn": 942, "nh": 391},
    {"hh": 430, "oo": 510, "oh": 455, "nn": 940, "nh": 395},
    {"hh": 436, "oo": 490, "oh": 465, "nn": 950, "nh": 385},
]
ANSWER = ("คายพลังงาน", "คายพลังงาน", 190.0)

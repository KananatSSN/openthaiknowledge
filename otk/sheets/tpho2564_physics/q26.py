"""Lab part 1 e): the sag grows with the end mass at slope 4 L^3 g/(E b h^3), so E = 4 L^3 g/(slope b h^3). The solution's 60 cm readings for N = 0 to 11 washers (end mass 0, then 15.2 + 10.4(N - 1) g) give a least-squares slope of 0.1045 cm/g and E = 60.5 GPa; its drawn trend line through all points gives 0.1024 cm/g and 62 GPa. Adapted: the readings vary; returns GPa."""

MASSES = (0.0, 15.2, 25.6, 36.0, 46.4, 56.8, 67.2, 77.6, 88.0, 98.4, 108.8, 119.2)
SAGS = (2.8, 4.3, 5.5, 6.6, 7.7, 8.7, 9.8, 10.9, 12.0, 13.1, 14.2, 15.2)


def solve(masses=MASSES, sags=SAGS, length=60.0):
    from otk.sheets.tpho2564_physics._shared import line
    from otk.sheets.tpho2564_physics.q25 import STRIP

    slope = line([m * 1e-3 for m in masses], [s * 1e-2 for s in sags])[0]
    return 4 * (length * 1e-2) ** 3 * 9.81 / (slope * STRIP["b"] * STRIP["h"] ** 3) / 1e9


def check(masses=MASSES, sags=SAGS, length=60.0):
    from otk.sheets.tpho2564_physics._shared import centred_line
    from otk.sheets.tpho2564_physics.q25 import STRIP

    slope = centred_line(masses, sags)[0] * 1e-2 / 1e-3
    return 4 * (length * 1e-2) ** 3 * 9.81 / (slope * STRIP["b"] * STRIP["h"] ** 3) / 1e9


PARAMS = {"masses": MASSES, "sags": SAGS, "length": 60.0}
VARIANTS = [
    {"sags": (2.9, 4.5, 5.6, 6.7, 7.9, 9.0, 10.1, 11.2, 12.3, 13.3, 14.5, 15.5)},
    {"length": 50.0, "sags": (1.4, 2.2, 2.8, 3.4, 4.0, 4.6, 5.2, 5.8, 6.4, 7.0, 7.6, 8.2)},
    {"masses": MASSES[:9], "sags": SAGS[:9]},
]
ANSWER = 60.525655500586055
TOL = 1e-9

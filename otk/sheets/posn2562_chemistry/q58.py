"""Freezing point depression: Y solution is 0.52 C colder."""


def solve(x_percent=10, y_percent=20, x_molar=200, y_molar=300, kf=1.86):
    x_m = (x_percent / x_molar) / ((100 - x_percent) / 1000)
    y_m = (y_percent / y_molar) / ((100 - y_percent) / 1000)
    return round((y_m - x_m) * kf, 2)


def check(x_percent=10, y_percent=20, x_molar=200, y_molar=300, kf=1.86):
    molal_x = 1000 * x_percent / (x_molar * (100 - x_percent))
    molal_y = 1000 * y_percent / (y_molar * (100 - y_percent))
    return round(kf * molal_y - kf * molal_x, 2)


PARAMS = {"x_percent": 10, "y_percent": 20, "x_molar": 200, "y_molar": 300, "kf": 1.86}
VARIANTS = [
    {"x_percent": 10, "y_percent": 20, "x_molar": 200, "y_molar": 400, "kf": 1.86},
    {"x_percent": 8, "y_percent": 20, "x_molar": 200, "y_molar": 300, "kf": 1.86},
    {"x_percent": 10, "y_percent": 25, "x_molar": 200, "y_molar": 300, "kf": 1.86},
]

ANSWER = solve(**PARAMS)

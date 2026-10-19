"""MC7: molecules in the whole atmosphere: its weight equals sea-level pressure times Earth's surface, so N = 4 pi R^2 P / (g m) ~ 9e43, about 10^44 (answer 2). Returns N."""

from math import exp, pi


def solve(pressure=1e5, mass=5e-26, g=10, radius=6e6):
    return 4 * pi * radius**2 * pressure / (g * mass)


def check(pressure=1e5, mass=5e-26, g=10, radius=6e6):
    # Integrate an isothermal column (scale height H) over height to get the
    # mass per unit area, times the surface; the column mass is P/g for any H.
    height = 8000.0
    n = 20000
    top = 20 * height
    dz = top / n
    surface_density = 0.0
    for k in range(n):
        z = (k + 0.5) * dz
        surface_density += pressure / (g * height) * exp(-z / height) * dz
    surface_density /= 1 - exp(-top / height)
    return 4 * pi * radius**2 * surface_density / mass


PARAMS = {"pressure": 1e5, "mass": 5e-26, "g": 10, "radius": 6e6}
VARIANTS = [{"radius": 3e6}, {"pressure": 9e6, "g": 9, "radius": 6e6, "mass": 7e-26}, {"g": 4}]
TOL = 1e-6
ANSWER = 9.047786842338603e+43

"""Theory III.c: heat in the liquid W = I^2 R with R = a/(sigma b L) and I = D g b h / B; for a = b = 1 cm, L = 10 cm, h = 1 cm, B = 1 T, sigma = 1, D = 1200, g = 9.8: 13.8 W. Watts."""


def solve(gap=0.01, width=0.01, length=0.1, level=0.01, field=1.0, sigma=1.0, density=1200, g=9.8):
    current = density * g * width * level / field
    return current**2 * gap / (sigma * width * length)


def check(gap=0.01, width=0.01, length=0.1, level=0.01, field=1.0, sigma=1.0, density=1200, g=9.8):
    # Current density J = I/(width length) through thickness gap; heat = J^2/sigma x volume.
    current = density * g * width * level / field
    j = current / (width * length)
    return j * j / sigma * (gap * width * length)


PARAMS = {"gap": 0.01, "width": 0.01, "length": 0.1, "level": 0.01, "field": 1.0, "sigma": 1.0, "density": 1200, "g": 9.8}
VARIANTS = [{"level": 0.02}, {"field": 0.5, "sigma": 2.0}, {"length": 0.05, "gap": 0.02}]
ANSWER = 13.829760000000006

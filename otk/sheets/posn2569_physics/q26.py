"""Part2 item 16: 1.8 g of water (0.1 mol) as ideal vapour at 127 C and 1e5 Pa: V = nRT/P = 3.32e-3 m^3 = 3320 cm^3 with R = 8.3."""


def solve(mass=1.8, celsius=127, pressure=1e5, gas=8.3):
    return mass / 18 * gas * (celsius + 273) / pressure * 1e6


def check(mass=1.8, celsius=127, pressure=1e5, gas=8.3):
    avogadro = 6.0e23
    molecules = mass / 18 * avogadro
    return molecules * (gas / avogadro) * (celsius + 273) / pressure * 1e6


PARAMS = {"mass": 1.8, "celsius": 127, "pressure": 1e5, "gas": 8.3}
VARIANTS = [{"mass": 3.6}, {"celsius": 227}, {"pressure": 2e5, "mass": 9}]
ANSWER = 3320.0

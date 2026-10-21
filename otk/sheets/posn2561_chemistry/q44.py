"""Source p10, MC44: acid identity from molarity, mass fraction and density."""

from fractions import Fraction


ACIDS = (("HCl", Fraction(73, 2)), ("HBr", Fraction(81)),
         ("CH₃COOH", Fraction(60)), ("H₃PO₄", Fraction(98)))


def solve(molarity="12.0", mass_percent="75.0", density="1.57"):
    assert Fraction(molarity) > 0 and 0 < Fraction(mass_percent) < 100
    implied_mass = Fraction(density) * 1000 * Fraction(mass_percent) / 100
    implied_mass /= Fraction(molarity)
    distances = [abs(implied_mass - mass) for _, mass in ACIDS]
    answer = min(range(len(ACIDS)), key=lambda index: distances[index])
    assert distances.count(distances[answer]) == 1
    return answer


def check(molarity="12.0", mass_percent="75.0", density="1.57"):
    # Predict mass percent for each candidate's molar mass; compare observations.
    target = Fraction(mass_percent)
    density_g_l = Fraction(density) * 1000
    predicted = [Fraction(molarity) * mass * 100 / density_g_l
                 for _, mass in ACIDS]
    differences = [abs(percent - target) for percent in predicted]
    return min(range(len(ACIDS)), key=lambda index: differences[index])


PARAMS = {"molarity": "12.0", "mass_percent": "75.0", "density": "1.57"}
VARIANTS = [
    {"molarity": "11.9", "mass_percent": "36.5", "density": "1.19"},
    {"molarity": "7.0", "mass_percent": "40.5", "density": "1.40"},
    {"molarity": "10.0", "mass_percent": "60.0", "density": "1.00"},
]
ANSWER = 3

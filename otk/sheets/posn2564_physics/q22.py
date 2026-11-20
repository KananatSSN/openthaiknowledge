"""MC22: scale A puts the ice point at -10 A and the steam point at 150 A; 25 C reads -10 + 160 * 25 / 100 = 30 A (answer 1)."""

from fractions import Fraction


def solve(ice=-10, steam=150, celsius=25):
    return ice + (steam - ice) * celsius / 100


def check(ice=-10, steam=150, celsius=25):
    # Fit reading = m C + c through (0, ice) and (100, steam) by Cramer's rule.
    a11, a12, b1 = Fraction(0), Fraction(1), Fraction(ice)
    a21, a22, b2 = Fraction(100), Fraction(1), Fraction(steam)
    det = a11 * a22 - a12 * a21
    m = (b1 * a22 - a12 * b2) / det
    c = (a11 * b2 - b1 * a21) / det
    return float(m * Fraction(celsius) + c)


PARAMS = {"ice": -10, "steam": 150, "celsius": 25}
VARIANTS = [{"ice": 20, "steam": 220, "celsius": 40}, {"celsius": 75}, {"ice": -40, "steam": 60}]
ANSWER = 30.0

"""Source p9, MC36: Mg required for NH₃ via Mg₃N₂ at a stated yield."""

from fractions import Fraction


def solve(target_ammonia_centiliters=448, nitride_yield_percent=40):
    assert target_ammonia_centiliters > 0
    assert 0 < nitride_yield_percent <= 100
    # 3Mg + N2 -> Mg3N2; Mg3N2 + 6H2O -> 3Mg(OH)2 + 2NH3.
    ammonia_moles = Fraction(target_ammonia_centiliters, 2240)
    magnesium_moles = ammonia_moles * Fraction(3, 2)
    magnesium_grams = magnesium_moles * 24 * 100 / nitride_yield_percent
    return magnesium_grams


def check(target_ammonia_centiliters=448, nitride_yield_percent=40):
    # Independently search tenths of a gram and forward-predict NH3 volume.
    requested = Fraction(target_ammonia_centiliters, 100)
    for tenths in range(1, 1001):
        grams = Fraction(tenths, 10)
        produced_liters = (grams / 24 * Fraction(nitride_yield_percent, 100)
                           * Fraction(2, 3) * Fraction(224, 10))
        if produced_liters == requested:
            return grams
    raise AssertionError("no tenths-of-a-gram solution in the variant range")


PARAMS = {"target_ammonia_centiliters": 448, "nitride_yield_percent": 40}
VARIANTS = [
    {"target_ammonia_centiliters": 224, "nitride_yield_percent": 40},
    {"target_ammonia_centiliters": 448, "nitride_yield_percent": 50},
    {"target_ammonia_centiliters": 672, "nitride_yield_percent": 60},
]
ANSWER = Fraction(18)

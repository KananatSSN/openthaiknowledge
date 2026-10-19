"""MC19: cylinder height20cm, lid area40cm², gas1/83mol; atmospheric100kPa; lid needs240N lift, negligible lid mass. Internal pressure40kPa, volume.0008m³, R8.3 =>T320K. Area is not cylinder volume."""

from fractions import Fraction


def solve(
    height_cm=20,
    area_cm2=40,
    force=240,
    atmosphere_kpa=100,
    moles_num=1,
    moles_den=83,
    gas_constant=8.3,
):
    area = Fraction(area_cm2, 10000)
    height = Fraction(height_cm, 100)
    numerator = (atmosphere_kpa * 1000 * area - force) * height
    return numerator / (Fraction(moles_num, moles_den) * Fraction(str(gas_constant)))


def check(
    height_cm=20,
    area_cm2=40,
    force=240,
    atmosphere_kpa=100,
    moles_num=1,
    moles_den=83,
    gas_constant=8.3,
):
    area = area_cm2 * 1e-4
    volume = area * height_cm / 100
    lo, hi = 0.0, 10000.0
    for _ in range(100):
        temp = (lo + hi) / 2
        inside = (moles_num / moles_den) * gas_constant * temp / volume
        lift = (atmosphere_kpa * 1000 - inside) * area
        if lift > force:
            lo = temp
        else:
            hi = temp
    return (lo + hi) / 2


PARAMS = {
    "height_cm": 20,
    "area_cm2": 40,
    "force": 240,
    "atmosphere_kpa": 100,
    "moles_num": 1,
    "moles_den": 83,
    "gas_constant": 8.3,
}
VARIANTS = [{"force": 160}, {"height_cm": 30}, {"moles_num": 2}]
ANSWER = Fraction(320, 1)

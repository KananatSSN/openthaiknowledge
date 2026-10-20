"""Theory 1.1 figure: a rectangular tank (5.00 L, 1.40 mol of gas at 300 K, total mass 2.50 kg) on a smooth floor in vacuum springs a 4.00 mm^2 leak at the middle of its left wall; the unbalanced pressure force P A = (nRT/V) A gives a = 1.12 m/s^2. Adapted: numbers vary; m/s^2 with R = 8.31."""


def solve(moles=1.4, temperature=300, litres=5.0, area_mm2=4.0, mass=2.5, gas=8.31):
    pressure = moles * gas * temperature / (litres * 1e-3)
    return pressure * area_mm2 * 1e-6 / mass


def check(moles=1.4, temperature=300, litres=5.0, area_mm2=4.0, mass=2.5, gas=8.31):
    # Net force as the sum over the four side walls' pressure forces, the left
    # wall missing the hole's area.
    pressure = moles * gas * temperature / (litres * 1e-3)
    wall = 0.01  # any wall area, m^2
    left = pressure * (wall - area_mm2 * 1e-6)
    right = pressure * wall
    return (right - left) / mass


PARAMS = {"moles": 1.4, "temperature": 300, "litres": 5.0, "area_mm2": 4.0, "mass": 2.5, "gas": 8.31}
VARIANTS = [{"moles": 2.0}, {"litres": 10.0, "area_mm2": 2.0}, {"mass": 5.0, "temperature": 350}]
ANSWER = 1.116864
TOL = 1e-9

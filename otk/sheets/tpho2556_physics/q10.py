"""Theory 2 (b): B's piston stops where the spring holds the gas pressure, k x = (mg/a) a, so V_B = a x = mga/k. Adapted: m (kg), a (cm^2) and k vary; returns V_B in cm^3 with g = 9.8."""


def solve(mass=5.0, area=50.0, spring=2000.0, g=9.8):
    return mass * g / spring * 100 * area      # x in cm times a in cm^2


def check(mass=5.0, area=50.0, spring=2000.0, g=9.8):
    from otk.sheets.tpho2556_physics._valve import transfer

    return transfer(mass, area * 1e-4, spring, 1.4, 300.0, g, parcels=200)[1] * 1e6


PARAMS = {"mass": 5.0, "area": 50.0, "spring": 2000.0, "g": 9.8}
VARIANTS = [{"spring": 500.0}, {"mass": 2.0, "area": 80.0}, {"area": 20.0}]
ANSWER = 122.50000000000001
TOL = 1e-9

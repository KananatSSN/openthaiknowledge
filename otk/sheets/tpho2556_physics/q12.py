"""Theory 2 (e): B's gas compresses the spring to x = mg/k, doing work (1/2) k x^2 = m^2 g^2/(2k) on the piston. Adapted: m (kg) and k vary; returns the work in joules with g = 9.8."""


def solve(mass=5.0, spring=2000.0, g=9.8):
    return (mass * g) ** 2 / (2 * spring)


def check(mass=5.0, spring=2000.0, g=9.8):
    from otk.sheets.tpho2556_physics._valve import transfer

    return transfer(mass, 50e-4, spring, 1.4, 300.0, g, parcels=500)[4]


PARAMS = {"mass": 5.0, "spring": 2000.0, "g": 9.8}
VARIANTS = [{"mass": 2.0}, {"spring": 500.0}, {"mass": 10.0, "spring": 5000.0}]
ANSWER = 0.60025
TOL = 1e-9

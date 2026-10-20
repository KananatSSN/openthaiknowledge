"""Theory 2 (f): the moved gas gains internal energy W_A - W_B = m^2 g^2/(2 gamma k). Adapted: m (kg), k and gamma vary; returns the change in joules with g = 9.8."""


def solve(mass=5.0, spring=2000.0, gamma=1.4, g=9.8):
    return (mass * g) ** 2 / (2 * gamma * spring)


def check(mass=5.0, spring=2000.0, gamma=1.4, g=9.8):
    from otk.sheets.tpho2556_physics._valve import transfer

    return transfer(mass, 50e-4, spring, gamma, 300.0, g)[5]


PARAMS = {"mass": 5.0, "spring": 2000.0, "gamma": 1.4, "g": 9.8}
VARIANTS = [{"gamma": 5 / 3}, {"mass": 2.0}, {"spring": 500.0, "gamma": 1.3}]
ANSWER = 0.42875
TOL = 1e-6

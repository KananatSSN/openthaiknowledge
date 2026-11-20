"""Theory 2.2 figure 2.2: a rod of length l spinning at omega about one end in a perpendicular B has V_a - V_b = (1/2) B omega l^2. Adapted: numbers; volts."""


def solve(field=0.5, omega=20, length=0.3):
    return field * omega * length**2 / 2


def check(field=0.5, omega=20, length=0.3, steps=1e-6):
    # Faraday: the flux swept by the rod in a short time.
    swept = 0.5 * length**2 * omega * steps
    return field * swept / steps


PARAMS = {"field": 0.5, "omega": 20, "length": 0.3}
VARIANTS = [{"omega": 100}, {"field": 1.5, "length": 0.1}, {"length": 2}]
ANSWER = 0.44999999999999996
TOL = 1e-9

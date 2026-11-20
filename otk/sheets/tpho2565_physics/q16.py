"""Theory 3 g): f(beta) peaks at beta* = (2/(gamma + 1))^(gamma/(gamma - 1)), so the flow is largest (Mach 1 at the outlet) when P1* = P0 (2/(gamma + 1))^(gamma/(gamma - 1)), 0.528 P0 for air. Adapted: P0 (kPa) and gamma vary; returns kPa."""


def solve(pressure=200.0, gamma=1.4):
    return pressure * (2 / (gamma + 1)) ** (gamma / (gamma - 1))


def check(pressure=200.0, gamma=1.4):
    from otk.sheets.tpho2565_physics._shared import golden_min
    from otk.sheets.tpho2565_physics.q15 import flow_factor

    return pressure * golden_min(lambda b: -flow_factor(b, gamma), 1e-6, 1.0)


PARAMS = {"pressure": 200.0, "gamma": 1.4}
VARIANTS = [{"gamma": 5 / 3}, {"pressure": 101.3}, {"gamma": 1.3}]
ANSWER = 105.65635754343484
TOL = 1e-6

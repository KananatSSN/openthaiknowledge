"""Theory 2 (b): resting dust dm sticks to the block at speed v; momentum m v = (m + dm) v' gives an energy change -(1/2) m dm v^2/(m + dm), about -(1/2) dm v^2. Adapted: dm (mg) and v vary; returns the loss in microjoules."""


def solve(dust=2.0, speed=0.8):
    return 0.5 * dust * 1e-6 * speed**2 * 1e6


def check(dust=2.0, speed=0.8, mass=0.2):
    # Exact sticking collision with the dust scaled down a thousandfold,
    # then scaled back up: the first-order loss.
    small = dust * 1e-6 * 1e-3
    after = mass * speed / (mass + small)
    loss = 0.5 * mass * speed**2 - 0.5 * (mass + small) * after**2
    return loss * 1e3 * 1e6


PARAMS = {"dust": 2.0, "speed": 0.8}
VARIANTS = [{"dust": 10.0}, {"speed": 1.5}, {"dust": 0.5, "speed": 0.3}]
ANSWER = 0.6400000000000001
TOL = 1e-6

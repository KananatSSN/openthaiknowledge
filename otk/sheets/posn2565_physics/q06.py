"""MC6 figure: emf E in series with R and C while charging; at the instant C holds q and the current is I, the source delivers power E I = q I / C + R I^2 (answer 3). SI units."""


def solve(charge=6e-6, capacitance=2e-6, current=0.5, resistance=4):
    return charge * current / capacitance + resistance * current**2


def check(charge=6e-6, capacitance=2e-6, current=0.5, resistance=4):
    # Find the emf from the loop rule, then power = E I; also confirm the
    # energy split: d/dt(q^2/2C) + I^2 R.
    emf = current * resistance + charge / capacitance
    dt = 1e-12
    stored_rate = ((charge + current * dt) ** 2 - charge**2) / (2 * capacitance * dt)
    assert abs(emf * current - stored_rate - current**2 * resistance) < 1e-3 * emf * current
    return emf * current


PARAMS = {"charge": 6e-6, "capacitance": 2e-6, "current": 0.5, "resistance": 4}
VARIANTS = [{"current": 2}, {"charge": 1e-5, "capacitance": 5e-6}, {"resistance": 10, "current": 0.1}]
ANSWER = 2.5

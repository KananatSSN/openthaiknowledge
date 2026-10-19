"""MC6 figure: light ball mass m volume V released from the bottom of water depth h; no drag. Treated as a point: net upward force rho V g - m g until the surface, then free flight. Height above the surface (rho V / m - 1) h (answer 1). Units: grams, cm^3, cm; water 1 g/cm^3."""


def solve(mass=2, volume=10, depth=10, density=1):
    return (density * volume / mass - 1) * depth


def check(mass=2, volume=10, depth=10, density=1):
    # March the motion in time: buoyant phase, then ballistic phase; g cancels.
    g, dt = 980.0, 1e-6
    y = v = 0.0
    while y < depth:
        v += (density * volume - mass) / mass * g * dt
        y += v * dt
    # Exact correction for the overshoot of the last step, then rise under g.
    v2 = v * v - 2 * (density * volume - mass) / mass * g * (y - depth)
    return v2 / (2 * g)


PARAMS = {"mass": 2, "volume": 10, "depth": 10, "density": 1}
VARIANTS = [{"mass": 5}, {"mass": 4, "depth": 15}, {"volume": 20, "mass": 8}]
TOL = 1e-3
ANSWER = 40.0

"""Part 1, 4: fully submerged buoyant sphere; upward speed, linear water drag C v."""


def solve(rho=1000, volume=0.001, mass=0.2, drag=2, g=9.8):
    if rho * volume <= mass or drag <= 0:
        raise ValueError("requires positive upward buoyancy and drag")
    return (rho * volume - mass) * g / drag


def check(rho=1000, volume=0.001, mass=0.2, drag=2, g=9.8):
    # Root of the original free-body force balance, independently bracketed.
    lo, hi = 0.0, rho * volume * g / drag + 1
    for _ in range(100):
        v = (lo + hi) / 2
        upward = rho * volume * g
        downward = mass * g + drag * v
        if upward > downward:
            lo = v
        else:
            hi = v
    return (lo + hi) / 2


PARAMS = {"rho": 1000, "volume": 0.001, "mass": 0.2, "drag": 2, "g": 9.8}
VARIANTS = [{"mass": 0.5}, {"volume": 0.002}, {"drag": 4}]
ANSWER = 3.9200000000000004

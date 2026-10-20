"""Theory 2(c): the empty, air-filled tank on the bed is pushed up by (Pa + rho g h)A - (Pa + rho g (h - L))A = rho g L A, so it needs mass at least rho L A (40e3 kg for L = 8.0 m, A = 5.0 m^2). Adapted: L and A given; kg."""


def solve(length=8.0, area=5.0, rho=1000.0):
    return rho * length * area


def check(length=8.0, area=5.0, rho=1000.0, g=10.0, depth=14.13, pa=1.013e5):
    # Pressure forces on the open bottom (air at bed pressure) and on the top.
    up = (pa + rho * g * depth) * area
    down = (pa + rho * g * (depth - length)) * area
    return (up - down) / g


PARAMS = {"length": 8.0, "area": 5.0, "rho": 1000.0}
VARIANTS = [{"length": 5}, {"area": 2.5}, {"rho": 1025.0}]
ANSWER = 40000.0
TOL = 1e-12

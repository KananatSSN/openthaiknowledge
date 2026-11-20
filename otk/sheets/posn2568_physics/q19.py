"""Short19 figure: parallel plates of area A, gap d, held at V; one plate pulls the other with F = eps0 A V^2/(2 d^2). Returns F / eps0 in SI units for A in cm^2 and d in mm."""


def solve(area=100, voltage=100, gap=1):
    return area * 1e-4 * voltage**2 / (2 * (gap / 1000) ** 2)


def check(area=100, voltage=100, gap=1):
    # Virtual work at fixed charge: F = -dU/dd with U = Q^2 d/(2 eps0 A)
    # (eps0 = 1), evaluated at the charge Q = A V / d.
    a, d = area * 1e-4, gap / 1000
    q = a * voltage / d
    energy = lambda x: q * q * x / (2 * a)
    h = d * 1e-6
    return (energy(d + h) - energy(d - h)) / (2 * h)


PARAMS = {"area": 100, "voltage": 100, "gap": 1}
VARIANTS = [{"voltage": 300}, {"area": 50, "gap": 2}, {"gap": 0.5}]
TOL = 1e-7
ANSWER = 50000000.0

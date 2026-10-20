"""Theory 3.7: E_Q = -dV_Q/dr = rho r/(3 eps0) - q'/(4 pi eps0 (r0 + r)^2), outward positive. Adapted: q' as the charge of a ball of radius s at density rho; returns E_Q in units of rho/eps0."""


def solve(radius=1.0, point=0.4, source=0.3, size=0.5):
    return point / 3 - size**3 / (3 * (source + point) ** 2)


def check(radius=1.0, point=0.4, source=0.3, size=0.5):
    # Central difference of the 3.5 potential.
    def potential(r):
        return (3 * radius**2 - r * r) / 6 - size**3 / (3 * (source + r))

    h = 1e-5
    return -(potential(point + h) - potential(point - h)) / (2 * h)


PARAMS = {"radius": 1.0, "point": 0.4, "source": 0.3, "size": 0.5}
VARIANTS = [{"point": 0.1}, {"source": 0.8, "size": 0.2}, {"radius": 2.0, "point": 1.5, "source": 1.0}]
ANSWER = 0.048299319727891143
TOL = 1e-6

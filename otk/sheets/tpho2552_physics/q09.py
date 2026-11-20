"""Theory 3.1: two parallel plates of area A with surface charges -sigma and +sigma attract with F = (sigma A)(sigma/(2 eps0)) = sigma^2 A/(2 eps0) (each plate feels only the other's field). Adapted: sigma in microC/m^2 and A in m^2; newtons."""

EPS0 = 8.85e-12


def solve(sigma=20.0, area=0.05):
    s = sigma * 1e-6
    return s * s * area / (2 * EPS0)


def check(sigma=20.0, area=0.05):
    # Energy route: U = (1/2) eps0 E^2 x A with E = sigma/eps0; F = dU/dx.
    s = sigma * 1e-6
    field = s / EPS0

    def energy(gap):
        return 0.5 * EPS0 * field**2 * gap * area

    h = 1e-6
    return (energy(1e-3 + h) - energy(1e-3)) / h


PARAMS = {"sigma": 20.0, "area": 0.05}
VARIANTS = [{"sigma": 5.0}, {"area": 0.2}, {"sigma": 50.0, "area": 0.01}]
ANSWER = 1.1299435028248583
TOL = 1e-6

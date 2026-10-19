"""Part2 item 6 figure: a fire hose of section A sends water out at v; the reaction on the hose is rho A v^2. Newtons, A in cm^2."""


def solve(area=10, speed=20, density=1000):
    return density * area * 1e-4 * speed**2


def check(area=10, speed=20, density=1000, dt=1e-3):
    # Momentum leaving in a short time over that time.
    mass = density * area * 1e-4 * speed * dt
    return mass * speed / dt


PARAMS = {"area": 10, "speed": 20, "density": 1000}
VARIANTS = [{"speed": 10}, {"area": 5, "speed": 30}, {"density": 800}]
ANSWER = 400.0

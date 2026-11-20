"""MC25 figure: a water jet (density rho) enters a U pipe of area A at speed v and leaves reversed; the pipe pushes the wall with 2 rho A v^2 (answer 2). Returns newtons for A in cm^2."""


def solve(density=1000, area=2, speed=5):
    return 2 * density * area * 1e-4 * speed**2


def check(density=1000, area=2, speed=5, dt=1e-3):
    # Momentum budget for the water passing in a short time dt.
    mass = density * area * 1e-4 * speed * dt
    change = mass * (-speed) - mass * speed
    return abs(change) / dt


PARAMS = {"density": 1000, "area": 2, "speed": 5}
VARIANTS = [{"speed": 10}, {"area": 5, "speed": 3}, {"density": 800}]
ANSWER = 10.0

"""MC3: sphere of mass M, volume V falling through a still fluid of density rho with drag beta v; terminal velocity (M - rho V) g / beta (answer 4). kg, litres, water; g = 10."""


def solve(mass=3, volume=1, beta=4, density=1000, g=10):
    return (mass - density * volume / 1000) * g / beta


def check(mass=3, volume=1, beta=4, density=1000, g=10):
    # Step the motion until the speed stops changing.
    v, dt = 0.0, 1e-4
    for _ in range(2000000):
        accel = (mass * g - density * volume / 1000 * g - beta * v) / mass
        v += accel * dt
        if abs(accel) < 1e-12:
            break
    return v


PARAMS = {"mass": 3, "volume": 1, "beta": 4, "density": 1000, "g": 10}
VARIANTS = [{"mass": 5, "beta": 2}, {"volume": 2, "mass": 2.5}, {"beta": 10}]
TOL = 1e-6
ANSWER = 5.0

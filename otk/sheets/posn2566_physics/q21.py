"""Short21 figure: a chain of mass per length lambda lies along OX; a hand sweeps it along OX at constant v, picking links up from rest. Force on the hand = lambda v^2. Newtons."""


def solve(density=0.5, speed=4):
    return density * speed**2


def check(density=0.5, speed=4, dt=1e-4, steps=10000):
    # Momentum of the moving part grows as links join; F = dp/dt averaged.
    moving_length = 0.0
    momentum0 = 0.0
    for _ in range(steps):
        moving_length += speed * dt
    momentum1 = density * moving_length * speed
    return (momentum1 - momentum0) / (dt * steps)


PARAMS = {"density": 0.5, "speed": 4}
VARIANTS = [{"speed": 10}, {"density": 2, "speed": 3}, {"density": 0.1}]
TOL = 1e-9
ANSWER = 8.0

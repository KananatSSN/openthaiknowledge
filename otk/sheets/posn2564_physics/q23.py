"""MC23: thin straight rod, 1 m, 1 kg, centre-of-mass speed 1 m/s, spinning about its centre at 1 rad/s. KE = 1/2 + 1/24 J (answer 4)."""


def solve(mass=1, length=1, speed=1, omega=1):
    return mass * speed**2 / 2 + mass * length**2 * omega**2 / 24


def check(mass=1, length=1, speed=1, omega=1):
    # Sum (1/2) dm |v_cm + omega x r|^2 over 20000 slices; the rod lies along x,
    # spins about z, and its centre moves at an angle to the rod (here along x).
    n = 20000
    total = 0.0
    for k in range(n):
        s = -length / 2 + length * (k + 0.5) / n
        vx, vy = speed, omega * s
        total += mass / n * (vx * vx + vy * vy) / 2
    return total


PARAMS = {"mass": 1, "length": 1, "speed": 1, "omega": 1}
VARIANTS = [{"mass": 2, "length": 3, "speed": 2, "omega": 2}, {"omega": 4}, {"length": 2, "speed": 0.5}]
TOL = 1e-6
ANSWER = 0.5416666666666666

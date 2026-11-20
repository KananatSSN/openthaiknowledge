"""Theory 1.1: v_A = (2 M_B u_B + (M_A - M_B) u_A)/(M_A + M_B). Adapted: numbers for the masses and speeds; m/s."""


def solve(mass_a=2, mass_b=3, speed_a=5, speed_b=1):
    return (2 * mass_b * speed_b + (mass_a - mass_b) * speed_a) / (mass_a + mass_b)


def check(mass_a=2, mass_b=3, speed_a=5, speed_b=1):
    # Solve momentum and kinetic energy directly: the quadratic in v_A has the
    # trivial root u_A and the collision root.
    p = mass_a * speed_a + mass_b * speed_b
    e = mass_a * speed_a**2 + mass_b * speed_b**2
    # v_B = (p - M_A v_A)/M_B ; M_A v_A^2 + (p - M_A v_A)^2/M_B = e
    a = mass_a + mass_a**2 / mass_b
    b = -2 * p * mass_a / mass_b
    c = p * p / mass_b - e
    disc = (b * b - 4 * a * c) ** 0.5
    roots = [(-b + disc) / (2 * a), (-b - disc) / (2 * a)]
    return min(roots, key=lambda r: -abs(r - speed_a))


PARAMS = {"mass_a": 2, "mass_b": 3, "speed_a": 5, "speed_b": 1}
VARIANTS = [{"speed_b": 0}, {"mass_a": 1, "mass_b": 9, "speed_b": -2}, {"mass_a": 5, "mass_b": 1}]
ANSWER = 0.2
TOL = 1e-9

"""Theory 1.1 figure: M_A at u_A hits M_B at u_B elastically on a smooth floor; v_B = (2 M_A u_A + (M_B - M_A) u_B)/(M_A + M_B). Adapted: numbers for the masses and speeds; m/s."""


def solve(mass_a=2, mass_b=3, speed_a=5, speed_b=1):
    return (2 * mass_a * speed_a + (mass_b - mass_a) * speed_b) / (mass_a + mass_b)


def check(mass_a=2, mass_b=3, speed_a=5, speed_b=1):
    # Centre-of-mass frame: velocities reverse there.
    centre = (mass_a * speed_a + mass_b * speed_b) / (mass_a + mass_b)
    return 2 * centre - speed_b


PARAMS = {"mass_a": 2, "mass_b": 3, "speed_a": 5, "speed_b": 1}
VARIANTS = [{"speed_b": 0}, {"mass_a": 3, "mass_b": 3}, {"mass_a": 1, "mass_b": 9, "speed_b": -2}]
ANSWER = 4.2

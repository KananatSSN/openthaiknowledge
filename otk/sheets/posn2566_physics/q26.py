"""Short26 figure: +q (mass m) fired from far away at +Q (mass M) at rest and free; at closest approach D they share a common velocity. KE_m = (k q Q / D)(1 + m/M). Joules, microcoulombs, metres, k = 9e9."""


K = 9e9


def solve(small_charge=1, big_charge=2, distance=0.1, small=1, big=4):
    return K * small_charge * big_charge * 1e-12 / distance * (1 + small / big)


def check(small_charge=1, big_charge=2, distance=0.1, small=1, big=4):
    # Bisect on the launch speed, using momentum to get the shared speed at
    # closest approach and energy to get the separation there.
    u_pot = K * small_charge * big_charge * 1e-12

    def closest(speed):
        v_common = small * speed / (small + big)
        lost = 0.5 * small * speed**2 - 0.5 * (small + big) * v_common**2
        return u_pot / lost

    lo, hi = 1e-9, 1e9
    for _ in range(300):
        mid = (lo + hi) / 2
        if closest(mid) > distance:
            lo = mid
        else:
            hi = mid
    speed = (lo + hi) / 2
    return 0.5 * small * speed * speed


PARAMS = {"small_charge": 1, "big_charge": 2, "distance": 0.1, "small": 1, "big": 4}
VARIANTS = [{"big": 1}, {"small": 2, "big": 2, "distance": 0.5}, {"small_charge": 3, "big": 9}]
TOL = 1e-9
ANSWER = 0.22499999999999995

"""MC10 figure: a limp chain lies folded on the floor: A..B still, then folded back under it from B to C, and C is pulled right. If the fold B moves right at u, C moves at 2u (answer 2). m/s."""


def solve(fold_speed=3):
    return 2 * fold_speed


def check(fold_speed=3, length=10.0, dt=1e-3):
    # Kinematics: the still strand ends at the fold b(t); the moving strand
    # runs from b back to c with the total length fixed. Step c and read b.
    # Length = (b - a) + (c_end distance back): with a at 0 and the moving
    # strand lying beside the still one, still = b, moving = b - c, so
    # still + moving = 2b - c = length. Bisect c's speed so b moves at u.
    def fold_rate(c_speed):
        c0 = -length / 2
        b0 = (length + c0) / 2
        c1 = c0 + c_speed * dt
        b1 = (length + c1) / 2
        return (b1 - b0) / dt

    lo, hi = 0.0, 100.0 * fold_speed + 1
    for _ in range(200):
        mid = (lo + hi) / 2
        if fold_rate(mid) < fold_speed:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"fold_speed": 3}
VARIANTS = [{"fold_speed": 1}, {"fold_speed": 0.5}, {"fold_speed": 7}]
TOL = 1e-9
ANSWER = 6

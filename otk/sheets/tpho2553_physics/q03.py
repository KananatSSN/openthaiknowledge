"""Theory 1.3: l_{n+1}/l_n = (v_n + V_n)/(v_{n+1} + V_{n+1}), so l_n (v_n + V_n) = l0 V0 for every n. Adapted: masses, V0 and l0 vary; returns l2, the distance of the third collision from the wall, in metres."""


def _speeds(big, small, speed, n):
    V, v = speed, 0.0
    for _ in range(n):
        V, v = ((big - small) * V + 2 * small * v) / (big + small), ((small - big) * v + 2 * big * V) / (big + small)
        v = -v  # m returns from the wall
    return V, -v


def solve(big=5, small=1, speed=3, gap=1.4):
    V2, v2 = _speeds(big, small, speed, 2)   # after the second M-m collision
    return gap * speed / (v2 + V2)


def check(big=5, small=1, speed=3, gap=1.4):
    from otk.sheets.tpho2553_physics._wall import collisions

    meetings = collisions(big, small, speed, gap, count=3)
    next(meetings)
    next(meetings)
    distance, _, _ = next(meetings)
    return distance


PARAMS = {"big": 5, "small": 1, "speed": 3, "gap": 1.4}
VARIANTS = [{"big": 10}, {"small": 2, "big": 9}, {"gap": 0.6, "speed": 1}]
ANSWER = 0.663157894736842
TOL = 1e-9

"""Part2 item 15 figure: m and heavy M both move at u toward a wall; M rebounds elastically from the wall, then meets m elastically. For mass ratio k = M/m, m leaves at u (3k - 1)/(k + 1), tending to 3u for m << M. Returns m's final speed for finite k."""


def solve(ratio=1000, speed=2):
    return speed * (3 * ratio - 1) / (ratio + 1)


def check(ratio=1000, speed=2):
    # 1-D elastic collision formula applied after M's rebound.
    m, big = 1.0, float(ratio)
    u1, u2 = speed, -speed
    v1 = ((m - big) * u1 + 2 * big * u2) / (m + big)
    return abs(v1)


PARAMS = {"ratio": 1000, "speed": 2}
VARIANTS = [{"ratio": 9}, {"ratio": 3, "speed": 4}, {"ratio": 1}]
ANSWER = 5.992007992007992

"""ข้อ 7 — ผลบวกของกำลังกลับส่วน

กำหนดให้ a เป็นจำนวนจริงที่ไม่เท่ากับศูนย์ และ a³ + 1/a³ = 18
จงหาค่าของ  1/a² + 1/a⁵ + 1/a⁶ + 1/a⁷ + a² + a⁵ + a⁶ + a⁷

The eight terms pair up into p_k = a^k + 1/a^k for k = 2, 5, 6, 7, and those
satisfy a linear recurrence once p₁ is known: p_k = p₁·p_{k-1} - p_{k-2}.

p₁ comes from the given value, since p₁³ - 3p₁ = a³ + 1/a³ = 18, whose only real
root is 3 (the other factor p₁² + 3p₁ + 6 has negative discriminant). From
p₁ = 3, p₂ = 7: 18, 47, 123, 322, 843 — and 7 + 123 + 322 + 843 = 1295.

``check`` solves a³ + 1/a³ = 18 numerically for an actual a and adds the eight
terms up, so a slip in the recurrence has nowhere to hide.
"""

from __future__ import annotations

PARAMS = {"cube_sum": 18, "wanted": (2, 5, 6, 7)}
ANSWER = 1295
VARIANTS = [
    {"cube_sum": 52},                     # p1 = 4
    {"cube_sum": 110},                    # p1 = 5
    {"cube_sum": 18, "wanted": (1, 2, 3)},
    {"cube_sum": 198},                    # p1 = 6
    {"cube_sum": 18, "wanted": (4, 8)},
]
TOL = 1e-6


def _p1(cube_sum: int) -> int | None:
    """The integer t with t³ - 3t = cube_sum, if there is one."""
    t = 1
    while t ** 3 - 3 * t <= cube_sum:
        if t ** 3 - 3 * t == cube_sum:
            return t
        t += 1
    return None


def solve(cube_sum=18, wanted=(2, 5, 6, 7)):
    """Σ (a^k + 1/a^k) over the wanted k, via the p_k recurrence."""
    t = _p1(cube_sum)
    if t is None:
        return None
    p = {0: 2, 1: t}
    for k in range(2, max(wanted) + 1):
        p[k] = t * p[k - 1] - p[k - 2]
    return sum(p[k] for k in wanted)


def check(cube_sum=18, wanted=(2, 5, 6, 7)):
    """Independent: find a real a with a³ + 1/a³ = cube_sum, then add it up."""
    if _p1(cube_sum) is None:
        return None

    def f(a: float) -> float:
        return a ** 3 + 1 / a ** 3 - cube_sum

    lo, hi = 1.0 + 1e-9, 10.0
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    a = (lo + hi) / 2
    return round(sum(a ** k + 1 / a ** k for k in wanted))

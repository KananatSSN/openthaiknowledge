"""ข้อ 6 — จำนวนเต็มบวก n ที่ n² อยู่ในรูป xx44yy

จงหาจำนวนเต็มบวก n ทั้งหมดที่มีสมบัติว่า ในระบบฐานสิบ n² อยู่ในรูป xx44yy
เมื่อ x และ y เป็นเลขโดด โดยที่ x > 0

xx44yy = 110000x + 4400 + 11y = 11·(10000x + 400 + y), so 11 divides n², hence
11 divides n and 121 divides n². That forces 11 | 10000x + 400 + y, and since
10000 ≡ 1 and 400 ≡ 4 (mod 11), it forces x + y ≡ 7 (mod 11).

Six digits means 317 ≤ n ≤ 999, and among the multiples of 11 there only one
survives: n = 880, n² = 774400 (x = 7, y = 0). ``solve`` searches the shape
directly; ``check`` builds every xx44yy from its two digits and asks whether it
is a perfect square, which never mentions 11.
"""

from __future__ import annotations

from math import isqrt

#: The fixed middle digits. Changing them changes which squares exist.
PARAMS = {"mid_a": 4, "mid_b": 4}
ANSWER = (880,)
VARIANTS = [
    {"mid_a": 0, "mid_b": 0},
    {"mid_a": 2, "mid_b": 5},
    {"mid_a": 1, "mid_b": 6},
    {"mid_a": 8, "mid_b": 9},
    {"mid_a": 6, "mid_b": 1},
]


def _shape(x: int, y: int, mid_a: int, mid_b: int) -> int:
    return int(f"{x}{x}{mid_a}{mid_b}{y}{y}")


def solve(mid_a=4, mid_b=4):
    """Every n whose square reads xx<mid_a><mid_b>yy, as a sorted tuple."""
    lo, hi = isqrt(99999) + 1, isqrt(999999)
    out = []
    for n in range(lo, hi + 1):
        s = str(n * n)
        if (s[0] == s[1] != "0" and s[2] == str(mid_a) and s[3] == str(mid_b)
                and s[4] == s[5]):
            out.append(n)
    return tuple(out)


def check(mid_a=4, mid_b=4):
    """Independent: build the 90 candidate numbers and test each for squareness."""
    out = []
    for x in range(1, 10):
        for y in range(10):
            v = _shape(x, y, mid_a, mid_b)
            r = isqrt(v)
            if r * r == v:
                out.append(r)
    return tuple(sorted(out))

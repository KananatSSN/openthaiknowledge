"""ข้อ 10 — n ที่มีจำนวนที่ไม่เป็นมิตรของ n จำกัด

Digit sums agree with numbers modulo 9, so if 3 | n no multiple has digit sum
≡ 1, 2 (mod 3) and infinitely many u are not friends. Otherwise n is invertible
mod 9: j·n (j = 1..9) gives every residue, and n(10ᵏ − 1) has digit sum 9k;
concatenating reaches every large u. The answer is the tuple of n ≤ limit with
3 ∤ n.

``check`` explores multiples digit by digit as states (remainder mod n, digit
sum) up to digit sum 80, and keeps the n whose reachable digit sums include
every value from 40 to 80.
"""

from __future__ import annotations

PARAMS = {"limit": 12}
ANSWER = (1, 2, 4, 5, 7, 8, 10, 11)
VARIANTS = [{"limit": 5}, {"limit": 20}, {"limit": 30}]


def solve(limit=12):
    return tuple(n for n in range(1, limit + 1) if n % 3)


def _reachable_sums(n, cap):
    start = {(d % n, d) for d in range(1, 10)}
    seen = set(start)
    frontier = list(start)
    while frontier:
        r, s = frontier.pop()
        for d in range(10):
            state = ((r * 10 + d) % n, s + d)
            if state[1] <= cap and state not in seen:
                seen.add(state)
                frontier.append(state)
    return {s for r, s in seen if r == 0}


def check(limit=12):
    return tuple(n for n in range(1, limit + 1) if set(range(40, 81)) <= _reachable_sums(n, 80))

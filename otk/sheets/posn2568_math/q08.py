"""ข้อ 8 — จำนวนเต็มบวก n ที่ทำให้ P(n) < 0

กำหนดให้ P(x) = (x − 1²)(x − 2²)(x − 3²)⋯(x − m²)      (โจทย์: m = 10)
จงหาว่ามีจำนวนเต็มบวก n ทั้งหมดกี่จำนวนที่ทำให้ P(n) < 0

Method: for a positive integer n let j = #{k ≤ m : k² < n}. Then exactly m − j
factors are negative, so P(n) < 0 iff m − j is odd (and n is not itself one of
the squares, where P = 0). The n with a given j are the integers strictly
between j² and (j+1)² — there are 2j of them. (j = 0 contributes nothing: its
only n is n = 1 = 1², which is a root, so P(1) = 0 rather than negative.)
So the count is  Σ 2j over j = 1..m−1 with m − j odd.

For m = 10 that is 2(1+3+5+7+9) = 50, and n > m² never contributes because
there every factor is positive.

``check`` evaluates the actual product for every n up to past m² and counts.
"""

from __future__ import annotations

PARAMS = {"m": 10}
ANSWER = 50
VARIANTS = [{"m": 1}, {"m": 2}, {"m": 3}, {"m": 7}, {"m": 12}, {"m": 15}]


def solve(m=10):
    """How many positive integers n make the product negative."""
    # j = 0 contributes nothing: its only n is n = 1, which is 1² — a root, so
    # P(1) = 0 rather than negative.
    return sum(2 * j for j in range(1, m) if (m - j) % 2 == 1)


def check(m=10):
    """Independent: multiply the factors out for each candidate n.

    Anything past m² has all factors positive, so the search window is finite.
    """
    count = 0
    for n in range(1, m * m + 2):
        product = 1
        for k in range(1, m + 1):
            product *= n - k * k
        if product < 0:
            count += 1
    return count

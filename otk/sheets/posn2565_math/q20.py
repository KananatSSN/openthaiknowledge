"""ข้อ 20 — รหัสปลดล็อกหีบสมบัติ

นายหินได้ขุดพบหีบสมบัติใบหนึ่งซึ่งถูกล็อคด้วยรหัส และพบกระดาษที่บอกใบ้ถึงรหัสดังนี้
    - รหัสเป็นเลขโดดห้าตัวเรียงจากน้อยไปมาก (อาจมีเลขซ้ำได้)
    - ฐานนิยมของเลขโดดห้าตัวนี้มีเพียงค่าเดียว
    - ค่าเฉลี่ยของเลขห้าตัวนี้มีค่าเท่ากับมัธยฐาน แต่มีค่าน้อยกว่าฐานนิยม
    - ค่าต่ำสุดของเลขห้าตัวนี้เป็นจำนวนเฉพาะคี่
จงหารหัสปลดล็อกหีบสมบัติใบนี้

Four statistics pinning down five digits. Written as d₁ ≤ … ≤ d₅:

* the median is d₃ and the mean is Σd/5, so **Σd = 5·d₃**;
* the mode is unique and strictly greater than the mean, so the repeated digit
  sits at or above the middle;
* d₁ ∈ {3, 5, 7} — the odd primes below 10.

Exactly one code survives — **3 5 6 8 8**: mode 8 (twice), median 6, mean
30/5 = 6, minimum 3. ``solve`` returns ``None`` rather than a guess if a constant
set leaves several, which most do, so the generator draws from a pool of the ones
that do not.

``solve`` walks the non-decreasing tuples directly (C(14,5) = 2002 of them);
``check`` runs over all 10⁵ *ordered* digit strings and tests the same four
statements on the sorted version, so the two searches share no bookkeeping.
"""

from __future__ import annotations

import itertools
from collections import Counter
from fractions import Fraction
from math import isqrt

#: how many digits, their range, and which minima are allowed.
PARAMS = {"length": 5, "top": 9, "min_kind": "odd_prime"}
ANSWER = (3, 5, 6, 8, 8)
VARIANTS = [
    {"length": 5, "top": 9, "min_kind": "prime"},
    {"length": 5, "top": 9, "min_kind": "odd"},
    {"length": 5, "top": 8, "min_kind": "odd_prime"},
    {"length": 5, "top": 11, "min_kind": "odd_prime"},
    {"length": 3, "top": 9, "min_kind": "odd_prime"},
    {"length": 5, "top": 9, "min_kind": "any"},        # far too many codes
]


def _is_prime(n: int) -> bool:
    return n >= 2 and all(n % f for f in range(2, isqrt(n) + 1))


def _allowed(value: int, kind: str) -> bool:
    return {"odd_prime": _is_prime(value) and value % 2 == 1,
            "prime": _is_prime(value),
            "odd": value % 2 == 1,
            "any": True}.get(kind, False)


def _fits(digits, kind: str) -> bool:
    """The four clues, tested on an already-sorted tuple."""
    counts = Counter(digits)
    top_count = max(counts.values())
    modes = [v for v, n in counts.items() if n == top_count]
    if len(modes) != 1 or top_count < 2:
        return False
    median = digits[len(digits) // 2] if len(digits) % 2 else \
        Fraction(digits[len(digits) // 2 - 1] + digits[len(digits) // 2], 2)
    mean = Fraction(sum(digits), len(digits))
    return mean == median and mean < modes[0] and _allowed(digits[0], kind)


def solve(length=5, top=9, min_kind="odd_prime"):
    """The one code the clues allow, as a tuple of digits."""
    if length < 3 or top < 1:
        return None
    hits = [d for d in itertools.combinations_with_replacement(range(top + 1),
                                                               length)
            if _fits(d, min_kind)]
    if len(hits) != 1:
        return None
    return hits[0]


def check(length=5, top=9, min_kind="odd_prime"):
    """Independent: sweep every ordered digit string and sort it before testing."""
    if length < 3 or top < 1:
        return None
    if (top + 1) ** length > 2 * 10 ** 6:
        return None
    hits = set()
    for combo in itertools.product(range(top + 1), repeat=length):
        digits = tuple(sorted(combo))
        if _fits(digits, min_kind):
            hits.add(digits)
    if len(hits) != 1:
        return None
    return next(iter(hits))

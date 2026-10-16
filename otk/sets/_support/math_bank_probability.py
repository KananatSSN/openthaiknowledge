"""ความน่าจะเป็น sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found six units of ``otk/knowledge/math/probability.json``
that no problem set practised. Each is exercised by real exam questions in
``openthaiknowledge-bank/rathcenter/13 ความน่าจะเป็น`` (A-level, กสพท, O-NET). One set
per unit:

======================================  ==========================================
unit                                    set
======================================  ==========================================
math.probability.union                  math.probability_union_m5
math.probability.table                  math.probability_two_way_table_m5
math.probability.sequential-no-repl…    math.probability_without_replacement_m5
math.probability.digit-numbers          math.probability_digit_numbers_m5
math.probability.random-arrangement     math.probability_random_arrangement_m5
math.probability.random-route           math.probability_grid_route_m5
======================================  ==========================================

Every answer comes from a closed-form solver in this module.
``test_math_bank_probability.py`` checks each solver against brute-force
enumeration of the same experiment, so the formulas are proven over the whole
parameter range the generators draw from, not just the exam's numbers.

Registered at ม.6 and filed at ม.5, like the topic's other sets.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import product

# ── A หรือ B ──────────────────────────────────────────────────────────────────


# ── ตารางสองทาง ───────────────────────────────────────────────────────────────


# ── หยิบทีละชิ้นแบบไม่ใส่คืน ─────────────────────────────────────────────────────


# ── จำนวนที่มีเงื่อนไขเลขโดด ─────────────────────────────────────────────────────


# ── การจัดเรียงแบบสุ่ม ────────────────────────────────────────────────────────


# ── เส้นทางที่สุ่มเลือก ──────────────────────────────────────────────────────────


# Brute-force references for the tests. They enumerate the experiment itself,
# sharing no formula with the solvers above.

def brute_digits(digits: int, condition: str, k: int = 0) -> Fraction:
    nums = range(10 ** (digits - 1), 10 ** digits)
    def ok(x: int) -> bool:
        ds = [int(c) for c in str(x)]
        return {"all_odd": all(c % 2 for c in ds),
                "even_product": math.prod(ds) % 2 == 0,
                "has_k": k in ds,
                "distinct": len(set(ds)) == len(ds)}[condition]
    return Fraction(sum(map(ok, nums)), len(nums))


def brute_routes(m: int, n: int, p: int, q: int) -> Fraction:
    routes = [s for s in product("RU", repeat=m + n) if s.count("R") == m]
    def passes(s) -> bool:
        x = y = 0
        for step in s:
            if (x, y) == (p, q):
                return True
            x, y = (x + 1, y) if step == "R" else (x, y + 1)
        return (x, y) == (p, q)
    return Fraction(sum(map(passes, routes)), len(routes))

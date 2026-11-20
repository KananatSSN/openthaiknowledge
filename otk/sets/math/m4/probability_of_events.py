"""ความน่าจะเป็นของเหตุการณ์

คณิตศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ค 3.2 ม.4/2

Sets moved here from: math_gaps_secondary.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p4 import as_mixed

PROVENANCE = Provenance("original")


_PROB_TOPIC = "ความน่าจะเป็นของเหตุการณ์"


def _dice_count(target: str, k: int) -> int:
    rolls = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    if target == "sum":
        return sum(a + b == k for a, b in rolls)
    if target == "sum_at_least":
        return sum(a + b >= k for a, b in rolls)
    return sum(a == b for a, b in rolls)


@question_type("math.sample_space_m4", display_name={"th": "ปริภูมิตัวอย่างและเหตุการณ์"},
               level={"th": "ม.4"}, topic=_PROB_TOPIC)
class SampleSpaceM4(WordProblem):
    _EXPERIMENTS = (
        ("โยนเหรียญ 2 เหรียญพร้อมกัน", 4),
        ("โยนเหรียญ 3 เหรียญพร้อมกัน", 8),
        ("ทอดลูกเต๋า 1 ลูก และโยนเหรียญ 1 เหรียญ", 12),
        ("ทอดลูกเต๋า 2 ลูกพร้อมกัน", 36),
        ("หยิบบัตร 1 ใบจากบัตรหมายเลข 1 ถึง 10 แล้วโยนเหรียญ 1 เหรียญ", 20),
    )

    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            what, size = rng.choice(self._EXPERIMENTS)
        elif kind == 1:
            # A spinner turned twice: one factor per turn.
            n = rng.randint(3, 8)
            what, size = f"หมุนวงล้อที่แบ่งเป็น {n} ช่องเท่ากัน 2 ครั้ง", n * n
        else:
            n, coins = rng.randint(3, 12), rng.randint(1, 2)
            what = f"หยิบลูกบอล 1 ลูกจากกล่องที่มีลูกบอลหมายเลข 1 ถึง {n} แล้วโยนเหรียญ {coins} เหรียญ"
            size = n * 2 ** coins
        return MathDraw("", str(size), prompt=f"{what} ปริภูมิตัวอย่างมีสมาชิกกี่ตัว",
                        distractors=_story.keep(size // 2, size + 2, size - 1, 2 * size, answer=size, lo=1)[:3])


@question_type("math.event_probability_m4", display_name={"th": "ความน่าจะเป็นของเหตุการณ์จากการนับ"},
               level={"th": "ม.4"}, topic=_PROB_TOPIC)
class EventProbabilityM4(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            k = rng.randint(3, 11)
            hits, total = _dice_count("sum", k), 36
            prompt = f"ทอดลูกเต๋า 2 ลูกพร้อมกัน ความน่าจะเป็นที่ผลรวมของแต้มเท่ากับ {k} เป็นเท่าใด"
        elif kind == 1:
            k = rng.randint(8, 11)
            hits, total = _dice_count("sum_at_least", k), 36
            prompt = f"ทอดลูกเต๋า 2 ลูกพร้อมกัน ความน่าจะเป็นที่ผลรวมของแต้มอย่างน้อย {k} เป็นเท่าใด"
        else:
            coins = rng.randint(2, 4)
            heads = rng.randint(1, coins - 1)
            hits, total = math.comb(coins, heads), 2 ** coins
            prompt = f"โยนเหรียญ {coins} เหรียญพร้อมกัน ความน่าจะเป็นที่จะออกหัวพอดี {heads} เหรียญเป็นเท่าใด"
        value = Fraction(hits, total)
        wrongs = [Fraction(hits, 11) if kind < 2 else Fraction(1, coins + 1), Fraction(1, total),
                  1 - value, Fraction(hits + 1, total)]
        return MathDraw("", as_mixed(value), prompt=prompt,
                        distractors=[as_mixed(w) for w in dict.fromkeys(wrongs) if w != value and 0 < w < 1])


@question_type("math.probability_by_choosing_m4", display_name={"th": "ความน่าจะเป็นโดยใช้การเลือก"},
               level={"th": "ม.4"}, topic=_PROB_TOPIC)
class ProbabilityByChoosingM4(WordProblem):
    def expr(self, rng: Random):
        boys, girls, r = rng.randint(3, 6), rng.randint(3, 6), 2
        total = math.comb(boys + girls, r)
        # (setting, first kind, second kind, counter, how two are picked)
        setting, x, y, unit, pick = rng.choice((
            ("ห้องเรียนมีนักเรียน", "นักเรียนชาย", "นักเรียนหญิง", "คน", "สุ่มเลือกตัวแทน 2 คน"),
            ("กล่องมีหลอดไฟ", "หลอดไฟดี", "หลอดไฟเสีย", "หลอด", "สุ่มหยิบพร้อมกัน 2 หลอด"),
            ("ถุงมีลูกอม", "ลูกอมรสส้ม", "ลูกอมรสองุ่น", "เม็ด", "สุ่มหยิบพร้อมกัน 2 เม็ด"),
        ))
        if rng.random() < 0.5:
            hits = math.comb(girls, 2)
            ask = f"ได้{y}ทั้ง 2 {unit}"
            wrongs = [Fraction(girls, boys + girls), Fraction(girls * girls, (boys + girls) ** 2),
                      Fraction(girls * (girls - 1), total)]
        else:
            hits = boys * girls
            ask = f"ได้{x} 1 {unit} และ{y} 1 {unit}"
            wrongs = [Fraction(1, 2), Fraction(boys * girls, (boys + girls) ** 2),
                      Fraction(2 * boys * girls, total)]
        value = Fraction(hits, total)
        return MathDraw("", as_mixed(value), prompt=(
            f"{setting} ได้แก่ {x} {boys} {unit} และ{y} {girls} {unit} {pick} "
            f"ความน่าจะเป็นที่จะ{ask}เป็นเท่าใด"),
            distractors=[as_mixed(w) for w in dict.fromkeys(wrongs) if w != value and 0 < w < 1])

from math import comb, gcd  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More probability (2026-11): exactly k heads, a card from the deck, one of each, at least one head,
# divisible by both, two people side by side, and a total above a number ──


@question_type("math.exactly_k_heads_m4", display_name={"th": "ความน่าจะเป็นที่ได้หัวพอดี k เหรียญ"}, level=LEVEL,
               topic="ความน่าจะเป็นของเหตุการณ์")
class ExactlyKHeadsM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 5)
        k = rng.randint(0, n)
        right = Fraction(comb(n, k), 2 ** n)
        prompt = f"โยนเหรียญ {n} เหรียญพร้อมกัน ความน่าจะเป็นที่จะออกหัวพอดี {k} เหรียญเท่ากับเท่าใด"
        # One outcome only; the count over the coins; k over n.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(1, 2 ** n), Fraction(k, n) if k else Fraction(1, n + 1),
                                         Fraction(comb(n, k), 2 * n), Fraction(comb(n, k) + 1, 2 ** n), answer=right))


@question_type("math.card_from_deck_m4", display_name={"th": "ความน่าจะเป็นของการหยิบไพ่"}, level=LEVEL,
               topic="ความน่าจะเป็นของเหตุการณ์")
class CardFromDeckM4(WordProblem):
    _EVENTS = (("ไพ่โพแดง", 13), ("ไพ่หน้าคน (J, Q, K)", 12), ("ไพ่เอซ", 4), ("ไพ่สีแดง", 26), ("ไพ่หมายเลข 7", 4),
               ("ไพ่โพแดงหรือไพ่เอซ", 16), ("ไพ่สีดำที่เป็นหน้าคน", 6))

    def expr(self, rng: Random):
        what, k = rng.choice(self._EVENTS)
        right = Fraction(k, 52)
        prompt = f"สุ่มหยิบไพ่ 1 ใบจากไพ่สำรับหนึ่ง (52 ใบ) ความน่าจะเป็นที่จะได้{what}เท่ากับเท่าใด"
        # Out of 13 or 26 cards; one card fewer.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(k, 13) if k < 13 else Fraction(1, 2) if k != 26 else Fraction(1, 4),
                                         Fraction(k - 1, 52), Fraction(k, 26) if k < 26 else Fraction(1, 52),
                                         Fraction(k + 1, 52), answer=right))


@question_type("math.one_of_each_m4", display_name={"th": "เลือกสองคนได้ชายหนึ่งหญิงหนึ่ง"}, level=LEVEL,
               topic="ความน่าจะเป็นของเหตุการณ์")
class OneOfEachM4(WordProblem):
    def expr(self, rng: Random):
        b, g = rng.randint(2, 8), rng.randint(2, 8)
        right = Fraction(b * g, comb(b + g, 2))
        prompt = f"ห้องเรียนมีนักเรียนชาย {b} คน หญิง {g} คน สุ่มเลือก 2 คน ความน่าจะเป็นที่จะได้ชายหนึ่งคนและหญิงหนึ่งคนเท่ากับเท่าใด"
        # Order counted; one half; both boys.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(b * g, (b + g) ** 2), Fraction(1, 2), Fraction(comb(b, 2), comb(b + g, 2)),
                                         Fraction(2 * b * g, (b + g) ** 2), answer=right))


@question_type("math.at_least_one_head_m4", display_name={"th": "ความน่าจะเป็นที่ได้หัวอย่างน้อยหนึ่งเหรียญ"},
               level=LEVEL, topic="ความน่าจะเป็นของเหตุการณ์")
class AtLeastOneHeadM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 6)
        right = 1 - Fraction(1, 2 ** n)
        prompt = f"โยนเหรียญ {n} เหรียญพร้อมกัน ความน่าจะเป็นที่จะออกหัวอย่างน้อยหนึ่งเหรียญเท่ากับเท่าใด"
        # No heads at all; exactly one; one half.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(1, 2 ** n), Fraction(n, 2 ** n), Fraction(1, 2), Fraction(n - 1, n),
                                         answer=right))


@question_type("math.divisible_by_both_m4", display_name={"th": "ความน่าจะเป็นที่หารด้วยสองจำนวนลงตัว"},
               level=LEVEL, topic="ความน่าจะเป็นของเหตุการณ์")
class DivisibleByBothM4(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.sample((2, 3, 4, 5, 6), 2)
        top = rng.choice((30, 40, 50, 60, 100))
        lcm = a * b // gcd(a, b)
        right = Fraction(top // lcm, top)
        prompt = f"สุ่มหยิบบัตร 1 ใบจากบัตรหมายเลข 1 ถึง {top} ความน่าจะเป็นที่จะได้หมายเลขที่หารด้วย {a} และ {b} ลงตัวเท่ากับเท่าใด"
        # Divisible by a or b; by the product; by a only.
        either = top // a + top // b - top // lcm
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(either, top), Fraction(top // (a * b), top) if top // (a * b) else Fraction(1, top),
                                         Fraction(top // a, top), Fraction(top // lcm + 1, top), answer=right))


@question_type("math.together_probability_m4", display_name={"th": "ความน่าจะเป็นที่สองคนนั่งติดกัน"}, level=LEVEL,
               topic="ความน่าจะเป็นของเหตุการณ์")
class TogetherProbabilityM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 9)
        right = Fraction(2, n)
        p, q = _story.names(rng)
        prompt = f"คน {n} คนรวมทั้ง{p}และ{q} นั่งเรียงแถวหน้ากระดานแบบสุ่ม ความน่าจะเป็นที่{p}กับ{q}นั่งติดกันเท่ากับเท่าใด"
        # The pair counted one way; one seat in n; not together.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(1, n), Fraction(1, n - 1), 1 - right if right != Fraction(1, 2) else Fraction(1, 3),
                                         Fraction(2, n - 1), answer=right))


@question_type("math.dice_total_above_m4", display_name={"th": "ความน่าจะเป็นที่ผลรวมแต้มมากกว่าค่าที่กำหนด"},
               level=LEVEL, topic="ความน่าจะเป็นของเหตุการณ์")
class DiceTotalAboveM4(WordProblem):
    def expr(self, rng: Random):
        s = rng.randint(4, 10)
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b > s)
        right = Fraction(ways, 36)
        prompt = f"ทอดลูกเต๋าสองลูกพร้อมกัน ความน่าจะเป็นที่ผลรวมของแต้มมากกว่า {s} เท่ากับเท่าใด"
        # "At least" counted; "less than"; out of 11 totals.
        at_least = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= s)
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk4(Fraction(at_least, 36), Fraction(36 - ways, 36), Fraction(12 - s, 11),
                                         Fraction(ways + 1, 36), answer=right))

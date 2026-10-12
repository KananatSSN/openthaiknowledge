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

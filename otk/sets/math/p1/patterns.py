"""แบบรูป

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.1/1

Sets moved here from: math_apply_stage, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p1 import (
    LEVEL,
    NumberPatternType,
    PatternRuleType,
    RepeatingPatternType,
)

PROVENANCE = Provenance("original")


@question_type("math.repeating_pattern_p1",
               display_name={"th": "แบบรูปซ้ำของรูป (ชุดละ 2 รูป)"},
               level=LEVEL, topic="แบบรูป")
class RepeatingPatternP1(RepeatingPatternType):
    UNIT = 2


@question_type("math.number_pattern_p1",
               display_name={"th": "แบบรูปของจำนวน (เพิ่มขึ้น/ลดลงทีละ 1 และ 10)"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP1(NumberPatternType):
    STEPS = (1, 10)


@question_type("math.pattern_word_p1", display_name={"th": "แบบรูปในชีวิตประจำวัน"},
               level={"th": "ป.1"}, topic="แบบรูป")
class PatternWordP1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # A repeating pattern: the k-th item is the ((k − 1) mod length)-th of the unit.
            unit = rng.sample(("แดง", "ฟ้า", "เหลือง", "เขียว"), rng.choice((2, 3)))
            k = rng.randint(len(unit) * 2 + 1, 15)
            shown = " ".join(f"สี{c}" for c in (unit * 3)[:len(unit) * 2])
            right = f"สี{unit[(k - 1) % len(unit)]}"
            return _choices([text(f"ร้อยลูกปัดเรียงเป็นแบบรูปซ้ำ {shown} ... ลูกปัดลูกที่ {k} เป็นสีอะไร")],
                            right, [f"สี{c}" for c in ("แดง", "ฟ้า", "เหลือง", "เขียว")], self.topic)
        step = rng.choice((2, 5, 10))
        thing, counter, unit = {2: ("นก", "ตัว", "ขา"), 5: ("ปลาดาว", "ตัว", "แขน"), 10: ("กล่องดินสอ", "กล่อง", "แท่ง")}[step]
        k = rng.randint(4, 10 if step != 10 else 9)
        stem = (f"{thing} 1, 2, 3 {counter} มี{unit} {step}, {2 * step}, {3 * step} {unit} "
                f"ถ้ามี{thing} {k} {counter} จะมี{unit}ทั้งหมดกี่{unit}")
        return maths([text(stem)], str(k * step), _nums(k * step, k + step, (k - 1) * step, (k + 1) * step, lo=1),
                     self.topic)


@question_type("math.pattern_rule_p1",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP1(PatternRuleType):
    STEPS = (1, 10)

"""แบบรูป

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: —

Sets moved here from: math_apply_stage, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p1 import NumberPatternType, PatternRuleType, RepeatingPatternType
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.repeating_pattern_p2",
               display_name={"th": "แบบรูปซ้ำของรูป (ชุดละ 3 รูป)"},
               level=LEVEL, topic="แบบรูป")
class RepeatingPatternP2(RepeatingPatternType):
    UNIT = 3


@question_type("math.number_pattern_p2",
               display_name={"th": "แบบรูปของจำนวน (ทีละ 2, 5, 10, 100)"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP2(NumberPatternType):
    STEPS = (2, 5, 10, 100)
    HI = 1000


@question_type("math.pattern_word_p2", display_name={"th": "แบบรูปของจำนวนที่เพิ่มขึ้นหรือลดลงในสถานการณ์"},
               level={"th": "ป.2"}, topic="แบบรูป")
class PatternWordP2(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step = rng.choice((2, 5, 10, 100))
        k = rng.randint(5, 9)
        who = rng.choice(_story.NAMES)
        # Every number stays within 1,000.
        if rng.random() < 0.5:
            start = step * rng.randint(1, 2) if step == 100 else rng.randint(1, 9) * (step if step != 2 else 1)
            terms = [start + step * i for i in range(3)]
            ans = start + step * (k - 1)
            frames = [f"{who}ออมเงินวันที่ 1, 2, 3 มีเงินสะสม {terms[0]}, {terms[1]}, {terms[2]} บาท "
                      f"ถ้าเพิ่มขึ้นแบบนี้ทุกวัน วันที่ {k} มีเงินสะสมกี่บาท"]
            if step != 100:
                frames.append(f"{who}อ่านหนังสือถึงหน้า {terms[0]}, {terms[1]}, {terms[2]} ในวันที่ 1, 2, 3 "
                              f"ถ้าอ่านเพิ่มเท่ากันทุกวัน วันที่ {k} อ่านถึงหน้าใด")
            stem = rng.choice(frames)
        else:
            if step == 100:
                k = min(k, 7)
            start = step * rng.randint(k + 2, min(k + 9, 1000 // step))
            ans = start - step * k
            stem = (f"ถังมีน้ำ {start} ลิตร ใช้น้ำไปวันละเท่ากัน วันที่ 1, 2, 3 เหลือน้ำ "
                    f"{start - step}, {start - 2 * step}, {start - 3 * step} ลิตร วันที่ {k} เหลือน้ำกี่ลิตร")
        # One step too many or too few, and the step taken as one.
        return maths([text(stem)], str(ans), _nums(ans, ans + step, ans - step, ans + 1, lo=0), self.topic)


@question_type("math.pattern_rule_p2",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป (ทีละ 2, 5, 10, 100)"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP2(PatternRuleType):
    STEPS = (2, 5, 10, 100)
    HI = 1000

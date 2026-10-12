"""แบบรูป

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.3/1

Sets moved here from: math_p3, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p1 import NumberPatternType, PatternRuleType
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_p2 import GROWING, P3

PROVENANCE = Provenance("original")


_P3_STEPS = (3, 4, 6, 7, 8, 9, 25, 50)


@question_type("math.number_pattern_p3",
               display_name={"th": "แบบรูปของจำนวนที่เพิ่มขึ้นหรือลดลงทีละเท่า ๆ กัน"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP3(NumberPatternType):
    STEPS = _P3_STEPS
    HI = 1000


@question_type("math.pattern_rule_p3",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป (ทีละเท่า ๆ กัน)"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP3(PatternRuleType):
    STEPS = _P3_STEPS
    HI = 1000


@question_type("math.growing_pattern_picture_p3", display_name={"th": "แบบรูปที่เพิ่มขึ้นจากภาพ"},
               level=P3, topic="แบบรูป")
class GrowingPatternPictureP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(GROWING)
        piece = "รูปสี่เหลี่ยม" if g.style == "tile" else "จุด"
        img = image(g.asset_id, alt=f"ภาพแบบรูปสามรูปแรก ประกอบด้วย{piece}")
        if rng.random() < 0.3:
            step = g.rows
            return _math_q([text(f"จากแบบรูป แต่ละรูปมี{piece}เพิ่มขึ้นจากรูปก่อนกี่{'รูป' if g.style == 'tile' else 'จุด'}"),
                            img], str(step), _near(step, g.count(1), g.count(3), step + 2, lo=1),
                           self.topic)
        n = rng.choice((4, 5, 6, 8, 10))
        right = g.count(n)
        # One more per figure instead of one more column; n pieces per row;
        # an off-by-one figure.
        wrongs = [g.count(3) + (n - 3), g.rows * n, g.count(n + 1), g.count(n - 1)]
        return _math_q([text(f"ถ้าแบบรูปนี้เพิ่มขึ้นแบบเดิมไปเรื่อย ๆ รูปที่ {n} มี{piece}ทั้งหมดเท่าใด"), img],
                       str(right), _near(right, *wrongs, lo=1), self.topic)


@question_type("math.growing_pattern_p3",
               display_name={"th": "แบบรูปที่เพิ่มขึ้น: รูปที่เท่าใดมีกี่ชิ้น"},
               level=LEVEL, topic="แบบรูป")
class GrowingPatternP3(WordProblem):
    _THINGS = (("จุด", "จุด"), ("ไม้ขีดไฟ", "ก้าน"), ("ลูกปัด", "เม็ด"), ("บล็อกไม้", "ก้อน"))

    def expr(self, rng: Random):
        thing, cl = rng.choice(self._THINGS)
        first, step = rng.randint(2, 9), rng.randint(2, 6)
        k = rng.randint(5, 12)
        shown = ", ".join(f"รูปที่ {i + 1} มี {first + step * i} {cl}" for i in range(3))
        ans = first + step * (k - 1)
        return MathDraw("", str(ans),
                        prompt=f"แบบรูปของ{thing}: {shown} ถ้าเพิ่มขึ้นแบบนี้ไปเรื่อย ๆ "
                               f"รูปที่ {k} มี{thing}กี่{cl}",
                        # Stepping k times instead of k − 1, and k × step alone.
                        distractors=_story.keep(first + step * k, step * k, ans - step,
                                                first * k, answer=ans, lo=1))

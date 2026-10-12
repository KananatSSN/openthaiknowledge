"""แบบรูป

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.6/1

Sets moved here from: math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_PATTERN_TOPIC = "แบบรูป"


@question_type("math.pattern_nth_term_p6",
               display_name={"th": "แบบรูป: หาพจน์ที่ n"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class PatternNthTermP6(WordProblem):
    def expr(self, rng: Random):
        first, step = rng.randint(1, 20), rng.choice((2, 3, 4, 5, 6, 7, 8, 9, 11, 12))
        n = rng.randint(10, 40)
        terms = [first + step * i for i in range(4)]
        ans = first + step * (n - 1)
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"จากแบบรูป พจน์ที่ {n} คือจำนวนใด",
            f"{p}ออมเงินวันที่ {n} กี่บาท ถ้าออมเงินแต่ละวันเป็นแบบรูปดังนี้ (บาท)",
            f"หอประชุมจัดเก้าอี้แต่ละแถวเป็นแบบรูปดังนี้ แถวที่ {n} มีเก้าอี้กี่ตัว",
        ))
        return MathDraw(r",\ ".join(map(str, terms)) + r",\ \ldots", str(ans),
                        prompt=prompt,
                        # n steps instead of n − 1, and n × step alone.
                        distractors=_story.keep(first + step * n, step * n, ans - first,
                                                first * n, answer=ans, lo=1))


@question_type("math.pattern_rule_expression_p6",
               display_name={"th": "แบบรูป: เขียนความสัมพันธ์ของพจน์ที่ n"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class PatternRuleExpressionP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        step = rng.randint(2, 9)
        c = rng.randint(-5, 9)
        while c == 0 or step + c <= 0:
            c = rng.randint(-5, 9)
        terms = [step * n + c for n in range(1, 5)]
        form = lambda k, m: f"{k}n {'+' if m > 0 else '-'} {abs(m)}" if m else f"{k}n"
        first = terms[0]
        wrongs = [f"n + {step}", form(step, c + step), form(c if c > 1 else step + 1, step),
                  f"{first}n"]
        right = form(step, c)
        return _maths([text("จากแบบรูป"), content_math(r",\ ".join(map(str, terms)) + r",\ \ldots"),
                       text("พจน์ที่ n คือข้อใด")], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.matchstick_pattern_p6",
               display_name={"th": "แบบรูปของรูปเรขาคณิต: ไม้ขีดไฟและรูปสี่เหลี่ยม"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class MatchstickPatternP6(WordProblem):
    _SHAPES = (("รูปสี่เหลี่ยมจัตุรัส", 4, 3), ("รูปสามเหลี่ยม", 3, 2),
               ("รูปหกเหลี่ยม", 6, 5), ("รูปห้าเหลี่ยม", 5, 4))

    def expr(self, rng: Random):
        n = rng.randint(6, 30)
        kind = rng.randrange(3)
        if kind == 0:
            shape, first, step = rng.choice(self._SHAPES)
            ans = first + step * (n - 1)
            prompt = (f"นำไม้ขีดไฟมาต่อเป็น{shape}เรียงติดกันเป็นแถว โดยรูปที่อยู่ติดกันใช้ไม้ขีด"
                      f"ร่วมกัน 1 ก้าน แถวที่มี{shape} 1, 2, 3 รูป ใช้ไม้ขีด "
                      f"{first}, {first + step}, {first + 2 * step} ก้าน ถ้าเรียง {n} รูป "
                      f"ต้องใช้ไม้ขีดไฟกี่ก้าน")
        elif kind == 1:
            # Tables pushed end to end: the joined sides lose their seats.
            table, first, step = rng.choice((("รูปสี่เหลี่ยมจัตุรัส", 4, 2), ("รูปหกเหลี่ยม", 6, 4),
                                              ("รูปสามเหลี่ยม", 3, 1)))
            ans = first + step * (n - 1)
            prompt = (f"นำโต๊ะ{table}มาต่อกันเป็นแถวยาว ด้านละ 1 ที่นั่ง โต๊ะ 1, 2, 3 ตัว นั่งได้ "
                      f"{first}, {first + step}, {first + 2 * step} คน ถ้าต่อโต๊ะ {n} ตัว จะนั่งได้กี่คน")
        else:
            # A path of dark tiles edged with white ones.
            first, step = 8, 2
            ans = first + step * (n - 1)
            prompt = (f"ปูทางเดินด้วยกระเบื้องสีดำเรียงเป็นแถว แล้วล้อมรอบด้วยกระเบื้องสีขาว "
                      f"กระเบื้องสีดำ 1, 2, 3 แผ่น ใช้กระเบื้องสีขาว {first}, {first + step}, "
                      f"{first + 2 * step} แผ่น ถ้ากระเบื้องสีดำมี {n} แผ่น ต้องใช้กระเบื้องสีขาวกี่แผ่น")
        return MathDraw("", str(ans), prompt=prompt,
                        # Counting every shape's sticks separately.
                        distractors=_story.keep(first * n, step * n, ans + step, ans - 1,
                                                answer=ans, lo=1))

"""กราฟความสัมพันธ์เชิงเส้น

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.1/2, ค 1.3 ม.1/3

Sets moved here from: math, math_diagrams, math_m1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, poly_tex
from otk.sets._support.math_diagrams import LINE_FN_ALT, LINE_FNS, _img, _math_q, _nums
from otk.sets._support.math_m1 import LEVEL, NL
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


_GRAPH_TOPIC = "กราฟความสัมพันธ์เชิงเส้น"


@question_type("math.linear_graph_point",
               display_name={"th": "หาค่า y จากสมการเส้นตรง"}, level={"th": "ม.1"},
               topic="กราฟความสัมพันธ์เชิงเส้น")
class LinearGraphPoint(WordProblem):
    def expr(self, rng: Random):
        m = rng.choice([n for n in range(-5, 6) if n])
        c = rng.randint(-10, 10)
        x = rng.randint(-5, 5)
        eq = poly_tex((m, "x"), (c, ""))
        return MathDraw(rf"y = {eq}", str(m * x + c),
                        prompt=f"จากสมการเส้นตรงต่อไปนี้ เมื่อ x = {x} จงหา y",
                        distractors=[str(m + x + c), str(m * x - c), str(m * x)])


@question_type("math.linear_graph_read_m1", display_name={"th": "อ่านค่าจากกราฟความสัมพันธ์เชิงเส้น"},
               level={"th": "ม.1"}, topic="กราฟความสัมพันธ์เชิงเส้น")
class LinearGraphReadM1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        fn = rng.choice(LINE_FNS)
        xs = [x for x in range(-5, 6) if -6 <= fn.m * x + fn.c <= 6]
        img = _img(fn.asset_id, LINE_FN_ALT)
        kind = rng.randrange(3)
        if kind == 0:
            x = rng.choice([v for v in xs if v != 0] or xs)
            y = fn.m * x + fn.c
            return _math_q([text(f"จากกราฟ เมื่อ x = {x} ค่าของ y เท่ากับเท่าใด"), img], str(y),
                           _nums(-y, y + 1, y - 1, x, answer=y, lo=-20), self.topic)
        if kind == 1:
            return _math_q([text("กราฟนี้ตัดแกน Y ที่จุดใด"), img], f"(0, {fn.c})",
                           [f"({fn.c}, 0)", f"(0, {fn.c + 1})", f"(0, {-fn.c})" if fn.c else "(0, 1)",
                            f"(0, {fn.m})" if fn.m != fn.c else "(0, 2)", f"(0, {fn.c - 1})",
                            f"(0, {fn.c + 2})"],
                           self.topic)
        ys = [fn.m * x + fn.c for x in xs]
        y = rng.choice(ys)
        x = xs[ys.index(y)]
        return _math_q([text(f"จากกราฟ ถ้า y = {y} แล้ว x เท่ากับเท่าใด"), img], str(x),
                       _nums(-x, x + 1, x - 1, y, answer=x, lo=-20), self.topic)


@question_type("math.linear_relation_context_m1",
               display_name={"th": "ความสัมพันธ์เชิงเส้นในชีวิตจริง"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class LinearRelationContextM1(WordProblem):
    _CASES = (("ค่าโดยสารแท็กซี่", "กิโลเมตรที่เดินทาง", "บาท", (35, 45), (5, 9)),
              ("ค่าโทรศัพท์รายเดือน", "นาทีที่โทร", "บาท", (99, 299), (1, 3)),
              ("ความยาวของเทียน", "ชั่วโมงที่จุด", "เซนติเมตร", (20, 40), (-3, -1)),
              ("ค่าจ้างช่างซ่อม", "ชั่วโมงที่ทำงาน", "บาท", (200, 500), (150, 300)))

    def expr(self, rng: Random):
        what, per, unit, (clo, chi), (mlo, mhi) = rng.choice(self._CASES)
        c = rng.randint(clo, chi)
        m = rng.choice([v for v in range(mlo, mhi + 1) if v])
        rule = f"y = {c} {'+' if m > 0 else '-'} {abs(m) if abs(m) != 1 else ''}x"
        x = rng.randint(2, 6 if m < 0 else 30)
        if m < 0:
            x = min(x, c // abs(m) - 1)
        y = c + m * x
        if rng.random() < 0.5:
            return MathDraw(rule, str(y),
                            prompt=(f"{what} (y {unit}) สัมพันธ์กับ{per} (x) ตามสมการต่อไปนี้ "
                                    f"เมื่อ x = {x} แล้ว y เท่ากับเท่าใด"),
                            distractors=_story.keep((c + m) * x, m * x, c * x + m, y + m,
                                                    answer=y, lo=0))
        return MathDraw(rule, str(x),
                        prompt=(f"{what} (y {unit}) สัมพันธ์กับ{per} (x) ตามสมการต่อไปนี้ "
                                f"ถ้า y = {y} แล้ว x เท่ากับเท่าใด"),
                        # Forgetting to divide by the rate, and adding the constant.
                        distractors=_story.keep(abs(y - c), abs(y + c) // abs(m), x + 1, x - 1,
                                                answer=x, lo=1))


@question_type("math.table_to_linear_equation_m1",
               display_name={"th": "เขียนสมการจากตารางความสัมพันธ์"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class TableToLinearEquationM1(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice([v for v in range(-5, 7) if v not in (-1, 0, 1)])
        c = rng.choice([v for v in range(-9, 10) if v])
        xs = sorted(rng.sample(range(-3, 7), 4))
        ys = [m * x + c for x in xs]
        rule = lambda k, b: rf"y = {k}x {'+' if b > 0 else '-'} {abs(b)}"
        right = rule(m, c)
        # Reading the rise per step as the constant, and the first y as the constant.
        wrongs = [rule(c, m) if c not in (0, 1) else rule(m, -c), rule(m, -c),
                  rule(m, ys[0]) if ys[0] and ys[0] != c else rule(m + 1, c),
                  rule(m + 1, c - xs[0]), rule(-m, c), rule(m, c + 1 if c != -1 else c + 2)]
        tab = [f"x | {' | '.join(map(str, xs))}", f"y | {' | '.join(map(str, ys))}"]
        return _maths([text("ตารางแสดงความสัมพันธ์ระหว่าง x และ y" + NL + NL.join(tab)),
                       text("สมการใดแสดงความสัมพันธ์นี้")], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)

"""กราฟความสัมพันธ์เชิงเส้น

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.1/2, ค 1.3 ม.1/3

Sets moved here from: math, math_diagrams, math_m1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
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


# ── More linear graphs (2026-11): which point is on a line, where a line meets the axes, quadrants, a table
# from an equation, a distance along a grid line, and how fast y grows ──

from otk.kit.math_problems import ChoiceType  # noqa: E402


def _line(m: int, c: int) -> str:
    return "y = " + poly_tex((m, "x"), (c, ""))


def _pt(p) -> str:
    return f"({p[0]}, {p[1]})"


@question_type("math.point_on_line_m1", display_name={"th": "จุดใดอยู่บนกราฟ"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class PointOnLineM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice([v for v in range(-4, 5) if v])
        c = rng.randint(-6, 6)
        x = rng.choice([v for v in range(-4, 5) if v])
        right = (x, m * x + c)
        # x and y swapped; y one off; the sign of x slipped.
        wrongs = [(right[1], right[0]), (x, right[1] + 1), (-x, right[1]), (x, right[1] - 2)]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right and w[1] != m * w[0] + c][:3]
        return _maths([text("จุดใดอยู่บนกราฟของ"), content_math(_line(m, c))], _pt(right), [_pt(w) for w in wrongs],
                      self.topic)


@question_type("math.axis_intercepts_m1", display_name={"th": "จุดที่กราฟตัดแกน"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class AxisInterceptsM1(QuestionType):
    """On the y-axis x = 0; on the x-axis y = 0."""

    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice([v for v in range(-5, 6) if v])
        x0 = rng.choice([v for v in range(-6, 7) if v])
        c = -m * x0
        if rng.random() < 0.5:
            right = (0, c)
            wrongs = [(c, 0), (0, m), (x0, 0)]
            ask = "แกน Y"
        else:
            right = (x0, 0)
            wrongs = [(0, x0), (-x0, 0), (0, c)]
            ask = "แกน X"
        # When two of those coincide: the gradient read as the crossing, a sign slipped.
        wrongs = [w for w in dict.fromkeys([*wrongs, (m, 0), (0, -c), (-x0, 0), (0, c + m)]) if w != right][:3]
        return _maths([text("กราฟของ"), content_math(_line(m, c)), text(f"ตัด{ask}ที่จุดใด")], _pt(right),
                      [_pt(w) for w in wrongs], self.topic)


_QUADRANTS = ("จตุภาคที่ 1", "จตุภาคที่ 2", "จตุภาคที่ 3", "จตุภาคที่ 4")


@question_type("math.quadrant_m1", display_name={"th": "จุดอยู่ในจตุภาคใด"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class QuadrantM1(ChoiceType):
    def compose(self, rng: Random):
        x, y = rng.choice([v for v in range(-9, 10) if v]), rng.choice([v for v in range(-9, 10) if v])
        q = (0 if y > 0 else 3) if x > 0 else (1 if y > 0 else 2)
        return f"จุด {_pt((x, y))} อยู่ในจตุภาคใด", _QUADRANTS[q], [n for i, n in enumerate(_QUADRANTS) if i != q]


@question_type("math.table_from_equation_m1", display_name={"th": "เติมตารางจากสมการ"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class TableFromEquationM1(WordProblem):
    def expr(self, rng: Random):
        m = rng.choice([v for v in range(-4, 6) if v])
        c = rng.randint(-8, 8)
        xs = sorted(rng.sample(range(-3, 6), 4))
        hide = rng.randrange(4)
        ys = [m * x + c for x in xs]
        cells = ", ".join("?" if i == hide else f"({x}, {y})" for i, (x, y) in enumerate(zip(xs, ys)))
        cells = cells.replace("?", f"({xs[hide]}, ?)")
        right = ys[hide]
        prompt = f"จากสมการ {_line(m, c).replace('-', '−')} คู่อันดับ {cells} ค่าที่หายไปคือเท่าใด"
        # m and x added; c left out; the sign of c flipped.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(m + xs[hide] + c, m * xs[hide], m * xs[hide] - c, right + m,
                                                answer=right, lo=-99))


@question_type("math.grid_distance_m1", display_name={"th": "ระยะทางระหว่างจุดบนเส้นขนานแกน"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class GridDistanceM1(WordProblem):
    """Same x (or same y): the distance is the difference of the other coordinate."""

    def expr(self, rng: Random):
        a, b = rng.sample(range(-9, 10), 2)
        k = rng.randint(-9, 9)
        vertical = rng.random() < 0.5
        p, q = ((k, a), (k, b)) if vertical else ((a, k), (b, k))
        right = abs(a - b)
        # Added instead of subtracted; the shared coordinate; without the absolute value.
        return MathDraw("", str(right), prompt=f"จุด A{_pt(p)} และจุด B{_pt(q)} อยู่ห่างกันกี่หน่วย",
                        distractors=_story.keep(abs(a + b), abs(k), abs(a) + abs(b) if a * b < 0 else right + 2,
                                                right + 1, answer=right, lo=1))


@question_type("math.rate_of_change_m1", display_name={"th": "y เพิ่มขึ้นเท่าใดเมื่อ x เพิ่มขึ้น"},
               level=LEVEL, topic=_GRAPH_TOPIC)
class RateOfChangeM1(WordProblem):
    def expr(self, rng: Random):
        m = rng.choice([v for v in range(-6, 7) if v not in (0, 1)])
        c = rng.randint(-9, 9)
        k = rng.randint(2, 6)
        right = m * k
        prompt = (f"จากสมการ {_line(m, c).replace('-', '−')} ถ้า x เพิ่มขึ้น {k} แล้ว y เปลี่ยนไปเท่าใด "
                  f"(ตอบเป็นจำนวน ถ้าลดลงให้ตอบเป็นจำนวนลบ)")
        # m alone; m + k; m·k + c.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(m, m + k, right + c if c else right + 1, -right, answer=right, lo=-99))

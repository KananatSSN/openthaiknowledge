"""ทฤษฎีบทพีทาโกรัส

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/5

Sets moved here from: math, math_diagrams, math_geometry, math_m2.
"""

from __future__ import annotations

import math

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import (
    RIGHT_TRIANGLE_FIGURES,
    _img,
    _math_q,
    _nums,
    figure_alt,
)
from otk.sets._support.math_geometry import _TRIPLES
from otk.sets._support.math_m2 import LEVEL, triple

PROVENANCE = Provenance("original")


_PYTH_TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17)]


_PY_TOPIC = "ทฤษฎีบทพีทาโกรัส"


@question_type("math.pythagoras",
               display_name={"th": "ทฤษฎีบทพีทาโกรัส"}, level={"th": "ม.2"},
               topic="ทฤษฎีบทพีทาโกรัส")
class Pythagoras(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 5):
        a, b, c = rng.choice(_PYTH_TRIPLES)
        k = rng.randint(k_lo, k_hi)
        a, b, c = a * k, b * k, c * k
        if rng.random() < 0.5:
            a, b = b, a
        unknown = rng.choice(["a", "b", "c"])
        sides = {"a": str(a), "b": str(b), "c": str(c)}
        val = {"a": a, "b": b, "c": c}[unknown]
        sides[unknown] = "x"
        # a, b are legs; c is the hypotenuse (the prompt says so).
        problem = rf"a = {sides['a']}, \; b = {sides['b']}, \; c = {sides['c']}"
        return MathDraw(problem, rf"x = {val}", hint=r"a^2 + b^2 = c^2",
                        prompt="สามเหลี่ยมมุมฉาก (c คือด้านตรงข้ามมุมฉาก) จงหา x")


@question_type("math.pythagoras_figure_m2", display_name={"th": "หาความยาวด้านของรูปสามเหลี่ยมมุมฉากจากรูป"},
               level={"th": "ม.2"}, topic="ทฤษฎีบทพีทาโกรัส")
class PythagorasFigureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(RIGHT_TRIANGLE_FIGURES)
        a, b, c = f.dims
        x = {"a": a, "b": b, "c": c}[f.unknown]
        if f.unknown == "c":
            wrongs = _nums(a + b, b - a if b > a else a - b, c + 1, answer=x, lo=1)
        else:
            other = b if f.unknown == "a" else a
            wrongs = _nums(c - other, c + other, other, x + 1, answer=x, lo=1)
        return _math_q([text("จากรูป x ยาวกี่เซนติเมตร"), _img(f.asset_id, figure_alt(f))],
                       str(x), wrongs, self.topic)


@question_type("math.pythagoras_diagonal",
               display_name={"th": "พีทาโกรัส: เส้นทแยงมุมของสี่เหลี่ยม"},
               level={"th": "ม.2"}, topic="ทฤษฎีบทพีทาโกรัส")
class PythagorasDiagonal(WordProblem):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 6):
        a, b, c = rng.choice(_TRIPLES)
        k = rng.randint(k_lo, k_hi)
        a, b, c = a * k, b * k, c * k
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมผืนผ้ากว้าง {a} เซนติเมตร ยาว {b} เซนติเมตร เส้นทแยงมุมยาวกี่เซนติเมตร",
            f"สนามรูปสี่เหลี่ยมผืนผ้ากว้าง {a} เมตร ยาว {b} เมตร ถ้าเดินตัดทแยงมุมสนาม "
            f"จะเดินได้ระยะทางกี่เมตร",
            f"ป้ายโฆษณารูปสี่เหลี่ยมผืนผ้ากว้าง {a} เดซิเมตร ยาว {b} เดซิเมตร "
            f"ติดไฟเส้นตามแนวทแยงมุมของป้าย ไฟเส้นยาวกี่เดซิเมตร",
        ))
        return MathDraw(
            "", str(c), prompt=prompt,
            hint=r"a^2 + b^2 = c^2",
            distractors=[str(a + b), str(abs(b - a)), str(2 * (a + b))])


@question_type("math.pythagoras_triple_check",
               display_name={"th": "เป็นสามเหลี่ยมมุมฉากหรือไม่"},
               level={"th": "ม.2"}, topic="ทฤษฎีบทพีทาโกรัส")
class PythagorasTripleCheck(ChoiceType):
    """The converse: the theorem also *tests* a triangle, not only measures one."""

    _KINDS = ("รูปสามเหลี่ยมมุมฉาก", "รูปสามเหลี่ยมมุมแหลม", "รูปสามเหลี่ยมมุมป้าน")

    def compose(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES)
        k = rng.randint(1, 4)
        a, b, c = a * k, b * k, c * k
        # c² = a² + b² is right; one less makes the largest angle acute, one
        # more makes it obtuse (a + b > c + 1 always holds for these triples).
        shift, kind = rng.choice(((0, self._KINDS[0]), (0, self._KINDS[0]), (-1, self._KINDS[1]),
                                  (1, self._KINDS[2])))
        s = c + shift
        stem = rng.choice((
            f"สามเหลี่ยมที่มีด้านยาว {a}, {b} และ {s} หน่วย เป็นรูปสามเหลี่ยมชนิดใด",
            f"ช่างไม้ต่อไม้สามท่อนยาว {a}, {b} และ {s} เซนติเมตร เป็นโครงรูปสามเหลี่ยม "
            f"โครงนี้เป็นรูปสามเหลี่ยมชนิดใด",
            f"ครูขึงเชือกเป็นรูปสามเหลี่ยมบนสนาม ด้านทั้งสามยาว {a}, {b} และ {s} เมตร "
            f"รูปที่ได้เป็นรูปสามเหลี่ยมชนิดใด",
        ))
        return stem, kind, [x for x in self._KINDS if x != kind] + ["ไม่สามารถสร้างรูปสามเหลี่ยมได้"]


@question_type("math.pythagoras_word_problem_m2",
               display_name={"th": "โจทย์ปัญหาทฤษฎีบทพีทาโกรัส"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasWordProblemM2(WordProblem):
    def expr(self, rng: Random):
        a, b, c = triple(rng, 4)
        kind = rng.randrange(5)
        if kind == 0:
            ans = b
            prompt = (f"บันไดยาว {c} ฟุต พาดกับกำแพงตั้งตรง โคนบันไดอยู่ห่างจากกำแพง {a} ฟุต "
                      f"ปลายบันไดอยู่สูงจากพื้นกี่ฟุต")
            wrongs = [c - a, c + a, a + b, c]
        elif kind == 1:
            ans = c
            prompt = (f"จอโทรทัศน์รูปสี่เหลี่ยมผืนผ้ากว้าง {b} นิ้ว สูง {a} นิ้ว "
                      f"เส้นทแยงมุมของจอยาวกี่นิ้ว")
            wrongs = [a + b, b - a + c, c + a, b]
        elif kind == 2:
            ans = c
            p = rng.choice(_story.NAMES)
            prompt = (f"{p}เดินไปทางทิศเหนือ {a * 10} เมตร แล้วเลี้ยวขวาเดินไปทางทิศตะวันออก {b * 10} เมตร "
                      f"ขณะนี้{p}อยู่ห่างจากจุดเริ่มต้นเป็นเส้นตรงกี่เมตร")
            ans, wrongs = c * 10, [(a + b) * 10, (b - a) * 10, c * 10 + 10]
        elif kind == 3:
            ans = b
            prompt = (f"ว่าวติดเชือกยาว {c} เมตร ตึงเป็นเส้นตรง จุดที่อยู่ใต้ว่าวบนพื้นห่างจากคนถือเชือก "
                      f"{a} เมตร ว่าวอยู่สูงจากพื้นกี่เมตร (ไม่คิดความสูงของคน)")
            wrongs = [c - a, c + a, a, c]
        else:
            ans = c
            prompt = (f"ทางลาดสำหรับรถเข็นสูง {a * 10} เซนติเมตร ระยะตามแนวราบยาว {b * 10} เซนติเมตร "
                      f"ทางลาดยาวกี่เซนติเมตร")
            ans, wrongs = c * 10, [(a + b) * 10, (b - a) * 10, c * 10 + 10]
        return MathDraw("", str(ans), prompt=prompt,
                        # Adding or subtracting the sides instead of their squares.
                        distractors=_story.keep(*wrongs, answer=ans, lo=1))


@question_type("math.pythagoras_grid_distance_m2",
               display_name={"th": "ระยะห่างระหว่างจุดสองจุดบนระนาบพิกัดฉาก"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasGridDistanceM2(MathType):
    def expr(self, rng: Random):
        a, b, c = triple(rng, 2)
        if rng.random() < 0.5:
            a, b = b, a
        x1, y1 = rng.randint(-9, 9), rng.randint(-9, 9)
        x2, y2 = x1 + rng.choice((a, -a)), y1 + rng.choice((b, -b))
        return MathDraw(rf"A({x1}, {y1}),\ B({x2}, {y2})", str(c),
                        prompt="จุด A และ B อยู่ห่างกันกี่หน่วย",
                        # Adding the two legs, and the difference of the legs.
                        distractors=_story.keep(a + b, abs(b - a), c * c, c + 1, answer=c, lo=1))


# ── More Pythagoras (สสวท. ม.2 เล่ม 1 บทที่ 1): the height of an isosceles triangle, a rectangle's side from
# its diagonal, a ladder that slides, and the diagonal of a box ──


def _legs(rng: Random, k_hi: int = 4) -> tuple[int, int, int]:
    a, b, c = triple(rng, k_hi)
    return (a, b, c) if rng.random() < 0.5 else (b, a, c)


@question_type("math.pythagoras_isosceles_m2", display_name={"th": "ส่วนสูงของรูปสามเหลี่ยมหน้าจั่ว"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasIsoscelesM2(WordProblem):
    """The height from the apex halves the base: (half base)² + height² = side²."""

    def expr(self, rng: Random):
        half, height, side = _legs(rng, 3)
        lead = (f"รูปสามเหลี่ยมหน้าจั่ว ABC มี AB = AC = {side} เซนติเมตร และฐาน BC ยาว {2 * half} เซนติเมตร ")
        if rng.random() < 0.5:
            # The whole base used; side less half base; the side itself.
            return MathDraw("", str(height), prompt=lead + "ส่วนสูงจากจุด A ถึงฐานยาวกี่เซนติเมตร",
                            distractors=_story.keep(side - half, side + half, side, 2 * height, answer=height, lo=1))
        area = half * height
        # The half forgotten; the side used as the height; half of the half.
        return MathDraw("", str(area), prompt=lead + "มีพื้นที่กี่ตารางเซนติเมตร",
                        distractors=_story.keep(2 * area, half * side, area // 2 if area % 2 == 0 else 0,
                                                2 * half * side, answer=area, lo=1))


@question_type("math.pythagoras_rectangle_m2", display_name={"th": "ด้านและพื้นที่ของรูปสี่เหลี่ยมผืนผ้าจากเส้นทแยงมุม"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasRectangleM2(WordProblem):
    """Given the diagonal and one side, the other side first, then the area or perimeter."""

    def expr(self, rng: Random):
        a, b, c = _legs(rng)
        lead = f"รูปสี่เหลี่ยมผืนผ้ามีเส้นทแยงมุมยาว {c} เซนติเมตร และด้านหนึ่งยาว {a} เซนติเมตร "
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(b), prompt=lead + "อีกด้านหนึ่งยาวกี่เซนติเมตร",
                            distractors=_story.keep(c - a, c + a, c, answer=b, lo=1))
        if kind == 1:
            # The diagonal used as a side; the diagonal times the side halved.
            return MathDraw("", str(a * b), prompt=lead + "มีพื้นที่กี่ตารางเซนติเมตร",
                            distractors=_story.keep(a * c, a * (c - a), a * b // 2 if a * b % 2 == 0 else 0,
                                                    answer=a * b, lo=1))
        per = 2 * (a + b)
        return MathDraw("", str(per), prompt=lead + "มีความยาวรอบรูปกี่เซนติเมตร",
                        distractors=_story.keep(2 * (a + c), a + b, a + b + c, answer=per, lo=1))


# A ladder of one length in two positions: (length, foot then, top then, foot after, top after).
_LADDERS = ((25, 7, 24, 15, 20), (50, 14, 48, 30, 40), (65, 25, 60, 39, 52), (65, 16, 63, 33, 56),
            (65, 33, 56, 39, 52), (75, 21, 72, 45, 60))


@question_type("math.pythagoras_ladder_m2", display_name={"th": "บันไดพิงกำแพงเลื่อนลง"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasLadderM2(WordProblem):
    """Two right triangles with the same hypotenuse: how far the top slides down."""

    def expr(self, rng: Random):
        length, foot, top, foot2, top2 = rng.choice(_LADDERS)
        lead = f"บันไดยาว {length} เดซิเมตร พิงกำแพงตั้งตรง ปลายล่างของบันไดห่างจากกำแพง {foot} เดซิเมตร "
        if rng.random() < 0.4:
            # The length less the gap; the two added; the length itself.
            return MathDraw("", str(top), prompt=lead + "ปลายบนของบันไดอยู่สูงจากพื้นกี่เดซิเมตร",
                            distractors=_story.keep(length - foot, length + foot, length, answer=top, lo=1))
        slide = top - top2
        prompt = lead + f"ถ้าเลื่อนปลายล่างออกห่างจากกำแพงอีก {foot2 - foot} เดซิเมตร ปลายบนจะเลื่อนลงกี่เดซิเมตร"
        # The same distance as the foot; the new height; the old height.
        return MathDraw("", str(slide), prompt=prompt,
                        distractors=_story.keep(foot2 - foot, top2, top, slide + 2, answer=slide, lo=1))


# Boxes whose space diagonal is a whole number: (width, length, height, diagonal).
_BOXES = ((1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11),
          (3, 4, 12, 13), (2, 10, 11, 15), (8, 9, 12, 17), (4, 5, 20, 21))


@question_type("math.pythagoras_box_diagonal_m2", display_name={"th": "เส้นทแยงมุมของทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasBoxDiagonalM2(WordProblem):
    """Pythagoras twice: across the floor, then up to the far top corner."""

    def expr(self, rng: Random):
        w, d, h, diag = rng.choice(_BOXES)
        k = rng.randint(1, 3)
        w, d, h, diag = w * k, d * k, h * k, diag * k
        prompt = (f"กล่องทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {d} ซม. สูง {h} ซม. ระยะจากมุมล่างมุมหนึ่ง"
                  f"ไปยังมุมบนที่อยู่ตรงข้ามกันยาวกี่เซนติเมตร")
        # The three edges added; one past; the longest edge.
        return MathDraw("", str(diag), prompt=prompt,
                        distractors=_story.keep(w + d + h, diag + k, diag - k, d + h, answer=diag, lo=1))


# ── To fifteen (2026-11): squares on the sides, a rhombus, perimeter and area of a right triangle, an
# isosceles trapezoid, and two right triangles sharing a leg ──


@question_type("math.pythagoras_square_areas_m2", display_name={"th": "พื้นที่ของรูปสี่เหลี่ยมจัตุรัสบนด้านของรูปสามเหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasSquareAreasM2(WordProblem):
    """The square on the hypotenuse has the area of the other two together."""

    def expr(self, rng: Random):
        a, b, c = _legs(rng, 3)
        lead = "สร้างรูปสี่เหลี่ยมจัตุรัสบนด้านทั้งสามของรูปสามเหลี่ยมมุมฉาก "
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(c * c), prompt=lead + (f"ถ้ารูปบนด้านประกอบมุมฉากมีพื้นที่ {a * a} และ {b * b} ตารางหน่วย "
                                                          f"รูปบนด้านตรงข้ามมุมฉากมีพื้นที่กี่ตารางหน่วย"),
                            distractors=_story.keep(a + b, (a + b) ** 2, c, abs(a * a - b * b), answer=c * c, lo=1))
        if kind == 1:
            return MathDraw("", str(b * b), prompt=lead + (f"ถ้ารูปบนด้านตรงข้ามมุมฉากมีพื้นที่ {c * c} ตารางหน่วย และรูปบนด้าน"
                                                          f"ประกอบมุมฉากด้านหนึ่งมีพื้นที่ {a * a} ตารางหน่วย อีกรูปหนึ่งมีพื้นที่กี่ตารางหน่วย"),
                            distractors=_story.keep(c * c + a * a, b, c - a, (c - a) ** 2, answer=b * b, lo=1))
        return MathDraw("", str(c), prompt=lead + (f"ถ้ารูปบนด้านประกอบมุมฉากมีพื้นที่ {a * a} และ {b * b} ตารางหน่วย "
                                                  f"ด้านตรงข้ามมุมฉากยาวกี่หน่วย"),
                        distractors=_story.keep(c * c, a + b, c + 1, b + 1, answer=c, lo=1))


@question_type("math.pythagoras_rhombus_m2", display_name={"th": "ด้านและเส้นทแยงมุมของรูปสี่เหลี่ยมขนมเปียกปูน"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasRhombusM2(WordProblem):
    """The diagonals bisect each other at right angles: half of each and a side make a right triangle."""

    def expr(self, rng: Random):
        a, b, c = _legs(rng, 3)
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(c), prompt=(f"รูปสี่เหลี่ยมขนมเปียกปูนมีเส้นทแยงมุมยาว {2 * a} และ {2 * b} เซนติเมตร "
                                               f"ด้านยาวด้านละกี่เซนติเมตร"),
                            # The full diagonals used; their halves added; their sum halved.
                            distractors=_story.keep(2 * c, a + b, c + 1, c - 1, answer=c, lo=1))
        if kind == 1:
            return MathDraw("", str(2 * b), prompt=(f"รูปสี่เหลี่ยมขนมเปียกปูนยาวด้านละ {c} เซนติเมตร และมีเส้นทแยงมุมเส้นหนึ่ง"
                                                   f"ยาว {2 * a} เซนติเมตร เส้นทแยงมุมอีกเส้นยาวกี่เซนติเมตร"),
                            distractors=_story.keep(b, 2 * c - 2 * a, c, 2 * b + 2, answer=2 * b, lo=1))
        area = 2 * a * b
        return MathDraw("", str(area), prompt=(f"รูปสี่เหลี่ยมขนมเปียกปูนยาวด้านละ {c} เซนติเมตร และมีเส้นทแยงมุมเส้นหนึ่ง"
                                              f"ยาว {2 * a} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร"),
                        # The half forgotten; the side times the diagonal; half the diagonals' halves.
                        distractors=_story.keep(4 * a * b, 2 * a * c, a * b, c * c, answer=area, lo=1))


@question_type("math.pythagoras_triangle_perimeter_m2", display_name={"th": "ความยาวรอบรูปและพื้นที่ของรูปสามเหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasTrianglePerimeterM2(WordProblem):
    def expr(self, rng: Random):
        a, b, c = _legs(rng)
        if rng.random() < 0.5:
            per = a + b + c
            return MathDraw("", str(per), prompt=(f"รูปสามเหลี่ยมมุมฉากมีด้านประกอบมุมฉากยาว {a} และ {b} เซนติเมตร "
                                                 f"มีความยาวรอบรูปกี่เซนติเมตร"),
                            # The two legs only; the hypotenuse doubled; the legs' squares added.
                            distractors=_story.keep(a + b, a + b + a + b, 2 * c + a, per + 1, answer=per, lo=1))
        area = a * b // 2
        return MathDraw("", str(area), prompt=(f"รูปสามเหลี่ยมมุมฉากมีด้านตรงข้ามมุมฉากยาว {c} เซนติเมตร และด้านประกอบมุมฉาก"
                                              f"ด้านหนึ่งยาว {a} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร"),
                        # The hypotenuse used as the height; the half forgotten.
                        distractors=_story.keep(a * c // 2 if a * c % 2 == 0 else a * c, a * b, a * c, area + a,
                                                answer=area, lo=1))


@question_type("math.pythagoras_trapezoid_m2", display_name={"th": "ส่วนสูงและพื้นที่ของรูปสี่เหลี่ยมคางหมูหน้าจั่ว"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasTrapezoidM2(WordProblem):
    """Drop heights from the short base: each end cuts off (B − b)/2, the leg is the hypotenuse."""

    def expr(self, rng: Random):
        a, h, c = _legs(rng, 3)
        b = rng.randint(2, 12)
        big = b + 2 * a
        lead = (f"รูปสี่เหลี่ยมคางหมูหน้าจั่วมีด้านคู่ขนานยาว {b} และ {big} เซนติเมตร "
                f"และด้านที่ไม่ขนานยาวด้านละ {c} เซนติเมตร ")
        if rng.random() < 0.5:
            # The whole difference of the bases used; the leg itself.
            wrong = math.isqrt(c * c - (big - b) ** 2) if c > big - b else 0
            return MathDraw("", str(h), prompt=lead + "สูงกี่เซนติเมตร",
                            distractors=_story.keep(wrong, c, c - a, h + 1, h + 2, answer=h, lo=1))
        area = (b + big) * h // 2
        return MathDraw("", str(area), prompt=lead + "มีพื้นที่กี่ตารางเซนติเมตร",
                        distractors=_story.keep((b + big) * h, (b + big) * c // 2 if (b + big) * c % 2 == 0 else 0,
                                                big * h, b * h, answer=area, lo=1))


# Right triangles sharing a leg L: (L, the other legs, their hypotenuses).
_SHARED = ((12, ((5, 13), (9, 15), (16, 20), (35, 37))), (24, ((7, 25), (10, 26), (18, 30), (32, 40))),
           (15, ((8, 17), (20, 25), (36, 39))), (20, ((15, 25), (21, 29), (48, 52))))


@question_type("math.pythagoras_two_step_m2", display_name={"th": "ใช้ทฤษฎีบทพีทาโกรัสสองครั้ง"},
               level=LEVEL, topic=_PY_TOPIC)
class PythagorasTwoStepM2(WordProblem):
    """C and D on one leg's line: BC and BD from two triangles with the leg AB in common, then CD."""

    def expr(self, rng: Random):
        leg, options = rng.choice(_SHARED)
        (m1, h1), (m2, h2) = sorted(rng.sample(options, 2))
        prompt = (f"รูปสามเหลี่ยม ABD มีมุม B เป็นมุมฉาก จุด C อยู่บน BD ถ้า AB = {leg} ซม. AC = {h1} ซม. "
                  f"และ AD = {h2} ซม. แล้ว CD ยาวกี่เซนติเมตร")
        right = m2 - m1
        # The hypotenuses subtracted; BD or BC alone; the two added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(h2 - h1, m2, m1, m1 + m2, answer=right, lo=1))

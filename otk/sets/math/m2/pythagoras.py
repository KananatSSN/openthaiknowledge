"""ทฤษฎีบทพีทาโกรัส

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/5

Sets moved here from: math, math_diagrams, math_geometry, math_m2.
"""

from __future__ import annotations

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

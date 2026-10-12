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

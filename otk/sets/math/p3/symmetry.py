"""รูปสมมาตร

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.3/*

Sets moved here from: math, math_apply_stage, math_diagrams_geo, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import SYMMETRY_SHAPES
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_geometry import _POLYGONS
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


_SYMMETRIC = (("ป้ายหยุดรูปแปดเหลี่ยมด้านเท่ามุมเท่า", 8), ("ธงชาติไทย", 2), ("ผีเสื้อ", 1),
              ("ป้ายเตือนรูปสามเหลี่ยมด้านเท่า", 3), ("หน้าต่างรูปสี่เหลี่ยมจัตุรัส", 4), ("ตัวเลข 8", 2),
              ("ตัวเลข 3", 1), ("ใบโพธิ์", 1), ("ดาวห้าแฉกที่ทุกแฉกเท่ากัน", 5), ("ประตูรูปสี่เหลี่ยมผืนผ้า", 2))


_ASYMMETRIC = ("ตัวเลข 7", "ตัวเลข 4", "ตัวอักษร F", "ตัวอักษร G")


SYMMETRY_ALT = "รูปเรขาคณิตสองมิติหนึ่งรูป"


@question_type("math.symmetry_axes",
               display_name={"th": "จำนวนแกนสมมาตร"}, level={"th": "ป.3"},
               topic="รูปสมมาตร")
class SymmetryAxes(WordProblem):
    _AXES = {"สามเหลี่ยมด้านเท่า": 3, "สี่เหลี่ยมจัตุรัส": 4,
             "สี่เหลี่ยมผืนผ้า": 2, "สามเหลี่ยมหน้าจั่ว": 1,
             "สามเหลี่ยมที่ด้านทั้งสามยาวไม่เท่ากัน": 0,
             "ห้าเหลี่ยมด้านเท่ามุมเท่า": 5, "หกเหลี่ยมด้านเท่ามุมเท่า": 6,
             "ครึ่งวงกลม": 1, "หัวใจ": 1, "ดาวห้าแฉกที่ทุกแฉกเท่ากัน": 5}

    def expr(self, rng: Random):
        shape = rng.choice(list(self._AXES))
        answer = self._AXES[shape]
        near = sorted({v for v in self._AXES.values() if v != answer}, key=lambda v: abs(v - answer))
        others = [str(v) for v in near]
        return MathDraw("", str(answer),
                        prompt=f"รูป{shape}มีแกนสมมาตรกี่แกน?",
                        distractors=others)


@question_type("math.symmetry_picture_p3", display_name={"th": "นับแกนสมมาตรจากรูป"},
               level={"th": "ป.3"}, topic="รูปสมมาตร")
class SymmetryPictureP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SYMMETRY_SHAPES)
        n = s.axes
        # One too few or many, the number of sides, and twice the answer.
        wrongs = [str(n + 1), str(abs(n - 1)) if n != 1 else "2", str(n + 2), str(2 * n) if n > 2 else "0"]
        return _math_q([text("รูปนี้มีแกนสมมาตรกี่แกน"), _img(s.asset_id, SYMMETRY_ALT)], str(n), wrongs,
                       self.topic)


@question_type("math.symmetry_letter", display_name={"th": "แกนสมมาตรของตัวอักษร"},
               level={"th": "ป.3"}, topic="รูปสมมาตร")
class SymmetryLetter(WordProblem):
    # Latin capitals, whose axes of symmetry are unambiguous in print.
    LETTERS = [("A", 1), ("B", 1), ("C", 1), ("D", 1), ("E", 1), ("H", 2),
               ("I", 2), ("M", 1), ("O", 2), ("T", 1), ("U", 1), ("V", 1),
               ("W", 1), ("X", 2), ("Y", 1), ("F", 0), ("G", 0), ("J", 0),
               ("L", 0), ("N", 0), ("P", 0), ("Q", 0), ("R", 0), ("S", 0),
               ("Z", 0)]

    def expr(self, rng: Random):
        letter, axes = rng.choice(self.LETTERS)
        return MathDraw("", str(axes),
                        prompt=f"ตัวอักษร {letter} (ตัวพิมพ์ใหญ่) มีแกนสมมาตรกี่แกน",
                        distractors=[str(axes + 1), str(axes + 2),
                                     str(abs(axes - 1))])


@question_type("math.symmetry_word_p3", display_name={"th": "แกนสมมาตรของสิ่งของรอบตัว"},
               level={"th": "ป.3"}, topic="รูปสมมาตร")
class SymmetryWordP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            thing, axes = rng.choice(_SYMMETRIC)
            return maths([text(f"{thing}มีแกนสมมาตรกี่แกน")], str(axes),
                         _nums(axes, axes + 1, axes - 1, axes * 2, lo=0), self.topic)
        if kind == 1:
            right = rng.choice(_ASYMMETRIC)
            return _choices([text("สิ่งใดไม่มีแกนสมมาตร")], right,
                            [t for t, _ in rng.sample(_SYMMETRIC, 3)], self.topic)
        stem = "พับกระดาษครึ่งหนึ่ง แล้วตัดเป็นรูปหนึ่งโดยไม่ตัดรอยพับออก เมื่อคลี่ออก รอยพับเป็นอะไรของรูปที่ได้"
        return _choices([text(stem)], "แกนสมมาตร", ["เส้นทแยงมุม", "ด้านของรูป", "เส้นรอบรูป"], self.topic)


@question_type("math.symmetry_regular_polygon",
               display_name={"th": "แกนสมมาตรของรูปหลายเหลี่ยมด้านเท่า"},
               level={"th": "ป.3"}, topic="รูปสมมาตร")
class SymmetryRegularPolygon(WordProblem):
    """A regular n-gon has exactly n axes — one per vertex or per edge midpoint."""

    def expr(self, rng: Random, sides_lo: int = 3, sides_hi: int = 10):
        name, n = rng.choice([p for p in _POLYGONS if sides_lo <= p[1] <= sides_hi])
        if rng.random() < 0.5:
            prompt = f"{name}ด้านเท่ามุมเท่ามีแกนสมมาตรกี่แกน"
        else:
            prompt = f"รูปหลายเหลี่ยมด้านเท่ามุมเท่ารูปหนึ่งมีแกนสมมาตร {n} แกน รูปนี้มีกี่ด้าน"
        return MathDraw("", str(n), prompt=prompt,
                        distractors=[str(n - 1), str(n + 1), str(n * 2)])

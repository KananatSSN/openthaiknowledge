"""ชนิดของรูปสามเหลี่ยม

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.6/*

Sets moved here from: math, math_diagrams_geo, math_gaps_shape_data, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q, _text_q
from otk.sets._support.math_diagrams_geo import TRI_ANGLES, TRI_SIDES, MarkedTriangle
from otk.sets._support.math_gaps_shape_data import _ConstructionSteps

PROVENANCE = Provenance("original")


def triangle_alt(t: MarkedTriangle) -> str:
    if t.sides:
        return "รูปสามเหลี่ยม ABC ด้าน AB ยาว {} ซม. ด้าน BC ยาว {} ซม. ด้าน CA ยาว {} ซม.".format(*t.sides)
    a, b, c = t.angles
    third = f"{c} องศา" if t.shown == "abc" else "x"
    return f"รูปสามเหลี่ยม ABC มุม A กำกับ {a} องศา มุม B กำกับ {b} องศา มุม C กำกับ {third}"


_BY_ANGLE = ("รูปสามเหลี่ยมมุมแหลม", "รูปสามเหลี่ยมมุมฉาก", "รูปสามเหลี่ยมมุมป้าน")


_BY_SIDE = ("รูปสามเหลี่ยมด้านเท่า", "รูปสามเหลี่ยมหน้าจั่ว", "รูปสามเหลี่ยมด้านไม่เท่า")


def angle_kind(angles) -> str:
    top = max(angles)
    return _BY_ANGLE[0 if top < 90 else 1 if top == 90 else 2]


def side_kind(sides) -> str:
    return _BY_SIDE[{1: 0, 2: 1, 3: 2}[len(set(sides))]]


@question_type("math.triangle_type_picture_p6", display_name={"th": "จำแนกชนิดของรูปสามเหลี่ยมจากรูป"},
               level={"th": "ป.6"}, topic="ชนิดของรูปสามเหลี่ยม")
class TriangleTypePictureP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(TRI_ANGLES + TRI_SIDES)
        img = _img(t.asset_id, triangle_alt(t))
        if t.sides:
            right = side_kind(t.sides)
            return _text_q([text("รูปสามเหลี่ยมนี้เป็นรูปสามเหลี่ยมชนิดใด เมื่อจำแนกตามความยาวของด้าน"), img],
                           right, [k for k in _BY_SIDE if k != right] + ["รูปสามเหลี่ยมมุมฉาก"], self.topic)
        a, b, c = t.angles
        if t.shown == "ab" and rng.random() < 0.5:
            return _math_q([text("จงหาขนาดของมุม x (องศา)"), img], str(c),
                           [str(a + b), str(180 - a), str(360 - a - b)], self.topic)
        ask = "เมื่อจำแนกตามขนาดของมุม" + (" (หาขนาดของมุม x ก่อน)" if t.shown == "ab" else "")
        right = angle_kind(t.angles)
        return _text_q([text(f"รูปสามเหลี่ยมนี้เป็นรูปสามเหลี่ยมชนิดใด {ask}"), img], right,
                       [k for k in _BY_ANGLE if k != right] + ["รูปสามเหลี่ยมด้านเท่า"], self.topic)


@question_type("math.classify_triangle_by_angle",
               display_name={"th": "จำแนกสามเหลี่ยมตามมุม"}, level={"th": "ป.6"},
               topic="ชนิดของรูปสามเหลี่ยม")
class ClassifyTriangleByAngle(ChoiceType):
    _LABELS = ["สามเหลี่ยมมุมแหลม", "สามเหลี่ยมมุมฉาก", "สามเหลี่ยมมุมป้าน"]

    def compose(self, rng: Random):
        kind = rng.choice(self._LABELS)
        if kind == "สามเหลี่ยมมุมฉาก":
            b = rng.randint(20, 70)
            angles = [90, b, 90 - b]
        elif kind == "สามเหลี่ยมมุมป้าน":
            a = rng.randint(91, 140)
            b = rng.randint(20, 180 - a - 10)
            angles = [a, b, 180 - a - b]
        else:
            while True:
                a, b = rng.randint(40, 80), rng.randint(40, 80)
                c = 180 - a - b
                if 0 < c < 90 and a < 90 and b < 90:
                    angles = [a, b, c]
                    break
        rng.shuffle(angles)
        stem = (f"สามเหลี่ยมที่มีมุม {angles[0]}°, {angles[1]}°, {angles[2]}° "
                f"เป็นสามเหลี่ยมชนิดใด (ตามมุม)?")
        return stem, kind, [x for x in self._LABELS if x != kind]


@question_type("math.construct_triangle_p6", display_name={"th": "ขั้นตอนการสร้างรูปสามเหลี่ยม"},
               level={"th": "ป.6"}, topic="ชนิดของรูปสามเหลี่ยม")
class ConstructTriangleP6(_ConstructionSteps):
    def procedures(self, rng):
        if rng.random() < 0.5:
            c, b, t = rng.randint(5, 9), rng.randint(3, 7), rng.choice((40, 50, 60, 70, 100, 120))
            goal = (f"การสร้างรูปสามเหลี่ยม ABC ที่มี AB ยาว {c} เซนติเมตร "
                    f"มุม BAC ขนาด {t} องศา และ AC ยาว {b} เซนติเมตร")
            steps = [
                f"ลากส่วนของเส้นตรง AB ยาว {c} เซนติเมตร",
                f"ที่จุด A ใช้โพรแทรกเตอร์สร้างมุมขนาด {t} องศา",
                f"บนแขนของมุมที่สร้าง วัดจากจุด A ยาว {b} เซนติเมตร ได้จุด C",
                "ลากส่วนของเส้นตรง BC",
            ]
            faulty = [f"ที่จุด B สร้างมุมขนาด {t} องศา",
                      f"จากจุด B วัดยาว {b} เซนติเมตร ได้จุด C"]
            return goal, steps, faulty
        while True:
            a, b, c = rng.randint(4, 9), rng.randint(3, 8), rng.randint(3, 8)
            # b ≠ c: with equal radii the faulty "radius b from B" step would
            # be a correct step.
            if a < b + c and b < a + c and c < a + b and b != c:
                break
        goal = (f"การสร้างรูปสามเหลี่ยม ABC ที่มี BC ยาว {a} เซนติเมตร "
                f"AC ยาว {b} เซนติเมตร และ AB ยาว {c} เซนติเมตร")
        steps = [
            f"ลากส่วนของเส้นตรง BC ยาว {a} เซนติเมตร",
            f"กางวงเวียนยาว {b} เซนติเมตร ใช้จุด C เป็นจุดศูนย์กลาง เขียนส่วนโค้ง",
            f"กางวงเวียนยาว {c} เซนติเมตร ใช้จุด B เป็นจุดศูนย์กลาง เขียนส่วนโค้งตัดส่วนโค้งแรกที่จุด A",
            "ลากส่วนของเส้นตรง AB และ AC",
        ]
        faulty = [f"กางวงเวียนยาว {b} เซนติเมตร ใช้จุด B เป็นจุดศูนย์กลาง เขียนส่วนโค้ง",
                  f"ที่จุด B ใช้โพรแทรกเตอร์สร้างมุมฉาก แล้ววัดยาว {c} เซนติเมตร"]
        return goal, steps, faulty


@question_type("math.triangle_missing_angle",
               display_name={"th": "มุมที่หายไปของรูปสามเหลี่ยม"},
               level={"th": "ป.6"}, topic="ชนิดของรูปสามเหลี่ยม")
class TriangleMissingAngle(WordProblem):
    def expr(self, rng: Random, lo: int = 20, hi: int = 120):
        a = rng.randint(lo, min(hi, 130))
        b = rng.randint(lo, max(lo + 1, 175 - a))
        c = 180 - a - b
        prompt = rng.choice((
            f"รูปสามเหลี่ยมรูปหนึ่งมีมุมสองมุมขนาด {a} และ {b} องศา มุมที่สามมีขนาดกี่องศา",
            f"รูปสามเหลี่ยม ABC มี ∠A = {a}° และ ∠B = {b}° จงหาขนาดของ ∠C (องศา)",
            f"ธงชายรูปสามเหลี่ยมผืนหนึ่งมีมุมสองมุมขนาด {a} และ {b} องศา "
            f"มุมที่สามของธงมีขนาดกี่องศา",
        ))
        return MathDraw(
            "", str(c), prompt=prompt,
            distractors=[str(a + b), str(360 - a - b), str(90 - min(a, b))])

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

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More types of triangles (2026-11): naming by sides, the base angles and the top angle of an isosceles
# triangle, the other acute angle of a right triangle, facts about triangles, and a side from the
# perimeter ──


@question_type("math.classify_by_sides_p6", display_name={"th": "จำแนกรูปสามเหลี่ยมตามความยาวของด้าน"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class ClassifyBySidesP6(ChoiceType):
    _KINDS = ("รูปสามเหลี่ยมด้านเท่า", "รูปสามเหลี่ยมหน้าจั่ว", "รูปสามเหลี่ยมด้านไม่เท่า")

    def compose(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            a = rng.randint(3, 20)
            sides = [a, a, a]
        elif kind == 1:
            a, b = rng.sample(range(4, 20), 2)
            if 2 * a <= b:
                a, b = b, a
            sides = [a, a, b]
        else:
            while True:
                sides = sorted(rng.sample(range(3, 20), 3))
                if sides[0] + sides[1] > sides[2]:
                    break
        rng.shuffle(sides)
        stem = f"รูปสามเหลี่ยมที่มีด้านยาว {sides[0]}, {sides[1]} และ {sides[2]} เซนติเมตร เป็นรูปสามเหลี่ยมชนิดใด"
        right = self._KINDS[kind]
        return stem, right, [k for k in self._KINDS if k != right] + ["รูปสามเหลี่ยมมุมฉาก"]


@question_type("math.isosceles_base_angle_p6", display_name={"th": "มุมที่ฐานของรูปสามเหลี่ยมหน้าจั่ว"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class IsoscelesBaseAngleP6(WordProblem):
    def expr(self, rng: Random):
        top = rng.randint(10, 80) * 2
        right = (180 - top) // 2
        prompt = f"รูปสามเหลี่ยมหน้าจั่วมีมุมยอดขนาด {top} องศา มุมที่ฐานแต่ละมุมมีขนาดกี่องศา"
        # Not halved; the top angle itself; taken as 90 less half.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - top, top, 90 + top // 2, right + 10, answer=right, lo=1))


@question_type("math.isosceles_top_angle_p6", display_name={"th": "มุมยอดของรูปสามเหลี่ยมหน้าจั่ว"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class IsoscelesTopAngleP6(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(20, 85)
        right = 180 - 2 * base
        prompt = f"รูปสามเหลี่ยมหน้าจั่วมีมุมที่ฐานมุมหนึ่งขนาด {base} องศา มุมยอดมีขนาดกี่องศา"
        # One base angle taken off; the base angle itself; doubled.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - base, base, 2 * base, right + 10, answer=right, lo=1))


@question_type("math.right_triangle_other_angle_p6", display_name={"th": "มุมแหลมอีกมุมของรูปสามเหลี่ยมมุมฉาก"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class RightTriangleOtherAngleP6(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(10, 80)
        while a == 45:
            a = rng.randint(10, 80)
        right = 90 - a
        prompt = f"รูปสามเหลี่ยมมุมฉากมีมุมแหลมมุมหนึ่งขนาด {a} องศา มุมแหลมอีกมุมมีขนาดกี่องศา"
        # The right angle forgotten; the given angle; added to a straight angle.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - a, a, 270 - a, right + 10, answer=right, lo=1))


@question_type("math.triangle_facts_p6", display_name={"th": "สมบัติของรูปสามเหลี่ยม"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class TriangleFactsP6(ConceptBankType):
    ITEMS = [
        Concept("มุมภายในทั้งสามมุมของรูปสามเหลี่ยมรวมกันได้กี่องศา", "180 องศา",
                ("90 องศา", "360 องศา", "270 องศา")),
        Concept("รูปสามเหลี่ยมด้านเท่ามีมุมแต่ละมุมขนาดกี่องศา", "60 องศา", ("45 องศา", "90 องศา", "30 องศา")),
        Concept("รูปสามเหลี่ยมรูปหนึ่งมีมุมป้านได้มากที่สุดกี่มุม", "1 มุม", ("2 มุม", "3 มุม", "ไม่มีเลย")),
        Concept("รูปสามเหลี่ยมหน้าจั่วมีมุมที่มีขนาดเท่ากันอย่างน้อยกี่มุม", "2 มุม", ("1 มุม", "3 มุม", "ไม่มีเลย")),
        Concept("รูปสามเหลี่ยมที่มีมุมทุกมุมเป็นมุมแหลม เรียกว่ารูปสามเหลี่ยมชนิดใด", "รูปสามเหลี่ยมมุมแหลม",
                ("รูปสามเหลี่ยมมุมฉาก", "รูปสามเหลี่ยมมุมป้าน", "รูปสามเหลี่ยมด้านไม่เท่า")),
    ]


@question_type("math.isosceles_side_from_perimeter_p6", display_name={"th": "หาความยาวด้านจากความยาวรอบรูปสามเหลี่ยม"},
               level=LEVEL, topic="ชนิดของรูปสามเหลี่ยม")
class IsoscelesSideFromPerimeterP6(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            side = rng.randint(3, 30)
            perimeter = 3 * side
            prompt = f"รูปสามเหลี่ยมด้านเท่ายาวรอบรูป {perimeter} เซนติเมตร ด้านแต่ละด้านยาวกี่เซนติเมตร"
            right = side
            wrongs = (perimeter // 2, perimeter - side, side + 3)
        else:
            base = rng.randint(3, 20)
            leg = rng.randint(base // 2 + 2, 30)
            perimeter = base + 2 * leg
            prompt = (f"รูปสามเหลี่ยมหน้าจั่วมีฐานยาว {base} เซนติเมตร ยาวรอบรูป {perimeter} เซนติเมตร "
                      "ด้านที่ยาวเท่ากันแต่ละด้านยาวกี่เซนติเมตร")
            right = leg
            wrongs = (perimeter - base, perimeter // 3, (perimeter + base) // 2)
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(*wrongs, right + 1, answer=right, lo=1))

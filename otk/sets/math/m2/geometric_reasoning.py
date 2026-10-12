"""การให้เหตุผลทางเรขาคณิต

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math_chapters, math_gaps_shape_data.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_chapters import NL, _deg, _distinct
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_p2 import _texts

PROVENANCE = Provenance("original")


M2 = {"th": "ม.2"}


_REASON_TOPIC = "การให้เหตุผลทางเรขาคณิต"


def _angles(correct: int, *wrong: int) -> list[str]:
    """Degree choices strictly between 0° and 180°, answer excluded."""
    return _distinct(_deg(correct), *[_deg(w) for w in wrong if 0 < w < 180])


# (statement, its converse, whether the converse is true)
_CONVERSES = (
    ("ถ้ารูปสามเหลี่ยมมีด้านยาวเท่ากันสองด้าน แล้วมุมที่อยู่ตรงข้ามด้านทั้งสองมีขนาดเท่ากัน",
     "ถ้ารูปสามเหลี่ยมมีมุมสองมุมที่มีขนาดเท่ากัน แล้วด้านที่อยู่ตรงข้ามมุมทั้งสองยาวเท่ากัน", True),
    ("ถ้าเส้นตรงสองเส้นขนานกันและมีเส้นตัด แล้วมุมแย้งมีขนาดเท่ากัน",
     "ถ้าเส้นตัดเส้นตรงสองเส้นทำให้มุมแย้งมีขนาดเท่ากัน แล้วเส้นตรงสองเส้นนั้นขนานกัน", True),
    ("ถ้ารูปสามเหลี่ยมเป็นรูปสามเหลี่ยมมุมฉาก แล้วกำลังสองของด้านที่ยาวที่สุดเท่ากับผลบวกของกำลังสองของอีกสองด้าน",
     "ถ้ากำลังสองของด้านที่ยาวที่สุดของรูปสามเหลี่ยมเท่ากับผลบวกของกำลังสองของอีกสองด้าน "
     "แล้วรูปสามเหลี่ยมนั้นเป็นรูปสามเหลี่ยมมุมฉาก", True),
    ("ถ้ารูปสี่เหลี่ยมเป็นรูปสี่เหลี่ยมด้านขนาน แล้วเส้นทแยงมุมแบ่งครึ่งซึ่งกันและกัน",
     "ถ้าเส้นทแยงมุมของรูปสี่เหลี่ยมแบ่งครึ่งซึ่งกันและกัน แล้วรูปสี่เหลี่ยมนั้นเป็นรูปสี่เหลี่ยมด้านขนาน", True),
    ("ถ้ารูปสี่เหลี่ยมเป็นรูปสี่เหลี่ยมจัตุรัส แล้วด้านทั้งสี่ยาวเท่ากัน",
     "ถ้ารูปสี่เหลี่ยมมีด้านทั้งสี่ยาวเท่ากัน แล้วรูปสี่เหลี่ยมนั้นเป็นรูปสี่เหลี่ยมจัตุรัส", False),
    ("ถ้ามุมสองมุมเป็นมุมตรงข้ามที่เกิดจากเส้นตรงสองเส้นตัดกัน แล้วมุมทั้งสองมีขนาดเท่ากัน",
     "ถ้ามุมสองมุมมีขนาดเท่ากัน แล้วมุมทั้งสองเป็นมุมตรงข้ามที่เกิดจากเส้นตรงสองเส้นตัดกัน", False),
    ("ถ้ารูปสามเหลี่ยมสองรูปเท่ากันทุกประการ แล้วรูปสามเหลี่ยมทั้งสองมีพื้นที่เท่ากัน",
     "ถ้ารูปสามเหลี่ยมสองรูปมีพื้นที่เท่ากัน แล้วรูปสามเหลี่ยมทั้งสองเท่ากันทุกประการ", False),
    ("ถ้าจำนวนนับใดหารด้วย 4 ลงตัว แล้วจำนวนนั้นหารด้วย 2 ลงตัว",
     "ถ้าจำนวนนับใดหารด้วย 2 ลงตัว แล้วจำนวนนั้นหารด้วย 4 ลงตัว", False),
    ("ถ้ารูปสามเหลี่ยมมีมุมทั้งสามมีขนาดเท่ากัน แล้วด้านทั้งสามยาวเท่ากัน",
     "ถ้ารูปสามเหลี่ยมมีด้านทั้งสามยาวเท่ากัน แล้วมุมทั้งสามมีขนาดเท่ากัน", True),
    ("ถ้า x = 3 แล้ว x² = 9", "ถ้า x² = 9 แล้ว x = 3", False),
)


# (angle, a construction with compass and straightedge that makes it)
_ANGLE_METHODS = (
    (60, "สร้างรูปสามเหลี่ยมด้านเท่า แล้วใช้มุมหนึ่งของรูปนั้น"),
    (30, "สร้างมุม 60 องศา แล้วแบ่งครึ่งมุม"),
    (90, "สร้างเส้นตั้งฉากที่จุดบนเส้นตรง"),
    (45, "สร้างมุมฉาก แล้วแบ่งครึ่งมุม"),
    (120, "สร้างมุม 60 องศาบนเส้นตรง แล้วใช้มุมประกอบสองมุมฉากของมุมนั้น"),
    (15, "สร้างมุม 60 องศา แบ่งครึ่งได้ 30 องศา แล้วแบ่งครึ่งอีกครั้ง"),
    (135, "สร้างมุมฉาก แล้วต่อด้วยมุม 45 องศาที่ได้จากการแบ่งครึ่งมุมฉาก"),
    (150, "สร้างมุม 30 องศาบนเส้นตรง แล้วใช้มุมประกอบสองมุมฉากของมุมนั้น"),
    (75, "สร้างมุม 60 องศา แล้วต่อด้วยมุม 15 องศา"),
)


@question_type("math.isosceles_triangle_angle_m2", display_name={"th": "มุมของรูปสามเหลี่ยมหน้าจั่ว"},
               level=M2, topic=_REASON_TOPIC)
class IsoscelesTriangleAngleM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            apex = rng.randrange(20, 141, 2)
            base = (180 - apex) // 2
            return MathDraw("", _deg(base),
                            prompt=f"รูปสามเหลี่ยม ABC มี AB = AC และ ∠A = {apex}° จงหาขนาดของ ∠B",
                            # Not halving, the apex itself, 90° less the apex.
                            distractors=_angles(base, 180 - apex, apex, 90 - apex, base + 10))
        if kind == 1:
            base = rng.randint(20, 85)
            apex = 180 - 2 * base
            return MathDraw("", _deg(apex),
                            prompt=f"รูปสามเหลี่ยม ABC มี AB = AC และ ∠B = {base}° จงหาขนาดของ ∠A",
                            distractors=_angles(apex, 180 - base, base, 90 - base, apex + 10))
        ext = rng.randint(95, 160)
        apex = 2 * ext - 180
        return MathDraw("", _deg(apex),
                        prompt=(f"รูปสามเหลี่ยม ABC มี AB = AC ต่อด้าน BC ออกไปทางจุด C ถึงจุด D "
                                f"ถ้า ∠ACD = {ext}° จงหาขนาดของ ∠A"),
                        # The base angle, and the exterior angle less the base angle.
                        distractors=_angles(apex, 180 - ext, 360 - 2 * ext, ext - 90, apex + 10))


@question_type("math.construct_angle_m2", display_name={"th": "สร้างมุมขนาดต่าง ๆ ด้วยวงเวียนและสันตรง"},
               level={"th": "ม.2"}, topic="การให้เหตุผลทางเรขาคณิต")
class ConstructAngleM2(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        angle, method = rng.choice(_ANGLE_METHODS)
        others = [(a, m) for a, m in _ANGLE_METHODS if a != angle]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _choices([text(f"การสร้างมุมขนาด {angle} องศา ด้วยวงเวียนและสันตรง ทำได้โดยวิธีใด")],
                            method, [m for _, m in others], self.topic)
        return _choices([text(f"“{method}” จะได้มุมขนาดกี่องศา")], f"{angle} องศา",
                        [f"{a} องศา" for a, _ in others], self.topic)


@question_type("math.exterior_angle_m2", display_name={"th": "มุมภายนอกของรูปสามเหลี่ยม"},
               level=M2, topic=_REASON_TOPIC)
class ExteriorAngleM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            a, b = rng.randint(25, 80), rng.randint(25, 80)
            return MathDraw("", _deg(a + b),
                            prompt=(f"รูปสามเหลี่ยม ABC ต่อด้าน BC ออกไปถึงจุด D ถ้า ∠A = {a}° "
                                    f"และ ∠B = {b}° จงหาขนาดของ ∠ACD"),
                            # The interior angle at C, and 180° less one angle.
                            distractors=_angles(a + b, 180 - a - b, 180 - a, 180 - b, abs(a - b)))
        if kind == 1:
            ext = rng.randint(100, 160)
            a = rng.randint(30, ext - 30)
            b = ext - a
            return MathDraw("", _deg(b),
                            prompt=(f"รูปสามเหลี่ยม ABC ต่อด้าน BC ออกไปถึงจุด D ถ้า ∠ACD = {ext}° "
                                    f"และ ∠A = {a}° จงหาขนาดของ ∠B"),
                            distractors=_angles(b, 180 - ext, 180 - a, ext + a, b + 10))
        x = rng.randint(10, 35)
        p, q = rng.randint(1, 20), rng.randint(1, 20)
        ext = 3 * x + p + q
        return MathDraw("", str(x),
                        prompt=(f"รูปสามเหลี่ยม ABC ต่อด้าน BC ออกไปถึงจุด D ถ้า ∠A = (2x + {p})° "
                                f"∠B = (x + {q})° และ ∠ACD = {ext}° จงหาค่า x"),
                        # Not dividing by 3, and ∠ACD taken as ∠ACB.
                        distractors=_story.keep(ext - p - q, (180 - p - q) // 3, x + 5, x - 5,
                                                answer=x, lo=1))


@question_type("math.converse_statement_m2", display_name={"th": "บทกลับของข้อความและการตรวจสอบบทกลับ"},
               level=M2, topic=_REASON_TOPIC)
class ConverseStatementM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            stmt, conv, _ = rng.choice(_CONVERSES)
            others = [c for s, c, _ in _CONVERSES if s != stmt]
            # The statement itself, and converses of other statements.
            return _texts([text("บทกลับของข้อความต่อไปนี้คือข้อใด" + NL + stmt)], conv,
                          [stmt] + rng.sample(others, 2), self.topic)
        want = kind == 1
        right = rng.choice([s for s, _, t in _CONVERSES if t == want])
        wrongs = rng.sample([s for s, _, t in _CONVERSES if t != want], 3)
        ask = "ข้อความในข้อใดมีบทกลับเป็นจริง" if want else "ข้อความในข้อใดมีบทกลับไม่เป็นจริง"
        return _texts([text(ask)], right, wrongs, self.topic)

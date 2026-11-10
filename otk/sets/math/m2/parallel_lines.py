"""เส้นขนาน

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math, math_diagrams_geo, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import (
    PARALLEL_BENDS,
    PARALLEL_TRIANGLES,
    PARALLEL_TWO,
    angle_at,
    bend_alt,
    parallel_alt,
    parallel_triangle_alt,
)
from otk.sets._support.math_geometry import _POLYGONS

PROVENANCE = Provenance("original")


@question_type("math.cointerior_angle",
               display_name={"th": "มุมภายในบนข้างเดียวกันของเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class CointeriorAngle(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(40, 140)
        prompt = rng.choice((
            f"เส้นขนานถูกตัดด้วยเส้นตัด มุมภายในบนข้างเดียวกันมุมหนึ่ง {a} องศา อีกมุมหนึ่งมีขนาดเท่าใด?",
            f"AB ขนานกับ CD มีเส้นตัด EF ตัด AB ที่ G และตัด CD ที่ H ถ้า ∠BGH = {a}° "
            f"∠GHD มีขนาดกี่องศา",
            f"ถนนสองสายขนานกัน มีถนนอีกสายตัดผ่าน มุมภายในบนข้างเดียวกันของเส้นตัดมุมหนึ่ง"
            f"มีขนาด {a} องศา อีกมุมหนึ่งมีขนาดกี่องศา",
        ))
        return MathDraw("", str(180 - a), prompt=prompt,
                        distractors=[str(a), str(90 - a), str(360 - a)])


@question_type("math.transversal_picture_m2", display_name={"th": "หาขนาดของมุมจากรูปเส้นขนานและเส้นตัด"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class TransversalPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARALLEL_TWO)
        (g, lab), (xp, _), (yp, _) = p.marks
        x, y = angle_at(p.theta, xp), angle_at(p.theta, yp)
        img = _img(p.asset_id, parallel_alt(p))
        ask, ans, wrongs = rng.choice((
            ("x + y", x + y, [x - y if x > y else y - x, 2 * x, 180]),
            ("x - y", x - y, [x + y, y - x, 0]),
            ("y", y, [180 - y, x if x != y else 180 - x, 90]),
        ))
        return _math_q([text("เส้นตรงสองเส้นในรูปขนานกัน จงหาค่าของ"), content_math(ask), img],
                       str(ans), [str(w) for w in wrongs], self.topic)


# Filed with ม.2 เส้นขนาน, where (n − 2) × 180° follows from a triangle's 180°;
# it was once listed under ป.1 shapes, where learners only name the shapes.
@question_type("math.polygon_angle_sum", display_name={"th": "ผลบวกมุมภายใน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class PolygonAngleSum(WordProblem):
    """(n − 2) × 180°, which is really "how many triangles does it cut into"."""

    def expr(self, rng: Random, sides_lo: int = 3, sides_hi: int = 10):
        name, n = rng.choice([p for p in _POLYGONS if sides_lo <= p[1] <= sides_hi])
        total = (n - 2) * 180
        return MathDraw("", str(total),
                        prompt=f"ผลบวกของมุมภายในทั้งหมดของ{name}เท่ากับกี่องศา",
                        distractors=[str(n * 180), str((n - 1) * 180), "360"])


@question_type("math.transversal_angle_chain",
               display_name={"th": "มุมบนเส้นตัดขวางของเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class TransversalAngleChain(WordProblem):
    def expr(self, rng: Random, lo: int = 25, hi: int = 155):
        a = rng.randint(lo, hi)
        kind, value = rng.choice([
            ("มุมแย้ง", a), ("มุมภายในบนข้างเดียวกันของเส้นตัด", 180 - a),
            ("มุมภายนอกที่อยู่ตรงข้ามกัน", a),
        ])
        return MathDraw(
            "", str(value),
            prompt=(f"เส้นตรงสองเส้นขนานกันถูกตัดด้วยเส้นตัดขวาง "
                    f"ถ้ามุมหนึ่งมีขนาด {a} องศา แล้ว{kind}กับมุมนั้นมีขนาดกี่องศา"),
            distractors=[str(180 - value), str(90 - value if value < 90 else value - 90),
                         str(360 - value)])


# ── More on parallel lines: a bend between them, a triangle between them, angles in x, the converse, and
# the reason for each step (สสวท. ม.2 เล่ม 1 บทที่ 4) ──

PICTURE_ASK = "เส้นตรงสองเส้นในรูปขนานกัน จงหาขนาดของมุม x (องศา)"


@question_type("math.parallel_bend_m2", display_name={"th": "มุมที่จุดหักระหว่างเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelBendM2(QuestionType):
    """A bend P between two parallel lines: ∠APB is the sum of the angles at the lines (draw the parallel
    through P and use alternate angles twice)."""

    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(PARALLEL_BENDS)
        bend = s.a + s.b
        if s.ask == "x":
            right = bend
            # The angles subtracted; the straight angle less the sum; the full turn less the sum.
            wrongs = [abs(s.a - s.b), 180 - bend, 360 - bend]
        else:
            right = s.a
            # The bend and the angle added; the straight angle less the bend; the angle at B again.
            wrongs = [bend + s.b, 180 - bend, s.b]
        return _math_q([text(PICTURE_ASK), _img(s.asset_id, bend_alt(s))], str(right),
                       [str(w) for w in wrongs if w > 0], self.topic)


@question_type("math.parallel_triangle_m2", display_name={"th": "รูปสามเหลี่ยมระหว่างเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelTriangleM2(QuestionType):
    """Triangle ABC with A on one parallel line and BC on the other: the angles the line makes at A are
    alternate to the base angles, so with the angle at A they make a straight angle."""

    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(PARALLEL_TRIANGLES)
        apex = 180 - t.p - t.q
        if t.ask == "apex":
            right = apex
            # The two given angles added; a straight angle less one of them; their difference.
            wrongs = [t.p + t.q, 180 - t.p, abs(t.p - t.q)]
        else:
            right = t.q
            # The given outer angle (alternate to B, not C); the angle at A; a straight angle less it.
            wrongs = [t.p, apex, 180 - apex]
        return _math_q([text(PICTURE_ASK), _img(t.asset_id, parallel_triangle_alt(t))], str(right),
                       [str(w) for w in wrongs if w > 0], self.topic)


def _expr(m: int, c: int) -> str:
    """mx + c in degrees, written as a Thai textbook would: (3x + 10)°, (x − 20)°, 4x°."""
    body = ("x" if m == 1 else f"{m}x") + (f" + {c}" if c > 0 else f" − {-c}" if c < 0 else "")
    return f"({body})°" if c else f"{body}°"


# (the two angles, their relation): both at G on AB and H on CD, cut by EF.
_PAIRS = (
    ("∠AGH", "∠GHD", "มุมแย้ง", True),
    ("∠EGB", "∠GHD", "มุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัด", True),
    ("∠BGH", "∠GHD", "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด", False),
)


@question_type("math.parallel_algebra_m2", display_name={"th": "หาค่าตัวแปรจากมุมที่เกิดจากเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelAlgebraM2(WordProblem):
    """Two angles written in x: equal (alternate or corresponding), or adding to 180° (interior on the same
    side). Ask for x or for one of the angles."""

    def expr(self, rng: Random):
        first, second, _name, equal = rng.choice(_PAIRS)
        while True:
            x = rng.randint(8, 40)
            m, n = rng.sample(range(1, 6), 2)
            c = rng.randrange(-30, 41, 5)
            u = m * x + c
            v = u if equal else 180 - u
            d = v - n * x
            if 20 <= u <= 160 and 20 <= v <= 160 and -60 <= d <= 80:
                break
        ask_x = rng.random() < 0.5
        stem = (f"AB ขนานกับ CD มีเส้นตัด EF ตัด AB ที่ G และตัด CD ที่ H "
                f"ถ้า {first} = {_expr(m, c)} และ {second} = {_expr(n, d)} ")
        if ask_x:
            # The other rule (equal for supplementary, or the reverse), when it gives a whole number.
            other = (180 - c - d) / (m + n) if equal else (d - c) / (m - n)
            wrongs = [int(other) if other == int(other) and other > 0 else x + 5, x * 2, abs(u - v) or x + 10]
            return MathDraw("", str(x), prompt=stem + "แล้ว x มีค่าเท่าใด", distractors=[str(w) for w in wrongs])
        # The value of x itself; the other angle of a supplementary pair; 180° less the answer.
        wrongs = [x, 180 - u if equal else v, 90 - u if u < 90 else u - 90]
        return MathDraw("", str(u), prompt=stem + f"แล้ว {first} มีขนาดกี่องศา",
                        distractors=[str(w) for w in wrongs if w > 0])


_TEST_RULES = (
    ("มุมแย้ง", True),
    ("มุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัด", True),
    ("มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด", False),
)


@question_type("math.parallel_test_m2", display_name={"th": "ตรวจสอบว่าเส้นตรงขนานกันหรือไม่"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelTestM2(ChoiceType):
    """The converse: two lines cut by a transversal are parallel exactly when alternate (or corresponding)
    angles are equal, or interior angles on the same side add to 180°."""

    def compose(self, rng: Random):
        name, equal = rng.choice(_TEST_RULES)
        u = rng.randint(40, 140)
        parallel = rng.random() < 0.5
        v = (u if equal else 180 - u) + (0 if parallel else rng.choice((-6, -4, -3, 3, 4, 6)))
        rule = "มีขนาดเท่ากัน" if equal else "รวมกันได้ 180 องศา"
        broken = "มีขนาดไม่เท่ากัน" if equal else "รวมกันไม่เท่ากับ 180 องศา"
        swapped = "รวมกันได้ 180 องศา" if equal else "มีขนาดเท่ากัน"
        stem = (f"เส้นตรง ℓ และ m ถูกตัดด้วยเส้นตัด t ถ้า{name}คู่หนึ่งมีขนาด {u} องศา และ {v} องศา "
                f"ข้อใดถูกต้อง")
        yes = f"ℓ ขนานกับ m เพราะ{name}{rule}"
        no = f"ℓ ไม่ขนานกับ m เพราะ{name}{broken}"
        # The verdict reversed; the other rule applied; that a picture is needed to tell.
        wrongs = [no if parallel else yes,
                  (f"ℓ ขนานกับ m เพราะ{name}{swapped}" if not parallel else f"ℓ ไม่ขนานกับ m เพราะ{name}ต้อง{swapped}"),
                  "บอกไม่ได้ เพราะต้องรู้ความยาวของเส้นตรง ℓ และ m"]
        return stem, (yes if parallel else no), wrongs


@question_type("math.parallel_reason_m2", display_name={"th": "เหตุผลของมุมที่เกิดจากเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelReasonM2(ConceptBankType):
    """Which fact justifies a step: the reasons a ม.2 proof about parallel lines cites."""

    _GIVEN = "AB ขนานกับ CD มีเส้นตัด EF ตัด AB ที่ G และตัด CD ที่ H "
    _REASONS = (
        "ถ้าเส้นตรงสองเส้นขนานกันและมีเส้นตัด แล้วมุมแย้งมีขนาดเท่ากัน",
        "ถ้าเส้นตรงสองเส้นขนานกันและมีเส้นตัด แล้วมุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัดมีขนาดเท่ากัน",
        "ถ้าเส้นตรงสองเส้นขนานกันและมีเส้นตัด แล้วผลบวกของขนาดของมุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดเท่ากับ 180 องศา",
        "ถ้าเส้นตรงสองเส้นตัดกัน แล้วมุมตรงข้ามมีขนาดเท่ากัน",
        "ขนาดของมุมตรงเท่ากับ 180 องศา",
    )
    ITEMS = [
        Concept(_GIVEN + "เหตุผลใดทำให้สรุปได้ว่า ∠AGH = ∠GHD", _REASONS[0],
                (_REASONS[1], _REASONS[3], _REASONS[2])),
        Concept(_GIVEN + "เหตุผลใดทำให้สรุปได้ว่า ∠EGB = ∠GHD", _REASONS[1],
                (_REASONS[0], _REASONS[3], _REASONS[4])),
        Concept(_GIVEN + "เหตุผลใดทำให้สรุปได้ว่า ∠BGH + ∠GHD = 180°", _REASONS[2],
                (_REASONS[4], _REASONS[0], _REASONS[1])),
        Concept(_GIVEN + "เหตุผลใดทำให้สรุปได้ว่า ∠AGE = ∠BGH", _REASONS[3],
                (_REASONS[0], _REASONS[1], _REASONS[4])),
        Concept(_GIVEN + "เหตุผลใดทำให้สรุปได้ว่า ∠AGH + ∠BGH = 180°", _REASONS[4],
                (_REASONS[2], _REASONS[3], _REASONS[0])),
        Concept("เส้นตรง ℓ และ m ถูกตัดด้วยเส้นตัด t ถ้ามุมแย้งคู่หนึ่งมีขนาดเท่ากัน ข้อสรุปใดถูกต้อง",
                "ℓ ขนานกับ m", ("ℓ ตั้งฉากกับ m", "ℓ และ m ตัดกันที่จุดหนึ่ง", "บอกไม่ได้ว่า ℓ และ m ขนานกันหรือไม่")),
    ]


# The eight angles where EF (E above AB) cuts AB at G and CD at H, sorted into the two sizes they come in:
# with ∠EGB = u, these four are u and the other four 180° − u.
NAMED_EQUAL = ("∠EGB", "∠AGH", "∠GHD", "∠CHF")
NAMED_SUPPLEMENT = ("∠AGE", "∠BGH", "∠CHG", "∠DHF")


@question_type("math.parallel_named_angle_m2", display_name={"th": "หาขนาดของมุมจากชื่อมุมบนเส้นขนาน"},
               level={"th": "ม.2"}, topic="เส้นขนาน")
class ParallelNamedAngleM2(WordProblem):
    """One angle at G given by name, another at H asked: equal or supplementary, often in two steps."""

    def expr(self, rng: Random):
        u = rng.choice([n for n in range(35, 146) if n != 90])
        given = rng.choice(NAMED_EQUAL[:2] + NAMED_SUPPLEMENT[:2])
        asked = rng.choice(NAMED_EQUAL[2:] + NAMED_SUPPLEMENT[2:])
        v = u if given in NAMED_EQUAL else 180 - u
        right = v if (given in NAMED_EQUAL) == (asked in NAMED_EQUAL) else 180 - v
        prompt = (f"AB ขนานกับ CD มีเส้นตัด EF ตัด AB ที่ G และตัด CD ที่ H ถ้า {given} = {v}° "
                  f"จงหาขนาดของ {asked} (องศา)")
        # The other size; its difference from a right angle; the given angle doubled.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - right, abs(90 - right), 2 * v, right + 10,
                                                answer=right, lo=1, hi=179))


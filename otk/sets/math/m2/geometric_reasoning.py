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


# ── More reasoning (สสวท. ม.2 เล่ม 2 บทที่ 4): angle sums with x, a polygon's exterior angles, which three
# lengths make a triangle, opposite and adjacent angles at a crossing, an angle bisector in a triangle,
# and the converse of the isosceles theorem ──


def _x(m: int, c: int) -> str:
    """mx + c as sentence text: 2x + 3, 5x − 9, x, 3x."""
    return ("x" if m == 1 else f"{m}x") + (f" + {c}" if c > 0 else f" − {-c}" if c < 0 else "")


def _deg_x(m: int, c: int) -> str:
    return f"({_x(m, c)})°" if c else f"{_x(m, c)}°"


@question_type("math.triangle_angle_algebra_m2", display_name={"th": "ผลบวกของมุมภายในรูปสามเหลี่ยมกับตัวแปร"},
               level=M2, topic=_REASON_TOPIC)
class TriangleAngleAlgebraM2(WordProblem):
    """The three angles add to 180°: written in x, or in a ratio."""

    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 2:
            while True:
                ratio = sorted(rng.sample(range(1, 8), 3))
                if 180 % sum(ratio) == 0:
                    break
            unit = 180 // sum(ratio)
            largest = ratio[2] * unit
            prompt = (f"มุมทั้งสามของรูปสามเหลี่ยมรูปหนึ่งมีขนาดเป็นอัตราส่วน {ratio[0]} : {ratio[1]} : {ratio[2]} "
                      f"มุมที่ใหญ่ที่สุดมีขนาดกี่องศา")
            # One part; 180° split by the largest part alone; the parts read as 360°.
            return MathDraw("", str(largest), prompt=prompt,
                            distractors=_story.keep(unit, ratio[2] * 360 // sum(ratio), 180 - largest,
                                                    ratio[1] * unit, answer=largest, lo=1))
        while True:
            x = rng.randint(8, 30)
            ms = [rng.randint(1, 4) for _ in range(3)]
            c1, c2 = rng.randrange(-20, 31, 5), rng.randrange(-20, 31, 5)
            c3 = 180 - sum(ms) * x - c1 - c2
            angles = [ms[0] * x + c1, ms[1] * x + c2, ms[2] * x + c3]
            if -40 <= c3 <= 60 and all(15 <= a <= 150 for a in angles):
                break
        stated = f"∠A = {_deg_x(ms[0], c1)}, ∠B = {_deg_x(ms[1], c2)} และ ∠C = {_deg_x(ms[2], c3)}"
        if kind == 0:
            # The constants left out of the 180°; the equation set to 360°; one angle offered as x.
            wrong_x = 180 // sum(ms)
            return MathDraw("", str(x), prompt=f"รูปสามเหลี่ยม ABC มี {stated} จงหาค่า x",
                            distractors=_story.keep(wrong_x, (360 - c1 - c2 - c3) // sum(ms), angles[0], x + 2,
                                                    x - 2, answer=x, lo=1))
        ask = rng.randrange(3)
        value = angles[ask]
        others = [a for n, a in enumerate(angles) if n != ask]
        return MathDraw("", str(value), prompt=f"รูปสามเหลี่ยม ABC มี {stated} จงหาขนาดของ ∠{'ABC'[ask]} (องศา)",
                        distractors=_story.keep(x, *others, 180 - value, answer=value, lo=1))


_REGULAR = (3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36)


@question_type("math.polygon_exterior_m2", display_name={"th": "มุมภายนอกของรูปหลายเหลี่ยม"},
               level=M2, topic=_REASON_TOPIC)
class PolygonExteriorM2(WordProblem):
    """The exterior angles of any polygon add to 360°; a regular n-gon's each measure 360°/n."""

    def expr(self, rng: Random):
        n = rng.choice(_REGULAR)
        ext, interior = 360 // n, 180 - 360 // n
        kind = rng.randrange(3)
        if kind == 0:
            # The interior angle; 180°/n; the sum of the interior angles.
            return MathDraw("", str(ext), prompt=f"รูป {n} เหลี่ยมด้านเท่ามุมเท่า มีมุมภายนอกแต่ละมุมขนาดกี่องศา",
                            distractors=_story.keep(interior, 180 // n if 180 % n == 0 else 0, (n - 2) * 180, 360,
                                                    answer=ext, lo=1))
        if kind == 1:
            # 180° divided by the angle; the interior read as exterior; n − 2.
            return MathDraw("", str(n), prompt=f"รูปหลายเหลี่ยมด้านเท่ามุมเท่ารูปหนึ่งมีมุมภายนอกแต่ละมุมขนาด {ext} องศา "
                                               f"รูปนี้มีกี่ด้าน",
                            distractors=_story.keep(180 // ext if 180 % ext == 0 else 0, n + 2, n - 2, 2 * n,
                                                    answer=n, lo=3))
        return MathDraw("", str(n), prompt=f"รูปหลายเหลี่ยมด้านเท่ามุมเท่ารูปหนึ่งมีมุมภายในแต่ละมุมขนาด {interior} องศา "
                                           f"รูปนี้มีกี่ด้าน",
                        # 360° divided by the interior angle; one more; one less.
                        distractors=_story.keep(360 // interior if 360 % interior == 0 else 0, n + 1, n - 1, 2 * n,
                                                answer=n, lo=3))


@question_type("math.triangle_inequality_m2", display_name={"th": "ความยาวด้านที่เป็นรูปสามเหลี่ยมได้"},
               level=M2, topic=_REASON_TOPIC)
class TriangleInequalityM2(WordProblem):
    """Any two sides together are longer than the third: the third side lies strictly between |a − b| and a + b."""

    def expr(self, rng: Random):
        a, b = sorted(rng.sample(range(3, 21), 2))
        lead = f"รูปสามเหลี่ยมรูปหนึ่งมีด้านสองด้านยาว {a} และ {b} เซนติเมตร ถ้าด้านที่สามยาวเป็นจำนวนเต็มเซนติเมตร "
        kind = rng.randrange(3)
        if kind == 0:
            right = a + b - 1
            # The sum itself; the difference; one past the sum.
            return MathDraw("", str(right), prompt=lead + "ด้านที่สามยาวได้มากที่สุดกี่เซนติเมตร",
                            distractors=_story.keep(a + b, b - a, a + b + 1, b, answer=right, lo=1))
        if kind == 1:
            right = b - a + 1
            return MathDraw("", str(right), prompt=lead + "ด้านที่สามยาวได้น้อยที่สุดกี่เซนติเมตร",
                            distractors=_story.keep(b - a, 1, b - a + 2, a, answer=right, lo=1))
        right = 2 * a - 1
        # Counting both ends; one end; the sum less the difference.
        return MathDraw("", str(right), prompt=lead + "ด้านที่สามมีความยาวที่เป็นไปได้กี่แบบ",
                        distractors=_story.keep(2 * a + 1, 2 * a, a + b - 1, b, answer=right, lo=1))


@question_type("math.vertical_angles_algebra_m2", display_name={"th": "มุมตรงข้ามและมุมประกอบกันเป็นมุมตรงกับตัวแปร"},
               level=M2, topic=_REASON_TOPIC)
class VerticalAnglesAlgebraM2(WordProblem):
    """AB and CD cross at O: ∠AOC = ∠BOD (opposite) and ∠AOC + ∠COB = 180° (on a straight line)."""

    def expr(self, rng: Random):
        x = rng.randint(5, 30)
        opposite = rng.random() < 0.5
        while True:
            m1, m2 = rng.sample(range(1, 6), 2)
            first = rng.randint(30, 150)
            second = first if opposite else 180 - first
            c1, c2 = first - m1 * x, second - m2 * x
            if c1 and c2 and abs(c1) <= 80 and abs(c2) <= 80 and first != 90:
                break
        names = ("∠AOC", "∠BOD") if opposite else ("∠AOC", "∠COB")
        lead = (f"เส้นตรง AB และ CD ตัดกันที่จุด O ถ้า {names[0]} = {_deg_x(m1, c1)} "
                f"และ {names[1]} = {_deg_x(m2, c2)} ")
        if rng.random() < 0.5:
            # The other relation used: sum 180 for opposite angles, equal for angles on a line.
            other = (180 - c1 - c2) / (m1 + m2) if opposite else (c2 - c1) / (m1 - m2)
            other = int(other) if other == int(other) and other > 0 else 0
            return MathDraw("", str(x), prompt=lead + "จงหาค่า x",
                            distractors=_story.keep(other, first, x + 2, x - 2, x + 5, answer=x, lo=1))
        return MathDraw("", str(first), prompt=lead + f"จงหาขนาดของ {names[0]} (องศา)",
                        distractors=_story.keep(180 - first, x, m1 * x, first + 10, answer=first, lo=1, hi=179))


@question_type("math.angle_bisector_triangle_m2", display_name={"th": "เส้นแบ่งครึ่งมุมในรูปสามเหลี่ยม"},
               level=M2, topic=_REASON_TOPIC)
class AngleBisectorTriangleM2(WordProblem):
    """AD bisects ∠A of triangle ABC: ∠BAD is half of ∠A, and ∠ADC is an exterior angle of △ABD."""

    def expr(self, rng: Random):
        while True:
            b, c = rng.randint(30, 90), rng.randint(30, 90)
            a = 180 - b - c
            if a >= 20 and a % 2 == 0:
                break
        half = a // 2
        lead = f"รูปสามเหลี่ยม ABC มี ∠B = {b}° และ ∠C = {c}° ลาก AD แบ่งครึ่ง ∠BAC ให้ D อยู่บน BC "
        kind = rng.randrange(3)
        if kind == 0:
            # Not halved; half of 180°; half of ∠B.
            return MathDraw("", str(half), prompt=lead + "จงหาขนาดของ ∠BAD (องศา)",
                            distractors=_story.keep(a, 90 - half, b // 2, half + 10, answer=half, lo=1))
        if kind == 1:
            right = b + half
            # The whole of ∠A added; ∠ADB instead; ∠C instead of ∠B.
            return MathDraw("", str(right), prompt=lead + "จงหาขนาดของ ∠ADC (องศา)",
                            distractors=_story.keep(b + a, 180 - right, c + half, right - 10, answer=right, lo=1, hi=179))
        right = c + half
        return MathDraw("", str(right), prompt=lead + "จงหาขนาดของ ∠ADB (องศา)",
                        distractors=_story.keep(c + a, 180 - right, b + half, right + 10, answer=right, lo=1, hi=179))


@question_type("math.isosceles_sides_m2", display_name={"th": "บทกลับของทฤษฎีบทรูปสามเหลี่ยมหน้าจั่ว"},
               level=M2, topic=_REASON_TOPIC)
class IsoscelesSidesM2(WordProblem):
    """Two equal angles mean the sides opposite them are equal: ∠B = ∠C gives AB = AC."""

    def expr(self, rng: Random):
        x = rng.randint(2, 9)
        while True:
            m1, m2 = rng.sample(range(1, 6), 2)
            side = rng.randint(10, 40)
            c1, c2 = side - m1 * x, side - m2 * x
            if c1 and c2 and abs(c1) <= 40 and abs(c2) <= 40:
                break
        base = rng.randint(4, 2 * side - 1)
        sides = f"AB = {_x(m1, c1)} เซนติเมตร", f"AC = {_x(m2, c2)} เซนติเมตร"
        lead = f"รูปสามเหลี่ยม ABC มี ∠B = ∠C ถ้า {sides[0]} และ {sides[1]} "
        if rng.random() < 0.5:
            other = (c2 - c1) // (m1 + m2) if (c2 - c1) % (m1 + m2) == 0 else 0
            return MathDraw("", str(x), prompt=lead + "จงหาค่า x",
                            distractors=_story.keep(other, side, x + 1, x - 1, x + 3, answer=x, lo=1))
        perimeter = 2 * side + base
        # BC counted twice instead of AB; one AB only; x read as the side.
        return MathDraw("", str(perimeter), prompt=(f"รูปสามเหลี่ยม ABC มี ∠B = ∠C ถ้า {sides[0]}, {sides[1]} และ BC = {base} เซนติเมตร "
                                                 f"จงหาความยาวรอบรูป (เซนติเมตร)"),
                        distractors=_story.keep(side + 2 * base, side + base, 2 * x + base, perimeter + 2,
                                                answer=perimeter, lo=1))


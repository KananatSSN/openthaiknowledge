"""การสร้างทางเรขาคณิต

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.1/*

Sets moved here from: math, math_formats_hi, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q

PROVENANCE = Provenance("original")


def _constructible() -> set[float]:
    """Angles reached from 60° and 90° by bisecting, adding and subtracting."""
    base = {60.0, 90.0}
    seen = set(base)
    for _ in range(3):
        new = {a / 2 for a in seen} | {a + b for a in seen for b in seen} | {
            abs(a - b) for a in seen for b in seen}
        seen |= {a for a in new if 0 < a <= 180}
    return seen


_REACHABLE = sorted(a for a in _constructible() if a == int(a) and 15 <= a <= 165)


_NOT_REACHABLE = (20, 40, 50, 70, 80, 100, 110, 130, 140, 160)


@question_type("math.angle_bisector",
               display_name={"th": "การแบ่งครึ่งมุม"}, level={"th": "ม.1"},
               topic="การสร้างทางเรขาคณิต")
class AngleBisector(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(10, 80) * 2                 # even → integer half
        prompt = rng.choice((
            f"แบ่งครึ่งมุมขนาด {a} องศา ได้มุมละกี่องศา?",
            f"รังสี OC แบ่งครึ่งมุม AOB ถ้ามุม AOB มีขนาด {a} องศา มุม AOC มีขนาดกี่องศา",
            f"พับกระดาษให้สันพับแบ่งครึ่งมุมขนาด {a} องศาพอดี มุมแต่ละข้างของสันพับมีขนาดกี่องศา",
        ))
        return MathDraw("", str(a // 2), prompt=prompt,
                        distractors=[str(a), str(2 * a), str(90 - a)])


@question_type("math.angle_bisector_measure",
               display_name={"th": "แบ่งครึ่งมุมแล้วได้มุมเท่าใด"},
               level={"th": "ม.1"}, topic="การสร้างทางเรขาคณิต")
class AngleBisectorMeasure(WordProblem):
    def expr(self, rng: Random, lo: int = 20, hi: int = 170):
        a = rng.randrange(lo, hi, 2)             # even, so the half is whole
        prompt = rng.choice((
            f"แบ่งครึ่งมุมขนาด {a} องศา ด้วยวงเวียนและสันตรง จะได้มุมย่อยขนาดกี่องศา",
            f"สร้างเส้นแบ่งครึ่งมุม PQR ซึ่งมีขนาด {a} องศา ตัด PR ที่จุด S มุม PQS มีขนาดกี่องศา",
            f"ช่างไม้ต้องการตัดไม้ที่มุมขนาด {a} องศาให้เป็นสองมุมเท่ากัน แต่ละมุมมีขนาดกี่องศา",
        ))
        return MathDraw("", str(a // 2), prompt=prompt,
                        distractors=[str(a), str(a * 2), str(90 - a // 2)])


@question_type("math.construct_angle_m1", display_name={"th": "มุมที่สร้างได้ด้วยวงเวียนและสันตรง"},
               level={"th": "ม.1"}, topic="การสร้างทางเรขาคณิต")
class ConstructAngleM1(QuestionType):
    _STEPS = (
        ("สร้างมุม 60° แล้วแบ่งครึ่ง", 30), ("สร้างมุม 90° แล้วแบ่งครึ่ง", 45),
        ("สร้างมุม 60° แล้วแบ่งครึ่งสองครั้ง", 15), ("สร้างมุม 90° แล้วแบ่งครึ่งสองครั้ง", 22.5),
        ("สร้างมุม 90° ต่อกับมุม 30°", 120), ("สร้างมุม 90° ต่อกับมุม 45°", 135),
        ("สร้างมุม 60° ต่อกับมุม 45°", 105), ("สร้างมุม 60° ต่อกับมุม 15°", 75),
        ("สร้างมุม 90° ต่อกับมุม 60°", 150), ("สร้างมุมตรง แล้วลบด้วยมุม 45°", 135),
    )

    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            step, angle = rng.choice(self._STEPS)
            fmt = f"{angle:g}"
            wrongs = [f"{angle * 2:g}", f"{angle / 2:g}", f"{180 - angle:g}", f"{angle + 15:g}"]
            return _math_q([text(f"{step} จะได้มุมขนาดกี่องศา")], fmt,
                           [w for w in wrongs if w != fmt], self.topic)
        odd = rng.choice(_NOT_REACHABLE)
        ok = rng.sample([a for a in _REACHABLE if a % 15 == 0], 3)
        return _math_q([text("ถ้าเริ่มจากการสร้างมุม 60° และ 90° แล้วแบ่งครึ่งมุมหรือนำมุมมาต่อกัน "
                             "มุมขนาดใดสร้างไม่ได้ (หน่วยเป็นองศา)")],
                       str(odd), [str(int(a)) for a in ok], self.topic)


@question_type("math.perpendicular_bisector",
               display_name={"th": "เส้นแบ่งครึ่งตั้งฉาก"},
               level={"th": "ม.1"}, topic="การสร้างทางเรขาคณิต")
class PerpendicularBisector(WordProblem):
    def expr(self, rng: Random, lo: int = 6, hi: int = 40):
        length = rng.randrange(lo, hi, 2)
        prompt = rng.choice((
            f"สร้างเส้นแบ่งครึ่งตั้งฉากของส่วนของเส้นตรงยาว {length} เซนติเมตร "
            f"ส่วนของเส้นตรงถูกแบ่งออกเป็นสองส่วน แต่ละส่วนยาวกี่เซนติเมตร",
            f"เส้นตรง ℓ แบ่งครึ่งและตั้งฉากกับ AB ที่จุด M ถ้า AB ยาว {length} เซนติเมตร "
            f"AM ยาวกี่เซนติเมตร",
            f"หาจุดกึ่งกลางของไม้ยาว {length} เซนติเมตร ด้วยการสร้างเส้นแบ่งครึ่งตั้งฉาก "
            f"จุดนั้นอยู่ห่างจากปลายไม้กี่เซนติเมตร",
        ))
        return MathDraw(
            "", str(length // 2), prompt=prompt,
            distractors=[str(length), str(length * 2), "90"])

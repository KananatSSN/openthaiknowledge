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


# ── More constructions (2026-11): the first steps, the tools, a segment built from others, which three lengths
# make a triangle, angles built from 60° and 90°, and halving a segment twice ──

from otk.kit import story as _story  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType  # noqa: E402

_CON_TOPIC = "การสร้างทางเรขาคณิต"
_M1 = {"th": "ม.1"}


@question_type("math.construction_first_step_m1", display_name={"th": "ขั้นตอนการสร้างพื้นฐาน"},
               level=_M1, topic=_CON_TOPIC)
class ConstructionFirstStepM1(ConceptBankType):
    ITEMS = [
        Concept("การสร้างเส้นแบ่งครึ่งส่วนของเส้นตรง AB เริ่มต้นอย่างไร",
                "กางวงเวียนเกินครึ่งหนึ่งของ AB เขียนส่วนโค้งจาก A และจาก B ให้ตัดกันสองจุด",
                ("กางวงเวียนยาวเท่ากับ AB แล้วเขียนวงกลมรอบจุดกึ่งกลางที่วัดด้วยไม้บรรทัด",
                 "ใช้ไม้โปรแทรกเตอร์วัดมุม 90 องศาที่จุด A แล้วลากเส้นตั้งฉากขึ้นไป",
                 "กางวงเวียนน้อยกว่าครึ่งหนึ่งของ AB เขียนส่วนโค้งจาก A เพียงจุดเดียว")),
        Concept("การแบ่งครึ่งมุม ABC เริ่มต้นอย่างไร",
                "ใช้ B เป็นจุดศูนย์กลาง เขียนส่วนโค้งตัดแขนทั้งสองของมุม",
                ("ใช้ A เป็นจุดศูนย์กลาง เขียนส่วนโค้งตัดแขนทั้งสองของมุม",
                 "วัดขนาดมุมด้วยไม้โปรแทรกเตอร์แล้วหารด้วยสอง",
                 "ลากส่วนของเส้นตรง AC แล้วหาจุดกึ่งกลางด้วยไม้บรรทัด")),
        Concept("การสร้างส่วนของเส้นตรงให้ยาวเท่ากับ AB ทำอย่างไร",
                "กางวงเวียนยาวเท่ากับ AB แล้วนำไปเขียนส่วนโค้งตัดเส้นตรงที่ลากไว้",
                ("วัดความยาว AB ด้วยวงเวียนแล้วจดตัวเลขไว้เพื่อลากใหม่",
                 "ลากเส้นตรงใหม่ให้ขนานกับ AB โดยใช้สันตรงเพียงอย่างเดียว",
                 "พับกระดาษให้ A ทับ B แล้วใช้รอยพับเป็นความยาวใหม่")),
        Concept("การสร้างเส้นตั้งฉากที่จุด P บนเส้นตรง เริ่มต้นอย่างไร",
                "ใช้ P เป็นจุดศูนย์กลาง เขียนส่วนโค้งตัดเส้นตรงสองจุดที่ห่างจาก P เท่ากัน",
                ("ใช้ P เป็นจุดศูนย์กลาง เขียนวงกลมรัศมีเท่าใดก็ได้โดยไม่ตัดเส้นตรง",
                 "วางไม้โปรแทรกเตอร์ที่ P แล้วทำเครื่องหมายที่ 90 องศา",
                 "ลากเส้นจาก P ไปยังจุดใดก็ได้นอกเส้นตรงแล้วแบ่งครึ่ง")),
    ]


@question_type("math.construction_tools_m1", display_name={"th": "วงเวียนและสันตรงใช้ทำอะไร"},
               level=_M1, topic=_CON_TOPIC)
class ConstructionToolsM1(ConceptBankType):
    ITEMS = [
        Concept("ในการสร้างทางเรขาคณิต สันตรงใช้ทำอะไร", "ลากส่วนของเส้นตรงหรือเส้นตรงผ่านจุดสองจุด",
                ("วัดความยาวของส่วนของเส้นตรงเป็นเซนติเมตรให้ได้ค่าที่แน่นอน", "วัดขนาดของมุมเป็นองศาก่อนลากแขนของมุม",
                 "เขียนส่วนโค้งและวงกลมที่มีรัศมีตามต้องการ")),
        Concept("ในการสร้างทางเรขาคณิต วงเวียนใช้ทำอะไร", "เขียนส่วนโค้งหรือวงกลมและถ่ายความยาว",
                ("วัดขนาดของมุมเป็นองศาแล้วจดค่าที่วัดได้ไว้", "ลากเส้นตรงผ่านจุดสองจุดที่กำหนดให้",
                 "วัดความยาวเป็นเซนติเมตรด้วยสเกลบนวงเวียน")),
        Concept("เครื่องมือใดไม่ใช้ในการสร้างทางเรขาคณิตตามแบบของหนังสือเรียน", "ไม้โปรแทรกเตอร์",
                ("วงเวียน", "สันตรง", "ดินสอดำ")),
    ]


@question_type("math.construct_segment_length_m1", display_name={"th": "สร้างส่วนของเส้นตรงจากความยาวที่กำหนด"},
               level=_M1, topic=_CON_TOPIC)
class ConstructSegmentLengthM1(WordProblem):
    """Laying copies of AB and CD end to end (or back over each other)."""

    def expr(self, rng: Random):
        ab, cd = rng.randint(4, 12), rng.randint(2, 6)
        p, q = rng.randint(1, 3), rng.randint(1, 2)
        sign = rng.choice((1, -1))
        right = p * ab + sign * q * cd
        if right <= 0:
            sign, right = 1, p * ab + q * cd
        op = "+" if sign > 0 else "−"
        expr = (f"{p if p > 1 else ''}AB {op} {q if q > 1 else ''}CD").strip()
        prompt = (f"กำหนดให้ AB ยาว {ab} ซม. และ CD ยาว {cd} ซม. ถ้าสร้างส่วนของเส้นตรงยาว {expr} "
                  f"ด้วยวงเวียนและสันตรง จะได้ส่วนของเส้นตรงยาวกี่เซนติเมตร")
        # The other sign; the multiples dropped; one length used twice.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(p * ab - sign * q * cd, ab + sign * cd, p * ab, right + 2,
                                                answer=right, lo=1))


@question_type("math.triangle_from_sides_m1", display_name={"th": "สร้างรูปสามเหลี่ยมจากความยาวด้านได้หรือไม่"},
               level=_M1, topic=_CON_TOPIC)
class TriangleFromSidesM1(ChoiceType):
    """Three lengths make a triangle only when the two shorter add to more than the longest."""

    def compose(self, rng: Random):
        def valid():
            while True:
                a, b, c = sorted(rng.sample(range(2, 15), 3))
                if a + b > c:
                    return a, b, c

        def invalid():
            while True:
                a, b = sorted(rng.sample(range(2, 10), 2))
                c = a + b + rng.randint(0, 3)
                if c <= 20:
                    return a, b, c

        cannot = rng.random() < 0.5
        right = invalid() if cannot else valid()
        others = []
        while len(others) < 3:
            t = valid() if cannot else invalid()
            if t not in others and t != right:
                others.append(t)
        show = lambda t: f"{t[0]}, {t[1]} และ {t[2]} ซม."
        ask = "สร้างรูปสามเหลี่ยมไม่ได้" if cannot else "สร้างรูปสามเหลี่ยมได้"
        return f"ด้านสามด้านในข้อใด{ask}", show(right), [show(t) for t in others]


@question_type("math.construct_angle_steps_m1", display_name={"th": "มุมที่ได้จากการสร้างมุมต่อกัน"},
               level=_M1, topic=_CON_TOPIC)
class ConstructAngleStepsM1(WordProblem):
    """Every constructible angle here comes from 60° and 90°, halved and added."""

    _STEPS = (
        ("สร้างมุม 60 องศา แล้วแบ่งครึ่งสองครั้ง", 15),
        ("สร้างมุม 90 องศา แล้วแบ่งครึ่งสองครั้ง", 22.5),
        ("สร้างมุม 90 องศา แล้วสร้างมุม 30 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 120),
        ("สร้างมุม 90 องศา แล้วสร้างมุม 45 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 135),
        ("สร้างมุม 60 องศา แล้วสร้างมุม 45 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 105),
        ("สร้างมุม 90 องศา แล้วสร้างมุม 60 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 150),
        ("สร้างมุม 60 องศาบนเส้นตรง แล้วใช้มุมที่เหลือบนเส้นตรงเดียวกัน", 120),
        ("สร้างมุม 45 องศาบนเส้นตรง แล้วใช้มุมที่เหลือบนเส้นตรงเดียวกัน", 135),
        ("สร้างมุม 90 องศา แล้วสร้างมุม 15 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 105),
        ("สร้างมุม 60 องศา แล้วสร้างมุม 15 องศาต่อจากแขนข้างหนึ่งออกไปด้านนอก", 75),
    )

    def expr(self, rng: Random):
        desc, angle = rng.choice(self._STEPS)
        show = lambda v: str(int(v)) if v == int(v) else f"{v:.1f}"
        others = sorted({a for _, a in self._STEPS if a != angle} | {30, 45, 60, 90})
        rng.shuffle(others)
        return MathDraw("", show(angle), prompt=f"“{desc}” จะได้มุมขนาดกี่องศา",
                        distractors=[show(v) for v in others[:3]])


@question_type("math.segment_halving_m1", display_name={"th": "แบ่งครึ่งส่วนของเส้นตรงซ้ำ"},
               level=_M1, topic=_CON_TOPIC)
class SegmentHalvingM1(WordProblem):
    def expr(self, rng: Random):
        length = 8 * rng.randint(2, 12)
        lead = (f"AB ยาว {length} ซม. สร้างเส้นแบ่งครึ่ง AB ได้จุดกึ่งกลาง M แล้วสร้างเส้นแบ่งครึ่ง AM "
                f"ได้จุดกึ่งกลาง N ")
        kind = rng.randrange(3)
        if kind == 0:
            right, asked = length // 4, "AN"
        elif kind == 1:
            right, asked = length // 4, "NM"
        else:
            right, asked = 3 * length // 4, "NB"
        return MathDraw("", str(right), prompt=lead + f"{asked} ยาวกี่เซนติเมตร",
                        distractors=_story.keep(length // 2, length // 8, length // 4 if right != length // 4 else 3 * length // 4,
                                                length - right // 2, answer=right, lo=1))


# ── To fifteen (2026-11): angles copied and combined, the bisectors of two angles on a line, what a
# construction makes, a line through a point, and which facts fix a triangle ──


@question_type("math.copied_angles_m1", display_name={"th": "สร้างมุมจากมุมที่กำหนดให้"},
               level=_M1, topic=_CON_TOPIC)
class CopiedAnglesM1(WordProblem):
    """Copying angles side by side adds them; copying inside subtracts."""

    def expr(self, rng: Random):
        a, b = rng.randint(20, 70), rng.randint(15, 60)
        kind = rng.randrange(3)
        if kind == 0:
            words, right = "∠A + ∠B", a + b
        elif kind == 1:
            words, right = "2∠A", 2 * a
        else:
            a, b = max(a, b + 5), min(a, b)
            words, right = "∠A − ∠B", a - b
        prompt = (f"กำหนด ∠A = {a}° และ ∠B = {b}° ถ้าใช้วงเวียนและสันตรงสร้างมุมที่มีขนาดเท่ากับ "
                  f"{words} จะได้มุมขนาดกี่องศา")
        # Another of the three; the two angles averaged.
        others = (a + b, 2 * a, abs(a - b), (a + b) // 2)
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(*others, right + 10, answer=right, lo=1, hi=359))


@question_type("math.bisectors_on_line_m1", display_name={"th": "เส้นแบ่งครึ่งมุมสองมุมที่ประกอบกันเป็นมุมตรง"},
               level=_M1, topic=_CON_TOPIC)
class BisectorsOnLineM1(WordProblem):
    """∠AOB + ∠BOC = 180°: halves add to 90°, so the two bisectors are perpendicular."""

    def expr(self, rng: Random):
        a = 2 * rng.randint(15, 75)
        lead = (f"จุด A, O และ C อยู่บนเส้นตรงเดียวกัน ∠AOB = {a}° สร้าง OP แบ่งครึ่ง ∠AOB "
                f"และ OQ แบ่งครึ่ง ∠BOC ")
        kind = rng.randrange(3)
        if kind == 0:
            right, asked, wrongs = 90, "∠POQ", (a // 2, 180 - a, 180 - a // 2)
        elif kind == 1:
            right, asked, wrongs = (180 - a) // 2, "∠BOQ", (180 - a, a // 2, 90 - a // 4)
        else:
            right, asked, wrongs = 180 - a // 2, "∠POC", (a // 2, 90 + a, 180 - a)
        return MathDraw("", str(right), prompt=lead + f"{asked} มีขนาดกี่องศา",
                        distractors=_story.keep(*wrongs, right + 10, answer=right, lo=1, hi=179))


@question_type("math.construction_result_m1", display_name={"th": "ขั้นตอนนี้สร้างอะไร"},
               level=_M1, topic=_CON_TOPIC)
class ConstructionResultM1(ConceptBankType):
    ITEMS = [
        Concept("เขียนส่วนโค้งจาก A และ B รัศมีเท่ากันเกินครึ่งหนึ่งของ AB ตัดกันสองจุด แล้วลากเส้นผ่านสองจุดนั้น "
                "ได้เส้นใด", "เส้นแบ่งครึ่งและตั้งฉากกับ AB",
                ("เส้นที่ขนานกับ AB", "เส้นแบ่งครึ่งมุมที่จุด A", "เส้นที่ผ่าน A และทำมุม 60 องศากับ AB")),
        Concept("ใช้จุดยอดของมุมเป็นจุดศูนย์กลางเขียนส่วนโค้งตัดแขนทั้งสอง แล้วเขียนส่วนโค้งรัศมีเท่ากันจากจุดตัดทั้งสอง "
                "ให้ตัดกัน ลากเส้นจากจุดยอดผ่านจุดตัดนั้น ได้เส้นใด", "เส้นแบ่งครึ่งมุม",
                ("เส้นตั้งฉากกับแขนของมุม", "เส้นที่ขนานกับแขนของมุม", "เส้นแบ่งครึ่งและตั้งฉากกับแขนของมุม")),
        Concept("เขียนส่วนโค้งจาก A และ B รัศมีเท่ากับ AB ตัดกันที่จุด C แล้วลากส่วนของเส้นตรง CA และ CB ได้รูปใด",
                "รูปสามเหลี่ยมด้านเท่า", ("รูปสามเหลี่ยมมุมฉาก", "รูปสี่เหลี่ยมจัตุรัส", "รูปสามเหลี่ยมหน้าจั่วที่มีมุมยอด 90 องศา")),
        Concept("จากจุด P นอกเส้นตรง เขียนส่วนโค้งตัดเส้นตรงสองจุด แล้วสร้างเส้นแบ่งครึ่งระหว่างสองจุดนั้น ได้เส้นใด",
                "เส้นตั้งฉากกับเส้นตรงที่ผ่านจุด P", ("เส้นที่ขนานกับเส้นตรงที่ผ่านจุด P", "เส้นแบ่งครึ่งมุมที่จุด P",
                                                     "เส้นที่ทำมุม 45 องศากับเส้นตรง")),
    ]


@question_type("math.parallel_construction_m1", display_name={"th": "สร้างเส้นขนานผ่านจุดที่กำหนด"},
               level=_M1, topic=_CON_TOPIC)
class ParallelConstructionM1(ConceptBankType):
    ITEMS = [
        Concept("การสร้างเส้นตรงผ่านจุด P ให้ขนานกับเส้นตรง ℓ ด้วยวงเวียนและสันตรง อาศัยสมบัติใด",
                "ถ้ามุมแย้งหรือมุมที่สมนัยกันมีขนาดเท่ากัน เส้นตรงสองเส้นนั้นขนานกัน",
                ("ถ้าเส้นตรงสองเส้นยาวเท่ากัน เส้นตรงสองเส้นนั้นขนานกัน",
                 "ถ้าเส้นตรงสองเส้นตั้งฉากกับเส้นตรงต่างเส้นกัน เส้นตรงสองเส้นนั้นขนานกัน",
                 "ถ้ามุมภายในบนข้างเดียวกันมีขนาดเท่ากัน เส้นตรงสองเส้นนั้นขนานกันเสมอ")),
        Concept("ขั้นแรกของการสร้างเส้นตรงผ่านจุด P ให้ขนานกับเส้นตรง ℓ คือข้อใด",
                "ลากเส้นผ่าน P ตัดเส้นตรง ℓ เพื่อให้เกิดมุมที่จุดตัด",
                ("วัดระยะจาก P ถึง ℓ ด้วยไม้บรรทัดแล้วลากเส้นห่างเท่ากัน", "ใช้ไม้โปรแทรกเตอร์วัดมุม 90 องศาที่จุด P",
                 "เขียนวงกลมรอบ P ให้สัมผัสเส้นตรง ℓ แล้วลากเส้นผ่านจุดสัมผัส")),
        Concept("หลังจากลากเส้นผ่าน P ตัดเส้นตรง ℓ แล้ว ขั้นต่อไปในการสร้างเส้นขนานคือข้อใด",
                "สร้างมุมที่ P ให้เท่ากับมุมที่จุดตัดในตำแหน่งที่สมนัยกัน",
                ("แบ่งครึ่งมุมที่จุดตัดแล้วลากเส้นผ่าน P", "สร้างเส้นตั้งฉากกับ ℓ ที่จุดตัด",
                 "แบ่งครึ่งส่วนของเส้นตรงจาก P ถึงจุดตัด")),
    ]


_TRIANGLE_DATA = (
    ("ความยาวของด้านทั้งสามด้าน", True), ("ความยาวของด้านสองด้านและขนาดของมุมระหว่างด้านทั้งสอง", True),
    ("ขนาดของมุมสองมุมและความยาวของด้านระหว่างมุมทั้งสอง", True),
    ("ขนาดของมุมทั้งสามมุม", False), ("ความยาวของด้านสองด้านเท่านั้น", False),
    ("ขนาดของมุมหนึ่งมุมและความยาวของด้านหนึ่งด้านเท่านั้น", False),
)


@question_type("math.triangle_data_m1", display_name={"th": "ข้อมูลที่ใช้สร้างรูปสามเหลี่ยมได้เพียงรูปเดียว"},
               level=_M1, topic=_CON_TOPIC)
class TriangleDataM1(ChoiceType):
    def compose(self, rng: Random):
        unique = rng.random() < 0.5
        right = rng.choice([d for d, ok in _TRIANGLE_DATA if ok == unique])
        wrongs = [d for d, ok in _TRIANGLE_DATA if ok != unique]
        ask = ("ข้อมูลในข้อใดเพียงพอที่จะสร้างรูปสามเหลี่ยมได้เพียงรูปเดียว" if unique
               else "ข้อมูลในข้อใดไม่เพียงพอที่จะสร้างรูปสามเหลี่ยมให้ได้เพียงรูปเดียว")
        return ask, right, wrongs

"""วงกลม

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.3/3

Sets moved here from: math, math_diagrams_geo, math_geometry, math_m3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import CIRCLE_ANGLES, TANGENTS, CircleAngle, Tangent
from otk.sets._support.math_m2 import triple
from otk.sets._support.math_m3 import LEVEL

PROVENANCE = Provenance("original")


def circle_alt(c: CircleAngle) -> str:
    return {
        "central": f"วงกลมจุดศูนย์กลาง O จุด A B C อยู่บนวงกลม มุม AOB กำกับ {c.value} องศา มุม ACB กำกับ x",
        "inscribed": f"วงกลมจุดศูนย์กลาง O จุด A B C อยู่บนวงกลม มุม ACB กำกับ {c.value} องศา มุม AOB กำกับ x",
        "semi": f"วงกลมมี AB เป็นเส้นผ่านศูนย์กลาง C อยู่บนวงกลม มุม CAB กำกับ {c.value} องศา มุม CBA กำกับ x",
        "cyclic": f"รูปสี่เหลี่ยม ABCD แนบในวงกลม มุม A กำกับ {c.value} องศา มุม C กำกับ x",
    }[c.kind]


def tangent_alt(t: Tangent) -> str:
    return {
        "pt": f"วงกลมจุดศูนย์กลาง O รัศมี OT ยาว {t.a} หน่วย PT สัมผัสวงกลมที่ T OP ยาว {t.b} หน่วย PT กำกับ x",
        "op": f"วงกลมจุดศูนย์กลาง O รัศมี OT ยาว {t.a} หน่วย PT สัมผัสวงกลมที่ T ยาว {t.b} หน่วย OP กำกับ x",
        "two": f"PA และ PB สัมผัสวงกลมที่ A และ B PA ยาว {t.a} หน่วย PB กำกับ x",
        "angle": f"PA และ PB สัมผัสวงกลมจุดศูนย์กลาง O ที่ A และ B มุม APB กำกับ {t.a} องศา มุม AOB กำกับ x",
    }[t.kind]


@question_type("math.central_inscribed_angle",
               display_name={"th": "มุมที่จุดศูนย์กลางกับมุมในส่วนโค้ง"},
               level={"th": "ม.3"}, topic="วงกลม")
class CentralInscribedAngle(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(20, 80)
        prompt = rng.choice((
            f"มุมในส่วนโค้งที่รองรับส่วนโค้งเดียวกันมีขนาด {a} องศา มุมที่จุดศูนย์กลางเท่าใด?",
            f"O เป็นจุดศูนย์กลางของวงกลม จุด A, B และ C อยู่บนวงกลม ถ้า ∠ACB = {a}° "
            f"∠AOB มีขนาดกี่องศา",
            f"จากจุด P บนวงกลม มองคอร์ด AB เป็นมุม {a} องศา มุมที่จุดศูนย์กลางซึ่งรองรับคอร์ด AB "
            f"ด้านเดียวกันมีขนาดกี่องศา",
        ))
        return MathDraw("", str(2 * a), prompt=prompt,
                        distractors=[str(a), str(a // 2), str(180 - a)])


@question_type("math.inscribed_angle_semicircle",
               display_name={"th": "มุมในครึ่งวงกลม"},
               level={"th": "ม.3"}, topic="วงกลม")
class InscribedAngleSemicircle(WordProblem):
    """Thales: an angle standing on a diameter is a right angle, so the other two
    angles of the triangle are complementary."""

    def expr(self, rng: Random, lo: int = 20, hi: int = 70):
        a = rng.randint(lo, hi)
        prompt = rng.choice((
            f"AB เป็นเส้นผ่านศูนย์กลางของวงกลม และ C เป็นจุดบนวงกลม "
            f"ถ้ามุม ABC มีขนาด {a} องศา แล้วมุม BAC มีขนาดกี่องศา",
            f"PQ เป็นเส้นผ่านศูนย์กลางของวงกลม และ R เป็นจุดบนวงกลม "
            f"ถ้ามุม PQR มีขนาด {a} องศา แล้วมุม QPR มีขนาดกี่องศา",
            f"รูปสามเหลี่ยมแนบในวงกลมรูปหนึ่งมีด้านหนึ่งเป็นเส้นผ่านศูนย์กลาง มุมแหลมมุมหนึ่ง"
            f"มีขนาด {a} องศา มุมแหลมอีกมุมหนึ่งมีขนาดกี่องศา",
        ))
        return MathDraw(
            "", str(90 - a), prompt=prompt,
            hint=r"\angle ACB = 90^\circ",
            distractors=[str(a), "90", str(180 - a)])


@question_type("math.circle_angle_picture_m3", display_name={"th": "หาขนาดของมุมในวงกลมจากรูป"},
               level={"th": "ม.3"}, topic="วงกลม")
class CircleAnglePictureM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(CIRCLE_ANGLES)
        ans = c.answer
        # Halving where it should double (and back), and the other theorem's rule.
        wrongs = {"central": [c.value, 2 * c.value, 180 - c.value],
                  "inscribed": [c.value, c.value // 2 or 1, 180 - c.value],
                  "semi": [c.value, 180 - c.value, 90],
                  "cyclic": [c.value, 90 - c.value if c.value < 90 else c.value - 90, 360 - c.value]}[c.kind]
        return _math_q([text("จากรูป จงหาขนาดของมุม x (องศา)"), _img(c.asset_id, circle_alt(c))], str(ans),
                       [str(w) for w in wrongs], self.topic)


@question_type("math.cyclic_quadrilateral",
               display_name={"th": "มุมตรงข้ามของสี่เหลี่ยมแนบในวงกลม"},
               level={"th": "ม.3"}, topic="วงกลม")
class CyclicQuadrilateral(WordProblem):
    def expr(self, rng: Random, lo: int = 40, hi: int = 140):
        a = rng.randint(lo, hi)
        prompt = rng.choice((
            f"ABCD เป็นรูปสี่เหลี่ยมแนบในวงกลม ถ้ามุม A มีขนาด {a} องศา แล้วมุม C มีขนาดกี่องศา",
            f"PQRS เป็นรูปสี่เหลี่ยมแนบในวงกลม ถ้ามุม Q มีขนาด {a} องศา แล้วมุม S มีขนาดกี่องศา",
            f"รูปสี่เหลี่ยมรูปหนึ่งมีจุดยอดทั้งสี่อยู่บนวงกลมวงเดียวกัน มุมหนึ่งมีขนาด {a} องศา "
            f"มุมที่อยู่ตรงข้ามมีขนาดกี่องศา",
        ))
        return MathDraw(
            "", str(180 - a), prompt=prompt,
            hint=r"\angle A + \angle C = 180^\circ",
            distractors=[str(a), str(90 - a if a < 90 else a - 90),
                         str(360 - a)])


@question_type("math.tangent_picture_m3", display_name={"th": "เส้นสัมผัสวงกลมจากรูป"},
               level={"th": "ม.3"}, topic="วงกลม")
class TangentPictureM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(TANGENTS)
        ans = t.answer
        wrongs = {"pt": [t.b - t.a, t.b + t.a, t.b],
                  "op": [t.a + t.b, t.b - t.a, t.b],
                  "two": [2 * t.a, t.a + 1, t.a // 2 or 1],
                  "angle": [t.a, 90 - t.a // 2, 360 - t.a]}[t.kind]
        ask = "จงหาขนาดของมุม x (องศา)" if t.kind == "angle" else "จงหาค่า x"
        return _math_q([text(f"จากรูป เส้นตรงที่แตะวงกลมเป็นเส้นสัมผัส {ask}"), _img(t.asset_id, tangent_alt(t))],
                       str(ans), [str(w) for w in wrongs], self.topic)


@question_type("math.tangent_length_m3",
               display_name={"th": "เส้นสัมผัสวงกลม"},
               level=LEVEL, topic="วงกลม")
class TangentLengthM3(WordProblem):
    def expr(self, rng: Random):
        r, t, d = triple(rng, 3)
        if rng.random() < 0.5:
            r, t = t, r
        if rng.random() < 0.5:
            prompt = rng.choice((
                f"จุด P อยู่ห่างจากจุดศูนย์กลางของวงกลมที่มีรัศมี {r} ซม. เป็นระยะ {d} ซม. "
                f"ลากเส้นสัมผัสจาก P ไปสัมผัสวงกลมที่จุด T ส่วนของเส้นตรง PT ยาวกี่เซนติเมตร",
                f"สระน้ำรูปวงกลมรัศมี {r} เมตร ต้นไม้ต้นหนึ่งอยู่ห่างจากจุดศูนย์กลางสระ {d} เมตร "
                f"ขึงเชือกจากต้นไม้ไปแตะขอบสระพอดีที่จุดเดียว เชือกยาวกี่เมตร",
            ))
            return MathDraw("", str(t), prompt=prompt,
                            # d − r treats the tangent as the gap to the circle.
                            distractors=_story.keep(d - r, d + r, d, answer=t, lo=1))
        return MathDraw("", "90",
                        prompt=(f"เส้นตรง PT สัมผัสวงกลมที่มีจุดศูนย์กลาง O ที่จุด T ถ้า OT ยาว {r} ซม. "
                                f"และ PT ยาว {t} ซม. มุม OTP มีขนาดกี่องศา"),
                        distractors=["45", "60", "180"])

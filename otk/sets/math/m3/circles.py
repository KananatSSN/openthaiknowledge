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

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More circles (2026-11): an inscribed angle from the central one, two tangents from a point, a chord from
# its distance to the centre, and inscribed angles on one arc ──

_TRIPLES3 = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20))


@question_type("math.inscribed_from_central_m3", display_name={"th": "มุมในส่วนโค้งจากมุมที่จุดศูนย์กลาง"},
               level=LEVEL, topic="วงกลม")
class InscribedFromCentralM3(WordProblem):
    def expr(self, rng: Random):
        central = 2 * rng.randint(15, 85)
        right = central // 2
        prompt = (f"มุมที่จุดศูนย์กลางของวงกลมมีขนาด {central} องศา "
                  "มุมในส่วนโค้งที่รองรับด้วยส่วนโค้งเดียวกันมีขนาดกี่องศา")
        # Doubled instead; the same; what is left of a straight angle.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(2 * central, central, 180 - central, 90 - right, answer=right, lo=1))


@question_type("math.two_tangents_m3", display_name={"th": "เส้นสัมผัสสองเส้นจากจุดภายนอก"},
               level=LEVEL, topic="วงกลม")
class TwoTangentsM3(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            length = rng.randint(5, 30)
            prompt = (f"PA และ PB เป็นเส้นสัมผัสวงกลมที่จุด A และ B จากจุด P ภายนอกวงกลม "
                      f"ถ้า PA ยาว {length} เซนติเมตร PB ยาวกี่เซนติเมตร")
            return MathDraw("", str(length), prompt=prompt,
                            distractors=_story.keep(2 * length, length // 2 if length > 9 else length + 4, length + 1,
                                                    answer=length, lo=1))
        apb = rng.randint(20, 140)
        right = 180 - apb
        prompt = (f"PA และ PB เป็นเส้นสัมผัสวงกลมที่มีจุดศูนย์กลาง O ที่จุด A และ B ถ้ามุม APB มีขนาด {apb} องศา "
                  "มุม AOB มีขนาดกี่องศา")
        # The same angle; a full turn less it; a right angle less it.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(apb, 360 - apb, abs(90 - apb), right + 10, answer=right, lo=1))


@question_type("math.chord_from_distance_m3", display_name={"th": "ความยาวคอร์ดจากระยะห่างถึงจุดศูนย์กลาง"},
               level=LEVEL, topic="วงกลม")
class ChordFromDistanceM3(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES3)
        d, half = rng.sample((a, b), 2)
        right = 2 * half
        prompt = (f"วงกลมรัศมี {c} เซนติเมตร คอร์ดเส้นหนึ่งอยู่ห่างจากจุดศูนย์กลาง {d} เซนติเมตร "
                  "คอร์ดเส้นนี้ยาวกี่เซนติเมตร")
        # Half the chord; the radius less the distance; the diameter.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(half, 2 * (c - d), 2 * c, c + d, answer=right, lo=1))


@question_type("math.angles_same_arc_m3", display_name={"th": "มุมในส่วนโค้งที่รองรับด้วยส่วนโค้งเดียวกัน"},
               level=LEVEL, topic="วงกลม")
class AnglesSameArcM3(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(20, 80)
        prompt = (f"จุด A, B, C และ D อยู่บนวงกลมเดียวกัน โดย C และ D อยู่ด้านเดียวกันของคอร์ด AB "
                  f"ถ้ามุม ACB มีขนาด {a} องศา มุม ADB มีขนาดกี่องศา")
        # Doubled as if central; the supplement; half.
        return MathDraw("", str(a), prompt=prompt,
                        distractors=_story.keep(2 * a, 180 - a, a // 2, 90 - a if a != 45 else a + 10, answer=a, lo=1))

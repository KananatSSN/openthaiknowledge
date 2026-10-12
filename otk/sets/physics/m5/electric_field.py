"""สนามไฟฟ้าและแรงไฟฟ้าที่กระทำต่อประจุในสนามไฟฟ้า

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/3

Sets moved here from: science_wave_f10.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f10 import DISTANCES, MICRO, SUBJECT, UPPER_FIVE, K, _exact

PROVENANCE = Provenance("original")


TOPIC_FIELD = "สนามไฟฟ้าและแรงไฟฟ้าที่กระทำต่อประจุในสนามไฟฟ้า"


def _field(q: int, r: Fraction) -> Fraction:
    return K * abs(q) * MICRO / (r * r)


FIELD_FACTS = (
    ("สนามไฟฟ้าของจุดประจุบวกมีทิศใด", "พุ่งออกจากประจุ", ("พุ่งเข้าหาประจุ", "วนรอบประจุ", "ขนานกับแกนหนึ่งเสมอ")),
    ("สนามไฟฟ้าของจุดประจุลบมีทิศใด", "พุ่งเข้าหาประจุ", ("พุ่งออกจากประจุ", "วนรอบประจุ", "ขนานกับแกนหนึ่งเสมอ")),
    ("อิเล็กตรอนในสนามไฟฟ้าได้รับแรงทิศใด", "ทิศตรงข้ามกับสนามไฟฟ้า",
     ("ทิศเดียวกับสนามไฟฟ้า", "ตั้งฉากกับสนามไฟฟ้า", "ไม่ได้รับแรง")),
    ("สนามไฟฟ้าระหว่างแผ่นโลหะขนานที่มีประจุตรงข้ามเป็นอย่างไร", "สม่ำเสมอ มีทิศจากแผ่นบวกไปแผ่นลบ",
     ("สม่ำเสมอ มีทิศจากแผ่นลบไปแผ่นบวก", "เป็นศูนย์", "แรงขึ้นใกล้แผ่นลบเท่านั้น")),
    ("หน่วยของสนามไฟฟ้าคือข้อใด", "N/C ซึ่งเท่ากับ V/m", ("C/N", "N·C", "J/C")),
)


@question_type(
    "phys.electric_field_foundation",
    display_name={"th": "ทิศของสนามไฟฟ้าและแรงที่กระทำต่อประจุในสนามไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class ElectricFieldFoundation(QuestionType):
    """Which way the field points, and F = qE."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(FIELD_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FIELD,
                             hint="สนามไฟฟ้ามีทิศเดียวกับแรงที่กระทำต่อประจุบวกทดสอบ")
        q = rng.randint(1, 20)
        e = rng.randint(1, 50) * 10 ** rng.randint(4, 5)
        return numeric(
            stem=f"ประจุ {q} μC อยู่ในสนามไฟฟ้าสม่ำเสมอขนาด {e:,} N/C ได้รับแรงไฟฟ้าขนาดเท่าใด",
            answer=q * e * MICRO, wrongs=[q * e * MICRO * 1000, Fraction(e, q) * MICRO, q * e * MICRO / 10],
            unit="N", topic=TOPIC_FIELD, hint="F = qE แปลง μC เป็น 10⁻⁶ C")


@question_type(
    "phys.electric_field_fluency",
    display_name={"th": "คำนวณสนามไฟฟ้าของจุดประจุ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class ElectricFieldFluency(QuestionType):
    """E = kq/r², and the charge back from a measured field."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        q, r = rng.choice([(q, r) for q in range(1, 21) for r in DISTANCES if _exact(_field(q, r))])
        e = _field(q, r)
        if rng.random() < 0.6:
            return numeric(
                stem=f"จุดประจุ {q} μC สนามไฟฟ้าที่ตำแหน่งห่างจากประจุ {show(r * 100)} cm มีขนาดเท่าใด (k = 9 × 10⁹ N·m²/C²)",
                answer=e, wrongs=[e * r, e / 2, e * 4], unit="N/C", topic=TOPIC_FIELD,
                hint="E = kq/r² (q เป็นคูลอมบ์ r เป็นเมตร)")
        return numeric(
            stem=(f"ที่ตำแหน่งห่างจากจุดประจุ {show(r * 100)} cm สนามไฟฟ้ามีขนาด {show(e)} N/C "
                  "จุดประจุมีขนาดกี่ไมโครคูลอมบ์ (k = 9 × 10⁹ N·m²/C²)"),
            answer=q, wrongs=[q * 2, Fraction(q, 2), q * 4], unit="μC", topic=TOPIC_FIELD,
            hint="q = Er²/k แล้วแปลงเป็นไมโครคูลอมบ์")


@question_type(
    "phys.electric_field_application",
    display_name={"th": "สนามไฟฟ้าลัพธ์จากจุดประจุหลายจุดแบบเวกเตอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class ElectricFieldApplication(QuestionType):
    """Fields from two charges on a line add or cancel; at right angles they add as vectors."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            sb = rng.choice((1, -1))
            # Equal like charges would cancel exactly at the midpoint; leave that case out.
            qa, qb, d = rng.choice([(a, b, d) for a in range(1, 13) for b in range(1, 13) if sb < 0 or a != b
                                    for d in (Fraction(1, 10), Fraction(3, 10), Fraction(1, 2), Fraction(3, 2), 3)
                                    if _exact(_field(a, d)) and _exact(_field(b, d))])
            ea, eb = _field(qa, d), _field(qb, d)
            # At the midpoint A's field points toward B; B's points toward B only if B is negative.
            answer = ea + eb if sb < 0 else abs(ea - eb)
            return numeric(
                stem=(f"จุดประจุ A = +{qa} μC และ B = {'+' if sb > 0 else '−'}{qb} μC วางห่างกัน {show(d * 2)} m "
                      "สนามไฟฟ้าลัพธ์ที่จุดกึ่งกลางระหว่าง A กับ B มีขนาดเท่าใด (k = 9 × 10⁹ N·m²/C²)"),
                answer=answer, wrongs=[abs(ea - eb) if sb < 0 else ea + eb, max(ea, eb), (ea + eb) / 2],
                unit="N/C", topic=TOPIC_FIELD,
                hint="หาสนามจากแต่ละประจุ ประจุชนิดเดียวกันสนามที่จุดกึ่งกลางมีทิศตรงข้ามจึงลบกัน ต่างชนิดทิศเดียวกันจึงบวกกัน")
        e1, e2, total = rng.choice(((3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)))
        scale = rng.choice((100, 1000, 10000, 2000, 5000))
        return numeric(
            stem=(f"ที่จุด P มีสนามไฟฟ้าจากจุดประจุสองจุด ขนาด {e1 * scale:,} N/C และ {e2 * scale:,} N/C ในทิศตั้งฉากกัน "
                  "สนามไฟฟ้าลัพธ์ที่ P มีขนาดเท่าใด"),
            answer=total * scale, wrongs=[(e1 + e2) * scale, abs(e2 - e1) * scale, (e1 + e2) * scale // 2],
            unit="N/C", topic=TOPIC_FIELD, hint="สนามไฟฟ้าเป็นเวกเตอร์: ตั้งฉากกันรวมด้วย E = √(E₁² + E₂²)")

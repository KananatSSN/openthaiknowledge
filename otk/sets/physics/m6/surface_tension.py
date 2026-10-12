"""ความตึงผิวและแรงหนืดของของเหลว

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/5

Sets moved here from: science_wave_f15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f15 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_SURFACE = "ความตึงผิวและแรงหนืดของของเหลว"


SURFACE_FACTS = (
    ("ความตึงผิวของของเหลวเกิดจากอะไร", "แรงยึดเหนี่ยวระหว่างโมเลกุลที่ดึงผิวของเหลวเข้าหาภายใน",
     ("แรงโน้มถ่วงที่กระทำต่อผิวของเหลวจนผิวถูกดึงให้ตึง", "ความดันอากาศที่กดผิวของเหลวลงทุกทิศทาง", "แรงลอยตัวของของเหลวที่ดันผิวขึ้นด้านบน")),
    ("หยดน้ำขนาดเล็กมีรูปร่างเกือบเป็นทรงกลม เพราะเหตุใด", "ความตึงผิวทำให้ผิวของเหลวมีพื้นที่น้อยที่สุด",
     ("แรงโน้มถ่วงดึงเข้าหาจุดศูนย์กลางของหยดน้ำ", "อากาศกดทุกด้านเท่ากันจนหยดน้ำกลม", "น้ำมีความหนืดมากจึงคงรูปทรงกลม")),
    ("เติมผงซักฟอกลงในน้ำ ความตึงผิวของน้ำเปลี่ยนไปอย่างไร", "ลดลง น้ำจึงแทรกซึมเข้าเส้นใยผ้าได้ดีขึ้น",
     ("เพิ่มขึ้น", "ไม่เปลี่ยน", "กลายเป็นศูนย์ทันทีจนน้ำไม่มีผิว")),
    ("แมลงจิงโจ้น้ำเดินบนผิวน้ำได้เพราะอะไร", "ความตึงผิวของน้ำรับน้ำหนักขาที่กดผิวน้ำไว้",
     ("แรงลอยตัวมากกว่าน้ำหนักของแมลงมาก", "ขาของแมลงดูดน้ำขึ้นมาช่วยพยุงตัว", "น้ำมีความหนืดสูงจึงพยุงขาแมลงไว้")),
    ("เมื่ออุณหภูมิสูงขึ้น ความหนืดของของเหลวเช่นน้ำผึ้งเป็นอย่างไร", "ลดลง จึงไหลได้ง่ายขึ้น",
     ("เพิ่มขึ้น", "ไม่เปลี่ยน", "เพิ่มแล้วลด")),
    ("ลูกเหล็กตกในน้ำมันหนืดจนมีความเร็วคงตัว (ความเร็วปลาย) เพราะเหตุใด", "แรงหนืดรวมกับแรงลอยตัวเท่ากับน้ำหนักของลูกเหล็ก",
     ("แรงหนืดหายไป", "น้ำหนักของลูกเหล็กลดลง", "แรงลอยตัวมากกว่าน้ำหนัก")),
)


@question_type(
    "phys.surface_tension_foundation",
    display_name={"th": "ความตึงผิวและความหนืดในชีวิตประจำวัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SURFACE,
)
class SurfaceTensionFoundation(QuestionType):
    """What surface tension and viscosity do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            stem, correct, wrongs = rng.choice(SURFACE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SURFACE,
                             hint="ความตึงผิวทำให้ผิวของเหลวเหมือนแผ่นยางยืด ความหนืดคือแรงต้านการไหล")
        gamma = Fraction(rng.randint(2, 8), 100)
        length = Fraction(rng.randint(1, 20), 100)
        force = gamma * length
        if not _exact(force * 1000):
            length = Fraction(rng.randint(1, 10) * 10, 100)
            force = gamma * length
        return numeric(
            stem=(f"ของเหลวมีความตึงผิว {show(gamma)} N/m ผิวของเหลวยาว {show(length * 100)} cm ดึงขอบวัตถุด้านเดียว "
                  "ด้วยแรงกี่มิลลินิวตัน"),
            answer=force * 1000, wrongs=[force * 2000, force * 10, gamma * 1000], unit="mN", topic=TOPIC_SURFACE,
            hint="แรงจากความตึงผิว F = γL เมื่อผิวดึงด้านเดียว")


@question_type(
    "phys.surface_tension_fluency",
    display_name={"th": "คำนวณความตึงผิวจากโครงลวดและฟิล์มสบู่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SURFACE,
)
class SurfaceTensionFluency(QuestionType):
    """A film has two faces: γ = F/(2L)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        gamma, length = rng.choice([(Fraction(g, 1000), Fraction(ell, 100)) for g in (20, 25, 30, 40, 50, 60, 70, 72, 75)
                                    for ell in (2, 4, 5, 8, 10, 12, 15, 20) if _exact(Fraction(g, 1000) * Fraction(ell, 100) * 2000)])
        force_mn = gamma * length * 2 * 1000
        if rng.random() < 0.55:
            return numeric(
                stem=(f"ยกโครงลวดยาว {show(length * 100)} cm ขึ้นจากน้ำสบู่ มีฟิล์มสบู่ติดขึ้นมา วัดแรงที่ฟิล์มดึงได้ "
                      f"{show(force_mn)} mN ความตึงผิวของน้ำสบู่กี่มิลลินิวตันต่อเมตร"),
                answer=gamma * 1000, wrongs=[gamma * 2000, force_mn / length / 100, gamma * 100], unit="mN/m",
                topic=TOPIC_SURFACE, hint="ฟิล์มมีสองผิว F = 2γL ดังนั้น γ = F/(2L)")
        return numeric(
            stem=(f"น้ำสบู่มีความตึงผิว {show(gamma * 1000)} mN/m โครงลวดยาว {show(length * 100)} cm ที่มีฟิล์มสบู่ "
                  "ถูกฟิล์มดึงด้วยแรงกี่มิลลินิวตัน"),
            answer=force_mn, wrongs=[force_mn / 2, force_mn * 10, gamma * length * 1000 * 4], unit="mN",
            topic=TOPIC_SURFACE, hint="ฟิล์มมีสองผิว F = 2γL")


@question_type(
    "phys.surface_tension_application",
    display_name={"th": "ใช้ความตึงผิวอธิบายปรากฏการณ์และหาแรงที่ต้องใช้"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SURFACE,
)
class SurfaceTensionApplication(QuestionType):
    """Pulling a ring free of water: the weight plus γ times both edges."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        gamma = rng.choice((Fraction(7, 100), Fraction(3, 100), Fraction(5, 100)))
        edge = Fraction(rng.randint(1, 20), 100)
        weight_mn = rng.randint(1, 50)
        pull = weight_mn + gamma * 2 * edge * 1000
        if not _exact(pull):
            edge = Fraction(rng.randint(1, 10) * 10, 100)
            pull = weight_mn + gamma * 2 * edge * 1000
        what = rng.choice(("วงแหวนลวดบาง", "แผ่นกระจกสไลด์", "ใบมีดโกนบาง"))
        return numeric(
            stem=(f"{what}หนัก {weight_mn} mN แตะผิวน้ำ ผิวน้ำเกาะขอบซึ่งยาวรวม {show(edge * 100)} cm ทั้งด้านในและด้านนอก "
                  f"ต้องออกแรงดึงขึ้นอย่างน้อยกี่มิลลินิวตันจึงหลุดจากผิวน้ำ (ความตึงผิวของน้ำ {show(gamma)} N/m)"),
            answer=pull, wrongs=[weight_mn + gamma * edge * 1000, gamma * 2 * edge * 1000, pull + weight_mn],
            unit="mN", topic=TOPIC_SURFACE,
            hint="แรงดึง = น้ำหนัก + แรงตึงผิวที่ดึงลง ซึ่งเท่ากับ γ × ความยาวขอบ × 2 (ผิวน้ำเกาะสองด้าน)")

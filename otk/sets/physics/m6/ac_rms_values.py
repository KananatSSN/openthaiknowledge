"""ความต่างศักย์และกระแสไฟฟ้าอาร์เอ็มเอส

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/5

Sets moved here from: science_wave_f13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f13 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_RMS = "ความต่างศักย์และกระแสไฟฟ้าอาร์เอ็มเอส"


def _root2(x) -> str:
    return f"{show(x)}√2"


RMS_FACTS = (
    ("ค่าอาร์เอ็มเอสของไฟฟ้ากระแสสลับหมายถึงอะไร", "ค่าของไฟฟ้ากระแสตรงที่ให้ความร้อนในตัวต้านทานเท่ากันในเวลาเท่ากัน",
     ("ค่าสูงสุดของกระแสสลับ", "ค่าเฉลี่ยของกระแสสลับในหนึ่งรอบ ซึ่งเป็นศูนย์", "ค่าต่ำสุดของกระแสสลับ")),
    ("ไฟฟ้าตามบ้านในประเทศไทย 220 V 50 Hz ค่า 220 V คือค่าใด", "ความต่างศักย์อาร์เอ็มเอส",
     ("ความต่างศักย์สูงสุด", "ความต่างศักย์เฉลี่ยในหนึ่งรอบ", "ความต่างศักย์ต่ำสุด")),
    ("แอมมิเตอร์และโวลต์มิเตอร์สำหรับไฟฟ้ากระแสสลับอ่านค่าใด", "ค่าอาร์เอ็มเอส",
     ("ค่าสูงสุด", "ค่าเฉลี่ยซึ่งเป็นศูนย์", "ค่าขณะหนึ่งแบบสุ่ม")),
    ("ไฟฟ้ากระแสสลับ 50 Hz เปลี่ยนทิศกี่ครั้งในหนึ่งวินาที", "100 ครั้ง",
     ("50 ครั้ง", "25 ครั้ง", "220 ครั้ง")),
)


@question_type(
    "phys.ac_rms_foundation",
    display_name={"th": "ความหมายของค่าอาร์เอ็มเอสและความสัมพันธ์กับค่าสูงสุด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RMS,
)
class AcRmsFoundation(QuestionType):
    """What rms means, and V_max = √2 V_rms each way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(RMS_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_RMS,
                             hint="ค่าอาร์เอ็มเอสคือค่ากระแสตรงที่ให้ผลความร้อนเท่ากัน มิเตอร์กระแสสลับอ่านค่านี้")
        rms = rng.choice((6, 12, 24, 100, 110, 120, 220, 230, 240)) if rng.random() < 0.6 else rng.randint(1, 30)
        if rng.random() < 0.3:
            return numeric(
                stem=f"กระแสไฟฟ้าสลับมีค่าสูงสุด {rms}√2 A กระแสอาร์เอ็มเอสเท่าใด",
                answer=rms, wrongs=[rms * 2, Fraction(rms, 2), rms + 1], unit="A", topic=TOPIC_RMS,
                hint="I_rms = I_max ÷ √2")
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ไฟฟ้ากระแสสลับมีความต่างศักย์อาร์เอ็มเอส {rms} V ความต่างศักย์สูงสุดเท่าใด",
                correct=f"{_root2(rms)} V",
                wrongs=(f"{show(Fraction(rms, 2))}√2 V", f"{rms} V", f"{rms * 2} V"),
                topic=TOPIC_RMS, hint="V_max = √2 × V_rms")
        return numeric(
            stem=f"ไฟฟ้ากระแสสลับมีความต่างศักย์สูงสุด {rms}√2 V ความต่างศักย์อาร์เอ็มเอสเท่าใด",
            answer=rms, wrongs=[rms * 2, Fraction(rms, 2), rms + 10], unit="V", topic=TOPIC_RMS,
            hint="V_rms = V_max ÷ √2")


@question_type(
    "phys.ac_rms_fluency",
    display_name={"th": "คำนวณกระแสและกำลังเฉลี่ยจากค่าอาร์เอ็มเอส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RMS,
)
class AcRmsFluency(QuestionType):
    """I_rms = V_rms/R and P = V_rms I_rms = V_rms²/R, as with direct current."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        v, r = rng.choice([(v, r) for v in (12, 24, 100, 110, 220) for r in (4, 5, 10, 11, 20, 22, 40, 44, 50, 55, 100, 110)
                           if _exact(Fraction(v, r)) and _exact(Fraction(v * v, r))])
        i = Fraction(v, r)
        if rng.random() < 0.5:
            return numeric(stem=f"ต่อตัวต้านทาน {r} Ω กับไฟฟ้ากระแสสลับ {v} V (อาร์เอ็มเอส) กระแสอาร์เอ็มเอสเท่าใด",
                           answer=i, wrongs=[i * 2, Fraction(r, v), i / 2], unit="A", topic=TOPIC_RMS,
                           hint="ใช้ค่าอาร์เอ็มเอสกับกฎของโอห์มได้เหมือนไฟฟ้ากระแสตรง: I = V/R")
        return numeric(stem=f"ต่อตัวต้านทาน {r} Ω กับไฟฟ้ากระแสสลับ {v} V (อาร์เอ็มเอส) กำลังไฟฟ้าเฉลี่ยเท่าใด",
                       answer=v * i, wrongs=[2 * v * i, v * i / 2, Fraction(v, r)], unit="W", topic=TOPIC_RMS,
                       hint="กำลังเฉลี่ย P = V_rms × I_rms = V_rms²/R (ถ้าใช้ค่าสูงสุดต้องหารด้วย 2)")


@question_type(
    "phys.ac_rms_application",
    display_name={"th": "กระแสอาร์เอ็มเอสและกระแสสูงสุดของเครื่องใช้ไฟฟ้า"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_RMS,
)
class AcRmsApplication(QuestionType):
    """An appliance's rating gives I_rms = P/V_rms; the peak is √2 times that."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        power = rng.choice([p for p in (110, 220, 330, 440, 550, 660, 880, 1100, 1320, 1650, 2200) if _exact(Fraction(p, 220))])
        device = rng.choice(("กาต้มน้ำไฟฟ้า", "เตารีด", "หม้อหุงข้าว", "เครื่องเป่าผม", "เตาไฟฟ้า"))
        i = Fraction(power, 220)
        if rng.random() < 0.5:
            return numeric(stem=f"{device} {power:,} W ใช้กับไฟบ้าน 220 V (อาร์เอ็มเอส) มีกระแสอาร์เอ็มเอสเท่าใด",
                           answer=i, wrongs=[i * 2, Fraction(220, power) * 10, i + 1], unit="A", topic=TOPIC_RMS,
                           hint="I_rms = P ÷ V_rms")
        return _labelled(
            stem=f"{device} {power:,} W ใช้กับไฟบ้าน 220 V (อาร์เอ็มเอส) กระแสสูงสุดที่ผ่านเครื่องเท่าใด",
            correct=f"{_root2(i)} A", wrongs=(f"{show(i)} A", f"{show(i * 2)} A", f"{show(i / 2)}√2 A"),
            topic=TOPIC_RMS, hint="หา I_rms = P/V_rms ก่อน แล้ว I_max = √2 × I_rms")

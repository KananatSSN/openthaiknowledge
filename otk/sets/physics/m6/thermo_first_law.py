"""งาน ความร้อน และพลังงานภายในระบบ

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/9

Sets moved here from: science_wave_f16.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f16 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_THERMO = "งาน ความร้อน และพลังงานภายในระบบ"


THERMO_FACTS = (
    ("อัดแก๊สในกระบอกสูบอย่างรวดเร็ว (ไม่มีเวลาถ่ายเทความร้อน) อุณหภูมิของแก๊สเปลี่ยนไปอย่างไร", "สูงขึ้น เพราะงานที่ทำต่อแก๊สเพิ่มพลังงานภายใน",
     ("ลดลง", "คงตัว", "เป็นศูนย์")),
    ("ฉีดสเปรย์ออกจากกระป๋องนาน ๆ กระป๋องเย็นลง เพราะเหตุใด", "แก๊สที่ขยายตัวทำงาน พลังงานภายในจึงลดลง",
     ("สเปรย์ดูดความร้อนจากอากาศภายนอก", "กระป๋องได้รับงานจากภายนอก", "แรงเสียดทานในหัวฉีด")),
    ("สูบลมยางจักรยานแรง ๆ แล้วตัวสูบร้อนขึ้น เพราะเหตุใด", "งานที่ใช้อัดอากาศทำให้พลังงานภายในของอากาศเพิ่มขึ้น",
     ("อากาศภายนอกร้อนขึ้น", "ยางดูดความร้อนจากถนน", "อากาศในสูบขยายตัว")),
    ("กฎข้อที่หนึ่งของอุณหพลศาสตร์กล่าวว่าอย่างไร", "ความร้อนที่ให้แก่ระบบ = พลังงานภายในที่เพิ่มขึ้น + งานที่ระบบทำ",
     ("พลังงานภายในคงตัวเสมอ", "งานที่ระบบทำมากกว่าความร้อนที่ได้รับเสมอ", "ความร้อนไหลจากที่เย็นไปที่ร้อนเอง")),
    ("ตู้เย็นทำให้ภายในเย็นได้โดยอาศัยหลักการใด", "สารทำความเย็นขยายตัวดูดความร้อนภายในตู้ แล้วถูกอัดคายความร้อนออกด้านหลัง",
     ("สร้างความเย็นขึ้นจากไฟฟ้าโดยตรง", "ปล่อยอากาศเย็นจากภายนอกเข้าไป", "ใช้น้ำแข็งที่เติมไว้")),
)


@question_type(
    "phys.thermo_first_law_foundation",
    display_name={"th": "งานที่ทำโดยแก๊สเมื่อความดันคงตัว W = PΔV"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_THERMO,
)
class ThermoFirstLawFoundation(QuestionType):
    """W = PΔV, with kPa × L giving joules directly."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            stem, correct, wrongs = rng.choice(THERMO_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_THERMO,
                             hint="Q = ΔU + W: งานที่ทำต่อแก๊สเพิ่มพลังงานภายใน แก๊สที่ขยายตัวทำงานจึงเสียพลังงานภายใน")
        p = rng.randint(1, 30) * 10
        v1 = rng.randint(1, 20)
        v2 = v1 + rng.randint(1, 20)
        return numeric(
            stem=f"แก๊สขยายตัวที่ความดันคงตัว {p} kPa จากปริมาตร {v1} L เป็น {v2} L แก๊สทำงานกี่จูล",
            answer=p * (v2 - v1), wrongs=[p * v2, p * (v2 - v1) * 1000, p * (v2 + v1)], unit="J", topic=TOPIC_THERMO,
            hint="W = PΔV และ kPa × L = (10³ Pa)(10⁻³ m³) = J")


@question_type(
    "phys.thermo_first_law_fluency",
    display_name={"th": "ความสัมพันธ์ระหว่างความร้อน พลังงานภายใน และงาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_THERMO,
)
class ThermoFirstLawFluency(QuestionType):
    """ΔU = Q − W with the signs read from the words."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        q = rng.randint(1, 50) * 20
        w = rng.randint(1, 50) * 10
        gains = rng.random() < 0.7
        does_work = rng.random() < 0.7
        heat = q if gains else -q
        work = w if does_work else -w
        du = heat - work
        return numeric(
            stem=(f"แก๊ส{'ได้รับ' if gains else 'คาย'}ความร้อน {q} J และ{'ทำงานต่อสิ่งแวดล้อม' if does_work else 'ถูกสิ่งแวดล้อมทำงานให้'} "
                  f"{w} J พลังงานภายในของแก๊สเปลี่ยนไปกี่จูล (ตอบค่าลบถ้าลดลง)"),
            answer=du, wrongs=[heat + work, -du, q + w], unit="J", topic=TOPIC_THERMO, allow_negative=True,
            hint="ΔU = Q − W โดย Q บวกเมื่อได้รับความร้อน และ W บวกเมื่อแก๊สทำงาน")


@question_type(
    "phys.thermo_first_law_application",
    display_name={"th": "ใช้กฎข้อที่หนึ่งของอุณหพลศาสตร์กับแก๊สที่ขยายตัวที่ความดันคงตัว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_THERMO,
)
class ThermoFirstLawApplication(QuestionType):
    """Heat in, work out at constant pressure, and the internal energy that is left."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p = rng.randint(1, 20) * 10
        dv = rng.randint(1, 10)
        work = p * dv
        du = rng.randint(1, 40) * 10
        heat = du + work
        if rng.random() < 0.5:
            return numeric(
                stem=(f"ให้ความร้อน {heat} J แก่แก๊สในกระบอกสูบ แก๊สดันลูกสูบให้ปริมาตรเพิ่มขึ้น {dv} L ที่ความดันคงตัว {p} kPa "
                      "พลังงานภายในของแก๊สเพิ่มขึ้นกี่จูล"),
                answer=du, wrongs=[heat, heat + work, work], unit="J", topic=TOPIC_THERMO,
                hint="หางาน W = PΔV ก่อน แล้ว ΔU = Q − W")
        return numeric(
            stem=(f"แก๊สในกระบอกสูบขยายตัว {dv} L ที่ความดันคงตัว {p} kPa และพลังงานภายในเพิ่มขึ้น {du} J "
                  "ต้องให้ความร้อนแก่แก๊สกี่จูล"),
            answer=heat, wrongs=[du, work, du - work if du > work else du + 2 * work], unit="J", topic=TOPIC_THERMO,
            hint="Q = ΔU + W โดย W = PΔV")

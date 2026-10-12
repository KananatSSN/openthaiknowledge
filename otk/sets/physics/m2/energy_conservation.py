"""การเปลี่ยนและการถ่ายโอนพลังงานโดยกฎการอนุรักษ์พลังงาน

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.2/6

Sets moved here from: science_wave_d31.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d30 import SECOND_SECONDARY

PROVENANCE = Provenance("original")


ENERGY_CONSERVATION_TOPIC = "การเปลี่ยนและการถ่ายโอนพลังงานโดยกฎการอนุรักษ์พลังงาน"


class EnergyConversion(NamedTuple):
    device: str
    total: int
    output1: str
    value1: int
    output2: str
    value2: int


ENERGY_CONVERSIONS = (
    EnergyConversion("หลอดไฟฟ้าแบบไส้", 100, "พลังงานแสง", 10, "พลังงานความร้อน", 90),
    EnergyConversion("มอเตอร์ไฟฟ้า", 100, "พลังงานกล", 85, "พลังงานความร้อนจากการเสียดทาน", 15),
    EnergyConversion("กังหันลมผลิตไฟฟ้า", 100, "พลังงานไฟฟ้า", 40, "พลังงานความร้อนและเสียงที่สูญเสียไป", 60),
    EnergyConversion("แผงโซลาร์เซลล์", 100, "พลังงานไฟฟ้า", 20, "พลังงานความร้อนที่สะท้อนหรือสูญเสียไป", 80),
    EnergyConversion("หลอดไฟ LED", 100, "พลังงานแสง", 40, "พลังงานความร้อน", 60),
    EnergyConversion("พัดลมไฟฟ้า", 100, "พลังงานจลน์ของใบพัด", 70, "พลังงานความร้อนและเสียง", 30),
    EnergyConversion("เครื่องยนต์รถยนต์", 100, "พลังงานกลที่ขับเคลื่อนรถ", 25, "พลังงานความร้อนที่สูญเสียไป", 75),
    EnergyConversion("ลำโพง", 100, "พลังงานเสียง", 5, "พลังงานความร้อน", 95),
)


CONSERVE_HINT = "พลังงานรวมก่อนและหลังเปลี่ยนรูปต้องเท่ากันเสมอตามกฎการอนุรักษ์พลังงาน"


def _scaled(rng: Random) -> tuple[EnergyConversion, int]:
    """A device from the bank with its input drawn; the shares stay in proportion."""
    item = rng.choice(ENERGY_CONVERSIONS)
    return item, rng.choice((1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20))


ENERGY_CONSERVATION_SCENARIOS = (
    ("โรงไฟฟ้าพลังน้ำแห่งหนึ่งมีประสิทธิภาพ 90% หมายความว่าพลังงานที่ป้อนเข้า 100% ถูกเปลี่ยนเป็นพลังงานไฟฟ้าที่ใช้ได้เพียง 90% ส่วนที่เหลือ 10% หายไปไหน",
     "ส่วนที่เหลือเปลี่ยนเป็นพลังงานความร้อนจากการเสียดทานในเครื่องจักรและระบบ ไม่ได้สูญหายไปจากจักรวาล",
     ("ส่วนที่เหลือสูญหายไปอย่างสิ้นเชิงโดยไม่เปลี่ยนเป็นพลังงานรูปใด", "ประสิทธิภาพ 90% หมายความว่าพลังงานเพิ่มขึ้น 10%", "พลังงานที่เหลือถูกเก็บไว้ในน้ำโดยไม่เปลี่ยนรูป")),
    ("ลูกตุ้มที่แกว่งไปมาในอากาศจะแกว่งได้ต่ำลงเรื่อย ๆ จนหยุดในที่สุด แม้ไม่มีใครไปแตะต้อง พลังงานกลที่ลดลงไปไหน",
     "พลังงานกลเปลี่ยนเป็นพลังงานความร้อนจากแรงต้านอากาศและการเสียดทานที่จุดหมุน ไม่ได้สูญหายไปจากระบบทั้งหมด",
     ("พลังงานกลสูญหายไปอย่างสิ้นเชิงโดยไม่เปลี่ยนเป็นพลังงานรูปใด", "ลูกตุ้มสร้างพลังงานเพิ่มขึ้นเองในทุกรอบการแกว่ง", "อากาศไม่มีผลต่อพลังงานของลูกตุ้มที่แกว่งอยู่เลย")),
    ("รถยนต์ไฟฟ้าที่มีระบบเบรกแบบนำพลังงานกลับ (regenerative braking) สามารถแปลงพลังงานจลน์ของรถขณะเบรกกลับเป็นพลังงานไฟฟ้าได้ ข้อใดอธิบายได้ถูกต้อง",
     "พลังงานจลน์ของรถไม่ได้สูญหายไปเป็นความร้อนที่ผ้าเบรกทั้งหมด แต่บางส่วนถูกเปลี่ยนกลับเป็นพลังงานไฟฟ้าเพื่อเก็บไว้ใช้ใหม่",
     ("รถยนต์ไฟฟ้าสร้างพลังงานเพิ่มขึ้นจากไม่มีอะไรเลยขณะเบรก", "พลังงานจลน์ขณะเบรกไม่มีความสัมพันธ์กับพลังงานไฟฟ้าที่เก็บได้", "ระบบเบรกแบบนี้ทำให้พลังงานรวมของระบบเพิ่มขึ้นเกินพลังงานจลน์เดิม")),
)


@question_type(
    "phys.energy_conservation_foundation",
    display_name={"th": "วิเคราะห์สถานการณ์การเปลี่ยนพลังงานตามกฎการอนุรักษ์พลังงาน"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=ENERGY_CONSERVATION_TOPIC,
)
class EnergyConservationFoundation(QuestionType):
    """Total energy is conserved: it changes form but the total stays the same."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item, k = _scaled(rng)
        total, v1, v2 = item.total * k, item.value1 * k, item.value2 * k
        return _labelled(
            stem=(f"{item.device}เปลี่ยนพลังงานที่ได้รับ {total} จูล เป็น{item.output1} {v1} จูล และ{item.output2} {v2} จูล "
                  "ข้อใดวิเคราะห์สถานการณ์นี้ตามกฎการอนุรักษ์พลังงานได้ถูกต้อง"),
            correct=f"พลังงานไม่ได้สูญหายไปไหน เพียงเปลี่ยนรูป ผลรวมยังเท่ากับ {total} จูล",
            wrongs=(f"พลังงาน {v2} จูล สูญหายไปจากระบบอย่างสิ้นเชิงโดยไม่เปลี่ยนเป็นพลังงานรูปอื่น",
                    "พลังงานที่ได้ทั้งหมดมากกว่าพลังงานที่ป้อนเข้าไป",
                    "กฎการอนุรักษ์พลังงานใช้ไม่ได้กับอุปกรณ์ที่มีการสูญเสียพลังงาน"),
            hint=CONSERVE_HINT, topic=ENERGY_CONSERVATION_TOPIC,
        )


@question_type(
    "phys.energy_conservation_fluency",
    display_name={"th": "อธิบายการเปลี่ยนและถ่ายโอนพลังงานโดยใช้กฎการอนุรักษ์พลังงาน"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=ENERGY_CONSERVATION_TOPIC,
)
class EnergyConservationFluency(QuestionType):
    """A device's energy input split into two outputs; the total stays conserved."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item, k = _scaled(rng)
        total, v1, v2 = item.total * k, item.value1 * k, item.value2 * k
        return _labelled(
            stem=(f"{item.device}เปลี่ยนพลังงานที่ป้อนเข้า {total} จูล เป็น{item.output1} {v1} จูล "
                  f"และ{item.output2} {v2} จูล จากข้อมูลนี้ ข้อใดอธิบายตามกฎการอนุรักษ์พลังงานได้ถูกต้อง"),
            correct=(f"{item.output1} {v1} จูล และ{item.output2} {v2} จูล "
                     f"รวม {total} จูล เท่ากับพลังงานที่ป้อนเข้า"),
            wrongs=(f"{item.output1} {v1} จูล เกิดขึ้นจริง แต่{item.output2} {v2} จูล "
                    "สูญหายจากระบบโดยไม่เปลี่ยนรูป",
                    f"{item.output1} {v1} จูล และ{item.output2} {v2} จูล "
                    "รวมกันมากกว่าพลังงานที่ป้อนเข้า",
                    f"เมื่อได้{item.output1}และ{item.output2}พร้อมกัน "
                    "กฎการอนุรักษ์พลังงานใช้กับอุปกรณ์นี้ไม่ได้"),
            hint="รวมพลังงานที่ได้ทุกรูปแบบ แล้วเทียบกับพลังงานที่ป้อนเข้า ผลรวมต้องเท่ากันเสมอ",
            topic=ENERGY_CONSERVATION_TOPIC,
        )


@question_type(
    "phys.energy_conservation_application",
    display_name={"th": "ใช้กฎการอนุรักษ์พลังงานอธิบายการสูญเสียและถ่ายโอนพลังงานจริง"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=ENERGY_CONSERVATION_TOPIC,
)
class EnergyConservationApplication(QuestionType):
    """Authored scenes, the missing share of an output, and efficiency."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            return _retopic(scenario_question(
                rng, ENERGY_CONSERVATION_SCENARIOS,
                hint="พลังงานที่ดูเหมือนหายไปมักเปลี่ยนเป็นความร้อนหรือรูปอื่นที่ตรวจจับได้ยาก ไม่ได้สูญหายไปจริง",
            ), ENERGY_CONSERVATION_TOPIC)
        item, k = _scaled(rng)
        total, v1, v2 = item.total * k, item.value1 * k, item.value2 * k
        if roll < 0.6:
            return numeric(stem=f"{item.device}ได้รับพลังงาน {show(total)} จูล เปลี่ยนเป็น{item.output1} {show(v1)} จูล ส่วนที่เหลือเป็น{item.output2} "
                                f"พลังงานส่วนนี้มีกี่จูล", answer=v2, wrongs=[total + v1, v1, Fraction(total, 2) if v2 * 2 != total else total],
                           unit="จูล", topic=ENERGY_CONSERVATION_TOPIC, hint=CONSERVE_HINT + " ส่วนที่เหลือ = พลังงานที่ได้รับ − พลังงานที่ได้ออกมาส่วนแรก")
        return numeric(stem=f"{item.device}ได้รับพลังงาน {show(total)} จูล ได้{item.output1}ที่ใช้ประโยชน์ {show(v1)} จูล ประสิทธิภาพเป็นร้อยละเท่าใด "
                            f"(ประสิทธิภาพ = พลังงานที่ใช้ประโยชน์ ÷ พลังงานที่ได้รับ × 100)", answer=item.value1,
                       wrongs=[item.value2, v1, 100 - item.value1 + 5], unit="%", topic=ENERGY_CONSERVATION_TOPIC,
                       hint="ประสิทธิภาพ = พลังงานที่ใช้ประโยชน์ ÷ พลังงานที่ได้รับ × 100")

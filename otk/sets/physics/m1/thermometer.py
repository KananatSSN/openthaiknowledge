"""การใช้เทอร์มอมิเตอร์วัดอุณหภูมิของสสาร

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/2

Sets moved here from: science_wave_d28.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import (
    THERMOMETERS,
    diagram_question,
    thermometer_alt,
    thermometer_wrongs,
)
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


THERMOMETER_TOPIC = "การใช้เทอร์มอมิเตอร์วัดอุณหภูมิของสสาร"


THERMO_FACTS = (
    ("เทอร์มอมิเตอร์แบบของเหลวในหลอดแก้ว (เช่น ปรอทหรือแอลกอฮอล์) วัดอุณหภูมิโดยอาศัยหลักการใด",
     "การขยายตัวหรือหดตัวของของเหลวในหลอดแก้วเมื่ออุณหภูมิเปลี่ยนแปลง",
     ("การเปลี่ยนสีของของเหลวเมื่ออุณหภูมิเปลี่ยนแปลง", "การระเหยของของเหลวออกจากหลอดแก้ว เมื่ออุณหภูมิเปลี่ยนแปลงไป", "การเปลี่ยนน้ำหนักของของเหลวในหลอดแก้ว",
      "การเปลี่ยนน้ำหนักของของเหลวในหลอดแก้วเมื่อได้รับความร้อน", "การขยายตัวของหลอดแก้วเมื่ออุณหภูมิสูงขึ้น ทำให้ของเหลวดูต่ำลง")),
    ("การอ่านค่าเทอร์มอมิเตอร์ที่ถูกต้องควรทำอย่างไร", "ให้สายตาอยู่ระดับเดียวกับระดับของเหลว และอ่านเมื่อระดับของเหลวคงที่แล้ว",
     ("มองจากด้านบนเฉียงลงมา", "อ่านทันทีที่จุ่มลงในสาร", "ยกกระเปาะขึ้นจากสารก่อนอ่าน", "มองจากด้านบนเฉียงลงมาที่ขีดสเกล และอ่านทันทีที่จุ่มกระเปาะลงในสาร", "ยกกระเปาะขึ้นจากสารก่อนอ่าน เพื่อให้มองเห็นระดับของเหลวได้ชัดเจนขึ้น")),
    ("เหตุใดจึงไม่ควรจับที่กระเปาะของเทอร์มอมิเตอร์ขณะวัดอุณหภูมิน้ำ", "ความร้อนจากมือจะทำให้ค่าที่อ่านได้คลาดเคลื่อน",
     ("กระเปาะจะแตกทันทีเมื่อจับ", "ความเย็นจากมือทำให้ของเหลวในหลอดหดตัวลง", "เทอร์มอมิเตอร์จะหยุดทำงาน", "ของเหลวในหลอดจะเปลี่ยนสี", "กระเปาะจะนำความร้อนออกจากมือจนมือเย็นลง")),
    ("น้ำบริสุทธิ์ที่ความดันปกติเดือดและแข็งตัวที่อุณหภูมิเท่าใด", "เดือดที่ 100 °C และแข็งตัวที่ 0 °C",
     ("เดือดที่ 0 °C และแข็งตัวที่ 100 °C", "เดือดที่ 50 °C และแข็งตัวที่ −50 °C", "เดือดที่ 212 °C และแข็งตัวที่ 32 °C", "เดือดที่ 100 °C และแข็งตัวที่ 10 °C", "เดือดที่ 90 °C และแข็งตัวที่ 0 °C")),
)


THERMO_HINT = "เทอร์มอมิเตอร์อาศัยการขยายตัวของของเหลว อ่านค่าเมื่อคงที่ สายตาอยู่ระดับเดียวกับของเหลว และเลือกช่วงสเกลให้ครอบคลุมอุณหภูมิที่วัด"


THERMOMETER_SCENARIOS = (
    ("เทอร์มอมิเตอร์วัดไข้ทางปากมีช่วงสเกลแคบและละเอียดกว่าเทอร์มอมิเตอร์วัดอุณหภูมิอากาศ เหตุใดจึงออกแบบต่างกัน",
     "อุณหภูมิร่างกายมนุษย์อยู่ในช่วงแคบและต้องอ่านค่าละเอียด จึงออกแบบสเกลให้เหมาะกับช่วงและความละเอียดที่ต้องการ",
     ("เทอร์มอมิเตอร์ทุกชนิดควรมีสเกลแบบเดียวกัน เพื่อให้อ่านค่าได้เหมือนกันทุกครั้งที่ใช้วัด", "เทอร์มอมิเตอร์วัดไข้ไม่จำเป็นต้องมีความละเอียดใด ๆ", "เทอร์มอมิเตอร์วัดไข้ต้องวัดได้ทุกอุณหภูมิ จึงออกแบบสเกลให้กว้างที่สุดเท่าที่ทำได้")),
    ("ก่อนใช้เทอร์มอมิเตอร์วัดอุณหภูมิ นักเรียนควรตรวจสอบสิ่งใดก่อนเพื่อให้ได้ค่าที่ถูกต้อง",
     "ตรวจสอบว่าเทอร์มอมิเตอร์ไม่มีของเหลวขาดตอนในหลอดแก้ว และรอให้ค่าคงที่ก่อนอ่าน",
     ("ไม่ต้องตรวจสอบใด ๆ เพราะเทอร์มอมิเตอร์อ่านค่าได้ถูกต้องเสมอ", "เขย่าเทอร์มอมิเตอร์แรง ๆ ก่อนใช้งานทุกครั้ง เพื่อให้ของเหลวในหลอดขยายตัว", "อ่านค่าทันทีที่สัมผัสกับสารโดยไม่ต้องรอ เพราะของเหลวขยายตัวได้ทันที")),
    ("เหตุใดจึงไม่ควรใช้เทอร์มอมิเตอร์วัดไข้ (ช่วง 35-42 องศาเซลเซียส) ไปวัดอุณหภูมิน้ำเดือด",
     "อุณหภูมิน้ำเดือดสูงเกินช่วงสเกลของเทอร์มอมิเตอร์วัดไข้ อาจทำให้เทอร์มอมิเตอร์เสียหายและอ่านค่าไม่ได้",
     ("เทอร์มอมิเตอร์วัดไข้วัดอุณหภูมิสูงได้ดีกว่าชนิดอื่นเสมอ", "อุณหภูมิน้ำเดือดต่ำกว่าช่วงสเกลของเทอร์มอมิเตอร์วัดไข้เสมอ", "เทอร์มอมิเตอร์วัดไข้ละเอียดกว่า จึงวัดอุณหภูมิน้ำเดือดได้แม่นยำกว่าชนิดที่ใช้ในห้องปฏิบัติการ")),
)


THERMO_RANGES = (("เทอร์มอมิเตอร์วัดไข้", 35, 42), ("เทอร์มอมิเตอร์วัดอากาศ", -10, 50), ("เทอร์มอมิเตอร์ห้องปฏิบัติการ", -10, 110),
                 ("เทอร์มอมิเตอร์ตู้แช่แข็ง", -40, 10))


@question_type(
    "phys.thermometer_foundation",
    display_name={"th": "บอกหลักการทำงานของเทอร์มอมิเตอร์"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMOMETER_TOPIC,
)
class ThermometerFoundation(QuestionType):
    """How the liquid thermometer works and how to read it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(THERMO_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=THERMO_HINT, topic=THERMOMETER_TOPIC)


@question_type(
    "phys.thermometer_fluency",
    display_name={"th": "อ่านค่าอุณหภูมิจากสเกลเทอร์มอมิเตอร์"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMOMETER_TOPIC,
)
class ThermometerFluency(QuestionType):
    """Reading a drawn thermometer; every draw shows one (see ``test_ms1_diagrams``).

    The drawn scale's division is not always one degree — a learner who counts
    divisions instead of reading them gets a scale of twos or fives wrong, so
    that mistake is offered whenever it is far enough from the answer to see.
    No two choices are closer than ``min_option_gap`` on the drawing: one
    division is only about five pixels on the dense scales.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(THERMOMETERS)
        wrongs = tuple(f"{value} องศาเซลเซียส" for value in thermometer_wrongs(spec))
        return diagram_question(
            spec.asset_id, thermometer_alt(spec),
            stem="จากภาพ เทอร์มอมิเตอร์อ่านค่าอุณหภูมิได้เท่าใด",
            correct=f"{spec.reading} องศาเซลเซียส",
            wrongs=tuple(wrongs),
            hint=("ดูก่อนว่าขีดเล็กหนึ่งขีดมีค่ากี่องศา แล้วจึงนับจากตัวเลขที่กำกับไว้ "
                  "ขึ้นไปจนถึงระดับของเหลว"),
            topic=THERMOMETER_TOPIC,
        )


@question_type(
    "phys.thermometer_application",
    display_name={"th": "เลือกใช้เทอร์มอมิเตอร์ให้เหมาะกับสถานการณ์"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMOMETER_TOPIC,
)
class ThermometerApplication(QuestionType):
    """Authored cases, and picking the thermometer whose range fits the task."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, THERMOMETER_SCENARIOS, hint=THERMO_HINT), THERMOMETER_TOPIC)
        task = rng.choice(("ของเหลวชนิดหนึ่ง", "สารตัวอย่าง ก", "สารตัวอย่าง ข", "สารในหลอดทดลอง", "สารละลายในบีกเกอร์"))
        temp = rng.randint(-40, 110)
        fits = sorted((hi - lo, n) for n, lo, hi in THERMO_RANGES if lo <= temp <= hi)
        fits = [fits[0][1]]
        right = fits[0]
        options = " ".join(f"{n} ({lo} ถึง {hi} °C)" for n, lo, hi in THERMO_RANGES)
        return _labelled(stem=f"ต้องการวัดอุณหภูมิ{task}ที่คาดว่าประมาณ {temp} °C มีเทอร์มอมิเตอร์ให้เลือก: {options} "
                              f"ควรใช้ชนิดใดที่ช่วงสเกลครอบคลุมและละเอียดที่สุด (ช่วงแคบที่สุดที่ยังครอบคลุม)",
                         correct=right, wrongs=tuple(n for n, _, _ in THERMO_RANGES if n != right), hint=THERMO_HINT, topic=THERMOMETER_TOPIC)

"""การทำงานของชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/6

Sets moved here from: science_wave_d33.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d32 import THIRD_SECONDARY

PROVENANCE = Provenance("original")


ELECTRONIC_COMPONENT_TOPIC = "การทำงานของชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย"


COMPONENT_HINT = ("ตัวต้านทานจำกัดกระแส ไดโอดให้ไหลทางเดียว LED เปล่งแสง ตัวเก็บประจุเก็บและปล่อยประจุ ทรานซิสเตอร์ขยายสัญญาณหรือเป็นสวิตช์ "
                  "ตัวต้านทานไวแสงเปลี่ยนความต้านทานตามแสง ตัวต้านทานปรับค่าได้ใช้ปรับกระแส")


class Component(NamedTuple):
    name: str
    evidence: str
    function: str


COMPONENTS = (
    Component("ตัวต้านทาน (resistor)",
              "เมื่อต่อในวงจร หลอดไฟสว่างน้อยลงเมื่อเปลี่ยนไปใช้ตัวต้านทานที่มีค่ามากขึ้น",
              "จำกัดปริมาณกระแสไฟฟ้าที่ไหลในวงจร"),
    Component("ไดโอด (diode)",
              "เมื่อต่อขั้วไดโอดให้ถูกทิศ หลอดไฟสว่าง แต่เมื่อสลับขั้วไดโอด หลอดไฟไม่สว่างเลย",
              "ยอมให้กระแสไฟฟ้าไหลผ่านได้ทิศทางเดียวเท่านั้น"),
    Component("หลอด LED",
              "เมื่อมีกระแสไฟฟ้าไหลผ่านในทิศทางที่ถูกต้อง หลอดเปล่งแสงออกมาโดยไม่ร้อนจัดเท่าหลอดไส้",
              "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานแสงโดยตรงอย่างมีประสิทธิภาพ"),
    Component("ตัวเก็บประจุ (capacitor)",
              "เมื่อตัดแหล่งกำเนิดไฟฟ้าออกจากวงจร หลอดไฟยังสว่างต่ออีกช่วงสั้น ๆ ก่อนดับ",
              "เก็บสะสมประจุไฟฟ้าไว้ชั่วคราวและปลดปล่อยออกมาเมื่อจำเป็น"),
    Component("ทรานซิสเตอร์ (transistor)",
              "กระแสไฟฟ้าเล็กน้อยที่ขาเบสทำให้กระแสไฟฟ้าผ่านขาคอลเลกเตอร์มากขึ้นจนมอเตอร์หมุนได้",
              "ขยายสัญญาณไฟฟ้าหรือทำหน้าที่เป็นสวิตช์เปิดปิดวงจร"),
    Component("ตัวต้านทานไวแสง (LDR)",
              "เมื่อใช้มือบังแสง หลอดไฟในวงจรสว่างน้อยลง เมื่อเอามือออกให้แสงส่อง หลอดไฟสว่างขึ้น",
              "เปลี่ยนความต้านทานตามปริมาณแสง ยิ่งแสงมากยิ่งมีความต้านทานน้อย"),
    Component("ตัวต้านทานปรับค่าได้ (variable resistor)",
              "เมื่อหมุนแกนของชิ้นส่วนไปทางหนึ่ง หลอดไฟค่อย ๆ สว่างขึ้น หมุนกลับหลอดไฟค่อย ๆ หรี่ลง",
              "ปรับค่าความต้านทานเพื่อเพิ่มหรือลดกระแสไฟฟ้าในวงจร"),
)


ELECTRONIC_COMPONENT_SCENARIOS = (
    ("เหตุใดวงจรอิเล็กทรอนิกส์หลายชนิดจึงต่อไดโอดไว้ที่ทางเข้าของแหล่งจ่ายไฟ",
     "เพื่อป้องกันความเสียหายหากมีการต่อขั้วแบตเตอรี่ผิด เพราะไดโอดยอมให้กระแสไหลทิศทางเดียว",
     ("เพื่อเพิ่มความสว่างให้กับวงจรโดยรวม", "เพื่อให้กระแสไฟฟ้าไหลได้ทั้งสองทิศทางเท่า ๆ กัน", "ไดโอดไม่มีผลต่อการป้องกันวงจรเลย")),
    ("เหตุใดไฟ LED จึงประหยัดพลังงานกว่าหลอดไส้ทั่วไปเมื่อให้ความสว่างเท่ากัน",
     "LED เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานแสงโดยตรงอย่างมีประสิทธิภาพ สูญเสียเป็นความร้อนน้อยกว่าหลอดไส้",
     ("LED เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานความร้อนเป็นหลัก", "หลอดไส้ใช้พลังงานน้อยกว่า LED เสมอ", "ชนิดของหลอดไฟไม่มีผลต่อปริมาณพลังงานที่ใช้")),
    ("แหล่งจ่ายไฟบางชนิดมีตัวเก็บประจุขนาดใหญ่ต่ออยู่ เหตุใดไฟจึงไม่ดับทันทีเมื่อตัดสวิตช์",
     "ตัวเก็บประจุที่เก็บประจุไฟฟ้าไว้ยังปลดปล่อยพลังงานออกมาต่ออีกช่วงสั้น ๆ",
     ("ตัวเก็บประจุสร้างพลังงานไฟฟ้าขึ้นมาใหม่เมื่อตัดสวิตช์", "การตัดสวิตช์ไม่มีผลต่อวงจรที่มีตัวเก็บประจุ", "ตัวเก็บประจุทำให้ไฟดับเร็วขึ้นกว่าปกติ")),
)


JOBS = (
    ("ไฟทางเดินที่ติดเองอัตโนมัติเมื่อฟ้ามืด", "ตัวต้านทานไวแสง (LDR)"),
    ("ปุ่มหมุนปรับความดังของวิทยุ", "ตัวต้านทานปรับค่าได้ (variable resistor)"),
    ("วงจรป้องกันความเสียหายเมื่อใส่ถ่านกลับขั้ว", "ไดโอด (diode)"),
    ("ไฟแสดงสถานะเปิดเครื่องบนเครื่องใช้ไฟฟ้า", "หลอด LED"),
    ("แฟลชกล้องถ่ายรูปที่ต้องปล่อยพลังงานออกมาในทันที", "ตัวเก็บประจุ (capacitor)"),
    ("วงจรขยายเสียงจากไมโครโฟนให้ดังออกลำโพง", "ทรานซิสเตอร์ (transistor)"),
    ("ชิ้นส่วนที่ต่อกับ LED เพื่อไม่ให้กระแสมากจน LED เสีย", "ตัวต้านทาน (resistor)"),
    ("ไฟหรี่ในห้องนอนที่ปรับความสว่างได้", "ตัวต้านทานปรับค่าได้ (variable resistor)"),
)


@question_type(
    "elec.electronic_component_foundation",
    display_name={"th": "ระบุชิ้นส่วนอิเล็กทรอนิกส์จากหน้าที่"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_COMPONENT_TOPIC,
)
class ElectronicComponentFoundation(QuestionType):
    """One function; which component performs it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(COMPONENTS))
        part = COMPONENTS[index]
        others = [c.name for i, c in enumerate(COMPONENTS) if i != index]
        return _labelled(
            stem=f"ชิ้นส่วนอิเล็กทรอนิกส์ใดทำหน้าที่{part.function}",
            correct=part.name,
            wrongs=tuple(others),
            hint=COMPONENT_HINT,
            topic=ELECTRONIC_COMPONENT_TOPIC,
        )


@question_type(
    "elec.electronic_component_fluency",
    display_name={"th": "บรรยายการทำงานของชิ้นส่วนอิเล็กทรอนิกส์จากข้อมูลที่รวบรวมได้"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_COMPONENT_TOPIC,
)
class ElectronicComponentFluency(QuestionType):
    """An observation of one component in a circuit; the function it demonstrates."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(COMPONENTS))
        part = COMPONENTS[index]
        others = [c.function for i, c in enumerate(COMPONENTS) if i != index]
        return _labelled(
            stem=f"{part.evidence} จากข้อมูลนี้ {part.name}ทำหน้าที่ใด",
            correct=part.function,
            wrongs=tuple(others),
            hint="ดูว่าการเปลี่ยนแปลงที่สังเกตได้เกี่ยวข้องกับกระแส ทิศทาง แสง การเก็บพลังงาน หรือการขยายสัญญาณ",
            topic=ELECTRONIC_COMPONENT_TOPIC,
        )


@question_type(
    "elec.electronic_component_application",
    display_name={"th": "ใช้ความรู้เรื่องชิ้นส่วนอิเล็กทรอนิกส์อธิบายอุปกรณ์จริง"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_COMPONENT_TOPIC,
)
class ElectronicComponentApplication(QuestionType):
    """Authored cases, and the component a real device needs for its job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, ELECTRONIC_COMPONENT_SCENARIOS, hint=COMPONENT_HINT), ELECTRONIC_COMPONENT_TOPIC)
        job, right = rng.choice(JOBS)
        others = [c.name for c in COMPONENTS if c.name != right]
        return _labelled(stem=f"ถ้าต้องการสร้าง{job} ควรเลือกใช้ชิ้นส่วนอิเล็กทรอนิกส์ใดเป็นหลัก", correct=right, wrongs=tuple(others),
                         hint=COMPONENT_HINT, topic=ELECTRONIC_COMPONENT_TOPIC)

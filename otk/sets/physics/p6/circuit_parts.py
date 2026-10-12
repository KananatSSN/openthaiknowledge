"""ส่วนประกอบและหน้าที่ของวงจรไฟฟ้าอย่างง่าย

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/1

Sets moved here from: science_wave_d26.
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
from otk.sets._support.science_wave_d26 import SIXTH

PROVENANCE = Provenance("original")


CIRCUIT_PARTS_TOPIC = "ส่วนประกอบและหน้าที่ของวงจรไฟฟ้าอย่างง่าย"


class Component(NamedTuple):
    name: str
    evidence: str
    function: str


COMPONENTS = (
    Component("เซลล์ไฟฟ้า", "เมื่อถอดเซลล์ไฟฟ้าออกจากวงจร หลอดไฟดับทันที แม้สายไฟและสวิตช์ยังต่ออยู่ครบ",
               "ให้พลังงานไฟฟ้าแก่วงจร"),
    Component("สายไฟ", "เมื่อตัดสายไฟเส้นหนึ่งในวงจร หลอดไฟดับทันที แม้เซลล์ไฟฟ้ายังอยู่ครบ",
               "เป็นตัวนำไฟฟ้าเชื่อมต่อส่วนประกอบต่าง ๆ เข้าด้วยกัน"),
    Component("หลอดไฟ", "เมื่อปิดวงจรโดยมีหลอดไฟต่ออยู่ หลอดไฟสว่างและรู้สึกอุ่นขึ้นเมื่อสัมผัสใกล้ ๆ",
               "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานแสงและความร้อน"),
    Component("สวิตช์", "เมื่อกดสวิตช์ปิดวงจร หลอดไฟสว่างทันที เมื่อกดสวิตช์เปิดวงจร หลอดไฟดับทันที",
               "ควบคุมการต่อและตัดวงจรไฟฟ้า"),
    Component("ออด (กริ่งไฟฟ้า)", "เมื่อต่อออดเข้าในวงจรที่ครบ ได้ยินเสียงดังออกมาตลอดเวลาที่วงจรครบ",
               "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานเสียง"),
    Component("มอเตอร์ของเล่น", "เมื่อต่อมอเตอร์เข้าในวงจรที่ครบ แกนมอเตอร์หมุนและใบพัดที่ติดอยู่หมุนตาม",
               "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกลทำให้เกิดการหมุน"),
)


CIRCUIT_HINT = "วงจรไฟฟ้าอย่างง่ายประกอบด้วยแหล่งพลังงาน (เซลล์ไฟฟ้า) สายไฟ เครื่องใช้ไฟฟ้า และสวิตช์ กระแสไหลได้เมื่อวงจรครบ"


CIRCUIT_PARTS_SCENARIOS = (
    ("ไฟฉายของนักเรียนไม่สว่างขึ้นเลย เมื่อตรวจสอบพบว่าสายไฟเส้นหนึ่งหลุดออกจากขั้วเซลล์ไฟฟ้า ข้อใดอธิบายได้ถูกต้อง",
     "สายไฟที่หลุดทำให้วงจรไม่ครบวงจร กระแสไฟฟ้าจึงไหลผ่านไม่ได้ หลอดไฟจึงไม่สว่าง",
     ("เซลล์ไฟฟ้าหมดพลังงานจึงไม่มีผลจากสายไฟที่หลุด", "หลอดไฟเสียจึงไม่สว่างไม่ว่าสายไฟจะต่ออยู่หรือไม่", "สวิตช์ต้องกดค้างไว้ตลอดเวลาจึงจะสว่าง")),
    ("นักเรียนเปลี่ยนเซลล์ไฟฟ้าเก่าที่หมดพลังงานเป็นเซลล์ไฟฟ้าใหม่ในไฟฉาย แล้วไฟฉายกลับมาสว่างได้ตามปกติ ข้อใดอธิบายได้ถูกต้อง",
     "เซลล์ไฟฟ้าเป็นแหล่งพลังงานไฟฟ้าของวงจร เมื่อเปลี่ยนเป็นเซลล์ใหม่ วงจรจึงมีพลังงานเพียงพอให้หลอดไฟสว่าง",
     ("สายไฟเป็นแหล่งพลังงานไฟฟ้าหลักของวงจร", "การเปลี่ยนเซลล์ไฟฟ้าไม่เกี่ยวกับความสว่างของหลอดไฟ", "หลอดไฟสร้างพลังงานไฟฟ้าขึ้นเองเมื่อเซลล์เก่าหมด")),
    ("สวิตช์ไฟในห้องเรียนอยู่ในตำแหน่ง \"ปิด\" (off) แต่หลอดไฟยังไม่สว่าง เหตุใดจึงเป็นเช่นนี้",
     "สวิตช์ตำแหน่ง \"ปิด\" หมายถึงตัดวงจร กระแสไฟฟ้าจึงไหลผ่านไม่ได้ หลอดไฟจึงไม่สว่างตามหน้าที่ของสวิตช์",
     ("สวิตช์ไม่มีหน้าที่เกี่ยวกับการต่อหรือตัดวงจรไฟฟ้า", "หลอดไฟควรสว่างเสมอไม่ว่าสวิตช์จะอยู่ตำแหน่งใด", "สวิตช์ตำแหน่ง \"ปิด\" หมายถึงต่อวงจรให้ครบเสมอ")),
)


CIRCUIT_CHECKS = (
    ("ต่อสายไฟจากขั้วบวกของถ่านไปที่หลอดไฟ และต่อจากหลอดไฟกลับไปที่ขั้วลบของถ่าน", True),
    ("ต่อสายไฟจากขั้วบวกของถ่านไปที่หลอดไฟเพียงเส้นเดียว ไม่มีสายกลับไปที่ขั้วลบ", False),
    ("ต่อสายไฟครบทุกเส้น แต่ใช้เชือกฟางแทนสายไฟหนึ่งเส้น", False),
    ("ต่อวงจรครบ และกดสวิตช์ไปที่ตำแหน่งเปิดไฟ (on)", True),
    ("ต่อวงจรครบ แต่สวิตช์อยู่ในตำแหน่งปิดไฟ (off)", False),
    ("ต่อสายไฟทั้งสองเส้นเข้าที่ขั้วบวกของถ่านเดียวกัน", False),
    ("ต่อสายไฟจากถ่านผ่านสวิตช์ที่เปิดอยู่ ผ่านออด แล้วกลับเข้าขั้วลบของถ่าน", True),
)


@question_type(
    "phys.circuit_parts_foundation",
    display_name={"th": "ระบุส่วนประกอบของวงจรไฟฟ้าอย่างง่ายจากหน้าที่"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_PARTS_TOPIC,
)
class CircuitPartsFoundation(QuestionType):
    """One function; which component performs it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(COMPONENTS))
        part = COMPONENTS[index]
        others = [c.name for i, c in enumerate(COMPONENTS) if i != index]
        return _labelled(
            stem=f"ส่วนประกอบใดของวงจรไฟฟ้าอย่างง่ายทำหน้าที่{part.function}",
            correct=part.name,
            wrongs=tuple(others),
            hint=CIRCUIT_HINT,
            topic=CIRCUIT_PARTS_TOPIC,
        )


@question_type(
    "phys.circuit_parts_fluency",
    display_name={"th": "บรรยายหน้าที่ของส่วนประกอบวงจรไฟฟ้าจากหลักฐานเชิงประจักษ์"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_PARTS_TOPIC,
)
class CircuitPartsFluency(QuestionType):
    """Removing or testing one part; the evidence for its function."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(COMPONENTS))
        part = COMPONENTS[index]
        others = [c.function for i, c in enumerate(COMPONENTS) if i != index]
        return _labelled(
            stem=f"{part.evidence} จากหลักฐานนี้ {part.name}ทำหน้าที่ใด",
            correct=part.function,
            wrongs=tuple(others),
            hint="ดูว่าการเปลี่ยนแปลงหรือถอดส่วนประกอบใดทำให้วงจรเปลี่ยนไปอย่างที่สังเกตได้",
            topic=CIRCUIT_PARTS_TOPIC,
        )


@question_type(
    "phys.circuit_parts_application",
    display_name={"th": "วินิจฉัยปัญหาวงจรไฟฟ้าจากหน้าที่ของส่วนประกอบ"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_PARTS_TOPIC,
)
class CircuitPartsApplication(QuestionType):
    """Authored faults, and whether a described circuit is complete."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, CIRCUIT_PARTS_SCENARIOS,
                hint="ตรวจสอบว่าส่วนประกอบใดขาดหรือเปลี่ยนไป แล้วเชื่อมโยงกับหน้าที่ของส่วนประกอบนั้น",
            ), CIRCUIT_PARTS_TOPIC)
        case, complete = rng.choice(CIRCUIT_CHECKS)
        kid = rng.choice(("ต้น", "ฝน", "มะลิ", "ภูมิ", "ข้าวหอม", "ปลา"))
        right = "วงจรครบ กระแสไฟฟ้าไหลได้ เครื่องใช้ไฟฟ้าจึงทำงาน" if complete else "วงจรไม่ครบ กระแสไฟฟ้าไหลไม่ได้ เครื่องใช้ไฟฟ้าจึงไม่ทำงาน"
        other = "วงจรไม่ครบ กระแสไฟฟ้าไหลไม่ได้ เครื่องใช้ไฟฟ้าจึงไม่ทำงาน" if complete else "วงจรครบ กระแสไฟฟ้าไหลได้ เครื่องใช้ไฟฟ้าจึงทำงาน"
        return _labelled(stem=f"{kid}{case} วงจรนี้เป็นอย่างไร", correct=right,
                         wrongs=(other, "เครื่องใช้ไฟฟ้าทำงานได้เสมอ ไม่ว่าวงจรจะครบหรือไม่", "ถ่านไฟฉายจะระเบิดทันที"),
                         hint=CIRCUIT_HINT, topic=CIRCUIT_PARTS_TOPIC)

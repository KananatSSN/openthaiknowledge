"""เยื่อหุ้มเซลล์และการลำเลียงสาร

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/1

Sets moved here from: science_wave_b19.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import MEMBRANE_SCENARIOS, UPPER_FOUR, Fact, _fact_question

PROVENANCE = Provenance("original")


CELL_TOPIC = "เซลล์และการลำเลียงสารผ่านเยื่อหุ้มเซลล์"


# Every answer names a structural feature and the transport consequence that
# follows from it, which is what "โครงสร้างและสมบัติ…ที่สัมพันธ์กับการลำเลียงสาร"
# asks for. An answer that stopped at the structure would not meet the indicator.
MEMBRANE_FACTS = (
    Fact("โครงสร้างพื้นฐานของเยื่อหุ้มเซลล์เป็นอย่างไร",
         "เป็นฟอสโฟลิพิดสองชั้น โดยหันส่วนหัวที่ชอบน้ำออกสู่ด้านนอกทั้งสองด้าน "
         "และหันส่วนหางที่ไม่ชอบน้ำเข้าหากันตรงกลาง"),
    Fact("เหตุใดแก๊สออกซิเจนและแก๊สคาร์บอนไดออกไซด์จึงผ่านเยื่อหุ้มเซลล์ได้เอง",
         "เป็นโมเลกุลขนาดเล็กและไม่มีขั้ว จึงละลายผ่านส่วนหางที่ไม่ชอบน้ำ"
         "ตรงกลางเยื่อได้โดยตรง"),
    Fact("เหตุใดไอออน เช่น โซเดียมไอออน จึงผ่านชั้นฟอสโฟลิพิดโดยตรงไม่ได้",
         "ไอออนมีประจุและมีน้ำล้อมรอบ จึงผ่านส่วนหางที่ไม่ชอบน้ำตรงกลางไม่ได้ "
         "ต้องอาศัยโปรตีนที่แทรกอยู่ในเยื่อเป็นทางผ่าน"),
    Fact("โปรตีนที่แทรกอยู่ในเยื่อหุ้มเซลล์เกี่ยวข้องกับการลำเลียงสารอย่างไร",
         "ทำหน้าที่เป็นช่องและเป็นตัวพาให้สารที่มีขั้วหรือมีประจุ เช่น กลูโคส"
         "และไอออน ผ่านเข้าออกเซลล์ได้"),
    Fact("การที่เยื่อหุ้มเซลล์เป็น “เยื่อเลือกผ่าน” หมายความว่าอย่างไร",
         "ยอมให้สารบางชนิดผ่านได้ดี บางชนิดผ่านได้ช้า และบางชนิดผ่านไม่ได้ "
         "โดยขึ้นกับขนาด ความมีขั้ว และประจุของสารนั้น"),
    Fact("คอเลสเทอรอลที่แทรกอยู่ในเยื่อหุ้มเซลล์สัตว์มีผลอย่างไร",
         "ช่วยรักษาความเป็นของไหลของเยื่อไว้ให้พอเหมาะเมื่ออุณหภูมิเปลี่ยนแปลง "
         "การลำเลียงสารผ่านเยื่อจึงยังเป็นไปตามปกติ"),
    Fact("คาร์โบไฮเดรตที่ยื่นออกมาจากผิวด้านนอกของเยื่อหุ้มเซลล์ทำหน้าที่ใด",
         "เป็นเครื่องหมายให้เซลล์อื่นและสารบางชนิดจำเซลล์นี้ได้ "
         "จึงเกี่ยวข้องกับการรับรู้ระหว่างเซลล์มากกว่าการเป็นทางผ่านของสาร"),
)


class Mode(NamedTuple):
    """One way of moving a substance across the membrane.

    ``gradient`` is empty for the vesicle modes: bulk transport does not move a
    substance along or against a concentration gradient at all, so those two are
    left out of the contrast form rather than given a made-up answer.
    """
    name: str
    description: str
    example: str
    energy: str
    gradient: str


MODES = (
    Mode("การแพร่",
         "สารเคลื่อนที่ผ่านชั้นฟอสโฟลิพิดเองจากบริเวณที่มีความเข้มข้นสูง"
         "ไปยังบริเวณที่มีความเข้มข้นต่ำ จนกระทั่งความเข้มข้นทั้งสองด้านเท่ากัน",
         "แก๊สออกซิเจนจากถุงลมเข้าสู่เลือด",
         "ไม่ใช้พลังงานจากเซลล์",
         "เคลื่อนที่ตามระดับความเข้มข้นเท่านั้น"),
    Mode("ออสโมซิส",
         "น้ำเคลื่อนที่ผ่านเยื่อเลือกผ่านจากบริเวณที่มีความเข้มข้นของตัวละลายต่ำ"
         "ไปยังบริเวณที่มีความเข้มข้นของตัวละลายสูงกว่า",
         "น้ำจากดินเข้าสู่เซลล์ขนราก",
         "ไม่ใช้พลังงานจากเซลล์",
         "เคลื่อนที่ตามระดับความเข้มข้นเท่านั้น"),
    Mode("การแพร่แบบฟาซิลิเทต",
         "สารเคลื่อนที่ตามระดับความเข้มข้นเช่นเดียวกับการแพร่ "
         "แต่ต้องผ่านโปรตีนที่เป็นช่องหรือเป็นตัวพาในเยื่อหุ้มเซลล์",
         "กลูโคสเข้าสู่เซลล์เม็ดเลือดแดง",
         "ไม่ใช้พลังงานจากเซลล์",
         "เคลื่อนที่ตามระดับความเข้มข้นเท่านั้น"),
    Mode("แอกทีฟทรานสปอร์ต",
         "โปรตีนตัวพาในเยื่อหุ้มเซลล์ใช้พลังงานลำเลียงสารจากบริเวณที่มีความเข้มข้นต่ำ"
         "ไปยังบริเวณที่มีความเข้มข้นสูงกว่า",
         "โซเดียม-โพแทสเซียมปั๊มที่เยื่อหุ้มเซลล์ประสาท",
         "ใช้พลังงานจาก ATP",
         "เคลื่อนที่ทวนระดับความเข้มข้นได้"),
    Mode("เอนโดไซโทซิส",
         "เยื่อหุ้มเซลล์เว้าเข้าไปโอบสารขนาดใหญ่จนกลายเป็นถุงอยู่ภายในเซลล์",
         "เซลล์เม็ดเลือดขาวกลืนกินแบคทีเรีย",
         "ใช้พลังงานจาก ATP",
         ""),
    Mode("เอกโซไซโทซิส",
         "ถุงที่บรรจุสารภายในเซลล์เคลื่อนไปรวมกับเยื่อหุ้มเซลล์ "
         "แล้วปล่อยสารขนาดใหญ่ออกสู่ภายนอก",
         "การหลั่งเอนไซม์ย่อยอาหารจากเซลล์ของตับอ่อน",
         "ใช้พลังงานจาก ATP",
         ""),
)


CONTRASTABLE = tuple(mode for mode in MODES if mode.gradient)


# การแพร่, ออสโมซิส and การแพร่แบบฟาซิลิเทต agree on both fields, so a contrast
# item built from any two of them would offer three choices that all say the same
# thing. Only pairs that actually differ somewhere are asked, and only on a field
# where they differ.
CONTRAST_PAIRS = tuple(
    (first, second, tuple(field for field in ("energy", "gradient")
                          if getattr(first, field) != getattr(second, field)))
    for index, first in enumerate(CONTRASTABLE)
    for second in CONTRASTABLE[index + 1:]
    if any(getattr(first, field) != getattr(second, field)
           for field in ("energy", "gradient"))
)


@question_type(
    "cell.membrane_structure_foundation",
    display_name={"th": "โครงสร้างและสมบัติของเยื่อหุ้มเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=CELL_TOPIC,
)
class MembraneStructureFoundation(QuestionType):
    """The membrane's structure, always tied to what it lets through."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, MEMBRANE_FACTS, topic=CELL_TOPIC,
            hint="ถามกลับว่าโครงสร้างส่วนนั้นอยู่ตรงไหนของเยื่อ "
                 "แล้วสารแบบใดจึงผ่านตรงนั้นได้หรือไม่ได้",
        )


@question_type(
    "cell.membrane_transport_fluency",
    display_name={"th": "เปรียบเทียบการลำเลียงสารผ่านเยื่อหุ้มเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=CELL_TOPIC,
)
class MembraneTransportFluency(QuestionType):
    """Tell the transport modes apart — the ``เปรียบเทียบ`` half of ``ม.4/1``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.35:
            item = rng.choice(MODES)
            others = [other.description for other in MODES
                      if other.name != item.name]
            rng.shuffle(others)
            return _labelled(
                stem=f"ข้อใดอธิบาย “{item.name}” ได้ถูกต้อง",
                correct=item.description, wrongs=tuple(others[:3]),
                hint="ดูสองอย่างเป็นหลัก คือใช้พลังงานหรือไม่ "
                     "และสารเคลื่อนที่ตามหรือทวนระดับความเข้มข้น",
                topic=CELL_TOPIC,
            )
        if draw < 0.7:
            item = rng.choice(MODES)
            others = [other.name for other in MODES if other.name != item.name]
            rng.shuffle(others)
            return _labelled(
                stem=f"“{item.example}” เป็นการลำเลียงสารผ่านเยื่อหุ้มเซลล์แบบใด",
                correct=item.name, wrongs=tuple(others[:3]),
                hint="ถามว่าสารนั้นใหญ่เกินกว่าจะผ่านโปรตีนหรือไม่ "
                     "และเคลื่อนไปทางที่ความเข้มข้นต่ำกว่าหรือสูงกว่า",
                topic=CELL_TOPIC,
            )
        first, second, fields = rng.choice(CONTRAST_PAIRS)
        if rng.random() < 0.5:
            first, second = second, first
        field = rng.choice(fields)
        one, two = getattr(first, field), getattr(second, field)
        return _labelled(
            stem=f"ข้อใดเปรียบเทียบ “{first.name}” กับ “{second.name}” "
                 f"ได้ถูกต้อง",
            correct=f"{first.name}{one} ส่วน{second.name}{two}",
            wrongs=(f"{first.name}{two} ส่วน{second.name}{one}",
                    f"ทั้ง{first.name}และ{second.name}ต่าง{one}",
                    f"ทั้ง{first.name}และ{second.name}ต่าง{two}"),
            hint="ตัดสินทีละแบบก่อนว่าแบบนั้นเป็นอย่างไร แล้วจึงนำมาเทียบกัน",
            topic=CELL_TOPIC,
        )


@question_type(
    "cell.membrane_transport_application",
    display_name={"th": "วิเคราะห์การลำเลียงสารผ่านเยื่อหุ้มเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=CELL_TOPIC,
)
class MembraneTransportApplication(QuestionType):
    """Decide which transport mode a described result implies, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MEMBRANE_SCENARIOS,
            hint="เทียบความเข้มข้นสองด้านก่อน แล้วจึงถามว่าต้องใช้โปรตีนหรือพลังงาน"
                 "หรือไม่",
        ), CELL_TOPIC)

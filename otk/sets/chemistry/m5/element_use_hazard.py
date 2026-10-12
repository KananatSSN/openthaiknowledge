"""ประโยชน์และอันตรายจากธาตุเรพรีเซนเททีฟและธาตุแทรนซิชัน

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/7

Sets moved here from: science_wave_e2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_a5 import REPRESENTATIVE, TRANSITION_BLOCK
from otk.sets._support.science_wave_e2 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_ELEMENT_USE = "ประโยชน์และอันตรายจากธาตุเรพรีเซนเททีฟและธาตุแทรนซิชัน"


class UseItem(NamedTuple):
    text: str
    block: str      # REPRESENTATIVE or TRANSITION_BLOCK
    kind: str        # "ประโยชน์" or "อันตราย"


BENEFIT, HAZARD = "ประโยชน์", "อันตราย"


USE_ITEMS: tuple[UseItem, ...] = (
    UseItem("โซเดียมและโพแทสเซียมเป็นส่วนประกอบสำคัญของปุ๋ยที่ช่วยให้พืชเจริญเติบโต",
            REPRESENTATIVE, BENEFIT),
    UseItem("ออกซิเจนเป็นแก๊สที่สิ่งมีชีวิตใช้ในการหายใจ",
            REPRESENTATIVE, BENEFIT),
    UseItem("สารประกอบฟลูออไรด์ในยาสีฟันช่วยป้องกันฟันผุ",
            REPRESENTATIVE, BENEFIT),
    UseItem("แก๊สคลอรีนที่รั่วไหลเป็นพิษต่อระบบทางเดินหายใจ",
            REPRESENTATIVE, HAZARD),
    UseItem("ฟอสฟอรัสขาวเป็นพิษและติดไฟได้ง่ายเมื่อสัมผัสอากาศ",
            REPRESENTATIVE, HAZARD),
    UseItem("เหล็กเป็นองค์ประกอบของฮีโมโกลบินที่ช่วยลำเลียงออกซิเจนในเลือด",
            TRANSITION_BLOCK, BENEFIT),
    UseItem("ทองแดงใช้ทำสายไฟฟ้าเพราะนำไฟฟ้าได้ดี",
            TRANSITION_BLOCK, BENEFIT),
    UseItem("ปรอทที่ปนเปื้อนในอาหารทะเลสะสมในร่างกายและเป็นพิษต่อระบบประสาท",
            TRANSITION_BLOCK, HAZARD),
    UseItem("แคดเมียมที่ปนเปื้อนในดินและน้ำเป็นพิษต่อไตของมนุษย์",
            TRANSITION_BLOCK, HAZARD),
    UseItem("แมกนีเซียมใช้ทำโลหะผสมน้ำหนักเบาสำหรับโครงจักรยานและเครื่องบิน",
            REPRESENTATIVE, BENEFIT),
    UseItem("ซิลิคอนใช้ผลิตชิปคอมพิวเตอร์และเซลล์สุริยะ",
            REPRESENTATIVE, BENEFIT),
    UseItem("ตะกั่วที่ปนอยู่ในสีทาบ้านเก่าเป็นพิษต่อระบบประสาทของเด็ก",
            REPRESENTATIVE, HAZARD),
    UseItem("โซเดียมโลหะทำปฏิกิริยารุนแรงกับน้ำจนลุกไหม้ได้",
            REPRESENTATIVE, HAZARD),
    UseItem("ไทเทเนียมใช้ทำข้อต่อกระดูกเทียมเพราะแข็งแรงและไม่เป็นสนิม",
            TRANSITION_BLOCK, BENEFIT),
    UseItem("สังกะสีใช้เคลือบแผ่นเหล็กเพื่อป้องกันสนิม",
            TRANSITION_BLOCK, BENEFIT),
    UseItem("โครเมียมบางรูปแบบในน้ำเสียจากโรงงานชุบโลหะเป็นสารก่อมะเร็ง",
            TRANSITION_BLOCK, HAZARD),
    UseItem("ฝุ่นแมงกานีสที่สูดดมเป็นเวลานานทำลายระบบประสาท",
            TRANSITION_BLOCK, HAZARD),
)


USE_CATEGORIES: tuple[tuple[str, str], ...] = tuple(sorted({
    (item.block, item.kind) for item in USE_ITEMS
}))


def _use_label(block: str, kind: str) -> str:
    return f"{kind}จาก{block}"


@question_type(
    "chem.element_use_hazard_foundation",
    display_name={"th": "ตัวอย่างนี้เกี่ยวข้องกับธาตุกลุ่มใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELEMENT_USE,
)
class ElementUseHazardFoundation(QuestionType):
    """Only the block half — not yet whether it is a benefit or a hazard."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(USE_ITEMS)
        other_block = TRANSITION_BLOCK if item.block == REPRESENTATIVE else REPRESENTATIVE
        return _labelled(
            stem=f"ตัวอย่างนี้เกี่ยวข้องกับธาตุกลุ่มใด: \"{item.text}\"",
            correct=item.block,
            wrongs=(other_block, "ธาตุกึ่งโลหะ", "ไม่เกี่ยวข้องกับกลุ่มธาตุใด",
                    "ธาตุที่มนุษย์สังเคราะห์ขึ้นในห้องปฏิบัติการ"),
            topic=TOPIC_ELEMENT_USE,
            hint="ธาตุเรพรีเซนเททีฟอยู่หมู่ 1-2 และ 13-18 ส่วนธาตุแทรนซิชันอยู่หมู่ 3-12",
        )


@question_type(
    "chem.element_use_hazard_fluency",
    display_name={"th": "ตัวอย่างนี้เป็นประโยชน์หรืออันตรายจากธาตุกลุ่มใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELEMENT_USE,
)
class ElementUseHazardFluency(QuestionType):
    """Both axes at once — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(USE_ITEMS)
        label = _use_label(item.block, item.kind)
        all_labels = [_use_label(block, kind) for block, kind in USE_CATEGORIES]
        wrongs = rng.sample([candidate for candidate in all_labels if candidate != label], 3)
        wrongs += ["ไม่เกี่ยวข้องกับธาตุกลุ่มใด", "เป็นทั้งประโยชน์และอันตรายจากธาตุกึ่งโลหะ"]
        return _labelled(
            stem=f"ตัวอย่างนี้เป็นประโยชน์หรืออันตรายจากธาตุกลุ่มใด: \"{item.text}\"",
            correct=label,
            wrongs=tuple(wrongs),
            topic=TOPIC_ELEMENT_USE,
            hint="ดูก่อนว่าธาตุที่กล่าวถึงอยู่กลุ่มเรพรีเซนเททีฟหรือแทรนซิชัน แล้วดูว่าข้อความเป็นผลดีหรือผลเสีย",
        )


@question_type(
    "chem.element_use_hazard_application",
    display_name={"th": "ตัวอย่างในข้อใดจัดอยู่ในหมวดที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ELEMENT_USE,
)
class ElementUseHazardApplication(QuestionType):
    """Reverse direction: given the category, pick the matching example."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        block, kind = rng.choice(USE_CATEGORIES)
        same = [item for item in USE_ITEMS if (item.block, item.kind) == (block, kind)]
        other = [item for item in USE_ITEMS if (item.block, item.kind) != (block, kind)]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        label = _use_label(block, kind)
        return _labelled(
            stem=f"ข้อใดต่อไปนี้เป็นตัวอย่าง{label}",
            correct=correct.text,
            wrongs=tuple(w.text for w in wrongs),
            topic=TOPIC_ELEMENT_USE,
            hint="ดูก่อนว่าธาตุที่กล่าวถึงอยู่กลุ่มเรพรีเซนเททีฟหรือแทรนซิชัน แล้วดูว่าข้อความเป็นผลดีหรือผลเสีย",
        )

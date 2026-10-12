"""วัสดุที่เกิดจากการผสมกัน

เคมี · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.2/2

Sets moved here from: science_wave_d2.
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
from otk.sets._support.science_wave_d1 import SECOND, SUBJECT

PROVENANCE = Provenance("original")


MIXING_TOPIC = "วัสดุที่เกิดจากการผสมกัน"


class Mix(NamedTuple):
    """Two materials, what each is like alone, and what the mixture is like."""
    first: str
    first_alone: str
    second: str
    second_alone: str
    after: str


MIXES = (
    Mix("แป้งข้าวเจ้า", "เป็นผงละเอียด ปั้นเป็นรูปร่างไม่ได้", "น้ำ", "เป็นของเหลว ไหลได้",
        "เหนียว ปั้นเป็นรูปร่างต่าง ๆ ได้"),
    Mix("ปูนซีเมนต์", "เป็นผงละเอียด ร่วนไม่เกาะกัน", "ทรายผสมน้ำ", "เม็ดทรายร่วน ไม่เกาะกันเป็นก้อน",
        "เมื่อแห้งแล้วแข็ง เกาะกันเป็นก้อน ทุบให้แตกได้ยาก"),
    Mix("กระดาษหนังสือพิมพ์", "บาง ฉีกขาดได้ง่าย", "กาวแป้งเปียก", "เหนียว ติดมือ",
        "เมื่อแห้งแล้วหนา แข็ง ฉีกขาดได้ยาก"),
    Mix("ดินเหนียว", "เมื่อแห้งแล้วแตกร้าวง่าย", "ฟางข้าว", "เป็นเส้นยาว เบา",
        "เมื่อแห้งแล้วเป็นก้อนที่แข็งแรง แตกร้าวน้อยลง"),
    Mix("ทรายแห้ง", "เม็ดร่วน ก่อเป็นรูปทรงไม่ได้", "น้ำเล็กน้อย", "เป็นของเหลว ไหลได้",
        "เม็ดทรายเกาะกัน ก่อเป็นรูปทรงได้"),
)


def _mixed(mix: Mix, after: str) -> str:
    return f"วัสดุที่ได้{after} ซึ่งต่างจาก{mix.first}ที่{mix.first_alone}"


MIXED_MADE = ("ปูนฉาบผนังบ้าน", "แป้งโดว์สำหรับปั้น", "อิฐดินเหนียวผสมแกลบ", "กระปุกกระดาษปาปิเยมาเช่")


NOT_MIXED = ("ก้อนหินในลำธาร", "ท่อนไม้ที่ตัดจากต้น", "เปลือกหอยจากชายหาด", "ขนนกที่หลุดจากปีก", "ใบไม้แห้งใต้ต้นไม้")


MIXING_SCENARIOS = (
    ("ชาวบ้านบางแห่งผสมฟางข้าวลงในดินเหนียวก่อนนำไปทำอิฐ ข้อใดเป็นเหตุผลที่ดีที่สุด",
     "ฟางช่วยให้ก้อนดินเมื่อแห้งแล้วแข็งแรงและแตกร้าวน้อยกว่าดินเหนียวอย่างเดียว",
     ("ฟางทำให้ก้อนดินนุ่มจนพับได้",
      "ฟางทำให้ดินเหนียวใสมองผ่านได้",
      "ฟางทำให้ดินเหนียวละลายน้ำได้ดีขึ้น",
      "ฟางทำให้ดินเหนียวมีกลิ่นหอม",
      "ฟางทำให้ก้อนดินยืดและหดกลับได้")),
    ("นักเรียนสร้างปราสาททรายด้วยทรายแห้ง แต่ทรายร่วนก่อเป็นรูปทรงไม่ได้ นักเรียนควรทำอย่างไร",
     "ผสมน้ำลงในทรายเล็กน้อย เพื่อให้เม็ดทรายเกาะกันและก่อเป็นรูปทรงได้",
     ("ใช้ทรายแห้งมากขึ้นเป็นสองเท่า",
      "ผสมน้ำลงไปจนทรายกลายเป็นน้ำโคลนที่ไหลได้",
      "นำทรายไปตากแดดให้แห้งกว่าเดิม",
      "ผสมน้ำตาลลงในทรายแห้ง",
      "เป่าลมใส่ทรายให้เม็ดทรายแยกจากกัน")),
    ("นักเรียนผสมแป้งกับน้ำในถ้วยสองใบ ใบแรกใส่น้ำพอเหมาะ ได้แป้งที่ปั้นได้ ใบที่สองใส่น้ำมากเกินไป ได้แป้งเหลวที่ปั้นไม่ได้ หลักฐานนี้บอกอะไร",
     "สมบัติของวัสดุผสมขึ้นอยู่กับปริมาณของวัสดุที่นำมาผสมกันด้วย",
     ("แป้งกับน้ำผสมกันไม่ได้",
      "น้ำยิ่งมากแป้งยิ่งปั้นได้ง่าย",
      "วัสดุผสมมีสมบัติเหมือนน้ำเสมอ",
      "แป้งกลายเป็นน้ำเมื่อผสม",
      "ปริมาณน้ำไม่มีผลต่อแป้งที่ได้")),
    ("ช่างผสมปูนซีเมนต์กับทรายและน้ำเพื่อก่ออิฐ เมื่อแห้งแล้วอิฐติดกันแน่น ข้อใดอธิบายได้ถูกต้อง",
     "วัสดุที่ได้จากการผสมเมื่อแห้งแล้วแข็งและยึดอิฐไว้ด้วยกัน ต่างจากผงปูนและทรายที่ร่วนก่อนผสม",
     ("ปูนซีเมนต์ผสมแล้วยังร่วนเหมือนเดิม",
      "ทรายทำให้อิฐนุ่มลง",
      "น้ำทำให้อิฐละลายติดกัน",
      "ปูนผสมแล้วใสมองผ่านได้",
      "อิฐติดกันเพราะอิฐเปียกเท่านั้น")),
    ("นักเรียนทำกระปุกออมสินจากกระดาษหนังสือพิมพ์ชุบกาวแป้งเปียกทับกันหลายชั้น เมื่อแห้งแล้วกระปุกแข็ง ข้อใดเป็นเหตุผลที่ดีที่สุด",
     "กระดาษที่ผสมกับกาวหลายชั้นเมื่อแห้งแล้วหนาและแข็งกว่ากระดาษแผ่นเดียว",
     ("กระดาษหนังสือพิมพ์แข็งอยู่แล้วตั้งแต่ก่อนผสม",
      "กาวแป้งเปียกทำให้กระดาษใสมองผ่านได้",
      "กาวทำให้กระดาษยืดและหดกลับได้",
      "กระดาษกลายเป็นโลหะเมื่อแห้ง",
      "กาวละลายกระดาษจนหายไป")),
)


@question_type(
    "chem.mixed_material_foundation",
    display_name={"th": "ระบุวัสดุที่เกิดจากการนำวัสดุมาผสมกัน"},
    level=SECOND, subject=SUBJECT, topic=MIXING_TOPIC,
)
class MixedMaterialFoundation(QuestionType):
    """Which of four things was made by mixing materials together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _labelled(
            stem="สิ่งใดทำจากวัสดุที่เกิดจากการนำวัสดุหลายชนิดมาผสมกัน",
            correct=rng.choice(MIXED_MADE),
            wrongs=tuple(NOT_MIXED),
            hint="สิ่งที่พบได้ตามธรรมชาติมักเป็นวัสดุชนิดเดียว ส่วนวัสดุผสมต้องมีคนนำวัสดุมาผสมกัน",
            topic=MIXING_TOPIC,
        )


@question_type(
    "chem.mixed_material_fluency",
    display_name={"th": "อธิบายสมบัติของวัสดุผสมจากหลักฐานการสังเกต"},
    level=SECOND, subject=SUBJECT, topic=MIXING_TOPIC,
)
class MixedMaterialFluency(QuestionType):
    """A before-and-after record; explain how the mixture differs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(MIXES))
        mix = MIXES[index]
        others = [other for i, other in enumerate(MIXES) if i != index]
        return _labelled(
            stem=(f"นักเรียนบันทึกผลการสังเกตได้ว่า ก่อนผสม {mix.first}{mix.first_alone} และ{mix.second}"
                  f"{mix.second_alone} เมื่อนำมาผสมกัน วัสดุที่ได้{mix.after} "
                  "จากหลักฐานนี้ ข้อใดอธิบายสมบัติของวัสดุที่ได้จากการผสมได้ถูกต้อง"),
            correct=_mixed(mix, mix.after),
            wrongs=(f"วัสดุที่ได้{mix.first_alone} เหมือน{mix.first}ก่อนผสมทุกอย่าง",
                    *(_mixed(mix, other.after) for other in others),
                    f"วัสดุที่ได้{mix.second_alone} เหมือน{mix.second}ก่อนผสมทุกอย่าง"),
            hint="เทียบสิ่งที่สังเกตได้หลังผสม กับสมบัติของวัสดุแต่ละชนิดก่อนผสม",
            topic=MIXING_TOPIC,
        )


@question_type(
    "chem.mixed_material_application",
    display_name={"th": "ใช้ความรู้เรื่องวัสดุผสมแก้ปัญหา"},
    level=SECOND, subject=SUBJECT, topic=MIXING_TOPIC,
)
class MixedMaterialApplication(QuestionType):
    """Straw in clay bricks, a sandcastle, and how much water to mix."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MIXING_SCENARIOS,
            hint="นึกว่าวัสดุผสมมีสมบัติต่างจากวัสดุเดิมอย่างไร และอะไรทำให้สมบัตินั้นเปลี่ยน",
        ), MIXING_TOPIC)

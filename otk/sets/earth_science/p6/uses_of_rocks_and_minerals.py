"""ประโยชน์ของหินและแร่

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/2

Sets moved here from: geology, science_wave_c14.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geology import SUBJECT, TOPIC
from otk.sets._support.geology import TOPIC as ROCK_TOPIC
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c14 import ROCK_MINERAL_SCENARIOS

PROVENANCE = Provenance("original")


ROCK = "หิน"


MINERAL = "แร่"


class Material(NamedTuple):
    """A rock or a mineral, an everyday thing made from it, and why it suits."""
    name: str
    kind: str
    product: str
    because: str


# Every product names one material; rocks and minerals are unambiguous at ป.6.
MATERIALS = (
    Material("หินปูน", ROCK, "ปูนซีเมนต์สำหรับสร้างบ้าน",
             "เมื่อเผาแล้วบดผสมกับวัตถุอื่นจะได้ปูนที่แข็งตัวเมื่อผสมน้ำ"),
    Material("หินอ่อน", ROCK, "พื้นและโต๊ะที่ขัดเป็นเงา",
             "เนื้อแน่นและขัดเงาได้สวยงาม"),
    Material("หินแกรนิต", ROCK, "ขั้นบันไดและเคาน์เตอร์ครัว",
             "แข็งมากและทนการขีดข่วน"),
    Material("หินชนวน", ROCK, "กระดานชนวน",
             "แยกออกเป็นแผ่นบางเรียบได้"),
    Material("แกรไฟต์", MINERAL, "ไส้ดินสอ",
             "นิ่มและทิ้งรอยสีดำเมื่อขีดบนกระดาษ"),
    Material("ยิปซัม", MINERAL, "ปูนปลาสเตอร์สำหรับเข้าเฝือก",
             "เมื่อผสมน้ำแล้วปั้นเป็นรูปและแข็งตัวได้เร็ว"),
    Material("ฮาไลต์", MINERAL, "เกลือแกงที่ใช้ปรุงอาหาร",
             "มีรสเค็มและละลายน้ำได้"),
    Material("ทัลก์", MINERAL, "แป้งฝุ่นทาตัว",
             "นิ่มมากจนบดเป็นผงละเอียดและลื่นมือ"),
)


def _of(kind: str) -> list[Material]:
    return [item for item in MATERIALS if item.kind == kind]


def survey_rows(rng: Random) -> list[Material]:
    """Two rocks and two minerals, shuffled, as a household survey records them."""
    rows = rng.sample(_of(ROCK), 2) + rng.sample(_of(MINERAL), 2)
    rng.shuffle(rows)
    return rows


def _examples(rock: Material, mineral: Material) -> str:
    return (f"ใช้ประโยชน์จาก{ROCK} เช่น นำ{rock.name}มาทำ{rock.product} "
            f"ส่วนใช้ประโยชน์จาก{MINERAL} เช่น นำ{mineral.name}มาทำ{mineral.product}")


@question_type("geo.rock_uses",
               display_name={"th": "การนำหินไปใช้ประโยชน์"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC)
class RockUses(ClassifyType):
    """โยงการใช้ประโยชน์เข้ากับหิน. แต่ละข้อระบุ *เหตุผล* ที่มาจากสมบัติของหินนั้น
    เอง จึงมีคำตอบถูกเพียงข้อเดียวแม้หลายชนิดจะใช้ตกแต่งอาคารเหมือนกัน."""

    CLASSIFY_STEM = "การนำไปใช้ประโยชน์ต่อไปนี้เป็นของหินชนิดใด: “{member}”"
    PICK_STEM = "ข้อใดคือการนำ{category}ไปใช้ประโยชน์"

    CATEGORIES = [
        Category("หินแกรนิต",
                 ("ใช้ทำแผ่นปูพื้นหรือเคาน์เตอร์ เพราะแข็ง ทนการขีดข่วน และขัดเงาได้",)),
        Category("หินบะซอลต์",
                 ("ใช้เป็นหินบดสำหรับทำถนน เพราะเนื้อแน่นและทนต่อการสึกกร่อน",)),
        Category("หินออบซิเดียน",
                 ("ใช้ทำมีดและอาวุธในสมัยโบราณ เพราะมีรอยแตกที่คม",)),
        Category("หินกรวด",
                 ("ใช้เป็นหินประดับผนังเมื่อผิวหินแสดงเม็ดกรวดมนหลายขนาด",)),
        Category("หินทราย",
                 ("ใช้ทำแผ่นปูและงานแกะสลัก เพราะตัดแต่งได้และเห็นลายชั้นสวยงาม",)),
        Category("หินดินดาน",
                 ("ใช้เป็นวัตถุดิบผลิตอิฐหรือปูนซีเมนต์ เพราะมีแร่ดินเหนียวเป็นส่วนมาก",)),
        Category("หินปูน",
                 ("ใช้ทำปูนซีเมนต์เพื่อผสมเป็นคอนกรีตสำหรับงานก่อสร้าง",)),
        Category("หินชนวน",
                 ("ใช้ทำกระดานชนวนและกระดานดำ เพราะกระเทาะออกเป็นแผ่นบางเรียบได้",
                  "ใช้มุงหลังคาหรือปูทางเท้า เพราะแยกออกเป็นแผ่นบาง ๆ ได้")),
        Category("หินอ่อน",
                 ("ใช้ตกแต่งอาคารและแกะสลัก เพราะเนื้อผลึกแน่นและขัดเงาได้",)),
        Category("หินควอร์ตไซต์",
                 ("ใช้เป็นหินบดหรือวัสดุทนการสึก เพราะมีควอตซ์ประสานกันแน่นและแข็งมาก",)),
    ]


@question_type(
    "geo.rock_mineral_use_foundation",
    display_name={"th": "สิ่งของที่ทำจากหินและแร่"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockMineralUseFoundation(QuestionType):
    """Name the rock or mineral behind an everyday thing, or why it suits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MATERIALS)
        others = [other for other in MATERIALS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.product}” ทำมาจาก{item.kind}ชนิดใด",
                correct=item.name,
                wrongs=tuple(other.name for other in others if other.kind == item.kind)[:3],
                hint="นึกถึงสมบัติที่สิ่งของนั้นต้องการ แล้วหาหินหรือแร่ที่มีสมบัตินั้น",
                topic=ROCK_TOPIC,
            )
        return _labelled(
            stem=f"เหตุใดจึงนำ{item.name}มาทำ{item.product}",
            correct=item.because,
            wrongs=tuple(other.because for other in others[:3]),
            hint="นึกถึงสมบัติที่สิ่งของนั้นต้องการ",
            topic=ROCK_TOPIC,
        )


@question_type(
    "geo.rock_mineral_use_fluency",
    display_name={"th": "บรรยายและยกตัวอย่างการใช้หินและแร่จากข้อมูลการสำรวจ"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockMineralUseFluency(QuestionType):
    """Give an example of a rock and of a mineral in use, from a survey record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = survey_rows(rng)
        record = " / ".join(f"{row.product} ทำจาก{row.name}" for row in rows)
        rocks = [row for row in rows if row.kind == ROCK]
        minerals = [row for row in rows if row.kind == MINERAL]
        rock, mineral = rocks[0], minerals[0]
        # A wrong choice misclassifies a material or pairs it with another row's
        # product, so it is wrong about this record, not just about the world.
        wrong_product_rock = rock._replace(product=rocks[1].product)
        return _labelled(
            stem=f"นักเรียนสำรวจสิ่งของในบ้านและบันทึกว่าทำจากอะไร — {record} "
                 "จากข้อมูลนี้ ข้อใดบรรยายและยกตัวอย่างการใช้ประโยชน์ของหินและแร่ได้ถูกต้อง",
            correct=_examples(rock, mineral),
            wrongs=(_examples(mineral, rock),
                    _examples(wrong_product_rock, mineral),
                    _examples(rocks[1], rock)),
            hint="แยกวัตถุดิบในบันทึกว่าเป็นหินหรือแร่ แล้วตรวจว่าทำเป็นสิ่งของใดตามบันทึก",
            topic=ROCK_TOPIC,
        )


@question_type(
    "geo.rock_mineral_use_application",
    display_name={"th": "เลือกใช้หินและแร่อย่างเหมาะสมและคุ้มค่า"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockMineralUseApplication(QuestionType):
    """Choose a material for a job, weigh a quarry's cost, and survey fairly."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ROCK_MINERAL_SCENARIOS,
            hint="นึกถึงสมบัติของหินหรือแร่ และผลต่อสิ่งแวดล้อมเมื่อนำมาใช้",
        ), ROCK_TOPIC)

"""การแก้ปัญหาด้วยความรู้เรื่องปฏิกิริยาเคมี

เคมี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.3/8

Sets moved here from: science_wave_d13.
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
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d10 import SECONDARY_THREE

PROVENANCE = Provenance("original")


DESIGN_TOPIC = "การแก้ปัญหาด้วยความรู้เรื่องปฏิกิริยาเคมี"


class Design(NamedTuple):
    problem: str
    solution: str


DESIGNS = (
    Design("ผู้ถูกมดคันไฟกัด ซึ่งพิษของมดมีกรดฟอร์มิก ทำให้แสบร้อน",
           "ทาบริเวณที่ถูกกัดด้วยสารละลายเบสอ่อน เช่น น้ำผสมผงฟู เพื่อสะเทินกรด"),
    Design("บ่อน้ำเสียจากโรงงานมีความเป็นกรดสูงก่อนปล่อยลงแหล่งน้ำ",
           "เติมปูนขาวปริมาณที่คำนวณไว้ลงในบ่อ เพื่อสะเทินกรดให้น้ำเป็นกลางก่อนปล่อย"),
    Design("ต้องการทำขนมเค้กให้ฟูนุ่มโดยไม่ใช้ยีสต์",
           "ผสมผงฟูที่มีเบกกิ้งโซดาและกรดอ่อน เมื่อโดนน้ำและความร้อนเกิดแก๊สคาร์บอนไดออกไซด์ทำให้เนื้อขนมฟู"),
    Design("เสาเหล็กของท่าเรือที่แช่อยู่ในน้ำทะเลผุกร่อนเร็ว",
           "ยึดแท่งสังกะสีหรือแมกนีเซียมไว้กับเสา ให้โลหะนั้นผุกร่อนแทนเหล็ก"),
    Design("ดินในแปลงผักเป็นกรดมากจนผักโตช้า",
           "โรยปูนขาวหรือโดโลไมต์ลงในดินตามปริมาณที่เหมาะสม เพื่อสะเทินกรดในดิน"),
    Design("กาต้มน้ำไฟฟ้ามีคราบหินปูนเกาะหนาที่ก้นกา",
           "ต้มน้ำส้มสายชูเจือจางในกาแล้วเทออก ให้กรดทำปฏิกิริยากับคราบหินปูนจนหลุดออก"),
    Design("ต้องการอุ่นอาหารระหว่างเดินป่าโดยไม่ใช้ไฟ",
           "ใช้ถุงให้ความร้อนที่ผงโลหะทำปฏิกิริยาคายความร้อนกับน้ำเกลือ วางห่ออาหารไว้บนถุง"),
    Design("นักกีฬาข้อเท้าแพลงกลางสนามที่ไม่มีน้ำแข็ง",
           "ใช้แผ่นประคบเย็นที่บีบให้สารเคมีผสมกับน้ำ เกิดปฏิกิริยาดูดความร้อน"),
)


DESIGN_SCENARIOS = (
    ("บ่อน้ำเสียมีกรดซึ่งต้องใช้ปูนขาว 2 กิโลกรัมต่อน้ำเสีย 1 ลูกบาศก์เมตรจึงจะเป็นกลาง ถ้าบ่อมีน้ำเสีย 15 ลูกบาศก์เมตร ต้องใช้ปูนขาวกี่กิโลกรัม",
     "30 กิโลกรัม", ("7.5 กิโลกรัม", "17 กิโลกรัม", "2 กิโลกรัม", "45 กิโลกรัม", "13 กิโลกรัม")),
    ("นักเรียนออกแบบถุงอุ่นมือแบบใช้ครั้งเดียว ควรเลือกปฏิกิริยาแบบใด และต้องทดสอบสิ่งใด",
     "เลือกปฏิกิริยาคายความร้อน เช่น การเกิดสนิมของผงเหล็กที่เร่งด้วยเกลือ และวัดว่าอุณหภูมิอุ่นพอแต่ไม่ร้อนจนเป็นอันตราย",
     ("เลือกปฏิกิริยาดูดความร้อน และทดสอบว่าเย็นลงมากที่สุด",
      "เลือกปฏิกิริยาใดก็ได้ ไม่ต้องทดสอบอุณหภูมิ",
      "เลือกการเผาไหม้แก๊สในถุงพลาสติก",
      "เลือกปฏิกิริยาดูดความร้อน เพราะถุงต้องดึงความร้อนจากมือ",
      "เลือกปฏิกิริยาคายความร้อนใดก็ได้ และทดสอบเพียงว่าถุงมีสีสวย")),
    ("ทีมนักเรียนเสนอสองวิธีป้องกันสนิมรั้วเหล็ก วิธีแรกทาสีราคา 300 บาท ต้องทาใหม่ทุก 2 ปี วิธีที่สองชุบสังกะสีราคา 1,200 บาท ใช้ได้ 10 ปี ในระยะ 10 ปี วิธีใดใช้ค่าใช้จ่ายน้อยกว่า",
     "ชุบสังกะสี เพราะ 1,200 บาท น้อยกว่าทาสี 5 ครั้งรวม 1,500 บาท",
     ("ทาสี เพราะ 300 บาท น้อยกว่า 1,200 บาท",
      "เท่ากัน เพราะใช้เงิน 1,200 บาทเท่ากัน",
      "ทาสี เพราะรวม 10 ปีใช้ 600 บาท",
      "ชุบสังกะสี เพราะ 1,200 บาท น้อยกว่าทาสีรวม 3,000 บาท",
      "ทาสี เพราะจ่ายทีละน้อยจึงถูกกว่าเสมอ")),
)


def lime_dose(rng: Random) -> GeneratedQuestion:
    """Lime per cubic metre times the volume of the pond."""
    rate, volume = rng.choice((2, 3, 4, 5)), rng.randint(8, 30)
    answer = rate * volume
    pool = (rate + volume, 2 * answer, rate * (volume - 1), rate * (volume + 1), volume)
    return _labelled(
        stem=(f"บ่อน้ำเสียมีกรดซึ่งต้องใช้ปูนขาว {rate} กิโลกรัมต่อน้ำเสีย 1 ลูกบาศก์เมตรจึงจะเป็นกลาง "
              f"ถ้าบ่อมีน้ำเสีย {volume} ลูกบาศก์เมตร ต้องใช้ปูนขาวกี่กิโลกรัม"),
        correct=f"{answer} กิโลกรัม",
        wrongs=tuple(dict.fromkeys(f"{w} กิโลกรัม" for w in pool if w != answer)),
        hint="ปริมาณปูนขาว = ปูนขาวต่อลูกบาศก์เมตร × ปริมาตรน้ำเสีย",
        topic=DESIGN_TOPIC,
    )


def rust_cost(rng: Random) -> GeneratedQuestion:
    """Repainting every few years against one galvanising, over ten years."""
    paint, every = rng.randrange(200, 501, 50), rng.choice((2, 5))
    coats = 10 // every
    total = paint * coats
    zinc = rng.choice([z for z in range(800, 2001, 100) if z != total])
    galv = f"ชุบสังกะสี เพราะ {zinc:,} บาท น้อยกว่าทาสี {coats} ครั้งรวม {total:,} บาท"
    coat = f"ทาสี เพราะทาสี {coats} ครั้งรวม {total:,} บาท น้อยกว่าชุบสังกะสี {zinc:,} บาท"
    same = "เท่ากัน เพราะทั้งสองวิธีใช้ได้ 10 ปีเหมือนกัน"
    if zinc < total:
        correct = galv
        wrongs = (coat, same, f"ทาสี เพราะทาสีครั้งละ {paint:,} บาท น้อยกว่าชุบสังกะสี {zinc:,} บาท",
                  "ทาสี เพราะจ่ายทีละน้อยจึงถูกกว่าเสมอ")
    else:
        correct = coat
        wrongs = (galv, same, f"ชุบสังกะสี เพราะ {zinc:,} บาท น้อยกว่าทาสีรวม {paint * (coats + 1):,} บาท",
                  "ชุบสังกะสี เพราะจ่ายครั้งเดียวจึงถูกกว่าเสมอ")
    return _labelled(
        stem=(f"ทีมนักเรียนเสนอสองวิธีป้องกันสนิมรั้วเหล็ก วิธีแรกทาสีราคา {paint:,} บาท ต้องทาใหม่ทุก {every} ปี "
              f"วิธีที่สองชุบสังกะสีราคา {zinc:,} บาท ใช้ได้ 10 ปี ในระยะ 10 ปี วิธีใดใช้ค่าใช้จ่ายน้อยกว่า"),
        correct=correct,
        wrongs=wrongs,
        hint="คิดค่าใช้จ่ายรวมตลอด 10 ปีของแต่ละวิธีแล้วเทียบกัน",
        topic=DESIGN_TOPIC,
    )


@question_type(
    "chem.reaction_design_foundation",
    display_name={"th": "ระบุปฏิกิริยาเคมีที่ใช้ในวิธีแก้ปัญหา"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class ReactionDesignFoundation(QuestionType):
    """A solution already in use; which reaction it relies on."""

    CASES = (
        ("ใช้ยาลดกรดที่เป็นเบสอ่อนบรรเทาอาการกรดในกระเพาะอาหารมากเกินไป", "ปฏิกิริยาระหว่างกรดกับเบส"),
        ("เคลือบสังกะสีบนแผ่นเหล็กทำหลังคา", "การป้องกันการเกิดสนิมของเหล็ก"),
        ("ใช้แก๊สหุงต้มเป็นเชื้อเพลิงให้ความร้อน", "การเผาไหม้"),
        ("ใช้ผงฟูทำให้ขนมปังฟู", "ปฏิกิริยาของผงฟูที่เกิดแก๊สคาร์บอนไดออกไซด์ทำให้เนื้อขนมขยายตัว"),
        ("ใช้น้ำส้มสายชูขจัดคราบหินปูนในกาต้มน้ำ", "ปฏิกิริยาระหว่างกรดกับหินปูนซึ่งเกิดแก๊สคาร์บอนไดออกไซด์"),
        ("ใช้ถุงอุ่นมือที่มีผงเหล็กให้ความร้อนเมื่อแกะซอง", "ปฏิกิริยาคายความร้อนของผงเหล็กกับออกซิเจน"),
        ("ใช้แผ่นประคบเย็นที่มีแอมโมเนียมไนเตรตกับน้ำ", "ปฏิกิริยาดูดความร้อน"),
        ("หมักแป้งขนมปังด้วยยีสต์", "การหมักที่ยีสต์เปลี่ยนน้ำตาลเป็นแก๊สคาร์บอนไดออกไซด์และเอทานอล"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(self.CASES))
        case, reaction = self.CASES[index]
        return _labelled(
            stem=f"การ{case} อาศัยความรู้เรื่องใด",
            correct=reaction,
            wrongs=tuple(r for i, (_, r) in enumerate(self.CASES) if i != index),
            hint="ดูว่าวิธีนั้นทำให้สารใดทำปฏิกิริยากัน และได้ผลิตภัณฑ์อะไร",
            topic=DESIGN_TOPIC,
        )


@question_type(
    "chem.reaction_design_fluency",
    display_name={"th": "ออกแบบวิธีแก้ปัญหาในชีวิตประจำวันโดยใช้ความรู้เรื่องปฏิกิริยาเคมี"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class ReactionDesignFluency(QuestionType):
    """A problem; the designed solution that uses a reaction to solve it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(DESIGNS))
        design = DESIGNS[index]
        return _labelled(
            stem=f"{design.problem} ข้อใดเป็นวิธีแก้ปัญหาที่ใช้ความรู้เรื่องปฏิกิริยาเคมีได้เหมาะสมที่สุด",
            correct=design.solution,
            wrongs=tuple(d.solution for i, d in enumerate(DESIGNS) if i != index),
            hint="ระบุสารที่เป็นต้นเหตุของปัญหา แล้วหาปฏิกิริยาที่เปลี่ยนสารนั้นหรือป้องกันไม่ให้เกิด",
            topic=DESIGN_TOPIC,
        )


@question_type(
    "chem.reaction_design_application",
    display_name={"th": "บูรณาการคณิตศาสตร์และวิศวกรรมในการแก้ปัญหาด้วยปฏิกิริยาเคมี"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class ReactionDesignApplication(QuestionType):
    """Dosing lime, a hand warmer, and costing rust protection."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return lime_dose(rng)
        if roll < 0.6:
            return rust_cost(rng)
        return _retopic(scenario_question(
            rng, DESIGN_SCENARIOS,
            hint="ใช้ความรู้เรื่องปฏิกิริยาเลือกวิธี แล้วใช้การคำนวณหรือการทดสอบตัดสินว่าใช้ได้จริง",
        ), DESIGN_TOPIC)

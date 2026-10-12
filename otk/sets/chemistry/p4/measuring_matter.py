"""การวัดมวลและปริมาตรของสสาร

เคมี · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.4/4

Sets moved here from: science_wave_d5.
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
from otk.sets._support.science_wave_d4 import FOURTH

PROVENANCE = Provenance("original")


MEASURING_TOPIC = "การวัดมวลและปริมาตรของสสาร"


class Task(NamedTuple):
    task: str
    tool: str
    wrongs: tuple[str, ...]


TASKS = (
    Task("วัดมวลของก้อนหิน", "เครื่องชั่ง",
         ("กระบอกตวง", "ไม้บรรทัด", "เทอร์โมมิเตอร์", "นาฬิกาจับเวลา", "ตลับเมตร")),
    Task("วัดปริมาตรของน้ำในขวด", "กระบอกตวง",
         ("เครื่องชั่ง", "ไม้บรรทัด", "นาฬิกาจับเวลา", "เทอร์โมมิเตอร์", "ตลับเมตร")),
    Task("วัดมวลของน้ำมันพืชในขวด", "เครื่องชั่ง",
         ("กระบอกตวงเพียงอย่างเดียว", "ไม้บรรทัด", "เทอร์โมมิเตอร์", "นาฬิกาจับเวลา", "ตลับเมตร")),
    Task("วัดปริมาตรของก้อนหินที่มีรูปร่างไม่แน่นอน", "กระบอกตวงที่ใส่น้ำไว้ แล้วดูระดับน้ำที่เพิ่มขึ้น",
         ("เครื่องชั่ง", "ไม้บรรทัดวัดความยาวด้านเดียว", "เทอร์โมมิเตอร์",
          "กระบอกตวงเปล่าที่ไม่มีน้ำ", "นาฬิกาจับเวลา")),
    Task("วัดปริมาตรของนมที่เทออกจากกล่อง", "กระบอกตวง",
         ("เครื่องชั่ง", "ไม้บรรทัด", "เทอร์โมมิเตอร์", "นาฬิกาจับเวลา", "ตลับเมตร")),
    Task("แสดงว่าอากาศในลูกบอลมีมวล", "เครื่องชั่ง โดยชั่งลูกบอลก่อนและหลังสูบลม",
         ("กระบอกตวง", "ไม้บรรทัด", "เทอร์โมมิเตอร์", "นาฬิกาจับเวลา", "ตลับเมตร")),
)


MEASURING_SCENARIOS = (
    ("นักเรียนต้องการแสดงว่าอากาศมีมวล โดยใช้เครื่องชั่ง ควรทำอย่างไร",
     "ชั่งลูกบอลที่ยังไม่สูบลม แล้วสูบลมเข้าไปจนแน่นและชั่งอีกครั้ง เปรียบเทียบมวลที่ได้",
     ("ชั่งอากาศในห้องโดยวางเครื่องชั่งไว้เปล่า ๆ",
      "วัดปริมาตรของลูกบอลด้วยไม้บรรทัด",
      "ชั่งลูกบอลที่สูบลมแล้วเพียงครั้งเดียว",
      "ชั่งลูกบอลแฟบสองครั้งติดกัน",
      "วัดความสูงของลูกบอลก่อนและหลังสูบลม")),
    ("ขณะอ่านปริมาตรน้ำในกระบอกตวง นักเรียนควรมองอย่างไรจึงอ่านค่าได้ถูกต้อง",
     "วางกระบอกตวงบนพื้นราบ แล้วมองระดับสายตาตรงกับส่วนโค้งล่างของผิวน้ำ",
     ("ยกกระบอกตวงขึ้นเหนือศีรษะแล้วมองจากด้านล่าง",
      "มองจากด้านบนของกระบอกตวงลงไป",
      "เอียงกระบอกตวงแล้วอ่านค่าที่ขอบบนสุดของน้ำ",
      "ย่อตัวมองจากระดับต่ำกว่าผิวน้ำ",
      "อ่านค่าขณะเขย่ากระบอกตวง")),
    ("ก้อนดินน้ำมันก้อนหนึ่งชั่งได้ 50 กรัม ถ้าปั้นให้เป็นรูปแผ่นแบนแล้วชั่งใหม่ จะได้มวลเท่าใด",
     "50 กรัม เพราะเปลี่ยนเพียงรูปร่าง เนื้อดินน้ำมันไม่ได้เพิ่มหรือลดลง",
     ("น้อยกว่า 50 กรัม เพราะแผ่นแบนบางลง",
      "มากกว่า 50 กรัม เพราะแผ่นแบนกว้างขึ้น",
      "0 กรัม เพราะรูปร่างเปลี่ยนไปแล้ว",
      "25 กรัม เพราะแผ่นแบนมีความหนาครึ่งหนึ่ง",
      "100 กรัม เพราะแผ่นแบนมีพื้นที่มากขึ้นสองเท่า")),
)


CLAY_SHAPES = ("ลูกกลม", "ตัวหนอนยาว", "แผ่นแบน", "รูปดาว", "รูปถ้วย")


def clay_pieces(rng: Random) -> GeneratedQuestion:
    """Clay reshaped and cut into equal pieces; each piece's mass."""
    pieces = rng.choice((2, 4, 5))
    each = rng.choice(range(10, 41, 5))
    total = pieces * each
    shape = rng.choice(CLAY_SHAPES)
    pool = (total, total * pieces, total - pieces, each + pieces, 2 * each)
    wrongs = tuple(dict.fromkeys(f"{w} กรัม" for w in pool if w != each))
    return _labelled(
        stem=(f"ดินน้ำมันก้อนหนึ่งชั่งได้ {total} กรัม นักเรียนปั้นเป็น{shape} แล้วแบ่งออกเป็น {pieces} ก้อนเท่า ๆ กัน "
              "ดินน้ำมันแต่ละก้อนมีมวลเท่าใด"),
        correct=f"{each} กรัม",
        wrongs=wrongs,
        hint="การปั้นเปลี่ยนเพียงรูปร่าง มวลรวมเท่าเดิม แล้วแบ่งมวลรวมเท่า ๆ กันตามจำนวนก้อน",
        topic=MEASURING_TOPIC,
    )


@question_type(
    "chem.measuring_matter_foundation",
    display_name={"th": "เลือกเครื่องมือวัดมวลหรือปริมาตรของสสาร"},
    level=FOURTH, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class MeasuringMatterFoundation(QuestionType):
    """A measuring task; the instrument for it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        task = rng.choice(TASKS)
        return _labelled(
            stem=f"นักเรียนต้องการ{task.task} ควรใช้เครื่องมือใด",
            correct=task.tool,
            wrongs=task.wrongs,
            hint="มวลวัดด้วยเครื่องชั่ง ปริมาตรของของเหลววัดด้วยกระบอกตวง",
            topic=MEASURING_TOPIC,
        )


@question_type(
    "chem.measuring_matter_fluency",
    display_name={"th": "หาปริมาตรหรือมวลของสสารจากค่าที่อ่านได้"},
    level=FOURTH, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class MeasuringMatterFluency(QuestionType):
    """Readings before and after; the mass or volume they give."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            before = rng.choice(range(50, 81, 10))
            added = rng.choice(range(10, 41, 5))
            after = before + added
            return _labelled(
                stem=(f"กระบอกตวงมีน้ำ {before} มิลลิลิตร เมื่อใส่ก้อนหินลงไปจนจมมิด ระดับน้ำขึ้นไปอยู่ที่ "
                      f"{after} มิลลิลิตร ก้อนหินมีปริมาตรเท่าใด"),
                correct=f"{added} ลูกบาศก์เซนติเมตร",
                wrongs=(f"{after} ลูกบาศก์เซนติเมตร", f"{before} ลูกบาศก์เซนติเมตร",
                        f"{before + after} ลูกบาศก์เซนติเมตร"),
                hint="ปริมาตรของก้อนหินเท่ากับปริมาตรน้ำที่เพิ่มขึ้น (1 มิลลิลิตร เท่ากับ 1 ลูกบาศก์เซนติเมตร)",
                topic=MEASURING_TOPIC,
            )
        empty = rng.choice(range(100, 201, 20))
        water = rng.choice([w for w in range(150, 301, 50) if w != empty])
        return _labelled(
            stem=(f"ชั่งแก้วเปล่าได้ {empty} กรัม เทน้ำใส่แล้วชั่งแก้วพร้อมน้ำได้ {empty + water} กรัม "
                  "น้ำในแก้วมีมวลเท่าใด"),
            correct=f"{water} กรัม",
            wrongs=(f"{empty + water} กรัม", f"{empty} กรัม", f"{2 * empty + water} กรัม"),
            hint="มวลของน้ำ = มวลของแก้วพร้อมน้ำ ลบ มวลของแก้วเปล่า",
            topic=MEASURING_TOPIC,
        )


@question_type(
    "chem.measuring_matter_application",
    display_name={"th": "วางแผนและตรวจการวัดมวลและปริมาตรของสสาร"},
    level=FOURTH, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class MeasuringMatterApplication(QuestionType):
    """Weighing air, reading a cylinder, and mass kept through a change of shape."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return clay_pieces(rng)
        return _retopic(scenario_question(
            rng, MEASURING_SCENARIOS,
            hint="คิดว่าต้องวัดอะไรด้วยเครื่องมือใด และค่าที่ได้เปลี่ยนเพราะสสารเปลี่ยนจริงหรือไม่",
        ), MEASURING_TOPIC)

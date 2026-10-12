"""วัตถุที่ประกอบจากชิ้นส่วนย่อย

เคมี · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.3/1

Sets moved here from: science_wave_d3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d3 import THIRD

PROVENANCE = Provenance("original")


PARTS_TOPIC = "วัตถุที่ประกอบจากชิ้นส่วนย่อย"


BUILT = ("ตัวต่อเลโก้ที่ต่อเป็นรูปบ้าน", "สร้อยข้อมือที่ร้อยจากลูกปัด", "ภาพจิ๊กซอว์ที่ต่อเสร็จแล้ว",
         "กำแพงที่ก่อจากอิฐก้อนเล็ก ๆ", "หุ่นยนต์ที่ประกอบจากบล็อกไม้")


WHOLE = ("ลูกโป่งที่เป่าลมแล้ว", "ไข่ไก่ทั้งฟอง", "แก้วน้ำใบเดียว", "ใบไม้สด", "ก้อนดินน้ำมันที่ปั้นเป็นก้อนกลม")


# (pieces, first build, second build)
SETS = (
    ("ตัวต่อพลาสติก", "บ้าน", "รถ"),
    ("บล็อกไม้", "หอคอย", "สะพาน"),
    ("ตัวต่อแม่เหล็ก", "หุ่นยนต์", "เรือ"),
)


COLOURS = ("สีแดง", "สีฟ้า")


PARTS_SCENARIOS = (
    ("นักเรียนต่อตัวต่อเป็นรูปบ้าน แล้วเพื่อนแยกออกไปต่อเป็นรูปรถโดยใช้ทุกชิ้น ข้อใดถูกต้อง",
     "บ้านและรถประกอบจากชิ้นส่วนย่อยชุดเดียวกัน เพียงจัดเรียงต่างกัน",
     ("รถเป็นวัสดุชนิดใหม่ที่ต่างจากตัวต่อเดิม",
      "ตัวต่อที่เคยเป็นบ้านนำมาต่อเป็นอย่างอื่นไม่ได้",
      "รถต้องมีจำนวนชิ้นส่วนมากกว่าบ้านเสมอ",
      "บ้านต้องมีจำนวนชิ้นส่วนมากกว่ารถเสมอ",
      "ตัวต่อละลายรวมกันเมื่อแยกออก")),
    ("สร้อยลูกปัดของนักเรียนขาด ลูกปัดหลุดออกมาทั้งหมด นักเรียนจะนำลูกปัดเหล่านั้นไปทำเป็นกำไลข้อมือได้หรือไม่ เพราะเหตุใด",
     "ได้ เพราะสร้อยประกอบจากลูกปัดซึ่งเป็นชิ้นส่วนย่อยที่นำมาร้อยประกอบใหม่ได้",
     ("ไม่ได้ เพราะลูกปัดที่หลุดออกจากสร้อยแล้วจะละลายหายไป",
      "ไม่ได้ เพราะลูกปัดใช้ได้เพียงครั้งเดียว",
      "ได้ แต่ต้องหลอมลูกปัดรวมกันเป็นก้อนเดียวก่อน",
      "ได้ แต่ต้องซื้อลูกปัดใหม่ทั้งหมด",
      "ไม่ได้ เพราะลูกปัดกลายเป็นวัสดุชนิดใหม่")),
    ("เก้าอี้ไม้ตัวหนึ่งประกอบจากแผ่นไม้หลายแผ่นยึดด้วยสกรู ถ้าคลายสกรูออกทั้งหมด จะนำแผ่นไม้ไปทำอะไรได้บ้าง",
     "นำแผ่นไม้มาประกอบใหม่เป็นชั้นวางของ เพราะเก้าอี้ประกอบจากชิ้นส่วนย่อยที่แยกออกได้",
     ("ทำอะไรไม่ได้ เพราะแผ่นไม้ที่แยกออกแล้วกลายเป็นขี้เลื่อยทั้งหมด",
      "นำไปประกอบได้เฉพาะเก้าอี้ตัวเดิมเท่านั้น",
      "ต้องนำแผ่นไม้ไปหลอมก่อนจึงจะใช้ได้",
      "ต้องเผาแผ่นไม้ก่อนจึงจะประกอบใหม่ได้",
      "แผ่นไม้ที่แยกออกแล้วใช้ได้เพียงทำฟืนเท่านั้น")),
    ("ภาพจิ๊กซอว์ 100 ชิ้นถูกแยกออกเก็บในกล่อง แล้วนำมาต่อใหม่ในวันรุ่งขึ้นโดยไม่มีชิ้นใดหาย ข้อใดถูกต้อง",
     "ภาพที่ต่อใหม่มี 100 ชิ้นเท่าเดิม เพราะประกอบจากชิ้นส่วนย่อยชุดเดิม",
     ("ภาพที่ต่อใหม่มี 200 ชิ้น เพราะแยกแล้วชิ้นส่วนเพิ่มขึ้น",
      "ภาพที่ต่อใหม่มี 50 ชิ้น เพราะชิ้นส่วนหายไปครึ่งหนึ่ง",
      "ต่อใหม่ไม่ได้ เพราะชิ้นส่วนเปลี่ยนรูปร่าง",
      "ภาพกลายเป็นกระดาษแผ่นเดียวที่ไม่มีรอยต่อ",
      "ต่อใหม่ได้เฉพาะเมื่อซื้อชิ้นส่วนเพิ่ม")),
    ("ถ้าเปรียบเทียบลูกโป่งที่เป่าลมแล้วกับกำแพงที่ก่อจากอิฐ ข้อใดถูกต้อง",
     "กำแพงประกอบจากชิ้นส่วนย่อยคือก้อนอิฐ ส่วนลูกโป่งเป็นวัตถุชิ้นเดียวที่ไม่ได้ประกอบจากชิ้นส่วนย่อยแบบนั้น",
     ("ลูกโป่งประกอบจากก้อนอิฐเล็ก ๆ",
      "ทั้งสองแยกเป็นชิ้นส่วนแล้วนำมาต่อใหม่ได้เหมือนกัน",
      "กำแพงเป็นวัตถุชิ้นเดียวที่แยกไม่ได้",
      "ลูกโป่งประกอบจากลูกปัดหลายเม็ด",
      "ทั้งสองไม่ได้ทำจากวัสดุใดเลย")),
)


@question_type(
    "chem.object_parts_foundation",
    display_name={"th": "ระบุวัตถุที่ประกอบจากชิ้นส่วนย่อยซึ่งแยกและประกอบใหม่ได้"},
    level=THIRD, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ObjectPartsFoundation(QuestionType):
    """Which object is built of small parts that come apart and go back together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _labelled(
            stem="วัตถุใดประกอบขึ้นจากชิ้นส่วนย่อย ๆ ที่แยกออกจากกันแล้วนำมาประกอบเป็นวัตถุชิ้นใหม่ได้",
            correct=rng.choice(BUILT),
            wrongs=tuple(WHOLE),
            hint="ลองนึกว่าถ้าแยกวัตถุนั้นออก จะได้ชิ้นส่วนเล็ก ๆ ที่นำมาต่อใหม่ได้หรือไม่",
            topic=PARTS_TOPIC,
        )


@question_type(
    "chem.object_parts_fluency",
    display_name={"th": "อธิบายการแยกและประกอบชิ้นส่วนย่อยเป็นวัตถุใหม่จากหลักฐาน"},
    level=THIRD, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ObjectPartsFluency(QuestionType):
    """Count the pieces of a build, take it apart, rebuild; explain what the new object holds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pieces, first, second = rng.choice(SETS)
        red = rng.randint(3, 9)
        blue = rng.choice([n for n in range(3, 10) if n != red])
        total = red + blue
        colour = rng.choice(COLOURS)
        part = red if colour == COLOURS[0] else blue
        return _labelled(
            stem=(f"นักเรียนต่อ{pieces}{COLOURS[0]} {red} ชิ้น และ{COLOURS[1]} {blue} ชิ้น เป็นรูป{first} "
                  f"จากนั้นแยกทุกชิ้นออกจากกัน แล้วนำชิ้นส่วนทั้งหมดมาต่อเป็นรูป{second} โดยไม่เพิ่มหรือทิ้งชิ้นใด "
                  f"จากหลักฐานนี้ ข้อใดอธิบาย{second}ได้ถูกต้อง"),
            correct=f"{second}มี {total} ชิ้น เพราะประกอบจากชิ้นส่วนย่อยชุดเดิมที่แยกออกจาก{first}",
            wrongs=(f"{second}มี {part} ชิ้น เพราะใช้เฉพาะชิ้นส่วน{colour}ที่แยกออกจาก{first}",
                    f"{second}มี {total * 2} ชิ้น เพราะเมื่อแยกออก ชิ้นส่วนแต่ละชิ้นแบ่งออกเป็นสองชิ้น",
                    f"{second}มี {total} ชิ้น เพราะชิ้นส่วนรวมกันเป็นเนื้อเดียว จึงแยกออกจากกันไม่ได้อีก",
                    # The wrong count and a wrong reason.
                    f"{second}มี {part} ชิ้น เพราะเมื่อแยกออก ชิ้นส่วนแต่ละชิ้นแบ่งออกเป็นสองชิ้น",
                    f"{second}มี {total * 2} ชิ้น เพราะชิ้นส่วนรวมกันเป็นเนื้อเดียว จึงแยกออกจากกันไม่ได้อีก"),
            hint="ชิ้นส่วนที่แยกออกไม่ได้หายไปหรือเพิ่มขึ้น เพียงนำมาจัดเรียงใหม่",
            topic=PARTS_TOPIC,
        )


@question_type(
    "chem.object_parts_application",
    display_name={"th": "ใช้ความรู้เรื่องชิ้นส่วนย่อยของวัตถุในชีวิตประจำวัน"},
    level=THIRD, subject=SUBJECT, topic=PARTS_TOPIC,
)
class ObjectPartsApplication(QuestionType):
    """Rebuilding blocks, restringing beads, and taking a chair apart."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PARTS_SCENARIOS,
            hint="วัตถุที่ประกอบจากชิ้นส่วนย่อย แยกออกแล้วยังได้ชิ้นส่วนเดิมที่นำไปประกอบใหม่ได้",
        ), PARTS_TOPIC)

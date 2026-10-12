"""แบบจำลองอะตอมของโบร์กับแบบจำลองอะตอมแบบกลุ่มหมอก

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/2

Sets moved here from: science_wave_e1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e1 import SUBJECT

PROVENANCE = Provenance("original")


TOPIC_MODEL = "แบบจำลองอะตอมของโบร์กับแบบจำลองอะตอมแบบกลุ่มหมอก"


BOHR = "แบบจำลองอะตอมของโบร์"


CLOUD = "แบบจำลองอะตอมแบบกลุ่มหมอก"


BOTH_MODELS = "ทั้งสองแบบจำลอง"


NEITHER_MODEL = "ไม่มีแบบจำลองใดกล่าวถึง"


# Two earlier models, offered as wrong choices so a fact cannot be matched by elimination.
MODEL_CHOICES = (BOHR, CLOUD, BOTH_MODELS, NEITHER_MODEL,
                 "แบบจำลองอะตอมของดาลตัน", "แบบจำลองอะตอมของทอมสัน")


MODEL_ONLY_FACTS: tuple[tuple[str, str], ...] = (
    ("อิเล็กตรอนเคลื่อนที่เป็นวงโคจรรอบนิวเคลียสด้วยระดับพลังงานที่แน่นอน", BOHR),
    ("สามารถระบุตำแหน่งและเส้นทางการเคลื่อนที่ของอิเล็กตรอนได้อย่างแน่นอนในแต่ละเวลา", BOHR),
    ("อิเล็กตรอนไม่มีเส้นทางการเคลื่อนที่ที่แน่นอน บอกได้เพียงโอกาสพบอิเล็กตรอนบริเวณต่าง ๆ รอบนิวเคลียส", CLOUD),
    ("บริเวณที่กลุ่มหมอกทึบกว่าแสดงว่ามีโอกาสพบอิเล็กตรอนสูงกว่าบริเวณที่กลุ่มหมอกจาง", CLOUD),
    ("อิเล็กตรอนในแต่ละวงมีรัศมีวงโคจรที่แน่นอนรอบนิวเคลียส", BOHR),
    ("อธิบายสเปกตรัมเส้นของอะตอมไฮโดรเจนได้ แต่อธิบายอะตอมที่มีหลายอิเล็กตรอนได้ไม่ดี", BOHR),
    ("แสดงอิเล็กตรอนเป็นบริเวณหนาแน่นรอบนิวเคลียสแทนการวาดเป็นวงโคจรเป็นเส้น", CLOUD),
    ("ใช้อธิบายสมบัติของอะตอมที่มีหลายอิเล็กตรอนได้ดีกว่าแบบจำลองที่มีวงโคจรเป็นเส้น", CLOUD),
)


DIFFERENCE_CORRECT = (
    "โบร์: อิเล็กตรอนโคจรเป็นวงที่มีระดับพลังงานแน่นอน กลุ่มหมอก: บอกได้เพียงโอกาสพบอิเล็กตรอนรอบนิวเคลียส"
)


DIFFERENCE_WRONGS = (
    "กลุ่มหมอก: อิเล็กตรอนโคจรเป็นวงที่มีระดับพลังงานแน่นอน โบร์: อิเล็กตรอนไม่มีเส้นทางแน่นอน",
    "ทั้งสองแบบจำลองอธิบายว่าสามารถระบุตำแหน่งที่แน่นอนของอิเล็กตรอนได้ในทุกเวลา",
    "แบบจำลองทั้งสองไม่มีความแตกต่างกันเลย เพราะอธิบายอิเล็กตรอนแบบเดียวกันทั้งหมด",
    "โบร์อธิบายว่าอะตอมไม่มีนิวเคลียส ส่วนกลุ่มหมอกอธิบายว่ามีนิวเคลียสอยู่ตรงกลาง",
    "กลุ่มหมอก: อิเล็กตรอนอยู่ภายในนิวเคลียส โบร์: อิเล็กตรอนโคจรเป็นวงรอบนิวเคลียส",
)


# (question, the right comparison, wrong ones) — the difference, the likeness, and why a new model.
MODEL_COMPARISONS = (
    ("ข้อใดกล่าวถึงความแตกต่างระหว่างแบบจำลองอะตอมของโบร์กับแบบจำลองอะตอมแบบกลุ่มหมอกได้ถูกต้อง",
     DIFFERENCE_CORRECT, DIFFERENCE_WRONGS),
    ("ข้อใดเป็นสิ่งที่แบบจำลองอะตอมของโบร์และแบบจำลองอะตอมแบบกลุ่มหมอกมีเหมือนกัน",
     "ทั้งสองแบบจำลองมีนิวเคลียสอยู่ตรงกลาง และมีอิเล็กตรอนอยู่รอบนิวเคลียส",
     ("ทั้งสองแบบจำลองระบุตำแหน่งที่แน่นอนของอิเล็กตรอนได้ทุกเวลา",
      "ทั้งสองแบบจำลองกล่าวว่าอะตอมเป็นทรงกลมตันที่แบ่งแยกไม่ได้",
      "ทั้งสองแบบจำลองกล่าวว่าอิเล็กตรอนอยู่ในนิวเคลียส",
      "ทั้งสองแบบจำลองวาดอิเล็กตรอนเป็นวงโคจรเป็นเส้นเหมือนกัน",
      "ทั้งสองแบบจำลองกล่าวว่าอะตอมไม่มีนิวเคลียส อิเล็กตรอนกระจายทั่วอะตอม",
      "ทั้งสองแบบจำลองกล่าวว่าอิเล็กตรอนเคลื่อนที่เป็นวงกลมด้วยความเร็วคงที่")),
    ("เหตุใดจึงมีการเสนอแบบจำลองอะตอมแบบกลุ่มหมอกขึ้นหลังแบบจำลองอะตอมของโบร์",
     "แบบจำลองของโบร์อธิบายสมบัติของอะตอมที่มีหลายอิเล็กตรอนได้ไม่ดี",
     ("แบบจำลองของโบร์ไม่มีนิวเคลียสอยู่ตรงกลางอะตอม", "แบบจำลองของโบร์อธิบายอะตอมไฮโดรเจนไม่ได้เลย",
      "แบบจำลองกลุ่มหมอกระบุเส้นทางของอิเล็กตรอนได้แน่นอนกว่า", "อิเล็กตรอนถูกค้นพบหลังแบบจำลองของโบร์",
      "แบบจำลองกลุ่มหมอกวาดได้ง่ายกว่าเท่านั้น ไม่ได้อธิบายสิ่งใดเพิ่ม",
      "แบบจำลองของโบร์ใช้ได้กับอะตอมทุกชนิดอยู่แล้ว แต่นักวิทยาศาสตร์ต้องการชื่อใหม่")),
)


MODEL_SCENARIOS: tuple[tuple[str, str], ...] = (
    ("จากการสังเกตแบบจำลอง นักเรียนพบว่าอิเล็กตรอนอยู่ได้เฉพาะในวงโคจรที่มีระดับพลังงานเป็นค่าเฉพาะเท่านั้น "
     "และเคลื่อนที่เป็นวงกลมรอบนิวเคลียสด้วยเส้นทางที่คำนวณได้แน่นอน", BOHR),
    ("จากการสังเกตแบบจำลอง นักเรียนพบว่าไม่สามารถระบุตำแหน่งของอิเล็กตรอนในขณะใดขณะหนึ่งได้ "
     "ทำได้เพียงแสดงบริเวณที่มีโอกาสพบอิเล็กตรอนสูงหรือต่ำรอบนิวเคลียสเป็นกลุ่มหมอก", CLOUD),
    ("นักเรียนวาดอะตอมไฮโดรเจนเป็นนิวเคลียสตรงกลาง มีอิเล็กตรอนหนึ่งตัวเคลื่อนที่บนวงกลมรัศมีคงที่ "
     "และเมื่อได้รับพลังงานค่าหนึ่งอิเล็กตรอนจะย้ายไปอยู่วงที่ใหญ่ขึ้น", BOHR),
    ("นักเรียนสร้างแบบจำลองโดยดัดลวดเป็นวงกลมหลายวงรอบลูกบอลตรงกลาง "
     "และติดลูกปัดแทนอิเล็กตรอนไว้บนลวดแต่ละวง", BOHR),
    ("นักเรียนใช้จุดจำนวนมากแสดงตำแหน่งที่อาจพบอิเล็กตรอน โดยจุดหนาแน่นใกล้นิวเคลียส "
     "และบางลงเมื่ออยู่ห่างออกไป", CLOUD),
    ("นักเรียนเปรียบอิเล็กตรอนกับใบพัดลมที่หมุนเร็วจนเห็นเป็นแผ่นเบลอ "
     "บอกได้เพียงบริเวณที่น่าจะพบ ไม่รู้ตำแหน่งแน่นอนในขณะใดขณะหนึ่ง", CLOUD),
)


@question_type(
    "chem.atomic_model_foundation",
    display_name={"th": "ข้อความเกี่ยวกับอะตอมนี้ตรงกับแบบจำลองใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelFoundation(QuestionType):
    """Match one fact to the model it belongs to."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        fact, model = rng.choice(MODEL_ONLY_FACTS)
        return GeneratedQuestion(
            stem=[text(f"ข้อความ \"{fact}\" กล่าวถึงแบบจำลองอะตอมใด")],
            correct=[text(model)],
            distractors=label_pool(list(MODEL_CHOICES)),
            topic=TOPIC_MODEL,
            hint=[text("แบบจำลองของโบร์กำหนดเส้นทางและระดับพลังงานของอิเล็กตรอนไว้แน่นอน "
                       "ส่วนแบบจำลองกลุ่มหมอกบอกได้เพียงโอกาสพบอิเล็กตรอน")],
        )


@question_type(
    "chem.atomic_model_fluency",
    display_name={"th": "ความแตกต่างระหว่างแบบจำลองอะตอมของโบร์กับแบบกลุ่มหมอก"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelFluency(QuestionType):
    """State the difference between the two models, not just one fact."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(MODEL_COMPARISONS)
        return GeneratedQuestion(
            stem=[text(stem)],
            correct=[text(correct)],
            distractors=label_pool([correct, *wrongs]),
            topic=TOPIC_MODEL,
            hint=[text("จุดต่างหลักคือแบบจำลองใดกำหนดเส้นทางของอิเล็กตรอนไว้แน่นอน "
                       "และแบบจำลองใดบอกได้เพียงโอกาสพบอิเล็กตรอน")],
        )


@question_type(
    "chem.atomic_model_application",
    display_name={"th": "สถานการณ์การสังเกตแบบจำลองอะตอม"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelApplication(QuestionType):
    """A described observation, not a bare fact — say which model it matches."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        scenario, model = rng.choice(MODEL_SCENARIOS)
        return GeneratedQuestion(
            stem=[text(f"{scenario} ข้อสังเกตนี้สอดคล้องกับแบบจำลองอะตอมใด")],
            correct=[text(model)],
            distractors=label_pool(list(MODEL_CHOICES)),
            topic=TOPIC_MODEL,
            hint=[text("มองหาว่าข้อสังเกตพูดถึงเส้นทางที่แน่นอนของอิเล็กตรอน (โบร์) "
                       "หรือพูดถึงโอกาสพบอิเล็กตรอนเป็นกลุ่มหมอก (กลุ่มหมอก)")],
        )

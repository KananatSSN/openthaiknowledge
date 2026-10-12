"""การวัดแรงด้วยเครื่องชั่งสปริง

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.5/3

Sets moved here from: science_wave_d16.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d16 import FIFTH

PROVENANCE = Provenance("original")


SPRING_TOPIC = "การวัดแรงด้วยเครื่องชั่งสปริง"


SPRING_FACTS = (
    ("แรงที่วัดด้วยเครื่องชั่งสปริงมีหน่วยใด", "นิวตัน",
     ("กิโลกรัม", "เมตร", "ลิตร", "องศาเซลเซียส", "วินาที")),
    ("ก่อนใช้เครื่องชั่งสปริงวัดแรงดึงในแนวราบ ควรทำอย่างไร", "วางเครื่องชั่งในแนวราบแล้วตรวจว่าเข็มชี้ที่ศูนย์",
     ("ดึงสปริงให้ยืดสุดก่อนแล้วจึงเริ่มวัดแรงดึง", "แขวนของหนักไว้ก่อน", "ไม่ต้องตรวจเข็ม เพราะเครื่องชั่งตั้งศูนย์มาจากโรงงานแล้ว", "ถือในแนวดิ่งแล้วตั้งศูนย์เท่านั้น", "ทาน้ำมันที่สปริง")),
    ("ขณะวัดแรงดึงกล่อง ควรดึงเครื่องชั่งสปริงอย่างไร", "ดึงในแนวเดียวกับทิศที่ต้องการให้กล่องเคลื่อนที่อย่างสม่ำเสมอ",
     ("กระตุกแรง ๆ", "ดึงเฉียงขึ้นมาก ๆ", "ดึงสลับไปมา", "ดึงแล้วปล่อยทันที", "บิดเครื่องชั่งขณะดึง")),
    ("เครื่องชั่งสปริงวัดแรงได้เพราะอะไร", "สปริงยืดออกมากขึ้นเมื่อแรงดึงมากขึ้น",
     ("สปริงหดเมื่อแรงมากขึ้น", "สปริงร้อนขึ้นตามแรง", "สปริงเปลี่ยนสีตามขนาดของแรงดึง", "เข็มหมุนเองตามเวลาที่ดึงค้างไว้", "สปริงดูดแรงไว้ภายในแล้วค่อย ๆ ปล่อยออก")),
    ("ถ้าเข็มเครื่องชั่งสปริงเลยขีดสูงสุด ควรทำอย่างไร", "หยุดดึงแล้วเปลี่ยนไปใช้เครื่องชั่งที่วัดได้มากกว่า",
     ("ดึงต่อไปจนกล่องขยับแล้วประมาณค่าเกินขีดเอง", "อ่านค่าเป็นค่าสูงสุดของเครื่องชั่งแล้วบันทึกไว้เป็นคำตอบ", "เดาค่าเอง", "ดึงแรงขึ้นอีก", "ไม่ต้องทำอะไร")),
)


SPRING_SCENARIOS = (
    ("เครื่องชั่งสปริงสองอันเกี่ยวกันแล้วดึงคนละข้าง อันหนึ่งอ่านได้ 6 นิวตัน อีกอันน่าจะอ่านได้เท่าใดถ้าทั้งสองอยู่นิ่ง",
     "6 นิวตัน", ("12 นิวตัน", "3 นิวตัน", "0 นิวตัน")),
    ("นักเรียนต้องการเปรียบเทียบแรงที่ใช้เปิดลิ้นชักสองใบให้ยุติธรรม ควรทำอย่างไร",
     "ใช้เครื่องชั่งสปริงอันเดียวกัน ดึงในแนวเดียวกันอย่างสม่ำเสมอ และอ่านค่าขณะลิ้นชักเริ่มเลื่อน",
     ("ใช้มือดึงแล้วเดาว่าอันไหนหนักกว่า", "ดึงลิ้นชักแรกช้า ๆ และลิ้นชักที่สองกระตุกแรง ๆ", "ดึงลิ้นชักแรกในแนวราบ ลิ้นชักที่สองในแนวเฉียง")),
    ("เครื่องชั่งสปริงอันหนึ่งวัดได้สูงสุด 5 นิวตัน นักเรียนลากกล่องแล้วเข็มชี้เกินขีดสูงสุด ข้อใดควรทำ",
     "หยุดดึงทันทีแล้วเปลี่ยนไปใช้เครื่องชั่งสปริงที่วัดได้มากกว่า",
     ("ดึงต่อจนกล่องเคลื่อนที่แล้วประมาณค่า", "อ่านว่าแรงเท่ากับ 5 นิวตันพอดี", "ใช้เครื่องชั่งสปริงสองอันต่อกันเป็นเส้นตรงแล้วบวกค่า")),
)


@question_type(
    "phys.spring_scale_force_foundation",
    display_name={"th": "ใช้เครื่องชั่งสปริงวัดแรงดึงอย่างถูกวิธี"},
    level=FIFTH, subject=SUBJECT, topic=SPRING_TOPIC,
)
class SpringScaleForceFoundation(QuestionType):
    """How to measure a pulling force with a spring scale, and reading one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            stem, right, wrongs = rng.choice(SPRING_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             hint="ดึงในทิศเดียวกับที่ต้องการวัดแรงอย่างสม่ำเสมอ และแรงมีหน่วยนิวตัน", topic=SPRING_TOPIC)
        if roll < 0.75:
            step = rng.choice((0.5, 1, 2, 5))
            marks = rng.randint(2, 12)
            thing = rng.choice(("ลิ้นชัก", "กล่องบนพื้น", "ประตูตู้", "รถของเล่น", "กระเป๋าล้อลาก"))
            value = step * marks
            wrongs = [marks, value + step, value * 2, value + 1, value + 2, value + 3]
            return _labelled(
                stem=(f"ใช้เครื่องชั่งสปริงที่มีขีดห่างกันขีดละ {step:g} นิวตัน ดึง{thing} เข็มเลื่อนจากศูนย์ไป {marks} ขีด "
                      "แรงดึงเท่าใด"),
                correct=f"{value:g} นิวตัน",
                wrongs=tuple(f"{w:g} นิวตัน" for w in dict.fromkeys(wrongs) if w != value)[:3],
                hint="แรง = จำนวนขีดที่เข็มเลื่อน × ค่าของหนึ่งขีด",
                topic=SPRING_TOPIC,
            )
        return _labelled(
            stem=rng.choice(("นักเรียนต้องการวัดแรงที่ใช้ลากกล่องบนพื้น ควรใช้เครื่องชั่งสปริงอย่างไร",
                             "ข้อใดเป็นวิธีวัดแรงดึงด้วยเครื่องชั่งสปริงที่ถูกต้อง")),
            correct="เกี่ยวเครื่องชั่งกับกล่อง ดึงขนานกับพื้นอย่างสม่ำเสมอ แล้วอ่านค่าเป็นนิวตัน",
            wrongs=("ดึงเครื่องชั่งสปริงขึ้นในแนวดิ่งแล้วอ่านค่าเป็นกิโลกรัม ขณะกล่องวางบนพื้น",
                    "กระตุกเครื่องชั่งสปริงแรง ๆ แล้วอ่านค่าสูงสุดที่เห็น",
                    "วางเครื่องชั่งสปริงไว้บนกล่องแล้วอ่านค่า"),
            hint="ดึงในทิศเดียวกับที่ต้องการวัดแรงอย่างสม่ำเสมอ และแรงมีหน่วยนิวตัน",
            topic=SPRING_TOPIC,
        )


@question_type(
    "phys.spring_scale_force_fluency",
    display_name={"th": "อ่านค่าแรงจากเครื่องชั่งสปริงในการทดลอง"},
    level=FIFTH, subject=SUBJECT, topic=SPRING_TOPIC,
)
class SpringScaleForceFluency(QuestionType):
    """Two readings; the larger force and by how much."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rough, smooth = sorted(rng.sample(range(2, 15), 2), reverse=True)
        return _labelled(
            stem=(f"นักเรียนใช้เครื่องชั่งสปริงลากกล่องใบเดียวกันอย่างสม่ำเสมอ บนพื้นพรมอ่านได้ {rough} นิวตัน "
                  f"และบนพื้นกระเบื้องอ่านได้ {smooth} นิวตัน ข้อใดถูกต้อง"),
            correct=f"การลากบนพื้นพรมใช้แรงมากกว่า {rough - smooth} นิวตัน",
            wrongs=(f"การลากบนพื้นกระเบื้องใช้แรงมากกว่า {rough - smooth} นิวตัน",
                    f"การลากบนพื้นพรมใช้แรงมากกว่า {rough + smooth} นิวตัน",
                    "ใช้แรงเท่ากัน เพราะเป็นกล่องใบเดียวกัน",
                    # The wrong floor and the wrong amount.
                    f"การลากบนพื้นกระเบื้องใช้แรงมากกว่า {rough + smooth} นิวตัน"),
            hint="ค่าที่อ่านได้มากกว่าแสดงว่าใช้แรงมากกว่า แล้วหาผลต่างของสองค่า",
            topic=SPRING_TOPIC,
        )


@question_type(
    "phys.spring_scale_force_application",
    display_name={"th": "วางแผนและตรวจการวัดแรงด้วยเครื่องชั่งสปริง"},
    level=FIFTH, subject=SUBJECT, topic=SPRING_TOPIC,
)
class SpringScaleForceApplication(QuestionType):
    """Authored cases, two hooked scales, and choosing a scale for a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            reading = rng.randint(2, 20)
            return _labelled(
                stem=(f"เครื่องชั่งสปริงสองอันเกี่ยวกันแล้วดึงคนละข้าง อันหนึ่งอ่านได้ {reading} นิวตัน "
                      "อีกอันน่าจะอ่านได้เท่าใดถ้าทั้งสองอยู่นิ่ง"),
                correct=f"{reading} นิวตัน",
                wrongs=(f"{reading * 2} นิวตัน", "0 นิวตัน", f"{reading + 1} นิวตัน"),
                hint="ทั้งสองอยู่นิ่ง แรงดึงทั้งสองข้างจึงต้องเท่ากัน",
                topic=SPRING_TOPIC,
            )
        if roll < 0.65:
            scales = sorted(rng.sample((5, 10, 20, 50, 100), 3))
            job = rng.randint(scales[0] + 1, scales[2] - 1)
            fit = next(c for c in scales if c > job)
            return _labelled(
                stem=(f"มีเครื่องชั่งสปริงที่วัดได้สูงสุด {scales[0]}, {scales[1]} และ {scales[2]} นิวตัน "
                      f"ต้องการวัดแรงลากกล่องซึ่งคาดว่าประมาณ {job} นิวตัน ควรเลือกเครื่องใดจึงเหมาะที่สุด"),
                correct=f"เครื่องที่วัดได้สูงสุด {fit} นิวตัน",
                wrongs=tuple(f"เครื่องที่วัดได้สูงสุด {c} นิวตัน" for c in scales if c != fit) + ("เครื่องใดก็ได้ เพราะวัดแรงเหมือนกัน",),
                hint="เลือกเครื่องที่วัดได้มากกว่าแรงที่คาด แต่ไม่มากเกินไป เพื่อให้อ่านค่าได้ละเอียด",
                topic=SPRING_TOPIC,
            )
        return _retopic(scenario_question(
            rng, SPRING_SCENARIOS,
            hint="ใช้เครื่องชั่งที่เหมาะกับขนาดแรง ดึงอย่างสม่ำเสมอในแนวเดียวกัน และเปรียบเทียบอย่างยุติธรรม",
        ), SPRING_TOPIC)

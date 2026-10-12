"""การวัดน้ำหนักด้วยเครื่องชั่งสปริง

ฟิสิกส์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.4/2

Sets moved here from: science_wave_d15.
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
from otk.sets._support.science_wave_d15 import FOURTH

PROVENANCE = Provenance("original")


SCALE_TOPIC = "การวัดน้ำหนักด้วยเครื่องชั่งสปริง"


SCALE_SCENARIOS = (
    ("นักเรียนแขวนถุงส้มกับเครื่องชั่งสปริงได้ 12 นิวตัน เมื่อหยิบส้มออกไปครึ่งถุง ค่าที่อ่านได้น่าจะเป็นเท่าใด โดยประมาณ",
     "ประมาณ 6 นิวตัน", ("ประมาณ 12 นิวตัน", "ประมาณ 24 นิวตัน", "0 นิวตัน")),
    ("เครื่องชั่งสปริงวัดได้สูงสุด 10 นิวตัน นักเรียนต้องการชั่งกระเป๋าที่คาดว่าหนักประมาณ 30 นิวตัน ควรทำอย่างไร",
     "เลือกเครื่องชั่งสปริงที่วัดได้มากกว่า 30 นิวตัน เพื่อไม่ให้สปริงเสียและอ่านค่าได้",
     ("ดึงสปริงให้ยืดเกินขีดสูงสุดแล้วประมาณค่า",
      "ชั่งด้วยเครื่องเดิมแล้วคูณด้วย 3",
      "ใช้ไม้บรรทัดวัดความยาวกระเป๋าแทน")),
    ("นักเรียนสองคนชั่งกล่องใบเดียวกัน คนแรกได้ 8 นิวตัน คนที่สองได้ 9 นิวตันเพราะเข็มไม่อยู่ที่ศูนย์ก่อนแขวน ข้อใดน่าจะถูกต้อง",
     "เข็มของเครื่องชั่งคนที่สองชี้ที่ 1 นิวตันก่อนแขวน น้ำหนักจริงจึงประมาณ 8 นิวตัน",
     ("กล่องหนัก 17 นิวตัน", "น้ำหนักจริงคือ 9 นิวตันเสมอ", "กล่องเปลี่ยนน้ำหนักระหว่างชั่ง")),
)


@question_type(
    "phys.spring_scale_weight_foundation",
    display_name={"th": "ใช้เครื่องชั่งสปริงอย่างถูกวิธี"},
    level=FOURTH, subject=SUBJECT, topic=SCALE_TOPIC,
)
class SpringScaleWeightFoundation(QuestionType):
    """The right step when weighing with a spring scale."""

    STEPS = (
        ("ก่อนแขวนวัตถุ ควรทำอย่างไรกับเครื่องชั่งสปริง",
         "ตรวจให้เข็มชี้ที่ศูนย์ ถ้าไม่ตรงให้ปรับก่อน",
         ("แขวนวัตถุทันทีโดยไม่ต้องดูเข็ม", "ดึงสปริงให้ยืดสุดก่อนทุกครั้ง", "ถอดสปริงออกมาทำความสะอาด")),
        ("ขณะอ่านค่าน้ำหนัก ควรทำอย่างไร",
         "ถือเครื่องชั่งให้ตั้งตรง รอให้วัตถุนิ่ง แล้วมองระดับสายตาตรงกับเข็ม",
         ("แกว่งเครื่องชั่งให้วัตถุเคลื่อนที่ก่อนอ่าน", "มองจากด้านล่างเครื่องชั่ง", "ถือเครื่องชั่งเอียง 45 องศา")),
        ("น้ำหนักที่อ่านได้จากเครื่องชั่งสปริงมีหน่วยใด",
         "นิวตัน",
         ("กิโลกรัม", "เซนติเมตร", "ลิตร")),
        ("ก่อนชั่ง ควรตรวจสิ่งใดของเครื่องชั่งสปริงเทียบกับวัตถุที่จะชั่ง",
         "ค่าสูงสุดที่เครื่องชั่งวัดได้ต้องมากกว่าน้ำหนักของวัตถุ",
         ("สีของเครื่องชั่งต้องเข้ากับวัตถุ", "เครื่องชั่งต้องมีน้ำหนักมากกว่าวัตถุที่นำมาชั่งเสมอ", "สปริงต้องยืดอยู่ก่อนแล้ว")),
        ("เครื่องชั่งสปริงวัดน้ำหนักได้เพราะอะไร",
         "สปริงยืดออกตามน้ำหนักที่แขวน ยิ่งหนักสปริงยิ่งยืดมาก",
         ("สปริงหดสั้นลงเมื่อแขวนของหนัก", "สปริงเปลี่ยนสีตามน้ำหนัก", "เข็มเลื่อนเองโดยไม่เกี่ยวกับสปริง แม้ไม่ได้แขวนวัตถุ")),
        ("หลังชั่งเสร็จ ควรทำอย่างไรกับเครื่องชั่งสปริง",
         "ปลดวัตถุออกและตรวจว่าเข็มกลับมาที่ศูนย์",
         ("แขวนวัตถุค้างไว้ตลอดเวลาหลังใช้งาน", "ดึงสปริงให้ยืดทิ้งไว้จนกว่าจะใช้ครั้งต่อไป", "นำไปแช่น้ำ")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            capacity = rng.choice((5, 10, 20, 50, 100))
            weight = rng.choice([w for w in range(2, 3 * capacity, max(1, capacity // 5)) if w != capacity])
            ok = weight < capacity
            thing = rng.choice(("ถุงส้ม", "กระเป๋านักเรียน", "ถุงทราย", "กล่องดินสอ", "ถุงข้าวสาร", "หนังสือ"))
            return _labelled(
                stem=f"เครื่องชั่งสปริงวัดได้สูงสุด {capacity} นิวตัน ต้องการชั่ง{thing}ที่หนักประมาณ {weight} นิวตัน ควรทำอย่างไร",
                correct=("ชั่งด้วยเครื่องนี้ได้ เพราะน้ำหนักไม่เกินค่าสูงสุด" if ok
                         else "เปลี่ยนไปใช้เครื่องชั่งที่วัดได้มากกว่า เพราะน้ำหนักเกินค่าสูงสุด"),
                wrongs=(("เปลี่ยนไปใช้เครื่องชั่งที่วัดได้มากกว่า เพราะน้ำหนักเกินค่าสูงสุด" if ok
                         else "ชั่งด้วยเครื่องนี้ได้ เพราะน้ำหนักไม่เกินค่าสูงสุด"),
                        "ดึงสปริงให้ยืดเกินขีดสูงสุดแล้วประมาณค่าเอาจากระยะที่ยืดออกไป", "ใช้ไม้บรรทัดวัดขนาดแทนการชั่ง"),
                hint="เลือกเครื่องชั่งที่ค่าสูงสุดมากกว่าน้ำหนักของวัตถุ เพื่อไม่ให้สปริงเสีย",
                topic=SCALE_TOPIC,
            )
        stem, right, wrongs = rng.choice(self.STEPS)
        return _labelled(stem=stem, correct=right, wrongs=wrongs,
                         hint="เข็มต้องเริ่มที่ศูนย์ วัตถุต้องนิ่ง และน้ำหนักมีหน่วยนิวตัน",
                         topic=SCALE_TOPIC)


@question_type(
    "phys.spring_scale_weight_fluency",
    display_name={"th": "อ่านค่าน้ำหนักจากเครื่องชั่งสปริง"},
    level=FOURTH, subject=SUBJECT, topic=SCALE_TOPIC,
)
class SpringScaleWeightFluency(QuestionType):
    """A scale's divisions and the needle's position; the weight it reads."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step = rng.choice((1, 2, 5, 10))
        marks = rng.randint(3, 12)
        weight = step * marks
        slips = (marks, weight + step, weight - step, step * (marks + 2))
        wrongs = [w for w in dict.fromkeys(slips) if w != weight and w > 0][:3]
        return _labelled(
            stem=(f"เครื่องชั่งสปริงมีขีดสเกลห่างกันขีดละ {step} นิวตัน เมื่อแขวนวัตถุ เข็มเลื่อนจากศูนย์ลงมา "
                  f"{marks} ขีดพอดี วัตถุมีน้ำหนักเท่าใด"),
            correct=f"{weight} นิวตัน",
            wrongs=tuple(f"{w} นิวตัน" for w in wrongs),
            hint="น้ำหนัก = จำนวนขีดที่เข็มเลื่อน × ค่าของหนึ่งขีด",
            topic=SCALE_TOPIC,
        )


@question_type(
    "phys.spring_scale_weight_application",
    display_name={"th": "ตรวจสอบและวางแผนการชั่งน้ำหนักด้วยเครื่องชั่งสปริง"},
    level=FOURTH, subject=SUBJECT, topic=SCALE_TOPIC,
)
class SpringScaleWeightApplication(QuestionType):
    """Authored cases, a needle off zero, and a bag with part of its load taken out."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            offset = rng.randint(1, 3)
            reading = rng.randint(3 * offset + 1, 25)  # keeps the four choices apart
            return _labelled(
                stem=(f"ก่อนแขวนวัตถุ เข็มของเครื่องชั่งสปริงชี้ที่ {offset} นิวตัน ไม่ใช่ศูนย์ เมื่อแขวนวัตถุ อ่านได้ {reading} นิวตัน "
                      "วัตถุหนักจริงประมาณเท่าใด"),
                correct=f"{reading - offset} นิวตัน",
                wrongs=(f"{reading} นิวตัน", f"{reading + offset} นิวตัน", f"{offset} นิวตัน"),
                hint="ค่าที่อ่านได้รวมค่าที่เข็มค้างอยู่ก่อนแขวน จึงต้องลบค่านั้นออก",
                topic=SCALE_TOPIC,
            )
        if roll < 0.7:
            each = rng.randint(1, 5)
            count = rng.randint(4, 12)
            taken = rng.randint(1, count - 1)
            thing = rng.choice(("ส้ม", "แอปเปิล", "ก้อนหิน", "ขวดน้ำ", "หนังสือ"))
            return _labelled(
                stem=(f"แขวนถุงที่ใส่{thing} {count} ชิ้น ชิ้นละ {each} นิวตัน กับเครื่องชั่งสปริง (ไม่คิดน้ำหนักถุง) "
                      f"ถ้าหยิบ{thing}ออก {taken} ชิ้น เครื่องชั่งจะอ่านได้เท่าใด"),
                correct=f"{each * (count - taken)} นิวตัน",
                wrongs=tuple(f"{w} นิวตัน" for w in dict.fromkeys((each * count, each * taken, count - taken,
                                                                    each * (count - taken) + each,
                                                                    each * (count - taken) + 2 * each, each * count + each))
                             if w != each * (count - taken))[:3],
                hint="น้ำหนักที่เหลือ = จำนวนชิ้นที่เหลือ × น้ำหนักต่อชิ้น",
                topic=SCALE_TOPIC,
            )
        return _retopic(scenario_question(
            rng, SCALE_SCENARIOS,
            hint="ตรวจว่าเครื่องชั่งเหมาะกับน้ำหนักและเริ่มที่ศูนย์ แล้วจึงแปลค่าที่อ่านได้",
        ), SCALE_TOPIC)

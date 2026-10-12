"""แรงโน้มถ่วงกับการเคลื่อนที่ของวัตถุรอบโลก

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/6

Sets moved here from: science_wave_e11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e11 import SUBJECT, UPPER_FIVE, G, _labelled, _numeric, show

PROVENANCE = Provenance("original")


TOPIC_ORBIT = "แรงโน้มถ่วงกับการเคลื่อนที่ของวัตถุรอบโลก"


ORBIT_FACTS = (
    ("แรงใดทำให้ดาวเทียมเคลื่อนที่เป็นวงกลมรอบโลกได้",
     "แรงโน้มถ่วงที่โลกดึงดาวเทียม ซึ่งทำหน้าที่เป็นแรงสู่ศูนย์กลาง",
     ("แรงจากเครื่องยนต์ของดาวเทียมที่ทำงานตลอดเวลา", "แรงลอยตัวของอากาศในอวกาศ",
      "แรงแม่เหล็กของโลกเพียงอย่างเดียว")),
    ("นักบินอวกาศในสถานีอวกาศที่โคจรรอบโลกรู้สึกไร้น้ำหนักเพราะเหตุใด",
     "นักบินอวกาศและสถานีตกเข้าหาโลกพร้อมกันด้วยความเร่งเท่ากัน",
     ("ในอวกาศไม่มีแรงโน้มถ่วงของโลกเลย นักบินอวกาศจึงลอยได้", "สถานีอวกาศอยู่ไกลจนโลกไม่ดึงดูดแล้ว ทุกอย่างในสถานีจึงลอย",
      "นักบินอวกาศมีมวลเป็นศูนย์เมื่ออยู่นอกโลก จึงไม่มีน้ำหนัก")),
    ("ดาวเทียมค้างฟ้า (ดาวเทียมสื่อสาร) อยู่เหนือตำแหน่งเดิมบนโลกตลอดเวลาได้อย่างไร",
     "ดาวเทียมโคจรรอบโลกหนึ่งรอบในเวลาเท่ากับที่โลกหมุนรอบตัวเองหนึ่งรอบ ในทิศเดียวกัน",
     ("ดาวเทียมหยุดนิ่งอยู่กับที่ในอวกาศ", "ดาวเทียมอยู่ไกลจนแรงโน้มถ่วงเป็นศูนย์",
      "ดาวเทียมใช้เครื่องยนต์ต้านแรงโน้มถ่วงไว้ตลอดเวลา")),
    ("ถ้าดาวเทียมโคจรอยู่ใกล้โลกมากขึ้น แรงโน้มถ่วงที่โลกดึงดาวเทียมจะเป็นอย่างไร",
     "มากขึ้น เพราะแรงโน้มถ่วงลดลงเมื่อระยะห่างเพิ่มขึ้น",
     ("น้อยลง เพราะดาวเทียมเคลื่อนที่เร็วขึ้น", "เท่าเดิม เพราะมวลของดาวเทียมเท่าเดิม",
      "เป็นศูนย์ เพราะดาวเทียมอยู่ในอวกาศ")),
    ("ดวงจันทร์ไม่ตกลงสู่โลกแม้โลกดึงดูดดวงจันทร์ตลอดเวลา เพราะเหตุใด",
     "ดวงจันทร์มีความเร็วในแนวสัมผัสวงโคจร แรงโน้มถ่วงจึงเปลี่ยนเพียงทิศของความเร็วให้โคจรรอบโลก",
     ("ดวงจันทร์ดึงโลกด้วยแรงที่มากกว่า", "ระหว่างโลกกับดวงจันทร์ไม่มีแรงโน้มถ่วง",
      "แรงหนีศูนย์กลางของดวงจันทร์หักล้างแรงทุกแรงจนไม่มีแรงลัพธ์")),
)


# The true and false statements are kept to similar lengths, so length does not sort them.
ORBIT_TRUE = (
    "แรงโน้มถ่วงของโลกที่กระทำต่อดาวเทียมมีทิศเข้าหาศูนย์กลางโลก",
    "ความเร็วของดาวเทียมมีทิศตามแนวสัมผัสกับวงโคจรทุกขณะ",
    "ถ้าแรงโน้มถ่วงหายไป ดาวเทียมจะเคลื่อนที่เป็นเส้นตรงตามแนวสัมผัส",
    "ดาวเทียมที่โคจรใกล้โลกกว่าต้องเคลื่อนที่เร็วกว่าดาวเทียมที่ไกลกว่า",
    "นักบินอวกาศยังถูกโลกดึงดูด แต่ตกไปพร้อมสถานีจึงรู้สึกไร้น้ำหนัก",
    "วัตถุที่ขว้างในแนวระดับเร็วพอ จะตกโค้งไปรอบโลกจนเป็นการโคจร",
    "แรงโน้มถ่วงเป็นแรงสู่ศูนย์กลางของดวงจันทร์ที่โคจรรอบโลก",
    "ดาวเทียมค้างฟ้าโคจรรอบโลกหนึ่งรอบในเวลาประมาณหนึ่งวัน",
)


ORBIT_FALSE = (
    "ดาวเทียมโคจรได้เพราะในอวกาศไม่มีแรงโน้มถ่วงของโลกดึงดูดอยู่เลย",
    "ดาวเทียมต้องเปิดเครื่องยนต์ตลอดเวลาจึงจะโคจรรอบโลกอยู่ได้",
    "แรงโน้มถ่วงที่กระทำต่อดาวเทียมมีทิศตามทิศการเคลื่อนที่ในวงโคจร",
    "ดาวเทียมที่โคจรไกลโลกมากกว่าต้องเคลื่อนที่เร็วกว่าดาวเทียมที่ใกล้กว่า",
    "นักบินอวกาศในสถานีอวกาศไม่มีมวลเมื่ออยู่นอกโลก จึงลอยได้",
    "ถ้าแรงโน้มถ่วงหายไปทันที ดาวเทียมจะหยุดนิ่งอยู่กับที่ในวงโคจร",
    "ดวงจันทร์ไม่ตกลงสู่โลกเพราะโลกไม่ได้ดึงดูดดวงจันทร์เลย",
    "ดาวเทียมค้างฟ้าหยุดนิ่งอยู่ในอวกาศ ไม่ได้เคลื่อนที่รอบโลก",
)


WORLDS = (("ดวงจันทร์", Fraction(16, 10)), ("ดาวอังคาร", Fraction(37, 10)),
          ("ดาวพฤหัสบดี", Fraction(25)), ("ดาวพุธ", Fraction(37, 10)))


@question_type(
    "phys.gravity_orbit_foundation",
    display_name={"th": "แรงโน้มถ่วง น้ำหนัก และระยะห่าง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ORBIT,
)
class GravityOrbitFoundation(QuestionType):
    """The pieces the explanation needs: weight is mg, mass is not, and the pull fades with distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            m = rng.randint(3, 90)
            return _numeric(
                stem=f"วัตถุมวล {m} กิโลกรัมบนผิวโลก (g = 10 m/s²) มีน้ำหนักเท่าใด",
                answer=m * G, wrongs=[m, Fraction(m, G), m * G * 2], unit="นิวตัน",
                topic=TOPIC_ORBIT, hint="น้ำหนัก = มวล × ความเร่งโน้มถ่วง (W = mg)")
        if shape == 1:
            world, _ = rng.choice(WORLDS)
            m = rng.randint(3, 90)
            return _labelled(
                stem=f"นักบินอวกาศมีมวล {m} กิโลกรัมบนโลก เมื่อไปอยู่บน{world} ข้อใดถูกต้อง",
                correct=f"มวลยังเป็น {m} กิโลกรัม แต่น้ำหนักเปลี่ยนไป",
                wrongs=("มวลและน้ำหนักเปลี่ยนไปทั้งคู่", "น้ำหนักเท่าเดิม แต่มวลเปลี่ยนไป",
                        "มวลและน้ำหนักเท่าเดิมทั้งคู่"),
                topic=TOPIC_ORBIT,
                hint="มวลคือปริมาณเนื้อสารจึงคงที่ น้ำหนักคือแรงโน้มถ่วงที่กระทำต่อมวลจึงขึ้นกับสถานที่")
        k = rng.choice((2, 3, 4))
        return _labelled(
            stem=f"ถ้าระยะห่างระหว่างจุดศูนย์กลางของโลกกับดาวเทียมเพิ่มขึ้นเป็น {k} เท่า แรงโน้มถ่วงระหว่างกันจะเป็นอย่างไร",
            correct=f"ลดลงเหลือ 1/{k * k} เท่า",
            wrongs=(f"ลดลงเหลือ 1/{k} เท่า", f"เพิ่มขึ้นเป็น {k * k} เท่า", "เท่าเดิม"),
            topic=TOPIC_ORBIT,
            hint="แรงโน้มถ่วงแปรผกผันกับกำลังสองของระยะห่างระหว่างจุดศูนย์กลาง")


@question_type(
    "phys.gravity_orbit_fluency",
    display_name={"th": "อธิบายการเคลื่อนที่ของดาวเทียมและดวงจันทร์รอบโลกด้วยแรงโน้มถ่วง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ORBIT,
)
class GravityOrbitFluency(QuestionType):
    """The indicator's อธิบาย: gravity as the centripetal force of every orbit round the Earth."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "วัตถุที่โคจรรอบโลกยังถูกโลกดึงอยู่ แรงโน้มถ่วงคือแรงที่ดึงให้เส้นทางโค้งเป็นวงรอบโลก"
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(ORBIT_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_ORBIT, hint=hint)
        # One true explanation among three common wrong ones, drawn afresh.
        if rng.random() < 0.5:
            return _labelled(stem="ข้อใดอธิบายการเคลื่อนที่ของวัตถุรอบโลกได้ถูกต้อง",
                             correct=rng.choice(ORBIT_TRUE), wrongs=tuple(ORBIT_FALSE),
                             topic=TOPIC_ORBIT, hint=hint)
        return _labelled(stem="ข้อใดอธิบายการเคลื่อนที่ของวัตถุรอบโลกไม่ถูกต้อง",
                         correct=rng.choice(ORBIT_FALSE), wrongs=tuple(ORBIT_TRUE),
                         topic=TOPIC_ORBIT, hint=hint)


@question_type(
    "phys.gravity_orbit_application",
    display_name={"th": "คำนวณน้ำหนักบนดาวอื่นและแรงโน้มถ่วงเมื่อระยะห่างเปลี่ยน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ORBIT,
)
class GravityOrbitApplication(QuestionType):
    """Weight on another world, and the inverse-square law with numbers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            world, g = rng.choice(WORLDS)
            m = rng.randint(2, 20) * 5
            return _numeric(
                stem=(f"ยานสำรวจมีน้ำหนัก {m * G:,} นิวตันบนโลก (g = 10 m/s²) "
                      f"ถ้าความเร่งโน้มถ่วงบน{world}เท่ากับ {show(g)} m/s² ยานนี้มีน้ำหนักบน{world}เท่าใด"),
                answer=m * g, wrongs=[m * G, m, Fraction(m * G, g)], unit="นิวตัน",
                topic=TOPIC_ORBIT,
                hint="หามวลจากน้ำหนักบนโลกก่อน (m = W/g) มวลไม่เปลี่ยน แล้วคูณด้วย g ของดาวดวงนั้น")
        k = rng.choice((2, 3, 4, 5))
        f = rng.randint(1, 20) * k * k * 10
        closer = rng.random() < 0.5
        if closer:
            stem = (f"ดาวเทียมดวงหนึ่งถูกโลกดึงด้วยแรง {f:,} นิวตัน ถ้าย้ายไปโคจรที่ระยะห่างจากจุดศูนย์กลางโลก"
                    f"เพิ่มขึ้นเป็น {k} เท่าของเดิม แรงโน้มถ่วงที่โลกดึงดาวเทียมจะเป็นเท่าใด")
            answer, wrongs = Fraction(f, k * k), [Fraction(f, k), f * k, f * k * k]
        else:
            stem = (f"ดาวเทียมดวงหนึ่งถูกโลกดึงด้วยแรง {f:,} นิวตัน ถ้ามวลของดาวเทียมเพิ่มขึ้นเป็น {k} เท่า "
                    "โดยระยะห่างเท่าเดิม แรงโน้มถ่วงที่โลกดึงดาวเทียมจะเป็นเท่าใด")
            answer, wrongs = f * k, [Fraction(f, k), f * k * k, f]
        return _numeric(stem=stem, answer=answer, wrongs=wrongs, unit="นิวตัน", topic=TOPIC_ORBIT,
                        hint="แรงโน้มถ่วงแปรผันตรงกับผลคูณของมวล และแปรผกผันกับกำลังสองของระยะห่าง")

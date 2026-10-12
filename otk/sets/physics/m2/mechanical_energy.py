"""การเปลี่ยนพลังงานศักย์โน้มถ่วงและพลังงานจลน์โดยพลังงานกลคงตัว

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.2/5

Sets moved here from: science_wave_d31.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d30 import SECOND_SECONDARY

PROVENANCE = Provenance("original")


MECHANICAL_ENERGY_TOPIC = "การเปลี่ยนพลังงานศักย์โน้มถ่วงและพลังงานจลน์โดยพลังงานกลคงตัว"


SWINGS = ("ลูกตุ้มที่แกว่ง", "ลูกบอลที่ถูกโยนขึ้นตรง ๆ", "รถไฟเหาะบนราง", "เด็กที่เล่นชิงช้า", "นักสกีบนลาดเขา", "ลูกมะพร้าวที่หล่นจากต้น")


MECHANICAL_ENERGY_SCENARIOS = (
    ("รถไฟเหาะตีลูกอยู่ที่จุดสูงสุดของราง (เกือบหยุดนิ่ง) แล้วไถลลงมาถึงจุดต่ำสุดด้วยอัตราเร็วสูงมาก ข้อใดอธิบายการเปลี่ยนพลังงานนี้ได้ถูกต้อง",
     "พลังงานศักย์โน้มถ่วงที่จุดสูงสุดเปลี่ยนเป็นพลังงานจลน์ที่จุดต่ำสุด โดยพลังงานกลรวมคงตัวเมื่อไม่มีแรงเสียดทานมาก",
     ("พลังงานจลน์ที่จุดสูงสุดเปลี่ยนเป็นพลังงานศักย์ที่จุดต่ำสุด", "พลังงานกลรวมเพิ่มขึ้นเองระหว่างการไถลลง", "ไม่มีการเปลี่ยนรูปพลังงานใด ๆ เกิดขึ้นระหว่างการไถลลง")),
    ("ลูกตุ้มนาฬิกาแกว่งไปมา ที่จุดสูงสุดทั้งสองข้างลูกตุ้มหยุดนิ่งชั่วขณะ ข้อใดอธิบายพลังงานของลูกตุ้ม ณ จุดเหล่านั้นได้ถูกต้อง",
     "ที่จุดสูงสุดทั้งสองข้าง พลังงานจลน์เป็นศูนย์ (หยุดนิ่ง) และพลังงานศักย์โน้มถ่วงมีค่าสูงสุด",
     ("ที่จุดสูงสุดทั้งสองข้าง พลังงานจลน์มีค่าสูงสุดเพราะกำลังจะแกว่งกลับ", "พลังงานศักย์โน้มถ่วงเป็นศูนย์ที่จุดสูงสุดเสมอ", "ลูกตุ้มไม่มีพลังงานใด ๆ ขณะหยุดนิ่งชั่วขณะ")),
    ("นักสกีไถลจากยอดเขาลงมาถึงเชิงเขาโดยไม่มีการเสียดทานกับหิมะ อัตราเร็วที่เชิงเขาเทียบกับยอดเขาเป็นอย่างไร และเพราะเหตุใด",
     "อัตราเร็วที่เชิงเขามากกว่ามาก เพราะพลังงานศักย์โน้มถ่วงที่ยอดเขาทั้งหมดเปลี่ยนเป็นพลังงานจลน์ที่เชิงเขา",
     ("อัตราเร็วที่เชิงเขาน้อยกว่าที่ยอดเขา เพราะพลังงานศักย์โน้มถ่วงหายไป", "อัตราเร็วเท่ากันตลอดเส้นทางไม่ว่าความสูงจะเปลี่ยนไปเท่าใด", "พลังงานศักย์โน้มถ่วงไม่เกี่ยวข้องกับอัตราเร็วของนักสกีเลย")),
)


@question_type(
    "phys.mechanical_energy_foundation",
    display_name={"th": "แปลความหมายข้อมูลความสูงและอัตราเร็วของวัตถุที่แกว่งหรือตกลงมา"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=MECHANICAL_ENERGY_TOPIC,
)
class MechanicalEnergyFoundation(QuestionType):
    """Height down and speed up means Ep to Ek; the reverse means Ek to Ep."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        thing = rng.choice(SWINGS)
        falling = rng.random() < 0.5 or thing == "ลูกมะพร้าวที่หล่นจากต้น"
        h1, h2 = sorted(rng.sample(range(1, 21), 2), reverse=falling)
        v1, v2 = sorted(rng.sample(range(1, 21), 2), reverse=not falling)
        right = "พลังงานศักย์โน้มถ่วงลดลงขณะพลังงานจลน์เพิ่มขึ้น" if falling else "พลังงานจลน์ลดลงขณะพลังงานศักย์โน้มถ่วงเพิ่มขึ้น"
        other = "พลังงานจลน์ลดลงขณะพลังงานศักย์โน้มถ่วงเพิ่มขึ้น" if falling else "พลังงานศักย์โน้มถ่วงลดลงขณะพลังงานจลน์เพิ่มขึ้น"
        return _labelled(
            stem=(f"ข้อมูลของ{thing}: ตำแหน่งแรกสูง {h1} m อัตราเร็ว {v1} m/s ตำแหน่งถัดมาสูง {h2} m อัตราเร็ว {v2} m/s "
                  "ข้อใดแปลความหมายข้อมูลนี้ได้ถูกต้อง"),
            correct=right, wrongs=(other, "พลังงานทั้งสองชนิดลดลงพร้อมกัน", "พลังงานศักย์โน้มถ่วงและพลังงานจลน์ไม่มีความสัมพันธ์กัน"),
            hint="ความสูงลดลงหมายถึงพลังงานศักย์โน้มถ่วงลดลง อัตราเร็วเพิ่มขึ้นหมายถึงพลังงานจลน์เพิ่มขึ้น",
            topic=MECHANICAL_ENERGY_TOPIC,
        )


@question_type(
    "phys.mechanical_energy_fluency",
    display_name={"th": "อธิบายการเปลี่ยนพลังงานศักย์และพลังงานจลน์โดยพลังงานกลคงตัวจากข้อมูลที่รวบรวมได้"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=MECHANICAL_ENERGY_TOPIC,
)
class MechanicalEnergyFluency(QuestionType):
    """Two points on a frictionless path; Ep and Ek trade off while the total stays fixed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        total = rng.choice((100, 120, 150, 200, 240, 300, 400, 500, 600, 800, 1000))
        step = total // 20 if total % 20 == 0 else 10
        ke_a, ke_b = rng.sample(range(step, total, step), 2)
        pe_a, pe_b = total - ke_a, total - ke_b
        down = ke_b > ke_a
        place = "ซึ่งอยู่ต่ำกว่า" if down else "ซึ่งอยู่สูงกว่า"
        change = "พลังงานศักย์โน้มถ่วงเปลี่ยนเป็นพลังงานจลน์" if down else "พลังงานจลน์เปลี่ยนเป็นพลังงานศักย์โน้มถ่วง"
        reverse = "พลังงานจลน์เปลี่ยนเป็นพลังงานศักย์โน้มถ่วง" if down else "พลังงานศักย์โน้มถ่วงเปลี่ยนเป็นพลังงานจลน์"
        return _labelled(
            stem=(f"วัตถุเคลื่อนที่จากจุด A ไปยังจุด B {place} โดยไม่มีแรงเสียดทาน ข้อมูลพลังงานที่วัดได้คือ "
                  f"จุด A: พลังงานศักย์โน้มถ่วง {pe_a} จูล พลังงานจลน์ {ke_a} จูล / "
                  f"จุด B: พลังงานศักย์โน้มถ่วง {pe_b} จูล พลังงานจลน์ {ke_b} จูล "
                  "จากข้อมูลนี้ ข้อใดอธิบายการเปลี่ยนพลังงานได้ถูกต้อง"),
            correct=f"{change} โดยพลังงานกล (ผลรวมของทั้งสอง) คงตัวเท่ากับ {total} จูลทั้งสองจุด",
            wrongs=(f"{reverse} โดยพลังงานกล (ผลรวมของทั้งสอง) คงตัวเท่ากับ {total} จูลทั้งสองจุด",
                    f"พลังงานกลรวมที่จุด B {'มากกว่า' if down else 'น้อยกว่า'}ที่จุด A เพราะพลังงานจลน์{'เพิ่มขึ้น' if down else 'ลดลง'} "
                    "โดยพลังงานศักย์โน้มถ่วงคงเดิม",
                    "พลังงานศักย์โน้มถ่วงและพลังงานจลน์ไม่มีความสัมพันธ์กันเลยในสถานการณ์นี้"),
            hint="รวมพลังงานศักย์โน้มถ่วงกับพลังงานจลน์ที่จุดแต่ละจุด แล้วเทียบว่าผลรวมเปลี่ยนไปหรือไม่",
            topic=MECHANICAL_ENERGY_TOPIC,
        )


@question_type(
    "phys.mechanical_energy_application",
    display_name={"th": "ใช้หลักพลังงานกลคงตัวอธิบายสถานการณ์การเคลื่อนที่จริง"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=MECHANICAL_ENERGY_TOPIC,
)
class MechanicalEnergyApplication(QuestionType):
    """Authored scenes, Ek at a lower point, and Ek at the ground from Ep = mgh."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            return _retopic(scenario_question(
                rng, MECHANICAL_ENERGY_SCENARIOS,
                hint="ไม่มีแรงเสียดทาน พลังงานกลรวม (ศักย์ + จลน์) คงตัวเสมอ แม้แต่ละส่วนจะเปลี่ยนแปลงไป",
            ), MECHANICAL_ENERGY_TOPIC)
        thing = rng.choice(("รถไฟเหาะ", "ลูกตุ้ม", "เด็กบนสไลเดอร์", "กล่องบนรางลื่น"))
        if roll < 0.6:
            top = rng.randrange(200, 2001, 50)
            lower = rng.randrange(0, top, 50)
            return numeric(stem=f"{thing}เริ่มหยุดนิ่งที่จุดสูงสุดซึ่งมีพลังงานศักย์โน้มถ่วง {show(top)} จูล ไม่มีแรงเสียดทาน "
                                f"เมื่อถึงจุดที่มีพลังงานศักย์โน้มถ่วง {show(lower)} จูล จะมีพลังงานจลน์กี่จูล",
                           answer=top - lower, wrongs=[top + lower, lower if lower else top // 2, top], unit="จูล", topic=MECHANICAL_ENERGY_TOPIC,
                           hint="พลังงานกลคงตัว: พลังงานจลน์ = พลังงานกลทั้งหมด − พลังงานศักย์โน้มถ่วง ณ จุดนั้น")
        mass = rng.choice((1, 2, 3, 4, 5, 10, 20, 50))
        height = rng.choice((2, 3, 5, 8, 10, 12, 15, 20))
        return numeric(stem=f"ปล่อยวัตถุมวล {mass} kg จากที่สูง {height} m (g = 10 N/kg ไม่คิดแรงต้านอากาศ) ขณะกระทบพื้นวัตถุมีพลังงานจลน์กี่จูล",
                       answer=10 * mass * height, wrongs=[mass * height, Fraction(10 * mass * height, 2), 10 * mass + height], unit="จูล",
                       topic=MECHANICAL_ENERGY_TOPIC, hint="พลังงานศักย์โน้มถ่วงตอนเริ่ม Ep = mgh เปลี่ยนเป็นพลังงานจลน์ทั้งหมดเมื่อถึงพื้น")

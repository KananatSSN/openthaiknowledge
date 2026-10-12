"""แรงลัพธ์กับการเคลื่อนที่

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/1

Sets moved here from: science_wave_d18.
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
from otk.sets._support.science_wave_d18 import SECONDARY_TWO, _facts

PROVENANCE = Provenance("original")


MOTION_TOPIC = "แรงลัพธ์กับการเคลื่อนที่"


RIGHT, LEFT = "ทางขวา", "ทางซ้าย"


AT_REST, MOVING_RIGHT = "อยู่นิ่ง", "กำลังเคลื่อนที่ไปทางขวา"


def predict(start: str, net: int) -> str:
    """What follows, for a resultant ``net`` (positive to the right)."""
    if net == 0:
        return "อยู่นิ่งต่อไป" if start == AT_REST else "เคลื่อนที่ไปทางขวาด้วยความเร็วคงที่"
    if start == AT_REST:
        return f"เริ่มเคลื่อนที่ไป{RIGHT if net > 0 else LEFT} โดยเร็วขึ้นเรื่อย ๆ"
    return "เคลื่อนที่ไปทางขวาเร็วขึ้นเรื่อย ๆ" if net > 0 else "เคลื่อนที่ไปทางขวาช้าลง"


MOVERS = ("รถเข็น", "ลูกบอล", "กล่อง", "รถของเล่น", "สเก็ตบอร์ด", "เรือเล็ก")


MOTION_HINT = "แรงลัพธ์เป็นศูนย์ วัตถุคงสภาพเดิม แรงลัพธ์ทิศเดียวกับการเคลื่อนที่ทำให้เร็วขึ้น ทิศตรงข้ามทำให้ช้าลง"


def motion_after(start: str, net: str) -> str:
    """``start`` is at rest or moving one way; ``net`` is ``zero`` or the resultant's side."""
    if start == "อยู่นิ่ง":
        return "อยู่นิ่งต่อไป" if net == "zero" else f"เริ่มเคลื่อนที่ไป{net} โดยเร็วขึ้นเรื่อย ๆ"
    side = start.removeprefix("กำลังเคลื่อนที่ไป")
    if net == "zero":
        return f"เคลื่อนที่ไป{side}ด้วยความเร็วคงที่"
    return f"เคลื่อนที่ไป{side}เร็วขึ้นเรื่อย ๆ" if net == side else f"เคลื่อนที่ไป{side}ช้าลง"


MOTION_FACTS = (
    ("วัตถุที่เคลื่อนที่ด้วยความเร็วคงที่ในแนวตรง มีแรงลัพธ์กระทำเท่าใด", "แรงลัพธ์เป็นศูนย์",
     ("แรงลัพธ์มีทิศเดียวกับการเคลื่อนที่", "แรงลัพธ์มีทิศตรงข้ามกับการเคลื่อนที่", "แรงลัพธ์มีค่ามากที่สุด",
      "แรงลัพธ์ชี้ลงในแนวดิ่งเสมอ", "แรงลัพธ์เท่ากับน้ำหนักของวัตถุ")),
    ("แรงลัพธ์หมายถึงสิ่งใด", "ผลรวมของแรงทุกแรงที่กระทำต่อวัตถุโดยคิดทั้งขนาดและทิศทาง",
     ("แรงที่มีขนาดมากที่สุดเพียงแรงเดียว", "ผลรวมขนาดของแรงทุกแรงโดยไม่คิดทิศทาง", "แรงที่กระทำต่อวัตถุเป็นแรงแรก",
      "ผลต่างระหว่างน้ำหนักกับมวลของวัตถุ", "แรงที่วัตถุออกแรงกระทำต่อพื้น")),
    ("วัตถุที่อยู่นิ่งจะเริ่มเคลื่อนที่ได้เมื่อใด", "เมื่อมีแรงลัพธ์ที่ไม่เป็นศูนย์มากระทำ",
     ("เมื่อแรงลัพธ์เป็นศูนย์", "เมื่อมีแรงสองแรงขนาดเท่ากันทิศตรงข้ามกระทำ", "เมื่อวัตถุมีมวลมาก",
      "เมื่อวัตถุวางอยู่บนพื้นลื่นโดยไม่มีแรงใดกระทำ", "ทุกครั้งที่มีแรงโน้มถ่วงกระทำ")),
    ("รถกำลังแล่นไปข้างหน้า แล้วมีแรงลัพธ์ทิศตรงข้ามกับการเคลื่อนที่กระทำ รถจะเป็นอย่างไร", "เคลื่อนที่ช้าลง",
     ("เคลื่อนที่เร็วขึ้น", "เคลื่อนที่ด้วยความเร็วคงที่", "ถอยหลังทันที", "หยุดนิ่งทันทีไม่ว่าแรงจะมากหรือน้อย",
      "เลี้ยวไปด้านข้าง")),
    ("มีแรง 5 นิวตันและ 5 นิวตันกระทำต่อกล่องในทิศตรงข้ามกัน กล่องที่อยู่นิ่งจะเป็นอย่างไร", "อยู่นิ่งต่อไป เพราะแรงลัพธ์เป็นศูนย์",
     ("เคลื่อนที่ด้วยแรงลัพธ์ 10 นิวตัน", "เคลื่อนที่ด้วยแรงลัพธ์ 5 นิวตัน", "เคลื่อนที่ไปทางแรงที่มากระทำก่อน",
      "สั่นไปมาอยู่กับที่", "ลอยขึ้นจากพื้น")),
)


PREDICTIONS = (
    "อยู่นิ่งต่อไป", "เคลื่อนที่ไปทางขวาด้วยความเร็วคงที่",
    "เริ่มเคลื่อนที่ไปทางขวา โดยเร็วขึ้นเรื่อย ๆ", "เริ่มเคลื่อนที่ไปทางซ้าย โดยเร็วขึ้นเรื่อย ๆ",
    "เคลื่อนที่ไปทางขวาเร็วขึ้นเรื่อย ๆ", "เคลื่อนที่ไปทางขวาช้าลง",
)


MOTION_SCENARIOS = (
    ("ยานอวกาศที่ดับเครื่องยนต์ในอวกาศซึ่งแทบไม่มีแรงใดกระทำ จะเคลื่อนที่อย่างไร",
     "เคลื่อนที่ต่อไปด้วยความเร็วคงที่ในแนวเดิม เพราะแรงลัพธ์เป็นศูนย์",
     ("หยุดทันทีเมื่อดับเครื่องยนต์", "ช้าลงจนหยุดเพราะแรงเสียดทานของอากาศ", "เร็วขึ้นเรื่อย ๆ")),
    ("รถยนต์แล่นด้วยความเร็วคงที่บนถนนตรง แรงขับของเครื่องยนต์กับแรงต้านรวมมีความสัมพันธ์กันอย่างไร",
     "มีขนาดเท่ากันและทิศตรงข้าม แรงลัพธ์จึงเป็นศูนย์",
     ("แรงขับมากกว่าแรงต้านเสมอ", "แรงต้านมากกว่าแรงขับ", "ไม่มีแรงใดกระทำต่อรถ")),
    ("ร่มชูชีพกางแล้วนักกระโดดตกลงด้วยความเร็วคงที่ แรงต้านอากาศมีขนาดเท่าใดเมื่อเทียบกับน้ำหนักของนักกระโดด",
     "เท่ากับน้ำหนัก เพราะแรงลัพธ์ต้องเป็นศูนย์เมื่อความเร็วคงที่",
     ("มากกว่าน้ำหนัก", "น้อยกว่าน้ำหนักมาก", "เป็นศูนย์")),
    ("นักปั่นจักรยานหยุดปั่นบนถนนราบ จักรยานค่อย ๆ ช้าลงจนหยุด เพราะเหตุใด",
     "แรงเสียดทานและแรงต้านอากาศเป็นแรงลัพธ์ทิศตรงข้ามกับการเคลื่อนที่",
     ("จักรยานหมดแรงในตัว", "แรงลัพธ์เป็นศูนย์จึงหยุด", "แรงโน้มถ่วงดึงจักรยานไปข้างหลัง")),
    ("ลิฟต์เคลื่อนที่ขึ้นด้วยความเร็วคงที่ แรงดึงของสายลิฟต์เป็นอย่างไรเมื่อเทียบกับน้ำหนักของลิฟต์",
     "เท่ากับน้ำหนักของลิฟต์ เพราะแรงลัพธ์เป็นศูนย์",
     ("มากกว่าน้ำหนักเสมอเพราะลิฟต์เคลื่อนที่ขึ้น", "น้อยกว่าน้ำหนัก", "เป็นศูนย์")),
    ("ผู้โดยสารบนรถโดยสารเซไปข้างหน้าเมื่อรถเบรกกะทันหัน เพราะเหตุใด",
     "ร่างกายยังคงเคลื่อนที่ไปข้างหน้าตามสภาพเดิม ขณะที่รถถูกแรงเบรกทำให้ช้าลง",
     ("มีแรงผลักผู้โดยสารไปข้างหน้า", "รถเร่งความเร็วขึ้นขณะเบรก", "แรงโน้มถ่วงเปลี่ยนทิศ")),
)


@question_type(
    "phys.net_force_motion_foundation",
    display_name={"th": "บอกผลของแรงลัพธ์ต่อสภาพการเคลื่อนที่"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOTION_TOPIC,
)
class NetForceMotionFoundation(QuestionType):
    """What a zero or non-zero resultant does to motion, in general or for one object."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _facts(rng, MOTION_FACTS, hint=MOTION_HINT, topic=MOTION_TOPIC)
        if rng.random() < 0.6:
            thing = rng.choice(MOVERS)
            start = rng.choice(("อยู่นิ่ง", f"กำลังเคลื่อนที่ไป{RIGHT}", f"กำลังเคลื่อนที่ไป{LEFT}"))
            net = rng.choice(("zero", RIGHT, LEFT))
            said = f"แรงลัพธ์ที่กระทำต่อ{thing}เป็นศูนย์" if net == "zero" else f"มีแรงลัพธ์ทิศไป{net}กระทำต่อ{thing}"
            answer = motion_after(start, net)
            options = [motion_after(s, n) for s in ("อยู่นิ่ง", f"กำลังเคลื่อนที่ไป{RIGHT}", f"กำลังเคลื่อนที่ไป{LEFT}")
                       for n in ("zero", RIGHT, LEFT)]
            return _labelled(
                stem=f"{thing}{start} ถ้า{said} {thing}จะเคลื่อนที่อย่างไร",
                correct=answer,
                wrongs=tuple(sorted({o for o in options if o != answer})),
                hint=MOTION_HINT, topic=MOTION_TOPIC,
            )
        zero = rng.random() < 0.5
        return _labelled(
            stem=f"ถ้าแรงลัพธ์ที่กระทำต่อวัตถุ{'เป็นศูนย์' if zero else 'ไม่เป็นศูนย์'} สภาพการเคลื่อนที่ของวัตถุเป็นอย่างไร",
            correct=("วัตถุคงสภาพเดิม คืออยู่นิ่งต่อไปหรือเคลื่อนที่ด้วยความเร็วคงที่" if zero
                     else "วัตถุเปลี่ยนสภาพการเคลื่อนที่ในทิศของแรงลัพธ์"),
            wrongs=(("วัตถุเปลี่ยนสภาพการเคลื่อนที่ในทิศของแรงลัพธ์" if zero
                     else "วัตถุคงสภาพเดิม คืออยู่นิ่งต่อไปหรือเคลื่อนที่ด้วยความเร็วคงที่"),
                    "วัตถุที่กำลังเคลื่อนที่จะหยุดทันทีเสมอ",
                    "วัตถุเคลื่อนที่ในทิศตรงข้ามกับแรงลัพธ์"),
            hint="แรงลัพธ์เป็นศูนย์ ไม่มีอะไรเปลี่ยน แรงลัพธ์ไม่เป็นศูนย์ ความเร็วเปลี่ยนตามทิศของแรงลัพธ์",
            topic=MOTION_TOPIC,
        )


@question_type(
    "phys.net_force_motion_fluency",
    display_name={"th": "พยากรณ์การเคลื่อนที่ของวัตถุจากแรงลัพธ์ของแรงหลายแรง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOTION_TOPIC,
)
class NetForceMotionFluency(QuestionType):
    """Forces on a trolley and how it starts; predict what follows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        start = rng.choice((AT_REST, MOVING_RIGHT))
        right = [rng.randint(2, 12) for _ in range(rng.choice((1, 2)))]
        total_right = sum(right)
        net = rng.choice((0, rng.randint(1, 6), -rng.randint(1, 6)))
        total_left = total_right - net
        while total_left <= 0:
            net = rng.randint(0, 3)
            total_left = total_right - net
        right_text = " และ ".join(f"{f} นิวตัน" for f in right)
        answer = predict(start, net)
        return _labelled(
            stem=(f"รถทดลองบนพื้นลื่น{start} มีแรง {right_text} กระทำไป{RIGHT} และแรง {total_left} นิวตัน กระทำไป{LEFT} "
                  "จากข้อมูลนี้ พยากรณ์ว่ารถจะเคลื่อนที่อย่างไร"),
            correct=answer,
            wrongs=tuple([p for p in PREDICTIONS if p != answer]),
            hint="รวมแรงแต่ละทิศแล้วหาแรงลัพธ์ จากนั้นดูว่ารถเริ่มจากอยู่นิ่งหรือกำลังเคลื่อนที่",
            topic=MOTION_TOPIC,
        )


@question_type(
    "phys.net_force_motion_application",
    display_name={"th": "ใช้แรงลัพธ์อธิบายการเคลื่อนที่ในสถานการณ์จริง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOTION_TOPIC,
)
class NetForceMotionApplication(QuestionType):
    """Authored cases, a tug of war, and a vehicle's drive against its resistance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            a, b = rng.sample(range(300, 801, 20), 2)
            if rng.random() < 0.25:
                b = a
            net = a - b
            answer = ("เชือกอยู่นิ่ง เพราะแรงลัพธ์เป็นศูนย์" if net == 0 else
                      f"เชือกเคลื่อนไปทางทีม {'ก' if net > 0 else 'ข'} เพราะแรงลัพธ์ {abs(net)} นิวตันมีทิศไปทางนั้น")
            options = ["เชือกอยู่นิ่ง เพราะแรงลัพธ์เป็นศูนย์",
                       f"เชือกเคลื่อนไปทางทีม ก เพราะแรงลัพธ์ {abs(net) or a + b} นิวตันมีทิศไปทางนั้น",
                       f"เชือกเคลื่อนไปทางทีม ข เพราะแรงลัพธ์ {abs(net) or a + b} นิวตันมีทิศไปทางนั้น",
                       f"เชือกเคลื่อนไปทางทีม {'ก' if net < 0 else 'ข'} เพราะแรงลัพธ์ {a + b} นิวตันมีทิศไปทางนั้น",
                       f"เชือกเคลื่อนไปทางทีม {'ก' if net > 0 else 'ข'} เพราะแรงลัพธ์ {a + b} นิวตันมีทิศไปทางนั้น",
                       "เชือกเคลื่อนไปทางทีมที่ออกแรงดึงก่อน เพราะแรงลัพธ์ขึ้นกับลำดับการดึง"]
            return _labelled(
                stem=(f"ชักเยอ ทีม ก ดึงเชือกไปทางซ้ายด้วยแรงรวม {a} นิวตัน ทีม ข ดึงไปทางขวาด้วยแรงรวม {b} นิวตัน "
                      "ขณะเริ่มดึงเชือกอยู่นิ่ง จากนั้นเชือกจะเป็นอย่างไร"),
                correct=answer,
                wrongs=tuple([o for o in dict.fromkeys(options) if o != answer]),
                hint="หาแรงลัพธ์จากผลต่างของแรงสองทิศ เชือกเคลื่อนตามทิศของแรงลัพธ์",
                topic=MOTION_TOPIC,
            )
        if roll < 0.7:
            vehicle = rng.choice(("รถยนต์", "รถบรรทุก", "รถจักรยานยนต์", "เรือยนต์", "รถไฟ"))
            drive = rng.randrange(1_000, 5_001, 100)
            resist = rng.choice((drive, drive - rng.randrange(100, 801, 100), drive + rng.randrange(100, 801, 100)))
            answer = ("แล่นด้วยความเร็วคงที่" if resist == drive else
                      "แล่นเร็วขึ้น" if drive > resist else "แล่นช้าลง")
            return _labelled(
                stem=(f"{vehicle}กำลังแล่นไปข้างหน้า มีแรงขับ {drive} นิวตัน และแรงต้านรวม {resist} นิวตัน "
                      f"{vehicle}จะแล่นอย่างไรต่อไป"),
                correct=answer,
                wrongs=tuple(o for o in ("แล่นด้วยความเร็วคงที่", "แล่นเร็วขึ้น", "แล่นช้าลง", "หยุดนิ่งทันที")
                             if o != answer),
                hint="เทียบแรงขับกับแรงต้าน เท่ากันความเร็วคงที่ แรงขับมากกว่าเร็วขึ้น แรงต้านมากกว่าช้าลง",
                topic=MOTION_TOPIC,
            )
        return _retopic(scenario_question(
            rng, MOTION_SCENARIOS,
            hint="ความเร็วคงที่หรืออยู่นิ่งหมายถึงแรงลัพธ์เป็นศูนย์",
        ), MOTION_TOPIC)

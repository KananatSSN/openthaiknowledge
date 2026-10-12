"""แผนภาพแสดงแรงที่กระทำต่อวัตถุในของเหลว

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/5

Sets moved here from: science_wave_d19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.force_diagrams import LIQUID_SPECS, diagram_question
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO
from otk.sets._support.science_wave_d19 import _facts

PROVENANCE = Provenance("original")


LIQUID_DIAGRAM_TOPIC = "แผนภาพแสดงแรงที่กระทำต่อวัตถุในของเหลว"


LIQUID_DIAGRAM_HINT = "แรงโน้มถ่วงดึงวัตถุลงเสมอ ของเหลวดันวัตถุขึ้น ความยาวลูกศรแปรตามขนาดของแรง"


LIQUID_DIAGRAM_FACTS = (
    ("ในแผนภาพแรงของวัตถุในของเหลว ลูกศรแรงพยุงชี้ไปทางใด", "ชี้ขึ้น",
     ("ชี้ลง", "ชี้ไปทางซ้าย", "ชี้ไปทางขวา", "ชี้เข้าหาก้นภาชนะ", "ไม่ต้องมีหัวลูกศร")),
    ("วัตถุลอยนิ่งอยู่ในน้ำ ลูกศรน้ำหนักกับลูกศรแรงพยุงควรยาวอย่างไร", "ยาวเท่ากัน ชี้ในทิศตรงข้ามกัน",
     ("แรงพยุงยาวกว่ามาก", "น้ำหนักยาวกว่ามาก", "ยาวเท่ากันและชี้ทิศเดียวกัน", "ไม่ต้องวาดลูกศรน้ำหนัก",
      "ไม่ต้องวาดลูกศรแรงพยุง")),
    ("วัตถุกำลังจมลงในน้ำ ลูกศรใดควรยาวกว่า", "ลูกศรน้ำหนัก",
     ("ลูกศรแรงพยุง", "ยาวเท่ากัน", "ไม่ต้องวาดลูกศรใดเลย", "ลูกศรแรงพยุงที่ชี้ลง", "ลูกศรแรงเสียดทาน")),
    ("ความยาวของลูกศรในแผนภาพแสดงแรงบอกสิ่งใด", "ขนาดของแรง",
     ("ทิศทางของแรง", "มวลของวัตถุ", "ความลึกของน้ำ", "ปริมาตรของวัตถุ", "ความเร็วของวัตถุ")),
    ("แรงพยุงเกิดจากสิ่งใด", "ความดันของของเหลวที่ดันใต้วัตถุมากกว่าที่ดันด้านบน",
     ("แรงแม่เหล็กของน้ำ", "อากาศที่อยู่เหนือผิวน้ำ", "น้ำหนักของวัตถุ", "ความร้อนของน้ำ", "แรงเสียดทานของน้ำ")),
)


LIQUID_DIAGRAM_SCENARIOS = (
    ("แผนภาพแสดงลูกศรน้ำหนัก 8 ช่องชี้ลง และลูกศรแรงพยุง 5 ช่องชี้ขึ้น วัตถุนี้จะเป็นอย่างไร",
     "จมลง เพราะน้ำหนักมากกว่าแรงพยุง", ("ลอยขึ้น", "ลอยนิ่ง", "เคลื่อนที่ไปด้านข้าง")),
    ("เพื่อนวาดแผนภาพลูกบอลที่ลอยนิ่งบนน้ำโดยมีลูกศรแรงพยุงยาวกว่าน้ำหนักมาก ข้อใดแก้ไขได้ถูกต้อง",
     "ลูกศรแรงพยุงควรยาวเท่าลูกศรน้ำหนัก เพราะวัตถุลอยนิ่ง แรงลัพธ์เป็นศูนย์",
     ("ถูกต้องแล้ว", "ลูกศรแรงพยุงควรชี้ลง", "ไม่ต้องวาดน้ำหนัก")),
    ("ถ้ากดลูกบอลให้จมอยู่นิ่งใต้น้ำด้วยมือ แผนภาพควรมีลูกศรใดบ้าง",
     "น้ำหนักและแรงกดจากมือชี้ลง แรงพยุงชี้ขึ้นโดยยาวเท่าผลรวมของสองแรงแรก",
     ("น้ำหนักชี้ลงเพียงแรงเดียว", "แรงพยุงชี้ลงและแรงกดชี้ขึ้น", "แรงพยุงยาวเท่าน้ำหนักเท่านั้น")),
)


@question_type(
    "phys.liquid_force_diagram_foundation",
    display_name={"th": "บอกแรงที่กระทำต่อวัตถุในของเหลว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=LIQUID_DIAGRAM_TOPIC,
)
class LiquidForceDiagramFoundation(QuestionType):
    """Which arrows belong on an object in a liquid, and how long each is drawn."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return _facts(rng, LIQUID_DIAGRAM_FACTS, hint=LIQUID_DIAGRAM_HINT, topic=LIQUID_DIAGRAM_TOPIC)
        if roll < 0.8:
            weight = rng.randint(4, 15)
            if rng.random() < 0.4:
                return _labelled(
                    stem=(f"วัตถุหนัก {weight} นิวตันลอยนิ่งอยู่ในน้ำ ถ้าใช้ 1 ช่องแทน 1 นิวตัน "
                          "ควรวาดลูกศรแรงพยุงอย่างไร"),
                    correct=f"ยาว {weight} ช่อง ชี้ขึ้น",
                    wrongs=(f"ยาว {weight} ช่อง ชี้ลง", f"ยาว {weight + 2} ช่อง ชี้ขึ้น", f"ยาว {weight // 2} ช่อง ชี้ขึ้น"),
                    hint=LIQUID_DIAGRAM_HINT, topic=LIQUID_DIAGRAM_TOPIC,
                )
            buoyant = rng.randint(1, weight - 1)
            return _labelled(
                stem=(f"วัตถุหนัก {weight} นิวตันจมมิดอยู่ในน้ำ ได้แรงพยุง {buoyant} นิวตัน "
                      "แรงลัพธ์ที่กระทำต่อวัตถุมีขนาดและทิศทางอย่างไร"),
                correct=f"{weight - buoyant} นิวตัน ชี้ลง",
                wrongs=(f"{weight - buoyant} นิวตัน ชี้ขึ้น", f"{weight + buoyant} นิวตัน ชี้ลง", "แรงลัพธ์เป็นศูนย์"),
                hint="แรงลัพธ์ = น้ำหนัก − แรงพยุง มีทิศตามแรงที่มากกว่า",
                topic=LIQUID_DIAGRAM_TOPIC,
            )
        return _labelled(
            stem="วัตถุที่อยู่ในน้ำ ควรวาดลูกศรแสดงแรงใดบ้างในแผนภาพ",
            correct="น้ำหนักของวัตถุชี้ลง และแรงพยุงของน้ำชี้ขึ้น",
            wrongs=("น้ำหนักของวัตถุชี้ขึ้น และแรงพยุงของน้ำชี้ลง",
                    "แรงพยุงชี้ลงเพียงแรงเดียว",
                    "ไม่มีแรงใดกระทำต่อวัตถุในน้ำ"),
            hint="แรงโน้มถ่วงดึงวัตถุลงเสมอ ของเหลวดันวัตถุขึ้น",
            topic=LIQUID_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.liquid_force_diagram_fluency",
    display_name={"th": "อ่านสภาพการจม-ลอยจากแผนภาพแรงในของเหลว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=LIQUID_DIAGRAM_TOPIC,
)
class LiquidForceDiagramFluency(QuestionType):
    """The student is shown the drawn diagram and reads the object's fate off it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(LIQUID_SPECS)
        weight = spec.of("W").newtons
        buoyant = spec.of("FB").newtons
        net = spec.vertical                     # positive is upwards
        floating = net == 0
        correct = ("แรงพยุงเท่ากับน้ำหนัก แรงลัพธ์เป็นศูนย์ วัตถุจึงลอยนิ่งอยู่กับที่" if floating else
                   f"น้ำหนักมากกว่าแรงพยุง {abs(net)} นิวตัน วัตถุจึงจมลง")
        wrongs = [
            # Reading the comparison backwards, and the two states it is not.
            (f"แรงพยุงมากกว่าน้ำหนัก {buoyant} นิวตัน วัตถุจึงลอยขึ้น" if floating else
             f"แรงพยุงมากกว่าน้ำหนัก {abs(net)} นิวตัน วัตถุจึงลอยขึ้น"),
            ("น้ำหนักมากกว่าแรงพยุง วัตถุจึงจมลง" if floating else
             "แรงพยุงเท่ากับน้ำหนัก วัตถุจึงลอยนิ่งอยู่กับที่"),
            f"แรงลัพธ์เท่ากับ {weight + buoyant} นิวตัน ชี้ลง วัตถุจึงจมลง",
            "ไม่มีแรงใดกระทำต่อวัตถุที่อยู่ในของเหลว",
        ]
        return diagram_question(
            spec,
            stem="จากแผนภาพ วัตถุนี้จะเป็นอย่างไร และเพราะเหตุใด",
            correct=correct,
            wrongs=tuple(dict.fromkeys(w for w in wrongs if w != correct))[:3],
            hint="เทียบความยาวลูกศรน้ำหนักกับลูกศรแรงพยุง ยาวเท่ากันคือลอยนิ่ง น้ำหนักยาวกว่าคือจม",
            topic=LIQUID_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.liquid_force_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพแรงของวัตถุในของเหลว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=LIQUID_DIAGRAM_TOPIC,
)
class LiquidForceDiagramApplication(QuestionType):
    """Authored cases, the hand force to hold a ball under, and a drawn pair to read."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            weight = rng.randint(1, 8)
            buoyant = rng.randint(weight + 2, 25)
            thing = rng.choice(("ลูกบอล", "ขวดพลาสติกเปล่าปิดฝา", "ทุ่นโฟม", "ห่วงยาง", "ก้อนไม้"))
            return numeric(
                stem=(f"{thing}หนัก {weight} นิวตัน เมื่อจมมิดน้ำได้แรงพยุง {buoyant} นิวตัน "
                      f"ต้องใช้มือกด{thing}ลงด้วยแรงเท่าใด {thing}จึงจะจมอยู่นิ่งใต้น้ำ"),
                answer=buoyant - weight, wrongs=(buoyant + weight, buoyant, weight),
                unit="นิวตัน", topic=LIQUID_DIAGRAM_TOPIC,
                hint="วัตถุอยู่นิ่งเมื่อแรงขึ้นเท่ากับแรงลงรวมกัน: แรงพยุง = น้ำหนัก + แรงกดจากมือ",
            )
        if roll < 0.7:
            weight = rng.randint(3, 15)
            buoyant = rng.choice([b for b in range(1, 16) if b != weight] + [weight] * 4)
            state = ("ลอยนิ่ง" if buoyant == weight else "จมลง" if weight > buoyant else "ลอยขึ้น")
            return _labelled(
                stem=(f"แผนภาพแสดงลูกศรน้ำหนัก {weight} ช่องชี้ลง และลูกศรแรงพยุง {buoyant} ช่องชี้ขึ้น "
                      "กระทำต่อวัตถุที่ถูกปล่อยนิ่งใต้น้ำ วัตถุนี้จะเป็นอย่างไร"),
                correct=state,
                wrongs=tuple(w for w in ("ลอยนิ่ง", "จมลง", "ลอยขึ้น", "เคลื่อนที่ไปด้านข้าง") if w != state),
                hint="เทียบความยาวลูกศรน้ำหนักกับแรงพยุง ยาวเท่ากันลอยนิ่ง น้ำหนักยาวกว่าจม แรงพยุงยาวกว่าลอยขึ้น",
                topic=LIQUID_DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, LIQUID_DIAGRAM_SCENARIOS,
            hint="วัตถุอยู่นิ่งเมื่อแรงขึ้นเท่ากับแรงลงรวมกัน",
        ), LIQUID_DIAGRAM_TOPIC)

"""การได้เปรียบเชิงกลและประสิทธิภาพของเครื่องกลอย่างง่าย

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/13

Sets moved here from: science_wave_f4.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f4 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MACHINE = "การได้เปรียบเชิงกลและประสิทธิภาพของเครื่องกลอย่างง่าย"


MACHINE_FACTS = (
    ("การได้เปรียบเชิงกลของเครื่องกลหมายถึงข้อใด", "อัตราส่วนของแรงต้านทาน (น้ำหนักที่ยก) ต่อแรงพยายาม",
     ("อัตราส่วนของแรงพยายามต่อแรงต้านทาน", "งานที่ได้ลบด้วยงานที่ใส่เข้าไป", "ความเร็วของเครื่องกล")),
    ("เครื่องกลอย่างง่ายช่วยในการทำงานอย่างไร", "ช่วยผ่อนแรงหรือเปลี่ยนทิศของแรง แต่ไม่ได้ลดงานที่ต้องทำ",
     ("ช่วยลดงานที่ต้องทำให้น้อยกว่างานที่ได้", "สร้างพลังงานเพิ่มขึ้นเอง", "ทำให้ประสิทธิภาพเกิน 100%")),
    ("เหตุใดประสิทธิภาพของเครื่องกลจริงจึงน้อยกว่า 100%", "มีพลังงานบางส่วนสูญเสียไปกับแรงเสียดทาน",
     ("เครื่องกลสร้างงานได้มากกว่าที่ใส่เข้าไป", "แรงพยายามมากกว่าน้ำหนักที่ยกเสมอ", "การได้เปรียบเชิงกลเป็นศูนย์")),
    ("รอกเดี่ยวตายตัวให้ประโยชน์ในข้อใด", "เปลี่ยนทิศของแรง โดยการได้เปรียบเชิงกลในอุดมคติเท่ากับ 1",
     ("ผ่อนแรงลงครึ่งหนึ่ง", "ลดงานที่ต้องทำลงครึ่งหนึ่ง", "เพิ่มระยะที่วัตถุเคลื่อนที่เป็นสองเท่า")),
)


@question_type(
    "phys.machine_advantage_foundation",
    display_name={"th": "การได้เปรียบเชิงกลของเครื่องกลอย่างง่าย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MACHINE,
)
class MachineAdvantageFoundation(QuestionType):
    """What the machine trades, and mechanical advantage = load ÷ effort."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(MACHINE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_MACHINE,
                             hint="เครื่องกลผ่อนแรงได้ แต่ต้องออกแรงเป็นระยะทางไกลขึ้น งานที่ได้ไม่เกินงานที่ใส่")
        effort = rng.randint(2, 20) * 10
        ma = rng.choice((Fraction(3, 2), 2, Fraction(5, 2), 3, 4, 5))
        load = effort * ma
        tool = rng.choice(("คานงัด", "รอกพวง", "พื้นเอียง", "ชะแลง"))
        return numeric(
            stem=f"ใช้{tool}ออกแรงพยายาม {effort} N ยกวัตถุหนัก {show(load)} N ได้ การได้เปรียบเชิงกลเท่าใด",
            answer=ma, wrongs=[Fraction(effort, load), load - effort, load * effort / 100], unit="",
            topic=TOPIC_MACHINE, hint="การได้เปรียบเชิงกล = แรงต้านทาน (น้ำหนักที่ยก) ÷ แรงพยายาม")


@question_type(
    "phys.machine_advantage_fluency",
    display_name={"th": "คำนวณประสิทธิภาพของเครื่องกลจากงานที่ได้และงานที่ใส่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MACHINE,
)
class MachineAdvantageFluency(QuestionType):
    """Efficiency = work out ÷ work in, on a slope, a pulley and a lever."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        load = rng.randint(2, 20) * 50
        h = rng.randint(1, 5)
        efficiency = rng.choice([e for e in (Fraction(1, 2), Fraction(3, 5), Fraction(3, 4), Fraction(4, 5))
                                 if (load * h / e).denominator == 1])
        work_in = load * h / efficiency
        length = rng.choice([x for x in (2, 4, 5, 8, 10, 20) if x > h and (work_in / x * 100).denominator == 1])
        effort = work_in / length
        return numeric(
            stem=(f"ใช้แรง {show(effort)} N ดันกล่องหนัก {load:,} N ขึ้นพื้นเอียงยาว {length} m ซึ่งสูง {h} m "
                  "ประสิทธิภาพของพื้นเอียงเท่ากับร้อยละเท่าใด"),
            answer=efficiency * 100, wrongs=[Fraction(effort * 100, load), Fraction(100 * h, length),
                                             100 - efficiency * 100],
            unit="เปอร์เซ็นต์", topic=TOPIC_MACHINE,
            hint="ประสิทธิภาพ = (งานที่ได้ ÷ งานที่ใส่) × 100 โดยงานที่ได้ = น้ำหนัก × ความสูง และงานที่ใส่ = แรง × ความยาวพื้นเอียง")


@question_type(
    "phys.machine_advantage_application",
    display_name={"th": "หาแรงที่ต้องใช้กับรอก พื้นเอียง และคาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MACHINE,
)
class MachineAdvantageApplication(QuestionType):
    """Ideal effort from the geometry, then real effort once efficiency bites."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            ropes = rng.choice((2, 3, 4, 5, 6))
            load = rng.randint(1, 20) * 60
            return numeric(
                stem=(f"รอกพวงมีเส้นเชือกช่วยรับน้ำหนัก {ropes} เส้น ใช้ยกวัตถุหนัก {load:,} N ในอุดมคติ "
                      "(ไม่คิดแรงเสียดทานและน้ำหนักรอก) ต้องออกแรงดึงเท่าใด"),
                answer=Fraction(load, ropes), wrongs=[load * ropes, Fraction(load, ropes + 1), Fraction(load, 2)],
                unit="N", topic=TOPIC_MACHINE,
                hint="เชือก n เส้นช่วยรับน้ำหนัก แรงที่ต้องใช้ในอุดมคติ = น้ำหนัก ÷ n")
        if shape == 1:
            load = rng.randint(2, 20) * 100
            h = rng.randint(1, 4)
            length = rng.choice([x for x in (2, 4, 5, 8, 10) if x > h])
            ideal = Fraction(load * h, length)
            efficiency = rng.choice([e for e in (Fraction(1, 2), Fraction(4, 5), Fraction(3, 4))
                                     if (ideal / e).denominator == 1] or [Fraction(1)])
            return numeric(
                stem=(f"ดันกล่องหนัก {load:,} N ขึ้นพื้นเอียงยาว {length} m สูง {h} m พื้นเอียงมีประสิทธิภาพ "
                      f"{show(efficiency * 100)}% ต้องออกแรงดันเท่าใด"),
                answer=ideal / efficiency, wrongs=[ideal, ideal * efficiency, Fraction(load, length)],
                unit="N", topic=TOPIC_MACHINE,
                hint="หาแรงในอุดมคติจาก น้ำหนัก × สูง ÷ ยาว แล้วหารด้วยประสิทธิภาพ (แรงจริงต้องมากกว่า)")
        load = rng.randint(2, 20) * 50
        load_arm = rng.choice((Fraction(1, 5), Fraction(1, 4), Fraction(1, 2)))
        effort_arm = rng.choice((1, 2))
        return numeric(
            stem=(f"ใช้ชะแลงงัดหินหนัก {load:,} N โดยจุดหมุนอยู่ห่างหิน {show(load_arm)} m และมือกดห่างจากจุดหมุน "
                  f"{show(effort_arm)} m ต้องออกแรงกดอย่างน้อยเท่าใด"),
            answer=load * load_arm / effort_arm, wrongs=[load * effort_arm / load_arm, load, load * load_arm],
            unit="N", topic=TOPIC_MACHINE,
            hint="คานสมดุลเมื่อโมเมนต์เท่ากัน: แรงพยายาม × แขนของแรงพยายาม = น้ำหนัก × แขนของน้ำหนัก")

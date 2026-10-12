"""การคำนวณปริมาณความร้อนที่ทำให้สสารเปลี่ยนอุณหภูมิและเปลี่ยนสถานะ

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/1

Sets moved here from: science_wave_d28.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import HEATING_CURVES, diagram_question, heating_curve_alt
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


HEAT_QUANTITY_TOPIC = "การคำนวณปริมาณความร้อนที่ทำให้สสารเปลี่ยนอุณหภูมิและเปลี่ยนสถานะ"


SPECIFIC_HEATS = (("น้ำ", 4200), ("น้ำมันพืช", 2000), ("อะลูมิเนียม", 900), ("เหล็ก", 450),
                  ("ทองแดง", 390), ("ทราย", 800), ("แอลกอฮอล์", 2400))


HEAT_QUANTITY_SCENARIOS = (
    ("น้ำและน้ำมันมวลเท่ากันได้รับความร้อนในอัตราเท่ากัน แต่น้ำมันมีอุณหภูมิสูงขึ้นเร็วกว่าน้ำมาก เหตุใดจึงเป็นเช่นนี้",
     "น้ำมีความร้อนจำเพาะสูงกว่าน้ำมัน จึงต้องใช้ความร้อนมากกว่าในการเพิ่มอุณหภูมิเท่ากัน",
     ("น้ำมีความร้อนจำเพาะต่ำกว่าน้ำมัน จึงต้องใช้ความร้อนน้อยกว่าในการเพิ่มอุณหภูมิเท่ากัน", "น้ำมันมีความหนาแน่นน้อยกว่าน้ำ จึงต้องใช้ความร้อนมากกว่าในการเพิ่มอุณหภูมิ", "ความร้อนจำเพาะไม่มีผลต่ออัตราการเพิ่มอุณหภูมิ")),
    ("น้ำแข็งที่กำลังละลายจะมีอุณหภูมิคงที่ 0 องศาเซลเซียสตลอดช่วงที่ยังละลายไม่หมด แม้ยังได้รับความร้อนต่อเนื่อง เหตุใดจึงเป็นเช่นนี้",
     "ความร้อนที่ได้รับถูกใช้ไปกับการเปลี่ยนสถานะจากของแข็งเป็นของเหลว ไม่ได้ใช้เพิ่มอุณหภูมิ",
     ("น้ำแข็งหยุดรับความร้อนโดยอัตโนมัติเมื่อเริ่มละลาย ความร้อนจึงไม่ถูกใช้ทำอะไรเลย", "อุณหภูมิ 0 องศาเซลเซียสเป็นอุณหภูมิสูงสุดที่น้ำแข็งรับได้", "ความร้อนที่ได้รับถูกใช้ไปกับการทำให้น้ำแข็งเย็นลง อุณหภูมิจึงยังคงที่อยู่ที่ 0 องศา")),
    ("สารมวล 2 กิโลกรัมและสารชนิดเดียวกันมวล 4 กิโลกรัม ได้รับความร้อนจากแหล่งความร้อนเดียวกันในอัตราเท่ากัน สารใดจะมีอุณหภูมิสูงขึ้นเร็วกว่า และเพราะเหตุใด",
     "สารมวล 2 กิโลกรัมจะมีอุณหภูมิสูงขึ้นเร็วกว่า เพราะมวลน้อยกว่าใช้ความร้อนน้อยกว่าในการเปลี่ยนอุณหภูมิเท่ากัน",
     ("สารมวล 4 กิโลกรัมจะมีอุณหภูมิสูงขึ้นเร็วกว่า เพราะมวลมากกว่ารับความร้อนได้มากกว่าในเวลาเท่ากัน", "ทั้งสองสารจะมีอุณหภูมิสูงขึ้นเร็วเท่ากัน เพราะเป็นสารชนิดเดียวกันและได้รับความร้อนเท่ากัน", "มวลของสารไม่มีผลต่ออัตราการเพิ่มขึ้นของอุณหภูมิ")),
)


@question_type(
    "phys.heat_quantity_foundation",
    display_name={"th": "แปลความหมายกราฟอุณหภูมิกับเวลาขณะให้ความร้อนแก่สาร"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_QUANTITY_TOPIC,
)
class HeatQuantityFoundation(QuestionType):
    """A flat stretch on a heating graph means the substance is changing state.

    The indicator says แปลความหมายข้อมูล, so the graph is drawn and the flat
    stretch is found rather than announced. Half the draws ask what the flat
    part means; half ask for a value read off the axes, which is the reading
    skill the meaning rests on.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEATING_CURVES)
        if rng.random() < 0.5:
            stem = "จากกราฟ ช่วงที่อุณหภูมิคงที่แม้ยังให้ความร้อนต่อไปหมายความว่าอย่างไร"
            correct = "สารกำลังเปลี่ยนสถานะ ความร้อนช่วงนี้ใช้เปลี่ยนสถานะ ไม่ได้ใช้เพิ่มอุณหภูมิ"
            wrongs = ("เครื่องมือวัดอุณหภูมิเสีย จึงอ่านค่าคงที่ผิดพลาด",
                      "สารได้หยุดรับความร้อนในช่วงนั้นแล้ว แม้แหล่งความร้อนยังทำงานอยู่ตามปกติ",
                      "สารกำลังเย็นตัวลงในช่วงนั้น แม้ยังได้รับความร้อนต่อไป")
        else:
            stem = "จากกราฟ สารเปลี่ยนสถานะที่อุณหภูมิใด และใช้เวลานานเท่าใด"
            correct = f"{spec.plateau} องศาเซลเซียส เป็นเวลา {spec.hold} นาที"
            wrongs = (f"{spec.plateau} องศาเซลเซียส เป็นเวลา {spec.total} นาที",
                      f"{spec.start} องศาเซลเซียส เป็นเวลา {spec.hold} นาที",
                      f"{spec.end} องศาเซลเซียส เป็นเวลา {spec.warm_to} นาที")
        return diagram_question(
            spec.asset_id, heating_curve_alt(spec),
            stem=stem, correct=correct, wrongs=wrongs,
            hint=("ช่วงที่เส้นกราฟราบคือช่วงที่อุณหภูมิไม่เปลี่ยน อ่านอุณหภูมิจากแกนตั้ง "
                  "และอ่านเวลาเริ่มกับเวลาสิ้นสุดของช่วงนั้นจากแกนนอน"),
            topic=HEAT_QUANTITY_TOPIC,
        )


@question_type(
    "phys.heat_quantity_fluency",
    display_name={"th": "คำนวณปริมาณความร้อนโดยใช้สมการ Q = mcΔT"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_QUANTITY_TOPIC,
)
class HeatQuantityFluency(QuestionType):
    """Compute Q = mcΔT from a given mass, specific heat, and temperature change."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mass = rng.choice((0.5, 1, 2))
        specific_heat = rng.choice((900, 2000, 4200))
        delta_t = rng.choice((5, 10, 15, 20))
        answer = mass * specific_heat * delta_t
        wrong_no_c = mass * delta_t
        wrong_no_dt = mass * specific_heat
        wrong_half = answer / 2
        return _labelled(
            stem=(f"สารมวล {mass:g} กิโลกรัม มีความร้อนจำเพาะ {specific_heat:g} จูลต่อกิโลกรัมต่อองศาเซลเซียส "
                  f"ได้รับความร้อนจนอุณหภูมิเปลี่ยนแปลงไป {delta_t} องศาเซลเซียส โดยไม่มีการเปลี่ยนสถานะ "
                  "ปริมาณความร้อนที่สารได้รับมีค่าเท่าใด (ใช้ Q = mcΔT)"),
            correct=f"{answer:g} จูล",
            wrongs=(f"{wrong_no_c:g} จูล", f"{wrong_no_dt:g} จูล", f"{wrong_half:g} จูล"),
            hint="Q = mcΔT คูณมวล ความร้อนจำเพาะ และผลต่างอุณหภูมิเข้าด้วยกันทั้งสามค่า",
            topic=HEAT_QUANTITY_TOPIC,
        )


@question_type(
    "phys.heat_quantity_application",
    display_name={"th": "ใช้ความรู้เรื่องปริมาณความร้อนอธิบายสถานการณ์จริง"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_QUANTITY_TOPIC,
)
class HeatQuantityApplication(QuestionType):
    """Authored cases, and which of two warmings takes more heat."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            while True:
                (n1, c1), (n2, c2) = rng.sample(SPECIFIC_HEATS, 2)
                m1, m2 = rng.choice((0.5, 1, 2, 3)), rng.choice((0.5, 1, 2, 3))
                t1, t2 = rng.choice((5, 10, 20, 30)), rng.choice((5, 10, 20, 30))
                q1, q2 = m1 * c1 * t1, m2 * c2 * t2
                if q1 != q2:
                    break
            more = "ก" if q1 > q2 else "ข"
            return _labelled(
                stem=(f"ก: {n1} {m1:g} กิโลกรัม (c = {c1} J/kg·°C) อุณหภูมิเพิ่มขึ้น {t1} °C / "
                      f"ข: {n2} {m2:g} กิโลกรัม (c = {c2} J/kg·°C) อุณหภูมิเพิ่มขึ้น {t2} °C "
                      "โดยไม่มีการเปลี่ยนสถานะ แบบใดต้องใช้ความร้อนมากกว่า"),
                correct=f"{more} เพราะผลคูณ mcΔT มีค่ามากกว่า ({q1:,.0f} กับ {q2:,.0f} จูล)",
                wrongs=(f"{'ข' if more == 'ก' else 'ก'} เพราะผลคูณ mcΔT มีค่ามากกว่า ({q1:,.0f} กับ {q2:,.0f} จูล)",
                        "ใช้ความร้อนเท่ากัน เพราะเป็นการเพิ่มอุณหภูมิเหมือนกัน",
                        f"{'ก' if c1 < c2 else 'ข'} เพราะมีความร้อนจำเพาะน้อยกว่าจึงต้องใช้ความร้อนมากกว่า"),
                hint="คำนวณ Q = mcΔT ของแต่ละแบบแล้วเปรียบเทียบ",
                topic=HEAT_QUANTITY_TOPIC,
            )
        return _retopic(scenario_question(
            rng, HEAT_QUANTITY_SCENARIOS,
            hint="ความร้อนจำเพาะที่สูงขึ้นหรือมวลที่มากขึ้นทำให้ต้องใช้ความร้อนมากขึ้นในการเปลี่ยนอุณหภูมิเท่ากัน",
        ), HEAT_QUANTITY_TOPIC)

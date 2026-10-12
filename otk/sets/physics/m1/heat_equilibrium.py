"""การคำนวณสมดุลความร้อนระหว่างสสาร

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/5

Sets moved here from: science_wave_d29.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


HEAT_EQUILIBRIUM_TOPIC = "การคำนวณสมดุลความร้อนระหว่างสสาร"


EQ_THINGS = ("ช้อนโลหะ", "ก้อนหิน", "แก้วน้ำ", "ลูกเหล็ก", "น้ำในแก้ว", "ผ้าเปียก", "ถุงน้ำแข็ง", "มือของนักเรียน")


EQ_HINT = "ความร้อนถ่ายโอนจากที่อุณหภูมิสูงไปที่อุณหภูมิต่ำเสมอ จนอุณหภูมิเท่ากันทั้งสองฝั่ง (สมดุลความร้อน)"


HEAT_MIX_COMBOS = (
    (2, 90, 1, 30, 70),
    (1, 70, 3, 10, 25),
    (3, 80, 1, 20, 65),
    (1, 100, 4, 20, 36),
    (4, 50, 1, 10, 42),
    (1, 90, 2, 30, 50),
)


def _mix(rng: Random) -> tuple[int, int, int, int, int]:
    """Two unequal masses of water whose mixed temperature is a whole degree."""
    while True:
        m1, m2 = rng.sample((1, 2, 3, 4, 5), 2)
        t1 = rng.randrange(50, 101, 5)
        t2 = rng.randrange(5, 41, 5)
        total = m1 * t1 + m2 * t2
        if total % (m1 + m2) == 0:
            return m1, t1, m2, t2, total // (m1 + m2)


HEAT_EQUILIBRIUM_SCENARIOS = (
    ("นักเรียนแช่ช้อนโลหะร้อนลงในน้ำเย็นปริมาณมาก เมื่อเทียบกับการแช่ในน้ำเย็นปริมาณน้อย กรณีใดทำให้อุณหภูมิสุดท้ายใกล้เคียงอุณหภูมิน้ำเย็นเดิมมากกว่า",
     "แช่ในน้ำเย็นปริมาณมาก เพราะน้ำปริมาณมากดูดกลืนความร้อนจากช้อนได้โดยอุณหภูมิเปลี่ยนแปลงน้อย",
     ("แช่ในน้ำเย็นปริมาณน้อย เพราะน้ำน้อยดูดความร้อนได้เร็วกว่า", "ทั้งสองกรณีให้อุณหภูมิสุดท้ายเท่ากันเสมอ", "ปริมาณน้ำไม่มีผลต่ออุณหภูมิสุดท้ายของระบบ")),
    ("กาต้มน้ำที่มีน้ำร้อนมากถูกเทลงผสมกับน้ำเย็นในถ้วยจนล้น เหตุใดอุณหภูมิสุดท้ายจึงใกล้เคียงกับอุณหภูมิน้ำร้อนมากกว่าน้ำเย็น",
     "เพราะมวลของน้ำร้อนมากกว่ามวลของน้ำเย็นมาก อุณหภูมิสมดุลจึงเอนเอียงไปทางน้ำร้อน",
     ("เพราะน้ำร้อนมีความร้อนจำเพาะต่ำกว่าน้ำเย็นเสมอ", "มวลของแต่ละส่วนไม่มีผลต่ออุณหภูมิสมดุล", "อุณหภูมิสมดุลจะอยู่กึ่งกลางระหว่างอุณหภูมิทั้งสองเสมอไม่ว่ามวลจะเป็นเท่าใด")),
    ("หากผสมน้ำร้อนและน้ำเย็นที่มีมวลเท่ากันในภาชนะฉนวนความร้อน อุณหภูมิสุดท้ายจะสัมพันธ์กับอุณหภูมิเริ่มต้นทั้งสองอย่างไร",
     "อุณหภูมิสุดท้ายจะเท่ากับค่าเฉลี่ยของอุณหภูมิเริ่มต้นทั้งสอง เพราะมวลเท่ากันจึงถ่วงน้ำหนักเท่ากัน",
     ("อุณหภูมิสุดท้ายจะเท่ากับอุณหภูมิของน้ำร้อนเสมอ", "อุณหภูมิสุดท้ายจะเท่ากับอุณหภูมิของน้ำเย็นเสมอ", "อุณหภูมิสุดท้ายไม่สามารถคำนวณได้เมื่อมวลเท่ากัน")),
)


@question_type(
    "phys.heat_equilibrium_foundation",
    display_name={"th": "วิเคราะห์ทิศทางการถ่ายโอนความร้อนระหว่างวัตถุ"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_EQUILIBRIUM_TOPIC,
)
class HeatEquilibriumFoundation(QuestionType):
    """Heat flows from hotter to colder until both reach the same temperature."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _labelled(
                stem="เมื่อวางวัตถุร้อนสัมผัสกับวัตถุเย็น ความร้อนจะถ่ายโอนไปในทิศทางใด",
                correct="จากวัตถุที่มีอุณหภูมิสูงไปยังวัตถุที่มีอุณหภูมิต่ำ จนกระทั่งอุณหภูมิเท่ากัน (สมดุลความร้อน)",
                wrongs=("จากวัตถุที่มีอุณหภูมิต่ำไปยังวัตถุที่มีอุณหภูมิสูง จนกระทั่งอุณหภูมิเท่ากัน",
                        "ความร้อนถ่ายโอนไปมาทั้งสองทิศทางเท่ากันตลอดเวลาโดยไม่มีวันสิ้นสุด",
                        "ไม่มีการถ่ายโอนความร้อนใด ๆ จนกว่าจะสัมผัสกันเป็นเวลานานมาก"),
                hint=EQ_HINT, topic=HEAT_EQUILIBRIUM_TOPIC,
            )
        a, b = rng.sample(EQ_THINGS, 2)
        ta, tb = rng.sample(range(-10, 91, 5), 2)
        hot, cold = (a, b) if ta > tb else (b, a)
        return _labelled(stem=f"{a}อุณหภูมิ {ta} °C สัมผัสกับ{b}อุณหภูมิ {tb} °C ความร้อนจะถ่ายโอนอย่างไร",
                         correct=f"จาก{hot}ไปยัง{cold} จนอุณหภูมิเท่ากัน",
                         wrongs=(f"จาก{cold}ไปยัง{hot} จนอุณหภูมิเท่ากัน", "ไม่มีการถ่ายโอนความร้อน เพราะเป็นวัตถุต่างชนิดกัน",
                                 f"จาก{hot}ไปยัง{cold} จน{cold}ร้อนกว่า{hot}",
                                 f"จาก{cold}ไปยัง{hot} จน{hot}ร้อนกว่า{cold}"),  # both halves wrong
                         hint=EQ_HINT, topic=HEAT_EQUILIBRIUM_TOPIC)


@question_type(
    "phys.heat_equilibrium_fluency",
    display_name={"th": "คำนวณอุณหภูมิสมดุลโดยใช้สมการ Qสูญเสีย เท่ากับ Qได้รับ"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_EQUILIBRIUM_TOPIC,
)
class HeatEquilibriumFluency(QuestionType):
    """Mixing hot and cold water in an insulated container; find the final temperature."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m1, t1, m2, t2, tf = rng.choice(HEAT_MIX_COMBOS) if rng.random() < 0.2 else _mix(rng)
        avg = (t1 + t2) / 2
        swap = (m2 * t1 + m1 * t2) / (m1 + m2)
        offset = tf + 5
        wrongs = []
        for w in (avg, swap, offset, tf - 5, tf + 10):
            if w != tf and f"{w:g}" not in wrongs:
                wrongs.append(f"{w:g}")
        return _labelled(
            stem=(f"นำน้ำร้อนมวล {m1} กิโลกรัม อุณหภูมิ {t1} องศาเซลเซียส ผสมกับน้ำเย็นมวล {m2} กิโลกรัม "
                  f"อุณหภูมิ {t2} องศาเซลเซียส ในภาชนะฉนวนความร้อนที่ไม่มีการสูญเสียความร้อนออกนอกระบบ "
                  "เมื่อถึงสมดุลความร้อน อุณหภูมิสุดท้ายของน้ำผสมเป็นเท่าใด (ใช้ Qสูญเสีย = Qได้รับ)"),
            correct=f"{tf:g} องศาเซลเซียส",
            wrongs=tuple(f"{w} องศาเซลเซียส" for w in wrongs[:3]),
            hint="Qสูญเสียของน้ำร้อน = Qได้รับของน้ำเย็น: m1(T1 − Tf) = m2(Tf − T2) แล้วแก้หา Tf",
            topic=HEAT_EQUILIBRIUM_TOPIC,
        )


@question_type(
    "phys.heat_equilibrium_application",
    display_name={"th": "ใช้ความรู้เรื่องสมดุลความร้อนอธิบายผลของมวลต่ออุณหภูมิสุดท้าย"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_EQUILIBRIUM_TOPIC,
)
class HeatEquilibriumApplication(QuestionType):
    """Authored cases, and the heat the hot water gives up (c = 4,200 J/kg·°C, stated)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, HEAT_EQUILIBRIUM_SCENARIOS,
                hint="อุณหภูมิสมดุลเอนเอียงไปทางฝั่งที่มีมวลมากกว่าเสมอ และเท่ากับค่าเฉลี่ยถ่วงน้ำหนักด้วยมวล",
            ), HEAT_EQUILIBRIUM_TOPIC)
        m1, t1, m2, t2, tf = _mix(rng)
        lost = m1 * 4200 * (t1 - tf)
        return numeric(stem=f"ผสมน้ำร้อนมวล {m1} kg อุณหภูมิ {t1} °C กับน้ำเย็นมวล {m2} kg อุณหภูมิ {t2} °C ในภาชนะฉนวน ได้อุณหภูมิสุดท้าย {tf} °C "
                            f"น้ำร้อนสูญเสียความร้อนกี่จูล (ความร้อนจำเพาะของน้ำ 4,200 J/kg·°C, Q = mcΔT)",
                       answer=lost, wrongs=[m2 * 4200 * (tf - t2) + 4200, m1 * 4200 * t1, lost // 2], unit="จูล", topic=HEAT_EQUILIBRIUM_TOPIC,
                       hint="ความร้อนที่น้ำร้อนสูญเสีย = m × 4,200 × (T ร้อน − T สุดท้าย) ซึ่งเท่ากับที่น้ำเย็นได้รับ")

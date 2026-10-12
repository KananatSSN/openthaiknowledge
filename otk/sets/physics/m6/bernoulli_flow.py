"""ของไหลอุดมคติ สมการความต่อเนื่อง และสมการแบร์นูลลี

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/6

Sets moved here from: science_wave_f15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, _labelled, numeric, show
from otk.sets._support.science_wave_f4 import DROPS
from otk.sets._support.science_wave_f15 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_FLOW = "ของไหลอุดมคติ สมการความต่อเนื่อง และสมการแบร์นูลลี"


WATER = 1000


FLOW_FACTS = (
    ("ข้อใดเป็นสมบัติของของไหลอุดมคติ", "ไหลอย่างสม่ำเสมอ ไม่มีความหนืด และอัดตัวไม่ได้",
     ("มีความหนืดสูงและอัดตัวได้", "ไหลแบบปั่นป่วนเสมอ", "ความหนาแน่นเปลี่ยนตามความเร็ว")),
    ("น้ำไหลในท่อที่ส่วนแคบลง อัตราเร็วของน้ำตรงส่วนแคบเป็นอย่างไร", "มากขึ้น เพราะ Av คงตัว",
     ("น้อยลง เพราะท่อแคบ", "เท่าเดิม", "เป็นศูนย์")),
    ("ตามสมการแบร์นูลลี ในท่อระดับเดียวกัน ตรงที่ของไหลเร็วขึ้น ความดันเป็นอย่างไร", "ความดันลดลง",
     ("ความดันเพิ่มขึ้น", "ความดันเท่าเดิม", "ความดันเป็นศูนย์")),
    ("ปีกเครื่องบินเกิดแรงยก เพราะเหตุใด", "อากาศเหนือปีกเร็วกว่าใต้ปีก ความดันเหนือปีกจึงน้อยกว่า",
     ("อากาศใต้ปีกเร็วกว่า ความดันใต้ปีกน้อยกว่า", "เครื่องยนต์ดันปีกขึ้นโดยตรง", "ปีกเบากว่าอากาศ")),
    ("กระบอกฉีดน้ำหอมดูดของเหลวขึ้นมาได้ เพราะเหตุใด", "อากาศที่พ่นผ่านปลายหลอดเร็ว ความดันตรงนั้นต่ำกว่าความดันในขวด",
     ("ของเหลวร้อนจึงลอยขึ้น", "แรงโน้มถ่วงดึงของเหลวขึ้น", "ความดันในขวดลดลงเอง")),
    ("เวลารถบรรทุกแล่นสวนกันเร็ว ๆ รถทั้งสองมักถูกดูดเข้าหากัน เพราะเหตุใด", "อากาศระหว่างรถเร็วขึ้น ความดันระหว่างรถจึงต่ำกว่าด้านนอก",
     ("รถทั้งสองมีประจุไฟฟ้าต่างชนิด", "แรงโน้มถ่วงระหว่างรถ", "ลมจากด้านนอกอ่อนลง")),
)


@question_type(
    "phys.bernoulli_flow_foundation",
    display_name={"th": "ของไหลอุดมคติ สมการความต่อเนื่อง และหลักการของแบร์นูลลีในอุปกรณ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLOW,
)
class BernoulliFlowFoundation(QuestionType):
    """Faster where narrower, lower pressure where faster."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(FLOW_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FLOW,
                             hint="ท่อแคบของไหลเร็วขึ้น (A₁v₁ = A₂v₂) และตรงที่ไหลเร็วความดันต่ำ (แบร์นูลลี)")
        a1 = rng.randint(2, 40)
        v1 = Fraction(rng.randint(1, 20), 10)
        a2 = rng.choice([x for x in range(1, a1) if _exact(a1 * v1 / x)])
        return numeric(
            stem=(f"น้ำไหลในท่อพื้นที่หน้าตัด {a1} cm² ด้วยอัตราเร็ว {show(v1)} m/s แล้วไหลเข้าส่วนที่มีพื้นที่หน้าตัด "
                  f"{a2} cm² อัตราเร็วของน้ำในส่วนนี้เท่าใด"),
            answer=a1 * v1 / a2, wrongs=[a2 * v1 / a1, v1, v1 * a1], unit="m/s", topic=TOPIC_FLOW,
            hint="สมการความต่อเนื่อง A₁v₁ = A₂v₂")


@question_type(
    "phys.bernoulli_flow_fluency",
    display_name={"th": "คำนวณด้วยสมการความต่อเนื่องและอัตราการไหล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLOW,
)
class BernoulliFlowFluency(QuestionType):
    """v scales with (d₁/d₂)², and the volume flow rate Av."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            d1, d2 = rng.choice(((2, 1), (3, 1), (4, 2), (4, 1), (6, 3), (6, 2), (5, 1), (10, 5)))
            v1 = Fraction(rng.randint(1, 20), 10)
            return numeric(
                stem=(f"ท่อน้ำเส้นผ่านศูนย์กลาง {d1} cm ต่อกับท่อเส้นผ่านศูนย์กลาง {d2} cm น้ำในท่อใหญ่ไหลด้วยอัตราเร็ว "
                      f"{show(v1)} m/s น้ำในท่อเล็กไหลเร็วเท่าใด"),
                answer=v1 * Fraction(d1, d2) ** 2, wrongs=[v1 * Fraction(d1, d2), v1 * Fraction(d2, d1) ** 2, v1],
                unit="m/s", topic=TOPIC_FLOW, hint="พื้นที่แปรผันตามเส้นผ่านศูนย์กลางกำลังสอง: v₂ = v₁(d₁/d₂)²")
        area = rng.randint(1, 50)
        v = Fraction(rng.randint(1, 20), 10)
        rate_l = area * v / 10  # cm² × m/s = 10⁻⁴ m³/s = 0.1 L/s
        return numeric(
            stem=f"น้ำไหลในท่อพื้นที่หน้าตัด {area} cm² ด้วยอัตราเร็ว {show(v)} m/s อัตราการไหลกี่ลิตรต่อวินาที",
            answer=rate_l, wrongs=[area * v, rate_l * 10, rate_l / 10], unit="L/s", topic=TOPIC_FLOW,
            hint="อัตราการไหล Q = Av (1 cm² = 10⁻⁴ m², 1 m³ = 1,000 L)")


@question_type(
    "phys.bernoulli_flow_application",
    display_name={"th": "ใช้สมการแบร์นูลลีหาผลต่างความดันและอัตราเร็วของน้ำที่พุ่งออกจากถัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLOW,
)
class BernoulliFlowApplication(QuestionType):
    """ΔP = ½ρ(v₂² − v₁²) in a level pipe, and v = √(2gh) from a hole in a tank."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            v1 = rng.randint(1, 5)
            v2 = v1 + rng.randint(1, 8)
            dp = Fraction(WATER * (v2 * v2 - v1 * v1), 2)
            return numeric(
                stem=(f"น้ำไหลในท่อระดับเดียวกัน ส่วนกว้างไหลด้วยอัตราเร็ว {v1} m/s ส่วนแคบไหลด้วยอัตราเร็ว {v2} m/s "
                      "ความดันในส่วนกว้างมากกว่าส่วนแคบกี่ปาสคัล (ความหนาแน่นน้ำ 1,000 kg/m³)"),
                answer=dp, wrongs=[Fraction(WATER * (v2 - v1) ** 2, 2), WATER * (v2 * v2 - v1 * v1), Fraction(WATER * v2 * v2, 2)],
                unit="Pa", topic=TOPIC_FLOW, hint="P₁ − P₂ = ½ρ(v₂² − v₁²) ไม่ใช่ ½ρ(v₂ − v₁)²")
        h, v = rng.choice(DROPS)
        return numeric(
            stem=(f"ถังน้ำเปิดด้านบนมีรูเล็ก ๆ อยู่ต่ำกว่าผิวน้ำ {show(h)} m น้ำพุ่งออกจากรูด้วยอัตราเร็วเท่าใด (g = 10 m/s²)"),
            answer=v, wrongs=[2 * G * h, G * h, v * 2], unit="m/s", topic=TOPIC_FLOW,
            hint="ทฤษฎีของทอร์ริเชลลี (จากแบร์นูลลี): v = √(2gh)")

"""มวลกับการเปลี่ยนแปลงการเคลื่อนที่

ฟิสิกส์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.4/3

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


MASS_TOPIC = "มวลกับการเปลี่ยนแปลงการเคลื่อนที่"


MASS_PAIRS = (("รถเข็นเปล่า", 8), ("รถเข็นบรรทุกข้าวสาร", 60), ("ลูกปิงปอง", 0.003), ("ลูกโบว์ลิ่ง", 6),
              ("จักรยาน", 12), ("รถจักรยานยนต์", 110), ("ลูกฟุตบอล", 0.4), ("ลูกเหล็กทุ่มน้ำหนัก", 4),
              ("กล่องเปล่า", 1), ("ตู้เย็น", 70), ("ลูกเทนนิส", 0.06), ("ถังน้ำเต็มถัง", 15))


MASS_PLANS = (
    ("ต้องเข็นรถเข็นขึ้นทางลาดให้ง่ายที่สุด ควรทำอย่างไร", "ลดของบนรถเข็นให้น้อยลงก่อน แล้วค่อยขนหลายรอบ",
     ("บรรทุกของเพิ่มให้เต็มคันในรอบเดียว", "เพิ่มก้อนหินถ่วงรถเข็น", "ทาสีรถเข็นใหม่", "เปลี่ยนเป็นรถเข็นที่หนักกว่าเพื่อให้เข็นได้มั่นคงขึ้น",
      "ผูกของหนักเพิ่มที่ด้ามจับ")),
    ("นักกีฬาต้องการให้เรือพายออกตัวได้เร็วที่สุด ควรทำอย่างไร", "นำสัมภาระที่ไม่จำเป็นออกจากเรือเพื่อลดมวล",
     ("บรรทุกน้ำหนักเพิ่มในเรือ", "เปลี่ยนสีพาย", "นั่งให้ห่างกันมากขึ้นในเรือโดยไม่ลดน้ำหนัก", "ใส่ทรายในเรือ", "เติมน้ำลงในเรือ")),
    ("เหตุใดรถบรรทุกที่บรรทุกของหนักจึงต้องขับช้าและเว้นระยะห่างจากรถคันหน้ามากกว่ารถเก๋ง",
     "รถบรรทุกมีมวลมาก จึงหยุดได้ยากและต้องใช้ระยะเบรกยาวกว่า",
     ("รถบรรทุกหยุดได้ง่ายกว่า เพราะล้อมีจำนวนมากกว่ารถเก๋ง", "รถบรรทุกไม่มีเบรก", "มวลไม่มีผลต่อการหยุดรถ", "รถเก๋งหยุดยากกว่ารถบรรทุกเสมอ เพราะรถเก๋งวิ่งเร็วกว่า",
      "ระยะห่างไม่เกี่ยวกับความปลอดภัย")),
    ("ผู้รักษาประตูรับลูกฟุตบอลได้ง่ายกว่ารับลูกเหล็กที่พุ่งมาเร็วเท่ากัน เพราะเหตุใด",
     "ลูกฟุตบอลมีมวลน้อยกว่า จึงทำให้หยุดได้ง่ายกว่า",
     ("ลูกฟุตบอลมีมวลมากกว่า", "ลูกเหล็กหยุดได้ง่ายกว่าเสมอ เพราะหนักจึงกลิ้งช้ากว่า", "มวลไม่เกี่ยวกับการหยุด", "ลูกฟุตบอลมีสีสดกว่า",
      "ลูกเหล็กไม่มีแรงโน้มถ่วง")),
    ("ในการแข่งรถของเล่นที่ผลักด้วยแรงเท่ากัน ทีมหนึ่งติดแบตเตอรี่ก้อนใหญ่เพิ่มบนรถ ผลที่น่าจะเกิดคืออะไร",
     "รถออกตัวช้าลง เพราะมวลรวมเพิ่มขึ้น",
     ("รถออกตัวเร็วขึ้น เพราะมวลเพิ่มขึ้น", "ไม่เปลี่ยนแปลง เพราะแรงผลักเท่าเดิม", "รถลอยขึ้นจากพื้น", "รถเปลี่ยนทิศเอง",
      "รถหยุดได้ง่ายขึ้น")),
)


MASS_SCENARIOS = (
    ("รถบรรทุกที่บรรทุกของเต็มคันต้องใช้ระยะเบรกยาวกว่ารถเก๋ง เพราะเหตุใด",
     "รถบรรทุกมีมวลมากกว่า จึงเปลี่ยนแปลงการเคลื่อนที่ให้หยุดได้ยากกว่า",
     ("รถบรรทุกมีมวลน้อยกว่า", "รถเก๋งไม่มีเบรก", "มวลไม่เกี่ยวกับการหยุดรถ")),
    ("นักเรียนต้องการให้รถของเล่นเร่งออกตัวได้เร็วที่สุดด้วยแรงผลักเท่าเดิม ควรทำอย่างไร",
     "เอาของที่บรรทุกบนรถออกเพื่อลดมวล",
     ("ใส่ของบนรถเพิ่มให้หนักขึ้น", "ทาสีรถใหม่", "เปลี่ยนล้อให้ใหญ่และหนักขึ้นโดยไม่ลดมวลส่วนอื่น")),
    ("ลูกโบว์ลิ่งกับลูกฟุตบอลขนาดใกล้กันกลิ้งมาด้วยความเร็วเท่ากัน ลูกใดหยุดด้วยมือได้ยากกว่า",
     "ลูกโบว์ลิ่ง เพราะมีมวลมากกว่า จึงเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่า",
     ("ลูกฟุตบอล เพราะมีมวลน้อยกว่า", "หยุดได้ยากเท่ากัน เพราะขนาดใกล้กัน", "ลูกฟุตบอล เพราะมีลมอยู่ข้างใน")),
)


@question_type(
    "phys.mass_motion_foundation",
    display_name={"th": "บอกความสัมพันธ์ระหว่างมวลกับการเปลี่ยนแปลงการเคลื่อนที่"},
    level=FOURTH, subject=SUBJECT, topic=MASS_TOPIC,
)
class MassMotionFoundation(QuestionType):
    """Which statement about mass and changing motion is true, or which of two is harder to move."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.7:
            (light, lm), (heavy, hm) = sorted(rng.sample(MASS_PAIRS, 2), key=lambda p: p[1])
            first, second = rng.sample(((light, lm), (heavy, hm)), 2)
            harder = rng.random() < 0.5
            pick = heavy if harder else light
            other = light if harder else heavy
            verb = rng.choice(("ผลักให้เริ่มเคลื่อนที่", "ทำให้หยุด", "ทำให้เปลี่ยนทิศทาง"))
            return _labelled(
                stem=(f"{first[0]} (มวล {first[1]} กิโลกรัม) กับ{second[0]} (มวล {second[1]} กิโลกรัม) "
                      f"ถ้าออกแรงเท่ากัน สิ่งใด{verb}ได้{'ยาก' if harder else 'ง่าย'}กว่า"),
                correct=f"{pick} เพราะมีมวล{'มาก' if harder else 'น้อย'}กว่า",
                wrongs=(f"{other} เพราะมีมวล{'น้อย' if harder else 'มาก'}กว่า", "ยากง่ายเท่ากัน เพราะออกแรงเท่ากัน",
                        f"{other} เพราะมีมวล{'มาก' if harder else 'น้อย'}กว่า"),
                hint="วัตถุที่มีมวลมากเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่า",
                topic=MASS_TOPIC,
            )
        return _labelled(
            stem=rng.choice(("ข้อใดกล่าวถึงมวลของวัตถุกับการเปลี่ยนแปลงการเคลื่อนที่ได้ถูกต้อง",
                             "ถ้าออกแรงเท่ากัน วัตถุแบบใดเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่า")),
            correct="วัตถุที่มีมวลมากเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่าวัตถุที่มีมวลน้อย",
            wrongs=("วัตถุที่มีมวลมากเปลี่ยนแปลงการเคลื่อนที่ได้ง่ายกว่าวัตถุที่มีมวลน้อย",
                    "มวลไม่มีผลต่อการเปลี่ยนแปลงการเคลื่อนที่ของวัตถุ",
                    "วัตถุที่มีมวลมากเคลื่อนที่ได้เองโดยไม่ต้องมีแรงกระทำ"),
            hint="นึกถึงการผลักรถเข็นเปล่ากับรถเข็นที่บรรทุกของเต็ม",
            topic=MASS_TOPIC,
        )


@question_type(
    "phys.mass_motion_fluency",
    display_name={"th": "บรรยายมวลของวัตถุที่มีผลต่อการเปลี่ยนแปลงการเคลื่อนที่จากหลักฐาน"},
    level=FOURTH, subject=SUBJECT, topic=MASS_TOPIC,
)
class MassMotionFluency(QuestionType):
    """Three carts of different mass, pushed alike; describe what the record shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        masses = sorted(rng.sample(range(1, 7), 3))
        distances = sorted(rng.sample(range(20, 121, 10), 3), reverse=True)
        rows = list(zip(("ก", "ข", "ค"), masses, distances))
        rng.shuffle(rows)
        record = " / ".join(f"รถ {label}: มวล {m} กิโลกรัม เคลื่อนที่ได้ {d} เซนติเมตร" for label, m, d in rows)
        heaviest = max(rows, key=lambda r: r[1])[0]
        lightest = min(rows, key=lambda r: r[1])[0]
        return _labelled(
            stem=(f"นักเรียนผลักรถทดลอง 3 คันด้วยแรงเท่ากันจากจุดเริ่มต้นเดียวกันบนพื้นเดียวกัน ได้ผลดังนี้ — {record} "
                  "จากหลักฐานนี้ ข้อใดบรรยายผลของมวลได้ถูกต้อง"),
            correct=f"รถ {heaviest} ซึ่งมีมวลมากที่สุดเคลื่อนที่ได้น้อยที่สุด แสดงว่าวัตถุที่มีมวลมากเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่า",
            wrongs=(f"รถ {heaviest} ซึ่งมีมวลมากที่สุดเคลื่อนที่ได้มากที่สุด แสดงว่าวัตถุที่มีมวลมากเปลี่ยนแปลงการเคลื่อนที่ได้ง่ายกว่า",
                    f"รถ {lightest} ซึ่งมีมวลน้อยที่สุดเคลื่อนที่ได้น้อยที่สุด แสดงว่ามวลน้อยทำให้เคลื่อนที่ยาก",
                    "รถทุกคันเคลื่อนที่ได้เท่ากัน แสดงว่ามวลไม่มีผลต่อการเคลื่อนที่",
                    # A true reading with a false conclusion.
                    f"รถ {lightest} ซึ่งมีมวลน้อยที่สุดเคลื่อนที่ได้มากที่สุด แสดงว่าวัตถุที่มีมวลน้อยเปลี่ยนแปลงการเคลื่อนที่ได้ยากกว่า",
                    f"รถ {heaviest} ซึ่งมีมวลมากที่สุดเคลื่อนที่ได้น้อยที่สุด แสดงว่ามวลไม่มีผลต่อการเปลี่ยนแปลงการเคลื่อนที่"),
            hint="เรียงรถตามมวล แล้วดูว่าระยะที่เคลื่อนที่ได้เปลี่ยนไปทางใด",
            topic=MASS_TOPIC,
        )


@question_type(
    "phys.mass_motion_application",
    display_name={"th": "ใช้ผลของมวลต่อการเคลื่อนที่อธิบายสถานการณ์"},
    level=FOURTH, subject=SUBJECT, topic=MASS_TOPIC,
)
class MassMotionApplication(QuestionType):
    """Authored cases, and planning with mass in mind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            case, right, wrongs = rng.choice(MASS_PLANS)
            return _labelled(stem=case, correct=right, wrongs=tuple(wrongs),
                             hint="มวลมากเปลี่ยนการเคลื่อนที่ได้ยาก ทั้งเริ่มเคลื่อนที่ เร่ง และหยุด", topic=MASS_TOPIC)
        return _retopic(scenario_question(
            rng, MASS_SCENARIOS,
            hint="มวลมากเปลี่ยนการเคลื่อนที่ได้ยาก ทั้งเริ่มเคลื่อนที่ เร่ง และหยุด",
        ), MASS_TOPIC)

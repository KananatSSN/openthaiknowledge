"""อัตราเร็วและความเร็วของการเคลื่อนที่

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/14

Sets moved here from: science_wave_d21.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO
from otk.sets._support.science_wave_d21 import _facts

PROVENANCE = Provenance("original")


SPEED_VELOCITY_TOPIC = "อัตราเร็วและความเร็วของการเคลื่อนที่"


SPEED_VELOCITY_CASES = (
    ("ข้อใดอธิบายความแตกต่างระหว่างอัตราเร็วกับความเร็วได้ถูกต้อง",
     "อัตราเร็วคือระยะทางหารด้วยเวลา เป็นสเกลาร์ ส่วนความเร็วคือการกระจัดหารด้วยเวลา เป็นเวกเตอร์",
     ("อัตราเร็วและความเร็วคำนวณจากสูตรเดียวกันเสมอ จึงมีค่าเท่ากันทุกกรณี",
      "อัตราเร็วเป็นเวกเตอร์ที่มีทิศทาง ส่วนความเร็วเป็นสเกลาร์ที่บอกเพียงขนาดโดยไม่มีทิศทาง",
      "อัตราเร็วหาจากการกระจัดหารด้วยเวลา ส่วนความเร็วหาจากระยะทางหารด้วยเวลา ทั้งสองเป็นสเกลาร์")),
    ("ปริมาณใดเป็นปริมาณเวกเตอร์ที่ต้องระบุทิศทางเสมอ",
     "ความเร็ว เพราะคำนวณจากการกระจัดซึ่งมีทิศทาง",
     ("อัตราเร็ว เพราะคำนวณจากระยะทางซึ่งมีทิศทาง",
      "ทั้งอัตราเร็วและความเร็วต่างก็เป็นปริมาณเวกเตอร์",
      "ทั้งอัตราเร็วและความเร็วต่างก็เป็นปริมาณสเกลาร์")),
)


SPEED_HINT = "อัตราเร็วมาจากระยะทาง (เส้นทางจริง) ไม่มีทิศทาง ความเร็วมาจากการกระจัด (เส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย) มีทิศทาง"


SPEED_FACTS = (
    ("สูตรใดใช้คำนวณอัตราเร็วเฉลี่ย", "ระยะทาง ÷ เวลา",
     ("การกระจัด ÷ เวลา", "เวลา ÷ ระยะทาง", "ระยะทาง × เวลา", "การกระจัด × เวลา", "มวล ÷ เวลา")),
    ("สูตรใดใช้คำนวณความเร็วเฉลี่ย", "การกระจัด ÷ เวลา",
     ("ระยะทาง ÷ เวลา", "เวลา ÷ การกระจัด", "การกระจัด × เวลา", "ระยะทาง × เวลา", "แรง ÷ เวลา")),
    ("หน่วยของอัตราเร็วและความเร็วในระบบเอสไอคือข้อใด", "เมตรต่อวินาที",
     ("เมตร", "วินาที", "นิวตัน", "เมตรต่อวินาทีกำลังสอง", "กิโลกรัมต่อเมตร")),
    ("การกระจัดต่างจากระยะทางอย่างไร", "การกระจัดวัดเป็นเส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้ายและมีทิศทาง ส่วนระยะทางวัดตามเส้นทางจริง",
     ("การกระจัดวัดตามเส้นทางจริงและไม่มีทิศทาง ส่วนระยะทางวัดเป็นเส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย", "ทั้งสองเหมือนกันทุกกรณี", "ระยะทางมีทิศทางเพราะวัดตามเส้นทางจริง ส่วนการกระจัดวัดเป็นเส้นตรงและไม่มีทิศทาง",
      "การกระจัดมากกว่าระยะทางเสมอ", "ระยะทางเป็นศูนย์ได้เมื่อกลับมาที่เดิม")),
    ("เมื่อใดขนาดของความเร็วเฉลี่ยเท่ากับอัตราเร็วเฉลี่ย", "เมื่อเคลื่อนที่เป็นเส้นตรงทิศเดียวโดยไม่ย้อนกลับ",
     ("เมื่อเคลื่อนที่เป็นวงกลมครบหนึ่งรอบพอดี", "เมื่อเดินไปแล้วย้อนกลับมาที่จุดเริ่มต้นเดิม", "ไม่มีกรณีใดเท่ากันได้", "เมื่อเคลื่อนที่เลี้ยวไปมาหลายครั้งแต่ไปทางเดียว",
      "เมื่อใช้เวลานานมาก")),
)


SPEED_VELOCITY_SCENARIOS = (
    ("นักวิ่งวิ่งรอบสนามหนึ่งรอบแล้วกลับมาที่จุดเริ่มต้นพอดี ใช้เวลา 2 นาที ข้อใดถูกต้อง",
     "อัตราเร็วเฉลี่ยมีค่ามากกว่าศูนย์ แต่ความเร็วเฉลี่ยเป็นศูนย์ เพราะการกระจัดเป็นศูนย์",
     ("อัตราเร็วและความเร็วเฉลี่ยเป็นศูนย์ทั้งคู่ เพราะกลับมาหยุดที่จุดเริ่มต้นเดิม", "อัตราเร็วและความเร็วเฉลี่ยมีค่าเท่ากันและมากกว่าศูนย์ เพราะวิ่งด้วยอัตราเร็วคงที่", "ความเร็วเฉลี่ยมากกว่าอัตราเร็วเฉลี่ย เพราะการกระจัดมากกว่าระยะทางเสมอ")),
    ("มาตรวัดความเร็วบนหน้าปัดรถยนต์แสดงค่าอะไร",
     "อัตราเร็ว เพราะแสดงเฉพาะขนาดโดยไม่ระบุทิศทางการเคลื่อนที่",
     ("ความเร็ว เพราะมาตรวัดแสดงทั้งขนาดและทิศทางของการเคลื่อนที่", "ทั้งอัตราเร็วและความเร็วพร้อมกัน เพราะสองค่านี้เท่ากันเสมอ", "ระยะทางสะสมทั้งหมดที่รถวิ่งมา")),
    ("รถวิ่งเป็นเส้นตรงไปทิศเหนือโดยไม่เลี้ยวหรือถอยหลังเลย ข้อใดถูกต้องเกี่ยวกับอัตราเร็วและความเร็วของรถ",
     "อัตราเร็วและขนาดของความเร็วเท่ากัน เพราะระยะทางเท่ากับขนาดของการกระจัดในเส้นทางตรง",
     ("อัตราเร็วมากกว่าขนาดของความเร็วเสมอ เพราะระยะทางมากกว่าการกระจัดทุกกรณี", "ขนาดของความเร็วมากกว่าอัตราเร็ว เพราะความเร็วรวมทิศทางเข้าไปด้วย", "ไม่สามารถบอกความเร็วได้ เพราะรถวิ่งตรงไปโดยไม่เลี้ยวจึงไม่มีทิศทางให้ระบุ")),
)


@question_type(
    "phys.speed_velocity_foundation",
    display_name={"th": "อธิบายความแตกต่างระหว่างอัตราเร็วและความเร็ว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SPEED_VELOCITY_TOPIC,
)
class SpeedVelocityFoundation(QuestionType):
    """Speed as a scalar from distance; velocity as a vector from displacement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return _facts(rng, SPEED_FACTS, hint=SPEED_HINT, topic=SPEED_VELOCITY_TOPIC)
        if roll < 0.8:
            mover, low, high, unit = rng.choice((
                ("รถยนต์", 30, 120, "กิโลเมตรต่อชั่วโมง"), ("นักวิ่ง", 2, 9, "เมตรต่อวินาที"),
                ("เรือ", 10, 40, "กิโลเมตรต่อชั่วโมง"), ("นกพิราบ", 8, 20, "เมตรต่อวินาที"),
                ("รถไฟ", 60, 160, "กิโลเมตรต่อชั่วโมง"), ("นักปั่นจักรยาน", 4, 12, "เมตรต่อวินาที")))
            value = rng.randint(low, high)
            way = rng.choice(("เหนือ", "ใต้", "ตะวันออก", "ตะวันตก"))
            vector = rng.random() < 0.5
            said = f"{value} {unit} ไปทางทิศ{way}" if vector else f"{value} {unit}"
            return _labelled(
                stem=f"\"{mover}เคลื่อนที่ {said}\" ข้อมูลนี้บอกปริมาณใด",
                correct=("ความเร็ว เพราะบอกทั้งขนาดและทิศทาง" if vector else "อัตราเร็ว เพราะบอกเพียงขนาด ไม่ได้บอกทิศทาง"),
                wrongs=(("อัตราเร็ว เพราะบอกเพียงขนาด ไม่ได้บอกทิศทาง" if vector else "ความเร็ว เพราะบอกทั้งขนาดและทิศทาง"),
                        "การกระจัด เพราะมีหน่วยเป็นเมตร", "ระยะทาง เพราะบอกว่าไปได้ไกลเท่าใด"),
                hint=SPEED_HINT, topic=SPEED_VELOCITY_TOPIC,
            )
        stem, correct, wrongs = rng.choice(SPEED_VELOCITY_CASES)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="อัตราเร็วมาจากระยะทาง (เส้นทางจริง) ความเร็วมาจากการกระจัด (เส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย)",
            topic=SPEED_VELOCITY_TOPIC,
        )


@question_type(
    "phys.speed_velocity_fluency",
    display_name={"th": "คำนวณอัตราเร็วและความเร็วจากหลักฐานเชิงประจักษ์โดยใช้สมการ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SPEED_VELOCITY_TOPIC,
)
class SpeedVelocityFluency(QuestionType):
    """A curved run with a known path length and a shorter straight displacement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        time = rng.choice((2, 4, 5, 10))
        speed = rng.choice((2, 3, 4, 5, 6))
        velocity = rng.choice([v for v in (1, 2, 3, 4, 5) if v < speed])
        distance = speed * time
        displacement = velocity * time

        def answer(speed_val: float, velocity_val: float, direction: bool) -> str:
            tail = " ในทิศจาก A ไป B" if direction else ""
            return (f"อัตราเร็ว: {distance} ÷ {time} = {speed_val:g} เมตรต่อวินาที / "
                    f"ความเร็ว: {displacement} ÷ {time} = {velocity_val:g} เมตรต่อวินาที{tail}")

        return _labelled(
            stem=(f"นักวิ่งวิ่งจากจุด A ไปจุด B ตามทางโค้ง ระยะทางที่วิ่งจริงคือ {distance} เมตร "
                  f"แต่การกระจัดจาก A ไป B วัดได้ {displacement} เมตร ใช้เวลา {time} วินาที "
                  "จากหลักฐานนี้ ข้อใดคำนวณอัตราเร็วและความเร็วได้ถูกต้องทั้งหมด"),
            correct=answer(speed, velocity, True),
            wrongs=(answer(velocity, speed, True),
                    answer(speed, speed, True),
                    answer(speed, velocity, False),
                    # Two parts wrong at once.
                    answer(velocity, speed, False),
                    answer(speed, speed, False)),
            hint="อัตราเร็ว = ระยะทาง ÷ เวลา ความเร็ว = การกระจัด ÷ เวลา และต้องระบุทิศทางของความเร็วด้วย",
            topic=SPEED_VELOCITY_TOPIC,
        )


@question_type(
    "phys.speed_velocity_application",
    display_name={"th": "ใช้อัตราเร็วและความเร็วอธิบายการเคลื่อนที่จริง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SPEED_VELOCITY_TOPIC,
)
class SpeedVelocityApplication(QuestionType):
    """Authored cases, and an out-and-back trip along a straight road."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            time = rng.choice((40, 50, 100))  # any multiple of 10 m over these is exact to 2 dp
            out = rng.randrange(20, 201, 10)
            back = rng.choice((out, rng.randrange(10, out, 10) if out > 10 else out))
            speed = Fraction(out + back, time)
            velocity = Fraction(out - back, time)
            walker = rng.choice(("นักเรียน", "สุนัข", "รถของเล่นบังคับวิทยุ", "นักวิ่ง"))
            tail = "" if velocity == 0 else " ไปทางทิศตะวันออก"
            correct = f"อัตราเร็วเฉลี่ย {show(speed)} เมตรต่อวินาที / ความเร็วเฉลี่ย {show(velocity)} เมตรต่อวินาที{tail}"
            wrongs = [f"อัตราเร็วเฉลี่ย {show(velocity)} เมตรต่อวินาที / ความเร็วเฉลี่ย {show(speed)} เมตรต่อวินาที ไปทางทิศตะวันออก",
                      f"อัตราเร็วเฉลี่ย {show(speed)} เมตรต่อวินาที / ความเร็วเฉลี่ย {show(speed)} เมตรต่อวินาที ไปทางทิศตะวันออก",
                      f"อัตราเร็วเฉลี่ย {show(speed)} เมตรต่อวินาที / ความเร็วเฉลี่ย {show(velocity)} เมตรต่อวินาที ไปทางทิศตะวันตก",
                      f"อัตราเร็วเฉลี่ย {show(Fraction(out, time))} เมตรต่อวินาที / ความเร็วเฉลี่ย {show(velocity)} เมตรต่อวินาที{tail}"]
            return _labelled(
                stem=(f"{walker}เคลื่อนที่บนถนนตรงไปทางทิศตะวันออก {out} เมตร แล้วย้อนกลับไปทางทิศตะวันตก {back} เมตร "
                      f"ใช้เวลารวม {time} วินาที ข้อใดถูกต้อง"),
                correct=correct,
                wrongs=tuple(w for w in dict.fromkeys(wrongs) if w != correct)[:3],
                hint="อัตราเร็วใช้ระยะทางรวมทั้งไปและกลับ ความเร็วใช้การกระจัดจากจุดเริ่มต้นถึงจุดสุดท้าย",
                topic=SPEED_VELOCITY_TOPIC,
            )
        return _retopic(scenario_question(
            rng, SPEED_VELOCITY_SCENARIOS,
            hint="ความเร็วเป็นศูนย์ได้แม้อัตราเร็วไม่เป็นศูนย์ เมื่อการกระจัดเป็นศูนย์แต่ระยะทางไม่เป็นศูนย์",
        ), SPEED_VELOCITY_TOPIC)

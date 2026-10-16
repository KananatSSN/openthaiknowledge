"""พลังงานความร้อนกับการเปลี่ยนสถานะ

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/10

Sets moved here from: science_wave_d8.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d7 import SECONDARY_ONE

PROVENANCE = Provenance("original")


HEAT_TOPIC = "พลังงานความร้อนกับการเปลี่ยนสถานะ"


class Change(NamedTuple):
    substance: str
    start_state: str
    end_state: str
    plateau: int      # °C
    below: bool       # heated up to the plateau from below


CHANGES = (
    Change("น้ำแข็ง", "ของแข็ง", "ของเหลว", 0, True),
    Change("น้ำ", "ของเหลว", "แก๊ส", 100, True),
    Change("แนฟทาลีน", "ของแข็ง", "ของเหลว", 80, True),
)


def heating_record(rng: Random, change: Change) -> tuple[list[int], int, int]:
    """Temperatures each minute; the plateau runs from ``start`` to ``end``."""
    rise = rng.choice((4, 5))
    start = rng.randint(2, 3)
    length = rng.randint(3, 4)
    end = start + length
    temps = []
    for minute in range(end + 3):
        if minute < start:
            temps.append(change.plateau - rise * (start - minute))
        elif minute <= end:
            temps.append(change.plateau)
        else:
            temps.append(change.plateau + rise * (minute - end))
    return temps, start, end


def heat_parts(change: Change, start: int, end: int, wrong_start: int, wrong_end: int) -> tuple[Part, ...]:
    return (
        Part("ช่วงที่เปลี่ยนสถานะ", f"นาทีที่ {start} ถึง {end} ซึ่งอุณหภูมิคงที่ที่ {change.plateau} องศาเซลเซียส",
             f"นาทีที่ {wrong_start} ถึง {wrong_end} ซึ่งอุณหภูมิสูงขึ้นต่อเนื่อง"),
        Part("พลังงานความร้อน",
             f"สารยังได้รับความร้อน แต่ความร้อนถูกใช้เปลี่ยนสถานะจาก{change.start_state}เป็น{change.end_state} อุณหภูมิจึงไม่เพิ่ม",
             "สารไม่ได้รับความร้อนในช่วงนั้น อุณหภูมิจึงไม่เพิ่ม"),
        Part("แบบจำลองอนุภาค",
             "ความร้อนทำให้อนุภาคเอาชนะแรงยึดเหนี่ยวระหว่างกัน อนุภาคจึงอยู่ห่างกันและเคลื่อนที่ได้อิสระมากขึ้น",
             "ความร้อนทำให้อนุภาคมีขนาดใหญ่ขึ้นและอยู่ชิดกันมากขึ้น"),
    )


# Second false readings of the energy and particle parts, drawn at Fluency.
ENERGY_SLIP = "ความร้อนทั้งหมดหนีออกไปสู่อากาศโดยไม่ถึงสาร อุณหภูมิจึงไม่เพิ่ม"


PARTICLE_SLIP = "อนุภาคหยุดเคลื่อนที่ชั่วคราวระหว่างเปลี่ยนสถานะ อุณหภูมิจึงคงที่"


HEAT_SCENARIOS = (
    ("เหตุใดไอน้ำที่ 100 องศาเซลเซียสลวกผิวหนังได้รุนแรงกว่าน้ำเดือดที่ 100 องศาเซลเซียส",
     "เมื่อไอน้ำควบแน่นบนผิวหนังจะคายความร้อนที่ใช้ในการกลายเป็นไอออกมาเพิ่มอีก",
     ("ไอน้ำมีอุณหภูมิสูงกว่าน้ำเดือดเสมอ",
      "น้ำเดือดไม่มีความร้อนเหลืออยู่",
      "ไอน้ำดูดความร้อนจากผิวหนังเมื่อควบแน่น",
      "อนุภาคของไอน้ำมีขนาดใหญ่กว่าอนุภาคของน้ำ",
      "น้ำเดือดคายความร้อนออกหมดก่อนถึงผิวหนัง")),
    ("แม่ค้าวางน้ำแข็งไว้บนกล่องใส่ปลาแทนการใช้น้ำเย็นที่อุณหภูมิ 0 องศาเซลเซียสเท่ากัน เพราะเหตุใดน้ำแข็งจึงรักษาความเย็นได้นานกว่า",
     "น้ำแข็งต้องดูดความร้อนจำนวนมากเพื่อหลอมเหลวโดยอุณหภูมิไม่เพิ่ม จึงดึงความร้อนจากปลาได้นานกว่า",
     ("น้ำแข็งมีอุณหภูมิต่ำกว่า 0 องศาเซลเซียสเสมอ",
      "น้ำเย็นคายความร้อนให้ปลา",
      "น้ำแข็งไม่ดูดความร้อนจากสิ่งใดเลย",
      "น้ำแข็งคายความร้อนให้ปลาจึงเย็น",
      "น้ำเย็นดูดความร้อนได้มากกว่าน้ำแข็ง")),
    ("ขณะต้มน้ำในหม้อที่เดือดแล้ว ถ้าเร่งไฟให้แรงขึ้น อุณหภูมิของน้ำที่ความดันปกติจะเป็นอย่างไร",
     "คงที่ประมาณ 100 องศาเซลเซียส แต่น้ำกลายเป็นไอเร็วขึ้น เพราะความร้อนที่เพิ่มถูกใช้เปลี่ยนสถานะ",
     ("สูงขึ้นเรื่อย ๆ ตามความแรงของไฟ",
      "ลดลง เพราะน้ำกลายเป็นไอมากขึ้น",
      "คงที่ และน้ำกลายเป็นไอช้าลง",
      "สูงขึ้นเป็น 120 องศาเซลเซียสทันที",
      "ลดลงเหลือ 90 องศาเซลเซียส เพราะน้ำระเหยไปหมด")),
    ("เหตุใดเมื่อทาแอลกอฮอล์บนผิวหนังจึงรู้สึกเย็น",
     "แอลกอฮอล์ระเหยโดยดูดความร้อนจากผิวหนังไปใช้ในการกลายเป็นไอ",
     ("แอลกอฮอล์คายความร้อนให้ผิวหนัง",
      "แอลกอฮอล์มีอุณหภูมิต่ำกว่า 0 องศาเซลเซียสเสมอ",
      "แอลกอฮอล์ควบแน่นบนผิวหนัง",
      "ผิวหนังดูดแอลกอฮอล์เข้าไปทั้งหมด",
      "แอลกอฮอล์ทำให้อนุภาคของผิวหนังชิดกันขึ้น")),
    ("หยดน้ำเกาะรอบแก้วน้ำเย็นจัดในวันที่อากาศร้อนชื้น ข้อใดอธิบายได้ถูกต้อง",
     "ไอน้ำในอากาศคายความร้อนให้ผิวแก้วที่เย็น แล้วควบแน่นเป็นหยดน้ำ",
     ("น้ำในแก้วซึมผ่านผิวแก้วออกมา",
      "ไอน้ำดูดความร้อนจากแก้วแล้วกลายเป็นน้ำ",
      "น้ำแข็งในแก้วระเหิดออกมาเกาะผิวแก้ว",
      "แก้วคายความร้อนให้อากาศจนเกิดหยดน้ำ",
      "อากาศร้อนหลอมผิวแก้วเป็นหยดน้ำ")),
)


@question_type(
    "chem.heat_state_change_foundation",
    display_name={"th": "บอกการดูดหรือคายความร้อนเมื่อสสารเปลี่ยนสถานะ"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class HeatStateChangeFoundation(QuestionType):
    """One change of state; whether heat is taken in or given out."""

    CASES = (
        ("การหลอมเหลว (ของแข็งเป็นของเหลว)", True), ("การกลายเป็นไอ (ของเหลวเป็นแก๊ส)", True),
        ("การระเหิด (ของแข็งเป็นแก๊ส)", True), ("การแข็งตัว (ของเหลวเป็นของแข็ง)", False),
        ("การควบแน่น (แก๊สเป็นของเหลว)", False), ("การระเหิดกลับ (แก๊สเป็นของแข็ง)", False),
        # The same six changes met in daily life.
        ("การที่ก้อนน้ำแข็งในแก้วละลายเป็นน้ำ", True),
        ("การที่น้ำในหม้อเดือดกลายเป็นไอ", True),
        ("การที่ลูกเหม็นในตู้เสื้อผ้าค่อย ๆ เล็กลงจนหมดไป", True),
        ("การที่เนื้อเทียนรอบไส้หลอมเหลวเมื่อจุดไฟ", True),
        ("การที่น้ำในถาดกลายเป็นก้อนน้ำแข็งในช่องแช่แข็ง", False),
        ("การที่มีหยดน้ำเกาะอยู่รอบนอกแก้วน้ำเย็น", False),
        ("การที่ไอน้ำในอากาศกลายเป็นเกล็ดน้ำแข็งบนยอดหญ้าในคืนที่หนาวจัด", False),
        ("การที่น้ำตาเทียนแข็งตัวเมื่อไหลลงมาตามแท่งเทียน", False),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change, absorbs = rng.choice(self.CASES)
        take = "สารดูดความร้อน อนุภาคจึงแยกห่างกันมากขึ้น"
        give = "สารคายความร้อน อนุภาคจึงเข้ามาอยู่ชิดกันมากขึ้น"
        return _labelled(
            stem=f"ข้อใดอธิบาย{change}ได้ถูกต้อง",
            correct=take if absorbs else give,
            wrongs=(give if absorbs else take,
                    "สารไม่ดูดและไม่คายความร้อน เพราะอุณหภูมิคงที่",
                    "สารดูดความร้อน อนุภาคจึงเข้ามาอยู่ชิดกันมากขึ้น" if absorbs
                    else "สารคายความร้อน อนุภาคจึงแยกห่างกันมากขึ้น",
                    "อนุภาคของสารมีขนาดใหญ่ขึ้นเมื่อเปลี่ยนสถานะ",
                    "จำนวนอนุภาคของสารเพิ่มขึ้นเมื่อเปลี่ยนสถานะ"),
            hint="เปลี่ยนไปเป็นสถานะที่อนุภาคห่างกันกว่าต้องได้รับความร้อน ย้อนกลับต้องคายความร้อน",
            topic=HEAT_TOPIC,
        )


@question_type(
    "chem.heat_state_change_fluency",
    display_name={"th": "อธิบายความสัมพันธ์ของพลังงานความร้อนกับการเปลี่ยนสถานะจากข้อมูลการทดลอง"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class HeatStateChangeFluency(QuestionType):
    """A heating record; explain the interval, the heat and the particles together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change = rng.choice(CHANGES)
        temps, start, end = heating_record(rng, change)
        wrong_start, wrong_end = end + 1, len(temps) - 1
        record = ", ".join(f"นาทีที่ {minute}: {t}" for minute, t in enumerate(temps))
        interval, energy, particles = heat_parts(change, start, end, wrong_start, wrong_end)
        energy = energy._replace(false=rng.choice((energy.false, ENERGY_SLIP)))
        particles = particles._replace(false=rng.choice((particles.false, PARTICLE_SLIP)))
        return parts_item(
            rng, (interval, energy, particles),
            stem=(f"นักเรียนให้ความร้อนแก่{change.substance}อย่างสม่ำเสมอ และบันทึกอุณหภูมิ (องศาเซลเซียส) ทุก 1 นาที — "
                  f"{record} จากหลักฐานและแบบจำลองอนุภาค ข้อใดอธิบายได้ถูกต้องทั้งหมด"),
            hint="หาช่วงที่อุณหภูมิไม่เปลี่ยนแม้ยังให้ความร้อน แล้วนึกว่าความร้อนนั้นไปทำอะไรกับอนุภาค",
            topic=HEAT_TOPIC,
        )


@question_type(
    "chem.heat_state_change_application",
    display_name={"th": "ใช้ความสัมพันธ์ของความร้อนกับการเปลี่ยนสถานะในชีวิตประจำวัน"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=HEAT_TOPIC,
)
class HeatStateChangeApplication(QuestionType):
    """Steam burns, ice on fish, and turning up the flame under boiling water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, HEAT_SCENARIOS,
            hint="ระหว่างเปลี่ยนสถานะ ความร้อนถูกดูดหรือคายโดยอุณหภูมิไม่เปลี่ยน",
        ), HEAT_TOPIC)


# More rows: the set drew from five, so a learner met them all in a few
# tries. Each added row is a situation no other row describes, since every
# row's answer is a distractor for the others, and has five wrong readings.
HEAT_SCENARIOS += (
    ('น้ำแข็งที่ 0 องศาเซลเซียสกำลังละลาย ระหว่างละลายอุณหภูมิของน้ำแข็งกับน้ำเป็นอย่างไร แม้ได้รับความร้อนต่อเนื่อง',
     'คงที่ที่ 0 องศาเซลเซียส เพราะความร้อนถูกใช้ในการเปลี่ยนสถานะ',
     ('เพิ่มขึ้นเรื่อย ๆ ระหว่างละลาย', 'ลดลงต่ำกว่า 0 องศาเซลเซียส', 'เพิ่มขึ้นเป็น 100 องศาเซลเซียสทันที', 'ขึ้นลงสลับกันไปมา', 'ไม่มีอุณหภูมิระหว่างละลาย')),
    ('บนยอดเขาสูง น้ำเดือดที่อุณหภูมิต่ำกว่า 100 องศาเซลเซียส เพราะเหตุใด',
     'ความดันอากาศบนยอดเขาต่ำกว่า น้ำจึงเดือดได้ที่อุณหภูมิต่ำกว่า',
     ('บนยอดเขามีออกซิเจนมากกว่า', 'น้ำบนยอดเขาเป็นน้ำคนละชนิด', 'ยอดเขาอยู่ใกล้ดวงอาทิตย์มากกว่า', 'ความดันอากาศบนยอดเขาสูงกว่า', 'ความร้อนจากเตาบนยอดเขาแรงกว่า')),
    ('เหตุใดหม้อดินเผาที่ใส่น้ำและตั้งไว้ในที่มีลมพัดจึงทำให้น้ำในหม้อเย็นลงได้',
     'น้ำซึมออกมาระเหยที่ผิวหม้อ การระเหยดึงความร้อนออกจากน้ำในหม้อ',
     ('ลมพัดความเย็นจากขั้วโลกมา', 'ดินเผาผลิตความเย็นออกมาเอง', 'น้ำในหม้อกลายเป็นน้ำแข็งทันที', 'การควบแน่นทำให้น้ำเย็นลง', 'หม้อดินเผาดูดความร้อนจากลมเข้าไปในน้ำ')),
    ('การนึ่งอาหารด้วยไอน้ำทำให้อาหารสุกเร็ว เพราะเหตุใด',
     'ไอน้ำควบแน่นบนอาหารและคายความร้อนแฝงออกมาให้อาหารจำนวนมาก',
     ('ไอน้ำเย็นกว่าน้ำเดือดมาก', 'ไอน้ำไม่มีความร้อนแฝง', 'ไอน้ำทำให้อาหารแห้งเท่านั้น', 'อาหารดูดน้ำเข้าไปจนสุกเอง', 'ไอน้ำระเหยออกจากอาหารแล้วทำให้อาหารร้อน')),
)

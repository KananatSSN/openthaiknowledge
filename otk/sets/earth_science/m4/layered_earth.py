"""โครงสร้างโลก

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/1

Sets moved here from: science_wave_f74.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f74 import GEOLOGY, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_LAYERS = "โครงสร้างโลก"


LAYERS = (
    ("เปลือกโลก", "ชั้นนอกสุด เป็นของแข็ง แบ่งเป็นเปลือกโลกทวีปและเปลือกโลกมหาสมุทร"),
    ("เนื้อโลก", "อยู่ใต้เปลือกโลก หนาที่สุด ส่วนบนบางช่วงหลอมเหลวบางส่วนและไหลได้ช้า"),
    ("แก่นโลกชั้นนอก", "เป็นของเหลว ประกอบด้วยเหล็กและนิกเกิล คลื่น S ผ่านไม่ได้"),
    ("แก่นโลกชั้นใน", "เป็นของแข็งที่มีความดันและอุณหภูมิสูงมาก ประกอบด้วยเหล็กและนิกเกิล"),
    ("ธรณีภาค", "ชั้นแข็งที่รวมเปลือกโลกกับเนื้อโลกส่วนบนสุด แตกเป็นแผ่นธรณี"),
    ("ฐานธรณีภาค", "ชั้นใต้ธรณีภาคที่เป็นของแข็งร้อนและไหลได้ช้า"),
)


BOUNDARIES = (("แนวไม่ต่อเนื่องโมโฮโรวิซิก", "ระหว่างเปลือกโลกกับเนื้อโลก"), ("แนวไม่ต่อเนื่องกูเทนเบิร์ก", "ระหว่างเนื้อโลกกับแก่นโลกชั้นนอก"),
              ("แนวไม่ต่อเนื่องเลห์มันน์", "ระหว่างแก่นโลกชั้นนอกกับแก่นโลกชั้นใน"))


LAYERS_HINT = ("เปลือกโลก → (โมโฮ) → เนื้อโลก → (กูเทนเบิร์ก) → แก่นโลกชั้นนอกที่เป็นของเหลว → (เลห์มันน์) → แก่นโลกชั้นในที่เป็นของแข็ง "
               "คลื่น P ผ่านได้ทั้งของแข็งและของเหลว คลื่น S ผ่านได้เฉพาะของแข็ง")


SEISMIC = (
    ("หลักฐานใดบอกว่าแก่นโลกชั้นนอกเป็นของเหลว", "คลื่น S ไม่สามารถเคลื่อนที่ผ่านแก่นโลกชั้นนอกได้",
     ("คลื่น P เคลื่อนที่เร็วขึ้นในแก่นโลกชั้นนอก", "คลื่น S เคลื่อนที่เร็วขึ้นในแก่นโลกชั้นนอก", "คลื่น P ไม่สามารถเคลื่อนที่ผ่านแก่นโลกชั้นนอกได้", "คลื่นผิวพื้นเคลื่อนที่ผ่านได้")),
    ("เขตเงาของคลื่น S เกิดขึ้นเพราะเหตุใด", "คลื่น S ผ่านแก่นโลกชั้นนอกที่เป็นของเหลวไม่ได้",
     ("คลื่น S ผ่านแก่นโลกชั้นในที่เป็นของแข็งไม่ได้", "เปลือกโลกดูดกลืนคลื่น S ทั้งหมด", "คลื่น S สะท้อนที่ผิวโลกเท่านั้น", "คลื่น S ผ่านแก่นโลกชั้นนอกได้ แต่ช้าลงมาก")),
    ("ความเร็วของคลื่นไหวสะเทือนที่เปลี่ยนไปอย่างฉับพลันบอกอะไร", "มีรอยต่อระหว่างชั้นที่มีสมบัติต่างกัน",
     ("มีแผ่นดินไหวเกิดขึ้นใหม่", "ชั้นหินทุกชั้นมีสมบัติเหมือนกัน", "คลื่นหยุดเคลื่อนที่ชั่วคราวที่รอยต่อ", "ชั้นหินมีอายุเท่ากัน")),
    ("เปลือกโลกทวีปต่างจากเปลือกโลกมหาสมุทรอย่างไร", "หนากว่าและมีความหนาแน่นน้อยกว่า ประกอบด้วยหินแกรนิตเป็นส่วนใหญ่",
     ("บางกว่าและหนาแน่นกว่า เป็นหินบะซอลต์", "หนากว่าและหนาแน่นมากกว่า ประกอบด้วยเหล็กและนิกเกิลเป็นส่วนใหญ่", "มีอายุน้อยกว่าเสมอ", "บางกว่าและหนาแน่นกว่า ประกอบด้วยหินบะซอลต์เป็นส่วนใหญ่")),
    ("เขตเงาของคลื่น P เกิดขึ้นเพราะเหตุใด", "คลื่น P หักเหเมื่อผ่านรอยต่อระหว่างเนื้อโลกกับแก่นโลก ทำให้บางบริเวณไม่ได้รับคลื่น",
     ("คลื่น P ผ่านของเหลวไม่ได้", "คลื่น P ถูกดูดกลืนในเปลือกโลก", "คลื่น P เดินทางได้เฉพาะบนผิวโลก", "คลื่น P ผ่านของเหลวไม่ได้ จึงหยุดเคลื่อนที่ที่รอยต่อเนื้อโลกกับแก่นโลก", "คลื่น P ถูกดูดกลืนหมดในเปลือกโลก ทำให้บางบริเวณไม่ได้รับคลื่น")),
    ("ชั้นใดของโลกมีปริมาตรมากที่สุด", "เนื้อโลก", ("เปลือกโลก", "แก่นโลกชั้นนอก", "แก่นโลกชั้นใน", "ธรณีภาค", "บรรยากาศ")),
    ("เหตุใดแก่นโลกชั้นในจึงเป็นของแข็งทั้งที่ร้อนกว่าแก่นโลกชั้นนอก", "ความดันสูงมากทำให้เหล็กและนิกเกิลคงสถานะเป็นของแข็ง",
     ("อุณหภูมิต่ำกว่าผิวโลก", "ประกอบด้วยหินแกรนิต", "ประกอบด้วยหินแกรนิตที่มีจุดหลอมเหลวสูงมาก", "อุณหภูมิต่ำกว่าผิวโลกมาก เหล็กและนิกเกิลจึงแข็งตัว")),
)


# (layer, top depth km, bottom depth km)
DEPTHS = (("เปลือกโลกทวีปโดยเฉลี่ย", 0, 35), ("เนื้อโลก", 35, 2900), ("แก่นโลกชั้นนอก", 2900, 5150), ("แก่นโลกชั้นใน", 5150, 6370))


@question_type(
    "geo.layered_earth_foundation",
    display_name={"th": "ชั้นและสมบัติของโครงสร้างโลก"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_LAYERS,
)
class LayeredEarthFoundation(QuestionType):
    """Each layer and each boundary."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            name, where = rng.choice(BOUNDARIES)
            others = [b for b in BOUNDARIES if b[0] != name]
            if rng.random() < 0.5:
                return _labelled(stem=f"{name}อยู่ที่ใด", correct=where, wrongs=(*(b[1] for b in others), "ระหว่างบรรยากาศกับเปลือกโลก"),
                                 topic=TOPIC_LAYERS, hint=LAYERS_HINT)
            return _labelled(stem=f"รอยต่อ{where}เรียกว่าอะไร", correct=name, wrongs=(*(b[0] for b in others), "แนวรอยเลื่อนแซนแอนเดรียส"),
                             topic=TOPIC_LAYERS, hint=LAYERS_HINT)
        name, what = rng.choice(LAYERS)
        others = rng.sample([ell for ell in LAYERS if ell[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีลักษณะอย่างไร", correct=what, wrongs=tuple(ell[1] for ell in others), topic=TOPIC_LAYERS, hint=LAYERS_HINT)
        return _labelled(stem=f"ชั้นใดของโลก{what}", correct=name, wrongs=tuple(ell[0] for ell in others), topic=TOPIC_LAYERS, hint=LAYERS_HINT)


@question_type(
    "geo.layered_earth_fluency",
    display_name={"th": "หลักฐานจากคลื่นไหวสะเทือนที่บอกโครงสร้างโลก"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_LAYERS,
)
class LayeredEarthFluency(QuestionType):
    """What P and S waves reveal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(SEISMIC)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LAYERS, hint=LAYERS_HINT)


@question_type(
    "geo.layered_earth_application",
    display_name={"th": "คำนวณความหนาของชั้นโลกและเวลาเดินทางของคลื่น"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_LAYERS,
)
class LayeredEarthApplication(QuestionType):
    """Thickness from boundary depths; travel time = distance ÷ speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, top, bottom = rng.choice(DEPTHS)
            return numeric(stem=f"ถ้า{name}อยู่ที่ความลึก {top:,} ถึง {bottom:,} km จากผิวโลก ชั้นนี้หนากี่กิโลเมตร", answer=bottom - top,
                           wrongs=[bottom + top, bottom, top or bottom // 2], unit="km", topic=TOPIC_LAYERS,
                           hint="ความหนา = ความลึกของขอบล่าง − ความลึกของขอบบน")
        wave = rng.choice((("P", (6, 8, 10, 12, 13)), ("S", (4, 5, 6, 7))))
        speed = rng.choice(wave[1])
        seconds = rng.randrange(10, 601, 10)
        distance = speed * seconds
        if rng.random() < 0.5:
            return numeric(stem=f"คลื่น {wave[0]} เคลื่อนที่ด้วยอัตราเร็วเฉลี่ย {speed} km/s ระยะทาง {distance:,} km ใช้เวลากี่วินาที", answer=seconds,
                           wrongs=[distance * speed, Fraction(seconds, 60) if (Fraction(seconds, 60) * 100).denominator == 1 else seconds * 2,
                                   seconds + speed], unit="วินาที", topic=TOPIC_LAYERS, hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
        p, s = rng.choice(((8, 4), (6, 3), (10, 5), (12, 6), (9, 6)))
        dist = rng.randrange(120, 2401, 120)
        gap = Fraction(dist, s) - Fraction(dist, p)
        if (gap * 100).denominator != 1:
            p, s = 8, 4
            gap = Fraction(dist, s) - Fraction(dist, p)
        return numeric(stem=f"สถานีวัดอยู่ห่างจุดเกิดแผ่นดินไหว {dist:,} km คลื่น P เร็ว {p} km/s คลื่น S เร็ว {s} km/s คลื่น S มาถึงช้ากว่าคลื่น P กี่วินาที",
                       answer=gap, wrongs=[Fraction(dist, s), Fraction(dist, p), Fraction(dist, s) + Fraction(dist, p)], unit="วินาที",
                       topic=TOPIC_LAYERS, hint="ผลต่างเวลา = ระยะทาง ÷ ความเร็วคลื่น S − ระยะทาง ÷ ความเร็วคลื่น P")

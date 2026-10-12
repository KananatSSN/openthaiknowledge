"""ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/10

Sets moved here from: science_wave_f80.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f80 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CLIMATE = "ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศ"


NATURAL = ("การเปลี่ยนแปลงรูปร่างวงโคจรของโลก", "การเปลี่ยนมุมเอียงของแกนโลก", "การส่ายของแกนโลก", "การปะทุของภูเขาไฟ",
           "การเปลี่ยนแปลงพลังงานที่ดวงอาทิตย์แผ่ออกมา", "การเคลื่อนที่ของแผ่นธรณีซึ่งเปลี่ยนตำแหน่งทวีป")


HUMAN = ("การเผาเชื้อเพลิงซากดึกดำบรรพ์", "การตัดไม้ทำลายป่า", "การปล่อยแก๊สมีเทนจากนาข้าวและปศุสัตว์", "การใช้ปุ๋ยไนโตรเจนปริมาณมาก",
         "การเปลี่ยนพื้นที่ป่าเป็นเมือง", "การรั่วไหลของสารทำความเย็นจำพวก HFC")


CLIMATE_FACTS = (
    ("การปะทุของภูเขาไฟขนาดใหญ่ เช่น ภูเขาไฟพินาทูโบ ปี 2534 มีผลต่ออุณหภูมิโลกในระยะสั้นอย่างไร", "อุณหภูมิเฉลี่ยลดลงชั่วคราวเพราะละอองซัลเฟตสะท้อนแสง",
     ("อุณหภูมิเฉลี่ยสูงขึ้นอย่างถาวร", "ไม่มีผลใดต่ออุณหภูมิ", "ทำให้เกิดยุคน้ำแข็งทันที", "ทำให้ชั้นโอโซนหนาขึ้นมาก")),
    ("ข้อมูลใดใช้ศึกษาภูมิอากาศย้อนหลังนับแสนปีได้", "ฟองอากาศในแกนน้ำแข็งขั้วโลก",
     ("บันทึกของสถานีตรวจอากาศรายวัน", "ภาพถ่ายดาวเทียมปัจจุบัน", "ข่าวพยากรณ์อากาศประจำวัน", "บันทึกเรือประมง")),
    ("วงปีของต้นไม้ใช้เป็นหลักฐานเรื่องภูมิอากาศได้อย่างไร", "วงปีกว้างแสดงปีที่อากาศเหมาะกับการเติบโต วงแคบแสดงปีที่แล้งหรือหนาว",
     ("วงปีบอกความลึกของน้ำใต้ดิน", "วงปีบอกจำนวนแผ่นดินไหวที่ต้นไม้ผ่านมาในแต่ละปี", "วงปีกว้างแสดงปีที่แห้งแล้งที่สุด วงแคบแสดงปีที่ฝนตกมาก", "วงปีมีจำนวนเท่ากันทุกต้นที่อายุเท่ากันจึงบอกภูมิอากาศไม่ได้")),
    ("ข้อมูลใดสนับสนุนว่าอุณหภูมิเฉลี่ยของโลกสูงขึ้น", "ธารน้ำแข็งทั่วโลกหดตัวและระดับน้ำทะเลเฉลี่ยสูงขึ้น",
     ("ธารน้ำแข็งทั่วโลกขยายตัวมากขึ้นและระดับน้ำทะเลลดลง", "ระดับน้ำทะเลเฉลี่ยลดลงต่อเนื่อง", "ปริมาณ CO₂ ในบรรยากาศลดลงและอุณหภูมิเฉลี่ยของโลกลดลง", "จำนวนวันที่อากาศหนาวจัดเพิ่มขึ้นทั่วโลก")),
    ("ปริมาณแก๊สคาร์บอนไดออกไซด์ในบรรยากาศช่วงก่อนยุคอุตสาหกรรมกับปัจจุบันเป็นอย่างไร", "เพิ่มจากประมาณ 280 ppm เป็นมากกว่า 400 ppm",
     ("ลดจากประมาณ 400 ppm เหลือ 280 ppm", "คงที่ประมาณ 280 ppm ตลอดช่วงเวลานั้น", "เพิ่มจากประมาณ 28 ppm เป็นมากกว่า 40 ppm", "ลดลงเกือบเป็นศูนย์")),
    ("วัฏจักรมิลานโควิชอธิบายการเปลี่ยนแปลงภูมิอากาศด้วยปัจจัยใด", "การเปลี่ยนแปลงวงโคจรและแกนของโลกที่มีคาบนับหมื่นถึงแสนปี",
     ("การปล่อยแก๊สเรือนกระจกของมนุษย์", "การเกิดพายุไต้ฝุ่นรายปีที่สะสมความร้อนติดต่อกันนับหมื่นปี", "การตัดไม้ทำลายป่า", "การเกิดเอลนีโญทุกปีที่ทำให้ยุคน้ำแข็งเกิดขึ้น")),
    ("ละอองเรณูที่สะสมในชั้นตะกอนทะเลสาบใช้เป็นหลักฐานเรื่องภูมิอากาศได้อย่างไร", "ชนิดของพืชในแต่ละชั้นบอกสภาพภูมิอากาศในช่วงเวลานั้น",
     ("บอกจำนวนแผ่นดินไหวในอดีตจากความหนาของแต่ละชั้น", "บอกความเค็มของน้ำทะเลปัจจุบันในบริเวณที่ขุดพบ", "บอกความเร็วลมรายวัน", "บอกอายุของดวงอาทิตย์จากจำนวนชั้นของละอองเรณู")),
    ("เหตุใดการตัดไม้ทำลายป่าจึงทำให้ภูมิอากาศโลกร้อนขึ้น", "ต้นไม้ที่ดูดซับ CO₂ ลดลง และการเผาป่าปล่อย CO₂ เพิ่มขึ้น",
     ("ต้นไม้ปล่อยออกซิเจนที่ทำให้โลกเย็นลงหมดไป", "พื้นที่ป่าสะท้อนแสงมากกว่าทะเลทราย โลกจึงเย็นลงเมื่อตัดป่า", "ป่าไม้เป็นแหล่งผลิตโอโซนเพียงแห่งเดียวของบรรยากาศ",
      "ต้นไม้ดูดความร้อนจากแกนโลก")),
)


CLIMATE_HINT = ("ปัจจัยธรรมชาติ: วงโคจรและแกนโลก (มิลานโควิช) พลังงานจากดวงอาทิตย์ ภูเขาไฟ การเคลื่อนที่ของทวีป "
                "ปัจจัยจากมนุษย์: แก๊สเรือนกระจกจากเชื้อเพลิง ป่าไม้ถูกทำลาย เกษตรกรรม หลักฐานได้แก่ แกนน้ำแข็ง วงปีไม้ ปะการัง "
                "และข้อมูลตรวจวัด CO₂ อุณหภูมิ ระดับน้ำทะเล")


@question_type(
    "geo.climate_factor_foundation",
    display_name={"th": "ปัจจัยธรรมชาติและปัจจัยจากมนุษย์ที่เปลี่ยนภูมิอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CLIMATE,
)
class ClimateFactorFoundation(QuestionType):
    """Sort factors into natural and human."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        human = rng.random() < 0.5
        right = rng.choice(HUMAN if human else NATURAL)
        wrongs = rng.sample(NATURAL if human else HUMAN, 3)
        return _labelled(stem=f"ข้อใดเป็นปัจจัย{'จากกิจกรรมของมนุษย์' if human else 'ทางธรรมชาติ'}ที่ทำให้ภูมิอากาศของโลกเปลี่ยนแปลง",
                         correct=right, wrongs=tuple(wrongs), topic=TOPIC_CLIMATE, hint=CLIMATE_HINT)


@question_type(
    "geo.climate_factor_fluency",
    display_name={"th": "หลักฐานและข้อมูลสนับสนุนการเปลี่ยนแปลงภูมิอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CLIMATE,
)
class ClimateFactorFluency(QuestionType):
    """Volcanoes, ice cores, tree rings, CO2 and Milankovitch."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(CLIMATE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CLIMATE, hint=CLIMATE_HINT)


@question_type(
    "geo.climate_factor_application",
    display_name={"th": "คำนวณอัตราการเพิ่มของ CO₂ และอุณหภูมิจากข้อมูล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CLIMATE,
)
class ClimateFactorApplication(QuestionType):
    """Rate of rise from two readings; projecting ahead; rise above pre-industrial."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            y1 = rng.randrange(1960, 2001, 5)
            years = rng.choice((10, 20, 25, 40, 50))
            y2 = min(y1 + years, 2025)
            years = y2 - y1
            rate = Fraction(rng.choice((10, 12, 14, 15, 16, 18, 20, 22, 24, 25)), 10)
            c1 = rng.randint(315, 370)
            c2 = c1 + rate * years
            if (c2 * 100).denominator != 1 or years == 0:
                years, y2 = 20, y1 + 20
                c2 = c1 + rate * years
            return numeric(stem=f"ปริมาณ CO₂ ในบรรยากาศวัดได้ {c1} ppm ในปี พ.ศ. {y1 + 543} และ {show(c2)} ppm ในปี พ.ศ. {y2 + 543} "
                                f"CO₂ เพิ่มขึ้นเฉลี่ยปีละกี่ ppm", answer=rate, wrongs=[c2 - c1, rate * 10, rate + 1], unit="ppm",
                           topic=TOPIC_CLIMATE, hint="อัตราการเพิ่ม = (ค่าหลัง − ค่าก่อน) ÷ จำนวนปี")
        if roll < 0.7:
            now = rng.randint(410, 425)
            rate = Fraction(rng.choice((15, 20, 24, 25, 30)), 10)
            years = rng.choice((10, 20, 25, 30, 40, 50))
            return numeric(stem=f"ปัจจุบัน CO₂ ในบรรยากาศประมาณ {now} ppm ถ้ายังเพิ่มขึ้นปีละ {show(rate)} ppm อีก {years} ปีจะมี CO₂ ประมาณกี่ ppm",
                           answer=now + rate * years, wrongs=[rate * years, now + years, now + rate * years * 2], unit="ppm",
                           topic=TOPIC_CLIMATE, hint="ค่าในอนาคต = ค่าปัจจุบัน + อัตราต่อปี × จำนวนปี")
        pre = 280
        now = rng.choice((336, 350, 364, 378, 392, 406, 420, 434))
        return numeric(stem=f"ก่อนยุคอุตสาหกรรม CO₂ ในบรรยากาศประมาณ {pre} ppm ถ้าปัจจุบันวัดได้ {now} ppm ปริมาณ CO₂ เพิ่มขึ้นร้อยละเท่าใด",
                       answer=Fraction(now - pre, pre) * 100, wrongs=[now - pre, Fraction(now - pre, now) * 100 if (Fraction(now - pre, now) * 10000).denominator == 1 else now - pre + 10,
                                                                      Fraction(now, pre) * 100],
                       unit="%", topic=TOPIC_CLIMATE, hint="ร้อยละที่เพิ่ม = (ค่าใหม่ − ค่าเดิม) ÷ ค่าเดิม × 100")

"""ปัญหาทรัพยากรน้ำและการจัดการ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/9

Sets moved here from: science_wave_f73.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f73 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_WATER = "ปัญหาทรัพยากรน้ำและการจัดการ"


WATER_FACTS = (
    ("ค่า BOD ของแหล่งน้ำสูงหมายความว่าอย่างไร", "มีสารอินทรีย์มาก จุลินทรีย์ใช้ออกซิเจนย่อยสลายมาก น้ำจึงเน่าเสียได้ง่าย",
     ("น้ำมีออกซิเจนละลายมาก จุลินทรีย์จึงย่อยสลายได้เร็วและน้ำสะอาด", "น้ำมีปลาชุกชุม เพราะมีสารอินทรีย์เป็นอาหารมากพอ",
      "น้ำเป็นเบสจัดจากสบู่ จุลินทรีย์จึงตายหมดและน้ำไม่เน่า", "น้ำไม่มีจุลินทรีย์เลย สารอินทรีย์จึงสะสมจนเน่าเองโดยไม่ใช้ออกซิเจน")),
    ("ปริมาณออกซิเจนที่ละลายในน้ำ (DO) ต่ำ ส่งผลอย่างไรต่อแหล่งน้ำ", "สัตว์น้ำขาดออกซิเจน อาจตายและน้ำเน่าเสีย",
     ("สัตว์น้ำเพิ่มจำนวนมากขึ้นเพราะน้ำนิ่ง", "น้ำใสขึ้นและมีปลามากขึ้นเพราะมีอาหารมาก",
      "สาหร่ายหายไปหมด น้ำจึงใสและสะอาดขึ้น", "ไม่มีผลใด ๆ ต่อสัตว์น้ำที่อยู่ใต้ผิวน้ำ")),
    ("การพบแบคทีเรียโคลิฟอร์มในแหล่งน้ำบ่งชี้อะไร", "น้ำปนเปื้อนสิ่งขับถ่ายของคนหรือสัตว์",
     ("น้ำมีแร่ธาตุมากจากหินใต้ดินหลายชนิด", "น้ำมีออกซิเจนสูงและสะอาด", "น้ำปนเปื้อนน้ำมันจากเรือและโรงงาน", "น้ำเค็มเกินกว่าจะใช้ดื่มได้")),
    ("ยูโทรฟิเคชันในแหล่งน้ำเกิดจากอะไร", "ไนเตรตและฟอสเฟตจากปุ๋ยไหลลงน้ำมาก สาหร่ายจึงเพิ่มจำนวนเร็ว",
     ("อุณหภูมิน้ำลดลงมากจนสาหร่ายแพร่พันธุ์เร็วกว่าปกติ", "ปลากินสาหร่ายมากเกินไป จนแหล่งน้ำไม่มีสาหร่ายเติมออกซิเจน",
      "น้ำมีออกซิเจนละลายสูง สาหร่ายจึงหายใจได้ดีและเพิ่มจำนวน", "น้ำไหลแรงตลอดปี พัดพาตะกอนและสาหร่ายมาสะสม")),
    ("ระบบบำบัดน้ำเสียแบบบ่อผึ่งอาศัยหลักการใด", "จุลินทรีย์ย่อยสารอินทรีย์ โดยสาหร่ายช่วยเติมออกซิเจน",
     ("ต้มน้ำเสียให้เดือดจนจุลินทรีย์และสารอินทรีย์สลายไปหมด", "เติมคลอรีนให้ฆ่าจุลินทรีย์ทุกชนิดในบ่อบำบัดน้ำเสีย",
      "กรองน้ำเสียด้วยทรายหลายชั้นจนสะอาดทันทีในวันเดียว", "ปล่อยให้น้ำระเหยหมด เหลือแต่ของเสียที่แห้งแล้วนำไปทิ้ง")),
    ("สาเหตุสำคัญของการขาดแคลนน้ำจืดคือข้อใด", "การตัดไม้ทำลายป่าต้นน้ำ ใช้น้ำเกินจำเป็น และปล่อยน้ำเสีย",
     ("ฝนตกมากเกินไปทุกปีจนแหล่งน้ำจืดกลายเป็นน้ำเค็ม", "การปลูกป่าต้นน้ำและการสร้างฝายชะลอน้ำที่กักน้ำไว้หมด",
      "การบำบัดน้ำเสียที่ทำให้ปริมาณน้ำในแหล่งน้ำลดลง", "การเก็บน้ำฝนไว้ใช้จนแม่น้ำไม่มีน้ำไหลลงทะเล")),
)


WATER_FIX = ("บำบัดน้ำเสียก่อนปล่อยลงแหล่งน้ำ", "เก็บกักน้ำฝนไว้ใช้ในฤดูแล้ง", "ปลูกป่าบริเวณต้นน้ำ", "นำน้ำที่บำบัดแล้วกลับมาใช้รดต้นไม้",
             "ใช้ระบบน้ำหยดในการเกษตร")


WATER_HARM = ("ทิ้งน้ำมันใช้แล้วลงท่อระบายน้ำ", "ปล่อยน้ำทิ้งจากฟาร์มสุกรลงแม่น้ำโดยตรง", "ใช้ปุ๋ยเคมีมากเกินจนไหลลงแหล่งน้ำ",
              "ตัดไม้บริเวณต้นน้ำ", "เปิดน้ำทิ้งไว้ขณะแปรงฟัน")


WATER_HINT = ("BOD คือออกซิเจนที่จุลินทรีย์ใช้ย่อยสารอินทรีย์ใน 5 วัน ยิ่งสูงน้ำยิ่งเสีย DO ต่ำทำให้สัตว์น้ำตาย "
              "แก้ปัญหาโดยบำบัดน้ำเสีย อนุรักษ์ป่าต้นน้ำ และใช้น้ำอย่างประหยัด")


@question_type(
    "biology.water_resource_foundation",
    display_name={"th": "ดัชนีคุณภาพน้ำและสาเหตุของปัญหาน้ำ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterResourceFoundation(QuestionType):
    """BOD, DO, coliforms, and why water runs short."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(WATER_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_WATER, hint=WATER_HINT)


@question_type(
    "biology.water_resource_fluency",
    display_name={"th": "แนวทางจัดการทรัพยากรน้ำ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterResourceFluency(QuestionType):
    """What helps and what harms."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        helps = rng.random() < 0.5
        right, wrong = (WATER_FIX, WATER_HARM) if helps else (WATER_HARM, WATER_FIX)
        return _labelled(stem=f"ข้อใด{'ช่วยแก้ปัญหา' if helps else 'เป็นสาเหตุของ'}ปัญหาการขาดแคลนน้ำหรือน้ำเสีย", correct=rng.choice(right),
                         wrongs=tuple(wrong), topic=TOPIC_WATER, hint=WATER_HINT)


@question_type(
    "biology.water_resource_application",
    display_name={"th": "คำนวณค่า BOD และการใช้น้ำ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WATER,
)
class WaterResourceApplication(QuestionType):
    """BOD from two DO readings; water saved by a change of habit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            start = Fraction(rng.randrange(60, 91), 10)
            used = Fraction(rng.randrange(5, 50), 10)
            if used >= start:
                used = start / 2
            end = start - used
            if rng.random() < 0.5:
                return numeric(stem=f"วัดออกซิเจนละลายในตัวอย่างน้ำได้ {show(start)} mg/L เก็บในที่มืด 20 °C นาน 5 วัน วัดได้ {show(end)} mg/L "
                                    f"ค่า BOD ของน้ำนี้เป็นกี่ mg/L", answer=used, wrongs=[start + end, end, start], unit="mg/L", topic=TOPIC_WATER,
                               hint="BOD = DO เริ่มต้น − DO หลังเก็บ 5 วัน")
            clean = used <= Fraction(15, 10)
            return _labelled(stem=f"แหล่งน้ำหนึ่งมีค่า DO เริ่มต้น {show(start)} mg/L และหลัง 5 วันเหลือ {show(end)} mg/L "
                                  f"ถ้าเกณฑ์ BOD ของน้ำผิวดินคุณภาพดีไม่เกิน 1.5 mg/L แหล่งน้ำนี้เป็นอย่างไร",
                             correct=f"BOD เท่ากับ {show(used)} mg/L {'อยู่ในเกณฑ์น้ำคุณภาพดี' if clean else 'เกินเกณฑ์น้ำคุณภาพดี'}",
                             wrongs=(f"BOD เท่ากับ {show(used)} mg/L {'เกินเกณฑ์น้ำคุณภาพดี' if clean else 'อยู่ในเกณฑ์น้ำคุณภาพดี'}",
                                     f"BOD เท่ากับ {show(end)} mg/L อยู่ในเกณฑ์น้ำคุณภาพดี" if end != used else f"BOD เท่ากับ {show(start)} mg/L เกินเกณฑ์น้ำคุณภาพดี",
                                     f"BOD เท่ากับ {show(start + end)} mg/L เกินเกณฑ์น้ำคุณภาพดี"),
                             topic=TOPIC_WATER, hint="BOD = DO เริ่มต้น − DO หลัง 5 วัน แล้วเทียบกับเกณฑ์")
        per_min = rng.choice((6, 8, 10, 12))
        minutes = rng.choice((2, 3, 4, 5))
        people = rng.randint(2, 6)
        days = rng.choice((7, 30))
        saved = per_min * minutes * people * days
        return numeric(stem=f"ก๊อกน้ำไหล {per_min} ลิตรต่อนาที ถ้าสมาชิก {people} คนปิดน้ำขณะแปรงฟันคนละ {minutes} นาทีต่อวัน "
                            f"ใน {days} วันจะประหยัดน้ำได้กี่ลิตร", answer=saved,
                       wrongs=[per_min * minutes * people, per_min * minutes * days, saved * 2], unit="ลิตร", topic=TOPIC_WATER,
                       hint="น้ำที่ประหยัด = อัตราการไหล × เวลาต่อคน × จำนวนคน × จำนวนวัน")

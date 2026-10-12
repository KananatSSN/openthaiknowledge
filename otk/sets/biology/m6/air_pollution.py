"""ปัญหามลพิษทางอากาศ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/10

Sets moved here from: science_wave_f73.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f73 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_AIR = "ปัญหามลพิษทางอากาศ"


POLLUTANTS = (
    ("ฝุ่นละออง PM2.5", "การเผาในที่โล่งและไอเสียเครื่องยนต์ดีเซล", "ผ่านเข้าถึงถุงลมและกระแสเลือด ทำให้เกิดโรคทางเดินหายใจและหัวใจ"),
    ("แก๊สคาร์บอนมอนอกไซด์", "การเผาไหม้ที่ไม่สมบูรณ์", "รวมกับฮีโมโกลบินได้ดีกว่าออกซิเจน ทำให้เนื้อเยื่อขาดออกซิเจน"),
    ("แก๊สซัลเฟอร์ไดออกไซด์", "การเผาถ่านหินและน้ำมันที่มีกำมะถัน", "ระคายเคืองทางเดินหายใจและทำให้เกิดฝนกรด"),
    ("แก๊สไนโตรเจนออกไซด์", "เครื่องยนต์ที่เผาไหม้ที่อุณหภูมิสูง", "ทำให้เกิดฝนกรดและหมอกควันเคมีแสง"),
    ("แก๊สโอโซนระดับพื้นดิน", "ปฏิกิริยาของไนโตรเจนออกไซด์กับสารอินทรีย์ระเหยง่ายเมื่อมีแสงแดด", "ระคายเคืองตาและปอด ทำลายใบพืช"),
    ("สาร CFC", "สารทำความเย็นและสเปรย์แบบเก่า", "ทำลายโอโซนในชั้นสตราโทสเฟียร์ ทำให้รังสีอัลตราไวโอเลตถึงพื้นโลกมากขึ้น"),
)


AIR_HINT = ("PM2.5 จากการเผาเข้าถึงถุงลม CO แย่งจับฮีโมโกลบิน SO₂ และ NOx ทำให้ฝนกรด โอโซนพื้นดินเกิดจากหมอกควันเคมีแสง "
            "CFC ทำลายชั้นโอโซน")


@question_type(
    "biology.air_pollution_foundation",
    display_name={"th": "สารมลพิษทางอากาศและแหล่งกำเนิด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AIR,
)
class AirPollutionFoundation(QuestionType):
    """Each pollutant and where it comes from."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, source, _ = rng.choice(POLLUTANTS)
        others = rng.sample([p for p in POLLUTANTS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีแหล่งกำเนิดสำคัญจากอะไร", correct=source, wrongs=tuple(p[1] for p in others), topic=TOPIC_AIR,
                             hint=AIR_HINT)
        return _labelled(stem=f"สารมลพิษใดเกิดจาก{source}เป็นหลัก", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_AIR, hint=AIR_HINT)


@question_type(
    "biology.air_pollution_fluency",
    display_name={"th": "ผลกระทบของมลพิษทางอากาศและแนวทางแก้ไข"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AIR,
)
class AirPollutionFluency(QuestionType):
    """What each pollutant does, and what reduces it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            name, _, harm = rng.choice(POLLUTANTS)
            others = rng.sample([p for p in POLLUTANTS if p[0] != name], 3)
            if rng.random() < 0.5:
                return _labelled(stem=f"{name}ส่งผลกระทบอย่างไร", correct=harm, wrongs=tuple(p[2] for p in others), topic=TOPIC_AIR, hint=AIR_HINT)
            return _labelled(stem=f"สารมลพิษใด{harm}", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_AIR, hint=AIR_HINT)
        fixes = ("งดเผาเศษวัชพืชและตอซังในที่โล่ง", "ติดตั้งเครื่องดักฝุ่นและกำจัดกำมะถันในปล่องโรงงาน", "ใช้ขนส่งสาธารณะแทนรถส่วนตัว",
                 "ตรวจสภาพเครื่องยนต์ไม่ให้มีควันดำ")
        harms = ("เผาขยะพลาสติกในที่โล่ง", "ติดเครื่องยนต์รถทิ้งไว้ขณะจอดนาน ๆ", "ใช้ถ่านหินที่มีกำมะถันสูงโดยไม่บำบัด", "เผาป่าเพื่อเตรียมพื้นที่เพาะปลูก")
        good = rng.random() < 0.5
        right, wrong = (fixes, harms) if good else (harms, fixes)
        return _labelled(stem=f"ข้อใด{'ช่วยลด' if good else 'ทำให้เพิ่ม'}มลพิษทางอากาศ", correct=rng.choice(right), wrongs=tuple(wrong),
                         topic=TOPIC_AIR, hint=AIR_HINT)


@question_type(
    "biology.air_pollution_application",
    display_name={"th": "วิเคราะห์ค่าฝุ่นละออง PM2.5"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_AIR,
)
class AirPollutionApplication(QuestionType):
    """Average the readings and compare with 37.5 μg/m³."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        days = rng.choice((4, 5))
        while True:
            readings = [rng.randrange(10, 121) for _ in range(days)]
            mean = Fraction(sum(readings), days)
            if (mean * 100).denominator == 1:
                break
        listing = ", ".join(str(r) for r in readings)
        roll = rng.random()
        if roll < 0.4:
            return numeric(stem=f"ค่า PM2.5 เฉลี่ย 24 ชั่วโมงใน {days} วันเป็น {listing} μg/m³ ค่าเฉลี่ยของช่วงนี้เป็นกี่ μg/m³", answer=mean,
                           wrongs=[sum(readings), max(readings), min(readings)], unit="μg/m³", topic=TOPIC_AIR,
                           hint="ค่าเฉลี่ย = ผลรวม ÷ จำนวนวัน")
        if roll < 0.7:
            over = sum(r > Fraction(75, 2) for r in readings)
            return numeric(stem=f"ค่า PM2.5 เฉลี่ย 24 ชั่วโมงใน {days} วันเป็น {listing} μg/m³ ถ้ามาตรฐานคือไม่เกิน 37.5 μg/m³ มีกี่วันที่เกินมาตรฐาน",
                           answer=over, wrongs=[days - over, days, over + 1] if over else [days, 1, 2], unit="วัน", topic=TOPIC_AIR,
                           hint="นับวันที่ค่ามากกว่า 37.5 μg/m³") if over else \
                _labelled(stem=f"ค่า PM2.5 เฉลี่ย 24 ชั่วโมงใน {days} วันเป็น {listing} μg/m³ เทียบกับมาตรฐาน 37.5 μg/m³ ข้อใดถูกต้อง",
                          correct="ทุกวันไม่เกินมาตรฐาน", wrongs=("ทุกวันเกินมาตรฐาน", "เกินมาตรฐาน 1 วัน", "เกินมาตรฐาน 2 วัน"),
                          topic=TOPIC_AIR, hint="เทียบค่าแต่ละวันกับ 37.5 μg/m³")
        worst = max(readings)
        times = Fraction(worst * 2, 75)
        if (times * 100).denominator != 1:
            worst = 75
            times = Fraction(2)
            readings[0] = 75
            listing = ", ".join(str(r) for r in readings)
        return numeric(stem=f"ค่า PM2.5 ในวันที่สูงที่สุดเท่ากับ {worst} μg/m³ ค่านี้เป็นกี่เท่าของมาตรฐาน 37.5 μg/m³", answer=times,
                       wrongs=[worst - Fraction(75, 2), times * 2, Fraction(75, 2)], unit="เท่า", topic=TOPIC_AIR, hint="จำนวนเท่า = ค่าที่วัดได้ ÷ 37.5")

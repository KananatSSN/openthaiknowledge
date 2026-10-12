"""ปัญหาทรัพยากรดิน

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/11

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


TOPIC_SOIL = "ปัญหาทรัพยากรดิน"


SOIL_PROBLEMS = (
    ("การชะล้างพังทลายของดิน", "ตัดไม้บนพื้นที่ลาดชันและไถพรวนตามแนวลาดเท", "ปลูกพืชขวางแนวลาดเทและปลูกหญ้าแฝก"),
    ("ดินเค็ม", "เกลือจากชั้นหินใต้ดินขึ้นมาสะสมที่ผิวดิน เช่น ในภาคตะวันออกเฉียงเหนือ", "ปลูกพืชทนเค็มและปลูกป่าเพื่อลดระดับน้ำใต้ดิน"),
    ("ดินเปรี้ยวจัด", "ดินที่มีสารประกอบกำมะถันถูกระบายน้ำจนเกิดกรด", "ใส่ปูนเพื่อปรับความเป็นกรดและควบคุมระดับน้ำ"),
    ("ดินเสื่อมความอุดมสมบูรณ์", "ปลูกพืชชนิดเดียวซ้ำ ๆ โดยไม่บำรุงดิน", "ปลูกพืชหมุนเวียนและใส่ปุ๋ยอินทรีย์"),
    ("ดินปนเปื้อนสารพิษ", "ใช้สารเคมีกำจัดศัตรูพืชมากเกินไปและทิ้งขยะอันตราย", "ลดการใช้สารเคมีและกำจัดขยะอันตรายอย่างถูกวิธี"),
)


SOIL_HINT = ("ดินถูกชะล้างเมื่อไม่มีพืชคลุม ดินเค็มเกิดจากเกลือใต้ดิน ดินเปรี้ยวแก้ด้วยปูน ดินเสื่อมแก้ด้วยพืชหมุนเวียนและปุ๋ยอินทรีย์ "
             "หญ้าแฝกมีรากลึกช่วยยึดดิน")


@question_type(
    "biology.soil_resource_foundation",
    display_name={"th": "ปัญหาทรัพยากรดินและสาเหตุ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOIL,
)
class SoilResourceFoundation(QuestionType):
    """Each soil problem and what causes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, cause, _ = rng.choice(SOIL_PROBLEMS)
        others = rng.sample([p for p in SOIL_PROBLEMS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีสาเหตุสำคัญจากอะไร", correct=cause, wrongs=tuple(p[1] for p in others), topic=TOPIC_SOIL, hint=SOIL_HINT)
        return _labelled(stem=f"\"{cause}\" ทำให้เกิดปัญหาดินแบบใด", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_SOIL, hint=SOIL_HINT)


@question_type(
    "biology.soil_resource_fluency",
    display_name={"th": "แนวทางแก้ไขปัญหาทรัพยากรดิน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOIL,
)
class SoilResourceFluency(QuestionType):
    """The fix for each problem."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, fix = rng.choice(SOIL_PROBLEMS)
        others = rng.sample([p for p in SOIL_PROBLEMS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ควรแก้ปัญหา{name}อย่างไร", correct=fix, wrongs=tuple(p[2] for p in others), topic=TOPIC_SOIL, hint=SOIL_HINT)
        return _labelled(stem=f"\"{fix}\" เป็นแนวทางแก้ปัญหาดินแบบใด", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_SOIL, hint=SOIL_HINT)


@question_type(
    "biology.soil_resource_application",
    display_name={"th": "คำนวณการสูญเสียหน้าดินและการปรับปรุงดิน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SOIL,
)
class SoilResourceApplication(QuestionType):
    """Soil lost per area per year, and lime by the rate given."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            rate = rng.choice((2, 3, 5, 8, 10, 12, 15))
            area = rng.choice((5, 10, 20, 25, 50))
            years = rng.randint(2, 10)
            if rng.random() < 0.5:
                return numeric(stem=f"พื้นที่ลาดชันที่ไม่มีพืชคลุมสูญเสียหน้าดิน {rate} ตันต่อไร่ต่อปี พื้นที่ {area} ไร่ ใน {years} ปีจะสูญเสียหน้าดินกี่ตัน",
                               answer=rate * area * years, wrongs=[rate * area, rate * years, rate + area + years], unit="ตัน", topic=TOPIC_SOIL,
                               hint="หน้าดินที่สูญเสีย = อัตรา × พื้นที่ × จำนวนปี")
            cut = rng.choice((50, 60, 75, 80, 90))
            saved = Fraction(rate * area * cut, 100)
            return numeric(stem=f"พื้นที่ {area} ไร่สูญเสียหน้าดิน {rate} ตันต่อไร่ต่อปี เมื่อปลูกหญ้าแฝกขวางแนวลาดเทช่วยลดการสูญเสียได้ร้อยละ {cut} "
                                f"จะลดการสูญเสียหน้าดินได้กี่ตันต่อปี", answer=saved,
                           wrongs=[rate * area, Fraction(rate * area * (100 - cut), 100), cut], unit="ตัน", topic=TOPIC_SOIL,
                           hint="ส่วนที่ลดได้ = การสูญเสียเดิม × ร้อยละที่ลด ÷ 100")
        per_rai = rng.choice((100, 150, 200, 250, 300, 500))
        area = rng.choice((2, 4, 5, 10, 15, 20))
        return numeric(stem=f"ดินเปรี้ยวจัดต้องใส่ปูนอัตรา {per_rai} กิโลกรัมต่อไร่ พื้นที่ {area} ไร่ต้องใช้ปูนกี่กิโลกรัม", answer=per_rai * area,
                       wrongs=[per_rai + area, per_rai * area * 2, per_rai], unit="kg", topic=TOPIC_SOIL, hint="ปริมาณปูน = อัตราต่อไร่ × จำนวนไร่")

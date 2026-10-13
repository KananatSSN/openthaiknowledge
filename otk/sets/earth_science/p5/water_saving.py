"""การใช้น้ำอย่างประหยัดและการอนุรักษ์น้ำ

ธรณีวิทยา · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.5/2

Sets moved here from: science_wave_c12.
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
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c12 import SAVING_SCENARIOS

PROVENANCE = Provenance("original")


SAVING_TOPIC = "การใช้น้ำอย่างประหยัดและการอนุรักษ์น้ำ"


SAVE = "ประหยัด"


CONSERVE = "อนุรักษ์"


class Practice(NamedTuple):
    """One practice, whether it saves or conserves water, and why it helps."""
    practice: str
    kind: str
    reason: str


PRACTICES = (
    Practice("ปิดก๊อกน้ำขณะแปรงฟันหรือถูสบู่", SAVE,
             "น้ำไม่ไหลทิ้งไปในช่วงที่ไม่ได้ใช้"),
    Practice("ซ่อมก๊อกและท่อน้ำที่รั่วทันที", SAVE,
             "น้ำที่หยดรั่วทีละน้อยรวมกันแล้วสูญเสียไปมาก"),
    Practice("นำน้ำที่ล้างผักแล้วไปรดต้นไม้", SAVE,
             "ใช้น้ำครั้งเดียวได้ประโยชน์สองอย่าง"),
    Practice("รองน้ำใส่ขันหรือกะละมังแทนการเปิดน้ำไหลตลอดเวลา", SAVE,
             "กำหนดปริมาณน้ำที่ใช้ได้ ไม่ปล่อยให้ไหลเกินจำเป็น"),
    Practice("ไม่ทิ้งขยะลงในแม่น้ำลำคลอง", CONSERVE,
             "แหล่งน้ำไม่เน่าเสีย จึงยังนำมาใช้ได้"),
    Practice("ปลูกต้นไม้บริเวณต้นน้ำและริมตลิ่ง", CONSERVE,
             "รากไม้ช่วยให้ดินอุ้มน้ำและลดการพังทลายของตลิ่ง"),
    Practice("บำบัดน้ำเสียจากบ้านเรือนก่อนปล่อยลงแหล่งน้ำ", CONSERVE,
             "ลดสิ่งสกปรกที่ไหลลงไปทำให้แหล่งน้ำเสีย"),
    Practice("ขุดลอกคูคลองและสร้างแหล่งกักเก็บน้ำฝน", CONSERVE,
             "แหล่งน้ำเก็บน้ำไว้ใช้ได้มากขึ้นในฤดูแล้ง"),
)


def _practices(kind: str) -> list[Practice]:
    return [practice for practice in PRACTICES if practice.kind == kind]


class Case(NamedTuple):
    """A community with one waste of water and one threat to its source.

    ``defensible`` lists practices that would also help this case, so they are
    never offered as its wrong half.
    """
    situation: str
    save: str
    conserve: str
    defensible: tuple[str, ...] = ()


CASES = (
    Case("ในโรงเรียนมีก๊อกน้ำหลายตัวหยดรั่วทั้งวัน และมีคนนำถุงขยะไปโยนทิ้งลงคลองหลังโรงเรียน",
         "ซ่อมก๊อกและท่อน้ำที่รั่วทันที",
         "ไม่ทิ้งขยะลงในแม่น้ำลำคลอง"),
    Case("ครอบครัวหนึ่งเปิดน้ำไหลทิ้งตลอดเวลาขณะแปรงฟัน และบ้านในซอยปล่อยน้ำซักล้างลงลำรางโดยตรงจนน้ำเน่า",
         "ปิดก๊อกน้ำขณะแปรงฟันหรือถูสบู่",
         "บำบัดน้ำเสียจากบ้านเรือนก่อนปล่อยลงแหล่งน้ำ",
         ("รองน้ำใส่ขันหรือกะละมังแทนการเปิดน้ำไหลตลอดเวลา",)),
    Case("ร้านอาหารล้างจานโดยเปิดน้ำไหลตลอดเวลาทั้งวัน และริมตลิ่งของลำธารต้นน้ำถูกตัดต้นไม้จนดินพังลงน้ำ",
         "รองน้ำใส่ขันหรือกะละมังแทนการเปิดน้ำไหลตลอดเวลา",
         "ปลูกต้นไม้บริเวณต้นน้ำและริมตลิ่ง",
         ("ปิดก๊อกน้ำขณะแปรงฟันหรือถูสบู่",)),
    Case("หมู่บ้านหนึ่งเททิ้งน้ำล้างผักทุกวันขณะที่สวนผักขาดน้ำ และคลองของหมู่บ้านตื้นเขินจนเก็บน้ำไว้ใช้หน้าแล้งไม่ได้",
         "นำน้ำที่ล้างผักแล้วไปรดต้นไม้",
         "ขุดลอกคูคลองและสร้างแหล่งกักเก็บน้ำฝน"),
)


CASES += (
    Case(situation='ร้านล้างรถในชุมชนเปิดน้ำไหลตลอดเวลาขณะล้างรถ และบึงสาธารณะของชุมชนตื้นเขินจนเก็บน้ำไว้ใช้หน้าแล้งไม่ได้',
         save='รองน้ำใส่ขันหรือกะละมังแทนการเปิดน้ำไหลตลอดเวลา',
         conserve='ขุดลอกคูคลองและสร้างแหล่งกักเก็บน้ำฝน',
         defensible=('ปิดก๊อกน้ำขณะแปรงฟันหรือถูสบู่',)),
    Case(situation='ห้องน้ำในตลาดมีท่อน้ำแตกรั่วไหลตลอดคืน และแม่ค้าทิ้งเศษผักกับถุงพลาสติกลงคลองข้างตลาดทุกวัน',
         save='ซ่อมก๊อกและท่อน้ำที่รั่วทันที',
         conserve='ไม่ทิ้งขยะลงในแม่น้ำลำคลอง',
         defensible=()),
)


def _proposal(save: str, conserve: str) -> str:
    return f"ใช้น้ำอย่าง{SAVE}โดย{save} และ{CONSERVE}แหล่งน้ำโดย{conserve}"


@question_type(
    "geo.water_saving_foundation",
    display_name={"th": "แนวทางประหยัดน้ำและอนุรักษ์น้ำ"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SAVING_TOPIC,
)
class WaterSavingFoundation(QuestionType):
    """Tell saving from conserving, and match a practice to why it helps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PRACTICES)
        others = [other for other in PRACTICES if other.practice != item.practice]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การ“{item.practice}” ช่วยเรื่องน้ำได้อย่างไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint="นึกว่าการกระทำนั้นลดน้ำที่เสียไป หรือดูแลให้แหล่งน้ำยังใช้ได้",
                topic=SAVING_TOPIC,
            )
        kind = rng.choice((SAVE, CONSERVE))
        other_kind = CONSERVE if kind == SAVE else SAVE
        correct = rng.choice(_practices(kind))
        wrongs = rng.sample(_practices(other_kind), 3)
        word = "การใช้น้ำอย่างประหยัด" if kind == SAVE else "การอนุรักษ์แหล่งน้ำ"
        return _labelled(
            stem=f"ข้อใดเป็นแนวทาง{word}",
            correct=correct.practice,
            wrongs=tuple(one.practice for one in wrongs),
            hint="ประหยัดคือใช้น้ำให้น้อยลง อนุรักษ์คือดูแลแหล่งน้ำไม่ให้เสียหรือหมดไป",
            topic=SAVING_TOPIC,
        )


@question_type(
    "geo.water_saving_fluency",
    display_name={"th": "เสนอแนวทางประหยัดน้ำและอนุรักษ์น้ำให้ตรงกับปัญหา"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SAVING_TOPIC,
)
class WaterSavingFluency(QuestionType):
    """Propose one saving and one conserving practice that fit a case.

    The indicator names both, so every answer proposes one of each; a wrong answer
    gets at least one of the two wrong for this case.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(CASES)
        other_saves = [one.practice for one in _practices(SAVE)
                       if one.practice not in (case.save, *case.defensible)]
        other_conserves = [one.practice for one in _practices(CONSERVE)
                           if one.practice not in (case.conserve, *case.defensible)]
        wrong_save = rng.choice(other_saves)
        wrong_conserve = rng.choice(other_conserves)
        return _labelled(
            stem=f"{case.situation} ควรเสนอแนวทางใดที่แก้ทั้งสองปัญหาได้ตรงที่สุด",
            correct=_proposal(case.save, case.conserve),
            wrongs=(_proposal(wrong_save, case.conserve),
                    _proposal(case.save, wrong_conserve),
                    _proposal(wrong_save, wrong_conserve)),
            hint="หาปัญหาที่ทำให้น้ำเสียไปเปล่า ๆ และปัญหาที่ทำให้แหล่งน้ำเสียหาย แล้วแก้ให้ตรงทีละปัญหา",
            topic=SAVING_TOPIC,
        )


@question_type(
    "geo.water_saving_application",
    display_name={"th": "วางแผนใช้น้ำอย่างคุ้มค่าในชุมชน"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SAVING_TOPIC,
)
class WaterSavingApplication(QuestionType):
    """Answer the "one drop" claim, plan for the dry season, and test a saving."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SAVING_SCENARIOS,
            hint="นึกว่าแนวทางนั้นลดน้ำที่เสียไป หรือทำให้แหล่งน้ำยังใช้ได้ในระยะยาว",
        ), SAVING_TOPIC)

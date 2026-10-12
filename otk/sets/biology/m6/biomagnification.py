"""ไบโอแมกนิฟิเคชัน

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/2

Sets moved here from: science_wave_f71.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f71 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_MAG = "ไบโอแมกนิฟิเคชัน"


MAG_FACTS = (
    ("ไบโอแมกนิฟิเคชันหมายถึงข้อใด", "การที่ความเข้มข้นของสารพิษที่สลายตัวยากเพิ่มขึ้นตามลำดับขั้นของการกิน",
     ("การที่สารพิษลดลงเมื่อผ่านโซ่อาหาร เพราะสิ่งมีชีวิตขับสารพิษออกได้หมด", "การเพิ่มจำนวนของผู้ผลิต", "การที่พลังงานเพิ่มขึ้นตามลำดับขั้นของการกินในโซ่อาหาร", "การย่อยสลายสารพิษโดยแบคทีเรีย")),
    ("สารที่เกิดไบโอแมกนิฟิเคชันได้ดีมักมีสมบัติใด", "สลายตัวยาก ละลายในไขมันได้ดี และขับออกจากร่างกายได้ยาก",
     ("สลายตัวเร็ว ละลายน้ำได้ดี และขับออกทางปัสสาวะได้ง่าย", "ระเหยเป็นแก๊สทันที", "ถูกขับออกทางปัสสาวะได้หมดภายในไม่กี่ชั่วโมง", "ไม่เป็นพิษต่อสิ่งมีชีวิต")),
    ("โรคมินามาตะเกิดจากการสะสมของสารใดในโซ่อาหาร", "ปรอท", ("แคดเมียม", "ดีดีที", "ตะกั่วในน้ำมัน", "ไนเตรต")),
    ("โรคอิไตอิไตเกิดจากการสะสมของสารใด", "แคดเมียม", ("ปรอท", "ดีดีที", "ฟอสเฟต", "คาร์บอนไดออกไซด์")),
    ("ในโซ่อาหารเดียวกัน สิ่งมีชีวิตใดมักมีความเข้มข้นของสารพิษที่สลายตัวยากสูงที่สุด", "ผู้บริโภคลำดับสุดท้าย",
     ("ผู้ผลิต", "ผู้บริโภคลำดับที่ 1", "ผู้ย่อยสลายในดิน", "ทุกลำดับเท่ากัน")),
    ("เหตุใดความเข้มข้นของสารพิษจึงเพิ่มขึ้นในผู้ล่า", "ผู้ล่ากินเหยื่อจำนวนมากตลอดชีวิต และสารพิษไม่ถูกขับออก",
     ("ผู้ล่าสร้างสารพิษขึ้นเองในร่างกายและสะสมไว้ตลอดชีวิต", "สารพิษสลายตัวเร็วในผู้ล่า", "ผู้ล่ากินอาหารน้อยกว่าเหยื่อ แต่ดูดซึมสารพิษได้ดีกว่า", "สารพิษละลายน้ำและถูกขับออกหมด")),
    ("นกอินทรีที่ได้รับดีดีทีสะสมมากมักมีปัญหาใด", "เปลือกไข่บางและแตกง่าย ลูกนกฟักออกได้น้อย",
     ("ขนร่วงหมดทันทีจนบินไม่ได้และหนาวตาย", "บินได้สูงขึ้น", "วางไข่มากขึ้น", "ไม่มีผลใด ๆ", "ตัวใหญ่ขึ้นผิดปกติและวางไข่ได้มากขึ้น")),
)


REDUCE = ("ใช้ศัตรูธรรมชาติควบคุมแมลงแทนสารเคมีที่สลายตัวยาก", "บำบัดน้ำเสียจากโรงงานก่อนปล่อยลงแหล่งน้ำ",
          "เลิกใช้สารฆ่าแมลงที่สลายตัวยากอย่างดีดีที", "ลดการกินปลาผู้ล่าขนาดใหญ่ที่อาจสะสมปรอท")


INCREASE = ("ฉีดพ่นดีดีทีในนาข้าวทุกสัปดาห์", "ทิ้งแบตเตอรี่ที่มีปรอทและแคดเมียมลงแม่น้ำ", "ปล่อยน้ำเสียจากเหมืองลงแหล่งน้ำโดยไม่บำบัด",
            "เผาขยะอิเล็กทรอนิกส์กลางแจ้ง")


MAG_HINT = ("สารพิษที่สลายตัวยากและละลายในไขมันสะสมในเนื้อเยื่อ เมื่อผู้ล่ากินเหยื่อจำนวนมาก ความเข้มข้นจึงเพิ่มขึ้นทุกลำดับ "
            "ลดได้โดยเลิกใช้สารเหล่านี้และบำบัดของเสียก่อนปล่อย")


CHAINS = (("แพลงก์ตอนพืช", "แพลงก์ตอนสัตว์", "ปลาเล็ก", "ปลาใหญ่", "นกกินปลา"), ("ข้าว", "หนู", "งู", "เหยี่ยว"),
          ("สาหร่าย", "หอย", "ปู", "ปลากะพง", "คน"))


@question_type(
    "biology.biomagnification_foundation",
    display_name={"th": "ความหมายและตัวอย่างของไบโอแมกนิฟิเคชัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class BiomagnificationFoundation(QuestionType):
    """What builds up, and the diseases it causes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(MAG_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_MAG, hint=MAG_HINT)


@question_type(
    "biology.biomagnification_fluency",
    display_name={"th": "แนวทางลดการเกิดไบโอแมกนิฟิเคชัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class BiomagnificationFluency(QuestionType):
    """Practices that cut the build-up, and ones that feed it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reduce = rng.random() < 0.5
        right, wrong = (REDUCE, INCREASE) if reduce else (INCREASE, REDUCE)
        return _labelled(stem=f"ข้อใด{'ช่วยลด' if reduce else 'ทำให้เพิ่ม'}การเกิดไบโอแมกนิฟิเคชัน", correct=rng.choice(right),
                         wrongs=tuple(wrong), topic=TOPIC_MAG, hint=MAG_HINT)


@question_type(
    "biology.biomagnification_application",
    display_name={"th": "คำนวณความเข้มข้นของสารพิษในโซ่อาหาร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class BiomagnificationApplication(QuestionType):
    """The concentration multiplies by the same factor at each step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(CHAINS)
        factor = rng.choice((2, 5, 10))
        start = Fraction(rng.choice((1, 2, 4, 5)), 100)
        steps = rng.randint(1, len(chain) - 1)
        level = start * factor ** steps
        text = " → ".join(chain)
        if rng.random() < 0.6:
            return numeric(stem=f"ในโซ่อาหาร {text} {chain[0]}มีสารพิษ {show(start)} ppm ถ้าความเข้มข้นเพิ่มขึ้น {factor} เท่าในแต่ละลำดับ "
                                f"{chain[steps]}มีสารพิษกี่ ppm", answer=level,
                           wrongs=[start * factor * steps, level / factor, level * factor], unit="ppm", topic=TOPIC_MAG,
                           hint="ความเข้มข้นที่ลำดับถัดไป = ความเข้มข้นเดิม × จำนวนเท่า ทำซ้ำตามจำนวนลำดับ")
        return numeric(stem=f"{chain[0]}มีสารพิษ {show(start)} ppm และ{chain[steps]}มี {show(level)} ppm ในโซ่อาหาร {text} "
                            f"ความเข้มข้นเพิ่มขึ้นกี่เท่าจาก{chain[0]}ถึง{chain[steps]}", answer=factor ** steps,
                       wrongs=[factor * steps, factor, factor ** steps * 10], unit="เท่า", topic=TOPIC_MAG,
                       hint="จำนวนเท่า = ความเข้มข้นปลายทาง ÷ ความเข้มข้นต้นทาง")

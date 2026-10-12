"""แนวคิดวิวัฒนาการของลามาร์กและดาร์วิน

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/13

Sets moved here from: science_wave_f51.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f51 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_THEORY = "แนวคิดวิวัฒนาการของลามาร์กและดาร์วิน"


THEORY_FACTS = (
    ("ลามาร์ก", "อวัยวะที่ใช้บ่อยจะเจริญ อวัยวะที่ไม่ใช้จะเสื่อมไป (กฎการใช้และไม่ใช้)"),
    ("ลามาร์ก", "ลักษณะที่เกิดขึ้นใหม่ระหว่างที่มีชีวิตอยู่ถ่ายทอดไปสู่ลูกได้ (กฎการถ่ายทอดลักษณะที่เกิดขึ้นใหม่)"),
    ("ดาร์วิน", "สิ่งมีชีวิตที่มีลักษณะเหมาะสมกับสิ่งแวดล้อมจะอยู่รอดและสืบพันธุ์ได้มากกว่า (การคัดเลือกโดยธรรมชาติ)"),
    ("ดาร์วิน", "สิ่งมีชีวิตในประชากรเดียวกันมีลักษณะแปรผันแตกต่างกัน และให้กำเนิดลูกมากเกินกว่าที่จะรอดได้ทั้งหมด"),
    ("ไวส์มันน์", "ตัดหางหนูติดต่อกันหลายรุ่น ลูกหนูยังมีหางยาวตามปกติ"),
    ("วอลเลซ", "เสนอแนวคิดการคัดเลือกโดยธรรมชาติในเวลาใกล้เคียงกับดาร์วิน"),
)


THEORY_HINT = ("ลามาร์ก: การใช้และไม่ใช้ และการถ่ายทอดลักษณะที่เกิดขึ้นใหม่ ดาร์วิน: ความแปรผัน การแข่งขัน "
               "และการคัดเลือกโดยธรรมชาติ ไวส์มันน์ตัดหางหนูเพื่อแย้งแนวคิดของลามาร์ก")


SCENARIOS = (
    ("ยีราฟคอยาว", "ยีราฟยืดคอกินใบไม้บนที่สูงบ่อย ๆ คอจึงยาวขึ้น แล้วถ่ายทอดคอที่ยาวขึ้นไปสู่ลูก",
     "ยีราฟในประชากรมีความยาวคอแตกต่างกัน ตัวที่คอยาวหาอาหารได้มากกว่า จึงอยู่รอดและมีลูกได้มากกว่า"),
    ("เป็ดมีพังผืดระหว่างนิ้วเท้า", "เป็ดใช้เท้าว่ายน้ำบ่อย ๆ พังผืดจึงเจริญขึ้น แล้วถ่ายทอดสู่ลูก",
     "เป็ดที่มีพังผืดระหว่างนิ้วมากว่ายน้ำหาอาหารได้ดีกว่า จึงอยู่รอดและถ่ายทอดลักษณะนี้ได้มากกว่า"),
    ("แบคทีเรียดื้อยาปฏิชีวนะ", "แบคทีเรียพยายามปรับตัวให้ทนยาเมื่อได้รับยาบ่อย ๆ แล้วถ่ายทอดความทนยานั้นต่อไป",
     "ในประชากรมีแบคทีเรียบางเซลล์ที่ทนยาอยู่แล้ว เมื่อใช้ยา เซลล์ที่ทนยารอดและเพิ่มจำนวนแทนเซลล์อื่น"),
    ("แมลงดื้อยาฆ่าแมลง", "แมลงได้รับยาบ่อยจนร่างกายเคยชินกับยา แล้วถ่ายทอดความเคยชินนั้นสู่ลูก",
     "แมลงบางตัวมีลักษณะทนยาอยู่แล้ว เมื่อฉีดยา ตัวที่ทนยารอดและสืบพันธุ์ได้มากกว่า"),
    ("ปลาในถ้ำมืดตาบอด", "ปลาไม่ได้ใช้ตาในที่มืดนาน ๆ ตาจึงเสื่อม แล้วถ่ายทอดตาที่เสื่อมสู่ลูก",
     "ในที่มืดปลาที่ตาเล็กหรือไม่มีตาไม่เสียเปรียบ และใช้พลังงานไปสร้างอวัยวะอื่นได้ จึงอยู่รอดได้ดีกว่า"),
    ("ผีเสื้อกลางคืนสีเข้มเพิ่มขึ้นในเขตอุตสาหกรรม", "ผีเสื้อเกาะต้นไม้ที่มีเขม่าจนสีตัวเข้มขึ้น แล้วถ่ายทอดสีเข้มสู่ลูก",
     "เมื่อต้นไม้มีเขม่าสีเข้ม ผีเสื้อสีเข้มพรางตัวได้ดีกว่า ถูกนกจับกินน้อยกว่า จึงอยู่รอดและสืบพันธุ์ได้มากกว่า"),
)


GENERIC_WRONGS = ("สิ่งมีชีวิตตั้งใจเปลี่ยนรูปร่างของตนเองได้ทันทีตามต้องการ โดยไม่ต้องรอหลายรุ่น",
                  "สิ่งแวดล้อมไม่มีผลใด ๆ ต่อการอยู่รอดของสิ่งมีชีวิต ลักษณะจึงเปลี่ยนไปแบบสุ่ม",
                  "สิ่งมีชีวิตทุกตัวในประชากรมีลักษณะเหมือนกันทุกประการ จึงอยู่รอดหรือตายไปพร้อมกันทั้งหมด")


@question_type(
    "biology.evolution_theory_foundation",
    display_name={"th": "สาระสำคัญของแนวคิดลามาร์กและทฤษฎีของดาร์วิน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_THEORY,
)
class EvolutionTheoryFoundation(QuestionType):
    """Whose idea is it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        who, idea = rng.choice(THEORY_FACTS)
        if rng.random() < 0.55:
            names = sorted({w for w, _ in THEORY_FACTS} - {who})
            return _labelled(stem=f"\"{idea}\" เป็นแนวคิดหรือผลงานของใคร", correct=who, wrongs=tuple(names),
                             topic=TOPIC_THEORY, hint=THEORY_HINT)
        others = [i for w, i in THEORY_FACTS if w != who]
        return _labelled(stem=f"ข้อใดเป็นแนวคิดหรือผลงานของ{who}", correct=idea, wrongs=tuple(others),
                         topic=TOPIC_THEORY, hint=THEORY_HINT)


@question_type(
    "biology.evolution_theory_fluency",
    display_name={"th": "อธิบายปรากฏการณ์ด้วยแนวคิดลามาร์กหรือดาร์วิน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_THEORY,
)
class EvolutionTheoryFluency(QuestionType):
    """The same change, told as use-and-inherit or as selection."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case, lamarck, darwin = rng.choice(SCENARIOS)
        want_darwin = rng.random() < 0.55
        right, other = (darwin, lamarck) if want_darwin else (lamarck, darwin)
        return _labelled(stem=f"ข้อใดอธิบายเรื่อง \"{case}\" ตาม{'ทฤษฎีการคัดเลือกโดยธรรมชาติของดาร์วิน' if want_darwin else 'แนวคิดของลามาร์ก'}",
                         correct=right, wrongs=(other, *rng.sample(GENERIC_WRONGS, 2)), topic=TOPIC_THEORY, hint=THEORY_HINT)


@question_type(
    "biology.evolution_theory_application",
    display_name={"th": "คำนวณการเปลี่ยนแปลงของประชากรจากการคัดเลือกโดยธรรมชาติ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_THEORY,
)
class EvolutionTheoryApplication(QuestionType):
    """Survivors of each kind after selection, and their new share."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cases = (("ผีเสื้อกลางคืน", "สีเข้ม", "สีอ่อน", "ถูกนกจับกิน"), ("แมลง", "ที่ทนยา", "ที่ไม่ทนยา", "ตายจากยาฆ่าแมลง"),
                 ("กระต่ายบนภูเขาหิมะ", "ขนสีขาว", "ขนสีน้ำตาล", "ถูกสัตว์ผู้ล่าจับกิน"))
        who, fit, unfit, fate = rng.choice(cases)
        while True:
            a = rng.randrange(100, 1001, 100)
            b = rng.randrange(100, 1001, 100)
            loss_a = rng.choice((0, 10, 20, 25))
            loss_b = rng.choice((40, 50, 60, 75, 80, 90))
            left_a = a * (100 - loss_a) // 100
            left_b = b * (100 - loss_b) // 100
            share = Fraction(left_a * 100, left_a + left_b)
            if (share * 100).denominator == 1:
                break
        intro = (f"ประชากร{who}มีตัว{fit} {a} ตัว และตัว{unfit} {b} ตัว ต่อมาตัว{fit}{fate}ไปร้อยละ {loss_a} "
                 f"ส่วนตัว{unfit}{fate}ไปร้อยละ {loss_b}")
        hint = "หาจำนวนที่เหลือของแต่ละแบบก่อน แล้วคิดสัดส่วนจากจำนวนที่เหลือทั้งหมด"
        if rng.random() < 0.5:
            return numeric(stem=f"{intro} ตัว{fit}ที่เหลือคิดเป็นร้อยละเท่าใดของประชากรที่เหลือ", answer=share,
                           wrongs=[Fraction(a * 100, a + b), 100 - share or 50, Fraction(100 - loss_a)], unit="%", topic=TOPIC_THEORY,
                           hint=hint)
        return numeric(stem=f"{intro} เหลือ{who}ทั้งหมดกี่ตัว", answer=left_a + left_b,
                       wrongs=[a + b, left_a + b, a + left_b], unit="ตัว", topic=TOPIC_THEORY, hint=hint)

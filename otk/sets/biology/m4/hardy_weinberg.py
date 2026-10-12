"""ภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/14

Sets moved here from: science_wave_f52.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f52 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_HW = "ภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก"


CONDITIONS = ("ประชากรมีขนาดใหญ่", "สมาชิกผสมพันธุ์กันแบบสุ่ม", "ไม่เกิดมิวเทชัน", "ไม่มีการอพยพเข้าหรือออกของสมาชิก",
              "ไม่มีการคัดเลือกโดยธรรมชาติ")


BREAKERS = (
    ("เจเนติกดริฟต์", "ประชากรขนาดเล็กที่ความถี่แอลลีลเปลี่ยนไปโดยบังเอิญ เช่น เกิดภัยพิบัติจนเหลือสมาชิกไม่กี่ตัว"),
    ("การเคลื่อนย้ายยีน", "สมาชิกจากประชากรอื่นอพยพเข้ามาผสมพันธุ์"),
    ("มิวเทชัน", "แอลลีลใหม่เกิดขึ้นจากการเปลี่ยนแปลงของ DNA"),
    ("การคัดเลือกโดยธรรมชาติ", "สมาชิกที่มีลักษณะเหมาะสมอยู่รอดและมีลูกได้มากกว่า"),
    ("การผสมพันธุ์แบบไม่สุ่ม", "สมาชิกเลือกคู่ผสมที่มีลักษณะเหมือนตนเอง"),
)


HW_HINT = ("ภาวะสมดุลของฮาร์ดี-ไวน์เบิร์กต้องมีประชากรขนาดใหญ่ ผสมพันธุ์แบบสุ่ม ไม่มีมิวเทชัน ไม่มีการอพยพ "
           "และไม่มีการคัดเลือกโดยธรรมชาติ")


def tenth(rng: Random) -> Fraction:
    return Fraction(rng.randint(1, 9), 10)


@question_type(
    "biology.hardy_weinberg_foundation",
    display_name={"th": "เงื่อนไขภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก และปัจจัยที่เปลี่ยนความถี่แอลลีล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HW,
)
class HardyWeinbergFoundation(QuestionType):
    """The five conditions, and the forces that break each."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        broken = ("ประชากรมีขนาดเล็กมาก", "สมาชิกเลือกคู่ผสมพันธุ์", "เกิดมิวเทชันบ่อย", "มีสมาชิกอพยพเข้าออกเสมอ",
                  "มีการคัดเลือกโดยธรรมชาติ")
        if roll < 0.4:
            if rng.random() < 0.5:
                return _labelled(stem="ข้อใดเป็นเงื่อนไขของภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก", correct=rng.choice(CONDITIONS),
                                 wrongs=tuple(broken), topic=TOPIC_HW, hint=HW_HINT)
            return _labelled(stem="ข้อใดทำให้ประชากรไม่อยู่ในภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก", correct=rng.choice(broken),
                             wrongs=tuple(CONDITIONS), topic=TOPIC_HW, hint=HW_HINT)
        name, case = rng.choice(BREAKERS)
        others = [b for b in BREAKERS if b[0] != name]
        picked = rng.sample(others, 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{case}\" เป็นปัจจัยใดที่ทำให้ความถี่ของแอลลีลในประชากรเปลี่ยนแปลง", correct=name,
                             wrongs=tuple(b[0] for b in picked), topic=TOPIC_HW, hint=HW_HINT)
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{name}", correct=case, wrongs=tuple(b[1] for b in picked), topic=TOPIC_HW,
                         hint=HW_HINT)


@question_type(
    "biology.hardy_weinberg_fluency",
    display_name={"th": "คำนวณความถี่แอลลีลและจีโนไทป์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HW,
)
class HardyWeinbergFluency(QuestionType):
    """p + q = 1 and p² + 2pq + q² = 1; or count alleles straight from genotypes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "p + q = 1 ความถี่จีโนไทป์ AA = p² Aa = 2pq aa = q²"
        if rng.random() < 0.45:
            while True:
                total = rng.choice((100, 200, 250, 400, 500, 1000))
                aa_big = rng.randrange(5, total, 5)
                het = rng.randrange(5, total - aa_big + 1, 5)
                small = total - aa_big - het
                p = Fraction(2 * aa_big + het, 2 * total)
                if small > 0 and (p * 100).denominator == 1:
                    break
            want_p = rng.random() < 0.5
            answer = p if want_p else 1 - p
            return numeric(stem=f"ประชากรหนึ่งมีจีโนไทป์ AA {aa_big} ตัว Aa {het} ตัว และ aa {small} ตัว "
                                f"ความถี่ของแอลลีล {'A' if want_p else 'a'} เท่ากับเท่าใด",
                           answer=answer, wrongs=[1 - answer, Fraction(aa_big if want_p else small, total), Fraction(het, total),
                                                  Fraction(small if want_p else aa_big, total)],
                           unit="", topic=TOPIC_HW, hint="ความถี่แอลลีล A = (2 × จำนวน AA + จำนวน Aa) ÷ (2 × จำนวนสมาชิก)")
        p = tenth(rng)
        q = 1 - p
        given_p = rng.random() < 0.5
        asks = (("AA", p * p), ("Aa", 2 * p * q), ("aa", q * q))
        genotype, answer = rng.choice(asks)
        return numeric(stem=f"ประชากรอยู่ในภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก ความถี่ของแอลลีล {'A' if given_p else 'a'} เท่ากับ "
                            f"{show(p if given_p else q)} ความถี่ของจีโนไทป์ {genotype} เท่ากับเท่าใด",
                       answer=answer, wrongs=[p * q, p if genotype == "AA" else q, 1 - answer], unit="", topic=TOPIC_HW, hint=hint)


@question_type(
    "biology.hardy_weinberg_application",
    display_name={"th": "ประมาณจำนวนพาหะในประชากรด้วยหลักฮาร์ดี-ไวน์เบิร์ก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HW,
)
class HardyWeinbergApplication(QuestionType):
    """From the share showing the recessive trait, q = √(q²); carriers are 2pq."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        disease = rng.choice(("ผิวเผือก", "ธาลัสซีเมียชนิดหนึ่ง", "ฟีนิลคีโตนูเรีย", "ลักษณะด้อยชนิดหนึ่ง"))
        d = rng.choice((5, 10, 20, 25, 50, 100))
        q = Fraction(1, d)
        p = 1 - q
        per = d * d
        people = per * rng.choice((10, 20, 25, 40, 50, 100, 200)) if d < 50 else per * rng.choice((1, 2, 4, 5))
        intro = (f"ประชากรที่อยู่ในภาวะสมดุลของฮาร์ดี-ไวน์เบิร์กมี {people:,} คน พบผู้ที่เป็น{disease} (ควบคุมด้วยแอลลีลด้อยบนออโตโซม) "
                 f"1 คนในทุก {per:,} คน")
        hint = "q² = สัดส่วนผู้แสดงลักษณะด้อย หา q แล้ว p = 1 − q พาหะมีความถี่ 2pq"
        kind = rng.randrange(3)
        if kind == 0:
            answer = people * 2 * p * q
            return numeric(stem=f"{intro} คาดว่ามีผู้ที่เป็นพาหะกี่คน", answer=answer,
                           wrongs=[people * p * q, people * q, people * q * q], unit="คน", topic=TOPIC_HW, hint=hint)
        if kind == 1:
            answer = people * p * p
            return numeric(stem=f"{intro} คาดว่ามีผู้ที่มีจีโนไทป์เด่นพันธุ์แท้กี่คน", answer=answer,
                           wrongs=[people * p, people * (1 - q * q), people * 2 * p * q], unit="คน", topic=TOPIC_HW, hint=hint)
        answer = 100 * q
        return numeric(stem=f"{intro} ความถี่ของแอลลีลด้อยคิดเป็นร้อยละเท่าใด", answer=answer,
                       wrongs=[100 * q * q if (100 * q * q * 100).denominator == 1 else 100 * 2 * q, 100 * p, 100 * 2 * q],
                       unit="%", topic=TOPIC_HW, hint=hint)

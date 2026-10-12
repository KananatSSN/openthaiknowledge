"""การแปรผันทางพันธุกรรม

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/4

Sets moved here from: science_wave_f49.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f49 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_VAR = "การแปรผันทางพันธุกรรม"


DISCONTINUOUS = ("หมู่เลือดระบบ ABO", "การมีลักยิ้ม", "ความสามารถในการห่อลิ้น", "ลักษณะติ่งหูติดหรือติ่งหูห้อย",
                 "ตาบอดสี", "สีดอกของถั่วลันเตา", "รูปร่างเมล็ดของถั่วลันเตา", "การมีหรือไม่มีเขาของวัว")


CONTINUOUS = ("ความสูงของคน", "น้ำหนักตัวของคน", "สีผิวของคน", "ปริมาณน้ำนมของวัว", "ความยาวฝักของถั่วฝักยาว",
              "น้ำหนักเมล็ดข้าวโพด", "ขนาดของผลมะเขือเทศ")


KIND_NAMES = {"cont": "ต่อเนื่อง", "disc": "ไม่ต่อเนื่อง"}


VAR_HINT = ("การแปรผันไม่ต่อเนื่องแบ่งกลุ่มได้ชัดเจน ควบคุมด้วยยีนน้อยคู่ การแปรผันต่อเนื่องมีค่าลดหลั่นกัน "
            "ควบคุมด้วยยีนหลายคู่และสิ่งแวดล้อมมีผลมาก")


VARIATION_TRAITS = {
    "cont": ("ควบคุมด้วยยีนหลายคู่ (พอลิยีน)", "สิ่งแวดล้อมมีผลต่อการแสดงออกมาก",
             "เมื่อเขียนกราฟความถี่ได้เป็นเส้นโค้งรูประฆังคว่ำ", "วัดเป็นตัวเลขได้และมีค่าลดหลั่นกันไป",
             "แบ่งกลุ่มได้ไม่ชัดเจน"),
    "disc": ("ควบคุมด้วยยีนหนึ่งหรือสองคู่", "สิ่งแวดล้อมมีผลต่อการแสดงออกน้อย",
             "เมื่อเขียนแผนภูมิความถี่ได้แท่งที่แยกกลุ่มกันชัดเจน", "แบ่งกลุ่มได้ชัดเจน เช่น มีหรือไม่มี",
             "อัตราส่วนลูกเป็นไปตามกฎของเมนเดลได้โดยตรง"),
}


LETTERS = "ABCD"


@question_type(
    "biology.variation_foundation",
    display_name={"th": "จำแนกลักษณะที่แปรผันต่อเนื่องและไม่ต่อเนื่อง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VAR,
)
class VariationFoundation(QuestionType):
    """Sort traits into the two kinds of variation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(("cont", "disc"))
        same, other = (CONTINUOUS, DISCONTINUOUS) if kind == "cont" else (DISCONTINUOUS, CONTINUOUS)
        if rng.random() < 0.6:
            return _labelled(stem=f"ข้อใดเป็นลักษณะทางพันธุกรรมที่มีการแปรผัน{KIND_NAMES[kind]}", correct=rng.choice(same),
                             wrongs=tuple(other), topic=TOPIC_VAR, hint=VAR_HINT)
        trait = rng.choice(same)
        return _labelled(stem=f"{trait}เป็นลักษณะที่มีการแปรผันแบบใด", correct=f"การแปรผัน{KIND_NAMES[kind]}",
                         wrongs=(f"การแปรผัน{KIND_NAMES['disc' if kind == 'cont' else 'cont']}", "ไม่ใช่ลักษณะทางพันธุกรรม",
                                 "ขึ้นกับสิ่งแวดล้อมเพียงอย่างเดียว"), topic=TOPIC_VAR, hint=VAR_HINT)


@question_type(
    "biology.variation_fluency",
    display_name={"th": "เปรียบเทียบการแปรผันต่อเนื่องและไม่ต่อเนื่อง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VAR,
)
class VariationFluency(QuestionType):
    """Few genes and clear groups, against many genes, environment and a bell curve."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(("cont", "disc"))
        other = "disc" if kind == "cont" else "cont"
        if rng.random() < 0.7:
            return _labelled(stem=f"ข้อใดเป็นลักษณะของการแปรผัน{KIND_NAMES[kind]}", correct=rng.choice(VARIATION_TRAITS[kind]),
                             wrongs=tuple(VARIATION_TRAITS[other]), topic=TOPIC_VAR, hint=VAR_HINT)
        statement = rng.choice(VARIATION_TRAITS[kind])
        trait = rng.choice(CONTINUOUS if kind == "cont" else DISCONTINUOUS)
        return _labelled(stem=f"{trait} เป็นการแปรผันที่มีลักษณะตรงกับข้อใด",
                         correct=statement, wrongs=tuple(VARIATION_TRAITS[other]), topic=TOPIC_VAR,
                         hint=VAR_HINT)


@question_type(
    "biology.variation_application",
    display_name={"th": "คำนวณลักษณะที่ควบคุมด้วยพอลิยีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VAR,
)
class VariationApplication(QuestionType):
    """Additive polygenes: each dominant allele adds the same amount."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.choice((2, 3, 4))
        letters = LETTERS[:n]
        base = rng.randrange(40, 151, 5)
        step = rng.choice((2, 2.5, 3, 4, 5, 6, 7.5, 8))
        step = Fraction(step)
        intro = (f"ความสูงของพืชชนิดหนึ่งถูกควบคุมด้วยยีน {n} คู่ ({', '.join(f'{c}/{c.lower()}' for c in letters)}) "
                 f"ที่อยู่คนละโครโมโซม ต้นที่ไม่มีแอลลีลตัวใหญ่เลยสูง {base} cm และแอลลีลตัวใหญ่แต่ละตัวเพิ่มความสูง {show(step)} cm")
        hint = "ความสูง = ความสูงฐาน + (จำนวนแอลลีลตัวใหญ่ × ความสูงที่เพิ่มต่อแอลลีล) ลูกจากพันธุ์ทางทุกคู่มีได้ 0 ถึง 2n แอลลีล"
        kind = rng.randrange(4)
        genotype = "".join(rng.choice((c + c, c + c.lower(), c.lower() + c.lower())) for c in letters)
        big = sum(ch.isupper() for ch in genotype)
        if kind == 0:
            return numeric(stem=f"{intro} ต้นจีโนไทป์ {genotype} สูงกี่ cm", answer=base + big * step,
                           wrongs=[base + (big + 1) * step, base + max(big - 1, 0) * step, base + big * step * 2], unit="cm",
                           topic=TOPIC_VAR, hint=hint)
        if kind == 1:
            return numeric(stem=f"{intro} ต้นที่สูง {show(base + big * step)} cm มีแอลลีลตัวใหญ่กี่แอลลีล", answer=big,
                           wrongs=[big + 1, max(big - 1, 0) or big + 2, 2 * n], unit="แอลลีล", topic=TOPIC_VAR, hint=hint)
        hetero = "".join(c + c.lower() for c in letters)
        if kind == 2:
            return numeric(stem=f"{intro} ผสม {hetero} × {hetero} ลูกมีความสูงแตกต่างกันได้กี่แบบ", answer=2 * n + 1,
                           wrongs=[2 * n, 3 ** n, 2 ** n], unit="แบบ", topic=TOPIC_VAR, hint=hint)
        tall, short = "".join(c + c for c in letters), "".join(c.lower() * 2 for c in letters)
        return numeric(stem=f"{intro} ผสมต้น {tall} กับต้น {short} ลูก F₁ สูงกี่ cm", answer=base + n * step,
                       wrongs=[base + 2 * n * step, base, base + (n + 1) * step], unit="cm", topic=TOPIC_VAR, hint=hint)

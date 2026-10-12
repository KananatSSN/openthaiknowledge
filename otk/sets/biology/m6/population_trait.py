"""ลักษณะเฉพาะของประชากร

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/6

Sets moved here from: science_wave_f72.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f72 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_TRAIT = "ลักษณะเฉพาะของประชากร"


DISPERSION = {
    "แบบกลุ่ม": ("ต้นไผ่ขึ้นเป็นกอ ๆ", "ปลาว่ายรวมเป็นฝูง", "ช้างป่าอยู่รวมเป็นโขลง"),
    "แบบสม่ำเสมอ": ("ต้นยางพาราในสวนที่ปลูกเป็นแถว", "นกนางนวลทำรังห่างกันเท่า ๆ กันบนหน้าผา", "ต้นไม้ในทะเลทรายที่แย่งน้ำกันจนขึ้นห่างเท่า ๆ กัน"),
    "แบบสุ่ม": ("ต้นหญ้าที่งอกจากเมล็ดที่ลมพัดมาตกทั่วทุ่ง", "แมงมุมบางชนิดกระจายอยู่ในป่าโดยไม่มีรูปแบบ", "ต้นไม้ในป่าที่ดินและแสงสม่ำเสมอ"),
}


SURVIVAL = (
    ("แบบที่ 1", "ตายน้อยในวัยเด็กและวัยกลางคน ตายมากในวัยชรา", ("คน", "ช้าง")),
    ("แบบที่ 2", "อัตราการตายใกล้เคียงกันทุกช่วงอายุ", ("ไฮดรา", "นกบางชนิด")),
    ("แบบที่ 3", "ตายมากในวัยอ่อน ส่วนที่รอดมีชีวิตยืนยาว", ("หอยนางรม", "ปลาที่วางไข่ครั้งละมาก ๆ")),
)


TRAIT_HINT = ("ความหนาแน่น = จำนวนต่อพื้นที่ การกระจายมีแบบกลุ่ม สม่ำเสมอ และสุ่ม โครงสร้างอายุที่ฐานกว้างบอกว่าประชากรกำลังเพิ่ม "
              "การจับ-ติดเครื่องหมาย-จับซ้ำ: N = (จำนวนที่ติดเครื่องหมาย × จำนวนที่จับครั้งที่สอง) ÷ จำนวนที่มีเครื่องหมายในครั้งที่สอง")


@question_type(
    "biology.population_trait_foundation",
    display_name={"th": "การกระจายและการรอดชีวิตของประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class PopulationTraitFoundation(QuestionType):
    """Clumped, uniform or random; and the three survivorship curves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            kind = rng.choice(sorted(DISPERSION))
            example = rng.choice(DISPERSION[kind])
            others = [k for k in DISPERSION if k != kind]
            if rng.random() < 0.5:
                return _labelled(stem=f"\"{example}\" เป็นการกระจายของประชากรแบบใด", correct=kind, wrongs=(*others, "แบบเอ็กโพเนนเชียล"),
                                 topic=TOPIC_TRAIT, hint=TRAIT_HINT)
            pool = [e for k in others for e in DISPERSION[k]]
            return _labelled(stem=f"ข้อใดเป็นการกระจายของประชากร{kind}", correct=example, wrongs=tuple(pool), topic=TOPIC_TRAIT,
                             hint=TRAIT_HINT)
        kind, shape, animals = rng.choice(SURVIVAL)
        others = [s for s in SURVIVAL if s[0] != kind]
        if rng.random() < 0.5:
            return _labelled(stem=f"การรอดชีวิตของ{rng.choice(animals)}เป็นแบบใด", correct=f"{kind}: {shape}",
                             wrongs=(*(f"{s[0]}: {s[1]}" for s in others), "ไม่มีรูปแบบการตายใดเลย"), topic=TOPIC_TRAIT, hint=TRAIT_HINT)
        pool = [a for s in others for a in s[2]]
        return _labelled(stem=f"สิ่งมีชีวิตใดมีรูปแบบการรอดชีวิตแบบที่ \"{shape}\"", correct=rng.choice(animals), wrongs=tuple(pool),
                         topic=TOPIC_TRAIT, hint=TRAIT_HINT)


@question_type(
    "biology.population_trait_fluency",
    display_name={"th": "โครงสร้างอายุของประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class PopulationTraitFluency(QuestionType):
    """Read an age pyramid from its shares."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.choice(("grow", "steady", "shrink"))
        young = {"grow": rng.randrange(40, 56), "steady": rng.randrange(30, 36), "shrink": rng.randrange(12, 20)}[shape]
        old = {"grow": rng.randrange(5, 11), "steady": rng.randrange(22, 30), "shrink": rng.randrange(35, 46)}[shape]
        mid = 100 - young - old
        answers = {"grow": "ประชากรกำลังเพิ่มขึ้น", "steady": "ประชากรค่อนข้างคงที่", "shrink": "ประชากรกำลังลดลง"}
        return _labelled(stem=f"ประชากรหนึ่งมีวัยก่อนเจริญพันธุ์ร้อยละ {young} วัยเจริญพันธุ์ร้อยละ {mid} และวัยหลังเจริญพันธุ์ร้อยละ {old} "
                              f"แนวโน้มของประชากรนี้เป็นอย่างไร", correct=answers[shape],
                         wrongs=(*(v for k, v in answers.items() if k != shape), "บอกไม่ได้ว่ามีเพศใดมากกว่า"), topic=TOPIC_TRAIT,
                         hint="ฐานพีระมิดกว้าง (วัยเด็กมาก) ประชากรเพิ่ม ใกล้เคียงกันทุกวัย ประชากรคงที่ ฐานแคบกว่ายอด ประชากรลดลง")


@question_type(
    "biology.population_trait_application",
    display_name={"th": "คำนวณความหนาแน่นและขนาดประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class PopulationTraitApplication(QuestionType):
    """Density per area, and mark-recapture estimates."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            while True:
                marked = rng.randrange(20, 201, 5)
                second = rng.randrange(20, 201, 5)
                recaptured = rng.randrange(2, min(marked, second) // 2 + 1)
                n = Fraction(marked * second, recaptured)
                if n.denominator == 1:
                    break
            animal = rng.choice(("ปลาในบ่อ", "หนูในทุ่งนา", "กิ้งก่าบนเกาะ", "ผีเสื้อในสวน"))
            return numeric(stem=f"จับ{animal}มาติดเครื่องหมาย {marked} ตัวแล้วปล่อยคืน ต่อมาจับใหม่ {second} ตัว พบที่มีเครื่องหมาย {recaptured} ตัว "
                                f"ประมาณขนาดประชากรได้กี่ตัว", answer=n,
                           wrongs=[marked + second, marked * second, Fraction(marked * recaptured, second) if Fraction(marked * recaptured, second).denominator == 1
                                   else marked + second - recaptured], unit="ตัว", topic=TOPIC_TRAIT, hint=TRAIT_HINT)
        count = rng.randrange(20, 2001, 10)
        area = rng.choice((2, 4, 5, 10, 20, 25, 50))
        density = Fraction(count, area)
        if (density * 100).denominator != 1:
            area = 10
            density = Fraction(count, area)
        return numeric(stem=f"สำรวจพบต้นหญ้าแฝก {count} ต้น ในพื้นที่ {area} ตารางเมตร ความหนาแน่นของประชากรเป็นกี่ต้นต่อตารางเมตร",
                       answer=density, wrongs=[count * area, Fraction(area, count) if (Fraction(area, count) * 100).denominator == 1 else density * 2,
                                               count], unit="ต้นต่อตารางเมตร", topic=TOPIC_TRAIT, hint=TRAIT_HINT)

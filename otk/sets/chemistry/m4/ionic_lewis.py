"""การเกิดไอออนและพันธะไอออนิก

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/9

Sets moved here from: science_wave_f20.
"""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f19 import REPRESENTATIVE
from otk.sets._support.science_wave_f20 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_IONIC = "การเกิดไอออนและพันธะไอออนิก"


SUPERSCRIPT = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


IONIC_ELEMENTS = tuple(e for e in REPRESENTATIVE if e[4] in (1, 2, 13, 15, 16, 17) and e[1] not in ("B", "Ga", "As", "Se", "Ge", "Si", "C"))


def valence(element) -> int:
    group = element[4]
    return group if group <= 2 else group - 10


def ion_charge(element) -> int:
    v = valence(element)
    return v if v <= 3 else v - 8


def ion_text(element) -> str:
    charge = ion_charge(element)
    size = "" if abs(charge) == 1 else str(abs(charge))
    return f"{element[1]}{(size + ('+' if charge > 0 else '-')).translate(SUPERSCRIPT)}"


@question_type(
    "chem.ionic_lewis_foundation",
    display_name={"th": "สัญลักษณ์แบบจุดของลิวอิสและเวเลนซ์อิเล็กตรอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_IONIC,
)
class IonicLewisFoundation(QuestionType):
    """Dots in a Lewis symbol are the valence electrons."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element = rng.choice(REPRESENTATIVE)
        if rng.random() < 0.5:
            others = rng.sample([e for e in REPRESENTATIVE if valence(e) != valence(element)], 3)
            return _labelled(
                stem=f"ธาตุใดมีสัญลักษณ์แบบจุดของลิวอิสเป็นสัญลักษณ์ธาตุล้อมด้วย {valence(element)} จุด",
                correct=f"{element[2]} ({element[1]}) หมู่ {element[4]}",
                wrongs=tuple(f"{e[2]} ({e[1]}) หมู่ {e[4]}" for e in others), topic=TOPIC_IONIC,
                hint="จำนวนจุดเท่ากับเวเลนซ์อิเล็กตรอน: หมู่ 1-2 เท่ากับเลขหมู่ หมู่ 13-17 เท่ากับเลขหมู่ − 10")
        return numeric(
            stem=f"สัญลักษณ์แบบจุดของลิวอิสของ{element[2]} ({element[1]}) ซึ่งอยู่หมู่ {element[4]} มีจุดรอบสัญลักษณ์กี่จุด",
            answer=valence(element), wrongs=[element[4] if element[4] != valence(element) else 8, element[3], 8 - valence(element) or 1],
            unit="จุด", topic=TOPIC_IONIC, hint="จำนวนจุดเท่ากับเวเลนซ์อิเล็กตรอน: หมู่ 1-2 เท่ากับเลขหมู่ หมู่ 13-17 เท่ากับเลขหมู่ − 10")


@question_type(
    "chem.ionic_lewis_fluency",
    display_name={"th": "ไอออนที่ธาตุเรพรีเซนเททีฟเกิดขึ้นตามกฎออกเตต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_IONIC,
)
class IonicLewisFluency(QuestionType):
    """Metals give up their valence electrons; non-metals take enough to reach eight."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element = rng.choice(IONIC_ELEMENTS)
        charge = ion_charge(element)
        right = ion_text(element)
        if rng.random() < 0.5:
            if rng.random() < 0.5:
                return numeric(
                    stem=f"{element[2]} (Z = {element[0]}) เมื่อเกิดเป็นไอออน {right} มีอิเล็กตรอนกี่ตัว",
                    answer=element[0] - charge, wrongs=[element[0], element[0] + charge, element[0] - charge + 2],
                    unit="ตัว", topic=TOPIC_IONIC, hint="ไอออนบวกมีอิเล็กตรอนน้อยกว่าโปรตอนเท่ากับประจุ ไอออนลบมีมากกว่า")
            return numeric(
                stem=f"{element[2]} (หมู่ {element[4]}) {'เสีย' if charge > 0 else 'รับ'}อิเล็กตรอนกี่ตัวเมื่อเกิดเป็นไอออนที่เสถียร",
                answer=abs(charge), wrongs=[valence(element) if valence(element) != abs(charge) else 8, 8 - abs(charge), abs(charge) + 1],
                unit="ตัว", topic=TOPIC_IONIC, hint="โลหะเสียเวเลนซ์อิเล็กตรอนทั้งหมด อโลหะรับอิเล็กตรอนจนครบแปด")
        pool = set()
        for c in (-charge, charge + 1, charge - 1, charge + 2 if charge > 0 else charge - 2):
            if c == 0:
                continue
            size = "" if abs(c) == 1 else str(abs(c))
            pool.add(f"{element[1]}{(size + ('+' if c > 0 else '-')).translate(SUPERSCRIPT)}")
        pool.discard(right)
        return _labelled(stem=f"{element[2]} ({element[1]}) หมู่ {element[4]} เกิดไอออนใดเพื่อให้มีการจัดเรียงอิเล็กตรอนแบบแก๊สมีตระกูล",
                         correct=right, wrongs=tuple(sorted(pool)[:3]), topic=TOPIC_IONIC,
                         hint="โลหะเสียเวเลนซ์อิเล็กตรอนเป็นไอออนบวก อโลหะรับอิเล็กตรอนจนครบแปดเป็นไอออนลบ")


@question_type(
    "chem.ionic_lewis_application",
    display_name={"th": "การถ่ายโอนอิเล็กตรอนเมื่อเกิดพันธะไอออนิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_IONIC,
)
class IonicLewisApplication(QuestionType):
    """Pair a metal with a non-metal: the ratio of ions and the electrons that move."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal = rng.choice([e for e in IONIC_ELEMENTS if ion_charge(e) > 0])
        nonmetal = rng.choice([e for e in IONIC_ELEMENTS if ion_charge(e) < 0])
        p, q = ion_charge(metal), -ion_charge(nonmetal)
        k = gcd(p, q)
        metals, nonmetals = q // k, p // k
        transferred = metals * p
        if rng.random() < 0.5:
            return numeric(
                stem=(f"{metal[2]} (หมู่ {metal[4]}) ทำปฏิกิริยากับ{nonmetal[2]} (หมู่ {nonmetal[4]}) เกิดสารประกอบไอออนิก "
                      "หนึ่งหน่วยสูตร มีการถ่ายโอนอิเล็กตรอนทั้งหมดกี่ตัว"),
                answer=transferred, wrongs=[p, q, p + q if p + q != transferred else transferred * 2], unit="ตัว",
                topic=TOPIC_IONIC, hint="หาไอออนของแต่ละธาตุ แล้วหาจำนวนไอออนที่ทำให้ประจุรวมเป็นศูนย์ อิเล็กตรอนที่ถ่ายโอน = ประจุบวกรวม")
        sub = lambda n: "" if n == 1 else str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
        right = f"{metal[1]}{sub(metals)}{nonmetal[1]}{sub(nonmetals)}"
        pool = {f"{metal[1]}{sub(nonmetals)}{nonmetal[1]}{sub(metals)}", f"{metal[1]}{nonmetal[1]}",
                f"{metal[1]}{sub(p)}{nonmetal[1]}{sub(q)}", f"{metal[1]}{sub(metals + 1)}{nonmetal[1]}{sub(nonmetals)}",
                f"{metal[1]}{nonmetal[1]}{sub(nonmetals + 1)}", f"{metal[1]}{sub(2)}{nonmetal[1]}{sub(3)}",
                f"{metal[1]}{sub(3)}{nonmetal[1]}{sub(2)}"}
        pool.discard(right)
        return _labelled(stem=f"สารประกอบไอออนิกที่เกิดจาก{metal[2]} ({ion_text(metal)}) กับ{nonmetal[2]} ({ion_text(nonmetal)}) มีสูตรใด",
                         correct=right, wrongs=tuple(sorted(pool)), topic=TOPIC_IONIC,
                         hint="จำนวนไอออนต้องทำให้ประจุบวกรวมเท่ากับประจุลบรวม (สลับเลขประจุแล้วทำให้เป็นอัตราส่วนอย่างต่ำ)")

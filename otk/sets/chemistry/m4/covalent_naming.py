"""สูตรและการเรียกชื่อสารโคเวเลนต์

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/15

Sets moved here from: science_wave_f22.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f22 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_NAME = "สูตรและการเรียกชื่อสารโคเวเลนต์"


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


PREFIX = {1: "มอนอ", 2: "ได", 3: "ไตร", 4: "เตตระ", 5: "เพนตะ", 6: "เฮกซะ", 7: "เฮปตะ"}


FIRST = (("C", "คาร์บอน"), ("N", "ไนโตรเจน"), ("P", "ฟอสฟอรัส"), ("S", "ซัลเฟอร์"), ("Si", "ซิลิคอน"), ("B", "โบรอน"),
         ("Cl", "คลอรีน"), ("Xe", "ซีนอน"))


SECOND = (("O", "ออกไซด์"), ("Cl", "คลอไรด์"), ("F", "ฟลูออไรด์"), ("Br", "โบรไมด์"), ("S", "ซัลไฟด์"), ("I", "ไอโอไดด์"))


COMPOUNDS = (("C", 1, "O", 1), ("C", 1, "O", 2), ("N", 2, "O", 1), ("N", 1, "O", 1), ("N", 1, "O", 2), ("N", 2, "O", 3),
             ("N", 2, "O", 4), ("N", 2, "O", 5), ("P", 1, "Cl", 3), ("P", 1, "Cl", 5), ("P", 2, "O", 5), ("P", 4, "O", 10),
             ("S", 1, "O", 2), ("S", 1, "O", 3), ("S", 1, "F", 6), ("C", 1, "Cl", 4), ("Si", 1, "O", 2), ("Si", 1, "Cl", 4),
             ("B", 1, "F", 3), ("C", 1, "S", 2), ("Cl", 2, "O", 7), ("Xe", 1, "F", 4), ("N", 1, "Cl", 3), ("P", 1, "Br", 3),
             ("S", 1, "Cl", 2), ("C", 1, "Br", 4), ("B", 1, "Cl", 3), ("I", 1, "Cl", 3))


PREFIX_EXTRA = {10: "เดคะ"}


def covalent_formula(a, na, b, nb) -> str:
    part = lambda s, n: s if n == 1 else f"{s}{str(n).translate(SUB)}"
    return part(a, na) + part(b, nb)


def covalent_name(a, na, b, nb) -> str:
    first = dict(FIRST).get(a, "ไอโอดีน" if a == "I" else a)
    second = dict(SECOND)[b]
    lead = "" if na == 1 else {**PREFIX, **PREFIX_EXTRA}[na]
    prefix = {**PREFIX, **PREFIX_EXTRA}[nb]
    # Thai names keep the whole prefix (เตตระออกไซด์, เพนตะออกไซด์); only mono-oxide elides.
    tail = "มอนอกไซด์" if nb == 1 and b == "O" else prefix + second
    return f"{lead}{first}{tail}"


@question_type(
    "chem.covalent_naming_foundation",
    display_name={"th": "เรียกชื่อสารโคเวเลนต์จากสูตร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NAME,
)
class CovalentNamingFoundation(QuestionType):
    """Greek prefixes give the count of each atom; the first atom drops mono-."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, na, b, nb = rng.choice(COMPOUNDS)
        right = covalent_name(a, na, b, nb)
        # Wrong counts of the second atom, a wrong count of the first, and the name without prefixes.
        pool = {covalent_name(a, na, b, n) for n in range(1, 8) if n != nb and abs(n - nb) <= 2}
        pool |= {covalent_name(a, n, b, nb) for n in (1, 2) if n != na}
        pool.add(dict(FIRST).get(a, "ไอโอดีน") + dict(SECOND)[b])
        pool.discard(right)
        return _labelled(stem=f"สาร {covalent_formula(a, na, b, nb)} มีชื่อว่าอย่างไร", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_NAME,
                         hint="บอกจำนวนอะตอมด้วยคำนำหน้า มอนอ ได ไตร เตตระ เพนตะ เฮกซะ (ธาตุแรกที่มีอะตอมเดียวไม่ต้องใส่มอนอ)")


@question_type(
    "chem.covalent_naming_fluency",
    display_name={"th": "เขียนสูตรสารโคเวเลนต์จากชื่อ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NAME,
)
class CovalentNamingFluency(QuestionType):
    """From the prefixes back to the subscripts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, na, b, nb = rng.choice(COMPOUNDS)
        right = covalent_formula(a, na, b, nb)
        pool = {covalent_formula(a, nb, b, na), covalent_formula(a, na, b, nb + 1), covalent_formula(a, 1, b, 1),
                covalent_formula(b, nb, a, na), covalent_formula(a, na + 1, b, nb)}
        pool.discard(right)
        return _labelled(stem=f"{covalent_name(a, na, b, nb)} มีสูตรเคมีใด", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_NAME,
                         hint="คำนำหน้าบอกจำนวนอะตอม: ได = 2 ไตร = 3 เตตระ = 4 เพนตะ = 5 เฮกซะ = 6")


@question_type(
    "chem.covalent_naming_application",
    display_name={"th": "จำนวนอะตอมในสารโคเวเลนต์จากชื่อ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NAME,
)
class CovalentNamingApplication(QuestionType):
    """Count the atoms, or the atoms of one element, named in a molecule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, na, b, nb = rng.choice(COMPOUNDS)
        label = covalent_name(a, na, b, nb)
        if rng.random() < 0.5:
            return numeric(stem=f"{label} หนึ่งโมเลกุลมีอะตอมทั้งหมดกี่อะตอม", answer=na + nb,
                           wrongs=[nb, na * nb, na + nb + 1], unit="อะตอม", topic=TOPIC_NAME,
                           hint="แปลงคำนำหน้าเป็นจำนวนอะตอมของแต่ละธาตุแล้วรวมกัน")
        count = rng.randint(2, 6)
        return numeric(stem=f"{label} {count} โมเลกุลมีอะตอมของ {b} ทั้งหมดกี่อะตอม", answer=count * nb,
                       wrongs=[nb, count * (na + nb), count + nb], unit="อะตอม", topic=TOPIC_NAME,
                       hint="จำนวนอะตอม = จำนวนโมเลกุล × จำนวนอะตอมต่อโมเลกุล")

"""สูตรและการเรียกชื่อสารประกอบไอออนิก

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/10

Sets moved here from: science_wave_f21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f21 import (
    ANIONS,
    CATIONS,
    SUBJECT,
    UPPER_FOUR,
    _pairs,
    _part,
    formula,
    ion,
    name,
)

PROVENANCE = Provenance("original")


TOPIC_FORMULA = "สูตรและการเรียกชื่อสารประกอบไอออนิก"


def _formula_wrongs(cation, anion, rng: Random) -> tuple[str, ...]:
    p, q = cation[2], anion[2]
    right = formula(cation, anion)
    pool = {_part(cation[0], p, cation[3]) + _part(anion[0], q, anion[3]),
            _part(cation[0], 1, cation[3]) + _part(anion[0], 1, anion[3]),
            _part(cation[0], q + 1, cation[3]) + _part(anion[0], p, anion[3]),
            _part(cation[0], 2, cation[3]) + _part(anion[0], 3, anion[3]),
            _part(cation[0], 3, cation[3]) + _part(anion[0], 2, anion[3]),
            _part(cation[0], 1, cation[3]) + _part(anion[0], max(p, q) + 1, anion[3])}
    pool.discard(right)
    return tuple(rng.sample(sorted(pool), 3))


@question_type(
    "chem.ionic_naming_foundation",
    display_name={"th": "เขียนสูตรสารประกอบไอออนิกจากชื่อ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class IonicNamingFoundation(QuestionType):
    """From a name, balance the charges into a formula."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion = rng.choice(_pairs())
        return _labelled(stem=f"{name(cation, anion)} มีสูตรเคมีใด ({ion(cation, 1)}, {ion(anion, -1)})",
                         correct=formula(cation, anion), wrongs=_formula_wrongs(cation, anion, rng), topic=TOPIC_FORMULA,
                         hint="ประจุบวกรวมต้องเท่ากับประจุลบรวม ใส่วงเล็บเมื่อไอออนกลุ่มอะตอมมีมากกว่าหนึ่ง")


@question_type(
    "chem.ionic_naming_fluency",
    display_name={"th": "เรียกชื่อสารประกอบไอออนิกจากสูตร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class IonicNamingFluency(QuestionType):
    """Cation name first, then the anion's -ide or -ate name."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion = rng.choice([p for p in _pairs() if "(" not in p[0][1]])
        right = name(cation, anion)
        others = [a for a in ANIONS if a[0] != anion[0]]
        pool = {name(cation, a) for a in rng.sample(others, 2)}
        pool.add(f"{anion[1]}{cation[1]}")
        other_cats = [c for c in CATIONS if c[0] != cation[0] and "(" not in c[1]]
        pool.add(name(rng.choice(other_cats), anion))
        pool.discard(right)
        return _labelled(stem=f"สารประกอบ {formula(cation, anion)} มีชื่อว่าอย่างไร", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_FORMULA,
                         hint="อ่านชื่อไอออนบวกก่อน แล้วตามด้วยชื่อไอออนลบ (ลงท้าย -ไอด์ หรือชื่อไอออนกลุ่มอะตอม)")


@question_type(
    "chem.ionic_naming_application",
    display_name={"th": "ชื่อและสูตรของสารประกอบที่โลหะมีได้หลายประจุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class IonicNamingApplication(QuestionType):
    """Roman numerals: read the metal's charge from the formula, or build the formula from it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion = rng.choice([p for p in _pairs() if "(" in p[0][1]])
        twins = [c for c in CATIONS if c[0] == cation[0] and c is not cation]
        right = name(cation, anion)
        if rng.random() < 0.5:
            base = cation[1].split("(")[0]
            wrongs = {name(t, anion) for t in twins}
            wrongs |= {f"{base}({roman}) {anion[1]}" for roman in ("I", "II", "III", "IV")}
            wrongs.add(f"{base}{anion[1]}")
            wrongs.add(name(cation, rng.choice([a for a in ANIONS if a[0] != anion[0]])))
            wrongs.discard(right)
            return _labelled(stem=f"สารประกอบ {formula(cation, anion)} มีชื่อว่าอย่างไร", correct=right,
                             wrongs=tuple(sorted(wrongs)), topic=TOPIC_FORMULA,
                             hint="หาประจุของโลหะจากประจุลบรวมก่อน แล้วระบุด้วยเลขโรมันในวงเล็บ")
        return _labelled(stem=f"{right} มีสูตรเคมีใด ({ion(anion, -1)})", correct=formula(cation, anion),
                         wrongs=_formula_wrongs(cation, anion, rng), topic=TOPIC_FORMULA,
                         hint="เลขโรมันบอกประจุของโลหะ แล้วทำให้ประจุรวมเป็นศูนย์")

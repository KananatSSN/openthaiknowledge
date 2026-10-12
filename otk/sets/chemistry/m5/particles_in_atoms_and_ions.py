"""จำนวนอนุภาคของอะตอมและไอออน

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/3

Sets moved here from: science_successors, science_wave_a5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import ELEMENTS, Element, Item, common_charges, full_name
from otk.sets._support.science_wave_a5 import (
    BY_Z,
    METALLOID_SYMBOLS,
    NUCLIDE_MAX_Z,
    SUBJECT,
    TOPIC_ATOM,
    _labelled,
    _nuclide,
)
from otk.sets.chemistry.m1.particles import _PinnedParticleCount

PROVENANCE = Provenance("original")


PROTON, NEUTRON, ELECTRON = "โปรตอน", "นิวตรอน", "อิเล็กตรอน"


# Metalloids are kept out of the ion drills. The หมู่ rule hands โบรอน a B3+ that
# no ม.5 course teaches as a real ion, and the rest of the staircase forms ions
# only in compounds well past this level.
def _forms_a_taught_ion(el: Element) -> bool:
    return (bool(common_charges(el)) and el.z <= NUCLIDE_MAX_Z
            and el.symbol not in METALLOID_SYMBOLS)


# Elements that form exactly one common monatomic ion, so "which ion does this
# atom form" has a single answer.
SINGLE_ION_ELEMENTS: tuple[Element, ...] = tuple(
    el for el in ELEMENTS
    if _forms_a_taught_ion(el) and len(common_charges(el)) == 1
)


def _charge_words(charge: int) -> str:
    return f"{'เสีย' if charge > 0 else 'รับ'}อิเล็กตรอน {abs(charge)} อนุภาค"


# Every ion the ม.5 drills recognise, with the charge it carries. An ion is kept
# only if it still holds an electron, which drops H+ — a bare proton has no
# electron count to identify it by, and no element sits at เลขอะตอม 0.
ION_POOL: tuple[tuple[Element, int], ...] = tuple(
    (el, charge)
    for el in ELEMENTS if _forms_a_taught_ion(el)
    for charge in common_charges(el)
    if el.z - charge >= 1
)


# The noble gases an ion can be isoelectronic with.
NOBLE_GASES: tuple[Element, ...] = tuple(
    el for el in ELEMENTS if el.group == 8 and el.z <= 36
)


@question_type(
    "chem.ion_particles_foundation",
    display_name={"th": "อะตอมกลายเป็นไอออน: อนุภาคใดเปลี่ยนไป"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ATOM,
)
class IonParticlesFoundation(QuestionType):
    """What changes when an atom becomes an ion — the fact the counting rests on.

    Deliberately not a counting drill: ``chem.particles_ions`` already counts
    particles for a given ion, and this set exists so the learner can say *why*
    only one of the three counts ever moves.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _labelled(
                stem="เมื่ออะตอมที่เป็นกลางกลายเป็นไอออน จำนวนอนุภาคชนิดใดเปลี่ยนแปลงไป",
                correct=ELECTRON,
                wrongs=(PROTON, NEUTRON, "ทั้งโปรตอนและนิวตรอน"),
                topic=TOPIC_ATOM,
                hint=("ไอออนเกิดจากการให้หรือรับอิเล็กตรอนที่อยู่วงนอก "
                      "อนุภาคในนิวเคลียสไม่ได้เปลี่ยนแปลง"),
            )
        el = rng.choice(SINGLE_ION_ELEMENTS)
        charge = common_charges(el)[0]
        verb = "เสีย" if charge > 0 else "รับ"
        return _labelled(
            stem=f"อะตอมของธาตุ {full_name(el)} กลายเป็นไอออนที่พบทั่วไปได้อย่างไร",
            correct=_charge_words(charge),
            wrongs=(
                _charge_words(-charge),
                f"{verb}โปรตอน {abs(charge)} อนุภาค",
                f"{verb}นิวตรอน {abs(charge)} อนุภาค",
            ),
            topic=TOPIC_ATOM,
            hint=("ธาตุหมู่ทางซ้ายเสียอิเล็กตรอนจนเหลือวงนอกเต็ม "
                  "ส่วนธาตุหมู่ทางขวารับอิเล็กตรอนเข้ามาจนวงนอกเต็ม"),
        )


@question_type(
    "chem.particles_ions",
    display_name={"th": "โปรตอน นิวตรอน อิเล็กตรอนของไอออน"},
    level={"th": "ม.5"}, subject="เคมี", topic="โครงสร้างอะตอม",
)
class IonParticleCount(_PinnedParticleCount):
    source_key = "chem.particles"

    def _item_pool(self, group_lo: int, group_hi: int, z_lo: int, z_hi: int):
        pool = super()._item_pool(group_lo, group_hi, z_lo, z_hi)
        charged = [element for element in pool if common_charges(element)]
        if not charged:
            raise ValueError("selected element range contains no common monatomic ions")
        return charged

    def _draw_item(self, rng: Random, pool, asked: str) -> Item:
        element = rng.choice(pool)
        return Item(element, asked, rng.choice(common_charges(element)))


@question_type(
    "chem.ion_particles_application",
    display_name={"th": "จำนวนอนุภาค → ระบุไอออน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_ATOM,
)
class IonParticlesApplication(QuestionType):
    """Identify a particle from its three counts, or find the isoelectronic ion.

    Both directions run the ม.5/3 rule backwards: the learner is given counts and
    has to say which single-atom particle they describe.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return self._identify(rng)
        return self._isoelectronic(rng)

    def _identify(self, rng: Random) -> GeneratedQuestion:
        el, charge = rng.choice(ION_POOL)
        neutrons = el.mass - el.z
        electrons = el.z - charge
        return GeneratedQuestion(
            stem=[text(f"อนุภาคหนึ่งมีโปรตอน {el.z} อนุภาค นิวตรอน {neutrons} อนุภาค "
                       f"และอิเล็กตรอน {electrons} อนุภาค อนุภาคนี้คือข้อใด")],
            correct=_nuclide(el.mass, el.z, el.symbol, charge),
            distractors=fixed(
                # เครื่องหมายประจุกลับด้าน
                _nuclide(el.mass, el.z, el.symbol, -charge),
                # ตอบเป็นอะตอมที่เป็นกลาง ทั้งที่อิเล็กตรอนไม่เท่ากับโปรตอน
                _nuclide(el.mass, el.z, el.symbol),
                # ใช้จำนวนอิเล็กตรอนเป็นเลขอะตอม
                _nuclide(el.mass, electrons, BY_Z[electrons].symbol, charge),
            ),
            topic=TOPIC_ATOM,
            hint=[text("เลขอะตอมมาจากจำนวนโปรตอนเสมอ "
                       "ส่วนประจุคือจำนวนโปรตอนลบด้วยจำนวนอิเล็กตรอน")],
        )

    def _isoelectronic(self, rng: Random) -> GeneratedQuestion:
        noble = rng.choice(NOBLE_GASES)
        matching = [item for item in ION_POOL if item[0].z - item[1] == noble.z]
        others = [item for item in ION_POOL if item[0].z - item[1] != noble.z]
        if not matching or len(others) < 3:
            return self._identify(rng)

        def label(el: Element, charge: int) -> str:
            size = abs(charge) if abs(charge) > 1 else ""
            sign = "+" if charge > 0 else "-"
            return f"ไอออน {el.symbol}{size}{sign} ของธาตุ {full_name(el)}"

        el, charge = rng.choice(matching)
        rng.shuffle(others)
        return _labelled(
            stem=(f"ไอออนในข้อใดมีจำนวนอิเล็กตรอนเท่ากับอะตอมของธาตุ {full_name(noble)} "
                  f"ซึ่งมีอิเล็กตรอน {noble.z} อนุภาค"),
            correct=label(el, charge),
            wrongs=tuple(label(other, other_charge)
                         for other, other_charge in others[:3]),
            topic=TOPIC_ATOM,
            hint=("จำนวนอิเล็กตรอนของไอออนคือเลขอะตอมลบด้วยประจุ "
                  "ไอออนบวกจึงมีอิเล็กตรอนน้อยกว่าเลขอะตอม"),
        )

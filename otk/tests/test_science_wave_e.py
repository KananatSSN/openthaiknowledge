"""Acceptance gate for Phase 5 Wave E — upper-secondary basic science, ``ม.4``-``ม.6``.

Slice 1 opens ``ว 2.1 ม.5`` with the atomic-structure cluster: ``ม.5/1``
(ธาตุ/สารประกอบ and อะตอม/โมเลกุล/ไอออน from a chemical formula), ``ม.5/2``
(the Bohr model vs the electron-cloud model), and ``ม.5/4`` (writing a nuclide
symbol and identifying an isotope — two free verbs, so both Foundation and
Fluency are exact).

Slice 2 adds ``ม.5/5`` (หมู่/คาบ and metal/nonmetal/metalloid/representative/
transition classification from the periodic table), ``ม.5/6`` (comparing
conductivity and electron-giving/receiving between metals and nonmetals), and
``ม.5/7`` (benefit/hazard examples for representative and transition elements
— สืบค้นข้อมูลและนำเสนอตัวอย่าง files under the default pattern, the same
precedent already set for ``chem.element_use_effect`` in Wave D).

Slice 3 adds ``ม.5/8`` (covalent bond order and shared electron-pair count),
``ม.5/9`` (polarity of two-atom molecules), and ``ม.5/10`` (hydrogen-bond
capability from a structural formula).

Slice 4 adds ``ม.5/11`` (boiling point vs intermolecular force), ``ม.5/12``
(writing ion and ionic-compound formulas), and ``ม.5/13`` (dissociation and
electrolyte/nonelectrolyte classification).

Slice 5 adds ``ม.5/14`` (saturated/unsaturated hydrocarbons), ``ม.5/15``
(polymer vs monomer physical properties), and ``ม.5/16`` (acid-base from
organic structure).

Slice 7 adds ``ว 2.2 ม.5/2`` (vector quantities and the resultant of coplanar
forces), built to fill the one real gap ``sheet_database/outputs/teaching_plan/ข้อสอบแรง.md`` found.
Its Foundation carries the whole prerequisite tier rather than the rule alone,
because the indicator's own verb — vector addition — has to sit in Fluency for
that stage to be ``exact``.

Slice 8 adds ``ม.5/20`` (the formulas on each side of a chemical equation and
the meaning of its symbols — two free verbs, so both Foundation and Fluency are
exact), ``ม.5/21`` (how concentration, surface area, temperature and a catalyst
change the rate) and ``ม.5/22`` (the same factors put to use at home and in
industry). Every computed answer — an atom count, a balancing coefficient, a
mass by conservation, the fastest run — is re-derived here.

Slice 9 closes ``ว 2.1 ม.5`` with ``ม.5/23`` (redox as giving and taking
electrons), ``ม.5/24`` (the properties of radioactive substances and the
half-life calculation — two free verbs, so both Foundation and Fluency are
exact) and ``ม.5/25`` (uses of radioisotopes and protection from radiation).
Slice 10 adds ``ว 2.2 ม.5/1`` (acceleration read off velocity-time data).

Slices 11 and 12 close ``ว 2.2 ม.5``: ``ม.5/3`` (F = ma), ``ม.5/4`` (action
and reaction), ``ม.5/5`` (acceleration in straight-line, projectile, circular
and oscillating motion — the exact set spans all four), ``ม.5/6`` (gravity and
orbits), ``ม.5/7`` (the field of a current), ``ม.5/8`` and ``ม.5/9`` (two
outcomes each joined by ``รวมทั้ง``, so both Foundation and Fluency are exact)
and ``ม.5/10`` (the strong and weak forces). Magnetic directions are cross
products in the page frame, re-derived here from each stem.

Slices 13 and 14 open ``ว 2.3 ม.5``: ``ม.5/1`` (fission, fusion and E = mc²),
``ม.5/2`` (renewable electricity, and efficiency and cost — two outcomes joined
by ``รวมทั้ง``), ``ม.5/3`` and ``ม.5/5`` (reflection, refraction, diffraction
and superposition, for waves and for sound), ``ม.5/4`` (natural frequency and
resonance), ``ม.5/6`` (intensity against level in decibels, and hearing) and
``ม.5/7`` (echo, beats, the Doppler effect and resonance of sound). Each
multi-object indicator's bank is asserted to reach every object it names.

Slice 15 closes ``ว 2.3 ม.5`` and Wave E's core content: ``ม.5/8`` (uses of
sound), ``ม.5/9`` (seeing colour and colour blindness), ``ม.5/10`` (filters,
mixing light and mixing pigment — computed as set arithmetic on the three
primary lights), ``ม.5/11`` (the electromagnetic wave and devices) and
``ม.5/12`` (communication, and analogue against digital — two free verbs).

Slice 6 adds ``ม.5/17`` (solubility in various solvents), ``ม.5/18``
(thermoplastic vs thermoset structure and use), and ``ม.5/19`` (polymer-
product impact on life and the environment, with mitigation).

What is checked here mirrors Wave D's own gate:

* the filing follows the indicator's grammar;
* each indicator holds all three stages, in its own curriculum unit and topic;
* Wave E is a cohort of its own, disjoint from every earlier wave, and every
  set not yet approved is on the reviewer's worklist;
* the content-correctness sets answer from their own stems, re-derived here.
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate
from otk.core.curriculum_science import (
    BASIC,
    REVIEW_PENDING,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_PLACEMENTS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_C_KEYS,
    SCIENCE_WAVE_D_KEYS,
    SCIENCE_WAVE_E_APPROVED_KEYS,
    SCIENCE_WAVE_E_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.core.registry import REGISTRY
from otk.sets._support.science_wave_a5 import (
    ISOTOPE_POOL,
    TABLE_POOL,
    WRITEABLE,
    block_class,
    metal_class,
    period_of,
)
from otk.sets._support.chemistry import full_name, iupac_group
from otk.sets.chemistry.m5.atomic_model import BOHR, CLOUD, MODEL_ONLY_FACTS, MODEL_SCENARIOS
from otk.sets.chemistry.m5.formula_particle import CATEGORIES, FORMULAS
from otk.sets.chemistry.m5.element_use_hazard import BENEFIT, HAZARD, USE_CATEGORIES, USE_ITEMS
from otk.sets._support.science_wave_a5 import METAL, NONMETAL, REPRESENTATIVE, TRANSITION_BLOCK
from otk.sets.chemistry.m5.periodic_position import (
    POSITIONS_TABLE,
    REPRESENTATIVE_ELEMENTS,
    TRANSITION_ELEMENTS,
)
from otk.sets.chemistry.m5.covalent_bond_order import (
    BOND_ITEMS,
    DOUBLE,
    MULTI_BOND_ITEMS,
    PAIRS_OF,
    SINGLE,
    TRIPLE,
)
from otk.sets.chemistry.m5.hydrogen_bond import CAN_H_BOND, CANNOT_H_BOND, H_BOND_ITEMS
from otk.sets.chemistry.m5.molecule_polarity import NONPOLAR, POLAR, POLARITY_ITEMS
from otk.sets.chemistry.m5.electrolyte_dissociation import (
    DISSOCIATION_ITEMS,
    ELECTROLYTE,
    NONELECTROLYTE,
    _electrolyte_label,
)
from otk.sets.chemistry.m5.boiling_point_force import (
    FORCE_ITEMS,
    FORCE_LABELS,
    FORCE_NAMES,
    HBOND_FORCE,
    NONPOLAR_FORCE,
    POLAR_FORCE,
    RANK,
)
from otk.sets.chemistry.m5.ionic_formula import ION_ITEMS, IONIC_COMPOUNDS
from otk.sets.chemistry.m5.organic_acid_base import ACID, BASE, NEUTRAL, ORGANIC_ITEMS
from otk.sets.chemistry.m5.hydrocarbon_saturation import HYDROCARBON_ITEMS, SATURATED, UNSATURATED
from otk.sets.chemistry.m5.polymer_property import POLYMER_ITEMS, _polymer_label
from otk.sets.chemistry.m5.solubility_solvent import DISSOLVES, DISSOLVE_WHY, SOLUBILITY_ITEMS
from otk.sets.chemistry.m5.polymer_impact import IMPACT, MITIGATION, POLYMER_IMPACT_ITEMS
from otk.sets.chemistry.m5.thermo_polymer import (
    STRUCTURE_LABEL,
    THERMOPLASTIC,
    THERMOSET,
    THERMO_POLYMER_ITEMS,
)
from otk.sets.chemistry.m5.redox_reactions import (
    DISPLACEMENTS,
    HALF_REACTIONS,
    METALS,
    NOT_REDOX_REACTANTS,
    REDOX_REACTANTS,
)
from otk.sets.chemistry.m5.radioisotope_use import FIELDS, PRINCIPLES, PROTECTIONS, RADIO_USES
from otk.sets._support.science_wave_e9 import ISOTOPES
from otk.sets.chemistry.m5.radioactive_decay import RAY_PROPERTIES
from otk.sets.physics.m5.acceleration_vt import record as accel_record
from otk.sets.physics.m5.accelerated_motion import ACCELERATION_OF, MOTION_EXAMPLES, MOTIONS
from otk.sets.physics.m5.newton_third import ACTION_PAIRS
from otk.sets.physics.m5.gravity_orbit import ORBIT_FALSE, ORBIT_TRUE
from otk.sets._support.science_wave_e13 import BEHAVIOURS
from otk.sets.physics.m5.nuclear_energy import NUCLEAR_FALSE, NUCLEAR_TRUE
from otk.sets.physics.m5.resonance import RESONANCE_TRUE
from otk.sets.physics.m5.wave_behaviour import WAVE_EXAMPLES, WAVE_FALSE, WAVE_TRUE
from otk.sets._support.science_wave_e13 import show as show13
from otk.sets.physics.m5.sound_effects import (
    EFFECT_EXAMPLES,
    EFFECT_FALSE,
    EFFECT_TRUE,
    SOUND_EFFECTS,
)
from otk.sets.physics.m5.sound_wave_behaviour import SOUND_EXAMPLES, SOUND_FALSE, SOUND_TRUE
from otk.sets._support.science_wave_e15 import COLOUR_NAME, LIGHT_NAME
from otk.sets.physics.m5.em_comms import SIGNAL_FACTS
from otk.sets.physics.m5.sound_use import SOUND_USES
from otk.sets.physics.m5.sound_use import PRINCIPLES as SOUND_PRINCIPLES
from otk.sets._support.science_wave_e12 import DIRECTION, cross
from otk.sets.physics.m5.induced_emf import EMF_NO, EMF_YES
from otk.sets.physics.m5.nuclear_force import NUCLEAR_PHENOMENA
from otk.sets._support.science_wave_e8 import EQUATIONS, formula_tex, species_tex
from otk.sets.chemistry.m5.rate_use import RATE_USES
from otk.sets.chemistry.m5.chemical_equation import element_counts, molar_mass, side_counts

SEEDS = 300


def _triple(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}_{stage}" for stage in ("foundation", "fluency", "application"))


INDICATORS = {
    "ว 2.1 ม.5/1": _triple("chem.formula_particle"),
    "ว 2.1 ม.5/2": _triple("chem.atomic_model"),
    "ว 2.1 ม.5/4": _triple("chem.nuclide_isotope"),
    "ว 2.1 ม.5/5": _triple("chem.periodic_position"),
    "ว 2.1 ม.5/6": _triple("chem.metal_conductivity"),
    "ว 2.1 ม.5/7": _triple("chem.element_use_hazard"),
    "ว 2.1 ม.5/8": _triple("chem.covalent_bond_order"),
    "ว 2.1 ม.5/9": _triple("chem.molecule_polarity"),
    "ว 2.1 ม.5/10": _triple("chem.hydrogen_bond"),
    "ว 2.1 ม.5/11": _triple("chem.boiling_point_force"),
    "ว 2.1 ม.5/12": _triple("chem.ionic_formula"),
    "ว 2.1 ม.5/13": _triple("chem.electrolyte_dissociation"),
    "ว 2.1 ม.5/14": _triple("chem.hydrocarbon_saturation"),
    "ว 2.1 ม.5/15": _triple("chem.polymer_property"),
    "ว 2.1 ม.5/16": _triple("chem.organic_acid_base"),
    "ว 2.1 ม.5/17": _triple("chem.solubility_solvent"),
    "ว 2.1 ม.5/18": _triple("chem.thermo_polymer"),
    "ว 2.1 ม.5/19": _triple("chem.polymer_impact"),
    "ว 2.2 ม.5/2": _triple("phys.vector_resultant"),
    "ว 2.1 ม.5/20": _triple("chem.chemical_equation"),
    "ว 2.1 ม.5/21": _triple("chem.rate_factor"),
    "ว 2.1 ม.5/22": _triple("chem.rate_use"),
    "ว 2.1 ม.5/23": _triple("chem.redox"),
    "ว 2.1 ม.5/24": _triple("chem.radioactive_decay"),
    "ว 2.1 ม.5/25": _triple("chem.radioisotope_use"),
    "ว 2.2 ม.5/1": _triple("phys.acceleration_vt"),
    "ว 2.2 ม.5/3": _triple("phys.newton_second"),
    "ว 2.2 ม.5/4": _triple("phys.newton_third"),
    "ว 2.2 ม.5/5": _triple("phys.accelerated_motion"),
    "ว 2.2 ม.5/6": _triple("phys.gravity_orbit"),
    "ว 2.2 ม.5/7": _triple("phys.current_field"),
    "ว 2.2 ม.5/8": _triple("phys.magnetic_force"),
    "ว 2.2 ม.5/9": _triple("phys.induced_emf"),
    "ว 2.2 ม.5/10": _triple("phys.nuclear_force"),
    "ว 2.3 ม.5/1": _triple("phys.nuclear_energy"),
    "ว 2.3 ม.5/2": _triple("phys.renewable_energy"),
    "ว 2.3 ม.5/3": _triple("phys.wave_behaviour"),
    "ว 2.3 ม.5/4": _triple("phys.resonance"),
    "ว 2.3 ม.5/5": _triple("phys.sound_wave_behaviour"),
    "ว 2.3 ม.5/6": _triple("phys.sound_intensity"),
    "ว 2.3 ม.5/7": _triple("phys.sound_effects"),
    "ว 2.3 ม.5/8": _triple("phys.sound_use"),
    "ว 2.3 ม.5/9": _triple("phys.colour_vision"),
    "ว 2.3 ม.5/10": _triple("phys.colour_mixing"),
    "ว 2.3 ม.5/11": _triple("phys.em_wave"),
    "ว 2.3 ม.5/12": _triple("phys.em_comms"),
}

TOPICS = {
    "ว 2.1 ม.5/1": "ธาตุ สารประกอบ และอนุภาคจากสูตรเคมี",
    "ว 2.1 ม.5/2": "แบบจำลองอะตอมของโบร์กับแบบจำลองอะตอมแบบกลุ่มหมอก",
    "ว 2.1 ม.5/4": "สัญลักษณ์นิวเคลียร์และไอโซโทป",
    "ว 2.1 ม.5/5": "หมู่ คาบ และการจัดกลุ่มธาตุจากตารางธาตุ",
    "ว 2.1 ม.5/6": "การนำไฟฟ้า การให้และรับอิเล็กตรอนของโลหะกับอโลหะ",
    "ว 2.1 ม.5/7": "ประโยชน์และอันตรายจากธาตุเรพรีเซนเททีฟและธาตุแทรนซิชัน",
    "ว 2.1 ม.5/8": "พันธะเดี่ยว พันธะคู่ พันธะสาม และจำนวนคู่อิเล็กตรอนร่วมพันธะ",
    "ว 2.1 ม.5/9": "สภาพขั้วของโมเลกุลที่ประกอบด้วยสองอะตอม",
    "ว 2.1 ม.5/10": "การเกิดพันธะไฮโดรเจนจากสูตรโครงสร้าง",
    "ว 2.1 ม.5/11": "จุดเดือดของสารโคเวเลนต์กับแรงดึงดูดระหว่างโมเลกุล",
    "ว 2.1 ม.5/12": "สูตรเคมีของไอออนและสารประกอบไอออนิก",
    "ว 2.1 ม.5/13": "การแตกตัวของสารและสารละลายอิเล็กโทรไลต์",
    "ว 2.1 ม.5/14": "ไฮโดรคาร์บอนอิ่มตัวและไม่อิ่มตัวจากสูตรโครงสร้าง",
    "ว 2.1 ม.5/15": "สมบัติทางกายภาพของพอลิเมอร์เทียบกับมอนอเมอร์",
    "ว 2.1 ม.5/16": "สมบัติกรด-เบสจากโครงสร้างของสารประกอบอินทรีย์",
    "ว 2.1 ม.5/17": "สมบัติการละลายในตัวทำละลายชนิดต่าง ๆ",
    "ว 2.1 ม.5/18": "โครงสร้างกับสมบัติเทอร์มอพลาสติกและเทอร์มอเซตของพอลิเมอร์",
    "ว 2.1 ม.5/19": "ผลกระทบของผลิตภัณฑ์พอลิเมอร์ต่อสิ่งมีชีวิตและสิ่งแวดล้อม",
    "ว 2.2 ม.5/2": "ปริมาณเวกเตอร์และการรวมแรงในระนาบเดียวกัน",
    "ว 2.1 ม.5/20": "สูตรเคมีของสารตั้งต้น ผลิตภัณฑ์ และสัญลักษณ์ในสมการเคมี",
    "ว 2.1 ม.5/21": "ผลของความเข้มข้น พื้นที่ผิว อุณหภูมิ และตัวเร่งปฏิกิริยาต่ออัตราการเกิดปฏิกิริยาเคมี",
    "ว 2.1 ม.5/22": "ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมีในชีวิตประจำวันและอุตสาหกรรม",
    "ว 2.1 ม.5/23": "ความหมายของปฏิกิริยารีดอกซ์",
    "ว 2.1 ม.5/24": "สมบัติของสารกัมมันตรังสี ครึ่งชีวิต และปริมาณของสารกัมมันตรังสี",
    "ว 2.1 ม.5/25": "ประโยชน์ของสารกัมมันตรังสีและการป้องกันอันตรายจากกัมมันตภาพรังสี",
    "ว 2.2 ม.5/1": "ความเร่งจากข้อมูลความเร็วกับเวลา",
    "ว 2.2 ม.5/3": "ความสัมพันธ์ระหว่างความเร่ง แรงลัพธ์ และมวล",
    "ว 2.2 ม.5/4": "แรงกิริยาและแรงปฏิกิริยา",
    "ว 2.2 ม.5/5": "ผลของความเร่งต่อการเคลื่อนที่แนวตรง โพรเจกไทล์ วงกลม และการสั่น",
    "ว 2.2 ม.5/6": "แรงโน้มถ่วงกับการเคลื่อนที่ของวัตถุรอบโลก",
    "ว 2.2 ม.5/7": "สนามแม่เหล็กเนื่องจากกระแสไฟฟ้า",
    "ว 2.2 ม.5/8": "แรงแม่เหล็กต่ออนุภาคที่มีประจุ ลวดที่มีกระแส และหลักการทำงานของมอเตอร์",
    "ว 2.2 ม.5/9": "การเกิดอีเอ็มเอฟเหนี่ยวนำและการนำไปใช้ประโยชน์",
    "ว 2.2 ม.5/10": "แรงเข้มและแรงอ่อน",
    "ว 2.3 ม.5/1": "พลังงานนิวเคลียร์ ฟิชชัน ฟิวชัน และความสัมพันธ์ระหว่างมวลกับพลังงาน",
    "ว 2.3 ม.5/2": "การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า ประสิทธิภาพ และความคุ้มค่า",
    "ว 2.3 ม.5/3": "การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่น",
    "ว 2.3 ม.5/4": "ความถี่ธรรมชาติ การสั่นพ้อง และผลของการสั่นพ้อง",
    "ว 2.3 ม.5/5": "การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นของคลื่นเสียง",
    "ว 2.3 ม.5/6": "ความเข้มเสียง ระดับเสียง และผลของความถี่กับระดับเสียงต่อการได้ยิน",
    "ว 2.3 ม.5/7": "เสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้องของเสียง",
    "ว 2.3 ม.5/8": "การนำความรู้เกี่ยวกับเสียงไปใช้ประโยชน์ในชีวิตประจำวัน",
    "ว 2.3 ม.5/9": "การมองเห็นสีของวัตถุและความผิดปกติในการมองเห็นสี",
    "ว 2.3 ม.5/10": "แผ่นกรองแสงสี การผสมแสงสี การผสมสารสี และการนำไปใช้ประโยชน์",
    "ว 2.3 ม.5/11": "คลื่นแม่เหล็กไฟฟ้า ส่วนประกอบ และหลักการทำงานของอุปกรณ์",
    "ว 2.3 ม.5/12": "การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้า และสัญญาณแอนะล็อกกับสัญญาณดิจิทัล",
}

# Two free verbs joined by "และ": both Foundation and Fluency are exact.
# ม.5/8 and ม.5/9 join two outcomes with รวมทั้ง, which files the same way.
TWO_FREE_VERBS = frozenset({"ว 2.1 ม.5/4", "ว 2.1 ม.5/20", "ว 2.1 ม.5/24",
                            "ว 2.2 ม.5/8", "ว 2.2 ม.5/9", "ว 2.3 ม.5/2", "ว 2.3 ม.5/12"})

UNASSESSABLE: frozenset[str] = frozenset()

NEW_KEYS = tuple(key for keys in INDICATORS.values() for key in keys)


def _texts(question) -> list[str]:
    return [" ".join(getattr(block, "text", getattr(block, "tex", "")) for block in choice.content)
            for choice in question.choices]


def _stem(question) -> str:
    return " ".join(getattr(block, "text", getattr(block, "tex", "")) for block in question.stem)


# ── filing ────────────────────────────────────────────────────────────────────

def test_every_new_key_is_registered_and_placed():
    for key in NEW_KEYS:
        assert key in REGISTRY, key
        assert key in SCIENCE_PLACEMENTS, key


def test_wave_e_is_its_own_cohort():
    assert set(NEW_KEYS) == SCIENCE_WAVE_E_KEYS
    for earlier in (SCIENCE_WAVE_KEYS, SCIENCE_WAVE_B_KEYS, SCIENCE_BIOLOGY_CLOSURE_KEYS,
                    SCIENCE_WAVE_C_KEYS, SCIENCE_WAVE_D_KEYS):
        assert not SCIENCE_WAVE_E_KEYS & earlier


def test_approval_is_recorded_for_whole_indicators_inside_wave_e():
    assert SCIENCE_WAVE_E_APPROVED_KEYS <= SCIENCE_WAVE_E_KEYS
    for code, keys in INDICATORS.items():
        assert set(keys) & SCIENCE_WAVE_E_APPROVED_KEYS in (set(), set(keys)), code


def test_every_unapproved_set_is_on_the_review_worklist():
    pending = set().union(*REVIEW_PENDING.values()) if REVIEW_PENDING else set()
    assert SCIENCE_WAVE_E_KEYS - SCIENCE_WAVE_E_APPROVED_KEYS <= pending


def test_each_indicator_holds_three_stages_in_one_unit():
    for code, keys in INDICATORS.items():
        specs = [SCIENCE_PLACEMENTS[key] for key in keys]
        assert {spec.indicator_codes for spec in specs} == {(code,)}, code
        assert len({spec.unit for spec in specs}) == 1, code
        assert len({spec.level for spec in specs}) == 1, code
        assert {spec.course_type for spec in specs} == {BASIC}, code


def test_the_filing_follows_the_indicator_grammar():
    for code, (foundation, fluency, application) in INDICATORS.items():
        status = {key: SCIENCE_PLACEMENTS[key].mapping_status for key in (foundation, fluency, application)}
        if code in UNASSESSABLE:
            assert "exact" not in status.values(), code
            continue
        assert status[fluency] == "exact", code
        assert status[foundation] == ("exact" if code in TWO_FREE_VERBS else "standard_scope"), code
        assert status[application] == "standard_scope", code


@pytest.mark.parametrize("key", NEW_KEYS)
def test_every_set_carries_its_unit_topic(key):
    code = next(one for one, keys in INDICATORS.items() if key in keys)
    assert generate(key, Random(0)).topic == TOPICS[code]
    assert SCIENCE_PLACEMENTS[key].unit == TOPICS[code]


# ── slice 1: ว 2.1 ม.5/1, ม.5/2, ม.5/4 ──────────────────────────────────────

def test_formula_categories_span_every_particle_form_an_element_or_compound_can_take():
    assert (ELEMENT := "ธาตุ") and (COMPOUND := "สารประกอบ")
    ecs = {ec for ec, _ in CATEGORIES}
    assert ecs == {ELEMENT, COMPOUND}
    # A compound cannot be a bare atom: it has more than one kind of atom in it.
    assert ("สารประกอบ", "อะตอม") not in CATEGORIES


def test_every_formula_item_has_a_unique_tex_string():
    texs = [item.tex for item in FORMULAS]
    assert len(texs) == len(set(texs))


def test_formula_particle_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.formula_particle_fluency", Random(seed))
        formula_tex = next(block.tex for block in question.stem if hasattr(block, "tex"))
        item = next(i for i in FORMULAS if i.tex == formula_tex)
        answer = _texts(question)[question.answer]
        assert answer == f"{item.element_or_compound}ที่อยู่ในรูป{item.particle}"


def test_formula_particle_foundation_choices_are_all_one_category():
    for seed in range(SEEDS):
        question = generate("chem.formula_particle_foundation", Random(seed))
        stem = _stem(question)
        target = "ธาตุ" if stem.endswith("ธาตุ") else "สารประกอบ"
        answer_tex = question.choices[question.answer].content[0].tex
        answer_item = next(i for i in FORMULAS if i.tex == answer_tex)
        assert answer_item.element_or_compound == target


def test_formula_particle_application_choices_all_match_the_named_category():
    for seed in range(SEEDS):
        question = generate("chem.formula_particle_application", Random(seed))
        answer_tex = question.choices[question.answer].content[0].tex
        answer_item = next(i for i in FORMULAS if i.tex == answer_tex)
        stem = _stem(question)
        assert stem.endswith(f"{answer_item.element_or_compound}ที่อยู่ในรูป{answer_item.particle}")


def test_atomic_model_facts_each_belong_to_exactly_one_model():
    models = {model for _, model in MODEL_ONLY_FACTS}
    assert models == {BOHR, CLOUD}


def test_atomic_model_foundation_answer_matches_the_fact_bank():
    for seed in range(SEEDS):
        question = generate("chem.atomic_model_foundation", Random(seed))
        stem = _stem(question)
        fact, model = next((f, m) for f, m in MODEL_ONLY_FACTS if f in stem)
        answer = _texts(question)[question.answer]
        assert answer == model


def test_atomic_model_application_scenarios_each_belong_to_exactly_one_model():
    models = {model for _, model in MODEL_SCENARIOS}
    assert models == {BOHR, CLOUD}
    for seed in range(SEEDS):
        question = generate("chem.atomic_model_application", Random(seed))
        stem = _stem(question)
        scenario, model = next((s, m) for s, m in MODEL_SCENARIOS if s in stem)
        answer = _texts(question)[question.answer]
        assert answer == model


def test_nuclide_isotope_foundation_symbol_matches_the_stated_particle_counts():
    for seed in range(SEEDS):
        question = generate("chem.nuclide_isotope_foundation", Random(seed))
        stem = _stem(question)
        el = next(e for e in WRITEABLE if e.th in stem)
        neutrons = el.mass - el.z
        assert f"โปรตอน {el.z} อนุภาค" in stem
        assert f"นิวตรอน {neutrons} อนุภาค" in stem
        answer_tex = question.choices[question.answer].content[-1].tex
        assert f"{{}}^{{{el.mass}}}_{{{el.z}}}\\mathrm{{{el.symbol}}}" == answer_tex


def test_nuclide_isotope_fluency_answer_keeps_the_same_atomic_number():
    for seed in range(SEEDS):
        question = generate("chem.nuclide_isotope_fluency", Random(seed))
        given_tex = next(block.tex for block in question.stem if hasattr(block, "tex"))
        el = next(e for e in ISOTOPE_POOL
                  if given_tex == f"{{}}^{{{e.mass}}}_{{{e.z}}}\\mathrm{{{e.symbol}}}")
        answer_tex = question.choices[question.answer].content[-1].tex
        assert answer_tex == f"{{}}^{{{el.mass + 2}}}_{{{el.z}}}\\mathrm{{{el.symbol}}}"


def test_nuclide_isotope_application_adds_the_stated_neutron_offset():
    for seed in range(SEEDS):
        question = generate("chem.nuclide_isotope_application", Random(seed))
        stem = _stem(question)
        el = next(e for e in WRITEABLE if e.th in stem)
        offset = next(n for n in (2, 4, 6) if f"อยู่ {n} อนุภาค" in stem)
        answer_tex = question.choices[question.answer].content[-1].tex
        assert f"{{}}^{{{el.mass + offset}}}_{{{el.z}}}\\mathrm{{{el.symbol}}}" == answer_tex


# ── slice 2: ว 2.1 ม.5/5, ม.5/6, ม.5/7 ──────────────────────────────────────

def test_periodic_position_foundation_answer_matches_the_elements_position():
    for seed in range(SEEDS):
        question = generate("chem.periodic_position_foundation", Random(seed))
        stem = _stem(question)
        el = next(e for e in TABLE_POOL if full_name(e) in stem)
        group, period = iupac_group(el), period_of(el)
        answer = _texts(question)[question.answer]
        assert answer == f"หมู่ {group} คาบ {period}"


def test_periodic_position_fluency_answer_matches_the_positions_table():
    for seed in range(SEEDS):
        question = generate("chem.periodic_position_fluency", Random(seed))
        stem = _stem(question)
        group = int(stem.split("หมู่ ")[1].split(" ")[0])
        period = int(stem.split("คาบ ")[1].split(" ")[0])
        el = POSITIONS_TABLE[(group, period)]
        kind, block = metal_class(el), block_class(el)
        answer = _texts(question)[question.answer]
        assert answer == f"{full_name(el)} จัดเป็น{kind} และอยู่ในกลุ่ม{block}"


def test_periodic_position_application_trio_all_shares_the_named_block():
    for seed in range(SEEDS):
        question = generate("chem.periodic_position_application", Random(seed))
        stem = _stem(question)
        block = TRANSITION_BLOCK if TRANSITION_BLOCK in stem else REPRESENTATIVE
        pool = TRANSITION_ELEMENTS if block == TRANSITION_BLOCK else REPRESENTATIVE_ELEMENTS
        symbols_by_pool = {el.symbol for el in pool}
        answer = _texts(question)[question.answer]
        symbols = answer.split(" และ ")
        assert len(symbols) == 3
        assert set(symbols) <= symbols_by_pool


def test_metal_conductivity_fluency_pairs_conductivity_with_electron_tendency():
    for seed in range(SEEDS):
        question = generate("chem.metal_conductivity_fluency", Random(seed))
        stem = _stem(question)
        kind = METAL if f"กลุ่ม{METAL}" in stem else NONMETAL
        answer = _texts(question)[question.answer]
        if kind == METAL:
            assert "นำไฟฟ้าได้ดี" in answer and "ให้อิเล็กตรอน" in answer
        else:
            assert "นำไฟฟ้าได้ไม่ดี" in answer and "รับอิเล็กตรอน" in answer


def test_metal_conductivity_application_matches_the_named_elements_class():
    for seed in range(SEEDS):
        question = generate("chem.metal_conductivity_application", Random(seed))
        stem = _stem(question)
        el = next(e for e in TABLE_POOL if full_name(e) in stem)
        kind = metal_class(el)
        answer = _texts(question)[question.answer]
        if kind == METAL:
            assert "นำไฟฟ้าได้ดี" in answer and "ให้อิเล็กตรอน" in answer
        else:
            assert "นำไฟฟ้าได้ไม่ดี" in answer and "รับอิเล็กตรอน" in answer


def test_use_items_span_every_block_and_kind_combination():
    assert set(USE_CATEGORIES) == {
        (REPRESENTATIVE, BENEFIT), (REPRESENTATIVE, HAZARD),
        (TRANSITION_BLOCK, BENEFIT), (TRANSITION_BLOCK, HAZARD),
    }


def test_element_use_hazard_foundation_answer_matches_the_items_block():
    for seed in range(SEEDS):
        question = generate("chem.element_use_hazard_foundation", Random(seed))
        stem = _stem(question)
        item = next(i for i in USE_ITEMS if i.text in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.block


def test_element_use_hazard_fluency_answer_matches_the_items_full_category():
    for seed in range(SEEDS):
        question = generate("chem.element_use_hazard_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in USE_ITEMS if i.text in stem)
        answer = _texts(question)[question.answer]
        assert answer == f"{item.kind}จาก{item.block}"


def test_element_use_hazard_application_choices_all_match_the_named_category():
    for seed in range(SEEDS):
        question = generate("chem.element_use_hazard_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in USE_ITEMS if i.text == answer)
        assert stem.endswith(f"{answer_item.kind}จาก{answer_item.block}")


# ── slice 3: ว 2.1 ม.5/8, ม.5/9, ม.5/10 ─────────────────────────────────────

def test_covalent_bond_order_foundation_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.covalent_bond_order_foundation", Random(seed))
        stem = _stem(question)
        item = next(i for i in BOND_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.bond_type


def test_covalent_bond_order_fluency_answer_matches_bond_type_and_pair_count():
    for seed in range(SEEDS):
        question = generate("chem.covalent_bond_order_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in BOND_ITEMS if i.name in stem)
        pairs = PAIRS_OF[item.bond_type]
        answer = _texts(question)[question.answer]
        assert answer == f"{item.bond_type} มีอิเล็กตรอนร่วมกัน {pairs} คู่"


def test_covalent_bond_order_application_counts_every_bond_in_the_molecule():
    for seed in range(SEEDS):
        question = generate("chem.covalent_bond_order_application", Random(seed))
        stem = _stem(question)
        name, count, bond_type = next(i for i in MULTI_BOND_ITEMS if i[0] in stem)
        answer = _texts(question)[question.answer]
        assert answer == f"มีพันธะโคเวเลนต์ทั้งหมด {count} พันธะ และเป็น{bond_type}ทุกพันธะ"


def test_bond_items_cover_all_three_bond_orders():
    assert {item.bond_type for item in BOND_ITEMS} == {SINGLE, DOUBLE, TRIPLE}


def test_molecule_polarity_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.molecule_polarity_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in POLARITY_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.polarity


def test_molecule_polarity_application_choices_all_match_the_named_polarity():
    for seed in range(SEEDS):
        question = generate("chem.molecule_polarity_application", Random(seed))
        stem = _stem(question)
        polarity = NONPOLAR if stem.endswith(NONPOLAR) else POLAR
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in POLARITY_ITEMS if i.name.endswith(f"({answer})"))
        assert answer_item.polarity == polarity


def test_polarity_items_cover_both_polarities():
    assert {item.polarity for item in POLARITY_ITEMS} == {POLAR, NONPOLAR}


def test_hydrogen_bond_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.hydrogen_bond_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in H_BOND_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.can_bond


def test_hydrogen_bond_application_choices_all_match_the_named_capability():
    for seed in range(SEEDS):
        question = generate("chem.hydrogen_bond_application", Random(seed))
        stem = _stem(question)
        capability = CAN_H_BOND if stem.endswith(CAN_H_BOND) else CANNOT_H_BOND
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in H_BOND_ITEMS if i.name == answer)
        assert answer_item.can_bond == capability


def test_h_bond_items_cover_both_capabilities():
    assert {item.can_bond for item in H_BOND_ITEMS} == {CAN_H_BOND, CANNOT_H_BOND}


# ── slice 4: ว 2.1 ม.5/11, ม.5/12, ม.5/13 ────────────────────────────────────

def test_force_rank_orders_hydrogen_bond_above_polar_above_nonpolar():
    assert RANK[HBOND_FORCE] > RANK[POLAR_FORCE] > RANK[NONPOLAR_FORCE]


def test_boiling_point_force_foundation_answer_is_the_higher_ranked_substance():
    for seed in range(SEEDS):
        question = generate("chem.boiling_point_force_foundation", Random(seed))
        stem = _stem(question)
        named = [item for item in FORCE_ITEMS if item.name in stem]
        higher = max(named, key=lambda item: RANK[item.force])
        answer = _texts(question)[question.answer]
        assert answer == higher.name


def test_boiling_point_force_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.boiling_point_force_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in FORCE_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == FORCE_LABELS[item.force]


def test_boiling_point_force_application_choices_all_match_the_named_force():
    for seed in range(SEEDS):
        question = generate("chem.boiling_point_force_application", Random(seed))
        stem = _stem(question)
        asked = next(f for f in (NONPOLAR_FORCE, POLAR_FORCE, HBOND_FORCE)
                     if stem.endswith(FORCE_NAMES[f]))
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in FORCE_ITEMS if i.name == answer)
        assert answer_item.force == asked


def test_ion_items_have_unique_names_and_formulas():
    names = [item.name for item in ION_ITEMS]
    texs = [item.tex for item in ION_ITEMS]
    assert len(names) == len(set(names))
    assert len(texs) == len(set(texs))


def test_ionic_formula_foundation_answer_matches_the_named_ion():
    for seed in range(SEEDS):
        question = generate("chem.ionic_formula_foundation", Random(seed))
        stem = _stem(question)
        item = next(i for i in ION_ITEMS if i.name in stem)
        answer_tex = question.choices[question.answer].content[0].tex
        assert answer_tex == item.tex


def test_ionic_formula_fluency_answer_matches_the_named_ion_pair():
    for seed in range(SEEDS):
        question = generate("chem.ionic_formula_fluency", Random(seed))
        stem = _stem(question)
        compound = next(c for c in IONIC_COMPOUNDS
                        if c.cation_name in stem and c.anion_name in stem)
        answer_tex = question.choices[question.answer].content[0].tex
        assert answer_tex == compound.tex


def test_ionic_formula_application_answer_matches_the_named_compound():
    for seed in range(SEEDS):
        question = generate("chem.ionic_formula_application", Random(seed))
        stem = _stem(question)
        compound = next(c for c in IONIC_COMPOUNDS if c.compound_name in stem)
        answer_tex = question.choices[question.answer].content[0].tex
        assert answer_tex == compound.tex


def test_ionic_compounds_have_unique_names_and_formulas():
    names = [c.compound_name for c in IONIC_COMPOUNDS]
    texs = [c.tex for c in IONIC_COMPOUNDS]
    assert len(names) == len(set(names))
    assert len(texs) == len(set(texs))


def test_dissociation_items_cover_both_electrolyte_classes():
    assert {item.dissociates for item in DISSOCIATION_ITEMS} == {True, False}


def test_electrolyte_dissociation_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.electrolyte_dissociation_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in DISSOCIATION_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == _electrolyte_label(item.dissociates)


def test_electrolyte_dissociation_application_choices_all_match_the_named_class():
    for seed in range(SEEDS):
        question = generate("chem.electrolyte_dissociation_application", Random(seed))
        stem = _stem(question)
        result = ELECTROLYTE if stem.endswith(ELECTROLYTE) and not stem.endswith(NONELECTROLYTE) else NONELECTROLYTE
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in DISSOCIATION_ITEMS if i.name == answer)
        assert answer_item.dissociates == (result == ELECTROLYTE)


# ── slice 5: ว 2.1 ม.5/14, ม.5/15, ม.5/16 ────────────────────────────────────

def test_hydrocarbon_items_cover_both_saturation_states():
    assert {item.saturated for item in HYDROCARBON_ITEMS} == {True, False}


def test_hydrocarbon_saturation_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.hydrocarbon_saturation_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in HYDROCARBON_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == (SATURATED if item.saturated else UNSATURATED)


def test_hydrocarbon_saturation_application_choices_all_match_the_named_kind():
    for seed in range(SEEDS):
        question = generate("chem.hydrocarbon_saturation_application", Random(seed))
        stem = _stem(question)
        kind = UNSATURATED if stem.endswith(UNSATURATED) else SATURATED
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in HYDROCARBON_ITEMS if i.name == answer)
        assert answer_item.saturated == (kind == SATURATED)


def test_polymer_items_have_unique_polymer_and_monomer_names():
    polymers = [item.polymer_name for item in POLYMER_ITEMS]
    monomers = [item.monomer_name for item in POLYMER_ITEMS]
    assert len(polymers) == len(set(polymers))
    assert len(monomers) == len(set(monomers))


def test_polymer_property_fluency_answer_is_the_higher_molecular_mass_label():
    for seed in range(SEEDS):
        question = generate("chem.polymer_property_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        assert answer == _polymer_label("สูงกว่า")


def test_polymer_property_application_answer_is_the_named_polymers_own_monomer():
    for seed in range(SEEDS):
        question = generate("chem.polymer_property_application", Random(seed))
        stem = _stem(question)
        item = next(i for i in POLYMER_ITEMS if i.polymer_name in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.monomer_name


def test_organic_items_cover_acid_base_and_neutral():
    assert {item.property for item in ORGANIC_ITEMS} == {ACID, BASE, NEUTRAL}


def test_organic_acid_base_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.organic_acid_base_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in ORGANIC_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.property


def test_organic_acid_base_application_choices_all_match_the_named_property():
    for seed in range(SEEDS):
        question = generate("chem.organic_acid_base_application", Random(seed))
        stem = _stem(question)
        property_ = next(p for p in (ACID, BASE, NEUTRAL) if stem.endswith(p))
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in ORGANIC_ITEMS if i.name == answer)
        assert answer_item.property == property_


# ── slice 6: ว 2.1 ม.5/17, ม.5/18, ม.5/19 ────────────────────────────────────

def test_solubility_items_cover_both_outcomes():
    assert {item.dissolves for item in SOLUBILITY_ITEMS} == {True, False}


def test_solubility_solvent_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.solubility_solvent_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in SOLUBILITY_ITEMS if i.pair_name in stem)
        answer = _texts(question)[question.answer]
        assert answer == DISSOLVE_WHY[item.dissolves]


def test_solubility_solvent_application_choices_all_match_the_named_outcome():
    for seed in range(SEEDS):
        question = generate("chem.solubility_solvent_application", Random(seed))
        stem = _stem(question)
        dissolves = stem.endswith(f"{DISSOLVES}เมื่อผสมกัน")
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in SOLUBILITY_ITEMS if i.pair_name == answer)
        assert answer_item.dissolves == dissolves


def test_thermo_polymer_items_cover_both_kinds():
    assert {item.kind for item in THERMO_POLYMER_ITEMS} == {THERMOPLASTIC, THERMOSET}


def test_thermo_polymer_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.thermo_polymer_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in THERMO_POLYMER_ITEMS if i.name in stem)
        answer = _texts(question)[question.answer]
        assert answer == f"{item.kind} เพราะ{STRUCTURE_LABEL[item.kind]}"


def test_thermo_polymer_application_choices_all_match_the_named_kind():
    for seed in range(SEEDS):
        question = generate("chem.thermo_polymer_application", Random(seed))
        stem = _stem(question)
        kind = next(k for k in (THERMOPLASTIC, THERMOSET) if stem.endswith(k))
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in THERMO_POLYMER_ITEMS if i.name == answer)
        assert answer_item.kind == kind


def test_polymer_impact_items_cover_both_categories():
    assert {item.kind for item in POLYMER_IMPACT_ITEMS} == {IMPACT, MITIGATION}


def test_polymer_impact_fluency_answer_matches_the_bank():
    for seed in range(SEEDS):
        question = generate("chem.polymer_impact_fluency", Random(seed))
        stem = _stem(question)
        item = next(i for i in POLYMER_IMPACT_ITEMS if i.text in stem)
        answer = _texts(question)[question.answer]
        assert answer == item.kind


def test_polymer_impact_application_choices_all_match_the_named_category():
    for seed in range(SEEDS):
        question = generate("chem.polymer_impact_application", Random(seed))
        stem = _stem(question)
        kind = next(k for k in (IMPACT, MITIGATION) if f"ตัวอย่างของ{k}" in stem)
        answer = _texts(question)[question.answer]
        answer_item = next(i for i in POLYMER_IMPACT_ITEMS if i.text == answer)
        assert answer_item.kind == kind


# ── slice 8: ว 2.1 ม.5/20, ม.5/21, ม.5/22 ───────────────────────────────────

def _maths(blocks) -> list[str]:
    return [block.tex for block in blocks if getattr(block, "kind", "") == "math"]


def _bank_equation(tex: str):
    """The bank equation a TeX string shows, matched on every formula it holds."""
    for eq in EQUATIONS:
        species = (*eq.reactants, *eq.products)
        if all(formula_tex(s.formula) in tex for s in species) \
                and tex.count("+") == len(species) - 2:
            return eq
    raise AssertionError(tex)


def _stem_equation(question):
    return _bank_equation(next(tex for tex in _maths(question.stem) if "rightarrow" in tex))


def test_every_equation_in_the_bank_is_balanced():
    for eq in EQUATIONS:
        assert side_counts(eq.reactants) == side_counts(eq.products), eq.thai


def test_the_formula_parser_adds_up_repeated_symbols():
    assert element_counts("C2H5OH") == {"C": 2, "H": 6, "O": 1}
    assert element_counts("Na2SO4") == {"Na": 2, "S": 1, "O": 4}


def test_every_equation_is_distinct_and_described_in_words():
    assert len({eq.thai for eq in EQUATIONS}) == len(EQUATIONS)
    assert len({(eq.reactants, eq.products) for eq in EQUATIONS}) == len(EQUATIONS)


def test_chemical_equation_fluency_atom_counts_match_the_equation():
    for seed in range(SEEDS):
        question = generate("chem.chemical_equation_fluency", Random(seed))
        stem = _stem(question)
        match = re.search(r"ทางด้าน(สารตั้งต้น|ผลิตภัณฑ์)มีอะตอมของธาตุ (\w+) ", stem)
        if not match:
            continue
        eq = _stem_equation(question)
        side = eq.reactants if match.group(1) == "สารตั้งต้น" else eq.products
        answer = _texts(question)[question.answer]
        assert answer == f"{side_counts(side)[match.group(2)]} อะตอม", (seed, stem)


def test_chemical_equation_application_blank_is_the_one_coefficient_that_balances():
    for seed in range(SEEDS):
        question = generate("chem.chemical_equation_application", Random(seed))
        shown = [tex for tex in _maths(question.stem) if r"\square" in tex]
        if not shown:
            continue
        eq = _bank_equation(shown[0])
        blank = next(s for s in (*eq.reactants, *eq.products)
                     if species_tex(s, coef=r"\square\,") in shown[0])
        balancing = []
        for n in range(1, 10):
            def trial(side, n=n):
                return tuple(s._replace(coef=n) if s == blank else s for s in side)
            if side_counts(trial(eq.reactants)) == side_counts(trial(eq.products)):
                balancing.append(n)
        assert balancing == [blank.coef], (seed, shown[0])
        assert _texts(question)[question.answer] == str(blank.coef)


def test_chemical_equation_application_mass_follows_conservation():
    for seed in range(SEEDS):
        question = generate("chem.chemical_equation_application", Random(seed))
        stem = _stem(question)
        if "กี่กรัม" not in stem:
            continue
        masses = [Fraction(m) for m in re.findall(r"([\d.]+) กรัม", stem)]
        eq = _stem_equation(question)
        given_in = masses[:len(eq.reactants)]
        given_out = masses[len(eq.reactants):]
        answer = Fraction(_texts(question)[question.answer].split()[0])
        assert answer == sum(given_in) - sum(given_out), (seed, stem)
        # The masses really are in the equation's mole ratio.
        ratio = {m / (s.coef * molar_mass(s.formula)) for m, s in zip(given_in, eq.reactants)}
        assert len(ratio) == 1, (seed, stem)


def test_chemical_equation_application_words_pick_the_bank_equation():
    for seed in range(SEEDS):
        question = generate("chem.chemical_equation_application", Random(seed))
        stem = _stem(question)
        if "เขียนเป็นสมการเคมี" not in stem:
            continue
        eq = next(e for e in EQUATIONS if stem.startswith(e.thai))
        correct = question.choices[question.answer].content[0].tex
        assert _bank_equation(correct) == eq
        assert all(species_tex(s) in correct for s in (*eq.reactants, *eq.products)), seed


def test_rate_factor_application_fastest_run_has_the_shortest_time():
    for seed in range(SEEDS):
        question = generate("chem.rate_factor_application", Random(seed))
        stem = _stem(question)
        if not stem.endswith("ชุดใดเกิดปฏิกิริยาเร็วที่สุด"):
            continue
        times = [int(t) for t in re.findall(r"ใช้เวลา (\d+) วินาที", stem)]
        assert _texts(question)[question.answer] == f"ชุดที่ {times.index(min(times)) + 1}"


def test_rate_factor_application_runs_speed_up_as_the_factor_rises():
    for seed in range(SEEDS):
        question = generate("chem.rate_factor_application", Random(seed))
        runs = re.findall(r"([\d.]+) (?:mol/dm³|°C) ใช้เวลา (\d+) วินาที", _stem(question))
        if runs:
            ordered = sorted((float(v), int(t)) for v, t in runs)
            assert [t for _, t in ordered] == sorted((t for _, t in ordered), reverse=True)


def test_rate_factor_application_average_rate_is_volume_over_time():
    for seed in range(SEEDS):
        question = generate("chem.rate_factor_application", Random(seed))
        match = re.search(r"ได้ (\d+) cm³ ในเวลา (\d+) วินาที", _stem(question))
        if match:
            volume, seconds = map(int, match.groups())
            answer = float(_texts(question)[question.answer].split()[0])
            assert answer == volume / seconds, (seed, _stem(question))


def test_rate_use_items_are_unique_and_every_factor_is_used():
    assert len({use.situation for use in RATE_USES}) == len(RATE_USES)
    assert {use.factor for use in RATE_USES} == {"ความเข้มข้น", "พื้นที่ผิว", "อุณหภูมิ", "ตัวเร่งปฏิกิริยา"}


def test_rate_use_foundation_answer_is_the_situations_factor():
    for seed in range(SEEDS):
        question = generate("chem.rate_use_foundation", Random(seed))
        stem = _stem(question)
        if "ใช้ปัจจัยใด" not in stem:
            continue
        use = next(u for u in RATE_USES if f'"{u.situation}"' in stem)
        assert _texts(question)[question.answer] == use.factor


def test_rate_use_application_answer_alone_shares_factor_and_direction():
    by_text = {u.situation: u for u in RATE_USES}
    for seed in range(SEEDS):
        question = generate("chem.rate_use_application", Random(seed))
        stem = _stem(question)
        use = next(u for u in RATE_USES if stem.startswith(f'"{u.situation}"'))
        for i, choice in enumerate(_texts(question)):
            other = by_text[choice]
            same = (other.factor, other.faster) == (use.factor, use.faster)
            assert same == (i == question.answer), (seed, choice)


# ── slice 9: ว 2.1 ม.5/23, ม.5/24, ม.5/25 ───────────────────────────────────

def test_every_half_reaction_moves_electrons_the_way_it_is_labelled():
    for half in HALF_REACTIONS:
        left, right = half.tex.split(r"\longrightarrow")
        electrons_on_right = "e^{-}" in right
        assert electrons_on_right == (half.kind == "ปฏิกิริยาออกซิเดชัน"), half.tex


def test_every_displacement_goes_from_the_readier_giver_and_is_balanced():
    for r in DISPLACEMENTS:
        left, right = r.tex.split(r"\longrightarrow")
        assert r.giver in left and r.taker in left
        assert r.giver_after in right and r.taker_after in right
    # Metals are listed readiest first, so only downhill pairs are built.
    metal_pairs = [r for r in DISPLACEMENTS if r.giver.startswith(r"\mathrm{") and "^" not in r.giver]
    order = [m.symbol for m in METALS]
    for r in metal_pairs:
        giver = r.giver[len(r"\mathrm{"):-1]
        taker = r.taker.split("}")[0][len(r"\mathrm{"):]
        assert order.index(giver) < order.index(taker), r.tex


def test_displacement_electron_counts_balance_charge():
    for metal in METALS:
        for other in METALS[METALS.index(metal) + 1:]:
            r = next(d for d in DISPLACEMENTS
                     if d.giver == rf"\mathrm{{{metal.symbol}}}"
                     and d.taker.startswith(rf"\mathrm{{{other.symbol}}}"))
            assert r.electrons % metal.charge == 0 and r.electrons % other.charge == 0


def test_redox_fluency_answer_is_the_giver_or_the_taker():
    for seed in range(SEEDS):
        question = generate("chem.redox_fluency", Random(seed))
        stem = _stem(question)
        tex = _maths(question.stem)[0]
        r = next(d for d in DISPLACEMENTS if d.tex == tex)
        if "สารใดให้อิเล็กตรอน" in stem:
            assert question.choices[question.answer].content[0].tex == r.giver
        elif "สารใดรับอิเล็กตรอน" in stem:
            assert question.choices[question.answer].content[0].tex == r.taker


def test_redox_application_lists_keep_redox_and_non_redox_apart():
    assert not REDOX_REACTANTS & NOT_REDOX_REACTANTS
    bank = {tuple(s.formula for s in e.reactants) for e in EQUATIONS}
    assert REDOX_REACTANTS <= bank and NOT_REDOX_REACTANTS <= bank


def test_redox_application_prediction_follows_the_stated_order():
    for seed in range(SEEDS):
        question = generate("chem.redox_application", Random(seed))
        stem = _stem(question)
        match = re.search(r"ของโลหะ: ([A-Za-z >]+) เมื่อจุ่มแผ่น(\S+?)ลงใน(\S+) ", stem)
        if not match:
            continue
        order = match.group(1).split(" > ")
        dipped = next(m for m in METALS if m.thai == match.group(2))
        solution = next(m for m in METALS if m.salt == match.group(3))
        answer = _texts(question)[question.answer]
        goes = order.index(dipped.symbol) < order.index(solution.symbol)
        assert answer.startswith("เกิดปฏิกิริยา" if goes else "ไม่เกิดปฏิกิริยา"), (seed, stem, answer)


def test_redox_application_electron_count_matches_the_equation():
    for seed in range(SEEDS):
        question = generate("chem.redox_application", Random(seed))
        if "ถ่ายโอนอิเล็กตรอนทั้งหมด" not in _stem(question):
            continue
        r = next(d for d in DISPLACEMENTS if d.tex == _maths(question.stem)[0])
        assert _texts(question)[question.answer] == f"{r.electrons} อิเล็กตรอน"


def test_ray_properties_cover_each_ray_three_times():
    counts = {ray: 0 for ray in ("รังสีแอลฟา", "รังสีบีตา", "รังสีแกมมา")}
    for _, ray in RAY_PROPERTIES:
        counts[ray] += 1
    assert set(counts.values()) == {3}


def _number(text_: str) -> Fraction:
    return Fraction(text_.split()[0].replace(",", ""))


def test_radioactive_decay_fluency_answers_follow_halving():
    for seed in range(SEEDS):
        question = generate("chem.radioactive_decay_fluency", Random(seed))
        stem = _stem(question)
        answer = _number(_texts(question)[question.answer])
        nums = [Fraction(x.replace(",", "")) for x in re.findall(r"(\d[\d,]*(?:\.\d+)?) (?:กรัม|มิลลิกรัม|ไมโครกรัม|วัน|ชั่วโมง|ปี)", stem)]
        if "จะเหลือ" in stem and "กี่" in stem:
            half, start, elapsed = nums
            assert answer == start / 2 ** int(elapsed / half), (seed, stem)
        elif "ต้องใช้เวลานานเท่าใด" in stem:
            half, start, left = nums
            n = (start / left).numerator.bit_length() - 1
            assert start / left == 2 ** n and answer == half * n, (seed, stem)
        elif "มีครึ่งชีวิตเท่าใด" in stem:
            start, left, elapsed = nums
            n = (start / left).numerator.bit_length() - 1
            assert answer == elapsed / n, (seed, stem)
        elif "สลายตัวไปแล้ว" in stem:
            half, start, elapsed = nums
            assert answer == start - start / 2 ** int(elapsed / half), (seed, stem)


def test_radioactive_decay_application_dating_and_storage_times():
    words = {"ครึ่งหนึ่ง": 1, "หนึ่งในสี่": 2, "หนึ่งในแปด": 3, "หนึ่งในสิบหก": 4, "หนึ่งในสามสิบสอง": 5}
    for seed in range(SEEDS):
        question = generate("chem.radioactive_decay_application", Random(seed))
        stem = _stem(question)
        if "คาร์บอน-14 เหลืออยู่" in stem:
            answer = _number(_texts(question)[question.answer])
            n = next(v for w, v in sorted(words.items(), key=lambda kv: -len(kv[0])) if f"เหลืออยู่{w}" in stem)
            assert answer == 5730 * n, (seed, stem)
        elif "ต้องเก็บไว้อย่างน้อย" in stem:
            answer = _number(_texts(question)[question.answer])
            half = Fraction(re.search(r"ครึ่งชีวิต ([\d.,]+)", stem).group(1).replace(",", ""))
            target = int(re.search(r"เหลือ 1/(\d+)", stem).group(1))
            assert answer == half * (target.bit_length() - 1), (seed, stem)


def test_radioactive_decay_application_longer_half_life_keeps_more():
    for seed in range(SEEDS):
        question = generate("chem.radioactive_decay_application", Random(seed))
        stem = _stem(question)
        if "อย่างละ 100 กรัม" not in stem:
            continue
        named = [iso for iso in ISOTOPES if f"{iso.name} (ครึ่งชีวิต" in stem]
        assert len(named) == 2, stem
        longer = max(named, key=lambda iso: iso.half_life).name
        assert _texts(question)[question.answer].startswith(f"{longer}เหลืออยู่มากกว่า"), (seed, stem)


def test_radioisotope_use_banks_are_unique_and_cover_every_field_and_principle():
    assert len({use for use, _ in RADIO_USES}) == len(RADIO_USES)
    assert {field for _, field in RADIO_USES} == set(FIELDS)
    assert len({step for step, _ in PROTECTIONS}) == len(PROTECTIONS)
    assert {p for _, p in PROTECTIONS} == set(PRINCIPLES)


def test_radioisotope_use_fluency_answer_alone_fits_the_named_field_or_principle():
    by_use = dict(RADIO_USES)
    by_step = dict(PROTECTIONS)
    for seed in range(SEEDS):
        question = generate("chem.radioisotope_use_fluency", Random(seed))
        stem = _stem(question)
        for i, choice in enumerate(_texts(question)):
            if choice in by_use:
                fits = stem.endswith(f"ด้าน{by_use[choice]}")
            else:
                fits = f'"{by_step[choice]}"' in stem
            assert fits == (i == question.answer), (seed, choice)


# ── slice 10: ว 2.2 ม.5/1 ────────────────────────────────────────────────────

def _records(stem: str) -> list[tuple[int, int]]:
    return [(int(t), int(v)) for t, v in re.findall(r"t = (\d+) s ความเร็ว (-?\d+) m/s", stem)]


def test_acceleration_records_are_uniform_and_never_reverse():
    for seed in range(SEEDS):
        times, velocities, a = accel_record(Random(seed))
        steps = {(v2 - v1) / (t2 - t1) for (t1, v1), (t2, v2)
                 in zip(zip(times, velocities), zip(times[1:], velocities[1:]))}
        assert steps == {a}
        assert min(velocities) >= 0


def test_acceleration_fluency_answer_is_change_in_velocity_over_time():
    for seed in range(SEEDS):
        question = generate("phys.acceleration_vt_fluency", Random(seed))
        stem = _stem(question)
        points = _records(stem) or [
            (int(t), int(v)) for t, v in re.findall(r"เวลา (\d+) s มีความเร็ว (\d+) m/s", stem)]
        (t1, v1), (t2, v2) = points[0], points[-1]
        answer = float(_texts(question)[question.answer].split()[0])
        assert answer == (v2 - v1) / (t2 - t1), (seed, stem)


def test_acceleration_application_answers_match_the_record():
    for seed in range(SEEDS):
        question = generate("phys.acceleration_vt_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        match = re.search(r"มีความเร็ว (\d+) m/s แล้ว(เร่ง|ลดความเร็ว)ด้วยความเร่งขนาด (\d+) m/s² คงตัวเป็นเวลา (\d+) วินาที", stem)
        if match:
            u, verb, a, t = int(match.group(1)), match.group(2), int(match.group(3)), int(match.group(4))
            assert answer == f"{u + (a if verb == 'เร่ง' else -a) * t} m/s", (seed, stem)
            continue
        points = _records(stem)
        accels = [(v2 - v1) / (t2 - t1) for (t1, v1), (t2, v2) in zip(points, points[1:])]
        spans = [f"ช่วง {t1}–{t2} s" for (t1, _), (t2, _) in zip(points, points[1:])]
        if "ช่วงใดที่ความเร่ง" in stem:
            want = {"เป็นศูนย์": lambda a: a == 0, "มีค่าเป็นลบ": lambda a: a < 0,
                    "มีค่าเป็นบวก": lambda a: a > 0}
            test = next(f for k, f in want.items() if stem.endswith(k))
            assert [s for s, a in zip(spans, accels) if test(a)] == [answer], (seed, stem)
        elif stem.endswith("(ให้ทิศการเคลื่อนที่เป็นบวก)"):
            span = re.search(r"ความเร่งใน(ช่วง \d+–\d+ s)", stem).group(1)
            assert float(answer.split()[0]) == accels[spans.index(span)], (seed, stem)
        else:
            first, last = abs(accels[0]), abs(accels[-1])
            assert first != last
            assert ("ช่วงเร่ง" if first > last else "ช่วงเบรก") in answer.split("มากกว่า")[0], (seed, stem)


# ── slice 11: ว 2.2 ม.5/3, ม.5/4, ม.5/5, ม.5/6 ──────────────────────────────

def _nums(stem: str) -> list[Fraction]:
    return [Fraction(x.replace(",", "")) for x in re.findall(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)", stem)]


def _value(question) -> Fraction:
    return Fraction(_texts(question)[question.answer].split()[0].replace(",", ""))


def test_newton_second_fluency_solves_f_equals_ma():
    for seed in range(SEEDS):
        question = generate("phys.newton_second_fluency", Random(seed))
        stem = _stem(question)
        answer = _value(question)
        if stem.endswith("วัตถุมีความเร่งเท่าใด"):
            f, m = _nums(stem)
            assert answer == f / m, (seed, stem)
        elif stem.startswith("ต้องใช้แรงลัพธ์เท่าใด"):
            m, a = _nums(stem)
            assert answer == m * a, (seed, stem)
        else:
            f, a = _nums(stem)
            assert answer == f / a, (seed, stem)


def test_newton_second_application_nets_the_forces_first():
    for seed in range(SEEDS):
        question = generate("phys.newton_second_application", Random(seed))
        stem = _stem(question)
        if "แรงเสียดทาน" in stem:
            push, m, friction = _nums(stem)
            assert _value(question) == (push - friction) / m, (seed, stem)
        elif stem.startswith("รถยนต์มวล"):
            m, v0, v, t = _nums(stem)
            assert _value(question) == m * (v - v0) / t, (seed, stem)


def test_newton_third_fluency_answer_is_the_bank_reaction():
    for seed in range(SEEDS):
        question = generate("phys.newton_third_fluency", Random(seed))
        pair = next(p for p in ACTION_PAIRS if f'"{p.action}"' in _stem(question))
        assert _texts(question)[question.answer] == pair.reaction


def test_newton_third_application_each_body_gets_force_over_its_own_mass():
    for seed in range(SEEDS):
        question = generate("phys.newton_third_application", Random(seed))
        stem = _stem(question)
        match = re.search(r"^(\S+)มวล (\d+) กิโลกรัมและ(\S+)มวล (\d+) กิโลกรัม.*ด้วยแรง (\d+) นิวตัน (\S+)มีความเร่ง", stem)
        if match:
            a, m1, b, m2, f, who = match.groups()
            mass = int(m1) if who == a else int(m2)
            assert _value(question) == Fraction(int(f), mass), (seed, stem)


def test_motion_bank_spans_all_four_named_motions_evenly():
    counts = {m: sum(1 for _, x in MOTION_EXAMPLES if x == m) for m in MOTIONS}
    assert set(ACCELERATION_OF) == set(MOTIONS)
    assert min(counts.values()) >= 5, counts


def test_accelerated_motion_fluency_describes_the_examples_motion():
    by_example = dict(MOTION_EXAMPLES)
    for seed in range(SEEDS):
        question = generate("phys.accelerated_motion_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        example = next((e for e in by_example if stem.startswith(f'"{e}"')), None)
        if example:
            assert answer == ACCELERATION_OF[by_example[example]], (seed, stem)
        elif answer in by_example:
            assert ACCELERATION_OF[by_example[answer]] in stem, (seed, stem)


def test_accelerated_motion_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.accelerated_motion_application", Random(seed))
        stem = _stem(question)
        if "ตกอิสระ" in stem:
            g, t = _nums(stem)
            expect = g * t if "ความเร็วเท่าใด" in stem else g * t * t / 2
            assert _value(question) == expect, (seed, stem)
        elif "ขอบโต๊ะสูง" in stem:
            h, u, g = _nums(stem)
            t = (2 * h / g) ** Fraction(1, 2)
            assert _value(question) == u * Fraction(t), (seed, stem)
        elif "วงกลมรัศมี" in stem:
            r, v = _nums(stem)
            assert _value(question) == v * v / r, (seed, stem)


def test_orbit_true_and_false_pools_are_disjoint():
    assert not set(ORBIT_TRUE) & set(ORBIT_FALSE)


def test_gravity_orbit_application_weight_and_inverse_square():
    for seed in range(SEEDS):
        question = generate("phys.gravity_orbit_application", Random(seed))
        stem = _stem(question)
        if stem.startswith("ยานสำรวจ"):
            weight, g_earth, g_there = _nums(stem)
            assert _value(question) == weight / g_earth * g_there, (seed, stem)
        elif "ระยะห่างจากจุดศูนย์กลางโลก" in stem:
            f, k = _nums(stem)
            assert _value(question) == f / (k * k), (seed, stem)
        else:
            f, k = _nums(stem)
            assert _value(question) == f * k, (seed, stem)


# ── slice 12: ว 2.2 ม.5/7, ม.5/8, ม.5/9, ม.5/10 ─────────────────────────────

_NAME_TO_VEC = {name: vec for vec, name in DIRECTION.items()}
_SIDE_TO_VEC = {"ทางขวาของ": (1, 0, 0), "ทางซ้ายของ": (-1, 0, 0),
                "ด้านบนของ": (0, 1, 0), "ด้านล่างของ": (0, -1, 0)}
_DIRS = "|".join(map(re.escape, sorted(_NAME_TO_VEC, key=len, reverse=True)))
_SIDES = "|".join(map(re.escape, _SIDE_TO_VEC))


def test_the_page_frame_is_right_handed():
    assert cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1)


def test_current_field_fluency_follows_the_right_hand_grip_rule():
    for seed in range(SEEDS):
        question = generate("phys.current_field_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        forward = re.search(rf"กระแสไฟฟ้าไหล({_DIRS}) จุด P อยู่({_SIDES})เส้นลวด", stem)
        backward = re.search(rf"จุด P อยู่({_SIDES})ลวดตรงยาวที่มีกระแสไฟฟ้า สนามแม่เหล็กที่จุด P มีทิศ({_DIRS}) ", stem)
        if forward:
            current, point = _NAME_TO_VEC[forward.group(1)], _SIDE_TO_VEC[forward.group(2)]
            assert _NAME_TO_VEC[answer] == cross(current, point), (seed, stem)
        elif backward:
            point, field = _SIDE_TO_VEC[backward.group(1)], _NAME_TO_VEC[backward.group(2)]
            assert cross(_NAME_TO_VEC[answer], point) == field, (seed, stem)
        else:
            clockwise = "ตามเข็มนาฬิกา" in stem
            assert answer.endswith("ขั้วใต้" if clockwise else "ขั้วเหนือ"), (seed, stem)


def test_magnetic_force_fluency_is_q_v_cross_b_for_charges_and_wires():
    kinds = set()
    for seed in range(SEEDS):
        question = generate("phys.magnetic_force_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        charge = re.search(rf"^(โปรตอน|อิเล็กตรอน|อนุภาคแอลฟา)เคลื่อนที่({_DIRS}) เข้าไปในสนามแม่เหล็กสม่ำเสมอที่มีทิศ({_DIRS}) ", stem)
        wire = re.search(rf"^ลวดตรงมีกระแสไฟฟ้าไหล({_DIRS}) วางอยู่ในสนามแม่เหล็กสม่ำเสมอที่มีทิศ({_DIRS}) ", stem)
        if charge:
            sign = -1 if charge.group(1) == "อิเล็กตรอน" else 1
            force = cross(_NAME_TO_VEC[charge.group(2)], _NAME_TO_VEC[charge.group(3)])
            expected = force if sign > 0 else tuple(-x for x in force)
            assert _NAME_TO_VEC[answer] == expected, (seed, stem)
            kinds.add("charge")
        elif wire:
            assert _NAME_TO_VEC[answer] == cross(_NAME_TO_VEC[wire.group(1)], _NAME_TO_VEC[wire.group(2)]), (seed, stem)
            kinds.add("wire")
        else:
            assert answer == "ไม่มีแรงกระทำ", (seed, stem)
    # The exact set reaches both objects the indicator names.
    assert kinds == {"charge", "wire"}


def test_magnetic_force_application_f_equals_bil():
    for seed in range(SEEDS):
        question = generate("phys.magnetic_force_application", Random(seed))
        stem = _stem(question)
        if stem.startswith("ลวดยาว"):
            length, current, b = _nums(stem)
            assert _value(question) == length * current * b, (seed, stem)


def test_induced_emf_application_transformer_follows_the_turns_ratio():
    for seed in range(SEEDS):
        question = generate("phys.induced_emf_application", Random(seed))
        stem = _stem(question)
        if stem.startswith("หม้อแปลงไฟฟ้ามีขดลวดปฐมภูมิ"):
            n_p, n_s, v_p, _ = _nums(stem)
            assert _value(question) == v_p * n_s / n_p, (seed, stem)


def test_emf_yes_and_no_cases_are_disjoint():
    assert not set(EMF_YES) & set(EMF_NO)


def test_nuclear_force_fluency_bank_reaches_both_named_forces():
    assert {force for _, _, force in NUCLEAR_PHENOMENA} == {"แรงเข้ม", "แรงอ่อน"}


# ── slice 13: ว 2.3 ม.5/1, ม.5/2, ม.5/3, ม.5/4 ──────────────────────────────

def _tex_value(tex: str) -> Fraction:
    mantissa, exponent = re.fullmatch(r"([\d.]+) \\times 10\^\{(-?\d+)\}", tex).groups()
    return Fraction(mantissa) * Fraction(10) ** int(exponent)


def test_nuclear_banks_cover_every_object_the_indicator_names():
    assert {about for _, about in NUCLEAR_TRUE} == {"ฟิชชัน", "ฟิวชัน", "มวลกับพลังงาน"}
    assert not {s for s, _ in NUCLEAR_TRUE} & set(NUCLEAR_FALSE)


def test_nuclear_energy_application_is_e_equals_m_c_squared():
    c2 = Fraction(9) * 10 ** 16
    for seed in range(SEEDS):
        question = generate("phys.nuclear_energy_application", Random(seed))
        given = _tex_value(_maths(question.stem)[0])
        answer = _tex_value(question.choices[question.answer].content[0].tex)
        if "พลังงานที่ปลดปล่อยออกมาเท่ากับกี่จูล" in _stem(question):
            assert answer == given * c2, seed
        else:
            assert answer == given / c2, seed
        values = [_tex_value(c.content[0].tex) for c in question.choices]
        assert len(set(values)) == 4


def test_renewable_energy_fluency_efficiency_payback_and_cost():
    for seed in range(SEEDS):
        question = generate("phys.renewable_energy_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        if "ประสิทธิภาพร้อยละ" in stem:
            given, useful = _nums(stem)
            assert _value(question) == useful / given * 100, (seed, stem)
        elif "คืนทุน" in stem:
            cost, saving = _nums(stem)
            assert _value(question) == cost / saving, (seed, stem)
        else:
            match = re.search(r"^(.+?)กำลังไฟฟ้า (\d+) วัตต์ และ(.+?)กำลังไฟฟ้า (\d+) วัตต์.*เปิดใช้ ([\d,]+) ชั่วโมง.*หน่วยละ (\d+) บาท", stem)
            a, pa, b, pb, hours, rate = match.groups()
            pa, pb, hours, rate = int(pa), int(pb), int(hours.replace(",", "")), int(rate)
            cheaper = a if pa < pb else b
            saving = Fraction(abs(pa - pb) * hours, 1000) * rate
            assert answer == f"{cheaper}คุ้มค่ากว่า ประหยัดค่าไฟฟ้าได้ {show13(saving)} บาท", (seed, stem)


def test_wave_banks_span_all_four_behaviours():
    for bank in (WAVE_EXAMPLES, WAVE_TRUE):
        assert {b for _, b in bank} == set(BEHAVIOURS)
    assert not {s for s, _ in WAVE_TRUE} & set(WAVE_FALSE)


def test_wave_behaviour_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.wave_behaviour_application", Random(seed))
        stem = _stem(question)
        if "มุมสะท้อน" in stem:
            (given,) = _nums(stem)
            angle = 90 - given if "ทำมุมกับผิวสะท้อน" in stem else given
            assert _value(question) == angle, (seed, stem)
        elif "ความยาวคลื่นในน้ำตื้น" in stem:
            f, _v1, v2 = _nums(stem)
            assert _value(question) == v2 / f, (seed, stem)
        elif "การกระจัดรวม" in stem:
            a, b = _nums(stem)
            expect = a + b if "สันคลื่นกับสันคลื่น" in stem else abs(a - b)
            assert _value(question) == expect, (seed, stem)
        else:
            gaps = [int(t.split()[0]) for t in _texts(question)]
            assert _value(question) == min(gaps), (seed, stem)


def test_resonance_bank_spans_its_three_objects():
    assert {about for _, about in RESONANCE_TRUE} == {"ความถี่ธรรมชาติ", "การสั่นพ้อง", "ผลของการสั่นพ้อง"}


def test_resonance_answers_follow_matching_frequency():
    for seed in range(SEEDS):
        question = generate("phys.resonance_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        if stem.startswith("แขวนลูกตุ้ม"):
            driver = re.search(r"ตัวขับที่ยาว (\d+)", stem).group(1)
            label = re.search(rf"ลูกตุ้ม (\S) ยาว {driver} เซนติเมตร", stem).group(1)
            assert answer == f"ลูกตุ้ม {label}", (seed, stem)
        elif stem.startswith("ชิงช้า"):
            assert answer == f"{_nums(stem)[0]} วินาที"
        else:
            assert answer.split()[0] == re.search(r"ความถี่ธรรมชาติ ([\d,]+)", stem).group(1)
    for seed in range(SEEDS):
        question = generate("phys.resonance_foundation", Random(seed))
        stem = _stem(question)
        if "ลูกตุ้มอย่างง่าย" in stem:
            lengths = [int(x) for x in re.search(r"ความยาวสาย ([\d, ]+) เซนติเมตร", stem).group(1).split(", ")]
            expect = min(lengths) if "สูงที่สุด" in stem else max(lengths)
            assert _texts(question)[question.answer] == f"{expect} เซนติเมตร"


# ── slice 14: ว 2.3 ม.5/5, ม.5/6, ม.5/7 ────────────────────────────────────

def test_sound_banks_span_their_named_objects():
    assert {b for _, b in SOUND_EXAMPLES} == set(BEHAVIOURS)
    assert {b for _, b in SOUND_TRUE} == set(BEHAVIOURS)
    assert {e for _, e in EFFECT_EXAMPLES} == set(SOUND_EFFECTS)
    assert {e for _, e in EFFECT_TRUE} == set(SOUND_EFFECTS)
    assert not {s for s, _ in SOUND_TRUE} & set(SOUND_FALSE)
    assert not {s for s, _ in EFFECT_TRUE} & set(EFFECT_FALSE)


def test_sound_wave_behaviour_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.sound_wave_behaviour_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        if "ลงไปในน้ำ" in stem:
            f = _nums(stem)[0]
            assert _value(question) == Fraction(1500) / f, (seed, stem)
        elif "331 + 0.6T" in stem:
            temp = _nums(stem)[-1]
            assert _value(question) == 331 + Fraction(6, 10) * temp, (seed, stem)
        else:
            wavelength, diff = _nums(stem)[-2:]
            halves = diff / (wavelength / 2)
            assert halves.denominator == 1
            assert answer.startswith("ดังมาก" if halves % 2 == 0 else "ค่อยมาก"), (seed, stem)


def test_sound_intensity_level_rises_ten_decibels_per_tenfold():
    for seed in range(SEEDS):
        question = generate("phys.sound_intensity_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        if stem.startswith("ถ้าความเข้มเสียงเพิ่มขึ้นเป็น"):
            factor = int(re.search(r"เป็น ([\d,]+) เท่า", stem).group(1).replace(",", ""))
            assert answer == f"{10 * (len(str(factor)) - 1)} เดซิเบล", (seed, stem)
        elif stem.startswith("ระดับเสียงเพิ่มขึ้น"):
            db = int(re.search(r"เพิ่มขึ้น (\d+) เดซิเบล", stem).group(1))
            assert answer == f"{10 ** (db // 10):,} เท่า", (seed, stem)
    for seed in range(SEEDS):
        question = generate("phys.sound_intensity_application", Random(seed))
        stem = _stem(question)
        if stem.startswith("เสียงมีความเข้ม"):
            k = int(re.search(r"10⁻([⁰¹²³⁴⁵⁶⁷⁸⁹]+) วัตต์", stem).group(1).translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")))
            assert _value(question) == 10 * (12 - k), (seed, stem)
        elif "เครื่องพร้อมกัน" in stem:
            base, n = _nums(stem)[:2]
            assert _value(question) == base + 10 * (len(str(int(n))) - 1), (seed, stem)


def test_sound_intensity_foundation_frequency_bands():
    for seed in range(SEEDS):
        question = generate("phys.sound_intensity_foundation", Random(seed))
        stem = _stem(question)
        match = re.search(r"ความถี่ ([\d,]+) เฮิรตซ์", stem)
        if match:
            f = int(match.group(1).replace(",", ""))
            want = "ใต้เสียง" if f < 20 else "เหนือเสียง" if f > 20_000 else "ได้ยิน"
            assert want in _texts(question)[question.answer], (seed, stem)


def test_sound_effects_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.sound_effects_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        if "ได้รับเสียงสะท้อน" in stem or "ได้ยินเสียงสะท้อนกลับ" in stem:
            v = 1500 if "ในน้ำ" in stem else 340
            t = _nums(stem)[-1]
            assert _value(question) == v * t / 2, (seed, stem)
        elif "บีตกี่ครั้ง" in stem:
            f1, f2 = _nums(stem)
            assert _value(question) == abs(f1 - f2), (seed, stem)
        elif "ขันสาย" in stem:
            f1, beats = _nums(stem)[:2]
            assert answer == f"{f1 - beats} เฮิรตซ์", (seed, stem)
        else:
            f = _nums(stem)[0]
            assert _value(question) == Fraction(340, 4) / f * 100, (seed, stem)


# ── slice 15: ว 2.3 ม.5/8-ม.5/12 ────────────────────────────────────────────

_COLOUR_BY_NAME = {name: c for c, name in COLOUR_NAME.items()}
_LIGHT_BY_NAME = {name: c for c, name in LIGHT_NAME.items()}
_COLOURS = "|".join(map(re.escape, sorted(_COLOUR_BY_NAME, key=len, reverse=True)))
_LIGHTS = "|".join(map(re.escape, sorted(_LIGHT_BY_NAME, key=len, reverse=True)))


def test_light_names_never_say_sunlight():
    assert "แสงแดง" not in _LIGHT_BY_NAME
    assert _LIGHT_BY_NAME["แสงสีแดง"] == frozenset({"R"})


def test_sound_use_bank_gives_every_principle_an_example():
    assert {p for _, p in SOUND_USES} == set(SOUND_PRINCIPLES)


def test_colour_vision_fluency_is_reflected_light_that_falls():
    for seed in range(SEEDS):
        question = generate("phys.colour_vision_fluency", Random(seed))
        stem = _stem(question)
        match = re.search(rf"เห็นเป็น({_COLOURS})ใต้แสงขาว .*?ส่องด้วย({_LIGHTS})เพียงอย่างเดียว", stem)
        if match:
            reflects, light = _COLOUR_BY_NAME[match.group(1)], _LIGHT_BY_NAME[match.group(2)]
            assert _texts(question)[question.answer] == COLOUR_NAME[reflects & light], (seed, stem)


def test_colour_vision_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.colour_vision_application", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        two = re.search(rf"เห็นเป็น({_COLOURS})ใต้แสงขาว ถูกส่องพร้อมกันด้วย({_LIGHTS})และ({_LIGHTS})ในห้องมืด", stem)
        stage = re.search(rf"บนเวทีที่ส่องด้วย({_LIGHTS})เพียงอย่างเดียว", stem)
        if two:
            reflects = _COLOUR_BY_NAME[two.group(1)]
            light = _LIGHT_BY_NAME[two.group(2)] | _LIGHT_BY_NAME[two.group(3)]
            assert answer == COLOUR_NAME[reflects & light], (seed, stem)
        elif stage:
            light = _LIGHT_BY_NAME[stage.group(1)]
            blacks = [c for c in _texts(question) if not _COLOUR_BY_NAME[c] & light]
            assert blacks == [answer], (seed, stem)


def test_colour_mixing_answers_are_set_arithmetic():
    for seed in range(SEEDS):
        question = generate("phys.colour_mixing_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        one = re.search(rf"^ส่อง({_LIGHTS})ผ่านแผ่นกรองแสง({_COLOURS}) ", stem)
        series = re.search(rf"^ส่องแสงขาวผ่านแผ่นกรองแสง({_COLOURS}) แล้วผ่านแผ่นกรองแสง({_COLOURS})ต่อ", stem)
        paint = re.search(rf"^ผสมสาร({_COLOURS})กับสาร({_COLOURS})ใน", stem)
        # Two filters in series also start "ส่องแสงขาวผ่านแผ่นกรองแสง...", so check them first.
        if series:
            assert answer == COLOUR_NAME[_COLOUR_BY_NAME[series.group(1)] & _COLOUR_BY_NAME[series.group(2)]]
        elif one:
            assert answer == COLOUR_NAME[_LIGHT_BY_NAME[one.group(1)] & _COLOUR_BY_NAME[one.group(2)]]
        elif paint:
            assert answer == COLOUR_NAME[_COLOUR_BY_NAME[paint.group(1)] & _COLOUR_BY_NAME[paint.group(2)]]
    for seed in range(SEEDS):
        question = generate("phys.colour_mixing_foundation", Random(seed))
        lights = re.findall(_LIGHTS, _stem(question))
        mixed = frozenset().union(*(_LIGHT_BY_NAME[ell] for ell in lights))
        assert _texts(question)[question.answer] == COLOUR_NAME[mixed], seed


def test_colour_mixing_application_filter_goggles():
    for seed in range(SEEDS):
        question = generate("phys.colour_mixing_application", Random(seed))
        match = re.search(rf"เห็นเป็น({_COLOURS})ใต้แสงขาว ผ่านแว่นที่ทำจากแผ่นกรองแสง({_COLOURS}) ", _stem(question))
        if match:
            expect = COLOUR_NAME[_COLOUR_BY_NAME[match.group(1)] & _COLOUR_BY_NAME[match.group(2)]]
            assert _texts(question)[question.answer] == expect, seed


def test_em_wave_application_is_c_equals_f_lambda():
    scale = {"เมกะเฮิรตซ์": 10 ** 6, "กิโลเฮิรตซ์": 10 ** 3, "กิกะเฮิรตซ์": 10 ** 9}
    for seed in range(SEEDS):
        question = generate("phys.em_wave_application", Random(seed))
        stem = _stem(question)
        forward = re.search(r"ส่งคลื่นความถี่ ([\d,]+) (\S+) ", stem)
        if forward:
            f = int(forward.group(1).replace(",", "")) * scale[forward.group(2)]
            assert _value(question) == Fraction(3 * 10 ** 8, f), (seed, stem)
        else:
            wavelength = Fraction(re.search(r"ความยาวคลื่น ([\d.]+) เมตร", stem).group(1))
            unit = re.search(r"มีความถี่กี่(\S+) ", stem).group(1)
            assert _value(question) * scale[unit] * wavelength == 3 * 10 ** 8, (seed, stem)


def test_signal_facts_cover_both_kinds():
    kinds = {k for _, k in SIGNAL_FACTS}
    assert kinds == {"สัญญาณแอนะล็อก", "สัญญาณดิจิทัล"}
    assert min(sum(1 for _, k in SIGNAL_FACTS if k == kind) for kind in kinds) >= 4


def test_em_comms_application_numbers():
    for seed in range(SEEDS):
        question = generate("phys.em_comms_application", Random(seed))
        stem = _stem(question)
        if "บิตต่อหนึ่งค่า" in stem:
            (bits,) = _nums(stem)
            assert _value(question) == 2 ** bits, seed
        elif "เมกะไบต์" in stem:
            size, rate = _nums(stem)[:2]
            assert _value(question) == size * 8 / rate, (seed, stem)

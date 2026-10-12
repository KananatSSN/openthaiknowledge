"""Regression checks for the Phase 2 Chemistry content review."""

from __future__ import annotations

from pathlib import Path

from otk.core import catalog
from otk.sets.chemistry.p6.acid_base import AcidBase
from otk.sets.chemistry.m1.particles_and_states_of_matter import StatesOfMatter
from otk.sets.chemistry.m2.separating_solutions import SeparationSolutionMethods
from otk.sets.chemistry.m1.atoms_elements_compounds import AtomMolecule, ElementOrCompound
from otk.sets.chemistry.m2.separating_solutions import Crystallization, SolventExtraction
from otk.sets.chemistry.m2.homo_separation import HomoSeparation
from otk.sets.chemistry.m1.pure_substances_and_mixtures import PureOrMixture
from otk.sets.chemistry.p6.sedimentation import Sedimentation


ROOT = Path(__file__).resolve().parents[2]


def _flat_category_text(question_type) -> str:
    return " ".join(
        text
        for category in question_type.CATEGORIES
        for text in (category.label, *category.members)
    )


def _bank_text(question_type) -> str:
    return " ".join(
        text
        for item in question_type.ITEMS
        for text in (item.stem, item.correct, *item.distractors)
    )


# The reviewed learning stages for every subject are checked together in
# test_science_stage_registry.py: five copies of that bookkeeping drifted
# apart, and the subject list there is derived from the registry so a new
# subject cannot be skipped. What stays here is content, not bookkeeping.


def test_the_phase_change_successor_is_published_as_an_application_set():
    """The Phase 2 split put this set at stage 3; it must stay there."""
    rows = {row["key"]: row for row in catalog()}
    assert rows["chem.phase_change_application"]["learning_stage"] == 3


def test_household_acid_base_examples_are_chemically_unambiguous():
    authored = _flat_category_text(AcidBase)
    assert "น้ำปลา" not in authored
    assert "น้ำยาล้างจาน" not in authored
    assert "น้ำยาล้างห้องน้ำชนิดกรด" in authored
    assert "สารละลายโซเดียมคลอไรด์บริสุทธิ์" in authored


def test_matter_and_particle_wording_does_not_overgeneralize():
    states = _flat_category_text(StatesOfMatter)
    assert "อย่างเป็นระเบียบ" not in states
    assert "ยึดตำแหน่งค่อนข้างคงที่" in states

    pure = _flat_category_text(PureOrMixture)
    elements = _flat_category_text(ElementOrCompound)
    atoms = _bank_text(AtomMolecule)
    assert "ทองคำแท่ง" not in pure
    assert "มีหน่วยย่อยที่เล็กที่สุดเป็นอะตอม" not in elements
    assert "เป็นอะตอมเสมอสำหรับสารทุกชนิด" in atoms
    assert "ทั้งสองเป็นประเภทของสารบริสุทธิ์" in atoms


def test_separation_repairs_remove_ambiguous_or_inaccurate_examples():
    assert "แยกแอลกอฮอล์ออกจากน้ำ" not in _flat_category_text(HomoSeparation)
    assert "แยกแอลกอฮอล์ออกจากน้ำ" not in _flat_category_text(SeparationSolutionMethods)
    assert "สารละลายจุนสี" in _flat_category_text(HomoSeparation)

    sedimentation = _bank_text(Sedimentation)
    assert "อนุภาคของสารส้มเป็นตัวกลาง" not in sedimentation
    assert "แรงต้านจากน้ำ" in sedimentation
    assert "อนุภาคที่หนาแน่นกว่าเคลื่อนออกจากแกน" in sedimentation

    crystallization = _bank_text(Crystallization)
    assert "ตกลงสู่ก้นภาชนะคล้ายกับการตกตะกอน" not in crystallization
    assert "บนเมล็ดผลึก" in crystallization

    extraction = _bank_text(SolventExtraction)
    assert "แช่กลีบดอกไม้ในตัวทำละลายที่เหมาะสม" in extraction

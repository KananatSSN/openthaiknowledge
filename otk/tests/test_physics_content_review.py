"""Regression checks for the Phase 2 Physics and electricity content review."""

from __future__ import annotations

from pathlib import Path
from random import Random

from otk.core import generate
from otk.sets.physics.m3.electric_power_and_energy import PowerConcept
from otk.sets.physics.m3.ohms_law import Quantities
from otk.sets.physics.m5.resistivity import ResistanceFactors
from otk.sets.physics.m3.series_and_parallel_circuits import SeriesParallelRules
from otk.sets.physics.m3.refraction_and_dispersion import Dispersion
from otk.sets.physics.m3.reflection_of_light import LightProperties


ROOT = Path(__file__).resolve().parents[2]


def _flat_category_text(question_type) -> str:
    return " ".join(
        value
        for category in question_type.CATEGORIES
        for value in (category.label, *category.members)
    )


def _bank_text(question_type) -> str:
    return " ".join(
        value
        for item in question_type.ITEMS
        for value in (item.stem, item.correct, *item.distractors)
    )


def _stem_text(question) -> str:
    return " ".join(block.text for block in question.stem if block.kind == "text")



# The reviewed learning stages for every subject are checked together in
# test_science_stage_registry.py: five copies of that bookkeeping drifted
# apart, and the subject list there is derived from the registry so a new
# subject cannot be skipped. What stays here is content, not bookkeeping.


def test_light_classifier_uses_single_property_examples():
    authored = _flat_category_text(LightProperties)
    assert "การเกิดปรากฏการณ์รุ้งกินน้ำ" not in authored
    assert "แยกเป็นสเปกตรัมสี" not in authored
    assert "เหรียญที่อยู่ก้นถ้วยน้ำดูเหมือนอยู่ตื้นขึ้น" in authored
    assert "แนวลำแสงเปลี่ยนทิศเมื่อเดินทางผ่านปริซึม" in authored

    dispersion = _bank_text(Dispersion)
    assert "การหักเห การสะท้อนภายใน และการกระจาย" in dispersion


def test_electricity_relationships_state_their_required_conditions():
    quantities = _flat_category_text(Quantities)
    resistance = _flat_category_text(ResistanceFactors)
    power = _bank_text(PowerConcept)

    assert "เมื่อความต่างศักย์เท่ากัน" in quantities
    assert "อุณหภูมิคงที่" in resistance
    assert "ลดความต่างศักย์และกระแสไฟฟ้า" in resistance
    assert "เมื่อใช้ความต่างศักย์เท่ากัน" in power


def test_parallel_resistance_rule_uses_the_reciprocal_of_total_resistance():
    rules = _flat_category_text(SeriesParallelRules)
    assert "ส่วนกลับของความต้านทานรวมเท่ากับผลบวกของส่วนกลับ" in rules
    assert "ความต้านทานรวมหาได้จากผลบวกของส่วนกลับ" not in rules


def test_qv_questions_ask_for_energy_transfer_magnitude_without_sign_ambiguity():
    for key in ("elec.energy", "elec.energy_charge_voltage"):
        stems = [_stem_text(generate(key, Random(seed))) for seed in range(200)]
        qv_stems = [stem for stem in stems if "คูลอมบ์" in stem]
        assert qv_stems
        assert all("พลังงานไฟฟ้าถ่ายโอนขนาดเท่าใด" in stem for stem in qv_stems)
        assert all("ต้องใช้พลังงานไฟฟ้า" not in stem for stem in qv_stems)

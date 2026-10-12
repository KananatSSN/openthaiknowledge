"""Content-scope checks for Phase 2's additive science successors."""

from __future__ import annotations

import json
from random import Random

from otk.core import REGISTRY, catalog, generate
from otk.core.curriculum_science import SCIENCE_SUCCESSOR_KEYS


def _text(blocks) -> str:
    return " ".join(
        getattr(block, "text", "") or getattr(block, "tex", "")
        for block in blocks
    )


def _question_text(question) -> str:
    parts = [_text(question.stem), _text(question.hint)]
    parts.extend(_text(choice.content) for choice in question.choices)
    return " ".join(parts)


def _samples(key: str, count: int = 200):
    return [generate(key, Random(seed)) for seed in range(count)]


def test_successors_are_additive_staged_views_of_the_five_legacy_keys():
    rows = {row["key"]: row for row in catalog() if row["key"] in SCIENCE_SUCCESSOR_KEYS}
    assert set(rows) == set(SCIENCE_SUCCESSOR_KEYS)
    assert {row["source_key"] for row in rows.values()} == {
        "chem.separation",
        "chem.particles",
        "chem.sedimentation",
        "chem.distillation",
        "elec.energy",
    }
    assert {row["learning_stage"] for row in rows.values()} <= {1, 2}
    assert all(row["learning_stage_key"] in {"foundation", "fluency"} for row in rows.values())


def test_every_successor_generates_distinct_choices_across_200_seeds():
    for key in SCIENCE_SUCCESSOR_KEYS:
        for question in _samples(key):
            rendered = [
                json.dumps(
                    [block.model_dump(mode="json") for block in choice.content],
                    ensure_ascii=False, sort_keys=True,
                )
                for choice in question.choices
            ]
            assert len(rendered) >= 2, key
            assert len(rendered) == len(set(rendered)), key
            assert question.type == key


def test_separation_successors_do_not_cross_method_scopes():
    primary = " ".join(_question_text(q) for q in _samples("chem.separation_filter_magnet"))
    assert "การกรอง" in primary and "แม่เหล็ก" in primary
    assert all(term not in primary for term in ("การกลั่น", "โครมาโทกราฟี", "กรวยแยก", "ระเหยแห้ง"))

    secondary = " ".join(_question_text(q) for q in _samples("chem.separation_solution_methods"))
    assert all(term in secondary for term in ("ระเหย", "กลั่นอย่างง่าย", "โครมาโทกราฟี"))
    assert all(term not in secondary for term in ("น้ำมันดิบ", "กรวยแยก", "แม่เหล็ก"))

    funnel = " ".join(_question_text(q) for q in _samples("chem.separation_immiscible_liquids"))
    assert "กรวยแยก" in funnel


def test_particle_successors_guarantee_neutral_and_ion_stems():
    neutral = _samples("chem.particles_neutral")
    ions = _samples("chem.particles_ions")
    assert all("อะตอมต่อไปนี้" in _text(question.stem) for question in neutral)
    assert all("ไอออนต่อไปนี้" in _text(question.stem) for question in ions)


def test_sedimentation_and_distillation_successors_pin_their_concepts():
    settling = " ".join(_question_text(q) for q in _samples("chem.sedimentation_settling"))
    centrifuge = " ".join(_question_text(q) for q in _samples("chem.sedimentation_centrifuge"))
    assert "หมุนเหวี่ยง" not in settling
    assert "หมุนเหวี่ยง" in centrifuge

    simple = " ".join(_question_text(q) for q in _samples("chem.distillation_simple"))
    fractional = " ".join(_question_text(q) for q in _samples("chem.distillation_fractional"))
    assert "ลำดับส่วน" not in simple and "น้ำมันดิบ" not in simple
    assert "ลำดับส่วน" in fractional and "น้ำมันดิบ" in fractional


def test_energy_successors_never_cross_formula_scopes():
    power_time = _samples("elec.energy_power_time")
    charge_voltage = _samples("elec.energy_charge_voltage")
    assert all("QV" not in _text(question.hint) for question in power_time)
    assert all("Pt" in _text(question.hint) or "W}{t" in _text(question.hint)
               for question in power_time)
    assert all("QV" in _text(question.hint) for question in charge_voltage)


def test_legacy_sources_remain_mixed_compatibility_sets():
    assert REGISTRY["chem.separation"].params() == {"ask": 0}
    assert REGISTRY["chem.particles"].params()["ion_chance"] == 60

    samples = {
        key: " ".join(_question_text(question) for question in _samples(key, 500))
        for key in (
            "chem.separation", "chem.particles", "chem.sedimentation",
            "chem.distillation", "elec.energy",
        )
    }
    assert "กรวยแยก" in samples["chem.separation"] and "แม่เหล็ก" in samples["chem.separation"]
    assert "อะตอมต่อไปนี้" in samples["chem.particles"] and "ไอออนต่อไปนี้" in samples["chem.particles"]
    assert "หมุนเหวี่ยง" in samples["chem.sedimentation"] and "ตกตะกอน" in samples["chem.sedimentation"]
    assert "ลำดับส่วน" in samples["chem.distillation"] and "น้ำมันดิบ" in samples["chem.distillation"]
    assert "QV" in samples["elec.energy"] and "Pt" in samples["elec.energy"]

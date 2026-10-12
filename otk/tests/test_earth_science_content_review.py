"""Regression checks for the Phase 2 Earth-science content review."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from PIL import Image

from otk.core import catalog
from otk.sets.earth_science.p6.rocks_and_the_rock_cycle import (
    IgneousCooling,
    ROCK_EVIDENCE,
    ROCK_PHOTOS,
    RockCycle,
    RockFormation,
    RockTerms,
    RockTexture,
)
from otk.sets.earth_science.p6.uses_of_rocks_and_minerals import RockUses


ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = ROOT / "otk/pictures"


def _category_text(question_type) -> str:
    return " ".join(
        value
        for category in question_type.CATEGORIES
        for value in (category.label, *category.members)
    )


def _concept_text(question_type) -> str:
    return " ".join(
        value
        for item in question_type.ITEMS
        for value in (item.stem, item.correct, *item.distractors)
    )



# The reviewed learning stages for every subject are checked together in
# test_science_stage_registry.py: five copies of that bookkeeping drifted
# apart, and the subject list there is derived from the registry so a new
# subject cannot be skipped. What stays here is content, not bookkeeping.


def test_igneous_content_distinguishes_magma_lava_and_non_universal_vesicles():
    formation = _category_text(RockFormation)
    cooling = _category_text(IgneousCooling)
    texture = _category_text(RockTexture)

    assert "แมกมาเย็นตัวและแข็งตัวอยู่ใต้ผิวโลก" in formation
    assert "ลาวาเย็นตัวและแข็งตัวบนหรือใกล้ผิวโลก" in formation
    assert "แมกมาเย็นตัวอย่างช้า ๆ ใต้ผิวโลก" in cooling
    assert "ผลึกแร่ขนาดเล็กมาก" in cooling
    assert "รูพรุน" not in cooling
    assert "รูพรุน" not in texture
    assert "แข็งมากกว่าหินประเภทอื่น" not in formation


def test_texture_and_use_tables_cover_all_ten_rocks_with_diagnostic_properties():
    expected = {photo.rock for photo in ROCK_PHOTOS}
    assert {category.label for category in RockTexture.CATEGORIES} == expected
    assert {category.label for category in RockUses.CATEGORIES} == expected
    assert "ขูดกระจกเป็นรอย" in _category_text(RockTexture)
    assert "ขัดเงาได้" in _category_text(RockUses)


def test_terms_and_cycle_do_not_retain_overgeneralized_claims():
    terms = _concept_text(RockTerms)
    cycle = _concept_text(RockCycle)

    assert "หินหลอมเหลวหรือหลอมเหลวบางส่วน" in terms
    assert "หินประเภทใดมีความแข็งมากกว่าหินประเภทอื่น" not in terms
    assert "กระบวนการหนึ่งที่ทำให้เกิดหินปูน" in terms
    assert "การอัดแน่นและการเชื่อมประสาน" in cycle
    assert "หินแต่ละชนิดเปลี่ยนไปได้หลายทาง" in cycle
    assert "แมกมา → ลาวา → หินอัคนี → หินตะกอน → หินแปร" not in cycle


def test_each_photo_has_unique_supporting_evidence_and_a_valid_bitmap():
    rocks = {photo.rock for photo in ROCK_PHOTOS}
    assert set(ROCK_EVIDENCE) == rocks
    assert len(set(ROCK_EVIDENCE.values())) == len(rocks) == 10

    assert len(ROCK_PHOTOS) == 30
    assert len({photo.asset_id for photo in ROCK_PHOTOS}) == 30
    assert Counter(photo.rock for photo in ROCK_PHOTOS) == dict.fromkeys(rocks, 3)
    for photo in ROCK_PHOTOS:
        with Image.open(ASSET_ROOT / f"{photo.asset_id}.png") as bitmap:
            assert min(bitmap.size) >= 400


def test_formation_and_cycle_mappings_do_not_claim_complete_model_explanations():
    rows = {row["key"]: row for row in catalog()}
    assert rows["geo.rock_formation"]["mapping_status"] == "standard_scope"
    assert rows["geo.rock_cycle"]["mapping_status"] == "standard_scope"
    assert rows["geo.rock_cycle"]["indicator_codes"] == ["ว 3.2 ป.6/1"]

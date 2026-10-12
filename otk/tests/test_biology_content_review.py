"""Regression checks for the Phase 2 Biology content review."""

from __future__ import annotations

from PIL import Image

from otk.core import catalog
from otk.core.render.assets import shipped_asset
from otk.sets.biology.m4.skeleton import SkeletonLabel
from otk.sets.biology.m3.relationships_between_organisms import Symbiosis




def _flat_category_text(question_type) -> str:
    return " ".join(
        value
        for category in question_type.CATEGORIES
        for value in (category.label, *category.members)
    )



# The reviewed learning stages for every subject are checked together in
# test_science_stage_registry.py: five copies of that bookkeeping drifted
# apart, and the subject list there is derived from the registry so a new
# subject cannot be skipped. What stays here is content, not bookkeeping.


def test_symbiosis_examples_make_both_organisms_benefits_explicit():
    authored = _flat_category_text(Symbiosis)
    assert "นกจับแมลงกินเศษอาหารในปากจระเข้" not in authored
    assert "เสือกับสิงโตแย่งชิงเหยื่อ" not in authored
    assert "ควายมีปรสิตลดลง" in authored
    assert "ผึ้งกินน้ำหวานจากดอกไม้และช่วยถ่ายเรณูให้พืช" in authored
    assert "สิงโตกับไฮยีนาแย่งชิงเหยื่อ" in authored


def test_symbiosis_mapping_does_not_claim_the_unassessed_survey_explanation():
    row = next(item for item in catalog() if item["key"] == "ecology.symbiosis")
    assert row["mapping_status"] == "standard_scope"
    assert row["indicator_codes"] == ["ว 1.1 ม.3/2"]


def test_skeleton_bitmap_coordinates_align_with_every_named_bone():
    with Image.open(shipped_asset("skeleton")).convert("RGB") as bitmap:
        width, height = bitmap.size
        assert (width, height) == (400, 400)
        for part in SkeletonLabel._PARTS:
            x = round(part.marker.x * (width - 1))
            y = round(part.marker.y * (height - 1))
            nearby = (
                bitmap.getpixel((px, py))
                for px in range(max(0, x - 6), min(width, x + 7))
                for py in range(max(0, y - 6), min(height, y + 7))
            )
            assert any(min(pixel) < 250 for pixel in nearby), part.label

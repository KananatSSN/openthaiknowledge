"""Regression checks for the Phase 2 Astronomy/space content review."""

from __future__ import annotations

from pathlib import Path

from otk.core import catalog
from otk.sets.astronomy.m3.solar_system_and_gravity import AstronomicalPhenomena, Gravity
from otk.sets.astronomy.m3.moon_phases_and_tides import MoonPhases, Tides
from otk.sets.astronomy.m3.space_technology import SatelliteUses, SpaceMissions, SpaceTechnology
from otk.sets.astronomy.m3.seasons_and_the_suns_path import Seasons, SunPath


ROOT = Path(__file__).resolve().parents[2]


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


def test_phenomenon_categories_separate_orbital_motion_from_gravity():
    moon_orbit = AstronomicalPhenomena.CATEGORIES[2]
    gravity = AstronomicalPhenomena.CATEGORIES[3]
    assert any("เวลาขึ้นและตกของดวงจันทร์" in item for item in moon_orbit.members)
    assert not any("น้ำขึ้น" in item or "น้ำลง" in item for item in moon_orbit.members)
    assert any("มวลน้ำ" in item for item in gravity.members)
    assert "การกำหนดทิศตะวันออก–ตะวันตก" not in _category_text(AstronomicalPhenomena)


def test_space_technology_and_satellite_roles_are_non_overlapping():
    labels = [category.label for category in SpaceTechnology.CATEGORIES]
    assert labels[0].startswith("ดาวเทียมที่ให้บริการหรือสำรวจโลก")
    assert labels[1].startswith("ยานสำรวจและรถสำรวจวัตถุอื่น")
    remote_sensing = SatelliteUses.CATEGORIES[-1]
    assert all("พายุ" not in item and "น้ำท่วม" not in item for item in remote_sensing.members)
    assert "วัตถุแถบไคเปอร์" in SpaceMissions.CATEGORIES[2].label
    assert "เดินทางออกนอกระบบสุริยะ" not in _category_text(SpaceMissions)


def test_gravity_bank_uses_the_inverse_square_relationship():
    authored = _concept_text(Gravity)
    assert "F = Gm₁m₂/r²" in authored
    assert "เหลือ 1/4 ของแรงเดิม" in authored
    assert "ทิศความเร็วของดาวเคราะห์เปลี่ยนไปตามวงโคจร" in authored


def test_season_and_sun_path_claims_are_location_and_time_qualified():
    seasons = _concept_text(Seasons)
    sun_path = _concept_text(SunPath)
    assert "พลังงานต่อพื้นที่มากกว่า" in seasons
    assert "เวลาเที่ยงสุริยะท้องถิ่น" in sun_path
    assert "ไม่จำเป็นต้องตรง 12:00 น." in sun_path
    assert "บริเวณส่วนใหญ่ในซีกโลกเหนือ" in sun_path
    assert "เวลาเที่ยงวัน" not in sun_path


def test_moon_bank_distinguishes_full_moon_from_lunar_eclipse_and_adds_timing():
    authored = _concept_text(MoonPhases)
    assert "ไม่จำเป็นต้องเรียงตรงจนเกิดจันทรุปราคา" in authored
    assert "ขึ้นใกล้เวลาที่ดวงอาทิตย์ตก" in authored
    assert "ขึ้นเวลาเดิมทุกวัน" in authored


def test_tide_bank_qualifies_frequency_and_uses_differential_gravity():
    authored = _concept_text(Tides)
    assert "ความแตกต่างของแรงโน้มถ่วงระหว่างด้านใกล้และไกลของโลก" in authored
    assert "ชายฝั่งส่วนใหญ่" in authored
    assert "24 ชั่วโมง 50 นาที" in authored
    assert "บางพื้นที่อาจมีรูปแบบต่างออกไป" in authored
    assert "ทำมุมใกล้ 90 องศา" in authored


def test_model_topics_do_not_claim_exact_coverage_without_model_construction():
    rows = {row["key"]: row for row in catalog()}
    for key in ("astro.seasons", "astro.sun_path", "astro.moon_phases", "astro.tides"):
        assert rows[key]["mapping_status"] == "standard_scope"
    assert rows["astro.gravity"]["mapping_status"] == "exact"

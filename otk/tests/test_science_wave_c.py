"""Acceptance gate for Phase 5 Wave C — earth science and astronomy.

Slice 1 delivers ``ว 3.1 ป.1/1``, ``ป.1/2`` and ``ป.3/1``; slice 2 adds ``ป.3/2``,
``ป.3/3`` and ``ป.4/1``; slice 3 adds ``ป.5/1``, ``ป.5/2`` and ``ป.6/2``; slice 4
adds ``ป.4/2``, ``ป.4/3`` and ``ป.6/1``, closing ``ว 3.1`` for the primary grades;
slice 5 stages out the three ``ม.3`` indicators that stood ``partial``; slice 6
opens ``ม.6`` with ``ม.6/1``, ``ม.6/2`` and ``ม.6/3``; slice 7 adds ``ม.6/4``,
``ม.6/5`` and ``ม.6/6``, the stars themselves; slice 8 adds ``ม.6/7``, ``ม.6/8``
and ``ม.6/9``; slice 9 adds ``ม.6/10`` and closes ``ว 3.1``; slice 10 opens
``ว 3.2`` with ``ป.1/1``, ``ป.2/1`` and ``ป.2/2``, rocks and soil; slice 11
adds ``ป.3/1``-``ป.3/4``, air and wind; slice 12 adds ``ป.5/1``-``ป.5/3``, water; slice 13 adds ``ป.5/4`` and
``ป.5/5``, what vapour becomes and what falls from clouds; slice 14 adds
``ป.6/2``-``ป.6/4``, rocks and minerals in use, fossils, and local winds;
slice 15 adds ``ป.6/5``-``ป.6/7``, monsoon seasons, hazards, and safety;
slice 16 adds ``ป.6/8``, ``ป.6/9`` and ``ม.1/1``, the greenhouse effect and the
atmosphere's layers; slice 17 adds ``ม.1/2``-``ม.1/4``, weather, storms and
forecasting; slice 18 adds ``ม.1/5``-``ม.1/7``, using forecasts and climate change;
slice 19 adds ``ม.2/1``-``ม.2/3``, fossil fuels and renewable energy; slice 20
adds ``ม.2/4``-``ม.2/6``, Earth's interior, surface processes and soil; slice 21
adds ``ม.2/7``-``ม.2/9``, soil in use, water sources and sustainable water use;
slice 22 adds ``ม.2/10`` and ``ม.6/1``-``ม.6/3``, surface hazards and plates;
slice 23 adds ``ม.6/4``-``ม.6/6``, volcanoes, earthquakes and tsunamis;
slice 24 adds ``ม.6/7``-``ม.6/9``, solar energy, pressure and the Coriolis effect;
slice 25 adds ``ม.6/10``-``ม.6/12``, global circulation, ocean currents and their effects;
slice 26 adds ``ม.6/13``-``ม.6/14``, climate change and weather maps, closing ``ว 3.2``.
What is checked here is what a reviewer would otherwise have to check by hand:

* the filing follows the evidence clause — the Fluency set is the ``exact`` one,
  because it is the set that puts the record or the demonstration in the stem;
* each indicator holds all three stages, in its own curriculum unit;
* Wave C is a cohort of its own, disjoint from every earlier one, so no gate
  that has already passed can be read as covering it;
* the data-reading sets really do answer from their own stems — the shadow table
  is re-parsed and the answer re-derived, and the sky record is checked to put
  exactly one object on both of its lines;
* ``ป.3/2`` names three objects, so its ``exact`` set is checked to span all three;
* every ``ว 3.1`` indicator of the primary grades is asserted to hold three
  stages, so none can be dropped again.

Slice 3 recorded ``ป.4/2``, ``ป.4/3`` and ``ป.6/1`` as unassessable because they
open with ``สร้างแบบจำลอง``. That was wrong: ``ว 3.1 ม.3/3`` reads ``สร้างแบบจำลอง
ที่อธิบายการเกิดข้างขึ้นข้างแรม…`` and has been filed complete, with an ``exact``
set, since the Phase 3 pilot. Where the model *explains* something, the
explanation is what is assessed and an item can carry the model in its stem;
only ``สร้างแบบจำลองแสดง Y``, where the model is the product, is out of reach —
which is why nothing here claims ``ป.4/3``'s first half.
"""

from __future__ import annotations

import re
from random import Random

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import (
    BASIC,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_PLACEMENTS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_C_APPROVED_KEYS,
    SCIENCE_WAVE_C_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.core.registry import REGISTRY
from otk.sets.earth_science.m6.climate_factors import ACTIVITIES as CLIMATE_ACTIVITIES
from otk.sets._support.science_wave_c26 import CLIMATE_FACTORS
from otk.sets.earth_science.m6.weather_map import SITUATIONS, SYMBOLS
from otk.sets.earth_science.m6.latitude_circulation import BELTS, WIND_BELTS
from otk.sets.earth_science.m6.ocean_currents import CURRENTS
from otk.sets._support.science_wave_c25 import OCEAN_PARTS
from otk.sets._support.science_wave_c25 import EFFECTS as CIRCULATION_EFFECTS
from otk.sets.earth_science.m6.circulation_effects import PHENOMENA as CIRCULATION_PHENOMENA
from otk.sets.earth_science.m6.coriolis import HEADINGS as AIR_HEADINGS
from otk.sets.earth_science.m6.pressure_circulation import PRESSURE_CHAIN, pressure_parts
from otk.sets._support.science_wave_c24 import SOLAR_FACTORS
from otk.sets._support.science_wave_c23 import CASES as HAZARD_CASES
from otk.sets._support.science_wave_c23 import EXPLANATIONS as HAZARD_EXPLANATIONS
from otk.sets._support.science_wave_c23 import MORE_FALSES as HAZARD_MORE_FALSES
from otk.sets._support.science_wave_c23 import MORE_PLAN_LINES as HAZARD_MORE_PLAN_LINES
from otk.sets._support.science_wave_c23 import MORE_TRUES as HAZARD_MORE_TRUES
from otk.sets._support.science_wave_c23 import PLANS as HAZARD_PLANS
from otk.sets.earth_science.m6.plate_boundary import BOUNDARIES, MORE_MOTIONS
from otk.sets.earth_science.m6.earth_layers import PHYSICAL_LAYERS
from otk.sets.earth_science.m6.plate_evidence import SPREADING, seafloor_record
from otk.sets.earth_science.m2.surface_hazard import SURFACE_HAZARDS
from otk.sets._support.science_wave_c21 import AGRICULTURE
from otk.sets.earth_science.m2.water_source import GROUND_TRUE, SURFACE_TRUE
from otk.sets.earth_science.m2.soil_property import PROFILES, TOOLS
from otk.sets.earth_science.m2.water_use_model import WATER_CARE, WATER_NEEDS, water_model
from otk.sets.earth_science.m2.soil_profile import CAUSES, FACTORS, HORIZONS
from otk.sets.earth_science.m2.surface_processes import MORE_MODELS, PROCESSES
from otk.sets.earth_science.m2.earth_interior import SHELLS, layer_table
from otk.sets.earth_science.m2.renewable_energy import ENERGIES, LOCALITIES
from otk.sets.earth_science.m2.fuel_saving import FUEL_CARE, FUEL_NEEDS
from otk.sets.earth_science.m2.fossil_fuel import FUELS, emissions_record
from otk.sets.earth_science.m1.climate_action import CLIMATE_CARE, CLIMATE_NEEDS
from otk.sets.earth_science.m1.climate_change import SERIES, climate_record
from otk.sets.earth_science.m1.forecast_use import PLANS as FORECAST_PLANS
from otk.sets.earth_science.m1.weather_forecast import (
    CLEAR,
    FORECAST_STEPS,
    INSTRUMENTS,
    RAIN,
    forecast_record,
)
from otk.sets.earth_science.m1.storms import STORM_CASES, STORMS
from otk.sets.earth_science.m1.weather_factors import day_record
from otk.sets.earth_science.p6.greenhouse_action import ACTION_CARE, ACTION_NEEDS
from otk.sets._support.science_wave_c16 import MECHANISM
from otk.sets.earth_science.p6.greenhouse_effect import jar_readings
from otk.sets.earth_science.p6.greenhouse_effect import EFFECTS as GREENHOUSE_EFFECTS
from otk.sets.earth_science.m1.atmosphere_layers import LAYERS as ATMOSPHERE_LAYERS
from otk.sets.earth_science.p6.natural_hazard import HAZARDS
from otk.sets.earth_science.p6.hazard_safety import PLANS
from otk.sets.earth_science.p6.monsoon_season import SEASONS, season_record
from otk.sets.earth_science.p6.fossil import FINDS, MODELS
from otk.sets.earth_science.p6.uses_of_rocks_and_minerals import MATERIALS, MINERAL, ROCK
from otk.sets.earth_science.p6.local_wind import WINDS
from otk.sets.earth_science.p5.precipitation_forms import FALLS, MORE_FALL_REPORTS
from otk.sets.earth_science.p5.condensation_forms import FORMS
from otk.sets.earth_science.p5.water_saving import CASES, CONSERVE, PRACTICES, SAVE
from otk.sets.earth_science.p5.water_amount import SOURCES, water_table
from otk.sets.earth_science.p5.water_cycle import STEPS
from otk.sets._support.science_wave_c1 import DEMOS, SKY_TOPIC
from otk.sets.astronomy.p1.day_night_sky import NIGHT_ONLY, UNRECORDED
from otk.sets.astronomy.p3.sun_path_pattern import SUN_TIMES, _shadow_lengths
from otk.sets.earth_science.p3.wind_use import BENEFIT, HARM, WIND_EVENTS, wind_record
from otk.sets.earth_science.p3.clean_air import CLEAN_AIR_CARE, CLEAN_AIR_NEEDS
from otk.sets.earth_science.p3.air_composition import (
    LEVELS,
    OBSERVATIONS,
    POLLUTIONS,
    pollution_record,
)
from otk.sets.earth_science.p3.wind_origin import PLACES, thermometer_readings
from otk.sets.earth_science.p2.soil_use import CATEGORIES, SOIL_USES, survey
from otk.sets.earth_science.p2.soil_type import COMPONENTS, SOILS
from otk.sets._support.science_wave_c10 import LETTERS
from otk.sets.earth_science.p1.rock_look import ROCKS, _describe
from otk.sets.astronomy.m6.space_exploration import (
    BANDS,
    DEFENSIBLE,
    PLATFORM_CLAUSES,
    PLATFORMS,
    SATELLITE,
    SPACECRAFT,
    STATION,
    TELESCOPE,
)
from otk.sets.astronomy.m6.stellar_evolution import CHANGES, TRACKS, _properties
from otk.sets.astronomy.m6.sun_structure import EFFECTS, LAYERS, SUN_SPANNING
from otk.sets.astronomy.m6.solar_system_origin import ORIGIN_SPANNING, ZONES
from otk.sets.astronomy.m6.stellar_luminosity_and_magnitude import FIVE_STEPS, STARS
from otk.sets.astronomy.m6.star_formation import FORMATION_SPANNING, STAGES
from otk.sets.astronomy.m6.star_colour_and_spectra import SPECTRAL, _spans_three
from otk.sets.astronomy.m6.bigbang_evidence import (
    BOTH_EVIDENCE,
    CMB,
    GALAXIES,
    HUBBLE,
    HUBBLE_CONSTANT,
)
from otk.sets.astronomy.m6.universe_after_the_big_bang import EPOCHS, SPANNING
from otk.sets.astronomy.m6.milky_way import GALAXY_PARTS
from otk.sets._support.science_wave_c5 import EQUATION_CASES
from otk.sets.astronomy.m3.space_technology import MISSIONS, ORBITS
from otk.sets.astronomy.m3.seasons_and_the_suns_path import SEASON_POINTS, _spans_both
from otk.sets.astronomy.p4.moon_shape_cycle import CYCLE
from otk.sets.astronomy.p6.eclipse import ECLIPSES, LUNAR, SOLAR, _eclipse_pair, _eclipse_swapped
from otk.sets.astronomy.p4.solar_system_periods import PLANETS
from otk.sets.astronomy.p5.star_planet_compare import (
    DIFFERENCES,
    PLANET,
    STAR,
    _both_sides,
    _swapped,
)
from otk.sets.astronomy.p6.space_tech_history import USES
from otk.sets.astronomy.p5.star_map import YEAR_CHART
from otk.sets._support.science_wave_c2 import ASPECTS, DAY_NIGHT, DIRECTION, RISING
from otk.sets.astronomy.p3.sun_benefits import BENEFITS
from otk.sets.astronomy.p4.moon_path_pattern import _moonrise_times


SEEDS = 300


def _triple(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}_{stage}"
                 for stage in ("foundation", "fluency", "application"))


INDICATORS = {
    "ว 3.1 ป.1/1": _triple("astro.day_night_sky"),
    "ว 3.1 ป.1/2": _triple("astro.daytime_stars"),
    "ว 3.1 ป.3/1": _triple("astro.sun_path_pattern"),
    "ว 3.1 ป.3/2": _triple("astro.earth_rotation"),
    "ว 3.1 ป.3/3": _triple("astro.sun_benefits"),
    "ว 3.1 ป.4/1": _triple("astro.moon_path_pattern"),
    "ว 3.1 ป.5/1": _triple("astro.star_planet_compare"),
    "ว 3.1 ป.5/2": _triple("astro.star_map"),
    "ว 3.1 ป.6/2": _triple("astro.space_tech_history"),
    "ว 3.1 ป.4/2": _triple("astro.moon_shape_cycle"),
    "ว 3.1 ป.4/3": _triple("astro.solar_system_periods"),
    "ว 3.1 ป.6/1": _triple("astro.eclipse"),
    "ว 3.1 ม.3/1": _triple("astro.gravity_orbit"),
    "ว 3.1 ม.3/2": _triple("astro.season_model"),
    "ว 3.1 ม.3/4": _triple("astro.space_tech_use"),
    "ว 3.1 ม.6/1": _triple("astro.universe_evolution"),
    "ว 3.1 ม.6/2": _triple("astro.bigbang_evidence"),
    "ว 3.1 ม.6/3": _triple("astro.milky_way"),
    "ว 3.1 ม.6/4": _triple("astro.star_formation"),
    "ว 3.1 ม.6/5": _triple("astro.star_luminosity"),
    "ว 3.1 ม.6/6": _triple("astro.star_spectrum"),
    "ว 3.1 ม.6/7": _triple("astro.stellar_evolution"),
    "ว 3.1 ม.6/8": _triple("astro.solar_system_origin"),
    "ว 3.1 ม.6/9": _triple("astro.sun_structure"),
    "ว 3.1 ม.6/10": _triple("astro.space_exploration"),
    "ว 3.2 ป.1/1": _triple("geo.rock_look"),
    "ว 3.2 ป.2/1": _triple("geo.soil_type"),
    "ว 3.2 ป.2/2": _triple("geo.soil_use"),
    "ว 3.2 ป.3/1": _triple("geo.air_composition"),
    "ว 3.2 ป.3/2": _triple("geo.clean_air"),
    "ว 3.2 ป.3/3": _triple("geo.wind_origin"),
    "ว 3.2 ป.3/4": _triple("geo.wind_use"),
    "ว 3.2 ป.5/1": _triple("geo.water_amount"),
    "ว 3.2 ป.5/2": _triple("geo.water_saving"),
    "ว 3.2 ป.5/3": _triple("geo.water_cycle"),
    "ว 3.2 ป.5/4": _triple("geo.condensation_forms"),
    "ว 3.2 ป.5/5": _triple("geo.precipitation_forms"),
    "ว 3.2 ป.6/2": _triple("geo.rock_mineral_use"),
    "ว 3.2 ป.6/3": _triple("geo.fossil"),
    "ว 3.2 ป.6/4": _triple("geo.local_wind"),
    "ว 3.2 ป.6/5": _triple("geo.monsoon_season"),
    "ว 3.2 ป.6/6": _triple("geo.natural_hazard"),
    "ว 3.2 ป.6/7": _triple("geo.hazard_safety"),
    "ว 3.2 ป.6/8": _triple("geo.greenhouse_effect"),
    "ว 3.2 ป.6/9": _triple("geo.greenhouse_action"),
    "ว 3.2 ม.1/1": _triple("geo.atmosphere_layers"),
    "ว 3.2 ม.1/2": _triple("geo.weather_factors"),
    "ว 3.2 ม.1/3": _triple("geo.storms"),
    "ว 3.2 ม.1/4": _triple("geo.weather_forecast"),
    "ว 3.2 ม.1/5": _triple("geo.forecast_use"),
    "ว 3.2 ม.1/6": _triple("geo.climate_change"),
    "ว 3.2 ม.1/7": _triple("geo.climate_action"),
    "ว 3.2 ม.2/1": _triple("geo.fossil_fuel"),
    "ว 3.2 ม.2/2": _triple("geo.fuel_saving"),
    "ว 3.2 ม.2/3": _triple("geo.renewable_energy"),
    "ว 3.2 ม.2/4": _triple("geo.earth_interior"),
    "ว 3.2 ม.2/5": _triple("geo.surface_processes"),
    "ว 3.2 ม.2/6": _triple("geo.soil_profile"),
    "ว 3.2 ม.2/7": _triple("geo.soil_property"),
    "ว 3.2 ม.2/8": _triple("geo.water_source"),
    "ว 3.2 ม.2/9": _triple("geo.water_use_model"),
    "ว 3.2 ม.2/10": _triple("geo.surface_hazard"),
    "ว 3.2 ม.6/1": _triple("geo.earth_layers"),
    "ว 3.2 ม.6/2": _triple("geo.plate_evidence"),
    "ว 3.2 ม.6/3": _triple("geo.plate_boundary"),
    "ว 3.2 ม.6/4": _triple("geo.volcano"),
    "ว 3.2 ม.6/5": _triple("geo.earthquake"),
    "ว 3.2 ม.6/6": _triple("geo.tsunami"),
    "ว 3.2 ม.6/7": _triple("geo.solar_energy"),
    "ว 3.2 ม.6/8": _triple("geo.pressure_circulation"),
    "ว 3.2 ม.6/9": _triple("geo.coriolis"),
    "ว 3.2 ม.6/10": _triple("geo.latitude_circulation"),
    "ว 3.2 ม.6/11": _triple("geo.ocean_currents"),
    "ว 3.2 ม.6/12": _triple("geo.circulation_effects"),
    "ว 3.2 ม.6/13": _triple("geo.climate_factors"),
    "ว 3.2 ม.6/14": _triple("geo.weather_map"),
}

# Two verbs joined by ``และ``, each with an object of its own, so by the
# conjunction rule each carries a free outcome and earns an ``exact`` set.
TWO_FREE_VERBS = frozenset({"ว 3.1 ป.5/2", "ว 3.1 ป.6/2",
                            "ว 3.1 ป.4/2", "ว 3.1 ป.6/1",
                            "ว 3.1 ม.3/4", "ว 3.1 ม.6/3",
                            "ว 3.1 ม.6/5", "ว 3.1 ม.6/7",
                            "ว 3.1 ม.6/9", "ว 3.2 ป.2/1",
                            "ว 3.2 ป.3/1", "ว 3.2 ป.5/1",
                            "ว 3.2 ป.6/3", "ว 3.2 ป.6/4",
                            "ว 3.2 ม.1/1", "ว 3.2 ม.1/3",
                            "ว 3.2 ม.1/4", "ว 3.2 ม.2/1",
                            "ว 3.2 ม.2/3", "ว 3.2 ม.2/5",
                            "ว 3.2 ม.2/6", "ว 3.2 ม.2/9",
                            "ว 3.2 ม.6/1", "ว 3.2 ม.6/3",
                            "ว 3.2 ม.6/4", "ว 3.2 ม.6/5",
                            "ว 3.2 ม.6/6", "ว 3.2 ม.6/13",
                            "ว 3.2 ม.6/14"})

# Every ``ว 3.1`` indicator of the primary grades.
PRIMARY_INDICATORS = frozenset(
    f"ว 3.1 ป.{grade}/{number}"
    for grade, count in ((1, 2), (3, 3), (4, 3), (5, 2), (6, 2))
    for number in range(1, count + 1))
NEW_KEYS = tuple(key for keys in INDICATORS.values() for key in keys)


def _texts(question) -> list[str]:
    return [
        " ".join(getattr(block, "text", getattr(block, "tex", ""))
                 for block in choice.content)
        for choice in question.choices
    ]


def _stem(question) -> str:
    return " ".join(getattr(block, "text", getattr(block, "tex", ""))
                    for block in question.stem)


# ── filing ────────────────────────────────────────────────────────────────────

def test_every_new_key_is_registered_and_placed():
    for key in NEW_KEYS:
        assert key in REGISTRY, key
        assert key in SCIENCE_PLACEMENTS, key


def test_wave_c_is_its_own_cohort():
    """Wave C carries its own open gate; no earlier gate looked at these sets."""
    assert set(NEW_KEYS) == SCIENCE_WAVE_C_KEYS
    for earlier in (SCIENCE_WAVE_KEYS, SCIENCE_WAVE_B_KEYS,
                    SCIENCE_BIOLOGY_CLOSURE_KEYS):
        assert not SCIENCE_WAVE_C_KEYS & earlier


def test_the_approved_sets_are_whole_indicators_inside_wave_c():
    """Approval is recorded per indicator, never for part of a learning path."""
    assert SCIENCE_WAVE_C_APPROVED_KEYS <= SCIENCE_WAVE_C_KEYS
    for code, keys in INDICATORS.items():
        approved = set(keys) & SCIENCE_WAVE_C_APPROVED_KEYS
        assert approved in (set(), set(keys)), code


def test_each_indicator_holds_three_stages_in_one_unit():
    for code, keys in INDICATORS.items():
        specs = [SCIENCE_PLACEMENTS[key] for key in keys]
        assert {spec.indicator_codes for spec in specs} == {(code,)}, code
        assert len({spec.mapping_status for spec in specs}) <= 2, code
        assert len({spec.unit for spec in specs}) == 1, code
        assert len({spec.level for spec in specs}) == 1, code


def test_the_evidence_reading_set_is_the_exact_one():
    """Each indicator names its evidence, so Fluency alone earns ``exact``.

    ``ป.3/3`` is the ``ตระหนัก`` one. Its evidence clause, ``โดยบรรยายประโยชน์``, is
    something a learner can be asked to do on paper, so by the rule Wave B settled
    for ``ม.2`` it earns exactly one ``exact`` set — and at Fluency, like the rest.
    """
    for code, (foundation, fluency, application) in INDICATORS.items():
        assert SCIENCE_PLACEMENTS[fluency].mapping_status == "exact", code
        expected = "exact" if code in TWO_FREE_VERBS else "standard_scope"
        assert SCIENCE_PLACEMENTS[foundation].mapping_status == expected, code
        assert SCIENCE_PLACEMENTS[application].mapping_status == "standard_scope", code


def test_no_application_set_claims_exact():
    for keys in INDICATORS.values():
        assert SCIENCE_PLACEMENTS[keys[2]].mapping_status != "exact"


# Slices 1-4 author new units under one shared topic. Slice 5 instead joins three
# units that legacy sets already occupy, so its sets carry those units' own
# topics — a learner reaching ``เทคโนโลยีอวกาศ`` has to find all of its stages in
# one place, not half of them under a new name.
JOINED_UNITS = {
    "ว 3.1 ม.3/1": "ระบบสุริยะและแรงโน้มถ่วง",
    "ว 3.1 ม.3/2": "ฤดูและการเคลื่อนที่ปรากฏของดวงอาทิตย์",
    "ว 3.1 ม.3/4": "เทคโนโลยีอวกาศ",
}

# Slice 6 opens ``ม.6``, where the content is far from the primary sky topic, so
# each indicator gets a topic of its own rather than being folded into it.
OWN_TOPICS = {
    "ว 3.1 ม.6/1": "วิวัฒนาการของเอกภพหลังบิกแบง",
    "ว 3.1 ม.6/2": "หลักฐานที่สนับสนุนทฤษฎีบิกแบง",
    "ว 3.1 ม.6/3": "กาแล็กซีทางช้างเผือก",
    "ว 3.1 ม.6/4": "การเกิดดาวฤกษ์",
    "ว 3.1 ม.6/5": "ความส่องสว่างและโชติมาตรของดาวฤกษ์",
    "ว 3.1 ม.6/6": "สี อุณหภูมิผิว และสเปกตรัมของดาวฤกษ์",
    "ว 3.1 ม.6/7": "วิวัฒนาการของดาวฤกษ์",
    "ว 3.1 ม.6/8": "การเกิดระบบสุริยะและเขตเอื้อต่อชีวิต",
    "ว 3.1 ม.6/9": "ดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ",
    "ว 3.1 ม.6/10": "การสำรวจอวกาศ",
    "ว 3.2 ป.1/1": "ลักษณะภายนอกของหิน",
    "ว 3.2 ป.2/1": "ส่วนประกอบและชนิดของดิน",
    "ว 3.2 ป.2/2": "การใช้ประโยชน์จากดิน",
    "ว 3.2 ป.3/1": "ส่วนประกอบและความสำคัญของอากาศ",
    "ว 3.2 ป.3/2": "การลดมลพิษทางอากาศ",
    "ว 3.2 ป.3/3": "การเกิดลม",
    "ว 3.2 ป.3/4": "ประโยชน์และโทษของลม",
    "ว 3.2 ป.5/1": "ปริมาณน้ำในแหล่งต่าง ๆ",
    "ว 3.2 ป.5/2": "การใช้น้ำอย่างประหยัดและการอนุรักษ์น้ำ",
    "ว 3.2 ป.5/3": "วัฏจักรน้ำ",
    "ว 3.2 ป.5/4": "เมฆ หมอก น้ำค้าง และน้ำค้างแข็ง",
    "ว 3.2 ป.5/5": "ฝน หิมะ และลูกเห็บ",
    "ว 3.2 ป.6/2": "หินและการเปลี่ยนแปลง",
    "ว 3.2 ป.6/3": "ซากดึกดำบรรพ์",
    "ว 3.2 ป.6/4": "ลมบก ลมทะเล และมรสุม",
    "ว 3.2 ป.6/5": "มรสุมและฤดูของประเทศไทย",
    "ว 3.2 ป.6/6": "ภัยธรรมชาติและธรณีพิบัติภัย",
    "ว 3.2 ป.6/7": "การเฝ้าระวังและปฏิบัติตนจากภัยธรรมชาติ",
    "ว 3.2 ป.6/8": "ปรากฏการณ์เรือนกระจก",
    "ว 3.2 ป.6/9": "การลดแก๊สเรือนกระจก",
    "ว 3.2 ม.1/1": "ชั้นบรรยากาศ",
    "ว 3.2 ม.1/2": "ลมฟ้าอากาศและปัจจัยที่มีผล",
    "ว 3.2 ม.1/3": "พายุฝนฟ้าคะนองและพายุหมุนเขตร้อน",
    "ว 3.2 ม.1/4": "การพยากรณ์อากาศ",
    "ว 3.2 ม.1/5": "การใช้ประโยชน์จากคำพยากรณ์อากาศ",
    "ว 3.2 ม.1/6": "การเปลี่ยนแปลงภูมิอากาศโลก",
    "ว 3.2 ม.1/7": "การปฏิบัติตนภายใต้การเปลี่ยนแปลงภูมิอากาศ",
    "ว 3.2 ม.2/1": "เชื้อเพลิงซากดึกดำบรรพ์",
    "ว 3.2 ม.2/2": "การใช้เชื้อเพลิงซากดึกดำบรรพ์อย่างรู้คุณค่า",
    "ว 3.2 ม.2/3": "พลังงานทดแทน",
    "ว 3.2 ม.2/4": "โครงสร้างภายในโลก",
    "ว 3.2 ม.2/5": "การผุพัง การกร่อน และการสะสมตัว",
    "ว 3.2 ม.2/6": "ชั้นหน้าตัดดินและการเกิดดิน",
    "ว 3.2 ม.2/7": "สมบัติของดินและการใช้ประโยชน์",
    "ว 3.2 ม.2/8": "แหล่งน้ำผิวดินและแหล่งน้ำใต้ดิน",
    "ว 3.2 ม.2/9": "การใช้น้ำอย่างยั่งยืน",
    "ว 3.2 ม.2/10": "ธรณีพิบัติภัยบนผิวโลก",
    "ว 3.2 ม.6/1": "การแบ่งชั้นและสมบัติของโครงสร้างโลก",
    "ว 3.2 ม.6/2": "หลักฐานการเคลื่อนที่ของแผ่นธรณี",
    "ว 3.2 ม.6/3": "แนวรอยต่อของแผ่นธรณี",
    "ว 3.2 ม.6/4": "ภูเขาไฟระเบิด",
    "ว 3.2 ม.6/5": "แผ่นดินไหว",
    "ว 3.2 ม.6/6": "สึนามิ",
    "ว 3.2 ม.6/7": "การได้รับพลังงานจากดวงอาทิตย์",
    "ว 3.2 ม.6/8": "การหมุนเวียนของอากาศจากความกดอากาศ",
    "ว 3.2 ม.6/9": "ทิศทางลมกับการหมุนรอบตัวเองของโลก",
    "ว 3.2 ม.6/10": "การหมุนเวียนของอากาศตามเขตละติจูด",
    "ว 3.2 ม.6/11": "การหมุนเวียนของน้ำผิวหน้าในมหาสมุทร",
    "ว 3.2 ม.6/12": "ผลของการหมุนเวียนของอากาศและน้ำในมหาสมุทร",
    "ว 3.2 ม.6/13": "ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศโลก",
    "ว 3.2 ม.6/14": "แผนที่อากาศและการวางแผนการดำเนินชีวิต",
}


@pytest.mark.parametrize("key", NEW_KEYS)
def test_every_set_is_basic_and_carries_its_unit_topic(key):
    assert SCIENCE_PLACEMENTS[key].course_type == BASIC
    code = next(one for one, keys in INDICATORS.items() if key in keys)
    expected = JOINED_UNITS.get(code) or OWN_TOPICS.get(code) or SKY_TOPIC
    assert generate(key, Random(0)).topic == expected


def test_all_three_stages_of_an_indicator_share_one_topic():
    """A learner practising a unit must find its whole path in one topic."""
    for code, keys in INDICATORS.items():
        topics = {generate(key, Random(0)).topic for key in keys}
        assert len(topics) == 1, (code, topics)


def test_the_joined_units_are_the_ones_the_legacy_sets_already_occupy():
    """Slice 5 completes existing units rather than opening rival ones.

    Only sets claiming the indicator on its own are counted. ``astro.phenomena``
    predates the consolidation and claims ``ม.3/1``, ``ม.3/2`` and ``ม.3/3`` at
    once, so it sits in one unit while speaking for three indicators; that is a
    legacy filing this slice does not touch.
    """
    for code, topic in JOINED_UNITS.items():
        units = {spec.unit for spec in SCIENCE_PLACEMENTS.values()
                 if spec.indicator_codes == (code,)}
        assert units == {topic}, (code, units)


# ── answer uniqueness ─────────────────────────────────────────────────────────


def test_the_authored_tables_hold_no_repeated_answer():
    """A repeated conclusion would make two demonstrations share an answer."""
    assert len({demo.conclusion for demo in DEMOS}) == len(DEMOS)
    for demo in DEMOS:
        assert demo.conclusion not in demo.wrongs
        assert len(set(demo.wrongs)) == len(demo.wrongs) >= 3


def test_the_three_object_indicator_is_answered_across_all_three():
    """``ป.3/2`` names three things, so the ``exact`` set has to reach them all."""
    assert {aspect.about for aspect in ASPECTS} == {RISING, DAY_NIGHT, DIRECTION}
    seen = set()
    for seed in range(SEEDS):
        stem = _stem(generate("astro.earth_rotation_fluency", Random(seed)))
        for aspect in ASPECTS:
            if aspect.question in stem:
                seen.add(aspect.about)
    assert seen == {RISING, DAY_NIGHT, DIRECTION}, seen


def test_the_comparison_set_always_states_both_sides():
    """``เปรียบเทียบ`` of two named objects is not answered by one side alone."""
    for seed in range(SEEDS):
        question = generate("astro.star_planet_compare_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        assert STAR in answer and PLANET in answer, (seed, answer)


def test_no_comparison_row_can_be_answered_by_its_own_mirror():
    """The swapped pairing is offered every draw, and is always false."""
    assert len({item.aspect for item in DIFFERENCES}) == len(DIFFERENCES)
    for item in DIFFERENCES:
        assert item.star != item.planet
        assert _swapped(item) != _both_sides(item)
        assert _both_sides(item) not in item.wrongs
        assert len(set(item.wrongs)) == 2


def test_the_yearly_star_chart_runs_east_to_west_and_never_back():
    """The record has to show the one direction a star group actually drifts."""
    positions = [where for _, where in YEAR_CHART]
    assert len(set(positions)) == len(positions)
    east = [index for index, where in enumerate(positions) if "ตะวันออก" in where]
    west = [index for index, where in enumerate(positions) if "ตะวันตก" in where]
    assert east and west
    assert max(east) < min(west), positions


def test_each_everyday_situation_needs_exactly_one_technology():
    """A situation answered by two rows would give the item two answers."""
    assert len({use.technology for use in USES}) == len(USES)
    assert len({use.situation for use in USES}) == len(USES)
    assert len({use.because for use in USES}) == len(USES)


def test_wo_three_one_is_complete_for_every_primary_grade():
    """``ว 3.1`` has no open indicator left in ป.1-ป.6, and none may be dropped."""
    assert PRIMARY_INDICATORS <= set(INDICATORS)
    covered = {code for spec in SCIENCE_PLACEMENTS.values()
               for code in spec.indicator_codes if code.startswith("ว 3.1 ป.")}
    assert PRIMARY_INDICATORS - covered == set()


def test_the_rock_record_answers_from_its_own_rows():
    """Re-read the printed record and check the answer names the right rock."""
    asked = set()
    for seed in range(SEEDS):
        question = generate("geo.rock_look_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record, asked_text = stem.split(" จากบันทึกนี้ ")
        rows = dict(part.split(": ", 1) for part in record.split(" — ", 1)[1].split(" / "))
        assert len(rows) == 4 and len(set(rows.values())) == 4, (seed, rows)
        if asked_text.startswith("หินก้อนใด"):
            asked.add("which")
            wanted = asked_text.removeprefix("หินก้อนใด").removeprefix("มี")
            parts = wanted.split("และ") if " " not in wanted else [wanted]
            matches = [name for name, row in rows.items()
                       if all(part in row for part in parts)]
            assert matches == [answer], (seed, asked_text, rows, answer)
        else:
            asked.add("describe")
            name = asked_text.split(" มีลักษณะ")[0]
            assert rows[name] == answer, (seed, name, answer)
    assert asked == {"which", "describe"}


def test_the_rock_table_shares_no_colour_surface_or_feature():
    for field in ("colour", "surface", "feature"):
        values = [getattr(rock, field) for rock in ROCKS]
        assert len(set(values)) == len(ROCKS), field
        for value in values:
            # A value inside another row's text would let two rows match a question.
            assert sum(value in _describe(rock) for rock in ROCKS) == 1, value
    assert LETTERS == ("ก", "ข", "ค", "ง")


def test_each_soil_test_shows_one_component_and_the_types_differ_on_both_criteria():
    assert len({item.name for item in COMPONENTS}) == len(COMPONENTS)
    assert len({item.evidence for item in COMPONENTS}) == len(COMPONENTS)
    for field in ("name", "texture", "cohesion"):
        assert len({getattr(soil, field) for soil in SOILS}) == len(SOILS), field


def test_every_classifying_answer_uses_both_criteria():
    """``ป.2/1`` classifies by texture and cohesion, so no answer rests on one alone."""
    for seed in range(SEEDS):
        question = generate("geo.soil_type_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        soil = next(soil for soil in SOILS if soil.name == answer or soil.name in stem)
        text = answer if soil.name in stem else stem
        assert soil.texture in text and soil.cohesion in text, (seed, stem, answer)


def test_the_soil_survey_has_one_most_common_use_and_one_absent_use():
    for seed in range(2000):
        rows, counts = survey(Random(seed))
        assert sorted(counts.values()) == [0, 1, 2, 3], counts
        assert set(counts) == set(CATEGORIES)
        tally = {category: sum(1 for _, used in rows if used == category)
                 for category in CATEGORIES}
        assert tally == counts, (seed, rows)


def test_the_soil_survey_answer_is_re_derived_from_the_stem():
    for seed in range(SEEDS):
        question = generate("geo.soil_use_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        tally = {category: stem.count(f"ใช้ดินเพื่อ{category}") for category in CATEGORIES}
        if "มากที่สุด" in stem:
            assert answer == max(tally, key=tally.get), (seed, tally, answer)
        else:
            assert tally[answer] == 0, (seed, tally, answer)
            assert sum(count == 0 for count in tally.values()) == 1


def test_each_soil_use_names_one_soil_and_one_reason():
    for field in ("use", "soil", "because"):
        assert len({getattr(use, field) for use in SOIL_USES}) == len(SOIL_USES), field


def test_each_activity_shows_one_component_of_air():
    assert len({row.seen for row in OBSERVATIONS}) == len(OBSERVATIONS)
    assert len({row.component for row in OBSERVATIONS}) == len(OBSERVATIONS)


def test_the_pollution_record_rises_with_the_level_in_every_draw():
    """The conclusion says harm grows with pollution, so the record must show it."""
    for seed in range(2000):
        item = POLLUTIONS[seed % len(POLLUTIONS)]
        _, days = pollution_record(Random(seed), item)
        by_level = [dict(days)[level] for level in LEVELS]
        assert by_level == sorted(by_level) and len(set(by_level)) == 4, (seed, days)


def test_every_air_fluency_answer_states_importance_and_harm():
    """``ป.3/1``'s second verb governs two objects, so the answer holds both."""
    for seed in range(SEEDS):
        question = generate("geo.air_composition_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        item = next(item for item in POLLUTIONS if item.source in _stem(question))
        assert item.importance in answer and item.effect in answer, (seed, answer)
        assert answer.endswith("มากขึ้น"), (seed, answer)


def test_each_clean_air_need_names_a_practice_from_its_own_table():
    practices = {care.practice for care in CLEAN_AIR_CARE}
    assert {need.practice for need in CLEAN_AIR_NEEDS} <= practices
    assert len({need.practice for need in CLEAN_AIR_NEEDS}) == len(CLEAN_AIR_NEEDS)
    assert len({care.reason for care in CLEAN_AIR_CARE}) == len(CLEAN_AIR_CARE)


def test_the_wind_blows_from_the_cooler_place_to_the_warmer_one():
    """Re-read both temperatures from the stem and check the stated direction."""
    for seed in range(2000):
        hot, cool = thermometer_readings(Random(seed))
        assert hot - cool >= 3, (seed, hot, cool)
    places = {place for pair in PLACES for place in pair}
    for seed in range(SEEDS):
        question = generate("geo.wind_origin_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้")[0].split(" และเมื่อจุดธูป")[0]
        temps = {}
        for part in record.split(" / "):
            place, degrees = part.removesuffix(" องศาเซลเซียส").rsplit(" ", 1)
            assert place in places, (seed, part)
            temps[place] = int(degrees)
        warm = max(temps, key=temps.get)
        cool = min(temps, key=temps.get)
        if "พัดไปทางใด" in stem:
            assert answer == f"พัดจาก{cool}ไปยัง{warm}", (seed, temps, answer)
        else:
            assert answer.startswith(f"อากาศเหนือ{warm}ร้อนกว่า"), (seed, temps, answer)
            assert f"ลอยเอียงไปทาง{warm}" in stem, (seed, stem)


def _split_benefit_harm(text: str) -> tuple[str, str]:
    benefit, harm = text.removeprefix(f"{BENEFIT}ของลม เช่น ").split(f" ส่วน{HARM}ของลม เช่น ")
    return benefit, harm


def test_the_wind_record_sorts_benefit_from_harm_in_the_answer():
    kinds = {event.event: event.kind for event in WIND_EVENTS}
    for seed in range(2000):
        rows = wind_record(Random(seed))
        assert sorted(row.kind for row in rows) == sorted([BENEFIT, BENEFIT, HARM, HARM])
    for seed in range(SEEDS):
        question = generate("geo.wind_use_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        benefit, harm = _split_benefit_harm(answer)
        assert kinds[benefit] == BENEFIT and kinds[harm] == HARM, (seed, answer)
        assert benefit in stem and harm in stem, (seed, answer)
        for wrong in _texts(question):
            if wrong != answer:
                b, h = _split_benefit_harm(wrong)
                assert (kinds[b], kinds[h]) != (BENEFIT, HARM), (seed, wrong)


def test_the_water_answers_are_re_derived_from_the_scaled_table():
    """Parse the printed table back out and check both water sets against it."""
    usable_names = [source.name for source in SOURCES if source.usable]
    for key in ("geo.water_amount_foundation", "geo.water_amount_fluency"):
        for seed in range(SEEDS):
            question = generate(key, Random(seed))
            stem, answer = _stem(question), _texts(question)[question.answer]
            table_text = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้ ")[0]
            table = {}
            for part in table_text.split(" / "):
                name, amount, unit = part.rsplit(" ", 2)
                table[name] = int(amount.replace(",", ""))
            assert list(table) == [source.name for source in SOURCES], (seed, table)
            usable = sum(table[name] for name in usable_names)
            if "มากที่สุด" in stem and "แหล่งน้ำใด" in stem:
                assert answer == max(table, key=table.get)
            elif "น้อยที่สุด" in stem:
                assert answer == min(table, key=table.get)
            elif "เรียงแหล่งน้ำ" in stem:
                assert answer == " > ".join(sorted(table, key=table.get, reverse=True))
            elif "มากกว่า" in stem:
                first, second = stem.split(" จากข้อมูลนี้ ")[1].split("มีน้ำมากกว่า")
                second = second.rsplit("กี่", 1)[0]
                assert answer == f"{table[first] - table[second]:,} {unit}", (seed, answer)
            elif "รวมกันมีกี่" in stem:
                assert answer.endswith(f"รวม {usable:,} {unit}"), (seed, answer)
                assert all(name in answer for name in usable_names)
            else:
                assert answer == f"{usable:,} {unit}", (seed, answer)


def test_the_scaled_table_keeps_its_proportions_and_distinct_amounts():
    for seed in range(500):
        _, amounts, _ = water_table(Random(seed))
        values = list(amounts.values())
        assert values == sorted(values, reverse=True) and len(set(values)) == 4
        assert values[0] // values[3] == SOURCES[0].parts // SOURCES[3].parts


def test_every_water_proposal_names_one_saving_and_one_conserving_practice():
    """``ป.5/2`` names both, so each answer holds one of each, right for its case."""
    kinds = {practice.practice: practice.kind for practice in PRACTICES}
    for case in CASES:
        assert kinds[case.save] == SAVE and kinds[case.conserve] == CONSERVE
        assert case.save not in case.defensible and case.conserve not in case.defensible
    for seed in range(SEEDS):
        question = generate("geo.water_saving_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        case = next(case for case in CASES if case.situation in stem)
        assert case.save in answer and case.conserve in answer, (seed, answer)
        for wrong in _texts(question):
            if wrong != answer:
                assert not (case.save in wrong and case.conserve in wrong)
                for practice in case.defensible:
                    assert practice not in wrong, (seed, wrong)


def test_the_water_cycle_model_runs_in_order_with_one_part_per_process():
    for field in ("name", "happens", "in_model"):
        assert len({getattr(step, field) for step in STEPS}) == len(STEPS), field
    assert [step.name for step in STEPS][0] == "การระเหย"


def test_the_condensation_comparison_holds_all_four_and_wrongs_swap_two():
    """``ป.5/4`` compares four objects, so every answer places all four."""
    names = [form.name for form in FORMS]
    for field in ("how", "model"):
        assert len({getattr(form, field) for form in FORMS}) == len(FORMS), field
    for seed in range(SEEDS):
        question = generate("geo.condensation_forms_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        parts = answer.split(" / ")
        assert len(parts) == 4, (seed, answer)
        if "→" in answer:
            record = stem.split(" — ", 1)[1].split(" ข้อใด")[0]
            model_of = dict(part.removeprefix("แบบจำลอง ").split(": ", 1)
                            for part in record.split(" / "))
            for part in parts:
                letter, name = part.removeprefix("แบบจำลอง ").split(" → ")
                form = next(form for form in FORMS if form.name == name)
                assert model_of[letter] == form.model, (seed, part)
        else:
            for part in parts:
                name, how = part.split(": ", 1)
                assert next(form for form in FORMS if form.name == name).how == how
        assert sorted(part.split(" → ")[-1].split(":")[0] for part in parts) == sorted(names)
        for wrong in _texts(question):
            if wrong != answer:
                # One swap, or two disjoint swaps combined by the convergence breaker.
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)


def test_the_precipitation_comparison_is_re_derived_from_the_record():
    """``ป.5/5`` compares three objects from collected data; read the record back."""
    for field in ("how", "report"):
        assert len({getattr(fall, field) for fall in FALLS}) == len(FALLS), field
    for seed in range(SEEDS):
        question = generate("geo.precipitation_forms_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้")[0]
        report_of = dict(part.removeprefix("เหตุการณ์ ").split(": ", 1)
                         for part in record.split(" / "))
        parts = answer.split(" / ")
        assert len(parts) == 3
        for part in parts:
            letter, rest = part.removeprefix("เหตุการณ์ ").split(" เป็น", 1)
            fall = next(fall for fall in FALLS if rest.startswith(fall.name + " เพราะ"))
            assert report_of[letter] in (fall.report, *MORE_FALL_REPORTS[fall.name]), (seed, part)
            assert rest == f"{fall.name} เพราะ{fall.how}"
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)  # one swap, or two combined


def test_new_slices_are_highlighted_for_review_until_approved():
    """A slice that lands after an approval must show up on the reviewer's worklist."""
    from otk.core.curriculum_science import REVIEW_PENDING
    pending = REVIEW_PENDING.get("Phase 5 Wave C", frozenset())
    assert pending == SCIENCE_WAVE_C_KEYS - SCIENCE_WAVE_C_APPROVED_KEYS


def test_the_rock_mineral_answer_is_re_derived_from_the_survey():
    """``ป.6/2`` names rocks and minerals, so the answer gives one of each, per the record."""
    kind_of = {item.name: item.kind for item in MATERIALS}
    for field in ("name", "product", "because"):
        assert len({getattr(item, field) for item in MATERIALS}) == len(MATERIALS), field
    for seed in range(SEEDS):
        question = generate("geo.rock_mineral_use_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้")[0]
        made_of = {}
        for row in record.split(" / "):
            product, material = row.rsplit(" ทำจาก", 1)
            made_of[material] = product
        rock_half, mineral_half = answer.split(f" ส่วนใช้ประโยชน์จาก{MINERAL} เช่น นำ")
        rock_name, rock_product = rock_half.removeprefix(f"ใช้ประโยชน์จาก{ROCK} เช่น นำ").split("มาทำ", 1)
        mineral_name, mineral_product = mineral_half.split("มาทำ", 1)
        assert kind_of[rock_name] == ROCK and kind_of[mineral_name] == MINERAL, (seed, answer)
        assert made_of[rock_name] == rock_product and made_of[mineral_name] == mineral_product


def test_the_rock_mineral_sets_join_the_legacy_unit():
    """``ป.6/2`` was partial; its new stages sit beside ``geo.rock_uses``, not apart from it."""
    units = {SCIENCE_PLACEMENTS[key].unit for key in INDICATORS["ว 3.2 ป.6/2"]}
    assert units == {SCIENCE_PLACEMENTS["geo.rock_uses"].unit}


def test_each_fossil_model_and_find_answers_one_way():
    for field in ("activity", "fossil", "forms"):
        assert len({getattr(model, field) for model in MODELS}) == len(MODELS), field
    for field in ("fossils", "environment"):
        assert len({getattr(find, field) for find in FINDS}) == len(FINDS), field


def test_every_wind_effect_answer_reaches_living_things_and_the_environment():
    for seed in range(SEEDS):
        question = generate("geo.local_wind_foundation", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        wind = next(wind for wind in WINDS if f"อธิบาย{wind.name} " in stem)
        assert answer == f"ต่อสิ่งมีชีวิต: {wind.on_living} / ต่อสิ่งแวดล้อม: {wind.on_environment}"


def test_the_wind_comparison_holds_all_three_and_wrongs_swap_two():
    for field in ("name", "forms", "on_living", "on_environment"):
        assert len({getattr(wind, field) for wind in WINDS}) == len(WINDS), field
    forms = {wind.name: wind.forms for wind in WINDS}
    for seed in range(SEEDS):
        question = generate("geo.local_wind_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        parts = answer.split(" / ")
        assert sorted(part.split(": ", 1)[0] for part in parts) == sorted(forms)
        for part in parts:
            name, form = part.split(": ", 1)
            assert forms[name] == form, (seed, part)
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)  # one swap, or two combined


def test_the_season_answer_is_re_derived_from_the_wind_on_its_row():
    """``ป.6/5`` explains a season from collected data; read the row back."""
    by_wind = {season.wind: season for season in SEASONS}
    for seed in range(2000):
        rows = season_record(Random(seed))
        assert sorted(season.name for season, *_ in rows) == sorted(s.name for s in SEASONS)
        rains = {season.name: rain for season, _, rain, _ in rows}
        assert rains["ฤดูฝน"] > rains["ฤดูร้อน"] > rains["ฤดูหนาว"], rows
    for seed in range(SEEDS):
        question = generate("geo.monsoon_season_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้ ")[0]
        wind_of = {}
        for row in record.split(" / "):
            month, rest = row.split(": ", 1)
            wind_of[month] = next(wind for wind in by_wind if rest.startswith(wind + " ปริมาณฝน"))
        asked = stem.split(" จากข้อมูลนี้ ")[1]
        if asked.startswith("เดือน") and "อยู่ในฤดูใด" in asked:
            month = asked.removeprefix("เดือน").split("อยู่ในฤดูใด")[0]
            season = by_wind[wind_of[month]]
            assert answer == f"{season.name} เพราะ{season.because}", (seed, answer)
        else:
            wind = asked.removeprefix("เดือนใดได้รับผลจาก")
            assert answer == "เดือน" + next(m for m, w in wind_of.items() if w == wind)


def test_every_hazard_answer_places_all_five_and_wrongs_swap_two():
    """``ป.6/6`` names five hazards under one verb, so every answer places all five."""
    for field in ("name", "description", "sign"):
        assert len({getattr(hazard, field) for hazard in HAZARDS}) == len(HAZARDS), field
    for seed in range(SEEDS):
        question = generate("geo.natural_hazard_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        listing = stem.split(" — ", 1)[1].split(" ข้อใดจับคู่")[0]
        described = dict(item.split(". ", 1) for item in listing.split(" / "))
        parts = answer.split(" / ")
        assert [part.split(" → ")[0] for part in parts] == [hazard.name for hazard in HAZARDS]
        for part, hazard in zip(parts, HAZARDS):
            assert described[part.split(" → ")[1]] == hazard.description, (seed, part)
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)  # one swap, or two combined


def test_every_safety_answer_proposes_both_halves_for_its_own_hazard():
    """``ป.6/7`` names monitoring and safe conduct; both must fit the case."""
    for field in ("hazard", "situation", "monitor", "act"):
        assert len({getattr(plan, field) for plan in PLANS}) == len(PLANS), field
    for seed in range(SEEDS):
        question = generate("geo.hazard_safety_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        plan = next(plan for plan in PLANS if plan.situation in stem)
        assert plan.monitor in answer and plan.act in answer, (seed, answer)
        for wrong in _texts(question):
            if wrong != answer:
                assert not (plan.monitor in wrong and plan.act in wrong), (seed, wrong)


def test_the_greenhouse_answer_is_re_derived_from_the_jar_readings():
    """``ป.6/8`` names the phenomenon and its effect; the warmer jar is read back."""
    for seed in range(2000):
        _, covered_end, open_end = jar_readings(Random(seed))
        assert covered_end - open_end >= 3
    for seed in range(SEEDS):
        question = generate("geo.greenhouse_effect_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        temps = {jar: int(temp) for jar, temp in re.findall(r"โหล (\S) (\d+) องศาเซลเซียส", stem)}
        warmer = max(temps, key=temps.get)
        assert f"ปิดปากโหล {warmer} ด้วยแผ่นพลาสติกใส" in stem, (seed, stem)
        assert f"โหล {warmer} จึงร้อนกว่า" in answer, (seed, answer)
        assert MECHANISM in answer and any(effect in answer for effect in GREENHOUSE_EFFECTS)


def test_each_greenhouse_need_names_a_practice_from_its_own_table():
    practices = {care.practice for care in ACTION_CARE}
    assert {need.practice for need in ACTION_NEEDS} <= practices
    assert len({need.practice for need in ACTION_NEEDS}) == len(ACTION_NEEDS)
    assert len({care.reason for care in ACTION_CARE}) == len(ACTION_CARE)


def test_every_layer_answer_places_all_five_and_wrongs_swap_two():
    """``ม.1/1`` compares every layer's benefit, so every answer places all five."""
    for field in ("name", "span", "trend", "benefit"):
        assert len({getattr(layer, field) for layer in ATMOSPHERE_LAYERS}) == len(ATMOSPHERE_LAYERS), field
    for seed in range(SEEDS):
        question = generate("geo.atmosphere_layers_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        listing = stem.split(" — ", 1)[1].split(" ข้อใดเปรียบเทียบ")[0]
        described = dict(item.split(". ", 1) for item in listing.split(" / "))
        parts = answer.split(" / ")
        for part, layer in zip(parts, ATMOSPHERE_LAYERS):
            name, letter = part.split(" → ")
            assert name == layer.name and described[letter] == layer.benefit, (seed, part)
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)  # one swap, or two combined


def test_the_lowest_humidity_is_read_back_from_the_day_record():
    """``ม.1/2`` explains from collected data; the warmest row must be the driest."""
    for seed in range(2000):
        rows = day_record(Random(seed))
        temps = [temp for _, temp, _ in rows]
        assert temps.count(max(temps)) == 1, rows
        assert max(rows, key=lambda row: row[1]) == min(rows, key=lambda row: row[2])
    for seed in range(SEEDS):
        question = generate("geo.weather_factors_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        if "ความชื้นสัมพัทธ์ต่ำที่สุด" in stem:
            readings = re.findall(r"(\d\d:\d\d) อุณหภูมิ (\d+) องศาเซลเซียส ความชื้นสัมพัทธ์ (\d+) %", stem)
            driest = min(readings, key=lambda row: int(row[2]))[0]
            assert answer.startswith(driest + " "), (seed, answer)
        else:
            values = dict(re.findall(r"สถานี (\S) (\d+) เฮกโตพาสคัล", stem))
            high = max(values, key=lambda k: int(values[k]))
            low = min(values, key=lambda k: int(values[k]))
            assert answer.startswith(f"จากสถานี {high} ไปสถานี {low} "), (seed, answer)


def test_the_storm_comparison_states_both_storms_formation_and_effects():
    """``ม.1/3`` compares two storms on formation and effects: every answer holds all four."""
    for seed in range(SEEDS):
        question = generate("geo.storms_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        if "ได้ถูกต้องทั้งหมด" not in _stem(question):
            thunder, cyclone = (storm.name for storm in STORMS)
            assert answer.index(thunder) < answer.index(cyclone), (seed, answer)
            continue
        for storm in STORMS:
            assert f"{storm.name}: เกิดจาก{storm.forms} ผลคือ{storm.effects}" in answer
        for wrong in _texts(question):
            if wrong != answer:
                assert not all(f"{s.name}: เกิดจาก{s.forms} ผลคือ{s.effects}" in wrong for s in STORMS)
    assert len({case.practice for case in STORM_CASES}) == len(STORM_CASES)


def test_the_forecast_follows_the_trends_in_the_record():
    """``ม.1/4`` forecasts from data: falling pressure with rising humidity means rain."""
    assert len({i.name for i in INSTRUMENTS}) == len({i.measures for i in INSTRUMENTS}) == len(INSTRUMENTS)
    assert len(set(FORECAST_STEPS)) == len(FORECAST_STEPS)
    for seed in range(2000):
        outcome, days = forecast_record(Random(seed))
        pressures = [p for _, p, _, _ in days]
        humidities = [h for _, _, h, _ in days]
        if outcome == RAIN:
            assert pressures == sorted(pressures, reverse=True) and humidities == sorted(humidities)
        else:
            assert outcome == CLEAR
            assert pressures == sorted(pressures) and humidities == sorted(humidities, reverse=True)
        assert len(set(pressures)) == 3 and len(set(humidities)) == 3
    for seed in range(SEEDS):
        question = generate("geo.weather_forecast_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        pressures = [int(p) for p in re.findall(r"ความกดอากาศ (\d+) เฮกโตพาสคัล", stem)]
        expected = RAIN if pressures[0] > pressures[-1] else CLEAR
        assert answer.startswith(expected + " เพราะ"), (seed, answer)


def test_every_forecast_answer_proposes_conduct_and_use_for_its_own_forecast():
    for seed in range(SEEDS):
        question = generate("geo.forecast_use_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        plan = next(plan for plan in FORECAST_PLANS if plan.situation in stem)
        assert plan.conduct in answer and plan.use in answer, (seed, answer)
        for wrong in _texts(question):
            if wrong != answer:
                assert not (plan.conduct in wrong and plan.use in wrong), (seed, wrong)


def test_the_climate_trend_is_read_back_from_the_record():
    """``ม.1/6`` states the situation the data shows; the numbers decide its direction."""
    for series in SERIES:
        for seed in range(500):
            values = [value for _, value in climate_record(Random(seed), series)]
            assert values == sorted(values, reverse=not series.rising), (series.measure, values)
            assert len(set(values)) == len(values)
    for seed in range(SEEDS):
        question = generate("geo.climate_change_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        series = next(series for series in SERIES if series.measure in stem)
        record = stem.split(" — ", 1)[1].split(" จากข้อมูลนี้")[0]
        values = [float(part.split(": ")[1]) for part in record.split(" / ")]
        rising = values[-1] > values[0]
        assert rising == series.rising
        assert answer == f"สถานการณ์: {series.situation} / ผลกระทบ: {series.effect}"


def test_each_climate_need_names_a_practice_from_its_own_table():
    practices = {care.practice for care in CLIMATE_CARE}
    assert {need.practice for need in CLIMATE_NEEDS} <= practices
    assert len({need.practice for need in CLIMATE_NEEDS}) == len(CLIMATE_NEEDS)
    assert len({care.reason for care in CLIMATE_CARE}) == len(CLIMATE_CARE)


def test_the_emission_answer_is_re_derived_from_the_table():
    """``ม.2/1`` explains effects from collected data; the largest emitter is read back."""
    for seed in range(2000):
        rows = emissions_record(Random(seed))
        order = [fuel.name for fuel, *_ in sorted(rows, key=lambda row: -row[1])]
        assert order == [fuel.name for fuel in FUELS], rows
    for seed in range(SEEDS):
        question = generate("geo.fossil_fuel_foundation", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        found = re.findall(r"(\S+): คาร์บอนไดออกไซด์ (\d+) หน่วย ซัลเฟอร์ไดออกไซด์ (\d+) หน่วย", stem)
        column = 1 if "แก๊สคาร์บอนไดออกไซด์ได้ถูกต้อง" in stem else 2
        worst = max(found, key=lambda row: int(row[column]))[0]
        assert answer.startswith(worst + "ปล่อยมากที่สุด และ"), (seed, answer)


def test_the_fuel_comparison_states_all_nine_and_wrongs_swap_one_aspect():
    for field in ("forms", "property", "use"):
        assert len({getattr(fuel, field) for fuel in FUELS}) == len(FUELS), field
    for seed in range(SEEDS):
        question = generate("geo.fossil_fuel_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        if "ทั้งหมด" in _stem(question) and "ของ" in _stem(question) and " — " not in answer:
            # One fuel: its own three aspects; every wrong borrows one from another fuel.
            fuel = next(f for f in FUELS if f"ของ{f.name}ได้" in _stem(question))
            assert answer == f"การเกิด: {fuel.forms}; สมบัติ: {fuel.property}; การใช้ประโยชน์: {fuel.use}"
            for wrong in _texts(question):
                if wrong != answer:
                    own = sum(aspect in wrong for aspect in (fuel.forms, fuel.property, fuel.use))
                    assert own == 2, wrong
            continue
        for fuel in FUELS:
            assert (f"{fuel.name} — การเกิด: {fuel.forms}; สมบัติ: {fuel.property}; "
                    f"การใช้ประโยชน์: {fuel.use}") in answer
        wrongs = [choice for choice in _texts(question) if choice != answer]
        assert len(wrongs) == 3


def test_each_fuel_need_names_a_practice_from_its_own_table():
    practices = {care.practice for care in FUEL_CARE}
    assert {need.practice for need in FUEL_NEEDS} == practices
    assert len({care.reason for care in FUEL_CARE}) == len(FUEL_CARE)


def test_every_locality_suits_one_energy_and_every_energy_has_a_locality():
    names = [energy.name for energy in ENERGIES]
    assert sorted(place.energy for place in LOCALITIES) == sorted(names)
    assert len({energy.summary for energy in ENERGIES}) == len(ENERGIES)


def test_every_renewable_answer_places_all_five_and_wrongs_swap_two():
    for seed in range(SEEDS):
        question = generate("geo.renewable_energy_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        listing = stem.split(" — ", 1)[1].split(" ข้อใดเปรียบเทียบ")[0]
        letters = re.findall(r"(?:^| / )(\S)\. ข้อดี", listing)
        summaries = re.split(r"(?:^| / )\S\. ", listing)[1:]
        described = dict(zip(letters, summaries))
        parts = answer.split(" / ")
        for part, energy in zip(parts, ENERGIES):
            name, letter = part.split(" → ")
            assert name == energy.name and described[letter] == energy.summary, (seed, part)
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (seed, wrong)  # one swap, or two combined


def test_the_layer_is_read_back_from_the_table():
    """``ม.2/4`` explains the interior from collected data; densities keep the real order."""
    for seed in range(2000):
        rows = layer_table(Random(seed))
        by_density = [shell.name for shell, _ in sorted(rows, key=lambda row: row[1])]
        assert by_density == [shell.name for shell in SHELLS]
    for seed in range(SEEDS):
        question = generate("geo.earth_interior_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        asked = stem.rsplit("ชั้น ", 1)[1].split(" ")[0]
        row = stem.split(f"ชั้น {asked}: ", 1)[1].split(" / ")[0]
        shell = next(shell for shell in SHELLS if f"ความลึก {shell.depth} ธาตุหลัก {shell.elements}" in row)
        assert answer == shell.name, (seed, answer)


def test_every_process_answer_places_all_three_against_its_model():
    for field in ("name", "means", "model"):
        assert len({getattr(process, field) for process in PROCESSES}) == len(PROCESSES), field
    examples = [example for process in PROCESSES for example in process.examples]
    assert len(set(examples)) == len(examples)
    for seed in range(SEEDS):
        question = generate("geo.surface_processes_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" ข้อใดอธิบาย")[0]
        model_of = dict(part.removeprefix("แบบจำลอง ").split(": ", 1) for part in record.split(" / "))
        parts = answer.split(" / ")
        assert len(parts) == 3
        for part in parts:
            letter, name = part.removeprefix("แบบจำลอง ").split(" → ")
            process = next(p for p in PROCESSES if p.name == name)
            assert model_of[letter] in (process.model, *MORE_MODELS[name])
        for wrong in _texts(question):
            if wrong != answer:
                # A swap of two, or a rotation that misplaces all three.
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 3), (seed, wrong)


def test_every_soil_case_differs_in_exactly_its_own_factor():
    assert sorted(cause.factor for cause in CAUSES) == sorted(FACTORS)
    assert len({horizon.description for horizon in HORIZONS}) == len(HORIZONS)
    for seed in range(SEEDS):
        question = generate("geo.soil_profile_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        listing = stem.split(" — ", 1)[1].split(" ข้อใดอธิบาย")[0]
        described = dict(item.split(". ", 1) for item in listing.split(" / "))
        for part, horizon in zip(answer.split(" / "), HORIZONS):
            name, letter = part.split(" → ")
            assert name == horizon.name and described[letter] == horizon.description


def test_the_soil_use_is_re_derived_from_the_test_record():
    """``ม.2/7`` proposes a use from soil data: pH band and texture decide the profile."""
    assert len({tool.tool for tool in TOOLS}) == len({tool.property for tool in TOOLS}) == len(TOOLS)
    for seed in range(SEEDS):
        question = generate("geo.soil_property_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        ph = float(re.search(r"pH (\d\.\d)", stem).group(1))
        texture = re.search(r"เนื้อดิน: (\S+)", stem).group(1)
        matches = [profile for profile in PROFILES
                   if profile.ph[0] <= ph <= profile.ph[1] and profile.texture == texture]
        assert len(matches) == 1 and answer == matches[0].use, (seed, ph, texture, answer)


def test_every_water_source_answer_explains_both_sources_correctly():
    for seed in range(SEEDS):
        question = generate("geo.water_source_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        if "ได้ถูกต้อง" in _stem(question) and "ปัจจัยและกระบวนการ" not in _stem(question):
            # One source: its true account, never the other's.
            surface = "แหล่งน้ำผิวดินจาก" in _stem(question)
            assert answer == (SURFACE_TRUE if surface else GROUND_TRUE)
            continue
        assert SURFACE_TRUE in answer and GROUND_TRUE in answer
        for wrong in _texts(question):
            if wrong != answer:
                assert not (SURFACE_TRUE in wrong and GROUND_TRUE in wrong)


def test_the_water_use_model_is_read_back_and_agriculture_leads():
    for seed in range(2000):
        parts = water_model(Random(seed))
        assert sum(parts.values()) == 20 and min(parts.values()) >= 1
        assert max(parts, key=parts.get) == AGRICULTURE
        assert len(set(parts.values())) == 4, parts
    for seed in range(SEEDS):
        question = generate("geo.water_use_model_foundation", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        record = stem.split(" — ", 1)[1].split(" จากแบบจำลองนี้")[0]
        counts = {part.rsplit(" ", 2)[0]: int(part.rsplit(" ", 2)[1]) for part in record.split(" / ")}
        ranked = sorted(counts, key=counts.get, reverse=True)
        if "อันดับสอง" in answer:
            assert answer == f"{ranked[1]}ใช้น้ำมากเป็นอันดับสอง รองจาก{ranked[0]}", (seed, counts)
        else:
            assert answer.startswith(ranked[0] + "ใช้น้ำมากที่สุด"), (seed, counts)


def test_each_water_need_names_a_practice_from_its_own_table():
    assert {need.practice for need in WATER_NEEDS} == {care.practice for care in WATER_CARE}
    assert len({care.reason for care in WATER_CARE}) == len(WATER_CARE)


def _check_matching(key: str, names: list[str], descriptions: list[str], marker: str):
    lookup = dict(zip(names, descriptions))
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        listing = stem.split(" — ", 1)[1].split(marker)[0]
        described = dict(item.split(". ", 1) for item in listing.split(" / "))
        parts = answer.split(" / ")
        assert [part.split(" → ")[0] for part in parts] == names
        for part in parts:
            name, letter = part.split(" → ")
            assert described[letter] == lookup[name], (key, seed, part)
        for wrong in _texts(question):
            if wrong != answer:
                differing = [a for a, b in zip(parts, wrong.split(" / ")) if a != b]
                assert len(differing) in (2, 4), (key, seed, wrong)  # one swap, or two combined


def test_the_five_part_matching_sets_place_every_item():
    _check_matching("geo.surface_hazard_fluency", [h.name for h in SURFACE_HAZARDS],
                    [h.description for h in SURFACE_HAZARDS], " ข้อใดจับคู่")
    _check_matching("geo.earth_layers_fluency", [layer.name for layer in PHYSICAL_LAYERS],
                    [layer.property for layer in PHYSICAL_LAYERS], " ข้อใดจับคู่")


def test_the_seafloor_answer_is_re_derived_from_the_ages():
    """``ม.6/2``: ages rise evenly both ways, and the rate is distance over age."""
    for seed in range(2000):
        rate, rows = seafloor_record(Random(seed))
        assert all(distance == age * rate for distance, age in rows), rows
    for seed in range(SEEDS):
        question = generate("geo.plate_evidence_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        rows = re.findall(r"ห่างไปทาง(\S+) (\d+) กิโลเมตร อายุ (\d+) ล้านปี", stem)
        west = [(int(d), int(a)) for side, d, a in rows if side == "ตะวันตก"]
        east = [(int(d), int(a)) for side, d, a in rows if side == "ตะวันออก"]
        assert west == east
        if "กี่กิโลเมตรต่อล้านปี" in stem:
            assert answer == f"{west[0][0] // west[0][1]} กิโลเมตรต่อล้านปี"
        else:
            assert answer == SPREADING


def test_every_boundary_answer_describes_all_three_patterns():
    for field in ("name", "motion", "example"):
        assert len({getattr(b, field) for b in BOUNDARIES}) == len(BOUNDARIES), field
    for seed in range(SEEDS):
        question = generate("geo.plate_boundary_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        for boundary in BOUNDARIES:
            assert any(f"{boundary.name}: {motion}" in answer
                       for motion in (boundary.motion, *MORE_MOTIONS[boundary.name]))


def test_every_hazard_explanation_states_each_part_and_wrongs_falsify_one():
    keys = {"ภูเขาไฟระเบิด": "geo.volcano", "แผ่นดินไหว": "geo.earthquake", "สึนามิ": "geo.tsunami"}
    for hazard, prefix in keys.items():
        parts = HAZARD_EXPLANATIONS[hazard]
        assert all(part.true != part.false for part in parts)
        for seed in range(SEEDS):
            question = generate(prefix + "_fluency", Random(seed))
            answer = _texts(question)[question.answer]
            trues = {p.label: (p.true, *HAZARD_MORE_TRUES[hazard, p.label]) for p in parts}
            falses = {p.label: (p.false, *HAZARD_MORE_FALSES[hazard, p.label]) for p in parts}
            if "ทั้งหมด" not in _stem(question):
                # One part: one of its true readings against its false ones.
                part = next(p for p in parts if f"อธิบาย{p.label}ของ" in _stem(question))
                assert answer in trues[part.label]
                assert {t for t in _texts(question) if t != answer} <= set(falses[part.label])
                continue
            chunks = dict(chunk.split(": ", 1) for chunk in answer.split(" / "))
            assert all(chunks[p.label] in trues[p.label] for p in parts), answer
            for wrong in _texts(question):
                if wrong != answer:
                    # One authored slip, or two when the convergence breaker
                    # combines them (so the answer is not the choice all agree on).
                    got = dict(chunk.split(": ", 1) for chunk in wrong.split(" / "))
                    falsified = [p for p in parts if got[p.label] in falses[p.label]]
                    assert 1 <= len(falsified) <= 2, (hazard, seed, wrong)


def test_every_hazard_plan_fits_its_own_hazard_in_both_halves():
    keys = {"ภูเขาไฟระเบิด": "geo.volcano", "แผ่นดินไหว": "geo.earthquake", "สึนามิ": "geo.tsunami"}
    for field in ("monitor", "conduct"):
        assert len({getattr(plan, field) for plan in HAZARD_PLANS.values()}) == 3
    for hazard, prefix in keys.items():
        plan = HAZARD_PLANS[hazard]
        for seed in range(SEEDS):
            question = generate(prefix + "_foundation", Random(seed))
            stem, answer = _stem(question), _texts(question)[question.answer]
            assert any(case in stem for case in HAZARD_CASES[hazard])
            monitors = (plan.monitor, HAZARD_MORE_PLAN_LINES[hazard][0])
            conducts = (plan.conduct, HAZARD_MORE_PLAN_LINES[hazard][1])
            assert any(m in answer for m in monitors) and any(c in answer for c in conducts)
            for wrong in _texts(question):
                if wrong != answer:
                    assert not (any(m in wrong for m in monitors) and any(c in wrong for c in conducts))


def _one_part_ok(question, parts) -> bool:
    """parts_item's one-part mode: the stem names one part, the answer is its
    true reading and every wrong one of its own false readings."""
    from otk.sets._support.science_wave_c24 import MORE_PART_FALSES
    stem = _stem(question)
    if "เฉพาะเรื่อง “" not in stem:
        return False
    label = stem.split("เฉพาะเรื่อง “")[1].split("”")[0]
    part = next(p for p in parts if p.label == label)
    texts = _texts(question)
    falses = {part.false, *MORE_PART_FALSES.get(part.false, ())}
    assert len(falses) >= 3, label
    assert texts[question.answer] == part.true, (label, texts)
    assert {t for t in texts if t != part.true} <= falses, (label, texts)
    return True


def _parts_line(parts, false_index=None):
    return " / ".join(f"{p.label}: {p.false if i == false_index else p.true}"
                      for i, p in enumerate(parts))


def _one_false_lines(parts):
    """Every line with exactly one part falsified, by any of its false readings."""
    from otk.sets._support.science_wave_c24 import MORE_PART_FALSES
    lines = set()
    for index, part in enumerate(parts):
        for false in (part.false, *MORE_PART_FALSES.get(part.false, ())):
            lines.add(" / ".join(f"{p.label}: {false if i == index else p.true}"
                                 for i, p in enumerate(parts)))
    return lines


def _slip_lines(parts):
    """Lines with one part falsified, or two: the convergence breaker combines
    two authored slips so the answer is not the choice every wrong agrees on."""
    from itertools import combinations
    from otk.sets._support.science_wave_c24 import MORE_PART_FALSES
    falses = [(part.false, *MORE_PART_FALSES.get(part.false, ())) for part in parts]
    lines = set(_one_false_lines(parts))
    for a, b in combinations(range(len(parts)), 2):
        for fa in falses[a]:
            for fb in falses[b]:
                lines.add(" / ".join(f"{p.label}: {fa if i == a else fb if i == b else p.true}"
                                     for i, p in enumerate(parts)))
    return lines


def test_the_solar_factor_explanation_states_all_four_and_wrongs_falsify_one():
    assert all(part.true != part.false for part in SOLAR_FACTORS)
    for seed in range(SEEDS):
        question = generate("geo.solar_energy_fluency", Random(seed))
        if _one_part_ok(question, SOLAR_FACTORS):
            continue
        texts = _texts(question)
        assert texts[question.answer] == _parts_line(SOLAR_FACTORS)
        wrongs = _slip_lines(SOLAR_FACTORS)
        assert {t for t in texts if t != texts[question.answer]} <= wrongs


def test_the_pressure_cell_is_rederived_from_the_temperature_record():
    for seed in range(SEEDS):
        question = generate("geo.pressure_circulation_fluency", Random(seed))
        stem = _stem(question)
        (first, t1), (second, t2) = re.findall(r"เหนือ(\S+?) (\d+) องศาเซลเซียส", stem)
        assert t1 != t2
        hot, cool = (first, second) if int(t1) > int(t2) else (second, first)
        parts = pressure_parts(hot, cool)
        texts = _texts(question)
        assert texts[question.answer] == _parts_line(parts)
        for wrong in texts:
            if wrong != texts[question.answer]:
                assert wrong in _slip_lines(parts)


def test_the_pressure_chain_is_ordered_from_warming_to_wind():
    for seed in range(SEEDS):
        question = generate("geo.pressure_circulation_foundation", Random(seed))
        stem = _stem(question)
        letter_of = {step: letter for letter, step in re.findall(r"([ก-จ])\. ([^/]+?)(?= / | ข้อใด)", stem)}
        assert _texts(question)[question.answer] == " → ".join(letter_of[step] for step in PRESSURE_CHAIN)


def test_the_coriolis_turn_is_rederived_from_hemisphere_and_heading():
    compass = ["ทิศเหนือ", "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออก", "ทิศตะวันออกเฉียงใต้",
               "ทิศใต้", "ทิศตะวันตกเฉียงใต้", "ทิศตะวันตก", "ทิศตะวันตกเฉียงเหนือ"]
    assert set(AIR_HEADINGS) <= set(compass)
    for seed in range(SEEDS):
        question = generate("geo.coriolis_fluency", Random(seed))
        stem = _stem(question)
        north = "ซีกโลกเหนือ" in stem
        heading = next(h for h in AIR_HEADINGS if f"ไปทาง{h}เป็นระยะทางไกล" in stem)
        turn = compass[(compass.index(heading) + (1 if north else -1)) % 8]
        answer = _texts(question)[question.answer]
        assert answer.startswith(f"เบนไปทาง{'ขวา' if north else 'ซ้าย'} จึงเคลื่อนที่เฉียงไปทาง{turn} ")
        for wrong in _texts(question):
            assert wrong == answer or f"เฉียงไปทาง{turn} " not in wrong


def test_each_latitude_answer_pairs_its_own_circulation_and_climate():
    assert len({belt.circulation for belt in BELTS}) == len({belt.climate for belt in BELTS}) == 4
    for seed in range(SEEDS):
        question = generate("geo.latitude_circulation_fluency", Random(seed))
        belt = next(b for b in BELTS if f"ละติจูด {b.latitude} " in _stem(question))
        answer = _texts(question)[question.answer]
        assert belt.circulation in answer and belt.climate in answer
        for wrong in _texts(question):
            if wrong != answer:
                assert not (belt.circulation in wrong and belt.climate in wrong)


def test_the_surface_wind_matches_band_and_hemisphere():
    assert WIND_BELTS[0].north.endswith("ตะวันออกเฉียงเหนือ") and WIND_BELTS[1].north.endswith("ตะวันตกเฉียงใต้")
    for seed in range(SEEDS):
        question = generate("geo.latitude_circulation_foundation", Random(seed))
        stem = _stem(question)
        belt = next(b for b in WIND_BELTS if f"ละติจูด {b.band}" in stem)
        source = belt.north if stem.endswith("เหนือ คือลมใด") else belt.south
        assert _texts(question)[question.answer] == f"{belt.name}ใน{belt.cell} พัดมาจาก{source}"


def test_a_current_is_warm_and_poleward_exactly_on_an_east_coast():
    for current in CURRENTS:
        assert current.warm == current.coast.startswith("ชายฝั่งตะวันออก")
    for seed in range(SEEDS):
        question = generate("geo.ocean_currents_foundation", Random(seed))
        east = "เลียบชายฝั่งตะวันออก" in _stem(question)
        expected = ("กระแสน้ำอุ่น ไหลจากเขตศูนย์สูตรไปทางขั้วโลก" if east
                    else "กระแสน้ำเย็น ไหลจากขั้วโลกมาทางเขตศูนย์สูตร")
        assert _texts(question)[question.answer] == expected


def test_parts_answers_span_every_part_and_wrongs_falsify_exactly_one():
    cases = [("geo.ocean_currents_fluency", lambda stem: OCEAN_PARTS),
             ("geo.circulation_effects_fluency",
              lambda stem: next(CIRCULATION_EFFECTS[k] for k, text in CIRCULATION_PHENOMENA.items() if text in stem))]
    for key, parts_for in cases:
        for seed in range(SEEDS):
            question = generate(key, Random(seed))
            parts = parts_for(_stem(question))
            if _one_part_ok(question, parts):
                continue
            texts = _texts(question)
            assert texts[question.answer] == _parts_line(parts)
            for wrong in texts:
                if wrong != texts[question.answer]:
                    assert wrong in _slip_lines(parts)


def test_a_circulation_effect_answer_is_never_offered_twice():
    for seed in range(SEEDS):
        question = generate("geo.circulation_effects_foundation", Random(seed))
        stem = _stem(question)
        phenomenon = next(k for k, text in CIRCULATION_PHENOMENA.items() if text in stem)
        aspect = next(i for i, name in enumerate(("ภูมิอากาศ", "ลมฟ้าอากาศ", "สิ่งมีชีวิต", "สิ่งแวดล้อม"))
                      if stem.endswith(f"ต่อ{name}"))
        assert _texts(question)[question.answer] == CIRCULATION_EFFECTS[phenomenon][aspect].true


def test_each_climate_case_is_answered_by_its_own_practice():
    assert len({activity.practice for activity in CLIMATE_ACTIVITIES}) == len(CLIMATE_ACTIVITIES)
    for seed in range(SEEDS):
        question = generate("geo.climate_factors_foundation", Random(seed))
        stem = _stem(question)
        activity = next(a for a in CLIMATE_ACTIVITIES if any(case in stem for case in a.cases))
        assert _texts(question)[question.answer] == activity.practice


def test_climate_factor_answers_are_true_throughout_and_wrongs_falsify_one():
    by_label = {part.label: part for part in CLIMATE_FACTORS}
    for seed in range(SEEDS):
        question = generate("geo.climate_factors_fluency", Random(seed))
        if _one_part_ok(question, CLIMATE_FACTORS):
            continue
        answer = _texts(question)[question.answer]
        labels = [chunk.split(": ", 1)[0] for chunk in answer.split(" / ")]
        assert len(labels) == 4
        parts = tuple(by_label[label] for label in labels)
        assert answer == _parts_line(parts)
        for wrong in _texts(question):
            if wrong != answer:
                assert wrong in _slip_lines(parts)


def test_every_weather_symbol_is_placed_by_its_look():
    look_of = {symbol.meaning: symbol.look for symbol in SYMBOLS}
    for seed in range(SEEDS):
        question = generate("geo.weather_map_foundation", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        for pair in answer.split(" / "):
            meaning, letter = pair.split(" → ")
            assert f"{letter}. {look_of[meaning]}" in stem


def test_each_weather_map_plan_fits_its_own_situation():
    assert len({situation.plan for situation in SITUATIONS}) == len(SITUATIONS)
    for seed in range(SEEDS):
        question = generate("geo.weather_map_fluency", Random(seed))
        stem = _stem(question)
        situation = next(s for s in SITUATIONS if s.shows in stem and s.who in stem)
        assert _texts(question)[question.answer] == situation.plan


def test_wo_three_two_is_complete():
    """Every one of the 52 ``ว 3.2`` indicators holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 3.2 "):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 52, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


def test_wo_three_one_is_complete():
    """Every one of the 26 ``ว 3.1`` indicators holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 3.1 "):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 26, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


def test_every_exploration_fluency_answer_names_all_four_means():
    """``ม.6/10``'s one assessable verb governs four objects, so every answer holds all four."""
    formats = set()
    for seed in range(SEEDS):
        question = generate("astro.space_exploration_fluency", Random(seed))
        choices = _texts(question)
        answer = choices[question.answer]
        for means in (TELESCOPE, SATELLITE, SPACECRAFT, STATION):
            assert means in answer, (seed, means, answer)
        formats.add("→" in answer)
        if "→" not in answer:
            # Each wrong choice falsifies exactly one clause of the answer.
            clauses = answer.split(" ")
            for wrong in choices:
                if wrong != answer:
                    assert wrong.split(" ") != clauses
                    for means in (TELESCOPE, SATELLITE, SPACECRAFT, STATION):
                        assert means in wrong, (seed, means, wrong)
    assert formats == {True, False}


def test_the_exploration_matching_never_moves_the_telescope_job_to_a_platform():
    """An orbiting telescope is a satellite, so that swap could be defended."""
    for seed in range(SEEDS):
        question = generate("astro.space_exploration_fluency", Random(seed))
        for choice in _texts(question):
            if "→" not in choice:
                continue
            first = choice.split(" / ")[0]
            assert first.split(" → ")[1].startswith(TELESCOPE), (seed, choice)


def test_no_band_is_offered_wrong_for_a_phenomenon_it_can_study():
    """Radio dishes do observe forming stars, so they are never the wrong band for them."""
    keys = ("astro.space_exploration_foundation", "astro.space_exploration_fluency")
    for band in BANDS:
        for defensible in DEFENSIBLE.get(band.name, ()):
            for seed in range(SEEDS):
                for key in keys:
                    question = generate(key, Random(seed))
                    if band.reveals not in _stem(question) + " ".join(_texts(question)):
                        continue
                    for choice in _texts(question):
                        assert f"{defensible}ศึกษา{band.reveals}" not in choice, (key, seed)
                        assert f"{band.reveals} → {TELESCOPE}{defensible}" not in choice, (key, seed)
                        if band.reveals in _stem(question):
                            assert choice != defensible, (key, seed)


def test_each_band_and_platform_answers_one_way_only():
    for field in ("name", "reveals", "placed"):
        values = [getattr(band, field) for band in BANDS]
        assert len(set(values)) == len(BANDS), field
    for field in ("name", "role", "job"):
        values = [getattr(platform, field) for platform in PLATFORMS]
        assert len(set(values)) == len(PLATFORMS), field
    for true, false in PLATFORM_CLAUSES.values():
        assert true != false


def test_the_mass_bands_do_not_overlap():
    """An initial mass must pick exactly one road and one remnant."""
    for field in ("mass", "path", "remnant"):
        values = [getattr(track, field) for track in TRACKS]
        assert len(set(values)) == len(TRACKS), field


def test_each_evolution_step_moves_its_properties_its_own_way():
    """Two steps sharing all three directions would give an item two answers."""
    assert len({_properties(change) for change in CHANGES}) == len(CHANGES)
    assert len({change.step for change in CHANGES}) == len(CHANGES)
    for change in CHANGES:
        spans = _properties(change)
        for word in ("รัศมี", "อุณหภูมิผิว", "ความส่องสว่าง"):
            assert word in spans, (change.step, word)


def test_the_origin_answer_links_formation_zoning_and_habitability():
    """``ม.6/8`` names all three under one verb, so one answer carries all three."""
    for word in ("เนบิวลา", "เขตชั้นใน", "เขตชั้นนอก", "ของเหลว"):
        assert word in ORIGIN_SPANNING, word


def test_each_zone_holds_members_of_its_own():
    for field in ("name", "where", "members", "why"):
        values = [getattr(zone, field) for zone in ZONES]
        assert len(set(values)) == len(ZONES), field


def test_the_sun_answer_reaches_structure_wind_and_storm():
    """``ม.6/9``'s first verb governs all three, so its answer holds all three."""
    for word in ("แก่น", "คอโรนา", "ลมสุริยะ", "พายุสุริยะ", "จุดมืด"):
        assert word in SUN_SPANNING, word


def test_the_sun_layers_and_storm_effects_stay_distinct():
    for field in ("name", "where", "what"):
        values = [getattr(layer, field) for layer in LAYERS]
        assert len(set(values)) == len(LAYERS), field
    for field in ("event", "result", "why"):
        values = [getattr(effect, field) for effect in EFFECTS]
        assert len(set(values)) == len(EFFECTS), field


def test_the_formation_answer_reaches_all_three_named_quantities():
    """``ม.6/4`` names ความดัน, อุณหภูมิ and ขนาด together."""
    for word in ("ความดัน", "อุณหภูมิ", "ขนาด"):
        assert word in FORMATION_SPANNING, word


def test_the_formation_table_carries_all_three_quantities_in_every_row():
    """The table is read across as well as down, so no row may omit one."""
    assert len({stage.name for stage in STAGES}) == len(STAGES)
    assert len({stage.what for stage in STAGES}) == len(STAGES)
    assert len({stage.temperature for stage in STAGES}) == len(STAGES)
    for stage in STAGES:
        assert stage.size and stage.pressure and stage.temperature, stage.name


def test_the_spectrum_answer_reaches_colour_temperature_and_spectrum():
    """``ม.6/6`` names all three under one verb, so one answer holds all three."""
    for item in SPECTRAL:
        spans = _spans_three(item)
        assert item.colour in spans and item.temperature in spans
        assert item.kind in spans and item.lines in spans


def test_the_spectral_table_runs_hot_to_cool_with_no_repeats():
    kelvins = [item.kelvin for item in SPECTRAL]
    assert kelvins == sorted(kelvins, reverse=True), kelvins
    for field in ("kind", "colour", "temperature", "lines"):
        values = [getattr(item, field) for item in SPECTRAL]
        assert len(set(values)) == len(SPECTRAL), field


def test_magnitude_runs_backwards_and_five_steps_is_a_hundred():
    """The brightest star is the smallest number, and the scale is pinned."""
    assert FIVE_STEPS == 100
    for field in ("name", "apparent", "absolute"):
        values = [getattr(star, field) for star in STARS]
        assert len(set(values)) == len(STARS), field
    # The two questions must not collapse into the same answer.
    assert (min(STARS, key=lambda star: star.apparent).name
            != min(STARS, key=lambda star: star.absolute).name)


def test_the_brightest_star_answer_is_the_smallest_magnitude():
    looks = min(STARS, key=lambda star: star.apparent).name
    truly = min(STARS, key=lambda star: star.absolute).name
    for seed in range(SEEDS):
        question = generate("astro.star_luminosity_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        if "ปรากฏสว่างที่สุดเมื่อมองจากโลก" in stem:
            assert answer == looks, (seed, answer)
        elif "ความส่องสว่างที่แท้จริงมากที่สุด" in stem:
            assert answer == truly, (seed, answer)


def test_the_universe_answer_reaches_all_four_named_objects():
    """``ม.6/1`` names พลังงาน, สสาร, ขนาด and อุณหภูมิ under one verb."""
    for word in ("พลังงาน", "สสาร", "ขนาด", "อุณหภูมิ"):
        assert word in SPANNING, word


def test_the_evidence_answer_reaches_both_bodies_of_evidence():
    """``ม.6/2`` names the velocity-distance relation and the background."""
    assert HUBBLE in BOTH_EVIDENCE
    assert CMB in BOTH_EVIDENCE


def test_the_galaxy_table_obeys_the_relation_it_asks_the_learner_to_find():
    """Every row is v = H0 d, so the straight line is really in the data."""
    for galaxy in GALAXIES:
        assert galaxy.speed == galaxy.distance * HUBBLE_CONSTANT, galaxy
    distances = [galaxy.distance for galaxy in GALAXIES]
    speeds = [galaxy.speed for galaxy in GALAXIES]
    assert distances == sorted(distances) and len(set(distances)) == len(GALAXIES)
    assert speeds == sorted(speeds) and len(set(speeds)) == len(GALAXIES)


def test_the_timeline_runs_forward_and_cools():
    """A row out of order, or a rise in temperature, would misstate the physics."""
    assert len({epoch.when for epoch in EPOCHS}) == len(EPOCHS)
    assert len({epoch.event for epoch in EPOCHS}) == len(EPOCHS)
    assert len({epoch.temperature for epoch in EPOCHS}) == len(EPOCHS)


def test_each_galaxy_part_holds_something_of_its_own():
    assert len({part.name for part in GALAXY_PARTS}) == len(GALAXY_PARTS)
    assert len({part.where for part in GALAXY_PARTS}) == len(GALAXY_PARTS)
    assert len({part.holds for part in GALAXY_PARTS}) == len(GALAXY_PARTS)


def test_the_season_set_reaches_both_objects_of_its_indicator():
    """``ม.3/2`` names the seasons and the sun's motion under one verb."""
    for item in SEASON_POINTS:
        assert item.season in _spans_both(item)
        assert item.sunrise in _spans_both(item)
    for seed in range(SEEDS):
        question = generate("astro.season_model_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        item = next(one for one in SEASON_POINTS if one.position in _stem(question))
        assert answer == _spans_both(item), (seed, answer)


def test_the_equation_table_states_each_change_once():
    """Two rows describing the same change would give an item two answers."""
    assert len({change for change, _, _ in EQUATION_CASES}) == len(EQUATION_CASES)
    for change, effect, wrongs in EQUATION_CASES:
        assert effect not in wrongs, change
        assert len(set(wrongs)) == len(wrongs) >= 3, change


def test_each_satellite_job_fixes_exactly_one_orbit():
    assert len({orbit.kind for orbit in ORBITS}) == len(ORBITS)
    assert len({orbit.orbit for orbit in ORBITS}) == len(ORBITS)
    assert len({orbit.because for orbit in ORBITS}) == len(ORBITS)


def test_the_mission_record_is_ordered_and_names_distinct_advances():
    assert len({mission.period for mission in MISSIONS}) == len(MISSIONS)
    assert len({mission.project for mission in MISSIONS}) == len(MISSIONS)
    assert len({mission.advance for mission in MISSIONS}) == len(MISSIONS)


def test_the_moon_cycle_never_offers_two_matching_shapes():
    """The two half-moons differ by which way they are heading, so each is unique."""
    assert len({phase.look for phase in CYCLE}) == len(CYCLE)
    assert len({phase.name for phase in CYCLE}) == len(CYCLE)


def test_the_predicted_shape_is_the_next_point_of_the_cycle():
    """Stepping one or two points on must land on the answer, never on the start."""
    looks = [phase.look for phase in CYCLE]
    for seed in range(SEEDS):
        question = generate("astro.moon_shape_cycle_fluency", Random(seed))
        stem, answer = _stem(question), _texts(question)[question.answer]
        here = next(phase for phase in CYCLE if phase.name in stem)
        steps = 1 if " 7 วัน" in stem or " 8 วัน" in stem else 2
        expected = CYCLE[(CYCLE.index(here) + steps) % len(CYCLE)]
        assert answer == expected.look, (seed, stem, answer)
        assert answer in looks


def test_orbital_periods_grow_with_distance_from_the_sun():
    """The comparison rests on the table, so the table has to carry the rule."""
    assert [planet.order for planet in PLANETS] == list(range(1, len(PLANETS) + 1))
    days = [planet.days for planet in PLANETS]
    assert days == sorted(days), days
    assert len(set(period.period for period in PLANETS)) == len(PLANETS)


def test_the_eclipse_set_always_states_both_phenomena():
    """``เปรียบเทียบ`` of two named phenomena is not answered by one alone."""
    for seed in range(SEEDS):
        question = generate("astro.eclipse_fluency", Random(seed))
        answer = _texts(question)[question.answer]
        assert SOLAR in answer and LUNAR in answer, (seed, answer)


def test_no_eclipse_row_can_be_answered_by_its_own_mirror():
    assert len({item.aspect for item in ECLIPSES}) == len(ECLIPSES)
    for item in ECLIPSES:
        assert item.solar != item.lunar
        assert _eclipse_swapped(item) != _eclipse_pair(item)
        assert _eclipse_pair(item) not in item.wrongs
        assert len(set(item.wrongs)) == 2


def test_each_gift_of_the_sun_has_one_reason_and_one_consequence():
    """Two rows sharing either would give a question two defensible answers."""
    assert len({gift.gift for gift in BENEFITS}) == len(BENEFITS)
    assert len({gift.because for gift in BENEFITS}) == len(BENEFITS)
    assert len({gift.without for gift in BENEFITS}) == len(BENEFITS)


def test_the_moonrise_record_always_runs_later_night_by_night():
    """The moon rises later each night; an unordered record would be untrue."""
    for seed in range(2000):
        times = _moonrise_times(Random(seed))
        assert len(times) == 4, (seed, times)
        assert times == sorted(times), (seed, times)
        assert len(set(times)) == 4, (seed, times)


def test_the_unrecorded_objects_are_never_in_the_night_table():
    """A wrong choice must be absent from the record, not merely unlucky."""
    assert not set(UNRECORDED) & set(NIGHT_ONLY)
    assert "ดวงจันทร์" not in NIGHT_ONLY
    assert "ดวงอาทิตย์" not in NIGHT_ONLY


# ── the two data-reading sets answer from their own stems ─────────────────────

def test_the_sky_record_names_the_moon_on_both_lines_and_the_sun_on_one():
    """The "both periods" answer has to be the only object on both lines."""
    for seed in range(SEEDS):
        question = generate("astro.day_night_sky_fluency", Random(seed))
        stem = _stem(question)
        day, night = stem.split(" / ")
        day = day.split("กลางวัน:")[1]
        assert "ดวงจันทร์" in day and "ดวงจันทร์" in night
        assert "ดวงอาทิตย์" in day and "ดวงอาทิตย์" not in night
        for star in NIGHT_ONLY:
            assert star not in day


def test_the_sky_record_answer_is_present_in_the_period_it_names():
    for seed in range(SEEDS):
        question = generate("astro.day_night_sky_fluency", Random(seed))
        stem = _stem(question)
        record, asked = stem.split("จากบันทึกนี้")
        day, night = record.split(" / ")
        answer = _texts(question)[question.answer]
        if "ทั้งในเวลากลางวัน" in asked:
            assert answer in day and answer in night
        elif "เฉพาะในเวลากลางคืน" in asked:
            assert answer in night and answer not in day
        else:
            assert answer in day and answer not in night


SHADOW = re.compile(r"(\d\d:\d\d) [^/]*?ความยาวเงาของเสา (\d+) เซนติเมตร")


def test_the_shadow_answer_is_re_derived_from_the_table_in_the_stem():
    """Parse the printed table back out and check the answer against it."""
    seen = set()
    for seed in range(SEEDS):
        question = generate("astro.sun_path_pattern_fluency", Random(seed))
        stem = _stem(question)
        table = {time: int(length) for time, length in SHADOW.findall(stem)}
        assert list(table) == list(SUN_TIMES), (seed, table)
        answer = _texts(question)[question.answer]
        if "ยาวที่สุด" in stem:
            seen.add("longest")
            assert answer == max(table, key=table.get), (seed, table, answer)
        elif "สั้นที่สุด" in stem:
            seen.add("shortest")
            assert answer == min(table, key=table.get), (seed, table, answer)
    assert seen == {"longest", "shortest"}


def test_the_shadow_table_describes_a_day_that_could_happen():
    """Longest at the ends, shortest at noon, and no two readings equal.

    Drawn independently, 07:00 could come out shorter than 09:00, and the record
    would then describe a day the sun does not have.
    """
    for seed in range(2000):
        lengths = _shadow_lengths(Random(seed))
        assert len(set(lengths)) == 5, (seed, lengths)
        morning, mid_morning, noon, mid_afternoon, afternoon = lengths
        assert morning > mid_morning > noon, (seed, lengths)
        assert noon < mid_afternoon < afternoon, (seed, lengths)


def test_the_sun_direction_answer_matches_the_row_it_asks_about():
    asked = 0
    for seed in range(SEEDS):
        question = generate("astro.sun_path_pattern_fluency", Random(seed))
        stem = _stem(question)
        match = re.search(r"ในเวลา (\d\d:\d\d) ดวงอาทิตย์อยู่ทางทิศใด", stem)
        if match is None:
            continue
        asked += 1
        row = re.search(rf"{match.group(1)} ดวงอาทิตย์อยู่ทาง(\S+) ", stem)
        answer = _texts(question)[question.answer]
        assert answer == row.group(1), (seed, stem, answer)
    assert asked, "no draw asked for a direction"

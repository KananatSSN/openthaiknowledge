"""Acceptance gate for Phase 5 Wave D — uncovered compulsory science, ``ว 2``.

Slice 1 delivers ``ว 2.1 ป.1/1``, ``ป.1/2`` and ``ป.2/1``, materials and water absorption;
slice 2 adds ``ป.2/2``-``ป.2/4``, mixed materials, choosing and reusing materials;
slice 3 adds ``ป.3/1`` and ``ป.3/2``, objects from small parts and materials heated or cooled;
slice 4 adds ``ป.4/1`` and ``ป.4/2``, physical properties tested and discussed;
slice 5 adds ``ป.4/3`` and ``ป.4/4``, the three states observed and measured;
slice 6 adds ``ป.5/2``-``ป.5/4``, dissolving, chemical change and reversibility;
slice 7 adds ``ม.1/1``-``ม.1/3``, element classes and using elements;
slice 8 adds ``ม.1/6`` and ``ม.1/10``, measuring substances and heat and change of state;
slice 9 adds ``ม.2/3`` and ``ม.2/4``, separation in use and solubility;
slice 10 adds ``ม.2/5``, ``ม.2/6`` and ``ม.3/1``, concentration, solutions in use and modern materials;
slice 11 adds ``ม.3/2`` and ``ม.3/3``, thrifty use of materials and the rearrangement of atoms;
slice 12 adds ``ม.3/4`` and ``ม.3/5``, conservation of mass and reaction heat;
slice 13 adds ``ม.3/6``-``ม.3/8``, reactions around us, closing ``ว 2.1``;
slice 14 opens ``ว 2.2`` with ``ป.3/1``-``ป.3/4``, forces and magnets;
slice 15 adds ``ป.4/1``-``ป.4/3``, gravity, weight and mass;
slice 16 adds ``ป.5/1``-``ป.5/4``, forces in a line, diagrams, measuring force and friction;
slice 17 adds ``ป.5/5``, ``ป.6/1`` and ``ม.1/1``, friction diagrams, static electricity and air pressure;
slice 18 adds ``ม.2/1``-``ม.2/4``, resultant force and motion, liquid pressure and buoyancy;
slice 19 adds ``ม.2/5``-``ม.2/7``, forces in liquids drawn and friction;
slice 20 adds ``ม.2/8``-``ม.2/11``, friction drawn and used, moments and fields;
slice 21 adds ``ม.2/12``-``ม.2/15``, field-force diagrams, force and distance,
speed and velocity, and displacement diagrams — closing ``ว 2.2`` for ป.1-ม.3;
slice 22 opens ``ว 2.3`` with ``ป.1/1``-``ป.2/2``, sound, light travel, and
seeing, and light safety;
slice 23 adds ``ป.3/1``-``ป.3/3``, energy transformation, generators and
their energy sources, and electricity safety;
slice 24 adds ``ป.4/1``, ``ป.5/1`` and ``ป.5/2``, light media, hearing through
a medium, and pitch;
slice 25 adds ``ป.5/3``-``ป.5/5``, loudness, sound-level measurement, and
noise pollution, closing ``ป.5``;
slice 26 opens ``ป.6`` with ``ป.6/1``-``ป.6/4``, circuit parts, circuit
diagrams, and series cells;
slice 27 closes ``ป.6`` and ``ว 2.3``'s primary grades with ``ป.6/5``-``ป.6/8``,
parallel bulbs and shadows;
slice 28 opens ``ม.1`` with ``ม.1/1``-``ม.1/4``, heat quantity, thermometers,
and thermal expansion;
slice 29 closes ``ม.1`` with ``ม.1/5``-``ม.1/7``, heat equilibrium, heat
transfer modes, and heat-transfer design;
slice 30 opens ``ม.2`` with ``ม.2/1``-``ม.2/3``, work and power, simple
machines, and their benefit;
slice 31 closes ``ม.2`` with ``ม.2/4``-``ม.2/6``, kinetic/potential energy
factors, mechanical energy, and the conservation of energy;
slice 32 closes three ``ม.3`` rows the Phase 3 pilot and Wave A left without
their own three stages — ``ม.3/2``, ``ม.3/3``, and ``ม.3/5`` (the V-I graph,
meter use, and resistor circuit diagrams);
slice 33 closes ``ม.3/6``, ``ม.3/7``, and ``ม.3/9`` (electronic components,
their diagrams, and appliance choice); slice 34 closes three more rows this
wave's own completeness check found still partial — ``ม.3/18``, ``ม.3/20``,
and ``ม.3/21`` (optics diagrams, light meters, and safe brightness) —
completing ``ว 2.3`` end to end from ป.1 through ม.3.
What is checked here is what a reviewer would otherwise have to check by hand:

* the filing follows the indicator's grammar — an evidence clause makes the set
  that carries the record ``exact``, two free verbs make Foundation and Fluency
  both ``exact``, and no Application set is ever ``exact``;
* each indicator holds all three stages, in its own curriculum unit and topic;
* Wave D is a cohort of its own, disjoint from every earlier one, and every set
  not yet approved is on the reviewer's worklist;
* the record-reading sets answer from their own stems, re-derived here.
"""

from __future__ import annotations

import re
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
    SCIENCE_WAVE_D_APPROVED_KEYS,
    SCIENCE_WAVE_D_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.core.registry import REGISTRY
from otk.sets.chemistry.p2.mixed_material import MIXES
from otk.sets.chemistry.p2.material_choice import PURPOSES, REUSES
from otk.sets.chemistry.p3.heating_change import CHANGES, COLDER, HOTTER
from otk.sets.chemistry.p3.object_parts import SETS
from otk.sets.chemistry.p4.material_physical import DESIGNS, comparison
from otk.sets.chemistry.p4.material_physical import MATERIALS as PHYSICAL_MATERIALS
from otk.sets.chemistry.p4.states_matter import STATES, state_parts
from otk.sets.chemistry.p5.chemical_change import ACTIVITIES as CHANGE_ACTIVITIES
from otk.sets.chemistry.p5.reversible_change import IRREVERSIBLE, REVERSIBLE
from otk.sets.chemistry.p5.dissolving import SOLUTES
from otk.sets.chemistry.m1.element_class_group import ELEMENTS, KINDS, TESTS
from otk.sets.chemistry.m1.element_safe_use import GUIDELINES
from otk.sets.chemistry.m1.heat_state_change import CHANGES as STATE_CHANGES
from otk.sets.chemistry.m1.substance_measuring import LIQUIDS
from otk.sets.chemistry.m2.separation_problem import PROBLEMS
from otk.sets.chemistry.m3.modern_material import KIND_PARTS, SAMPLES
from otk.sets.chemistry.m2.concentration import MIXTURES
from otk.sets.chemistry.m3.reaction_model import REACTIONS, count_atoms, model, word_equation
from otk.sets.chemistry.m3.reaction_heat import HEATS
from otk.core import catalog
from otk.sets.chemistry.m3.everyday_reaction import EXPERIMENTS
from otk.sets.chemistry.m3.reaction_impact import IMPACTS
from otk.sets.physics.p3.magnet_sort import ATTRACTED, NOT_ATTRACTED
from otk.sets.physics.p3.force_effect import PUSHES
from otk.sets.physics.p4.gravity_effect import SIGHTINGS
from otk.sets.physics.m1.air_pressure_height import PLACES, pressure_at
from otk.sets.physics.m2.net_force_motion import predict
from otk.sets.physics.m2.field_compare import FIELD_PARTS
from otk.sets.physics.m2.friction_use import PROBLEMS as FRICTION_PROBLEMS
from otk.sets.physics.m2.field_force_diagram import FIELD_DIAGRAM_CASES
from otk.sets.physics.p2.light_safety import LIGHT_PROBLEMS
from otk.sets.physics.p1.sound_source import SOUND_SOURCES
from otk.sets.physics.p3.energy_change import DEVICES, ENERGY_CHANGES
from otk.sets.physics.p3.electricity_safety import ELECTRICITY_PROBLEMS
from otk.sets.physics.p3.generator import POWER_SOURCES
from otk.sets.physics.p4.light_medium import CATEGORY_DESCRIPTIONS, MEDIA
from otk.sets.physics.p5.hearing_medium import HEARING_RECORDS
from otk.sets.physics.p5.noise_pollution import NOISE_PROBLEMS
from otk.sets.physics.p5.sound_level import SOUND_PLACES
from otk.sets.physics.p6.circuit_parts import COMPONENTS
from otk.sets.physics.p6.series_cells_benefit import SERIES_DEVICES
from otk.sets.physics.p6.parallel_bulbs_benefit import BULB_USES
from otk.sets.physics.m1.thermal_expansion_benefit import EXPANSION_PROBLEMS
from otk.sets.physics.m1.heat_transfer_design import DESIGN_PROBLEMS
from otk.sets.physics.m1.heat_equilibrium import HEAT_MIX_COMBOS
from otk.sets.physics.m1.heat_transfer_mode import HEAT_TRANSFER_PARTS
from otk.sets.physics.m2.simple_machine_benefit import MACHINE_USES
from otk.sets.physics.m2.simple_machine import MACHINES
from otk.sets.physics.m2.work_power import WORK_POWER_COMBOS
from otk.sets.physics.m2.energy_conservation import ENERGY_CONVERSIONS
from otk.sets.physics.m2.ke_pe_factor import KE_PE_PARTS
from otk.sets._support.science_wave_d31 import MECHANICAL_ENERGY_COMBOS
from otk.sets._support.science_wave_d32 import VI_GRAPH_COMBOS
from otk.sets.physics.m3.appliance_choice import APPLIANCE_PROBLEMS
from otk.sets.physics.m3.electronic_component import COMPONENTS as ELECTRONIC_COMPONENTS
from otk.sets.physics.m3.brightness_arrangement import LIGHT_ARRANGEMENT_PROBLEMS
from otk.sets.physics.m3.light_meter import LIGHT_METER_READINGS
from otk.sets.chemistry.p2.water_absorption import BANDS
from otk.sets.chemistry.p1.material_grouping import CRITERIA, ITEMS
from otk.sets._support.science_wave_d1 import PROPERTY
from otk.sets.chemistry.p1.material_property import THINGS

SEEDS = 300


def _triple(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}_{stage}" for stage in ("foundation", "fluency", "application"))


INDICATORS = {
    "ว 2.1 ป.1/1": _triple("chem.material_property"),
    "ว 2.1 ป.1/2": _triple("chem.material_grouping"),
    "ว 2.1 ป.2/1": _triple("chem.water_absorption"),
    "ว 2.1 ป.2/2": _triple("chem.mixed_material"),
    "ว 2.1 ป.2/3": _triple("chem.material_choice"),
    "ว 2.1 ป.2/4": _triple("chem.reuse_benefit"),
    "ว 2.1 ป.3/1": _triple("chem.object_parts"),
    "ว 2.1 ป.3/2": _triple("chem.heating_change"),
    "ว 2.1 ป.4/1": _triple("chem.material_physical"),
    "ว 2.1 ป.4/2": _triple("chem.property_discussion"),
    "ว 2.1 ป.4/3": _triple("chem.states_matter"),
    "ว 2.1 ป.4/4": _triple("chem.measuring_matter"),
    "ว 2.1 ป.5/2": _triple("chem.dissolving"),
    "ว 2.1 ป.5/3": _triple("chem.chemical_change"),
    "ว 2.1 ป.5/4": _triple("chem.reversible_change"),
    "ว 2.1 ม.1/1": _triple("chem.element_class_group"),
    "ว 2.1 ม.1/2": _triple("chem.element_use_effect"),
    "ว 2.1 ม.1/3": _triple("chem.element_safe_use"),
    "ว 2.1 ม.1/6": _triple("chem.substance_measuring"),
    "ว 2.1 ม.1/10": _triple("chem.heat_state_change"),
    "ว 2.1 ม.2/3": _triple("chem.separation_problem"),
    "ว 2.1 ม.2/4": _triple("chem.solubility_factor"),
    "ว 2.1 ม.2/5": _triple("chem.concentration"),
    "ว 2.1 ม.2/6": _triple("chem.solution_use"),
    "ว 2.1 ม.3/1": _triple("chem.modern_material"),
    "ว 2.1 ม.3/2": _triple("chem.material_thrift"),
    "ว 2.1 ม.3/3": _triple("chem.reaction_model"),
    "ว 2.1 ม.3/4": _triple("chem.conservation_mass"),
    "ว 2.1 ม.3/5": _triple("chem.reaction_heat"),
    "ว 2.1 ม.3/6": _triple("chem.everyday_reaction"),
    "ว 2.1 ม.3/7": _triple("chem.reaction_impact"),
    "ว 2.1 ม.3/8": _triple("chem.reaction_design"),
    "ว 2.2 ป.3/1": _triple("phys.force_effect"),
    "ว 2.2 ป.3/2": _triple("phys.contact_force"),
    "ว 2.2 ป.3/3": _triple("phys.magnet_sort"),
    "ว 2.2 ป.3/4": _triple("phys.magnet_pole"),
    "ว 2.2 ป.4/1": _triple("phys.gravity_effect"),
    "ว 2.2 ป.4/2": _triple("phys.spring_scale_weight"),
    "ว 2.2 ป.4/3": _triple("phys.mass_motion"),
    "ว 2.2 ป.5/1": _triple("phys.resultant_line"),
    "ว 2.2 ป.5/2": _triple("phys.force_diagram"),
    "ว 2.2 ป.5/3": _triple("phys.spring_scale_force"),
    "ว 2.2 ป.5/4": _triple("phys.friction_effect"),
    "ว 2.2 ป.5/5": _triple("phys.friction_diagram"),
    "ว 2.2 ป.6/1": _triple("phys.static_force"),
    "ว 2.2 ม.1/1": _triple("phys.air_pressure_height"),
    "ว 2.2 ม.2/1": _triple("phys.net_force_motion"),
    "ว 2.2 ม.2/2": _triple("phys.net_force_diagram"),
    "ว 2.2 ม.2/3": _triple("phys.liquid_pressure"),
    "ว 2.2 ม.2/4": _triple("phys.buoyancy"),
    "ว 2.2 ม.2/5": _triple("phys.liquid_force_diagram"),
    "ว 2.2 ม.2/6": _triple("phys.friction_kinds"),
    "ว 2.2 ม.2/7": _triple("phys.friction_factor"),
    "ว 2.2 ม.2/8": _triple("phys.friction_forces_diagram"),
    "ว 2.2 ม.2/9": _triple("phys.friction_use"),
    "ว 2.2 ม.2/10": _triple("phys.moment_balance"),
    "ว 2.2 ม.2/11": _triple("phys.field_compare"),
    "ว 2.2 ม.2/12": _triple("phys.field_force_diagram"),
    "ว 2.2 ม.2/13": _triple("phys.field_distance"),
    "ว 2.2 ม.2/14": _triple("phys.speed_velocity"),
    "ว 2.2 ม.2/15": _triple("phys.displacement_diagram"),
    "ว 2.3 ป.1/1": _triple("phys.sound_source"),
    "ว 2.3 ป.2/1": _triple("phys.light_travel"),
    "ว 2.3 ป.2/2": _triple("phys.light_safety"),
    "ว 2.3 ป.3/1": _triple("phys.energy_change"),
    "ว 2.3 ป.3/2": ("phys.generator_work_foundation", "phys.generator_source_fluency", "phys.generator_source_application"),
    "ว 2.3 ป.3/3": _triple("phys.electricity_safety"),
    "ว 2.3 ป.4/1": _triple("phys.light_medium"),
    "ว 2.3 ป.5/1": _triple("phys.hearing_medium"),
    "ว 2.3 ป.5/2": _triple("phys.pitch"),
    "ว 2.3 ป.5/3": _triple("phys.loudness"),
    "ว 2.3 ป.5/4": _triple("phys.sound_level"),
    "ว 2.3 ป.5/5": _triple("phys.noise_pollution"),
    "ว 2.3 ป.6/1": _triple("phys.circuit_parts"),
    "ว 2.3 ป.6/2": _triple("phys.circuit_diagram"),
    "ว 2.3 ป.6/3": _triple("phys.series_cells"),
    "ว 2.3 ป.6/4": _triple("phys.series_cells_benefit"),
    "ว 2.3 ป.6/5": _triple("phys.parallel_bulbs"),
    "ว 2.3 ป.6/6": _triple("phys.parallel_bulbs_benefit"),
    "ว 2.3 ป.6/7": _triple("phys.shadow"),
    "ว 2.3 ป.6/8": _triple("phys.shadow_diagram"),
    "ว 2.3 ม.1/1": _triple("phys.heat_quantity"),
    "ว 2.3 ม.1/2": _triple("phys.thermometer"),
    "ว 2.3 ม.1/3": _triple("phys.thermal_expansion"),
    "ว 2.3 ม.1/4": _triple("phys.thermal_expansion_benefit"),
    "ว 2.3 ม.1/5": _triple("phys.heat_equilibrium"),
    "ว 2.3 ม.1/6": _triple("phys.heat_transfer_mode"),
    "ว 2.3 ม.1/7": _triple("phys.heat_transfer_design"),
    "ว 2.3 ม.2/1": _triple("phys.work_power"),
    "ว 2.3 ม.2/2": _triple("phys.simple_machine"),
    "ว 2.3 ม.2/3": _triple("phys.simple_machine_benefit"),
    "ว 2.3 ม.2/4": _triple("phys.ke_pe_factor"),
    "ว 2.3 ม.2/5": _triple("phys.mechanical_energy"),
    "ว 2.3 ม.2/6": _triple("phys.energy_conservation"),
    "ว 2.3 ม.3/2": _triple("elec.vi_graph"),
    "ว 2.3 ม.3/3": _triple("elec.meter_use"),
    "ว 2.3 ม.3/5": _triple("elec.resistor_diagram"),
    "ว 2.3 ม.3/6": _triple("elec.electronic_component"),
    "ว 2.3 ม.3/7": _triple("elec.electronic_diagram"),
    "ว 2.3 ม.3/9": _triple("elec.appliance_choice"),
    "ว 2.3 ม.3/18": _triple("phys.optics_diagram"),
    "ว 2.3 ม.3/20": _triple("phys.light_meter"),
    "ว 2.3 ม.3/21": _triple("phys.brightness_arrangement"),
}

TOPICS = {
    "ว 2.1 ป.1/1": "สมบัติของวัสดุที่ใช้ทำวัตถุ",
    "ว 2.1 ป.1/2": "ชนิดและการจัดกลุ่มวัสดุ",
    "ว 2.1 ป.2/1": "การดูดซับน้ำของวัสดุ",
    "ว 2.1 ป.2/2": "วัสดุที่เกิดจากการผสมกัน",
    "ว 2.1 ป.2/3": "การเลือกวัสดุและการนำวัสดุกลับมาใช้ใหม่",
    "ว 2.1 ป.2/4": "ประโยชน์ของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่",
    "ว 2.1 ป.3/1": "วัตถุที่ประกอบจากชิ้นส่วนย่อย",
    "ว 2.1 ป.3/2": "การเปลี่ยนแปลงของวัสดุเมื่อร้อนขึ้นหรือเย็นลง",
    "ว 2.1 ป.4/1": "สมบัติทางกายภาพของวัสดุ",
    "ว 2.1 ป.4/2": "การอภิปรายสมบัติของวัสดุจากผลการทดลอง",
    "ว 2.1 ป.4/3": "สมบัติของสสารทั้ง 3 สถานะ",
    "ว 2.1 ป.4/4": "การวัดมวลและปริมาตรของสสาร",
    "ว 2.1 ป.5/2": "การละลายของสารในน้ำ",
    "ว 2.1 ป.5/3": "การเปลี่ยนแปลงทางเคมี",
    "ว 2.1 ป.5/4": "การเปลี่ยนแปลงที่ผันกลับได้และผันกลับไม่ได้",
    "ว 2.1 ม.1/1": "สมบัติของธาตุโลหะ อโลหะ และกึ่งโลหะ",
    "ว 2.1 ม.1/2": "ผลจากการใช้ธาตุ",
    "ว 2.1 ม.1/3": "การใช้ธาตุอย่างปลอดภัยและคุ้มค่า",
    "ว 2.1 ม.1/6": "การวัดมวลและปริมาตรของสารบริสุทธิ์และสารผสม",
    "ว 2.1 ม.1/10": "พลังงานความร้อนกับการเปลี่ยนสถานะ",
    "ว 2.1 ม.2/3": "การนำวิธีการแยกสารไปแก้ปัญหา",
    "ว 2.1 ม.2/4": "สภาพละลายได้ของสาร",
    "ว 2.1 ม.2/5": "ความเข้มข้นของสารละลาย",
    "ว 2.1 ม.2/6": "การใช้สารละลายอย่างถูกต้องและปลอดภัย",
    "ว 2.1 ม.3/1": "พอลิเมอร์ เซรามิก และวัสดุผสม",
    "ว 2.1 ม.3/2": "การใช้วัสดุอย่างประหยัดและคุ้มค่า",
    "ว 2.1 ม.3/3": "การเกิดปฏิกิริยาเคมี",
    "ว 2.1 ม.3/4": "กฎทรงมวล",
    "ว 2.1 ม.3/5": "ปฏิกิริยาดูดความร้อนและคายความร้อน",
    "ว 2.1 ม.3/6": "ปฏิกิริยาเคมีในชีวิตประจำวัน",
    "ว 2.1 ม.3/7": "ประโยชน์และโทษของปฏิกิริยาเคมี",
    "ว 2.1 ม.3/8": "การแก้ปัญหาด้วยความรู้เรื่องปฏิกิริยาเคมี",
    "ว 2.2 ป.3/1": "ผลของแรงต่อการเคลื่อนที่ของวัตถุ",
    "ว 2.2 ป.3/2": "แรงสัมผัสและแรงไม่สัมผัส",
    "ว 2.2 ป.3/3": "วัตถุที่แม่เหล็กดึงดูด",
    "ว 2.2 ป.3/4": "ขั้วแม่เหล็ก",
    "ว 2.2 ป.4/1": "แรงโน้มถ่วงของโลก",
    "ว 2.2 ป.4/2": "การวัดน้ำหนักด้วยเครื่องชั่งสปริง",
    "ว 2.2 ป.4/3": "มวลกับการเปลี่ยนแปลงการเคลื่อนที่",
    "ว 2.2 ป.5/1": "แรงลัพธ์ในแนวเดียวกัน",
    "ว 2.2 ป.5/2": "แผนภาพแสดงแรง",
    "ว 2.2 ป.5/3": "การวัดแรงด้วยเครื่องชั่งสปริง",
    "ว 2.2 ป.5/4": "แรงเสียดทานกับการเคลื่อนที่",
    "ว 2.2 ป.5/5": "แผนภาพแสดงแรงเสียดทาน",
    "ว 2.2 ป.6/1": "แรงไฟฟ้าจากการขัดถู",
    "ว 2.2 ม.1/1": "ความดันอากาศกับความสูง",
    "ว 2.2 ม.2/1": "แรงลัพธ์กับการเคลื่อนที่",
    "ว 2.2 ม.2/2": "แผนภาพแสดงแรงลัพธ์",
    "ว 2.2 ม.2/3": "ความดันของของเหลว",
    "ว 2.2 ม.2/4": "แรงพยุงและการจมการลอย",
    "ว 2.2 ม.2/5": "แผนภาพแสดงแรงที่กระทำต่อวัตถุในของเหลว",
    "ว 2.2 ม.2/6": "แรงเสียดทานสถิตและแรงเสียดทานจลน์",
    "ว 2.2 ม.2/7": "ปัจจัยที่มีผลต่อแรงเสียดทาน",
    "ว 2.2 ม.2/8": "แผนภาพแสดงแรงเสียดทานและแรงอื่น ๆ",
    "ว 2.2 ม.2/9": "การลดและเพิ่มแรงเสียดทาน",
    "ว 2.2 ม.2/10": "โมเมนต์ของแรง",
    "ว 2.2 ม.2/11": "สนามแม่เหล็ก สนามไฟฟ้า และสนามโน้มถ่วง",
    "ว 2.2 ม.2/12": "แผนภาพแสดงแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง",
    "ว 2.2 ม.2/13": "ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากแหล่งของสนาม",
    "ว 2.2 ม.2/14": "อัตราเร็วและความเร็วของการเคลื่อนที่",
    "ว 2.2 ม.2/15": "แผนภาพแสดงการกระจัดและความเร็ว",
    "ว 2.3 ป.1/1": "การเกิดเสียงและทิศทางการเคลื่อนที่ของเสียง",
    "ว 2.3 ป.2/1": "แนวการเคลื่อนที่ของแสงและการมองเห็นวัตถุ",
    "ว 2.3 ป.2/2": "การป้องกันอันตรายจากแสงสว่างไม่เหมาะสม",
    "ว 2.3 ป.3/1": "การเปลี่ยนพลังงานจากรูปหนึ่งไปเป็นอีกรูปหนึ่ง",
    "ว 2.3 ป.3/2": "การทำงานของเครื่องกำเนิดไฟฟ้าและแหล่งพลังงาน",
    "ว 2.3 ป.3/3": "การใช้ไฟฟ้าอย่างประหยัดและปลอดภัย",
    "ว 2.3 ป.4/1": "การจำแนกวัตถุเป็นตัวกลางโปร่งใส ตัวกลางโปร่งแสง และวัตถุทึบแสง",
    "ว 2.3 ป.5/1": "การได้ยินเสียงผ่านตัวกลาง",
    "ว 2.3 ป.5/2": "ลักษณะและการเกิดเสียงสูง เสียงต่ำ",
    "ว 2.3 ป.5/3": "ลักษณะและการเกิดเสียงดัง เสียงค่อย",
    "ว 2.3 ป.5/4": "การวัดระดับเสียงด้วยเครื่องมือวัดระดับเสียง",
    "ว 2.3 ป.5/5": "การหลีกเลี่ยงและลดมลพิษทางเสียง",
    "ว 2.3 ป.6/1": "ส่วนประกอบและหน้าที่ของวงจรไฟฟ้าอย่างง่าย",
    "ว 2.3 ป.6/2": "แผนภาพและการต่อวงจรไฟฟ้าอย่างง่าย",
    "ว 2.3 ป.6/3": "วิธีการและผลของการต่อเซลล์ไฟฟ้าแบบอนุกรม",
    "ว 2.3 ป.6/4": "ประโยชน์ของการต่อเซลล์ไฟฟ้าแบบอนุกรม",
    "ว 2.3 ป.6/5": "การต่อหลอดไฟฟ้าแบบอนุกรมและแบบขนาน",
    "ว 2.3 ป.6/6": "ประโยชน์ ข้อจำกัด และการประยุกต์ใช้การต่อหลอดไฟฟ้า",
    "ว 2.3 ป.6/7": "การเกิดเงามืดเงามัว",
    "ว 2.3 ป.6/8": "แผนภาพรังสีของแสงแสดงการเกิดเงามืดเงามัว",
    "ว 2.3 ม.1/1": "การคำนวณปริมาณความร้อนที่ทำให้สสารเปลี่ยนอุณหภูมิและเปลี่ยนสถานะ",
    "ว 2.3 ม.1/2": "การใช้เทอร์มอมิเตอร์วัดอุณหภูมิของสสาร",
    "ว 2.3 ม.1/3": "แบบจำลองการขยายตัวหรือหดตัวของสสารเนื่องจากความร้อน",
    "ว 2.3 ม.1/4": "ประโยชน์ของความรู้เรื่องการขยายตัวและหดตัวของสสาร",
    "ว 2.3 ม.1/5": "การคำนวณสมดุลความร้อนระหว่างสสาร",
    "ว 2.3 ม.1/6": "แบบจำลองการถ่ายโอนความร้อนโดยการนำ การพา และการแผ่รังสี",
    "ว 2.3 ม.1/7": "การออกแบบอุปกรณ์แก้ปัญหาด้วยความรู้เรื่องการถ่ายโอนความร้อน",
    "ว 2.3 ม.2/1": "การคำนวณงานและกำลังโดยใช้สมการ W = Fs และ P = W/t",
    "ว 2.3 ม.2/2": "หลักการทำงานของเครื่องกลอย่างง่าย",
    "ว 2.3 ม.2/3": "ประโยชน์ของเครื่องกลอย่างง่าย",
    "ว 2.3 ม.2/4": "ปัจจัยที่มีผลต่อพลังงานจลน์และพลังงานศักย์โน้มถ่วง",
    "ว 2.3 ม.2/5": "การเปลี่ยนพลังงานศักย์โน้มถ่วงและพลังงานจลน์โดยพลังงานกลคงตัว",
    "ว 2.3 ม.2/6": "การเปลี่ยนและการถ่ายโอนพลังงานโดยกฎการอนุรักษ์พลังงาน",
    "ว 2.3 ม.3/2": "กราฟความสัมพันธ์ระหว่างกระแสไฟฟ้าและความต่างศักย์ไฟฟ้า",
    "ว 2.3 ม.3/3": "การใช้โวลต์มิเตอร์และแอมมิเตอร์วัดปริมาณทางไฟฟ้า",
    "ว 2.3 ม.3/5": "แผนภาพวงจรไฟฟ้าแสดงการต่อตัวต้านทานแบบอนุกรมและขนาน",
    "ว 2.3 ม.3/6": "การทำงานของชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย",
    "ว 2.3 ม.3/7": "แผนภาพและการต่อชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย",
    "ว 2.3 ม.3/9": "การเลือกใช้เครื่องใช้ไฟฟ้าอย่างประหยัดและปลอดภัย",
    "ว 2.3 ม.3/18": "แผนภาพการเคลื่อนที่ของแสงแสดงภาพจากทัศนอุปกรณ์และเลนส์ตา",
    "ว 2.3 ม.3/20": "การวัดความสว่างของแสงด้วยอุปกรณ์วัดความสว่าง",
    "ว 2.3 ม.3/21": "การจัดความสว่างของแสงให้เหมาะสมกับกิจกรรม",
}

# Indicators joining two free verbs, each with objects of its own.
TWO_FREE_VERBS = frozenset({"ว 2.1 ป.1/2", "ว 2.1 ป.2/1", "ว 2.1 ป.2/3", "ว 2.1 ป.4/1",
                            "ว 2.1 ม.1/1", "ว 2.1 ม.2/4",
                            "ว 2.1 ม.3/6", "ว 2.1 ม.3/7",
                            "ว 2.2 ป.3/4", "ว 2.2 ม.2/10", "ว 2.2 ม.2/14",
                            "ว 2.3 ป.2/1", "ว 2.3 ป.3/2", "ว 2.3 ป.6/1",
                            "ว 2.3 ม.1/1", "ว 2.3 ม.1/5", "ว 2.3 ม.2/1",
                            "ว 2.3 ม.2/5", "ว 2.3 ม.2/6"})

# Indicators with no assessable verb: all three stages, none of them exact.
UNASSESSABLE = frozenset({"ว 2.1 ป.2/4", "ว 2.1 ป.4/2", "ว 2.1 ป.4/4", "ว 2.1 ม.1/6",
                          "ว 2.2 ป.4/2", "ว 2.2 ป.5/2", "ว 2.2 ป.5/3",
                          "ว 2.2 ป.5/5", "ว 2.2 ม.2/2",
                          "ว 2.2 ม.2/5", "ว 2.2 ม.2/8",
                          "ว 2.2 ม.2/12", "ว 2.2 ม.2/15",
                          "ว 2.3 ป.5/4", "ว 2.3 ป.6/2", "ว 2.3 ป.6/8",
                          "ว 2.3 ม.1/2", "ว 2.3 ม.3/2", "ว 2.3 ม.3/3", "ว 2.3 ม.3/5",
                          "ว 2.3 ม.3/7", "ว 2.3 ม.3/18", "ว 2.3 ม.3/20"})

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


def test_wave_d_is_its_own_cohort():
    assert set(NEW_KEYS) == SCIENCE_WAVE_D_KEYS
    for earlier in (SCIENCE_WAVE_KEYS, SCIENCE_WAVE_B_KEYS, SCIENCE_BIOLOGY_CLOSURE_KEYS,
                    SCIENCE_WAVE_C_KEYS):
        assert not SCIENCE_WAVE_D_KEYS & earlier


def test_approval_is_recorded_for_whole_indicators_inside_wave_d():
    assert SCIENCE_WAVE_D_APPROVED_KEYS <= SCIENCE_WAVE_D_KEYS
    for code, keys in INDICATORS.items():
        assert set(keys) & SCIENCE_WAVE_D_APPROVED_KEYS in (set(), set(keys)), code


def test_every_unapproved_set_is_on_the_review_worklist():
    pending = set().union(*REVIEW_PENDING.values()) if REVIEW_PENDING else set()
    assert SCIENCE_WAVE_D_KEYS - SCIENCE_WAVE_D_APPROVED_KEYS <= pending


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


# ── slice 1 ───────────────────────────────────────────────────────────────────

def test_each_observed_property_names_one_material():
    assert len(set(PROPERTY.values())) == len(PROPERTY)


def test_the_object_record_is_explained_part_by_part():
    by_property = {text: material for material, text in PROPERTY.items()}
    for seed in range(SEEDS):
        question = generate("chem.material_property_fluency", Random(seed))
        stem = _stem(question)
        thing = next(t for t in THINGS if stem.startswith(f"นักเรียนสังเกต{t.name} "))
        materials = [by_property[text] for text in PROPERTY.values()
                     if any(f"{part}{text}" in stem for part, _ in thing.parts)]
        assert sorted(materials) == sorted(m for _, m in thing.parts)
        answer = _texts(question)[question.answer]
        count = "ชนิดเดียว" if len(thing.parts) == 1 else f" {len(thing.parts)} ชนิด"
        assert answer.startswith(f"ทำจากวัสดุ{count} คือ ")
        for material in materials:
            assert f"{material} ซึ่ง{PROPERTY[material]}" in answer


def test_every_object_is_grouped_by_its_material():
    for criterion in CRITERIA:
        assert not criterion.have & criterion.lack
    for seed in range(SEEDS):
        question = generate("chem.material_grouping_fluency", Random(seed))
        stem = _stem(question)
        criterion = next(c for c in CRITERIA if f'"{c.name}"' in stem)
        listed = stem.split("ได้แก่ ", 1)[1].split(" ตามสมบัติ")[0].split(", ")
        have = [item for item in listed if ITEMS[item] in criterion.have]
        lack = [item for item in listed if ITEMS[item] in criterion.lack]
        assert len(have) + len(lack) == 5
        expected = f"กลุ่มที่{criterion.name}: {', '.join(have)} / กลุ่มที่{criterion.opposite}: {', '.join(lack)}"
        assert _texts(question)[question.answer] == expected


def test_the_absorption_ranking_is_read_from_the_record():
    band_of = {name: i for i, band in enumerate(BANDS) for name in band}
    for seed in range(SEEDS):
        question = generate("chem.water_absorption_fluency", Random(seed))
        rows = [(name, int(amount)) for name, amount in
                re.findall(r"(\S+) (\d+) มิลลิลิตร(?= / | จาก)", _stem(question))]
        assert len(rows) == 4 and len({amount for _, amount in rows}) == 4
        assert sorted(band_of[name] for name, _ in rows) == [0, 1, 2, 3]
        ranked = [name for name, _ in sorted(rows, key=lambda row: -row[1])]
        assert _texts(question)[question.answer] == " → ".join(ranked)


# ── slice 2 ───────────────────────────────────────────────────────────────────

def test_the_mixture_is_explained_from_its_record():
    assert len({mix.after for mix in MIXES}) == len(MIXES)
    for seed in range(SEEDS):
        question = generate("chem.mixed_material_fluency", Random(seed))
        stem = _stem(question)
        mix = next(m for m in MIXES if f"ก่อนผสม {m.first}{m.first_alone} " in stem)
        assert f"วัสดุที่ได้{mix.after} " in stem
        assert _texts(question)[question.answer] == f"วัสดุที่ได้{mix.after} ซึ่งต่างจาก{mix.first}ที่{mix.first_alone}"


def test_the_chosen_material_is_the_one_whose_result_meets_the_need():
    for purpose in PURPOSES:
        results = dict(purpose.results)
        assert [name for name, result in purpose.results if result == purpose.need] == [purpose.best]
        assert purpose.best in results
    for seed in range(SEEDS):
        question = generate("chem.material_choice_foundation", Random(seed))
        purpose = next(p for p in PURPOSES if _stem(question).startswith(f"นักเรียนจะทำ{p.make} "))
        assert _texts(question)[question.answer].startswith(f"{purpose.best} เพราะ{purpose.need} ")


def test_a_reuse_is_never_marked_wrong_where_the_material_could_serve():
    uses = {reuse.new_use for reuse in REUSES}
    assert len(uses) == len(REUSES)
    for reuse in REUSES:
        assert reuse.defensible <= uses and reuse.new_use not in reuse.defensible
    for seed in range(SEEDS):
        question = generate("chem.material_choice_fluency", Random(seed))
        reuse = next(r for r in REUSES if _stem(question).startswith(f"นักเรียนสังเกต{r.used} "))
        texts = _texts(question)
        assert texts[question.answer] == f"ทำเป็น{reuse.new_use} เพราะ{reuse.observed}"
        for wrong in texts:
            if wrong != texts[question.answer]:
                assert not any(wrong.startswith(f"ทำเป็น{use} ") for use in reuse.defensible)


# ── slice 3 ───────────────────────────────────────────────────────────────────

def test_the_rebuilt_object_holds_every_piece_counted():
    for seed in range(SEEDS):
        question = generate("chem.object_parts_fluency", Random(seed))
        stem = _stem(question)
        red, blue = (int(n) for n in re.findall(r"(\d+) ชิ้น", stem)[:2])
        second = next(s for _, _, s in SETS if f"มาต่อเป็นรูป{s} " in stem)
        answer = _texts(question)[question.answer]
        assert answer.startswith(f"{second}มี {red + blue} ชิ้น เพราะประกอบจากชิ้นส่วนย่อยชุดเดิม")


def test_the_change_is_explained_from_what_was_done_and_seen():
    heats = {"กระทะ", "น้ำอุ่น", "จุดไฟ", "ทอด"}
    for change in CHANGES:
        assert (change.action == HOTTER) == any(word in change.how for word in heats)
        assert change.action in (HOTTER, COLDER) and change.before != change.after
    for seed in range(SEEDS):
        question = generate("chem.heating_change_fluency", Random(seed))
        stem = _stem(question)
        change = next(c for c in CHANGES if stem.startswith(f"นักเรียนนำ{c.material}ซึ่งเป็น{c.before} "))
        assert f"กลายเป็น{change.after} " in stem
        assert _texts(question)[question.answer] == (
            f"เมื่อ{change.action} {change.material}เปลี่ยนจาก{change.before}กลายเป็น{change.after}")


# ── slice 4 ───────────────────────────────────────────────────────────────────

def test_the_four_property_comparison_is_read_from_the_tests():
    for seed in range(SEEDS):
        question = generate("chem.material_physical_fluency", Random(seed))
        stem = _stem(question)
        a, b = sorted((m for m in PHYSICAL_MATERIALS if m.name in stem), key=lambda m: stem.index(m.name))
        scratched = next(m for m in (a, b) if f"{m.name}เกิดรอยขูด" in stem)
        assert scratched.hardness < max(a.hardness, b.hardness)
        for m in (a, b):
            assert (f"{m.name}กลับสู่รูปเดิม" in stem) == m.elastic
            assert (f"เมื่อใช้{m.name}หลอดไฟสว่าง" in stem) == m.conducts
        parts = comparison(a, b)
        assert _texts(question)[question.answer] == " / ".join(f"{p.label}: {p.true}" for p in parts)


def test_no_design_offers_its_own_material_as_wrong():
    assert len({d.part for d in DESIGNS}) == len(DESIGNS)
    for design in DESIGNS:
        assert not any(wrong.startswith(design.material + " ") for wrong in design.wrongs)


# ── slice 5 ───────────────────────────────────────────────────────────────────

def test_two_states_are_compared_on_all_four_aspects():
    for seed in range(SEEDS):
        question = generate("chem.states_matter_fluency", Random(seed))
        stem = _stem(question)
        a = next(s for s in STATES if f"เปรียบเทียบ{s.name} " in stem)
        b = next(s for s in STATES if f"กับ{s.name} " in stem)
        parts = state_parts(a, b)
        assert len({p.label for p in parts}) == 4
        assert _texts(question)[question.answer] == " / ".join(f"{p.label}: {p.true}" for p in parts)


def test_measured_quantities_are_differences_of_the_readings():
    for seed in range(SEEDS):
        question = generate("chem.measuring_matter_fluency", Random(seed))
        stem = _stem(question)
        first, second = (int(n) for n in re.findall(r"(\d+) (?:มิลลิลิตร|กรัม)", stem)[:2])
        unit = "ลูกบาศก์เซนติเมตร" if "กระบอกตวง" in stem else "กรัม"
        assert _texts(question)[question.answer] == f"{second - first} {unit}"


# ── slice 6 ───────────────────────────────────────────────────────────────────

def test_each_substance_is_explained_by_what_was_seen():
    for seed in range(SEEDS):
        question = generate("chem.dissolving_fluency", Random(seed))
        stem = _stem(question)
        shown = [s for s in SOLUTES if f"{s.name}: {s.seen}" in stem]
        assert len(shown) == 3 and {s.dissolves for s in shown} == {True, False}
        answer = _texts(question)[question.answer]
        for s in shown:
            assert f"{s.name}: {'ละลายน้ำ' if s.dissolves else 'ไม่ละลายน้ำ'} " in answer


def test_the_chemical_change_answer_cites_its_own_record():
    for seed in range(SEEDS):
        question = generate("chem.chemical_change_fluency", Random(seed))
        activity = next(a for a in CHANGE_ACTIVITIES if _stem(question).startswith(f"นักเรียน{a.doing} "))
        answer = _texts(question)[question.answer]
        kind = "เกิดการเปลี่ยนแปลงทางเคมี" if activity.chemical else "ไม่เกิดการเปลี่ยนแปลงทางเคมี"
        assert answer.startswith(kind) and answer.endswith(activity.seen)


def test_every_change_is_sorted_into_its_kind():
    assert not set(REVERSIBLE) & set(IRREVERSIBLE)
    for seed in range(SEEDS):
        question = generate("chem.reversible_change_fluency", Random(seed))
        listed = _stem(question).split("ได้แก่ ", 1)[1].split(" ข้อใด")[0].split(", ")
        back = [c for c in listed if c in REVERSIBLE]
        stay = [c for c in listed if c in IRREVERSIBLE]
        assert len(back) + len(stay) == 5
        expected = f"ผันกลับได้: {', '.join(back)} / ผันกลับไม่ได้: {', '.join(stay)}"
        assert _texts(question)[question.answer] == expected


# ── slice 7 ───────────────────────────────────────────────────────────────────

def test_the_elements_are_grouped_by_their_test_results():
    by_result = {tests: kind for kind, tests in TESTS.items()}
    assert len(by_result) == len(TESTS)
    for seed in range(SEEDS):
        question = generate("chem.element_class_group_foundation", Random(seed))
        stem = _stem(question)
        groups = {kind: [] for kind in KINDS}
        for chunk in stem.split(" — ", 1)[1].split(" จากผล")[0].split(" / "):
            name = chunk.split(": ", 1)[0]
            element = next(e for e in ELEMENTS if e.name == name)
            kind = next(k for (lamp, hammer), k in by_result.items() if lamp in chunk and hammer in chunk)
            assert kind == element.kind
            groups[kind].append(name)
        expected = " / ".join(f"{k}: {', '.join(groups[k]) or 'ไม่มี'}" for k in KINDS)
        assert _texts(question)[question.answer] == expected


def test_a_guideline_answer_takes_both_halves_from_its_own_case():
    for seed in range(SEEDS):
        question = generate("chem.element_safe_use_fluency", Random(seed))
        guide = next(g for g in GUIDELINES if _stem(question).startswith(g.case))
        answer = _texts(question)[question.answer]
        assert answer == f"ปลอดภัย: {guide.safe} / คุ้มค่า: {guide.worthwhile}"
        for wrong in _texts(question):
            if wrong != answer:
                assert not (guide.safe in wrong and guide.worthwhile in wrong)


# ── slice 8 ───────────────────────────────────────────────────────────────────

def test_the_density_is_worked_out_from_the_readings():
    for seed in range(SEEDS):
        question = generate("chem.substance_measuring_fluency", Random(seed))
        stem = _stem(question)
        empty, volume, full = (float(n) for n in re.findall(r"([\d.]+) (?:กรัม|ลูกบาศก์เซนติเมตร)", stem)[:3])
        liquid = next(item for item in LIQUIDS if f"เท{item.name}ลงไป" in stem)
        assert round((full - empty) / volume, 2) == liquid.density
        assert _texts(question)[question.answer] == f"{liquid.density:g} กรัมต่อลูกบาศก์เซนติเมตร"


def test_the_change_of_state_interval_is_read_from_the_record():
    for seed in range(SEEDS):
        question = generate("chem.heat_state_change_fluency", Random(seed))
        stem = _stem(question)
        temps = [int(t) for t in re.findall(r"นาทีที่ \d+: (-?\d+)", stem)]
        change = next(c for c in STATE_CHANGES if f"ความร้อนแก่{c.substance}อย่าง" in stem)
        flat = [minute for minute, t in enumerate(temps) if t == change.plateau]
        assert flat == list(range(flat[0], flat[-1] + 1)) and len(flat) >= 4
        answer = _texts(question)[question.answer]
        assert f"นาทีที่ {flat[0]} ถึง {flat[-1]} ซึ่งอุณหภูมิคงที่" in answer
        assert f"จาก{change.start_state}เป็น{change.end_state}" in answer


# ── slice 9 ───────────────────────────────────────────────────────────────────

def test_no_separation_problem_offers_a_defensible_method_as_wrong():
    for seed in range(SEEDS):
        question = generate("chem.separation_problem_fluency", Random(seed))
        problem = next(p for p in PROBLEMS if _stem(question).startswith(p.problem))
        texts = _texts(question)
        assert texts[question.answer].startswith(f"ใช้{problem.method} เพราะ")
        for wrong in texts:
            assert not any(wrong.startswith(f"ใช้{m} ") for m in problem.defensible)


def test_each_solubility_effect_follows_its_own_experiment():
    for seed in range(SEEDS):
        question = generate("chem.solubility_factor_fluency", Random(seed))
        stem = _stem(question)
        one, two, three = stem.split("การทดลองที่ ")[1:4]
        (a, qa), (b, qb) = re.findall(r"(\S+) ละลายได้ ([\d.]+) กรัม", one)
        more, less = (a, b) if float(qa) > float(qb) else (b, a)
        solute, s1, q1, s2, q2 = re.search(r"\): (\S+?)ละลายใน(\S+?)ได้ ([\d.]+) กรัม, ใน(\S+?)ได้ ([\d.]+) กรัม", two).groups()
        good, poor = (s1, s2) if float(q1) > float(q2) else (s2, s1)
        warm, w1, t1, w2, t2 = re.search(r"\): (\S+?)ละลายได้ ([\d.]+) กรัมที่ (\d+) องศาเซลเซียส และ ([\d.]+) กรัมที่ (\d+)", three).groups()
        rises = (float(w2) > float(w1)) == (int(t2) > int(t1))
        answer = _texts(question)[question.answer]
        assert f"{more}ละลายได้มากกว่า{less}" in answer
        assert f"{solute}ละลายใน{good}ได้มากกว่าใน{poor}" in answer
        assert f"{warm}ละลายน้ำได้{'มากขึ้น' if rises else 'น้อยลง'}เมื่ออุณหภูมิสูงขึ้น" in answer


# ── slice 10 ──────────────────────────────────────────────────────────────────

def test_every_concentration_is_worked_out_from_its_description():
    for seed in range(SEEDS):
        question = generate("chem.concentration_fluency", Random(seed))
        stem = _stem(question)
        answer = _texts(question)[question.answer]
        for row in stem.split(" — ", 1)[1].split(" ข้อใด")[0].split(" / "):
            label = row.split(":")[0]
            numbers = [int(n) for n in re.findall(r"(\d+) (?:กรัม|ลูกบาศก์เซนติเมตร)", row)]
            unit = next(u for u, m in MIXTURES.items() if m.solute in row)
            whole = numbers[0] + numbers[1] if "ในน้ำ" in row else numbers[1]
            assert f"{label}: ร้อยละ {100 * numbers[0] // whole} โดย{unit}" in answer


def test_the_material_answer_covers_every_kind_in_the_record():
    kinds = {sample.kind for sample in SAMPLES}
    assert kinds == set(KIND_PARTS)
    for seed in range(SEEDS):
        question = generate("chem.modern_material_fluency", Random(seed))
        stem = _stem(question)
        assert {s.kind for s in SAMPLES if f"{s.name} ({s.kind}): {s.tested}" in stem} == kinds
        assert _texts(question)[question.answer] == " / ".join(f"{p.label}: {p.true}" for p in KIND_PARTS.values())


# ── slice 11 ──────────────────────────────────────────────────────────────────

def test_every_reaction_model_conserves_atoms():
    for reaction in REACTIONS:
        assert count_atoms(reaction.reactants) == count_atoms(reaction.products)


def test_the_reaction_answer_counts_the_atoms_in_the_model():
    for seed in range(SEEDS):
        question = generate("chem.reaction_model_fluency", Random(seed))
        stem = _stem(question)
        reaction = next(r for r in REACTIONS
                        if f"ก่อนเกิดปฏิกิริยามี {model(r.reactants)} หลังเกิดปฏิกิริยามี {model(r.products)} " in stem)
        answer = _texts(question)[question.answer]
        assert answer.startswith(f"สมการข้อความ: {word_equation(reaction)} /")
        for atom, n in count_atoms(reaction.reactants).items():
            assert f"{atom} {n} อะตอม" in answer


# ── slice 12 ──────────────────────────────────────────────────────────────────

def test_the_mass_answer_follows_the_vessel_and_the_readings():
    for seed in range(SEEDS):
        question = generate("chem.conservation_mass_fluency", Random(seed))
        stem = _stem(question)
        before, after = (float(n) for n in re.findall(r"([\d.]+) กรัม", stem)[:2])
        answer = _texts(question)[question.answer]
        if "ปิดฝาสนิท" in stem:
            assert before == after and answer.startswith("มวลเท่าเดิม")
        else:
            assert answer.startswith(f"มวลลดลง {before - after:.1f} กรัม เพราะแก๊ส")


def test_the_reaction_heat_is_classified_from_the_temperatures():
    for seed in range(SEEDS):
        question = generate("chem.reaction_heat_fluency", Random(seed))
        stem = _stem(question)
        start, end = (int(n) for n in re.findall(r"ได้ (\d+) องศาเซลเซียส", stem))
        heat = next(h for h in HEATS if stem.startswith(f"นักเรียน{h.what} "))
        assert (end > start) == heat.gives_out
        answer = _texts(question)[question.answer]
        kind = "ปฏิกิริยาคายความร้อน" if end > start else "ปฏิกิริยาดูดความร้อน"
        change = f"อุณหภูมิ{'เพิ่มขึ้น' if end > start else 'ลดลง'} {abs(end - start)} องศาเซลเซียส"
        assert answer.startswith(f"ประเภท: {kind} / หลักฐาน: {change} /")


# ── slice 13 ──────────────────────────────────────────────────────────────────

def test_every_experiment_gets_its_own_word_equation():
    for seed in range(SEEDS):
        question = generate("chem.everyday_reaction_fluency", Random(seed))
        stem = _stem(question)
        order = sorted(EXPERIMENTS, key=lambda e: stem.index(f"{e.name}: {e.seen}"))
        expected = " / ".join(f"{e.equation.label}: {e.equation.true}" for e in order)
        assert _texts(question)[question.answer] == expected


def test_a_reaction_problem_is_answered_by_its_own_remedy():
    assert len({impact.remedy for impact in IMPACTS}) == len(IMPACTS)
    for seed in range(SEEDS):
        question = generate("chem.reaction_impact_fluency", Random(seed))
        impact = next(i for i in IMPACTS if _stem(question).startswith(i.problem))
        assert _texts(question)[question.answer] == impact.remedy


def test_wo_two_one_is_complete_from_primary_to_lower_secondary():
    """Every ``ว 2.1`` indicator from ป.1 to ม.3 holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.1 ป.") or code.startswith(("ว 2.1 ม.1/", "ว 2.1 ม.2/", "ว 2.1 ม.3/")):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 41, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 14 ──────────────────────────────────────────────────────────────────

def test_the_force_effect_matches_its_record():
    for seed in range(SEEDS):
        question = generate("phys.force_effect_fluency", Random(seed))
        push = next(p for p in PUSHES if p.record in _stem(question))
        assert _texts(question)[question.answer] == push.effect


def test_objects_are_sorted_by_the_magnet_test_record():
    assert not set(ATTRACTED) & set(NOT_ATTRACTED)
    for seed in range(SEEDS):
        question = generate("phys.magnet_sort_fluency", Random(seed))
        record = _stem(question).split(" — ", 1)[1].split(" ข้อใด")[0].split(" / ")
        yes = [r.split(": ")[0] for r in record if r.endswith(": ติดแม่เหล็ก")]
        no = [r.split(": ")[0] for r in record if r.endswith(": ไม่ติดแม่เหล็ก")]
        assert set(yes) <= set(ATTRACTED) and set(no) <= set(NOT_ATTRACTED)
        expected = f"แม่เหล็กดึงดูด: {', '.join(yes)} / แม่เหล็กไม่ดึงดูด: {', '.join(no)}"
        assert _texts(question)[question.answer] == expected


def test_magnet_meetings_follow_the_facing_poles():
    for seed in range(SEEDS):
        question = generate("phys.magnet_pole_fluency", Random(seed))
        if not _stem(question).startswith("วางแม่เหล็กแท่ง 3 แท่งเรียงกันจากซ้ายไปขวา โดย"):
            continue  # Wave H's other layouts are checked in test_science_wave_h.py
        poles = re.findall(r"แท่ง [กขค]: (ขั้ว\S+) – (ขั้ว\S+)", _stem(question))
        meet = ["ผลักกัน" if poles[i][1] == poles[i + 1][0] else "ดึงดูดกัน" for i in range(2)]
        assert _texts(question)[question.answer] == f"แท่ง ก กับ ข {meet[0]} / แท่ง ข กับ ค {meet[1]}"


def test_an_unknown_pole_is_named_from_the_test():
    for seed in range(SEEDS):
        question = generate("phys.magnet_pole_foundation", Random(seed))
        stem = _stem(question)
        if not stem.startswith("นำขั้ว"):
            continue  # Wave H's pole facts
        known = "ขั้วเหนือ" if stem.startswith("นำขั้วเหนือ") else "ขั้วใต้"
        other = "ขั้วใต้" if known == "ขั้วเหนือ" else "ขั้วเหนือ"
        end = known if "พบว่าผลักกัน" in stem else other
        far = other if end == known else known
        assert _texts(question)[question.answer] == f"ปลาย X เป็น{end} ปลายอีกด้านเป็น{far}"


# ── slice 15 ──────────────────────────────────────────────────────────────────

def test_the_gravity_effect_matches_the_observation():
    for seed in range(SEEDS):
        question = generate("phys.gravity_effect_fluency", Random(seed))
        sighting = next(s for s in SIGHTINGS if s.record in _stem(question))
        assert _texts(question)[question.answer] == sighting.effect


def test_the_heaviest_cart_moves_least_in_every_record():
    for seed in range(SEEDS):
        question = generate("phys.mass_motion_fluency", Random(seed))
        rows = [(label, int(m), int(d)) for label, m, d in
                re.findall(r"รถ ([กขค]): มวล (\d+) กิโลกรัม เคลื่อนที่ได้ (\d+) เซนติเมตร", _stem(question))]
        heaviest = max(rows, key=lambda r: r[1])
        assert heaviest[2] == min(r[2] for r in rows)
        assert _texts(question)[question.answer].startswith(f"รถ {heaviest[0]} ซึ่งมีมวลมากที่สุดเคลื่อนที่ได้น้อยที่สุด")


# ── slice 16 ──────────────────────────────────────────────────────────────────

def test_the_resultant_at_rest_is_worked_from_the_readings():
    for seed in range(SEEDS):
        question = generate("phys.resultant_line_fluency", Random(seed))
        a, b, c = (int(n) for n in re.findall(r"อ่านได้ (\d+) นิวตัน", _stem(question)))
        assert a + b == c
        assert _texts(question)[question.answer].startswith(f"แรงไปทางซ้ายรวมกันได้ {a} + {b} = {c} นิวตัน")


def test_the_force_diagram_is_drawn_to_scale():
    for seed in range(SEEDS):
        question = generate("phys.force_diagram_fluency", Random(seed))
        left, right = (int(n) for n in re.findall(r"แรง (\d+) นิวตัน", _stem(question))[:2])
        toward = "ทางขวา" if right > left else "ทางซ้าย"
        expected = (f"แรง: ลูกศรยาว {left} ช่องชี้ไปทางซ้าย และ ลูกศรยาว {right} ช่องชี้ไปทางขวา / "
                    f"แรงลัพธ์: ลูกศรยาว {abs(right - left)} ช่องชี้ไป{toward}")
        assert _texts(question)[question.answer] == expected


def test_friction_is_greatest_where_the_box_slid_least():
    for seed in range(SEEDS):
        question = generate("phys.friction_effect_fluency", Random(seed))
        rows = [(s, int(d)) for s, d in re.findall(r"(พื้น\S+): ไถลได้ (\d+) เซนติเมตร", _stem(question))]
        most = min(rows, key=lambda r: r[1])[0]
        assert _texts(question)[question.answer].startswith(f"{most}มีแรงเสียดทานมากที่สุด")


# ── slice 17 ──────────────────────────────────────────────────────────────────

def test_pressure_falls_with_height_and_the_answer_names_the_highest_place():
    readings = [pressure_at(h) for _, h in sorted(PLACES, key=lambda p: p[1])]
    assert readings == sorted(readings, reverse=True) and len(set(readings)) == len(readings)
    for seed in range(SEEDS):
        question = generate("phys.air_pressure_height_fluency", Random(seed))
        rows = re.findall(r"(\S+(?: \S+)*?) สูง ([\d,]+) เมตร: (\d+) กิโลพาสคัล", _stem(question).split("ข้อมูลที่วัดได้: ")[1])
        highest = max(rows, key=lambda r: int(r[1].replace(",", "")))
        assert int(highest[2]) == min(int(r[2]) for r in rows)
        assert _texts(question)[question.answer].startswith(f"ยิ่งสูงความดันอากาศยิ่งลดลง {highest[0].strip(' /')}จึง")


# ── slice 18 ──────────────────────────────────────────────────────────────────

def test_the_predicted_motion_follows_the_resultant():
    for seed in range(SEEDS):
        question = generate("phys.net_force_motion_fluency", Random(seed))
        stem = _stem(question)
        right_part, left_part = stem.split("กระทำไปทางขวา")[0], stem.split("กระทำไปทางขวา")[1]
        right = sum(int(n) for n in re.findall(r"(\d+) นิวตัน", right_part))
        left = int(re.search(r"แรง (\d+) นิวตัน กระทำไปทางซ้าย", left_part).group(1))
        start = "อยู่นิ่ง" if "พื้นลื่นอยู่นิ่ง" in stem else "กำลังเคลื่อนที่ไปทางขวา"
        assert _texts(question)[question.answer] == predict(start, right - left)


def test_the_buoyant_force_is_the_difference_of_the_readings():
    for seed in range(SEEDS):
        question = generate("phys.buoyancy_fluency", Random(seed))
        air, water = (int(n) for n in re.findall(r"อ่านได้ (\d+) นิวตัน", _stem(question)))
        assert _texts(question)[question.answer].startswith(f"น้ำให้แรงพยุง {air - water} นิวตันในทิศขึ้น")


def test_liquid_pressure_answers_follow_the_three_experiments():
    for seed in range(SEEDS):
        question = generate("phys.liquid_pressure_fluency", Random(seed))
        stem = _stem(question)
        (d1, n1), (d2, n2) = [(int(d), int(n)) for d, n in re.findall(r"ที่ลึก (\d+) เซนติเมตร (?:น้ำ)?พุ่ง(?:ออกจากรู)?ได้ไกล (\d+)", stem)]
        deep = d1 if n1 > n2 else d2
        dense = re.search(r"\): (\S+?)พุ่งได้ไกลกว่า", stem).group(1)
        answer = _texts(question)[question.answer]
        assert f"ที่ลึก {deep} เซนติเมตร ความดันมากกว่า" in answer
        assert f"ที่ความลึกเท่ากัน {dense}มีความดันมากกว่า" in answer
        assert "รูปร่างภาชนะจึงไม่มีผล" in answer


# ── slice 19 ──────────────────────────────────────────────────────────────────

def test_the_friction_record_gives_static_and_kinetic_friction():
    for seed in range(SEEDS):
        question = generate("phys.friction_kinds_fluency", Random(seed))
        readings = [int(n) for n in re.findall(r"อ่านได้ (\d+) นิวตัน", _stem(question))]
        low, _, peak, kinetic = readings
        assert low < peak and kinetic < peak
        answer = _texts(question)[question.answer]
        assert f"แรงเสียดทานสถิตสูงสุด: มีค่า {peak} นิวตัน" in answer
        assert f"เกิดแรงเสียดทานจลน์ {kinetic} นิวตัน ซึ่งน้อยกว่า" in answer


def test_friction_factor_answers_follow_the_three_experiments():
    for seed in range(SEEDS):
        question = generate("phys.friction_factor_fluency", Random(seed))
        stem = _stem(question)
        light, f_light, heavy, f_heavy = (int(n) for n in re.findall(
            r"กล่องหนัก (\d+) นิวตัน ลากได้ด้วยแรง (\d+) นิวตัน", stem)[0] + re.findall(
            r"กล่องหนัก (\d+) นิวตัน ลากได้ด้วยแรง (\d+) นิวตัน", stem)[1])
        assert f_heavy > f_light
        s1, n1, s2, n2 = re.search(r"บน(\S+)ใช้แรง (\d+) นิวตัน บน(\S+)ใช้แรง (\d+) นิวตัน", stem).groups()
        rough, smooth = (s1, s2) if int(n1) > int(n2) else (s2, s1)
        answer = _texts(question)[question.answer]
        assert f"จาก {light} เป็น {heavy} นิวตัน แรงเสียดทานเพิ่มขึ้น" in answer
        assert f"{rough}ซึ่งขรุขระกว่ามีแรงเสียดทานมากกว่า{smooth}" in answer


# ── slice 20 ──────────────────────────────────────────────────────────────────

def test_the_balanced_moments_are_equal_in_the_record():
    for seed in range(SEEDS):
        question = generate("phys.moment_balance_foundation", Random(seed))
        if "สมดุลที่จุดหมุน" not in _stem(question):
            continue  # Wave H's unbalanced rulers are checked in test_science_wave_h.py
        lf, ld, rf, rd = (int(n) for n in re.findall(r"(\d+) (?:นิวตัน|เซนติเมตร)", _stem(question))[:4])
        assert lf * ld == rf * rd
        assert _texts(question)[question.answer].startswith(f"โมเมนต์ทวนเข็มนาฬิกา {lf} × {ld} = {lf * ld}")


def test_the_lever_calculation_balances():
    for seed in range(SEEDS):
        question = generate("phys.moment_balance_fluency", Random(seed))
        stem = _stem(question)
        answer = float(_texts(question)[question.answer].split()[0])
        numbers = [float(n) for n in re.findall(r"([\d.]+) (?:นิวตัน|เมตร)", stem)]
        if stem.endswith("หนักเท่าใด"):
            w1, d1, d2 = numbers
            assert w1 * d1 == answer * d2
        else:
            w1, d1, w2 = numbers
            assert w1 * d1 == w2 * answer


def test_the_friction_proposal_matches_its_problem():
    for seed in range(SEEDS):
        question = generate("phys.friction_use_fluency", Random(seed))
        problem = next(p for p in FRICTION_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == f"ควร{problem.change} โดย{problem.method}"


def test_every_field_answer_covers_all_three_fields():
    for seed in range(SEEDS):
        question = generate("phys.field_compare_fluency", Random(seed))
        assert _texts(question)[question.answer] == " / ".join(f"{p.label}: {p.true}" for p in FIELD_PARTS)


# ── slice 21 ──────────────────────────────────────────────────────────────────

def test_field_force_diagram_foundation_cases_are_all_distinct():
    assert len({case.stem for case in FIELD_DIAGRAM_CASES}) == len(FIELD_DIAGRAM_CASES)
    for case in FIELD_DIAGRAM_CASES:
        assert case.correct not in case.wrongs


def test_the_field_force_diagram_shows_a_drawing_rather_than_describing_one():
    """``ม.2/12``'s Fluency set now renders the diagram instead of wording it.

    The invariant this test used to check by parsing "ลูกศรยาว N ช่อง" out of the
    answer — that the normal force is drawn as long as the weight — is enforced
    against the spec pool itself by
    ``test_force_diagrams.test_a_resting_object_never_has_an_unbalanced_vertical_pair``,
    which is stronger: it holds for every spec, not only the ones a seed reaches.
    """
    for seed in range(SEEDS):
        question = generate("phys.field_force_diagram_fluency", Random(seed))
        assert any(block.kind == "image" for block in question.stem), seed
        assert "ลูกศรยาว" not in _texts(question)[question.answer]


def test_the_field_distance_record_always_falls_with_distance():
    for seed in range(SEEDS):
        question = generate("phys.field_distance_fluency", Random(seed))
        stem = _stem(question)
        rows = [(int(d), int(f)) for d, f in
                re.findall(r"ระยะ (\d+) เซนติเมตร: แรง (\d+) นิวตัน", stem)]
        assert len(rows) == 3
        by_distance = sorted(rows)
        assert [f for _, f in by_distance] == sorted((f for _, f in rows), reverse=True)
        answer = _texts(question)[question.answer]
        assert answer.endswith("ยิ่งมีขนาดลดลง")


def test_speed_and_velocity_come_from_distance_and_displacement():
    for seed in range(SEEDS):
        question = generate("phys.speed_velocity_fluency", Random(seed))
        stem = _stem(question)
        distance, displacement, time = (int(n) for n in re.findall(
            r"ระยะทางที่วิ่งจริงคือ (\d+) เมตร แต่การกระจัดจาก A ไป B วัดได้ (\d+) เมตร ใช้เวลา (\d+) วินาที", stem)[0])
        assert displacement < distance
        answer = _texts(question)[question.answer]
        assert answer == (f"อัตราเร็ว: {distance} ÷ {time} = {distance / time:g} เมตรต่อวินาที / "
                           f"ความเร็ว: {displacement} ÷ {time} = {displacement / time:g} เมตรต่อวินาที ในทิศจาก A ไป B")


def test_the_displacement_arrow_matches_the_position_change():
    for seed in range(SEEDS):
        question = generate("phys.displacement_diagram_fluency", Random(seed))
        stem = _stem(question)
        start, end = (int(n) for n in re.findall(r"ตำแหน่ง (\d+) เมตร", stem)[:2])
        direction = "ตะวันออก" if end > start else "ตะวันตก"
        answer = _texts(question)[question.answer]
        assert answer == f"ลูกศรยาว {abs(end - start)} ช่อง ชี้ไปทาง{direction}"


# ── slice 22 ──────────────────────────────────────────────────────────────────

def test_the_sound_answer_names_its_own_vibrating_source():
    assert len({s.part for s in SOUND_SOURCES}) == len(SOUND_SOURCES)
    for seed in range(SEEDS):
        question = generate("phys.sound_source_fluency", Random(seed))
        source = next(s for s in SOUND_SOURCES if s.seen in _stem(question))
        answer = _texts(question)[question.answer]
        assert answer == f"เสียงเกิดจากการสั่นของ{source.part} และเคลื่อนที่ออกจากแหล่งกำเนิดเสียงไปทุกทิศทางรอบตัว"


def test_the_light_safety_proposal_matches_its_problem():
    assert len({p.method for p in LIGHT_PROBLEMS}) == len(LIGHT_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.light_safety_fluency", Random(seed))
        problem = next(p for p in LIGHT_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method


# ── slice 23 ──────────────────────────────────────────────────────────────────

def test_the_energy_change_answer_names_its_own_before_and_after():
    assert len({(c.before, c.after) for c in ENERGY_CHANGES}) == len(ENERGY_CHANGES)
    for seed in range(SEEDS):
        question = generate("phys.energy_change_fluency", Random(seed))
        change = next(c for c in ENERGY_CHANGES if _stem(question).startswith(c.record))
        assert _texts(question)[question.answer] == f"เปลี่ยนจาก{change.before}เป็น{change.after}"


def test_the_device_energy_answer_matches_its_own_device():
    by_device = dict(DEVICES)
    assert len(by_device) == len(DEVICES)
    for seed in range(SEEDS):
        question = generate("phys.energy_change_foundation", Random(seed))
        device = next(d for d in by_device if f"เมื่อเสียบปลั๊ก{d} " in _stem(question))
        assert _texts(question)[question.answer] == by_device[device]


def test_the_power_source_answer_matches_its_own_record():
    assert len({s.source for s in POWER_SOURCES}) == len(POWER_SOURCES)
    for seed in range(SEEDS):
        question = generate("phys.generator_source_fluency", Random(seed))
        record = next(s for s in POWER_SOURCES if _stem(question).startswith(s.record))
        assert _texts(question)[question.answer] == record.source


def test_the_electricity_safety_proposal_matches_its_problem():
    assert len({p.method for p in ELECTRICITY_PROBLEMS}) == len(ELECTRICITY_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.electricity_safety_fluency", Random(seed))
        problem = next(p for p in ELECTRICITY_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method


# ── slice 24 ──────────────────────────────────────────────────────────────────

def test_the_medium_classification_matches_its_own_object():
    assert set(m.category for m in MEDIA) == set(CATEGORY_DESCRIPTIONS)
    for seed in range(SEEDS):
        question = generate("phys.light_medium_fluency", Random(seed))
        stem = _stem(question)
        item = next(m for m in MEDIA if (f"ถือ{m.name}บังตา" in stem and m.seen in stem) or f"ส่องไฟฉายผ่าน{m.name}ไปยังฉาก" in stem)
        assert _texts(question)[question.answer] == item.category


def test_the_hearing_medium_matches_its_own_record():
    assert len({m for _, m in HEARING_RECORDS}) == len(HEARING_RECORDS)
    for seed in range(SEEDS):
        question = generate("phys.hearing_medium_fluency", Random(seed))
        if not any(_stem(question).startswith(r[0]) for r in HEARING_RECORDS):
            continue  # Wave H's other branches are checked in test_science_wave_h.py
        record, medium = next(r for r in HEARING_RECORDS if _stem(question).startswith(r[0]))
        assert _texts(question)[question.answer] == medium


def test_the_pitch_answer_ties_faster_vibration_to_higher_pitch():
    for seed in range(SEEDS):
        question = generate("phys.pitch_fluency", Random(seed))
        if not _stem(question).startswith("นักเรียนดีดปลายไม้บรรทัด"):
            continue  # Wave H's length-table branch is checked in test_science_wave_h.py
        short, long_ = (int(n) for n in re.findall(r"(\d+) เซนติเมตร", _stem(question))[:2])
        assert short < long_
        assert _texts(question)[question.answer] == (
            "ส่วนที่สั่นถี่กว่า (ความถี่สูงกว่า) ทำให้เกิดเสียงสูงกว่า ส่วนที่สั่นห่างกว่า (ความถี่ต่ำกว่า) ทำให้เกิดเสียงต่ำกว่า")


# ── slice 25 ──────────────────────────────────────────────────────────────────

def test_the_loudness_answer_ties_bigger_amplitude_to_louder_sound():
    for seed in range(SEEDS):
        question = generate("phys.loudness_fluency", Random(seed))
        if "ครั้งแรกดีดแรง" not in _stem(question):
            continue  # Wave H's force table is checked in test_science_wave_h.py
        assert _texts(question)[question.answer] == (
            "การสั่นที่มีแอมพลิจูดมากกว่าทำให้เกิดเสียงดังกว่า การสั่นที่มีแอมพลิจูดน้อยกว่าทำให้เกิดเสียงค่อยกว่า")


def test_the_sound_level_ranking_is_always_ascending_by_decibel():
    ascending = sorted(SOUND_PLACES, key=lambda p: p.level)
    assert [p.level for p in ascending] == sorted(p.level for p in SOUND_PLACES)
    for seed in range(SEEDS):
        question = generate("phys.sound_level_fluency", Random(seed))
        shown = re.findall(r"(?:— | / )([^:/]+?): (\d+) เดซิเบล", _stem(question))
        assert len(shown) == 4, _stem(question)
        expected = " → ".join(name for name, _ in sorted(shown, key=lambda p: int(p[1])))
        assert _texts(question)[question.answer] == expected


def test_the_noise_pollution_proposal_matches_its_problem():
    assert len({p.method for p in NOISE_PROBLEMS}) == len(NOISE_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.noise_pollution_fluency", Random(seed))
        problem = next(p for p in NOISE_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method


def test_wo_two_three_po_five_is_complete():
    """Every ``ว 2.3 ป.5`` indicator holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.3 ป.5/"):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 5, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 26 ──────────────────────────────────────────────────────────────────

def test_the_circuit_part_function_pairing_is_consistent_both_ways():
    assert len({c.name for c in COMPONENTS}) == len(COMPONENTS)
    assert len({c.function for c in COMPONENTS}) == len(COMPONENTS)
    for seed in range(SEEDS):
        question = generate("phys.circuit_parts_foundation", Random(seed))
        part = next(c for c in COMPONENTS if _stem(question).endswith(c.function))
        assert _texts(question)[question.answer] == part.name


def test_the_circuit_part_evidence_answer_matches_its_own_component():
    for seed in range(SEEDS):
        question = generate("phys.circuit_parts_fluency", Random(seed))
        part = next(c for c in COMPONENTS if _stem(question).startswith(c.evidence))
        assert _texts(question)[question.answer] == part.function


def test_the_series_cells_answer_ties_more_cells_to_more_energy():
    for seed in range(SEEDS):
        question = generate("phys.series_cells_fluency", Random(seed))
        if not _stem(question).startswith("นักเรียนต่อวงจรโดยใช้เซลล์ไฟฟ้า 1 เซลล์"):
            continue  # Wave H's comparison and voltage branches are checked in test_science_wave_h.py
        assert _texts(question)[question.answer] == (
            "การต่อเซลล์ไฟฟ้าแบบอนุกรมทำให้พลังงานไฟฟ้ารวมในวงจรมากขึ้น หลอดไฟจึงสว่างขึ้น")


def test_the_series_cells_benefit_reason_matches_its_own_device():
    assert len({d.reason for d in SERIES_DEVICES}) == len(SERIES_DEVICES)
    for seed in range(SEEDS):
        question = generate("phys.series_cells_benefit_fluency", Random(seed))
        device = next(d for d in SERIES_DEVICES
                      if _stem(question) == f"เหตุใด{d.device}จึงมักต่อเซลล์ไฟฟ้าหลายเซลล์แบบอนุกรม")
        assert _texts(question)[question.answer] == device.reason


# ── slice 27 ──────────────────────────────────────────────────────────────────

def test_the_bulb_use_trait_matches_its_own_device():
    assert len({u.trait for u in BULB_USES}) == len(BULB_USES)
    for seed in range(SEEDS):
        question = generate("phys.parallel_bulbs_benefit_fluency", Random(seed))
        use = next(u for u in BULB_USES if _stem(question) == f"{u.device} มีประโยชน์และข้อจำกัดอย่างไร")
        assert _texts(question)[question.answer] == use.trait


def test_the_shadow_answer_ties_source_size_to_penumbra():
    for seed in range(SEEDS):
        question = generate("phys.shadow_fluency", Random(seed))
        if not _stem(question).startswith("นักเรียนใช้ไฟฉายขนาดเล็ก"):
            continue  # Wave H's distance-table branch is checked in test_science_wave_h.py
        assert _texts(question)[question.answer] == (
            "แหล่งกำเนิดแสงเป็นจุดทำให้เกิดเงามืดเพียงอย่างเดียว ส่วนแหล่งกำเนิดแสงขนาดใหญ่ทำให้เกิดทั้งเงามืดและเงามัว "
            "เพราะบางบริเวณได้รับแสงจากบางส่วนของแหล่งกำเนิดเท่านั้น")


def test_wo_two_three_is_complete_from_primary_to_po_six():
    """Every ``ว 2.3`` indicator from ป.1 to ป.6 holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.3 ป."):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 20, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 28 ──────────────────────────────────────────────────────────────────

def test_the_heat_quantity_answer_multiplies_all_three_given_values():
    for seed in range(SEEDS):
        question = generate("phys.heat_quantity_fluency", Random(seed))
        stem = _stem(question)
        mass = float(re.search(r"สารมวล ([\d.]+) กิโลกรัม", stem).group(1))
        specific_heat = float(re.search(r"ความร้อนจำเพาะ (\d+) จูล", stem).group(1))
        delta_t = float(re.search(r"เปลี่ยนแปลงไป (\d+) องศาเซลเซียส", stem).group(1))
        answer = _texts(question)[question.answer]
        assert answer == f"{mass * specific_heat * delta_t:g} จูล"


def test_the_expansion_problem_method_matches_its_own_case():
    assert len({p.method for p in EXPANSION_PROBLEMS}) == len(EXPANSION_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.thermal_expansion_benefit_fluency", Random(seed))
        problem = next(p for p in EXPANSION_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method


# ── slice 29 ──────────────────────────────────────────────────────────────────

def test_the_heat_mix_answer_is_the_mass_weighted_average():
    for m1, t1, m2, t2, tf in HEAT_MIX_COMBOS:
        assert m1 != m2
        assert (m1 * t1 + m2 * t2) / (m1 + m2) == tf
    for seed in range(SEEDS):
        question = generate("phys.heat_equilibrium_fluency", Random(seed))
        m1, t1, m2, t2 = (float(n) for n in re.findall(
            r"มวล ([\d.]+) กิโลกรัม อุณหภูมิ ([\d.]+) องศาเซลเซียส", _stem(question))[0] + re.findall(
            r"มวล ([\d.]+) กิโลกรัม อุณหภูมิ ([\d.]+) องศาเซลเซียส", _stem(question))[1])
        tf = (m1 * t1 + m2 * t2) / (m1 + m2)
        assert _texts(question)[question.answer] == f"{tf:g} องศาเซลเซียส"


def test_every_heat_transfer_mode_is_stated_truly():
    for seed in range(SEEDS):
        question = generate("phys.heat_transfer_mode_fluency", Random(seed))
        if not _stem(question).startswith("นักเรียนสังเกตเหตุการณ์สามอย่าง"):
            continue  # Wave H's single-event and two-event branches are checked in test_science_wave_h.py
        expected = " / ".join(f"{p.label}: {p.true}" for p in HEAT_TRANSFER_PARTS)
        assert _texts(question)[question.answer] == expected


def test_the_design_method_matches_its_own_problem():
    assert len({m for _, m in DESIGN_PROBLEMS}) == len(DESIGN_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.heat_transfer_design_fluency", Random(seed))
        case, method = next(p for p in DESIGN_PROBLEMS if _stem(question).startswith(p[0]))
        assert _texts(question)[question.answer] == method


def test_wo_two_three_mo_one_is_complete():
    """Every ``ว 2.3 ม.1`` indicator holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.3 ม.1/"):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 7, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 30 ──────────────────────────────────────────────────────────────────

def test_the_power_answer_divides_work_by_time():
    for force, distance, time, power in WORK_POWER_COMBOS:
        assert force * distance / time == power
    for seed in range(SEEDS):
        question = generate("phys.work_power_fluency", Random(seed))
        force, distance, time = (int(n) for n in re.findall(
            r"แรง (\d+) นิวตัน .*ระยะทาง (\d+) เมตร ในเวลา (\d+) วินาที", _stem(question))[0])
        assert _texts(question)[question.answer] == f"{force * distance / time:g} วัตต์"


def test_the_machine_principle_matches_its_own_evidence():
    assert len({m.principle for m in MACHINES}) == len(MACHINES)
    for seed in range(SEEDS):
        question = generate("phys.simple_machine_fluency", Random(seed))
        machine = next(m for m in MACHINES if m.evidence in _stem(question))
        assert _texts(question)[question.answer] == machine.principle


def test_the_machine_benefit_matches_its_own_device():
    assert len({u.benefit for u in MACHINE_USES}) == len(MACHINE_USES)
    for seed in range(SEEDS):
        question = generate("phys.simple_machine_benefit_fluency", Random(seed))
        use = next(u for u in MACHINE_USES if _stem(question) == f"{u.device} มีประโยชน์อย่างไร")
        assert _texts(question)[question.answer] == use.benefit


# ── slice 31 ──────────────────────────────────────────────────────────────────

def test_every_ke_pe_factor_part_is_stated_truly():
    for seed in range(SEEDS):
        question = generate("phys.ke_pe_factor_fluency", Random(seed))
        if not _stem(question).startswith("นักเรียนทำการทดลองสามชุด"):
            continue  # Wave H's one-experiment branch is checked in test_science_wave_h.py
        expected = " / ".join(f"{p.label}: {p.true}" for p in KE_PE_PARTS)
        assert _texts(question)[question.answer] == expected


def test_the_mechanical_energy_answer_names_the_fixed_total():
    for ke_a, ke_b in MECHANICAL_ENERGY_COMBOS:
        assert ke_a != ke_b
    for seed in range(SEEDS):
        question = generate("phys.mechanical_energy_fluency", Random(seed))
        stem = _stem(question)
        pe_a, ke_a, pe_b, ke_b = (int(n) for n in re.findall(
            r"พลังงานศักย์โน้มถ่วง (\d+) จูล พลังงานจลน์ (\d+) จูล", stem)[0] + re.findall(
            r"พลังงานศักย์โน้มถ่วง (\d+) จูล พลังงานจลน์ (\d+) จูล", stem)[1])
        total = pe_a + ke_a
        assert pe_b + ke_b == total
        change = ("พลังงานศักย์โน้มถ่วงเปลี่ยนเป็นพลังงานจลน์" if ke_b > ke_a
                  else "พลังงานจลน์เปลี่ยนเป็นพลังงานศักย์โน้มถ่วง")
        answer = _texts(question)[question.answer]
        assert answer == f"{change} โดยพลังงานกล (ผลรวมของทั้งสอง) คงตัวเท่ากับ {total} จูลทั้งสองจุด"


def test_the_energy_conservation_answer_names_its_own_split():
    for item in ENERGY_CONVERSIONS:
        assert item.value1 + item.value2 == item.total
    for seed in range(SEEDS):
        question = generate("phys.energy_conservation_fluency", Random(seed))
        item = next(i for i in ENERGY_CONVERSIONS if _stem(question).startswith(i.device))
        total = int(re.search(r"ป้อนเข้า (\d+) จูล", _stem(question)).group(1))
        k = total // item.total
        assert k * item.total == total
        answer = _texts(question)[question.answer]
        assert f"{item.output1} {item.value1 * k} จูล และ{item.output2} {item.value2 * k} จูล" in answer


def test_wo_two_three_mo_two_is_complete():
    """Every ``ว 2.3 ม.2`` indicator holds all three stages."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.3 ม.2/"):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 6, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 32 ──────────────────────────────────────────────────────────────────

def test_the_vi_graph_resistance_is_read_from_the_slope():
    for resistance, i1, i2, i3 in VI_GRAPH_COMBOS:
        assert round(2 / i1) == round(4 / i2) == round(6 / i3) == resistance
    for seed in range(SEEDS):
        question = generate("elec.vi_graph_fluency", Random(seed))
        stem = _stem(question)
        pairs = [(float(v), float(i)) for v, i in re.findall(r"(\d+) โวลต์: ([\d.]+) แอมแปร์", stem)]
        assert len(pairs) == 3
        slopes = {round(v / i, 6) for v, i in pairs}
        assert len(slopes) == 1, stem  # a constant resistor: every pair gives the same R
        resistance = slopes.pop()
        assert _texts(question)[question.answer] == f"กราฟเป็นเส้นตรงผ่านจุดกำเนิด มีความต้านทาน {resistance:g} โอห์ม"


def test_resistor_diagram_classification_matches_the_stated_current_pattern():
    for seed in range(SEEDS):
        question = generate("elec.resistor_diagram_fluency", Random(seed))
        stem = _stem(question)
        from otk.sets.physics.m3.resistor_diagram import PARALLEL_CUES, SERIES_CUES
        series = any(cue in stem for cue in SERIES_CUES)
        assert series != any(cue in stem for cue in PARALLEL_CUES), stem
        answer = _texts(question)[question.answer]
        assert answer.startswith("แบบอนุกรม" if series else "แบบขนาน")


# ── slice 33 ──────────────────────────────────────────────────────────────────

def test_the_electronic_component_function_pairing_is_consistent_both_ways():
    assert len({c.name for c in ELECTRONIC_COMPONENTS}) == len(ELECTRONIC_COMPONENTS)
    assert len({c.function for c in ELECTRONIC_COMPONENTS}) == len(ELECTRONIC_COMPONENTS)
    for seed in range(SEEDS):
        question = generate("elec.electronic_component_foundation", Random(seed))
        part = next(c for c in ELECTRONIC_COMPONENTS if _stem(question).endswith(c.function))
        assert _texts(question)[question.answer] == part.name


def test_the_electronic_component_evidence_answer_matches_its_own_component():
    for seed in range(SEEDS):
        question = generate("elec.electronic_component_fluency", Random(seed))
        part = next(c for c in ELECTRONIC_COMPONENTS if _stem(question).startswith(c.evidence))
        assert _texts(question)[question.answer] == part.function


def test_the_appliance_choice_method_matches_its_own_problem():
    assert len({p.method for p in APPLIANCE_PROBLEMS}) == len(APPLIANCE_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("elec.appliance_choice_fluency", Random(seed))
        problem = next(p for p in APPLIANCE_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method


def test_wo_two_three_is_complete_end_to_end():
    """Every ``ว 2.3`` indicator from ป.1 through ม.3 holds all three stages
    (``ม.5`` is Wave E)."""
    stages: dict[str, set[int]] = {}
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.startswith("ว 2.3 ") and not code.startswith("ว 2.3 ม.5/"):
                stages.setdefault(code, set()).add(row["learning_stage"])
    assert len(stages) == 54, sorted(stages)
    assert {code for code, seen in stages.items() if seen != {1, 2, 3}} == set()


# ── slice 34 ──────────────────────────────────────────────────────────────────

def test_the_light_meter_ratio_matches_the_stated_readings():
    for day, evening in LIGHT_METER_READINGS:
        assert day % evening == 0
    for seed in range(SEEDS):
        question = generate("phys.light_meter_fluency", Random(seed))
        day, evening = (int(n) for n in re.findall(
            r"ได้ (\d+) ลักซ์ในห้องเรียนช่วงกลางวัน และ (\d+) ลักซ์", _stem(question))[0])
        assert _texts(question)[question.answer] == f"ห้องเรียนช่วงกลางวันมีความสว่างมากกว่าช่วงเย็นถึง {day // evening} เท่า"


def test_the_brightness_arrangement_method_matches_its_own_case():
    assert len({p.method for p in LIGHT_ARRANGEMENT_PROBLEMS}) == len(LIGHT_ARRANGEMENT_PROBLEMS)
    for seed in range(SEEDS):
        question = generate("phys.brightness_arrangement_fluency", Random(seed))
        problem = next(p for p in LIGHT_ARRANGEMENT_PROBLEMS if _stem(question).startswith(p.case))
        assert _texts(question)[question.answer] == problem.method

"""Acceptance gate for Phase 5 Wave F — additional-course science.

Slice 1 opens the wave from ``openthaiknowledge-bank/Faii/ข้อสอบแรง.pdf``. The sheet's
conceptual half is already filed under ``ว 2.2 ม.2`` by Wave D; its calculating
half is what these sets cover, and it lands on four ``ฟิสิกส์เพิ่มเติม``
outcomes that stood at zero sets:

* ``ฟิสิกส์เพิ่มเติม 1 ม.4/7`` — สัมประสิทธิ์ความเสียดทาน, ``f = μN``;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/8`` — สมดุลกลและผลรวมของโมเมนต์;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/3`` — ความดันเกจและความดันสัมบูรณ์, ``P = ρgh``;
* ``ฟิสิกส์เพิ่มเติม 4 ม.6/4`` — แรงพยุงจากของไหล, ``F = ρVg``.

Slice 2 adds ``ฟิสิกส์เพิ่มเติม 1 ม.4/6`` — ``W = mg``, the formula the rest of
the sheet stands on, since every μ, pressure, buoyancy and moment question
converts a mass to a weight first.

Slices 3 and 4 work through ``ฟิสิกส์ 1`` in textbook order: ``ม.4/3``
(constant acceleration), ``ม.4/4`` (two forces at an angle), ``ม.4/5``
(Newton's laws applied), ``ม.4/10`` (work and power), ``ม.4/11`` (energy and
work), ``ม.4/12`` (conservation of mechanical energy) and ``ม.4/13`` (simple
machines). Every number is drawn so the answer is exact; ``numeric`` refuses a
repeating decimal outright.

Slices 5 and 6 close ``ฟิสิกส์ 1``: ``ม.4/9`` (centre of mass and
stability), ``ม.4/14`` (momentum and impulse), ``ม.4/15`` (collisions),
``ม.4/16`` (projectiles), ``ม.4/17`` (circular motion and satellites),
``ม.4/1`` (where physics came from) and ``ม.4/2`` (measurement and
straight-line graphs).

Slices 7 and 8 open ``ฟิสิกส์ 2`` at ``ม.5/1``-``/7``: simple harmonic
motion, natural frequency and resonance, waves and superposition, water
waves, sound and its speed, decibels, and pipes, beats, Doppler and shock
waves.

Slice 9 closes ``ฟิสิกส์ 2`` with ``ม.5/8`` (interference of light), ``ม.5/11``
(thin lenses), ``ม.5/12`` (light in the sky) and ``ม.5/13`` (colour); slice 10
opens ``ฟิสิกส์ 3`` with ``ม.5/1``-``/3``: charging, Coulomb's law and the
electric field.

Slices 11 and 12 continue ``ฟิสิกส์ 3``: capacitors, static electricity at
work, drift velocity, batteries in DC circuits, renewable electricity, and
at ``ม.6`` magnetic flux and the magnetic force. Directions by the
right-hand rule are checked as cross products in the page's frame.

Slices 13 and 14 close ``ฟิสิกส์ 3`` at ``ม.6/3``-``/8`` (motors and meters,
induction, rms values, transformers and three-phase power, polarisation, and
communication) and open ``ฟิสิกส์ 4`` with ``ม.6/1`` (heat).

Slices 15 and 16 continue ``ฟิสิกส์ 4``: elasticity, surface tension and
viscosity, fluids in motion, the gas laws, kinetic theory, the first law of
thermodynamics, and Planck and Bohr.

Slices 17 and 18 close ``ฟิสิกส์ 4`` and with it ``ฟิสิกส์เพิ่มเติม``: the
photoelectric effect, matter waves, radioactivity, half-life, binding energy,
fission and fusion, radiation at work and its safety, and particle physics.

Slices 19 and 20 open ``เคมีเพิ่มเติม``: atomic models, electron
configuration, periodic trends, transition metals, half-life, elements in use,
and ions with Lewis symbols. The strand is read from each outcome's code.

Slices 21 and 22 cover ionic and covalent compounds, ``เคมีเพิ่มเติม 1
ม.4/10``-``/16``: formulas and names, the Born-Haber cycle, ionic
properties, net ionic equations, Lewis structures, covalent names, and bond
energies.

Slices 23 and 24 cover ``เคมีเพิ่มเติม 1 ม.4/17``-``/21`` and ``ม.5/1``-``/2``:
molecular shape and polarity, forces between molecules, network solids,
metallic bonding, comparing bond types, and the gas laws.

Slices 25 and 26 cover ``เคมีเพิ่มเติม 1 ม.5/3``-``/6`` and ``ม.6/1``-``/3``:
the ideal gas law, Dalton's and Graham's laws, gases at work, bonds in
everyday organic compounds, structural formulas, and functional groups.

Slices 27 and 28 cover ``เคมีเพิ่มเติม 1 ม.6/4``-``/8``, ``ม.6/10`` and ``/11``:
IUPAC names, isomers, boiling points, hydrocarbon and ester reactions, uses,
and polymerisation, all drawn from one bank of compounds.

Slices 29 and 30 cover ``เคมีเพิ่มเติม 1 ม.6/12``, ``/14`` and ``/15`` (polymer
structure, modification and waste) and open ``เคมีเพิ่มเติม 2`` with ``ม.4/1``-``/4``:
balancing and stoichiometry by mass, concentration and gas volume.

Slices 31 and 32 cover ``เคมีเพิ่มเติม 2 ม.4/5``-``/7`` (multi-step
stoichiometry, the limiting reagent, percent yield) and the rate outcomes
``ม.5/2``, ``/3``, ``/5`` and ``/6``.

Slices 33 and 34 cover ``เคมีเพิ่มเติม 2 ม.5/1``, ``/7`` and ``/8`` (rate graphs,
reversible reactions, the approach to equilibrium) and ``ม.5/9``-``/12`` (K,
equilibrium concentrations, multi-step K, Le Chatelier).

Slices 35 and 36 cover ``เคมีเพิ่มเติม 2 ม.5/13``-``/19``: equilibrium at work,
acid-base theories and conjugate pairs, strength, pH, neutralisation and salt
hydrolysis.

Slices 37 and 38 cover ``เคมีเพิ่มเติม 2 ม.5/20``-``/26``: titration and
indicators, buffers, acids and bases at work, oxidation numbers, redox agents
and half-equations, and comparing reducing and oxidising strength.

Slices 39 and 40 finish ``เคมีเพิ่มเติม 2`` with ``ม.5/27``-``/32`` (balancing
redox, cells and E°, batteries, electrolysis, new cell technology) and open
``เคมีเพิ่มเติม 3`` with ``ม.4/1`` (lab safety).

Slices 41 and 42 cover ``เคมีเพิ่มเติม 3 ม.4/2`` and ``/4``-``/9``: lab
equipment, units, atomic mass, the mole, definite proportions, empirical
formulas and concentration units.

Slices 43 and 44 finish ``เคมีเพิ่มเติม`` with ``เคมีเพิ่มเติม 3 ม.4/10``-``/11``
(solution preparation, boiling and freezing points) and open
``ชีววิทยาเพิ่มเติม 1`` with ``ม.4/1``-``/5``.

Slices 45 and 46 cover ``ชีววิทยาเพิ่มเติม 1 ม.4/6``-``/12``: lipids, nucleic
acids, metabolism, enzymes, the light microscope, cell boundaries and
organelles.

Slices 47 and 48 finish ``ชีววิทยาเพิ่มเติม 1`` with ``ม.4/13``-``/17`` (nucleus,
membrane and bulk transport, cell division, respiration) and open
``ชีววิทยาเพิ่มเติม 2`` with Mendel (``ม.4/1``-``/2``).

Slices 49 and 50 carry ``ชีววิทยาเพิ่มเติม 2`` through ``ม.4/3``-``/9``
(beyond Mendel, variation, sex linkage, DNA, protein synthesis, gene to
trait, mutation).

Slices 51 and 52 carry ``ชีววิทยาเพิ่มเติม 2`` through ``ม.4/10``-``/15``
and ``ม.6/1`` (gene technology, evolution, population genetics, speciation,
biodiversity).

Slices 53 and 54 finish ``ชีววิทยาเพิ่มเติม 2`` with ``ม.6/2``-``/5`` (first
cells, the groups of life, naming, keys) and open ``ชีววิทยาเพิ่มเติม 3`` with
``ม.5/1``-``/3`` (plant tissues, roots, stems).

Slices 55 and 56 carry ``ชีววิทยาเพิ่มเติม 3`` through ``ม.5/4``-``/10`` (leaf,
transpiration, water and nutrients, phloem, the photosynthesis experiments,
C3).

Slices 57 and 58 carry ``ชีววิทยาเพิ่มเติม 3`` through ``ม.5/11``-``/17`` (C4
and CAM, limiting factors, the flower's life cycle and gametes, seeds and
fruits, germination, hormones).

Slices 59 and 60 finish ``ชีววิทยาเพิ่มเติม 3`` with ``ม.5/18`` (responses to
stimuli) and open ``ชีววิทยาเพิ่มเติม 4`` with ``ม.5/1``-``/6`` (digestion and
gas exchange).

Slices 61 and 62 carry ``ชีววิทยาเพิ่มเติม 4`` through ``ม.5/7``-``/13``
(breathing volumes, circulation, the heart, blood and transfusion).

Slices 63 and 64 carry ``ชีววิทยาเพิ่มเติม 4`` through ``ม.5/14``-``/20`` (lymph,
immunity, immune disorders, excretion, the kidney and the nephron).

Slices 65 and 66 carry ``ชีววิทยาเพิ่มเติม 4`` through ``ม.5/21`` and
``ม.6/1``-``/6`` (kidney disease, nervous systems, the neuron and impulse,
CNS and PNS, the brain, the autonomic system).

Slices 67 and 68 carry ``ชีววิทยาเพิ่มเติม 4`` through ``ม.6/7``-``/13`` (senses,
the blind spot, locomotion, bones and muscles, joints, reproduction).

Slices 69 and 70 finish ``ชีววิทยาเพิ่มเติม 4`` with ``ม.6/14``-``/19`` (gametes,
embryos, hormones, behaviour, communication) and open ``ชีววิทยาเพิ่มเติม 5``
with ``ม.6/1`` (energy flow).

Slices 71 and 72 carry ``ชีววิทยาเพิ่มเติม 5`` through ``ม.6/2``-``/8``
(biomagnification, nutrient cycles, biomes, succession, populations).

Slices 73 and 74 finish ``ชีววิทยาเพิ่มเติม 5`` with ``ม.6/9``-``/13`` (water,
air, soil, forests, wildlife) and open ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1``
with ``ม.4/1``-``/2`` (the Earth's layers, drift evidence).

Slices 75 and 76 carry ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1`` through
``ม.4/3``-``/9`` (plate boundaries, rock history, volcanoes, earthquakes,
tsunamis, minerals, rocks).

Slices 77 and 78 finish ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1`` with
``ม.4/10``-``/12`` (fossil fuels and maps) and open ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2``
with ``ม.5/1``-``/4`` (sunlight, energy balance, forces on air, the cells).

Slices 79 and 80 carry ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2`` through
``ม.5/5``-``/11`` (ocean layers and currents, their effects, air stability,
fronts, and climate change).

Slices 81 and 82 finish ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2`` with
``ม.5/12``-``/13`` (weather maps and forecasting) and open
``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3`` with ``ม.6/1``-``/5`` (the early universe,
its evidence, the Milky Way, star birth and fusion).

Slices 83 and 84 carry ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3`` through
``ม.6/6``-``/12`` (magnitude, colour, parallax, the H-R diagram, the solar
system's birth, Kepler's laws, and solar storms).

Slices 85 and 86 finish ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3`` with
``ม.6/13``-``/19`` (the celestial sphere, star paths, solar time, time zones,
elongation, space exploration, and planning a stargazing night).

An additional-course outcome is filed whole, so every set here is
``additional_outcome`` — there is no exact/standard_scope grammar to check, and
the filing tests instead pin the course, the level, and the unit.

The content tests parse the numbers back out of each generated stem and redo
the physics from them, rather than re-reading the module's own pools. That is
what catches a stem whose wording and whose answer have drifted apart — and it
is the check that found the two wrong answers in the source sheet itself
(recorded in :mod:`otk.sets._support.science_wave_f1`).
"""

from __future__ import annotations

import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate
from otk.core.curriculum_science import (
    ADDITIONAL,
    REVIEW_PENDING,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_PLACEMENTS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_C_KEYS,
    SCIENCE_WAVE_D_KEYS,
    SCIENCE_WAVE_E_KEYS,
    SCIENCE_WAVE_F_APPROVED_KEYS,
    SCIENCE_WAVE_F_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.core.registry import REGISTRY
from otk.sets.physics.m6.gauge_pressure import ATM
from otk.sets.physics.m4.friction_coefficient import FRICTION_POOL
from otk.sets._support.science_wave_f1 import G
from otk.sets.physics.m4.weight_gravity import EARTH_G, PLACES


SEEDS = 300


def _triple(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}_{stage}" for stage in ("foundation", "fluency", "application"))


INDICATORS = {
    "ฟิสิกส์เพิ่มเติม 1 ม.4/7": _triple("phys.friction_coefficient"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/8": _triple("phys.mechanical_equilibrium"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/3": _triple("phys.gauge_pressure"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/4": _triple("phys.fluid_buoyancy"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/6": _triple("phys.weight_gravity"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/3": _triple("phys.uniform_accel"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/4": _triple("phys.force_angle"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/5": _triple("phys.newton_applied"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/10": _triple("phys.work_graph"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/11": _triple("phys.work_energy"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/12": _triple("phys.energy_conservation_calc"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/13": _triple("phys.machine_advantage"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/9": _triple("phys.centre_of_mass"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/14": _triple("phys.momentum_impulse"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/15": _triple("phys.collision_1d"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/16": _triple("phys.projectile"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/17": _triple("phys.circular_motion"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/1": _triple("phys.physics_history"),
    "ฟิสิกส์เพิ่มเติม 1 ม.4/2": _triple("phys.measurement_graph"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/1": _triple("phys.shm"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/2": _triple("phys.natural_frequency"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/3": _triple("phys.wave_superposition"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/4": _triple("phys.water_wave"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/5": _triple("phys.sound_propagation"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/6": _triple("phys.sound_decibel"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/7": _triple("phys.sound_resonance_tube"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/8": _triple("phys.light_interference"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/11": _triple("phys.thin_lens"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/12": _triple("phys.light_phenomena"),
    "ฟิสิกส์เพิ่มเติม 2 ม.5/13": _triple("phys.colour_perception"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/1": _triple("phys.charging"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/2": _triple("phys.coulomb_force"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/3": _triple("phys.electric_field"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/5": _triple("phys.capacitor"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/6": _triple("phys.electrostatic_use"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/7": _triple("phys.drift_current"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/10": _triple("phys.battery_emf"),
    "ฟิสิกส์เพิ่มเติม 3 ม.5/11": _triple("phys.renewable_electricity"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/1": _triple("phys.magnetic_flux"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/2": _triple("phys.magnetic_force_charge"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/3": _triple("phys.motor_galvanometer"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/4": _triple("phys.faraday_induction"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/5": _triple("phys.ac_rms"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/6": _triple("phys.transformer_threephase"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/7": _triple("phys.polarisation_em"),
    "ฟิสิกส์เพิ่มเติม 3 ม.6/8": _triple("phys.signal_communication"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/1": _triple("phys.heat_calorimetry"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/2": _triple("phys.elasticity_modulus"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/5": _triple("phys.surface_tension"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/6": _triple("phys.bernoulli_flow"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/7": _triple("phys.ideal_gas_law"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/8": _triple("phys.kinetic_gas"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/9": _triple("phys.thermo_first_law"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/10": _triple("phys.bohr_spectrum"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/11": _triple("phys.photoelectric"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/12": _triple("phys.de_broglie"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/13": _triple("phys.alpha_beta_gamma"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/14": _triple("phys.half_life_decay"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/15": _triple("phys.binding_energy"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/16": _triple("phys.fission_fusion"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/17": _triple("phys.radiation_safety"),
    "ฟิสิกส์เพิ่มเติม 4 ม.6/18": _triple("phys.particle_standard_model"),
    "เคมีเพิ่มเติม 1 ม.4/1": _triple("chem.atomic_model_history"),
    "เคมีเพิ่มเติม 1 ม.4/3": _triple("chem.electron_config"),
    "เคมีเพิ่มเติม 1 ม.4/5": _triple("chem.periodic_trend"),
    "เคมีเพิ่มเติม 1 ม.4/6": _triple("chem.transition_metal"),
    "เคมีเพิ่มเติม 1 ม.4/7": _triple("chem.half_life_calc"),
    "เคมีเพิ่มเติม 1 ม.4/8": _triple("chem.element_application"),
    "เคมีเพิ่มเติม 1 ม.4/9": _triple("chem.ionic_lewis"),
    "เคมีเพิ่มเติม 1 ม.4/10": _triple("chem.ionic_naming"),
    "เคมีเพิ่มเติม 1 ม.4/11": _triple("chem.born_haber"),
    "เคมีเพิ่มเติม 1 ม.4/12": _triple("chem.ionic_property"),
    "เคมีเพิ่มเติม 1 ม.4/13": _triple("chem.net_ionic"),
    "เคมีเพิ่มเติม 1 ม.4/14": _triple("chem.covalent_lewis"),
    "เคมีเพิ่มเติม 1 ม.4/15": _triple("chem.covalent_naming"),
    "เคมีเพิ่มเติม 1 ม.4/16": _triple("chem.bond_energy"),
    "เคมีเพิ่มเติม 1 ม.4/17": _triple("chem.vsepr_shape"),
    "เคมีเพิ่มเติม 1 ม.4/18": _triple("chem.intermolecular_force"),
    "เคมีเพิ่มเติม 1 ม.4/19": _triple("chem.network_covalent"),
    "เคมีเพิ่มเติม 1 ม.4/20": _triple("chem.metallic_bond"),
    "เคมีเพิ่มเติม 1 ม.4/21": _triple("chem.bond_type_compare"),
    "เคมีเพิ่มเติม 1 ม.5/1": _triple("chem.gas_law"),
    "เคมีเพิ่มเติม 1 ม.5/2": _triple("chem.combined_gas"),
    "เคมีเพิ่มเติม 1 ม.5/3": _triple("chem.ideal_gas"),
    "เคมีเพิ่มเติม 1 ม.5/4": _triple("chem.dalton_pressure"),
    "เคมีเพิ่มเติม 1 ม.5/5": _triple("chem.graham_diffusion"),
    "เคมีเพิ่มเติม 1 ม.5/6": _triple("chem.gas_application"),
    "เคมีเพิ่มเติม 1 ม.6/1": _triple("chem.organic_bond"),
    "เคมีเพิ่มเติม 1 ม.6/2": _triple("chem.structural_formula"),
    "เคมีเพิ่มเติม 1 ม.6/3": _triple("chem.functional_group"),
    "เคมีเพิ่มเติม 1 ม.6/4": _triple("chem.iupac_name"),
    "เคมีเพิ่มเติม 1 ม.6/5": _triple("chem.structural_isomer"),
    "เคมีเพิ่มเติม 1 ม.6/6": _triple("chem.organic_property"),
    "เคมีเพิ่มเติม 1 ม.6/7": _triple("chem.hydrocarbon_reaction"),
    "เคมีเพิ่มเติม 1 ม.6/8": _triple("chem.ester_amide"),
    "เคมีเพิ่มเติม 1 ม.6/10": _triple("chem.organic_use"),
    "เคมีเพิ่มเติม 1 ม.6/11": _triple("chem.polymerization"),
    "เคมีเพิ่มเติม 1 ม.6/12": _triple("chem.polymer_structure"),
    "เคมีเพิ่มเติม 1 ม.6/14": _triple("chem.polymer_modify"),
    "เคมีเพิ่มเติม 1 ม.6/15": _triple("chem.polymer_waste"),
    "เคมีเพิ่มเติม 2 ม.4/1": _triple("chem.equation_balance"),
    "เคมีเพิ่มเติม 2 ม.4/2": _triple("chem.stoich_mass"),
    "เคมีเพิ่มเติม 2 ม.4/3": _triple("chem.stoich_solution"),
    "เคมีเพิ่มเติม 2 ม.4/4": _triple("chem.stoich_gas"),
    "เคมีเพิ่มเติม 2 ม.4/5": _triple("chem.stoich_multistep"),
    "เคมีเพิ่มเติม 2 ม.4/6": _triple("chem.limiting_reagent"),
    "เคมีเพิ่มเติม 2 ม.4/7": _triple("chem.percent_yield"),
    "เคมีเพิ่มเติม 2 ม.5/2": _triple("chem.rate_calc"),
    "เคมีเพิ่มเติม 2 ม.5/3": _triple("chem.collision_theory"),
    "เคมีเพิ่มเติม 2 ม.5/5": _triple("chem.rate_compare"),
    "เคมีเพิ่มเติม 2 ม.5/6": _triple("chem.rate_application"),
    "เคมีเพิ่มเติม 2 ม.5/1": _triple("chem.rate_graph"),
    "เคมีเพิ่มเติม 2 ม.5/7": _triple("chem.reversible_equilibrium"),
    "เคมีเพิ่มเติม 2 ม.5/8": _triple("chem.equilibrium_approach"),
    "เคมีเพิ่มเติม 2 ม.5/9": _triple("chem.equilibrium_constant"),
    "เคมีเพิ่มเติม 2 ม.5/10": _triple("chem.equilibrium_concentration"),
    "เคมีเพิ่มเติม 2 ม.5/11": _triple("chem.equilibrium_multistep"),
    "เคมีเพิ่มเติม 2 ม.5/12": _triple("chem.le_chatelier"),
    "เคมีเพิ่มเติม 2 ม.5/13": _triple("chem.equilibrium_life"),
    "เคมีเพิ่มเติม 2 ม.5/14": _triple("chem.acid_base_theory"),
    "เคมีเพิ่มเติม 2 ม.5/15": _triple("chem.conjugate_pair"),
    "เคมีเพิ่มเติม 2 ม.5/16": _triple("chem.acid_strength"),
    "เคมีเพิ่มเติม 2 ม.5/17": _triple("chem.ph_calc"),
    "เคมีเพิ่มเติม 2 ม.5/18": _triple("chem.neutralization"),
    "เคมีเพิ่มเติม 2 ม.5/19": _triple("chem.salt_hydrolysis"),
    "เคมีเพิ่มเติม 2 ม.5/20": _triple("chem.titration_indicator"),
    "เคมีเพิ่มเติม 2 ม.5/21": _triple("chem.titration_calc"),
    "เคมีเพิ่มเติม 2 ม.5/22": _triple("chem.buffer"),
    "เคมีเพิ่มเติม 2 ม.5/23": _triple("chem.acid_base_use"),
    "เคมีเพิ่มเติม 2 ม.5/24": _triple("chem.oxidation_number"),
    "เคมีเพิ่มเติม 2 ม.5/25": _triple("chem.redox_agent"),
    "เคมีเพิ่มเติม 2 ม.5/26": _triple("chem.redox_series"),
    "เคมีเพิ่มเติม 2 ม.5/27": _triple("chem.redox_balance"),
    "เคมีเพิ่มเติม 2 ม.5/28": _triple("chem.electrochemical_cell"),
    "เคมีเพิ่มเติม 2 ม.5/29": _triple("chem.cell_potential"),
    "เคมีเพิ่มเติม 2 ม.5/30": _triple("chem.battery_type"),
    "เคมีเพิ่มเติม 2 ม.5/31": _triple("chem.electrolysis"),
    "เคมีเพิ่มเติม 2 ม.5/32": _triple("chem.cell_technology"),
    "เคมีเพิ่มเติม 3 ม.4/1": _triple("chem.lab_safety"),
    "เคมีเพิ่มเติม 3 ม.4/2": _triple("chem.lab_equipment"),
    "เคมีเพิ่มเติม 3 ม.4/4": _triple("chem.unit_conversion"),
    "เคมีเพิ่มเติม 3 ม.4/5": _triple("chem.atomic_mass"),
    "เคมีเพิ่มเติม 3 ม.4/6": _triple("chem.mole_relation"),
    "เคมีเพิ่มเติม 3 ม.4/7": _triple("chem.definite_proportion"),
    "เคมีเพิ่มเติม 3 ม.4/8": _triple("chem.empirical_formula"),
    "เคมีเพิ่มเติม 3 ม.4/9": _triple("chem.solution_units"),
    "เคมีเพิ่มเติม 3 ม.4/10": _triple("chem.solution_prep"),
    "เคมีเพิ่มเติม 3 ม.4/11": _triple("chem.colligative"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/1": _triple("biology.life_property"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/2": _triple("biology.scientific_method"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/3": _triple("biology.water_element"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/4": _triple("biology.carbohydrate"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/5": _triple("biology.protein"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/6": _triple("biology.lipid"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/7": _triple("biology.nucleic_acid"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/8": _triple("biology.metabolism"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/9": _triple("biology.enzyme"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/10": _triple("biology.microscope"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/11": _triple("biology.cell_boundary"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/12": _triple("biology.organelle"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/13": _triple("biology.nucleus"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/14": _triple("biology.membrane_transport"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/15": _triple("biology.bulk_transport"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/16": _triple("biology.cell_division"),
    "ชีววิทยาเพิ่มเติม 1 ม.4/17": _triple("biology.respiration"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/1": _triple("biology.mendel_experiment"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/2": _triple("biology.mendel_law"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/3": _triple("biology.mendel_extension"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/4": _triple("biology.variation"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/5": _triple("biology.chromosome_inheritance"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/6": _triple("biology.dna_replication"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/7": _triple("biology.gene_expression"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/8": _triple("biology.gene_to_trait"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/9": _triple("biology.mutation"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/10": _triple("biology.recombinant_dna"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/11": _triple("biology.dna_technology_use"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/12": _triple("biology.evolution_evidence"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/13": _triple("biology.evolution_theory"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/14": _triple("biology.hardy_weinberg"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/15": _triple("biology.speciation"),
    "ชีววิทยาเพิ่มเติม 2 ม.6/1": _triple("biology.biodiversity"),
    "ชีววิทยาเพิ่มเติม 2 ม.6/2": _triple("biology.first_cells"),
    "ชีววิทยาเพิ่มเติม 2 ม.6/3": _triple("biology.life_groups"),
    "ชีววิทยาเพิ่มเติม 2 ม.6/4": _triple("biology.taxonomy"),
    "ชีววิทยาเพิ่มเติม 2 ม.6/5": _triple("biology.dichotomous_key"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/1": _triple("biology.plant_tissue"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/2": _triple("biology.root_structure"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/3": _triple("biology.stem_structure"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/4": _triple("biology.leaf_structure"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/5": _triple("biology.transpiration"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/6": _triple("biology.water_transport"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/7": _triple("biology.plant_nutrient"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/8": _triple("biology.food_transport"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/9": _triple("biology.photosynthesis_history"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/10": _triple("biology.photosynthesis_c3"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/11": _triple("biology.c4_cam"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/12": _triple("biology.photosynthesis_factor"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/13": _triple("biology.plant_life_cycle"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/14": _triple("biology.plant_gamete"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/15": _triple("biology.seed_fruit"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/16": _triple("biology.germination"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/17": _triple("biology.plant_hormone"),
    "ชีววิทยาเพิ่มเติม 3 ม.5/18": _triple("biology.plant_response"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/1": _triple("biology.animal_digestion"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/2": _triple("biology.hydra_planaria"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/3": _triple("biology.human_digestion"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/4": _triple("biology.animal_gas_exchange"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/5": _triple("biology.mammal_lung"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/6": _triple("biology.human_gas_exchange"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/7": _triple("biology.lung_volume"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/8": _triple("biology.circulation_type"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/9": _triple("biology.fish_tail_blood"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/10": _triple("biology.heart_vessel"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/11": _triple("biology.heart_flow"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/12": _triple("biology.blood_component"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/13": _triple("biology.blood_transfusion"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/14": _triple("biology.lymph"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/15": _triple("biology.immune_defense"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/16": _triple("biology.immunization"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/17": _triple("biology.immune_disorder"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/18": _triple("biology.animal_excretion"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/19": _triple("biology.kidney_structure"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/20": _triple("biology.nephron"),
    "ชีววิทยาเพิ่มเติม 4 ม.5/21": _triple("biology.kidney_disease"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/1": _triple("biology.animal_nervous"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/2": _triple("biology.neuron"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/3": _triple("biology.nerve_impulse"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/4": _triple("biology.cns_pns"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/5": _triple("biology.brain"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/6": _triple("biology.autonomic"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/7": _triple("biology.sense_organ"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/8": _triple("biology.blind_spot"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/9": _triple("biology.animal_locomotion"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/10": _triple("biology.skeleton_muscle"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/11": _triple("biology.joint_muscle"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/12": _triple("biology.animal_reproduction"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/13": _triple("biology.reproductive_system"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/14": _triple("biology.gametogenesis"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/15": _triple("biology.embryo_development"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/16": _triple("biology.hormone"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/17": _triple("biology.animal_behavior"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/18": _triple("biology.behavior_evolution"),
    "ชีววิทยาเพิ่มเติม 4 ม.6/19": _triple("biology.animal_communication"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/1": _triple("biology.energy_flow"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/2": _triple("biology.biomagnification"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/3": _triple("biology.nutrient_cycle"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/4": _triple("biology.biome"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/5": _triple("biology.succession"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/6": _triple("biology.population_trait"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/7": _triple("biology.population_growth"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/8": _triple("biology.population_control"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/9": _triple("biology.water_resource"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/10": _triple("biology.air_pollution"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/11": _triple("biology.soil_resource"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/12": _triple("biology.forest_conservation"),
    "ชีววิทยาเพิ่มเติม 5 ม.6/13": _triple("biology.wildlife_conservation"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/1": _triple("geo.layered_earth"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/2": _triple("geo.drift_evidence"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/3": _triple("geo.plate_margin"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/4": _triple("geo.geologic_history"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/5": _triple("geo.eruption_style"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/6": _triple("geo.quake_magnitude"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/7": _triple("geo.tsunami_wave"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/8": _triple("geo.mineral_id"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/9": _triple("geo.rock_id"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/10": _triple("geo.petroleum_coal"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/11": _triple("geo.fossil_product"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/12": _triple("geo.geologic_map"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/1": _triple("geo.solar_heating"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/2": _triple("geo.energy_balance"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/3": _triple("geo.air_force"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/4": _triple("geo.latitude_wind"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/5": _triple("geo.ocean_layer"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/6": _triple("geo.ocean_current"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/7": _triple("geo.current_effect"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/8": _triple("geo.air_stability"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/9": _triple("geo.weather_front"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/10": _triple("geo.climate_factor"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/11": _triple("geo.climate_mitigation"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/12": _triple("geo.station_model"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/13": _triple("geo.weather_outlook"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/1": _triple("astro.cosmic_timeline"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/2": _triple("astro.hubble_law"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/3": _triple("astro.galaxy_structure"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/4": _triple("astro.protostar"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/5": _triple("astro.fusion_chain"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/6": _triple("astro.magnitude_scale"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/7": _triple("astro.star_color"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/8": _triple("astro.parallax"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/9": _triple("astro.hr_diagram"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/10": _triple("astro.habitable_zone"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/11": _triple("astro.kepler_law"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/12": _triple("astro.solar_storm"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/13": _triple("astro.celestial_sphere"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/14": _triple("astro.star_path"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/15": _triple("astro.apparent_solar_time"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/16": _triple("astro.time_zone"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/17": _triple("astro.elongation"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/18": _triple("astro.space_telescope"),
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/19": _triple("astro.stargazing_plan"),
}

TOPICS = {
    "ฟิสิกส์เพิ่มเติม 1 ม.4/7": "แรงเสียดทานและสัมประสิทธิ์ความเสียดทาน",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/8": "สมดุลกลและผลรวมของโมเมนต์",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/3": "ความดันเกจและความดันสัมบูรณ์",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/4": "แรงพยุงจากของไหล",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/6": "น้ำหนักของวัตถุในสนามโน้มถ่วง",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/3": "การเคลื่อนที่แนวตรงด้วยความเร่งคงตัว",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/4": "แรงลัพธ์ของแรงสองแรงที่ทำมุมต่อกัน",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/5": "กฎการเคลื่อนที่ของนิวตันและการนำไปใช้",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/10": "งานของแรงคงตัวและกำลังเฉลี่ย",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/11": "พลังงานจลน์ พลังงานศักย์ และความสัมพันธ์ระหว่างงานกับพลังงาน",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/12": "กฎการอนุรักษ์พลังงานกล",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/13": "การได้เปรียบเชิงกลและประสิทธิภาพของเครื่องกลอย่างง่าย",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/9": "ศูนย์กลางมวล ศูนย์ถ่วง และเสถียรภาพของวัตถุ",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/14": "โมเมนตัม การดล และแรงดล",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/15": "การชนและการดีดตัวแยกจากกันในหนึ่งมิติ",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/16": "การเคลื่อนที่แบบโพรเจกไทล์",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/17": "การเคลื่อนที่แบบวงกลมและการโคจรของดาวเทียม",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/1": "ประวัติและพัฒนาการของความรู้ทางฟิสิกส์",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/2": "การวัด ความคลาดเคลื่อน และการวิเคราะห์กราฟเส้นตรง",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/1": "การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/2": "ความถี่ธรรมชาติและการสั่นพ้อง",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/3": "ชนิด ส่วนประกอบ และการซ้อนทับของคลื่น",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/4": "การสะท้อน การหักเห การแทรกสอด และการเลี้ยวเบนของคลื่นผิวน้ำ",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/5": "การเกิดและการเคลื่อนที่ของเสียง และสมบัติของคลื่นเสียง",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/6": "ความเข้มเสียง ระดับความเข้มเสียง และการได้ยิน",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/7": "การสั่นพ้องของอากาศในท่อ บีต คลื่นนิ่ง ปรากฏการณ์ดอปเพลอร์ และคลื่นกระแทก",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/8": "การแทรกสอดและการเลี้ยวเบนของแสง",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/11": "ภาพจากเลนส์บางและการนำไปใช้",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/12": "ปรากฏการณ์ธรรมชาติที่เกี่ยวกับแสง",
    "ฟิสิกส์เพิ่มเติม 2 ม.5/13": "การมองเห็นสี สีของวัตถุ การผสมสารสีและแสงสี และการบอดสี",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/1": "การทำให้วัตถุมีประจุไฟฟ้า",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/2": "แรงไฟฟ้าตามกฎของคูลอมบ์",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/3": "สนามไฟฟ้าและแรงไฟฟ้าที่กระทำต่อประจุในสนามไฟฟ้า",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/5": "ตัวเก็บประจุและความจุไฟฟ้า",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/6": "การนำความรู้เรื่องไฟฟ้าสถิตไปใช้",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/7": "กระแสไฟฟ้าในลวดตัวนำและความเร็วลอยเลื่อนของอิเล็กตรอน",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/10": "อีเอ็มเอฟสมมูลและวงจรไฟฟ้ากระแสตรง",
    "ฟิสิกส์เพิ่มเติม 3 ม.5/11": "การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/1": "สนามแม่เหล็กและฟลักซ์แม่เหล็ก",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/2": "แรงแม่เหล็กที่กระทำต่อประจุและเส้นลวดที่มีกระแสไฟฟ้า",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/3": "หลักการทำงานของแกลแวนอมิเตอร์และมอเตอร์ไฟฟ้ากระแสตรง",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/4": "อีเอ็มเอฟเหนี่ยวนำและกฎการเหนี่ยวนำของฟาราเดย์",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/5": "ความต่างศักย์และกระแสไฟฟ้าอาร์เอ็มเอส",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/6": "เครื่องกำเนิดไฟฟ้ากระแสสลับ 3 เฟสและหม้อแปลง",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/7": "คลื่นแม่เหล็กไฟฟ้า แสงโพลาไรส์ และการนำไปใช้",
    "ฟิสิกส์เพิ่มเติม 3 ม.6/8": "การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้าและสัญญาณแอนะล็อกกับดิจิทัล",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/1": "ความร้อนกับการเปลี่ยนอุณหภูมิและสถานะของสสาร",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/2": "สภาพยืดหยุ่น ความเค้น ความเครียด และมอดุลัสของยัง",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/5": "ความตึงผิวและแรงหนืดของของเหลว",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/6": "ของไหลอุดมคติ สมการความต่อเนื่อง และสมการแบร์นูลลี",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/7": "กฎของแก๊สอุดมคติ",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/8": "ทฤษฎีจลน์ของแก๊สและอัตราเร็วอาร์เอ็มเอส",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/9": "งาน ความร้อน และพลังงานภายในระบบ",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/10": "สมมติฐานของพลังค์ แบบจำลองอะตอมของโบร์ และสเปกตรัมไฮโดรเจน",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/11": "ปรากฏการณ์โฟโตอิเล็กทริก",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/12": "ทวิภาวะของคลื่นและอนุภาคและความยาวคลื่นเดอบรอยล์",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/13": "กัมมันตภาพรังสีและรังสีแอลฟา บีตา แกมมา",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/14": "การสลายของนิวเคลียสกัมมันตรังสีและครึ่งชีวิต",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/15": "แรงนิวเคลียร์ เสถียรภาพของนิวเคลียส และพลังงานยึดเหนี่ยว",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/16": "ปฏิกิริยานิวเคลียร์ฟิชชันและฟิวชัน",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/17": "ประโยชน์ อันตราย และการป้องกันรังสี",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/18": "ฟิสิกส์อนุภาคและแบบจำลองมาตรฐาน",
    "เคมีเพิ่มเติม 1 ม.4/1": "วิวัฒนาการของแบบจำลองอะตอม",
    "เคมีเพิ่มเติม 1 ม.4/3": "การจัดเรียงอิเล็กตรอนในอะตอม",
    "เคมีเพิ่มเติม 1 ม.4/5": "แนวโน้มสมบัติของธาตุเรพรีเซนเททีฟ",
    "เคมีเพิ่มเติม 1 ม.4/6": "สมบัติของธาตุแทรนซิชัน",
    "เคมีเพิ่มเติม 1 ม.4/7": "สมบัติของไอโซโทปกัมมันตรังสีและครึ่งชีวิต",
    "เคมีเพิ่มเติม 1 ม.4/8": "การนำธาตุไปใช้ประโยชน์และผลกระทบ",
    "เคมีเพิ่มเติม 1 ม.4/9": "การเกิดไอออนและพันธะไอออนิก",
    "เคมีเพิ่มเติม 1 ม.4/10": "สูตรและการเรียกชื่อสารประกอบไอออนิก",
    "เคมีเพิ่มเติม 1 ม.4/11": "พลังงานกับการเกิดสารประกอบไอออนิกและวัฏจักรบอร์น-ฮาเบอร์",
    "เคมีเพิ่มเติม 1 ม.4/12": "สมบัติของสารประกอบไอออนิก",
    "เคมีเพิ่มเติม 1 ม.4/13": "สมการไอออนิกและสมการไอออนิกสุทธิ",
    "เคมีเพิ่มเติม 1 ม.4/14": "พันธะโคเวเลนต์และโครงสร้างลิวอิส",
    "เคมีเพิ่มเติม 1 ม.4/15": "สูตรและการเรียกชื่อสารโคเวเลนต์",
    "เคมีเพิ่มเติม 1 ม.4/16": "ความยาวพันธะ พลังงานพันธะ และพลังงานของปฏิกิริยา",
    "เคมีเพิ่มเติม 1 ม.4/17": "รูปร่างโมเลกุลและสภาพขั้วของโมเลกุลโคเวเลนต์",
    "เคมีเพิ่มเติม 1 ม.4/18": "แรงยึดเหนี่ยวระหว่างโมเลกุลและสมบัติของสารโคเวเลนต์",
    "เคมีเพิ่มเติม 1 ม.4/19": "สารโคเวเลนต์โครงร่างตาข่าย",
    "เคมีเพิ่มเติม 1 ม.4/20": "พันธะโลหะและสมบัติของโลหะ",
    "เคมีเพิ่มเติม 1 ม.4/21": "สมบัติและการใช้ประโยชน์ของสารประกอบไอออนิก สารโคเวเลนต์ และโลหะ",
    "เคมีเพิ่มเติม 1 ม.5/1": "กฎของบอยล์ กฎของชาร์ล และกฎของเกย์-ลูสแซก",
    "เคมีเพิ่มเติม 1 ม.5/2": "กฎรวมแก๊ส",
    "เคมีเพิ่มเติม 1 ม.5/3": "กฎของอาโวกาโดรและกฎแก๊สอุดมคติ",
    "เคมีเพิ่มเติม 1 ม.5/4": "กฎความดันย่อยของดอลตัน",
    "เคมีเพิ่มเติม 1 ม.5/5": "การแพร่ของแก๊สและกฎการแพร่ผ่านของเกรแฮม",
    "เคมีเพิ่มเติม 1 ม.5/6": "การประยุกต์ใช้สมบัติและกฎของแก๊ส",
    "เคมีเพิ่มเติม 1 ม.6/1": "สารประกอบอินทรีย์ที่มีพันธะเดี่ยว พันธะคู่ และพันธะสามในชีวิตประจำวัน",
    "เคมีเพิ่มเติม 1 ม.6/2": "สูตรโครงสร้างลิวอิส สูตรโครงสร้างแบบย่อ และสูตรโครงสร้างแบบเส้น",
    "เคมีเพิ่มเติม 1 ม.6/3": "หมู่ฟังก์ชันและประเภทของสารประกอบอินทรีย์",
    "เคมีเพิ่มเติม 1 ม.6/4": "การเรียกชื่อสารประกอบอินทรีย์ตามระบบ IUPAC",
    "เคมีเพิ่มเติม 1 ม.6/5": "ไอโซเมอร์โครงสร้างของสารประกอบอินทรีย์",
    "เคมีเพิ่มเติม 1 ม.6/6": "จุดเดือดและการละลายน้ำของสารประกอบอินทรีย์",
    "เคมีเพิ่มเติม 1 ม.6/7": "ประเภทและปฏิกิริยาของสารประกอบไฮโดรคาร์บอน",
    "เคมีเพิ่มเติม 1 ม.6/8": "ปฏิกิริยาเอสเทอริฟิเคชัน การสังเคราะห์เอไมด์ ไฮโดรลิซิส และสะปอนนิฟิเคชัน",
    "เคมีเพิ่มเติม 1 ม.6/10": "การใช้ประโยชน์สารประกอบอินทรีย์ในชีวิตประจำวันและอุตสาหกรรม",
    "เคมีเพิ่มเติม 1 ม.6/11": "ประเภทของปฏิกิริยาการเกิดพอลิเมอร์",
    "เคมีเพิ่มเติม 1 ม.6/12": "โครงสร้าง สมบัติ และการใช้ประโยชน์ของพอลิเมอร์",
    "เคมีเพิ่มเติม 1 ม.6/14": "การปรับเปลี่ยนโครงสร้างและการสังเคราะห์พอลิเมอร์",
    "เคมีเพิ่มเติม 1 ม.6/15": "ผลกระทบจากการใช้และการกำจัดผลิตภัณฑ์พอลิเมอร์",
    "เคมีเพิ่มเติม 2 ม.4/1": "สมการเคมีและการดุลสมการเคมี",
    "เคมีเพิ่มเติม 2 ม.4/2": "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับมวล",
    "เคมีเพิ่มเติม 2 ม.4/3": "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับความเข้มข้นของสารละลาย",
    "เคมีเพิ่มเติม 2 ม.4/4": "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับปริมาตรแก๊ส",
    "เคมีเพิ่มเติม 2 ม.4/5": "การคำนวณปริมาณสารในปฏิกิริยาเคมีหลายขั้นตอน",
    "เคมีเพิ่มเติม 2 ม.4/6": "สารกำหนดปริมาณ",
    "เคมีเพิ่มเติม 2 ม.4/7": "ผลได้ร้อยละ",
    "เคมีเพิ่มเติม 2 ม.5/2": "การคำนวณอัตราการเกิดปฏิกิริยาเคมี",
    "เคมีเพิ่มเติม 2 ม.5/3": "ทฤษฎีการชนและพลังงานก่อกัมมันต์",
    "เคมีเพิ่มเติม 2 ม.5/5": "ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี",
    "เคมีเพิ่มเติม 2 ม.5/6": "ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาในชีวิตประจำวันและอุตสาหกรรม",
    "เคมีเพิ่มเติม 2 ม.5/1": "กราฟการเปลี่ยนแปลงปริมาณสารในปฏิกิริยา",
    "เคมีเพิ่มเติม 2 ม.5/7": "ปฏิกิริยาผันกลับได้และภาวะสมดุล",
    "เคมีเพิ่มเติม 2 ม.5/8": "การเปลี่ยนแปลงความเข้มข้นและอัตราการเกิดปฏิกิริยาจนถึงภาวะสมดุล",
    "เคมีเพิ่มเติม 2 ม.5/9": "ค่าคงที่สมดุล",
    "เคมีเพิ่มเติม 2 ม.5/10": "การคำนวณความเข้มข้นของสารที่ภาวะสมดุล",
    "เคมีเพิ่มเติม 2 ม.5/11": "ค่าคงที่สมดุลของปฏิกิริยาหลายขั้นตอน",
    "เคมีเพิ่มเติม 2 ม.5/12": "ปัจจัยที่มีผลต่อภาวะสมดุลและหลักของเลอชาเตอลิเอ",
    "เคมีเพิ่มเติม 2 ม.5/13": "สมดุลเคมีในสิ่งมีชีวิต ธรรมชาติ และอุตสาหกรรม",
    "เคมีเพิ่มเติม 2 ม.5/14": "ทฤษฎีกรด-เบส",
    "เคมีเพิ่มเติม 2 ม.5/15": "คู่กรด-เบสตามทฤษฎีเบรินสเตด-ลาวรี",
    "เคมีเพิ่มเติม 2 ม.5/16": "ความแรงของกรดและเบส",
    "เคมีเพิ่มเติม 2 ม.5/17": "pH ของสารละลายกรดและเบส",
    "เคมีเพิ่มเติม 2 ม.5/18": "ปฏิกิริยาสะเทิน",
    "เคมีเพิ่มเติม 2 ม.5/19": "ไฮโดรลิซิสของเกลือ",
    "เคมีเพิ่มเติม 2 ม.5/20": "หลักการไทเทรตและการเลือกอินดิเคเตอร์",
    "เคมีเพิ่มเติม 2 ม.5/21": "การคำนวณจากการไทเทรตกรด-เบส",
    "เคมีเพิ่มเติม 2 ม.5/22": "สารละลายบัฟเฟอร์",
    "เคมีเพิ่มเติม 2 ม.5/23": "การใช้ประโยชน์ความรู้เกี่ยวกับกรด-เบส",
    "เคมีเพิ่มเติม 2 ม.5/24": "เลขออกซิเดชันและปฏิกิริยารีดอกซ์",
    "เคมีเพิ่มเติม 2 ม.5/25": "ตัวรีดิวซ์ ตัวออกซิไดส์ และครึ่งปฏิกิริยา",
    "เคมีเพิ่มเติม 2 ม.5/26": "ความสามารถในการเป็นตัวรีดิวซ์และตัวออกซิไดส์",
    "เคมีเพิ่มเติม 2 ม.5/27": "การดุลสมการรีดอกซ์",
    "เคมีเพิ่มเติม 2 ม.5/28": "องค์ประกอบของเซลล์เคมีไฟฟ้า",
    "เคมีเพิ่มเติม 2 ม.5/29": "ศักย์ไฟฟ้ามาตรฐานของเซลล์",
    "เคมีเพิ่มเติม 2 ม.5/30": "เซลล์ปฐมภูมิและเซลล์ทุติยภูมิ",
    "เคมีเพิ่มเติม 2 ม.5/31": "การชุบโลหะ การแยกสารด้วยไฟฟ้า และการป้องกันการกัดกร่อน",
    "เคมีเพิ่มเติม 2 ม.5/32": "เทคโนโลยีที่เกี่ยวข้องกับเซลล์เคมีไฟฟ้า",
    "เคมีเพิ่มเติม 3 ม.4/1": "ความปลอดภัยในการทำปฏิบัติการเคมี",
    "เคมีเพิ่มเติม 3 ม.4/2": "การเลือกและใช้อุปกรณ์ในการทำปฏิบัติการเคมี",
    "เคมีเพิ่มเติม 3 ม.4/4": "หน่วยวัดและการเปลี่ยนหน่วยด้วยแฟกเตอร์เปลี่ยนหน่วย",
    "เคมีเพิ่มเติม 3 ม.4/5": "มวลอะตอม มวลโมเลกุล และมวลสูตร",
    "เคมีเพิ่มเติม 3 ม.4/6": "ความสัมพันธ์ของโมล จำนวนอนุภาค มวล และปริมาตรแก๊ส",
    "เคมีเพิ่มเติม 3 ม.4/7": "อัตราส่วนโดยมวลของธาตุตามกฎสัดส่วนคงที่",
    "เคมีเพิ่มเติม 3 ม.4/8": "สูตรอย่างง่ายและสูตรโมเลกุล",
    "เคมีเพิ่มเติม 3 ม.4/9": "ความเข้มข้นของสารละลายในหน่วยต่าง ๆ",
    "เคมีเพิ่มเติม 3 ม.4/10": "การเตรียมสารละลาย",
    "เคมีเพิ่มเติม 3 ม.4/11": "จุดเดือดและจุดเยือกแข็งของสารละลาย",
    "ชีววิทยาเพิ่มเติม 1 ม.4/1": "สมบัติของสิ่งมีชีวิตและการจัดระบบของสิ่งมีชีวิต",
    "ชีววิทยาเพิ่มเติม 1 ม.4/2": "การระบุปัญหา สมมติฐาน และการออกแบบการทดลอง",
    "ชีววิทยาเพิ่มเติม 1 ม.4/3": "น้ำและธาตุที่สำคัญต่อสิ่งมีชีวิต",
    "ชีววิทยาเพิ่มเติม 1 ม.4/4": "คาร์โบไฮเดรต",
    "ชีววิทยาเพิ่มเติม 1 ม.4/5": "โปรตีน",
    "ชีววิทยาเพิ่มเติม 1 ม.4/6": "ลิพิด",
    "ชีววิทยาเพิ่มเติม 1 ม.4/7": "กรดนิวคลีอิก",
    "ชีววิทยาเพิ่มเติม 1 ม.4/8": "ปฏิกิริยาเคมีในสิ่งมีชีวิต",
    "ชีววิทยาเพิ่มเติม 1 ม.4/9": "เอนไซม์และปัจจัยที่มีผลต่อการทำงานของเอนไซม์",
    "ชีววิทยาเพิ่มเติม 1 ม.4/10": "กล้องจุลทรรศน์ใช้แสง",
    "ชีววิทยาเพิ่มเติม 1 ม.4/11": "ส่วนที่ห่อหุ้มเซลล์",
    "ชีววิทยาเพิ่มเติม 1 ม.4/12": "ออร์แกเนลล์",
    "ชีววิทยาเพิ่มเติม 1 ม.4/13": "โครงสร้างและหน้าที่ของนิวเคลียส",
    "ชีววิทยาเพิ่มเติม 1 ม.4/14": "การลำเลียงสารผ่านเยื่อหุ้มเซลล์",
    "ชีววิทยาเพิ่มเติม 1 ม.4/15": "เอกโซไซโทซิสและเอนโดไซโทซิส",
    "ชีววิทยาเพิ่มเติม 1 ม.4/16": "การแบ่งนิวเคลียสแบบไมโทซิสและไมโอซิส",
    "ชีววิทยาเพิ่มเติม 1 ม.4/17": "การหายใจระดับเซลล์",
    "ชีววิทยาเพิ่มเติม 2 ม.4/1": "การทดลองของเมนเดล",
    "ชีววิทยาเพิ่มเติม 2 ม.4/2": "กฎแห่งการแยกและกฎแห่งการรวมกลุ่มอย่างอิสระ",
    "ชีววิทยาเพิ่มเติม 2 ม.4/3": "ส่วนขยายของพันธุศาสตร์เมนเดล",
    "ชีววิทยาเพิ่มเติม 2 ม.4/4": "การแปรผันทางพันธุกรรม",
    "ชีววิทยาเพิ่มเติม 2 ม.4/5": "ยีนบนออโตโซมและโครโมโซมเพศ",
    "ชีววิทยาเพิ่มเติม 2 ม.4/6": "สมบัติ โครงสร้าง และการจำลอง DNA",
    "ชีววิทยาเพิ่มเติม 2 ม.4/7": "การสังเคราะห์โปรตีน",
    "ชีววิทยาเพิ่มเติม 2 ม.4/8": "ความสัมพันธ์ระหว่างยีน แอลลีล โปรตีน และลักษณะ",
    "ชีววิทยาเพิ่มเติม 2 ม.4/9": "มิวเทชัน",
    "ชีววิทยาเพิ่มเติม 2 ม.4/10": "ดีเอ็นเอรีคอมบิแนนท์และสิ่งมีชีวิตดัดแปรพันธุกรรม",
    "ชีววิทยาเพิ่มเติม 2 ม.4/11": "การประยุกต์ใช้เทคโนโลยีทางดีเอ็นเอ",
    "ชีววิทยาเพิ่มเติม 2 ม.4/12": "หลักฐานการเกิดวิวัฒนาการ",
    "ชีววิทยาเพิ่มเติม 2 ม.4/13": "แนวคิดวิวัฒนาการของลามาร์กและดาร์วิน",
    "ชีววิทยาเพิ่มเติม 2 ม.4/14": "ภาวะสมดุลของฮาร์ดี-ไวน์เบิร์ก",
    "ชีววิทยาเพิ่มเติม 2 ม.4/15": "การเกิดสปีชีส์ใหม่",
    "ชีววิทยาเพิ่มเติม 2 ม.6/1": "ความหลากหลายทางชีวภาพ",
    "ชีววิทยาเพิ่มเติม 2 ม.6/2": "การเกิดเซลล์เริ่มแรกและวิวัฒนาการของสิ่งมีชีวิตเซลล์เดียว",
    "ชีววิทยาเพิ่มเติม 2 ม.6/3": "ลักษณะของสิ่งมีชีวิตกลุ่มต่าง ๆ",
    "ชีววิทยาเพิ่มเติม 2 ม.6/4": "ลำดับขั้นการจำแนกและชื่อวิทยาศาสตร์",
    "ชีววิทยาเพิ่มเติม 2 ม.6/5": "ไดโคโทมัสคีย์",
    "ชีววิทยาเพิ่มเติม 3 ม.5/1": "เนื้อเยื่อพืช",
    "ชีววิทยาเพิ่มเติม 3 ม.5/2": "โครงสร้างภายในของราก",
    "ชีววิทยาเพิ่มเติม 3 ม.5/3": "โครงสร้างภายในของลำต้น",
    "ชีววิทยาเพิ่มเติม 3 ม.5/4": "โครงสร้างภายในของใบ",
    "ชีววิทยาเพิ่มเติม 3 ม.5/5": "การแลกเปลี่ยนแก๊สและการคายน้ำ",
    "ชีววิทยาเพิ่มเติม 3 ม.5/6": "การลำเลียงน้ำและธาตุอาหาร",
    "ชีววิทยาเพิ่มเติม 3 ม.5/7": "ธาตุอาหารของพืช",
    "ชีววิทยาเพิ่มเติม 3 ม.5/8": "การลำเลียงอาหารในพืช",
    "ชีววิทยาเพิ่มเติม 3 ม.5/9": "การศึกษาการสังเคราะห์ด้วยแสงในอดีต",
    "ชีววิทยาเพิ่มเติม 3 ม.5/10": "กระบวนการสังเคราะห์ด้วยแสงของพืช C3",
    "ชีววิทยาเพิ่มเติม 3 ม.5/11": "การตรึงคาร์บอนไดออกไซด์ในพืช C3 C4 และ CAM",
    "ชีววิทยาเพิ่มเติม 3 ม.5/12": "ปัจจัยที่มีผลต่อการสังเคราะห์ด้วยแสง",
    "ชีววิทยาเพิ่มเติม 3 ม.5/13": "วัฏจักรชีวิตแบบสลับของพืชดอก",
    "ชีววิทยาเพิ่มเติม 3 ม.5/14": "การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของพืชดอก",
    "ชีววิทยาเพิ่มเติม 3 ม.5/15": "การเกิดเมล็ดและผล",
    "ชีววิทยาเพิ่มเติม 3 ม.5/16": "การงอกของเมล็ดและการพักตัว",
    "ชีววิทยาเพิ่มเติม 3 ม.5/17": "ฮอร์โมนพืช",
    "ชีววิทยาเพิ่มเติม 3 ม.5/18": "สิ่งเร้าภายนอกที่มีผลต่อการเจริญเติบโตของพืช",
    "ชีววิทยาเพิ่มเติม 4 ม.5/1": "การย่อยอาหารของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.5/2": "การกินอาหารของไฮดราและพลานาเรีย",
    "ชีววิทยาเพิ่มเติม 4 ม.5/3": "การย่อยอาหารและการดูดซึมของมนุษย์",
    "ชีววิทยาเพิ่มเติม 4 ม.5/4": "โครงสร้างแลกเปลี่ยนแก๊สของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.5/5": "โครงสร้างของปอดสัตว์เลี้ยงลูกด้วยน้ำนม",
    "ชีววิทยาเพิ่มเติม 4 ม.5/6": "การแลกเปลี่ยนแก๊สของมนุษย์",
    "ชีววิทยาเพิ่มเติม 4 ม.5/7": "การทำงานของปอดและปริมาตรอากาศ",
    "ชีววิทยาเพิ่มเติม 4 ม.5/8": "ระบบหมุนเวียนเลือดแบบเปิดและแบบปิด",
    "ชีววิทยาเพิ่มเติม 4 ม.5/9": "การไหลของเลือดในหางปลา",
    "ชีววิทยาเพิ่มเติม 4 ม.5/10": "โครงสร้างและการทำงานของหัวใจและหลอดเลือด",
    "ชีววิทยาเพิ่มเติม 4 ม.5/11": "ทิศทางการไหลของเลือดผ่านหัวใจ",
    "ชีววิทยาเพิ่มเติม 4 ม.5/12": "องค์ประกอบของเลือด",
    "ชีววิทยาเพิ่มเติม 4 ม.5/13": "หมู่เลือดและการให้รับเลือด",
    "ชีววิทยาเพิ่มเติม 4 ม.5/14": "ระบบน้ำเหลือง",
    "ชีววิทยาเพิ่มเติม 4 ม.5/15": "กลไกการต่อต้านสิ่งแปลกปลอม",
    "ชีววิทยาเพิ่มเติม 4 ม.5/16": "ภูมิคุ้มกันก่อเองและภูมิคุ้มกันรับมา",
    "ชีววิทยาเพิ่มเติม 4 ม.5/17": "ความผิดปกติของระบบภูมิคุ้มกัน",
    "ชีววิทยาเพิ่มเติม 4 ม.5/18": "การกำจัดของเสียของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.5/19": "โครงสร้างและหน้าที่ของไต",
    "ชีววิทยาเพิ่มเติม 4 ม.5/20": "การทำงานของหน่วยไต",
    "ชีววิทยาเพิ่มเติม 4 ม.5/21": "ความผิดปกติของไต",
    "ชีววิทยาเพิ่มเติม 4 ม.6/1": "ระบบประสาทของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/2": "โครงสร้างและหน้าที่ของเซลล์ประสาท",
    "ชีววิทยาเพิ่มเติม 4 ม.6/3": "ศักย์เยื่อเซลล์และการถ่ายทอดกระแสประสาท",
    "ชีววิทยาเพิ่มเติม 4 ม.6/4": "ระบบประสาทส่วนกลางและระบบประสาทรอบนอก",
    "ชีววิทยาเพิ่มเติม 4 ม.6/5": "สมองและไขสันหลัง",
    "ชีววิทยาเพิ่มเติม 4 ม.6/6": "ระบบประสาทโซมาติกและระบบประสาทอัตโนวัติ",
    "ชีววิทยาเพิ่มเติม 4 ม.6/7": "อวัยวะรับความรู้สึก",
    "ชีววิทยาเพิ่มเติม 4 ม.6/8": "จุดบอด โฟเวีย และความไวของผิวหนัง",
    "ชีววิทยาเพิ่มเติม 4 ม.6/9": "การเคลื่อนที่ของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/10": "กระดูกและกล้ามเนื้อของมนุษย์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/11": "ข้อต่อและการทำงานของกล้ามเนื้อโครงร่าง",
    "ชีววิทยาเพิ่มเติม 4 ม.6/12": "การสืบพันธุ์ของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/13": "ระบบสืบพันธุ์ของมนุษย์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/14": "การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของมนุษย์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/15": "การเจริญเติบโตของสัตว์",
    "ชีววิทยาเพิ่มเติม 4 ม.6/16": "ฮอร์โมนจากต่อมไร้ท่อ",
    "ชีววิทยาเพิ่มเติม 4 ม.6/17": "พฤติกรรมที่เป็นมาแต่กำเนิดและที่เกิดจากการเรียนรู้",
    "ชีววิทยาเพิ่มเติม 4 ม.6/18": "พฤติกรรมกับวิวัฒนาการของระบบประสาท",
    "ชีววิทยาเพิ่มเติม 4 ม.6/19": "การสื่อสารระหว่างสัตว์",
    "ชีววิทยาเพิ่มเติม 5 ม.6/1": "การถ่ายทอดพลังงานในระบบนิเวศ",
    "ชีววิทยาเพิ่มเติม 5 ม.6/2": "ไบโอแมกนิฟิเคชัน",
    "ชีววิทยาเพิ่มเติม 5 ม.6/3": "วัฏจักรไนโตรเจน กำมะถัน และฟอสฟอรัส",
    "ชีววิทยาเพิ่มเติม 5 ม.6/4": "ไบโอม",
    "ชีววิทยาเพิ่มเติม 5 ม.6/5": "การเปลี่ยนแปลงแทนที่",
    "ชีววิทยาเพิ่มเติม 5 ม.6/6": "ลักษณะเฉพาะของประชากร",
    "ชีววิทยาเพิ่มเติม 5 ม.6/7": "การเพิ่มของประชากร",
    "ชีววิทยาเพิ่มเติม 5 ม.6/8": "ปัจจัยที่ควบคุมการเติบโตของประชากร",
    "ชีววิทยาเพิ่มเติม 5 ม.6/9": "ปัญหาทรัพยากรน้ำและการจัดการ",
    "ชีววิทยาเพิ่มเติม 5 ม.6/10": "ปัญหามลพิษทางอากาศ",
    "ชีววิทยาเพิ่มเติม 5 ม.6/11": "ปัญหาทรัพยากรดิน",
    "ชีววิทยาเพิ่มเติม 5 ม.6/12": "การทำลายป่าไม้และการอนุรักษ์",
    "ชีววิทยาเพิ่มเติม 5 ม.6/13": "การลดลงของสัตว์ป่าและการอนุรักษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/1": "โครงสร้างโลก",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/2": "หลักฐานการเคลื่อนที่ของแผ่นธรณี",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/3": "แนวรอยต่อของแผ่นธรณี",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/4": "ลำดับเหตุการณ์ทางธรณีวิทยา",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/5": "ภูเขาไฟระเบิด",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/6": "แผ่นดินไหว",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/7": "สึนามิ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/8": "แร่และการใช้ประโยชน์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/9": "หินและการใช้ประโยชน์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/10": "การเกิดและการสำรวจปิโตรเลียมและถ่านหิน",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/11": "ผลิตภัณฑ์จากปิโตรเลียมและถ่านหิน",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/12": "แผนที่ภูมิประเทศและแผนที่ธรณีวิทยา",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/1": "การรับและคายพลังงานจากดวงอาทิตย์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/2": "สมดุลพลังงานของโลก",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/3": "แรงที่มีผลต่อการหมุนเวียนของอากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/4": "การหมุนเวียนของอากาศตามเขตละติจูด",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/5": "การแบ่งชั้นน้ำในมหาสมุทร",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/6": "การหมุนเวียนของน้ำในมหาสมุทร",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/7": "ผลของการหมุนเวียนของน้ำในมหาสมุทร",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/8": "เสถียรภาพอากาศและการเกิดเมฆ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/9": "แนวปะทะอากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/10": "ปัจจัยที่มีผลต่อการเปลี่ยนแปลงภูมิอากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/11": "ผลและการชะลอการเปลี่ยนแปลงภูมิอากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/12": "สัญลักษณ์ลมฟ้าอากาศบนแผนที่อากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/13": "การคาดการณ์ลมฟ้าอากาศจากแผนที่อากาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/1": "วิวัฒนาการของเอกภพหลังบิกแบง",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/2": "หลักฐานสนับสนุนทฤษฎีบิกแบง",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/3": "กาแล็กซีทางช้างเผือก",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/4": "กระบวนการเกิดดาวฤกษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/5": "การสร้างพลังงานของดาวฤกษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/6": "ความส่องสว่างและโชติมาตรของดาวฤกษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/7": "สี อุณหภูมิผิว และสเปกตรัมของดาวฤกษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/8": "ระยะทางของดาวฤกษ์ด้วยแพรัลแลกซ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/9": "วิวัฒนาการของดาวฤกษ์และแผนภาพเฮิร์ตซ์สปรุง-รัสเซลล์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/10": "การเกิดระบบสุริยะและดาวเคราะห์ที่เอื้อต่อชีวิต",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/11": "กฎของเคพเลอร์และกฎความโน้มถ่วงของนิวตัน",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/12": "โครงสร้างดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/13": "ทรงกลมฟ้าและระบบพิกัดของดาว",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/14": "เส้นทางการขึ้นตกของดวงอาทิตย์และดาวฤกษ์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/15": "เวลาสุริยคติปรากฏ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/16": "เวลาสุริยคติปานกลางและเขตเวลา",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/17": "มุมห่างและตำแหน่งปรากฏของดาวเคราะห์",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/18": "การสำรวจอวกาศและเทคโนโลยีอวกาศ",
    "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/19": "การวางแผนสังเกตดาวบนท้องฟ้า",
}

LEVELS = {
    "ฟิสิกส์เพิ่มเติม 1 ม.4/7": "ม.4",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/8": "ม.4",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/3": "ม.6",
    "ฟิสิกส์เพิ่มเติม 4 ม.6/4": "ม.6",
    "ฟิสิกส์เพิ่มเติม 1 ม.4/6": "ม.4",
    **{f"ฟิสิกส์เพิ่มเติม 1 ม.4/{n}": "ม.4" for n in (1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16, 17)},
    **{f"ฟิสิกส์เพิ่มเติม 2 ม.5/{n}": "ม.5" for n in (1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13)},
    **{f"ฟิสิกส์เพิ่มเติม 3 ม.5/{n}": "ม.5" for n in (1, 2, 3, 5, 6, 7, 10, 11)},
    **{f"ฟิสิกส์เพิ่มเติม 3 ม.6/{n}": "ม.6" for n in range(1, 9)},
    **{f"ฟิสิกส์เพิ่มเติม 4 ม.6/{n}": "ม.6" for n in (1, 2, *range(5, 19))},
    **{f"เคมีเพิ่มเติม 1 ม.4/{n}": "ม.4" for n in (1, 3, *range(5, 22))},
    "เคมีเพิ่มเติม 1 ม.5/1": "ม.5",
    "เคมีเพิ่มเติม 1 ม.5/2": "ม.5",
    **{f"เคมีเพิ่มเติม 1 ม.5/{n}": "ม.5" for n in (3, 4, 5, 6)},
    **{f"เคมีเพิ่มเติม 1 ม.6/{n}": "ม.6" for n in (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15)},
    **{f"เคมีเพิ่มเติม 2 ม.4/{n}": "ม.4" for n in range(1, 8)},
    **{f"เคมีเพิ่มเติม 2 ม.5/{n}": "ม.5" for n in (1, 2, 3, *range(5, 33))},
    **{f"เคมีเพิ่มเติม 3 ม.4/{n}": "ม.4" for n in (1, 2, *range(4, 12))},
    **{f"ชีววิทยาเพิ่มเติม 1 ม.4/{n}": "ม.4" for n in range(1, 18)},
    **{f"ชีววิทยาเพิ่มเติม 2 ม.4/{n}": "ม.4" for n in range(1, 16)},
    **{f"ชีววิทยาเพิ่มเติม 2 ม.6/{n}": "ม.6" for n in range(1, 6)},
    **{f"ชีววิทยาเพิ่มเติม 3 ม.5/{n}": "ม.5" for n in range(1, 19)},
    **{f"ชีววิทยาเพิ่มเติม 4 ม.5/{n}": "ม.5" for n in range(1, 22)},
    **{f"ชีววิทยาเพิ่มเติม 4 ม.6/{n}": "ม.6" for n in range(1, 20)},
    **{f"ชีววิทยาเพิ่มเติม 5 ม.6/{n}": "ม.6" for n in range(1, 14)},
    **{f"โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/{n}": "ม.4" for n in range(1, 13)},
    **{f"โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/{n}": "ม.5" for n in range(1, 14)},
    **{f"โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/{n}": "ม.6" for n in range(1, 20)},
}

NEW_KEYS = tuple(key for keys in INDICATORS.values() for key in keys)


def _stem(question) -> str:
    return " ".join(getattr(block, "text", getattr(block, "tex", ""))
                    for block in question.stem)


def _answer(question) -> str:
    return " ".join(getattr(block, "text", getattr(block, "tex", ""))
                    for block in question.choices[question.answer].content)


def _numbers(stem: str) -> list[float]:
    return [float(match) for match in re.findall(r"\d+(?:\.\d+)?", stem)]


def _value(label: str) -> float:
    return float(re.findall(r"\d+(?:\.\d+)?", label)[0])


# ── filing ────────────────────────────────────────────────────────────────────

def test_every_new_key_is_registered_and_placed():
    for key in NEW_KEYS:
        assert key in REGISTRY, key
        assert key in SCIENCE_PLACEMENTS, key


def test_wave_f_is_its_own_cohort():
    assert set(NEW_KEYS) == SCIENCE_WAVE_F_KEYS
    for earlier in (SCIENCE_WAVE_KEYS, SCIENCE_WAVE_B_KEYS, SCIENCE_BIOLOGY_CLOSURE_KEYS,
                    SCIENCE_WAVE_C_KEYS, SCIENCE_WAVE_D_KEYS, SCIENCE_WAVE_E_KEYS):
        assert not SCIENCE_WAVE_F_KEYS & earlier


def test_approval_is_recorded_for_whole_indicators_inside_wave_f():
    assert SCIENCE_WAVE_F_APPROVED_KEYS <= SCIENCE_WAVE_F_KEYS
    for code, keys in INDICATORS.items():
        assert set(keys) & SCIENCE_WAVE_F_APPROVED_KEYS in (set(), set(keys)), code


def test_every_unapproved_set_is_on_the_review_worklist():
    pending = set().union(*REVIEW_PENDING.values()) if REVIEW_PENDING else set()
    assert SCIENCE_WAVE_F_KEYS - SCIENCE_WAVE_F_APPROVED_KEYS <= pending


def test_each_indicator_holds_three_stages_in_one_unit():
    for code, keys in INDICATORS.items():
        specs = [SCIENCE_PLACEMENTS[key] for key in keys]
        assert {spec.indicator_codes for spec in specs} == {(code,)}, code
        assert {spec.unit for spec in specs} == {TOPICS[code]}, code
        assert {spec.level for spec in specs} == {LEVELS[code]}, code
        assert {spec.course_type for spec in specs} == {ADDITIONAL}, code
        # The strand is everything before the course number; the earth strand has spaces in it.
        assert {spec.strand_code for spec in specs} == {code.rsplit(" ", 2)[0]}, code


def test_an_additional_outcome_is_filed_whole():
    """No stage may claim ``exact``: the outcome is not split into indicators."""
    for key in NEW_KEYS:
        assert SCIENCE_PLACEMENTS[key].mapping_status == "additional_outcome", key


@pytest.mark.parametrize("key", NEW_KEYS)
def test_every_set_carries_its_unit_topic(key):
    code = next(one for one, keys in INDICATORS.items() if key in keys)
    assert generate(key, Random(0)).topic == TOPICS[code]


# ── ฟิสิกส์เพิ่มเติม 1 ม.4/7 — μ = f/N ────────────────────────────────────────

def test_the_friction_pool_never_offers_an_unwritable_answer():
    assert FRICTION_POOL
    for mass, mu, force in FRICTION_POOL:
        assert force == mu * mass * G
        assert force == int(force)


def test_friction_coefficient_fluency_answers_force_over_weight():
    for seed in range(SEEDS):
        question = generate("phys.friction_coefficient_fluency", Random(seed))
        mass, force, gravity = _numbers(_stem(question))
        assert gravity == G
        assert _value(_answer(question)) == pytest.approx(force / (mass * G))


def test_friction_coefficient_application_runs_the_same_law_backwards():
    saw_force = saw_weight = False
    for seed in range(SEEDS):
        question = generate("phys.friction_coefficient_application", Random(seed))
        stem = _stem(question)
        answer = _value(_answer(question))
        if "จงหาน้ำหนักของวัตถุ" in stem:
            force, mu = _numbers(stem)
            assert answer == pytest.approx(force / mu)
            saw_weight = True
        else:
            mass, mu, gravity = _numbers(stem)
            assert gravity == G
            assert answer == pytest.approx(mu * mass * G)
            saw_force = True
    assert saw_force and saw_weight


def test_friction_never_multiplies_mu_by_a_horizontal_force():
    """The mistake the source sheet's ข้อ 20 makes is not reproduced.

    Every stem that states μ states either a mass (so ``N = mg``) or a friction
    force — never an applied horizontal pull that μ could be multiplied by.
    """
    for key in ("phys.friction_coefficient_fluency", "phys.friction_coefficient_application"):
        for seed in range(SEEDS):
            stem = _stem(generate(key, Random(seed)))
            assert "ผลัก" not in stem


# ── ฟิสิกส์เพิ่มเติม 1 ม.4/8 — ผลรวมของโมเมนต์ ────────────────────────────────

def test_mechanical_equilibrium_fluency_balances_the_sum_of_moments():
    for seed in range(SEEDS):
        question = generate("phys.mechanical_equilibrium_fluency", Random(seed))
        w1, d1, w2, d2, d3 = _numbers(_stem(question))
        answer = _value(_answer(question))
        assert answer * d3 == pytest.approx(w1 * d1 + w2 * d2)


def test_mechanical_equilibrium_application_trades_force_against_lever_arm():
    for seed in range(SEEDS):
        question = generate("phys.mechanical_equilibrium_application", Random(seed))
        load, a, length = _numbers(_stem(question))
        answer = _value(_answer(question))
        assert answer * length == pytest.approx(load * a)
        # The effort arm is always the longer one, so the effort beats the load.
        assert answer < load


# ── ฟิสิกส์เพิ่มเติม 4 ม.6/3 — P = ρgh ────────────────────────────────────────

def test_gauge_pressure_fluency_answers_rho_g_h():
    for seed in range(SEEDS):
        question = generate("phys.gauge_pressure_fluency", Random(seed))
        rho, depth, gravity = _numbers(_stem(question))
        assert gravity == G
        assert _value(_answer(question)) == pytest.approx(rho * G * depth)


def test_gauge_pressure_application_adds_the_atmosphere_or_multiplies_the_base():
    saw_absolute = saw_force = False
    for seed in range(SEEDS):
        question = generate("phys.gauge_pressure_application", Random(seed))
        stem = _stem(question)
        answer = _value(_answer(question))
        if "ความดันสัมบูรณ์" in stem:
            rho, depth, atm, gravity = _numbers(stem)
            assert (atm, gravity) == (ATM, G)
            assert answer == pytest.approx(ATM + rho * G * depth)
            saw_absolute = True
        else:
            side_a, side_b, rho, depth, gravity = _numbers(stem)
            assert gravity == G
            assert answer == pytest.approx(rho * G * depth * side_a * side_b)
            saw_force = True
    assert saw_absolute and saw_force


def test_force_from_pressure_is_only_ever_asked_for_a_flat_bottom():
    """``F = PA`` with one pressure holds on the base, not on a side wall.

    The source sheet's ข้อ 5 applies the bottom pressure to a vertical wall and
    doubles its own answer; no stem here asks for a side.
    """
    for seed in range(SEEDS):
        stem = _stem(generate("phys.gauge_pressure_application", Random(seed)))
        assert "ด้านข้าง" not in stem
        if "จงหาแรง" in stem:
            assert "ก้นถัง" in stem


# ── ฟิสิกส์เพิ่มเติม 4 ม.6/4 — แรงพยุง ────────────────────────────────────────

def test_fluid_buoyancy_fluency_is_the_difference_of_two_weighings():
    for seed in range(SEEDS):
        question = generate("phys.fluid_buoyancy_fluency", Random(seed))
        in_air, in_water = _numbers(_stem(question))
        answer = _value(_answer(question))
        assert answer == pytest.approx(in_air - in_water)
        assert 0 < answer < in_air


def test_fluid_buoyancy_application_runs_rho_v_g_both_ways():
    saw_force = saw_volume = False
    for seed in range(SEEDS):
        question = generate("phys.fluid_buoyancy_application", Random(seed))
        stem = _stem(question)
        answer = _value(_answer(question))
        if "จงหาปริมาตรของวัตถุ" in stem:
            rho, force, gravity = _numbers(stem)
            assert gravity == G
            assert answer == pytest.approx(force / (rho * G))
            saw_volume = True
        else:
            volume, rho, gravity = _numbers(stem)
            assert gravity == G
            assert answer == pytest.approx(rho * volume * G)
            saw_force = True
    assert saw_force and saw_volume


# ── ฟิสิกส์เพิ่มเติม 1 ม.4/6 — W = mg ─────────────────────────────────────────

def test_weight_gravity_fluency_multiplies_or_divides_by_g():
    saw_weight = saw_mass = False
    for seed in range(SEEDS):
        question = generate("phys.weight_gravity_fluency", Random(seed))
        stem = _stem(question)
        answer = _value(_answer(question))
        if "จงหาน้ำหนัก" in stem:
            mass, gravity = _numbers(stem)
            assert gravity == EARTH_G
            assert answer == pytest.approx(mass * EARTH_G)
            saw_weight = True
        else:
            weight, gravity = _numbers(stem)
            assert gravity == EARTH_G
            assert answer == pytest.approx(weight / EARTH_G)
            saw_mass = True
    assert saw_weight and saw_mass


def test_weight_gravity_application_uses_the_stated_field_not_earths():
    saw_value = saw_compare = False
    for seed in range(SEEDS):
        question = generate("phys.weight_gravity_application", Random(seed))
        stem = _stem(question)
        if "จะมีน้ำหนักเท่าใด" in stem:
            mass, g_there = _numbers(stem)
            assert g_there in {place.g for place in PLACES}
            assert _value(_answer(question)) == pytest.approx(mass * g_there)
            saw_value = True
        else:
            mass, g_here, g_there = _numbers(stem)
            assert g_here == EARTH_G
            # The right answer keeps the mass and changes only the weight.
            answer = _answer(question)
            assert f"{mass:g} กิโลกรัมเท่าเดิม" in answer
            saw_compare = True
    assert saw_value and saw_compare


def test_mass_is_never_reported_in_newtons_or_weight_in_kilograms():
    for key in ("phys.weight_gravity_fluency", "phys.weight_gravity_application"):
        for seed in range(SEEDS):
            question = generate(key, Random(seed))
            stem, answer = _stem(question), _answer(question)
            if "จงหามวล" in stem:
                assert "นิวตัน" not in answer
            elif "จงหาน้ำหนัก" in stem:
                assert "กิโลกรัม" not in answer


# ── Slices 3-4: ฟิสิกส์เพิ่มเติม 1 ม.4/3-5 and ม.4/10-13 ───────────────────────
#
# Each test pulls the numbers out of the stem by the words around them and
# redoes the physics with exact fractions.

def _q(pattern: str, stem: str) -> list[Fraction]:
    match = re.search(pattern, stem)
    assert match, (pattern, stem)
    return [Fraction(g.replace(",", "")) for g in match.groups()]


def _ans(question) -> Fraction:
    return Fraction(_answer(question).split()[0].replace(",", ""))


N = r"(-?[\d,]+(?:\.\d+)?)"


def test_uniform_accel_answers():
    for seed in range(SEEDS):
        q = generate("phys.uniform_accel_foundation", Random(seed))
        s = _stem(q)
        if "ความเร็วต้น" in s:
            u, a, t = _q(rf"ความเร็วต้น {N} m/s และเร่งด้วยความเร่ง {N} m/s² เป็นเวลา {N} s", s)
            assert _ans(q) == u + a * t, s
        elif "ความเร็วเฉลี่ย" in s:
            u, v = _q(rf"จาก {N} m/s เป็น {N} m/s", s)
            assert _ans(q) == (u + v) / 2, s
        q = generate("phys.uniform_accel_fluency", Random(seed))
        s = _stem(q)
        if "ในเวลา" in s:
            u, a, t = _q(rf"ความเร็วต้น {N} m/s และเร่งด้วยความเร่ง {N} m/s² คงตัว ในเวลา {N} s", s)
            assert _ans(q) == u * t + a * t * t / 2, s
        elif "จนได้การกระจัด" in s:
            u, a, d = _q(rf"ความเร็วต้น {N} m/s เร่งด้วยความเร่ง {N} m/s² คงตัว จนได้การกระจัด {N} m", s)
            assert _ans(q) ** 2 == u * u + 2 * a * d, s
        else:
            t1, u, v, v2, t2 = _q(rf"0 ถึง {N} s ความเร็วเพิ่มจาก {N} m/s เป็น {N} m/s อย่างสม่ำเสมอ แล้วคงที่ที่ {N} m/s อีก {N} s", s)
            assert _ans(q) == (u + v) / 2 * t1 + v2 * t2, s
        q = generate("phys.uniform_accel_application", Random(seed))
        s = _stem(q)
        if "ตกอิสระ" in s:
            (t,) = _q(rf"ใช้เวลา {N} s", s)
            assert _ans(q) == 5 * t * t, s
        elif "สูงสุด" in s:
            (u,) = _q(rf"ด้วยความเร็ว {N} m/s", s)
            assert _ans(q) == u * u / 20, s
        elif "กลับมาถึงมือ" in s:
            (u,) = _q(rf"ด้วยความเร็ว {N} m/s", s)
            assert _ans(q) == 2 * u / 10, s
        else:
            u, react, a = _q(rf"ความเร็ว {N} m/s .*ตัดสินใจ {N} s .*ความหน่วง {N} m/s²", s)
            assert _ans(q) == u * react + u * u / (2 * a), s


def test_force_angle_answers():
    cos = {60: Fraction(1, 2), 90: 0, 120: Fraction(-1, 2)}
    for seed in range(SEEDS):
        q = generate("phys.force_angle_fluency", Random(seed))
        s = _stem(q)
        f1, f2, angle = _q(rf"แรง {N} N และ {N} N .*ทำมุม {N}°", s)
        assert _ans(q) ** 2 == f1 * f1 + f2 * f2 + 2 * f1 * f2 * cos[int(angle)], s
        q = generate("phys.force_angle_foundation", Random(seed))
        s = _stem(q)
        f1, f2 = _q(rf"แรง {N} N และ {N} N", s)
        if "ทำมุม 0°" in s:
            assert _ans(q) == f1 + f2
        elif "ทำมุม 180°" in s:
            assert _ans(q) == abs(f2 - f1)
        q = generate("phys.force_angle_application", Random(seed))
        s = _stem(q)
        if "องค์ประกอบ" in s:
            angle, f = _q(rf"ทำมุม {N}° กับแนวระดับด้วยแรง {N} N", s)
            horizontal = "แนวระดับมีขนาด" in s
            factor = {(37, True): Fraction(4, 5), (37, False): Fraction(3, 5),
                      (53, True): Fraction(3, 5), (53, False): Fraction(4, 5)}[(int(angle), horizontal)]
            assert _ans(q) == f * factor, s
        else:
            f1, f2, angle = _q(rf"แรง {N} N และ {N} N ทำมุม {N}°", s)
            assert _ans(q) ** 2 == f1 * f1 + f2 * f2 + 2 * f1 * f2 * cos[int(angle)], s


def test_newton_applied_answers():
    for seed in range(SEEDS):
        q = generate("phys.newton_applied_foundation", Random(seed))
        s = _stem(q)
        if "ความเร่งของกล่อง" in s:
            push, m, friction = _q(rf"ออกแรง {N} N ผลักกล่องมวล {N} kg บนพื้นราบ มีแรงเสียดทาน {N} N", s)
            assert _ans(q) == (push - friction) / m, s
        q = generate("phys.newton_applied_fluency", Random(seed))
        s = _stem(q)
        f, m1, m2 = _q(rf"ออกแรง {N} N .* ก มีมวล {N} kg และ ข มีมวล {N} kg", s)
        a = f / (m1 + m2)
        assert _ans(q) == (a if "ความเร่งของระบบ" in s else m2 * a), s
        q = generate("phys.newton_applied_application", Random(seed))
        s = _stem(q)
        if "ลิฟต์" in s:
            m, a = _q(rf"คนมวล {N} kg .*ความเร่ง {N} m/s²", s)
            assert _ans(q) == m * (10 + a if "เร่งขึ้น" in s else 10 - a), s
        elif "รอกลื่น" in s:
            m1, m2 = _q(rf"แขวนมวล {N} kg และ {N} kg", s)
            assert _ans(q) == (m1 - m2) * 10 / (m1 + m2), s
        else:
            assert _ans(q) == 6, s


def test_work_and_power_answers():
    for seed in range(SEEDS):
        q = generate("phys.work_graph_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("ออกแรง"):
            f, d = _q(rf"ออกแรง {N} N ลากกล่องไปตามแนวแรงได้ระยะ {N} m", s)
            assert _ans(q) == f * d
        elif s.startswith("แรงเสียดทาน"):
            f, d = _q(rf"แรงเสียดทาน {N} N ต้านกล่องที่ไถลไปได้ระยะ {N} m", s)
            assert _ans(q) == -f * d
        elif "ถือกระเป๋า" in s:
            assert _ans(q) == 0
        else:
            f, angle, d = _q(rf"แรง {N} N ในแนวทำมุม {N}° กับพื้น ลากไปตามพื้นได้ระยะ {N} m", s)
            assert _ans(q) == f * d * (Fraction(4, 5) if angle == 37 else Fraction(3, 5)), s
        q = generate("phys.work_graph_fluency", Random(seed))
        s = _stem(q)
        if "ลดลงเป็นเส้นตรง" in s:
            f, x1, x2 = _q(rf"แรงคงที่ {N} N ตั้งแต่ x = 0 ถึง x = {N} m .*ที่ x = {N} m", s)
            assert _ans(q) == f * x1 + f * (x2 - x1) / 2, s
        elif "เพิ่มจาก 0" in s:
            f, x = _q(rf"เป็น {N} N อย่างสม่ำเสมอ ตั้งแต่ x = 0 ถึง x = {N} m", s)
            assert _ans(q) == f * x / 2, s
        else:
            f, x = _q(rf"แรงคงที่ {N} N ตั้งแต่ x = 0 ถึง x = {N} m", s)
            assert _ans(q) == f * x, s
        q = generate("phys.work_graph_application", Random(seed))
        s = _stem(q)
        if s.startswith("เครน"):
            m, h, t = _q(rf"มวล {N} kg ขึ้นสูง {N} m .*ในเวลา {N} s", s)
            assert _ans(q) == m * 10 * h / t, s
        elif "บันได" in s:
            m, h, t = _q(rf"มวล {N} kg วิ่งขึ้นบันไดสูง {N} m ในเวลา {N} s", s)
            assert _ans(q) == m * 10 * h / t, s
        else:
            v, f = _q(rf"ความเร็วคงตัว {N} m/s โดยเครื่องยนต์ออกแรงขับ {N} N", s)
            assert _ans(q) == f * v, s


def test_energy_answers():
    for seed in range(SEEDS):
        q = generate("phys.work_energy_foundation", Random(seed))
        s = _stem(q)
        if "พลังงานจลน์" in s:
            m, v = _q(rf"มวล {N} kg เคลื่อนที่ด้วยความเร็ว {N} m/s", s)
            assert _ans(q) == m * v * v / 2
        elif "พลังงานศักย์" in s:
            m, h = _q(rf"มวล {N} kg อยู่สูงจากพื้น {N} m", s)
            assert _ans(q) == m * 10 * h
        else:
            k, cm = _q(rf"ค่านิจ {N} N/m .*ยืดออก {N} cm", s)
            assert _ans(q) == k * cm / 100, s
        q = generate("phys.work_energy_fluency", Random(seed))
        s = _stem(q)
        if "ถูกอัด" in s:
            k, x = _q(rf"ค่านิจ {N} N/m ถูกอัดเข้าไป {N} m", s)
            assert _ans(q) == k * x * x / 2
        elif "เปลี่ยนความเร็ว" in s:
            m, u, v = _q(rf"มวล {N} kg เปลี่ยนความเร็วจาก {N} m/s เป็น {N} m/s", s)
            assert _ans(q) == m * (v * v - u * u) / 2
        else:
            w, m, u = _q(rf"ทำงาน {N} J กับวัตถุมวล {N} kg ที่มีความเร็วต้น {N} m/s", s)
            assert m * _ans(q) ** 2 / 2 == m * u * u / 2 + w, s
        q = generate("phys.work_energy_application", Random(seed))
        s = _stem(q)
        if "เบรก" in s:
            m, v, d = _q(rf"มวล {N} kg วิ่งด้วยความเร็ว {N} m/s เบรกจนหยุดในระยะ {N} m", s)
            assert _ans(q) == m * v * v / 2 / d, s
        else:
            m, h, v = _q(rf"มวล {N} kg จากพื้นขึ้นไปสูง {N} m แล้วปล่อยให้มีความเร็ว {N} m/s", s)
            assert _ans(q) == m * 10 * h + m * v * v / 2, s


def test_energy_conservation_answers():
    for seed in range(SEEDS):
        q = generate("phys.energy_conservation_calc_foundation", Random(seed))
        s = _stem(q)
        m, h = _q(rf"มวล {N} kg จากความสูง {N} m", s)
        if "พลังงานกล" in s:
            assert _ans(q) == m * 10 * h
        else:
            (pct,) = _q(rf"ตกลงมาได้ {N}%", s)
            assert _ans(q) == m * 10 * h * pct / 100, s
        q = generate("phys.energy_conservation_calc_fluency", Random(seed))
        s = _stem(q)
        if "จุดต่ำสุด" in s:
            (h,) = _q(rf"สูงกว่าจุดต่ำสุด {N} m", s)
            assert _ans(q) ** 2 == 20 * h, s
        elif "โยนลูกบอล" in s:
            (v,) = _q(rf"อัตราเร็ว {N} m/s", s)
            assert _ans(q) == v * v / 20, s
        else:
            k, x, m = _q(rf"สปริงค่านิจ {N} N/m ถูกอัดเข้าไป {N} m แล้วดีดลูกบอลมวล {N} kg", s)
            assert _ans(q) == k * x * x / 2 / (m * 10), s
        q = generate("phys.energy_conservation_calc_application", Random(seed))
        s = _stem(q)
        if "ยาว" in s:
            m, h, length, v = _q(rf"มวล {N} kg ไถลลงสไลเดอร์สูง {N} m ยาว {N} m .*อัตราเร็ว {N} m/s", s)
            assert _ans(q) == (m * 10 * h - m * v * v / 2) / length, s
        else:
            m, h, v = _q(rf"มวล {N} kg ไถลลงสไลเดอร์สูง {N} m .*อัตราเร็ว {N} m/s", s)
            assert _ans(q) == m * 10 * h - m * v * v / 2, s


def test_machine_answers():
    for seed in range(SEEDS):
        q = generate("phys.machine_advantage_foundation", Random(seed))
        s = _stem(q)
        if "การได้เปรียบเชิงกลเท่าใด" in s:
            effort, load = _q(rf"แรงพยายาม {N} N ยกวัตถุหนัก {N} N", s)
            assert _ans(q) == load / effort, s
        q = generate("phys.machine_advantage_fluency", Random(seed))
        s = _stem(q)
        effort, load, length, h = _q(rf"ใช้แรง {N} N ดันกล่องหนัก {N} N ขึ้นพื้นเอียงยาว {N} m ซึ่งสูง {N} m", s)
        assert _ans(q) == load * h / (effort * length) * 100, s
        q = generate("phys.machine_advantage_application", Random(seed))
        s = _stem(q)
        if "รอกพวง" in s:
            ropes, load = _q(rf"รับน้ำหนัก {N} เส้น ใช้ยกวัตถุหนัก {N} N", s)
            assert _ans(q) == load / ropes, s
        elif "พื้นเอียง" in s:
            load, length, h, eff = _q(rf"หนัก {N} N ขึ้นพื้นเอียงยาว {N} m สูง {N} m พื้นเอียงมีประสิทธิภาพ {N}%", s)
            assert _ans(q) == load * h / length / (eff / 100), s
        else:
            load, la, ea = _q(rf"หินหนัก {N} N โดยจุดหมุนอยู่ห่างหิน {N} m และมือกดห่างจากจุดหมุน {N} m", s)
            assert _ans(q) == load * la / ea, s


# ── Slices 5-6: ฟิสิกส์เพิ่มเติม 1 ม.4/9, /14-/17, /1 and /2 ─────────────────────

def test_centre_of_mass_answers():
    for seed in range(SEEDS):
        q = generate("phys.centre_of_mass_foundation", Random(seed))
        s = _stem(q)
        if "แท่งเบา" in s:
            m1, m2, length, near = _q(rf"ติดมวล {N} kg และ {N} kg .*ยาว {N} cm .*ห่างจากมวล {N} kg", s)
            assert near == m1 and _ans(q) == m2 * length / (m1 + m2), s
        q = generate("phys.centre_of_mass_fluency", Random(seed))
        s = _stem(q)
        if "บนแกน x" in s:
            pairs = [(Fraction(m), Fraction(x)) for m, x in re.findall(r"มวล (\d+) kg ที่ x = (\d+) m", s)]
            assert len(pairs) == 3, s
            assert _ans(q) == sum(m * x for m, x in pairs) / sum(m for m, _ in pairs), s
        else:
            rod, length, mass = _q(rf"มวล {N} kg ยาว {N} cm มีมวล {N} kg", s)
            assert _ans(q) == mass * (length / 2) / (rod + mass), s
        q = generate("phys.centre_of_mass_application", Random(seed))
        s = _stem(q)
        if "ยื่นพ้นขอบโต๊ะ" in s:
            plank, length, load = _q(rf"มวล {N} kg ยาว {N} m .*กล่องมวล {N} kg", s)
            x = _ans(q)
            # The system's centre of mass sits exactly over the edge.
            assert plank * (length / 2 - x) == load * x, s
        elif "ยกปลายแผ่นไม้" in s:
            b, h = _q(rf"ฐานกว้าง {N} cm สูง {N} cm", s)
            assert _answer(q) == {Fraction(3, 4): "37°", 1: "45°", Fraction(4, 3): "53°"}[b / h], s
        else:
            objects = re.findall(r"(\S) ฐานกว้าง (\d+) cm ศูนย์ถ่วงสูงจากพื้น (\d+) cm", s)
            best = max(objects, key=lambda o: Fraction(int(o[1]), int(o[2])))
            assert _answer(q) == f"ชิ้น {best[0]}", s


def test_momentum_and_impulse_answers():
    for seed in range(SEEDS):
        q = generate("phys.momentum_impulse_foundation", Random(seed))
        s = _stem(q)
        if " g " in s:
            grams, v = _q(rf"มวล {N} g .*ความเร็ว {N} m/s", s)
            assert _ans(q) == grams / 1000 * v, s
        elif "มีโมเมนตัม" in s:
            m, v = _q(rf"มวล {N} kg .*ความเร็ว {N} m/s", s)
            assert _ans(q) == m * v, s
        q = generate("phys.momentum_impulse_fluency", Random(seed))
        s = _stem(q)
        if "คงที่อีก" in s:
            f, t1, t2, t3 = _q(rf"เป็น {N} N ในเวลา {N} s คงที่อีก {N} s แล้วลดเป็น 0 ในเวลา {N} s", s)
            assert _ans(q) == f * (t2 + (t1 + t3) / 2), s
        elif "แรงคงที่" in s:
            f, t = _q(rf"แรงคงที่ {N} N เป็นเวลา {N} s", s)
            assert _ans(q) == f * t, s
        elif "ลดกลับเป็น 0" in s:
            f, t = _q(rf"เป็น {N} N แล้วลดกลับเป็น 0 เป็นเส้นตรง ในเวลารวม {N} s", s)
            assert _ans(q) == f * t / 2, s
        elif "กระดอนกลับ" in s:
            m, u, v = _q(rf"มวล {N} kg .*อัตราเร็ว {N} m/s .*อัตราเร็ว {N} m/s", s)
            assert _ans(q) == m * (u + v), s
        else:
            m, u, j = _q(rf"มวล {N} kg .*ความเร็ว {N} m/s ได้รับการดลขนาด {N} N·s", s)
            assert _ans(q) == u + j / m, s
        q = generate("phys.momentum_impulse_application", Random(seed))
        s = _stem(q)
        if "ชนกำแพง" in s:
            m, v, dt = _q(rf"มวล {N} kg .*ความเร็ว {N} m/s .*ในเวลา {N} s", s)
            assert _ans(q) == m * v / dt, s
        elif "ลูกฟุตบอล" in s:
            grams, u, v, ms = _q(rf"มวล {N} g .*อัตราเร็ว {N} m/s .*อัตราเร็ว {N} m/s .*นาน {N} ms", s)
            assert _ans(q) == grams / 1000 * (u + v) / (ms / 1000), s
        elif "ได้รับแรงดลเฉลี่ย" in s:
            t1, f1, t2 = _q(rf"หยุดในเวลา {N} s ได้รับแรงดลเฉลี่ย {N} N .*ใช้เวลาหยุด {N} s", s)
            assert _ans(q) == f1 * t1 / t2, s
        else:
            assert _answer(q) == "เพิ่มเวลาในการเปลี่ยนโมเมนตัม แรงดลเฉลี่ยจึงลดลง", s


def test_collision_answers_conserve_momentum():
    for seed in range(SEEDS):
        q = generate("phys.collision_1d_foundation", Random(seed))
        s = _stem(q)
        if "ติดกันไป" in s and "มวล" in s:
            m1, u, m2 = _q(rf"มวล {N} kg เคลื่อนที่ด้วยความเร็ว {N} m/s ชน\S*มวล {N} kg", s)
            assert _ans(q) * (m1 + m2) == m1 * u, s
        q = generate("phys.collision_1d_fluency", Random(seed))
        s = _stem(q)
        if "ชนประสานงา" in s:
            m1, u1, m2, u2 = _q(rf"มวล {N} kg วิ่งไปทางขวาด้วยอัตราเร็ว {N} m/s .*มวล {N} kg ที่วิ่งไปทางซ้ายด้วยอัตราเร็ว {N} m/s", s)
            assert _ans(q) * (m1 + m2) == m1 * u1 - m2 * u2, s
        elif "ชนลูกบอล ข" in s:
            m1, u, m2, v1 = _q(rf"มวล {N} kg เคลื่อนที่ด้วยความเร็ว {N} m/s ชนลูกบอล ข มวล {N} kg .*ความเร็ว {N} m/s", s)
            assert m1 * u == m1 * v1 + m2 * _ans(q), s
        elif "ปืน" in s:
            gun, grams, v = _q(rf"ปืนมวล {N} kg ยิงกระสุนมวล {N} g ออกไปด้วยอัตราเร็ว {N} m/s", s)
            assert gun * _ans(q) == grams / 1000 * v, s
        else:
            m1, m2, v = _q(rf"มวล {N} kg และ {N} kg .*เคลื่อนที่ออกด้วย\s*อัตราเร็ว {N} m/s", s)
            assert m2 * _ans(q) == m1 * v, s
        q = generate("phys.collision_1d_application", Random(seed))
        s = _stem(q)
        if "สูญเสีย" in s:
            m1, u, m2 = _q(rf"มวล {N} kg เคลื่อนที่ด้วยความเร็ว {N} m/s ชนวัตถุมวล {N} kg", s)
            v = m1 * u / (m1 + m2)
            assert _ans(q) == m1 * u * u / 2 - (m1 + m2) * v * v / 2, s
        elif "เป็นแบบใด" in s:
            m1, u, m2, v1, v2 = _q(rf"มวล {N} kg .*ความเร็ว {N} m/s ชนรถทดลอง ข มวล {N} kg .*ความเร็ว {N} m/s และ {N} m/s", s)
            assert m1 * u == m1 * v1 + m2 * v2, s
            elastic = m1 * u * u == m1 * v1 * v1 + m2 * v2 * v2
            assert m1 * u * u >= m1 * v1 * v1 + m2 * v2 * v2, s
            assert _answer(q).startswith("การชนแบบยืดหยุ่น" if elastic else "การชนแบบไม่ยืดหยุ่น"), s
        elif "มวลเท่ากัน" in s:
            (u,) = _q(rf"ความเร็ว {N} m/s ชนตรง", s)
            assert _answer(q) == f"ก หยุดนิ่ง และ ข เคลื่อนที่ด้วยความเร็ว {u} m/s", s
        else:
            m1, u, m2 = _q(rf"มวล {N} kg เคลื่อนที่ด้วยความเร็ว {N} m/s ชนตรงกับวัตถุมวล {N} kg", s)
            v2 = _ans(q)
            v1 = (m1 * u - m2 * v2) / m1
            # Both momentum and kinetic energy survive an elastic hit.
            assert m1 * u * u == m1 * v1 * v1 + m2 * v2 * v2, s


def test_projectile_answers():
    for seed in range(SEEDS):
        q = generate("phys.projectile_foundation", Random(seed))
        s = _stem(q)
        if "ใช้เวลาเท่าใดจึงถึงพื้น" in s:
            (h,) = _q(rf"สูง {N} m", s)
            assert 5 * _ans(q) ** 2 == h, s
        elif "เมื่อผ่านไป" in s:
            (u,) = _q(rf"ความเร็ว {N} m/s", s)
            assert _ans(q) == u, s
        q = generate("phys.projectile_fluency", Random(seed))
        s = _stem(q)
        if "จากที่สูง" in s:
            u, h = _q(rf"ความเร็ว {N} m/s จากที่สูง {N} m", s)
        else:
            h, u = _q(rf"สูง {N} m.*?ความเร็ว {N} m/s", s)
        t = next(Fraction(k, 10) for k in range(1, 100) if 5 * Fraction(k, 10) ** 2 == h)
        if "ตกห่าง" in s:
            assert _ans(q) == u * t, s
        elif "แนวดิ่ง" in s:
            assert _ans(q) == 10 * t, s
        else:
            assert _ans(q) ** 2 == u * u + (10 * t) ** 2, s
        q = generate("phys.projectile_application", Random(seed))
        s = _stem(q)
        u, angle = _q(rf"ความเร็ว {N} m/s ทำมุม {N}°", s)
        sin = Fraction(3, 5) if angle == 37 else Fraction(4, 5)
        cos = Fraction(4, 5) if angle == 37 else Fraction(3, 5)
        flight = 2 * u * sin / 10
        if "นานเท่าใด" in s:
            assert _ans(q) == flight, s
        elif "สูงสุด" in s:
            assert _ans(q) == (u * sin) ** 2 / 20, s
        else:
            assert _ans(q) == u * cos * flight, s


def test_circular_motion_answers():
    for seed in range(SEEDS):
        q = generate("phys.circular_motion_foundation", Random(seed))
        s = _stem(q)
        if "รอบในเวลา" in s:
            n, t = _q(rf"ครบ {N} รอบในเวลา {N} s", s)
            assert _ans(q) == (t / n if "คาบ" in s else n / t), s
        elif "อัตราเร็วเชิงเส้น" in s:
            r, w = _q(rf"รัศมี {N} m ด้วยอัตราเร็วเชิงมุม {N} rad/s", s)
            assert _ans(q) == w * r, s
        q = generate("phys.circular_motion_fluency", Random(seed))
        s = _stem(q)
        if "จุกยาง" in s:
            m, r, v = _q(rf"มวล {N} kg .*รัศมี {N} m .*อัตราเร็ว {N} m/s", s)
            assert _ans(q) == m * v * v / r, s
        elif "วงเวียน" in s:
            r, v = _q(rf"รัศมี {N} m ด้วยอัตราเร็วคงตัว {N} m/s", s)
            assert _ans(q) == v * v / r, s
        elif "เชิงมุม" in s:
            m, r, w = _q(rf"มวล {N} kg .*รัศมี {N} m ด้วยอัตราเร็วเชิงมุม {N} rad/s", s)
            assert _ans(q) == m * w * w * r, s
        else:
            tension, m, r = _q(rf"มากที่สุด {N} N .*มวล {N} kg .*รัศมี {N} m", s)
            assert m * _ans(q) ** 2 / r == tension, s
        q = generate("phys.circular_motion_application", Random(seed))
        s = _stem(q)
        if "สัมประสิทธิ์" in s:
            r, mu = _q(rf"รัศมีความโค้ง {N} m สัมประสิทธิ์ความเสียดทานสถิตระหว่างยางกับถนน {N}", s)
            assert _ans(q) ** 2 == mu * 10 * r, s
        elif "ต้องมีแรงเสียดทาน" in s:
            m, r, v = _q(rf"มวล {N} kg .*รัศมีความโค้ง {N} m ด้วยอัตราเร็วคงตัว {N} m/s", s)
            assert _ans(q) == m * v * v / r, s
        elif "ดาวเทียม" in s:
            r, g = _q(rf"รัศมี {N} km .*เท่ากับ {N} m/s²", s)
            assert _ans(q) ** 2 == g * r * 1000, s
        else:
            found = re.search(r"อัตราเร็วเพิ่มเป็น (\d+) เท่า", s)
            speed = Fraction(found.group(1)) if found else 1
            radius = (Fraction(1, 2) if "ครึ่งหนึ่ง" in s else 1 if "รัศมีเท่าเดิม" in s
                      else Fraction(re.search(r"รัศมีเพิ่มเป็น (\d+) เท่า", s).group(1)))
            assert _ans(q) == speed * speed / radius, s


def test_physics_history_pairs_each_physicist_with_their_own_work():
    from otk.sets.physics.m4.physics_history import SCIENTISTS, TECHNOLOGY
    work_of = dict(SCIENTISTS)
    idea_of = dict(TECHNOLOGY)
    for seed in range(SEEDS):
        q = generate("phys.physics_history_foundation", Random(seed))
        s = _stem(q)
        assert s == f"นักวิทยาศาสตร์คนใด{work_of[_answer(q)]}", s
        q = generate("phys.physics_history_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ผลงานที่สำคัญของ"):
            name = s.removeprefix("ผลงานที่สำคัญของ").removesuffix("คือข้อใด")
            assert _answer(q) == work_of[name], s
        q = generate("phys.physics_history_application", Random(seed))
        s = _stem(q)
        if s.startswith("เทคโนโลยีใด"):
            assert s.endswith(idea_of[_answer(q)]), s
        else:
            assert s.startswith(next(t for t, i in TECHNOLOGY if i == _answer(q))), s


def _significant(reading: str) -> int:
    digits = reading.replace(".", "").lstrip("0")
    return len(digits)


def test_measurement_answers():
    exponent = {"k": 3, "M": 6, "G": 9, "c": -2, "m": -3, "µ": -6, "n": -9}
    superscript = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")
    for seed in range(SEEDS):
        q = generate("phys.measurement_graph_foundation", Random(seed))
        s = _stem(q)
        if "เลขนัยสำคัญ" in s:
            reading = re.search(r"ค่าที่วัดได้ (\S+)", s).group(1)
            assert _answer(q) == f"{_significant(reading)} ตัว", s
        else:
            value, prefix = re.search(r"^(\d+) (\S)", s).groups()
            power = int(re.search(r"× 10(\S+)", _answer(q)).group(1).translate(superscript))
            assert _answer(q).startswith(f"{value} × 10") and power == exponent[prefix], s
        q = generate("phys.measurement_graph_fluency", Random(seed))
        s = _stem(q)
        if "ควรรายงาน" in s:
            a, da, b, db = _q(rf"\({N} ± {N}\) cm และ \({N} ± {N}\) cm", s)
            total = a + b if "ผลรวม" in s else abs(a - b)
            got = [Fraction(x) for x in re.findall(r"[\d.]+", _answer(q))]
            assert got == [total, da + db], s
        elif "พื้นที่" in s:
            ell, dl, w, dw = _q(rf"\({N} ± {N}\) cm และ \({N} ± {N}\) cm", s)
            assert _ans(q) == (dl / ell + dw / w) * 100, s
        else:
            standard, measured = _q(rf"ค่ามาตรฐาน {N} .*วัดได้ {N}", s)
            assert _ans(q) == abs(measured - standard) / standard * 100, s
        q = generate("phys.measurement_graph_application", Random(seed))
        s = _stem(q)
        if "ผ่านจุด" in s:
            x1, y1, x2, y2 = _q(rf"ผ่านจุด \({N} \S+, {N} \S+\) และ \({N} \S+, {N} \S+\)", s)
            slope = (y2 - y1) / (x2 - x1)
            assert _ans(q) == (y1 - slope * x1 if "x = 0" in s or "= 0)" in s else slope), s


# ── Slices 7-8: ฟิสิกส์เพิ่มเติม 2 ม.5/1-7 ──────────────────────────────────────

def _speed_at(celsius: Fraction) -> Fraction:
    return 331 + Fraction(3, 5) * celsius


def test_shm_answers():
    for seed in range(SEEDS):
        q = generate("phys.shm_foundation", Random(seed))
        s = _stem(q)
        if "รอบในเวลา" in s:
            n, t = _q(rf"ครบ {N} รอบในเวลา {N} s", s)
            assert _ans(q) == (t / n if "คาบ" in s else n / t), s
        elif "ห่างกัน" in s:
            (span,) = _q(rf"ห่างกัน {N} cm", s)
            assert _ans(q) == span / 2, s
        q = generate("phys.shm_fluency", Random(seed))
        s = _stem(q)
        m, k = _q(rf"มวล {N} kg ติดปลายสปริงค่านิจ {N} N/m", s)
        w = next(x for x in range(1, 50) if x * x == k / m)
        if "ความถี่เชิงมุม" in s:
            assert _ans(q) == w, s
        elif "อัตราเร็วสูงสุด" in s:
            (amp,) = _q(rf"แอมพลิจูด {N} cm", s)
            assert _ans(q) == amp / 100 * w, s
        elif "ความเร่งสูงสุด" in s:
            (amp,) = _q(rf"แอมพลิจูด {N} cm", s)
            assert _ans(q) == amp / 100 * w * w, s
        else:
            got = Fraction(_answer(q).split("π")[0] or "1")
            assert got == Fraction(2, w), s
        q = generate("phys.shm_application", Random(seed))
        s = _stem(q)
        if "ลูกตุ้มอย่างง่ายยาว" in s:
            (length,) = _q(rf"ยาว {N} m", s)
            assert _ans(q) ** 2 == 4 * length, s
        elif "ต้องใช้เชือกยาว" in s:
            (t,) = _q(rf"คาบ {N} s", s)
            assert _ans(q) == t * t / 4, s
        elif "π² ≈ 10" in s:
            m, k = _q(rf"มวล {N} kg ติดปลายสปริงค่านิจ {N} N/m", s)
            assert _ans(q) ** 2 == 40 * m / k, s
        else:
            found = re.search(r"เพิ่มเป็น (\d+) เท่า", s)
            factor = Fraction(found.group(1)) if found else 1 / Fraction(re.search(r"ลดเหลือ 1/(\d+) เท่า", s).group(1))
            grows = "ความยาวเชือก" in s or "ถ้ามวล" in s
            assert _ans(q) ** 2 == (factor if grows else 1 / factor), s


def test_natural_frequency_answers():
    for seed in range(SEEDS):
        q = generate("phys.natural_frequency_foundation", Random(seed))
        s = _stem(q)
        if "ชิงช้าแกว่งเอง" in s:
            n, t = _q(rf"ครบ {N} รอบในเวลา {N} s", s)
            assert Fraction(_answer(q).split()[0]) == n / t, s
        q = generate("phys.natural_frequency_fluency", Random(seed))
        s = _stem(q)
        if "ตัวขับ" in s:
            (driver,) = _q(rf"ตัวขับที่ยาว {N} cm", s)
            name = _answer(q).split()[-1]
            assert f"{name} ยาว {driver} cm" in s, s
        else:
            (period,) = _q(rf"คาบ {N} s", s)
            assert _ans(q) == 1 / period, s
        q = generate("phys.natural_frequency_application", Random(seed))
        s = _stem(q)
        if "ความถี่ธรรมชาติ" in s and "Hz" in s:
            (f,) = _q(rf"ความถี่ธรรมชาติ {N} Hz", s)
            assert _ans(q) == f * 60, s
        elif "รอบต่อนาที" in s:
            (rpm,) = _q(rf"อัตรา {N} รอบต่อนาที", s)
            assert _ans(q) == rpm / 60, s
        else:
            assert "ความถี่ธรรมชาติ" in _answer(q), s


def test_wave_answers():
    for seed in range(SEEDS):
        q = generate("phys.wave_superposition_foundation", Random(seed))
        s = _stem(q)
        if "สันคลื่น" in s and "ห่างกัน" in s:
            crests, span = _q(rf"สันคลื่น {N} สัน.*ห่างกัน {N} m", s)
            assert _ans(q) == span / (crests - 1), s
        elif "จากท้องคลื่นถึงสันคลื่น" in s:
            (height,) = _q(rf"สันคลื่น {N} cm", s)
            assert _ans(q) == height / 2, s
        q = generate("phys.wave_superposition_fluency", Random(seed))
        s = _stem(q)
        if "มีคาบ" in s:
            (f,) = _q(rf"ความถี่ {N} Hz", s)
            assert _ans(q) == 1 / f, s
        elif "มีอัตราเร็ว" in s:
            f, wl = _q(rf"ความถี่ {N} Hz ความยาวคลื่น {N} m", s)
            assert _ans(q) == f * wl, s
        elif "มีความยาวคลื่น" in s:
            v, f = _q(rf"อัตราเร็ว {N} m/s ความถี่ {N} Hz", s)
            assert _ans(q) * f == v, s
        else:
            v, wl = _q(rf"อัตราเร็ว {N} m/s ความยาวคลื่น {N} m", s)
            assert _ans(q) * wl == v, s
        q = generate("phys.wave_superposition_application", Random(seed))
        s = _stem(q)
        if "คลื่นดล" in s:
            a, b = _q(rf"แอมพลิจูด {N} cm และ {N} cm", s)
            assert _ans(q) == (a + b if "ด้านเดียวกัน" in s else abs(a - b)), s
        else:
            wl, gap = _q(rf"ความยาวคลื่น {N} cm .*ห่างกัน {N} cm", s)
            halves = gap / (wl / 2)
            assert halves.denominator == 1, s
            assert _answer(q) == ("เฟสตรงกัน" if halves % 2 == 0 else "เฟสตรงข้ามกัน"), s


def test_water_wave_answers():
    sines = {30: Fraction(1, 2), 37: Fraction(3, 5), 53: Fraction(4, 5)}
    for seed in range(SEEDS):
        q = generate("phys.water_wave_foundation", Random(seed))
        s = _stem(q)
        if "ความถี่ในน้ำตื้น" in s:
            (f,) = _q(rf"ความถี่ {N} Hz", s)
            assert _ans(q) == f, s
        elif "ความยาวคลื่นในน้ำตื้น" in s:
            f, v2 = _q(rf"ความถี่ {N} Hz .*อัตราเร็วเหลือ {N} cm/s", s)
            assert _ans(q) == v2 / f, s
        q = generate("phys.water_wave_fluency", Random(seed))
        s = _stem(q)
        a1, a2 = (int(x) for x in re.findall(r"มุม(?:ตกกระทบ)? (\d+)°", s)[:2])
        ratio = sines[a2] / sines[a1]
        if "ความยาวคลื่นในน้ำตื้น" in s:
            (wl,) = _q(rf"ความยาวคลื่น {N} cm", s)
            assert _ans(q) == wl * ratio, s
        else:
            (v,) = _q(rf"อัตราเร็ว {N} cm/s", s)
            assert _ans(q) == v * ratio, s
        q = generate("phys.water_wave_application", Random(seed))
        s = _stem(q)
        if "อยู่บนแนวใด" in s:
            wl, a, b = _q(rf"ความยาวคลื่น {N} cm จุด P อยู่ห่าง S₁ {N} cm และห่าง S₂ {N} cm", s)
            lines = (b - a) / wl
            if lines.denominator == 1:
                assert _answer(q) == f"แนวปฏิบัพที่ {lines}", s
            else:
                assert _answer(q) == f"แนวบัพที่ {lines + Fraction(1, 2)}", s
        else:
            n, a, b = _q(rf"แนวปฏิบัพที่ {N} .*S₁ {N} cm และห่าง S₂ {N} cm", s)
            assert _ans(q) * n == b - a, s


def test_sound_answers():
    for seed in range(SEEDS):
        q = generate("phys.sound_propagation_foundation", Random(seed))
        s = _stem(q)
        if "อัตราเร็วของเสียงในอากาศเท่าใด" in s:
            (t,) = _q(rf"อุณหภูมิ {N} °C", s)
            assert _ans(q) == _speed_at(t), s
        elif "ใช้เวลาเท่าใด" in s:
            t, d = _q(rf"อุณหภูมิ {N} °C เป็นระยะ {N} m", s)
            assert _ans(q) * _speed_at(t) == d, s
        q = generate("phys.sound_propagation_fluency", Random(seed))
        s = _stem(q)
        if "วัดอัตราเร็ว" in s:
            (v,) = _q(rf"ได้ {N} m/s", s)
            assert _speed_at(_ans(q)) == v, s
        elif "หน้าผาอยู่ห่าง" in s:
            t, echo = _q(rf"อุณหภูมิ {N} °C .*หลังจากตะโกน {N} s", s)
            assert _ans(q) == _speed_at(t) * echo / 2, s
        else:
            f, t = _q(rf"ความถี่ {N} Hz .*อุณหภูมิ {N} °C", s)
            assert _ans(q) == _speed_at(t) / f, s
        q = generate("phys.sound_propagation_application", Random(seed))
        s = _stem(q)
        if "ได้ยินเสียงอย่างไร" in s:
            f, t, a, b = _q(rf"ความถี่ {N} Hz ในอากาศอุณหภูมิ {N} °C .*ตัวหนึ่ง {N} m และอีกตัว {N} m", s)
            halves = (b - a) / (_speed_at(t) / f / 2)
            assert halves.denominator == 1, s
            assert _answer(q).startswith("ดัง" if halves % 2 == 0 else "ค่อย"), s
        else:
            t, gap = _q(rf"อุณหภูมิ {N} °C .*ทั้งสอง {N} m", s)
            assert _ans(q) == _speed_at(t) / (2 * gap), s


def _power_of_ten(label: str) -> int:
    if label.split()[0] == "1":
        return 0
    return int(re.search(r"10(\S+)", label).group(1).translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")))


def test_decibel_answers():
    for seed in range(SEEDS):
        q = generate("phys.sound_decibel_foundation", Random(seed))
        s = _stem(q)
        if "กำลัง" in s:
            p, a = _q(rf"กำลัง {N} W ผ่านพื้นที่ตั้งฉาก {N} m²", s)
            assert _ans(q) == p / a, s
        q = generate("phys.sound_decibel_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("เสียง ก"):
            loud, quiet = (_power_of_ten(x) for x in re.findall(r"ความเข้ม (1|10\S+) W/m²", s))
            assert _ans(q) == 10 * (loud - quiet), s
        elif s.startswith("เสียงมีความเข้ม"):
            exponent = _power_of_ten(re.search(r"ความเข้ม (1|10\S+) W/m²", s).group(1))
            assert _ans(q) == 10 * (exponent + 12), s
        else:
            (level,) = _q(rf"ระดับความเข้มเสียง {N} dB", s)
            assert _power_of_ten(_answer(q)) == level / 10 - 12, s
        q = generate("phys.sound_decibel_application", Random(seed))
        s = _stem(q)
        steps = {10: 10, 100: 20, 1000: 30, 2: 3, 20: 13, 200: 23}
        if "เครื่องพร้อมกัน" in s:
            base, count = _q(rf"ได้ยินเสียง {N} dB .*แบบเดียวกัน {N} เครื่อง", s)
            assert _ans(q) == base + steps[int(count)], s
        elif "ถอยออกไป" in s:
            r, level, far = _q(rf"ห่างจากแหล่งกำเนิดเสียง {N} m ได้ยินเสียง {N} dB .*อยู่ห่าง {N} m", s)
            assert _ans(q) == level - 2 * steps[int(far / r)], s
        else:
            (gap,) = _q(rf"อยู่ {N} dB", s)
            assert _answer(q) == f"{10 ** int(gap / 10):,} เท่า", s


def test_pipe_beat_and_doppler_answers():
    for seed in range(SEEDS):
        q = generate("phys.sound_resonance_tube_foundation", Random(seed))
        s = _stem(q)
        if "บีตกี่ครั้ง" in s:
            f1, f2 = _q(rf"ความถี่ {N} Hz และ {N} Hz", s)
            assert _ans(q) == abs(f1 - f2), s
        q = generate("phys.sound_resonance_tube_fluency", Random(seed))
        s = _stem(q)
        if "ครั้งแรกและครั้งที่สอง" in s:
            f, l1, l2 = _q(rf"ความถี่ {N} Hz .*ยาว {N} cm และ {N} cm", s)
            assert _ans(q) == f * 2 * (l2 - l1) / 100, s
        elif "ลำอากาศยาวเท่าใด" in s:
            f, t = _q(rf"ความถี่ {N} Hz .*อุณหภูมิ {N} °C", s)
            n = {"ครั้งแรก": 1, "ครั้งที่สอง": 2, "ครั้งที่สาม": 3}[re.search(r"สั่นพ้อง(ครั้ง\S+?) ขณะ", s).group(1)]
            assert _ans(q) == (2 * n - 1) * _speed_at(t) / f / 4 * 100, s
        else:
            f, nodes, span = _q(rf"ความถี่ {N} Hz .*มีบัพ {N} บัพ .*ห่างกัน {N} m", s)
            assert _ans(q) == f * 2 * span / (nodes - 1), s
        q = generate("phys.sound_resonance_tube_application", Random(seed))
        s = _stem(q)
        if "ไซเรน" in s:
            f, vs = _q(rf"ความถี่ {N} Hz วิ่งด้วยอัตราเร็ว {N} m/s", s)
            expected = f * 340 / (340 - vs if "เข้าหา" in s else 340 + vs)
            assert _ans(q) == expected, s
        elif "เลขมัค" in s:
            (v,) = _q(rf"อัตราเร็ว {N} m/s", s)
            assert _ans(q) == v / 340, s
        else:
            assert _answer(q).startswith("เกิด"), s


# ── Slices 9-10: ฟิสิกส์เพิ่มเติม 2 ม.5/8, /11-/13 and ฟิสิกส์เพิ่มเติม 3 ม.5/1-/3 ──

_SIN = {30: Fraction(1, 2), 37: Fraction(3, 5), 53: Fraction(4, 5)}


def test_light_interference_answers():
    for seed in range(SEEDS):
        q = generate("phys.light_interference_foundation", Random(seed))
        s = _stem(q)
        if "ผลต่างระยะทาง" in s and "nm" in s:
            wl, diff = _q(rf"ความยาวคลื่น {N} nm .*สลิตทั้งสอง {N} nm", s)
            ratio = diff / wl
            expected = (f"แถบสว่างอันดับที่ {ratio}" if ratio.denominator == 1
                        else f"แถบมืดอันดับที่ {ratio + Fraction(1, 2)}")
            assert _answer(q) == expected, s
        q = generate("phys.light_interference_fluency", Random(seed))
        s = _stem(q)
        if "แสงมีความยาวคลื่น" in s:
            d, screen, spacing = _q(rf"ห่างกัน {N} mm ฉากอยู่ห่างสลิต {N} m .*ถัดกันได้ {N} mm", s)
            assert _ans(q) == spacing * d / screen * 1000, s
        else:
            wl, d, screen = _q(rf"ความยาวคลื่น {N} nm ผ่านสลิตคู่ที่ห่างกัน {N} mm ฉากอยู่ห่างสลิต {N} m", s)
            assert _ans(q) == wl * screen / d / 1000, s
        q = generate("phys.light_interference_application", Random(seed))
        s = _stem(q)
        if "เกรตติง" in s:
            lines, n, angle = _q(rf"เกรตติงมี {N} ช่องต่อมิลลิเมตร .*อันดับที่ {N} ทำมุม {N}°", s)
            assert _ans(q) * n == Fraction(10 ** 6) / lines * _SIN[int(angle)], s
        else:
            wl, angle = _q(rf"ความยาวคลื่น {N} nm .*มุม {N}°", s)
            assert _ans(q) * _SIN[int(angle)] == wl, s


def test_thin_lens_answers():
    for seed in range(SEEDS):
        q = generate("phys.thin_lens_foundation", Random(seed))
        s = _stem(q)
        if "เลนส์นูน" in s:
            f, dist = _q(rf"ความยาวโฟกัส {N} cm ห่างจากเลนส์ {N} cm", s)
            ratio = dist / f
            expected = ("ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ" if ratio > 2 else "ภาพจริง หัวกลับ ขนาดเท่าวัตถุ" if ratio == 2
                        else "ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ" if ratio > 1 else "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ")
            assert _answer(q) == expected, s
        elif "เลนส์เว้า" in s:
            assert _answer(q) == "ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ", s
        q = generate("phys.thin_lens_fluency", Random(seed))
        s = _stem(q)
        f, dist = _q(rf"ความยาวโฟกัส {N} cm เป็นระยะ {N} cm", s)
        image = dist * f / (dist - f)
        assert 1 / f == 1 / dist + 1 / image
        assert _ans(q) == (image / dist if "กำลังขยาย" in s else image), s
        q = generate("phys.thin_lens_application", Random(seed))
        s = _stem(q)
        if "ภาพที่ปรากฏบนฉากสูง" in s:
            h, f, dist = _q(rf"วัตถุสูง {N} cm .*ความยาวโฟกัส {N} cm เป็นระยะ {N} cm", s)
            assert _ans(q) == h * (dist * f / (dist - f)) / dist, s
        elif "เลนส์เว้า" in s and "ภาพเสมือน" in s:
            f, dist = _q(rf"ความยาวโฟกัส {N} cm เป็นระยะ {N} cm", s)
            # 1/(−f) = 1/s + 1/s′ with s′ negative: |s′| = sf/(s + f).
            assert -1 / f == 1 / dist - 1 / _ans(q), s
        else:
            (f,) = _q(rf"ความยาวโฟกัส {N} cm", s)
            assert _ans(q) == (100 / f) * (-1 if "เลนส์เว้า" in s else 1), s


def test_light_phenomena_pairs_each_scene_with_its_cause():
    from otk.sets.physics.m5.light_phenomena import PHENOMENA, SITUATIONS
    cause_of = dict(PHENOMENA)
    name_of = {c: n for n, c in PHENOMENA}
    scene_of = dict(SITUATIONS)
    for seed in range(SEEDS):
        q = generate("phys.light_phenomena_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("ปรากฏการณ์ \""):
            assert _answer(q) == cause_of[s.split("\"")[1]], s
        else:
            assert s == f"ปรากฏการณ์ใดเกิดจาก{cause_of[_answer(q)]}", s
            assert name_of[cause_of[_answer(q)]] == _answer(q)
        q = generate("phys.light_phenomena_fluency", Random(seed))
        s = _stem(q)
        assert _answer(q) == scene_of[s.removesuffix(" เป็นปรากฏการณ์ใด")], s
        q = generate("phys.light_phenomena_application", Random(seed))
        s = _stem(q)
        if "ยอดของรุ้ง" in s:
            (sun,) = _q(rf"ขอบฟ้า {N}°", s)
            assert _ans(q) == 42 - sun, s
        elif "จะเห็นรุ้งปฐมภูมิหรือไม่" in s:
            (sun,) = _q(rf"ขอบฟ้า {N}°", s)
            assert sun > 42 and _answer(q).startswith("ไม่เห็น"), s
        elif "ยกกำลังสี่" in s:
            short, long_ = _q(rf"ความยาวคลื่น {N} nm .*ความยาวคลื่น {N} nm", s)
            assert _ans(q) == (long_ / short) ** 4, s


def test_colour_answers_follow_the_primaries():
    from otk.sets._support.science_wave_e15 import COLOUR_NAME, LIGHT_NAME, NAME_COLOUR, PIGMENTS
    light_colour = {name: c for c, name in LIGHT_NAME.items()}
    for seed in range(SEEDS):
        q = generate("phys.colour_perception_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("ฉาย"):
            lights = [light_colour[m] for m in re.findall(r"แสงสี\S+?(?: \(\S+\))?(?= แสง|ซ้อนกัน)", s)]
            assert len(lights) >= 2, s
            assert _answer(q) == COLOUR_NAME[frozenset().union(*lights)].split(" (")[0], s
        q = generate("phys.colour_perception_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ผสม"):
            names = [n for n in PIGMENTS if f"สาร{n}" in s]
            assert _answer(q) == COLOUR_NAME[frozenset.intersection(*(PIGMENTS[n] for n in names))], s
        else:
            body = NAME_COLOUR[re.search(r"ที่เห็นเป็น(.+?)ในแสงขาว", s).group(1)]
            light = light_colour[re.search(r"ไว้ใต้(.+?) จะเห็น", s).group(1)]
            assert _answer(q) == COLOUR_NAME[body & light], s
        q = generate("phys.colour_perception_application", Random(seed))
        s = _stem(q)
        if "ดูเป็นสีดำ" in s:
            body = NAME_COLOUR[re.search(r"ชุดที่เห็นเป็น(.+?)ในแสงขาว", s).group(1)]
            assert not (light_colour[_answer(q)] & body), s
        elif "ฉายแสงสีใดเพิ่ม" in s:
            start = light_colour[re.search(r"^ฉาย(.+?)บนฉาก", s).group(1)]
            target = NAME_COLOUR[re.search(r"จึงเห็นเป็น(.+)$", s).group(1)]
            assert start | light_colour[_answer(q)] == target, s


def test_charge_answers():
    for seed in range(SEEDS):
        q = generate("phys.charging_fluency", Random(seed))
        s = _stem(q)
        if "แตะกัน" in s:
            q1, q2 = (Fraction(("-" if sign == "−" else "") + v) for sign, v in re.findall(r"([+−])(\d+) μC", s))
            assert _ans(q) == (q1 + q2) / 2, s
        q = generate("phys.charging_application", Random(seed))
        s = _stem(q)
        positive = any(k in s for k in ("แท่งแก้วที่ถูกับผ้าไหม", "แท่งประจุบวก"))
        rod, other = ("บวก", "ลบ") if positive else ("ลบ", "บวก")
        if "เอานิ้วออก" in s:
            assert _answer(q) == f"ประจุ{other}", s
        elif "แยก A กับ B" in s:
            assert _answer(q).startswith(f"A มีประจุ{other} และ B มีประจุ{rod}"), s
        elif "(ไม่แตะ)" in s:
            assert _answer(q) == f"ประจุ{rod} แผ่นโลหะกางออก", s
        elif s.startswith("แตะ"):
            assert _answer(q).startswith(f"ประจุ{rod}"), s


def test_coulomb_and_field_answers():
    k, micro = 9 * 10 ** 9, Fraction(1, 10 ** 6)
    for seed in range(SEEDS):
        q = generate("phys.coulomb_force_fluency", Random(seed))
        s = _stem(q)
        if "วางห่างกัน" in s:
            q1, q2, r = _q(rf"จุดประจุ {N} μC และ {N} μC วางห่างกัน {N} cm", s)
            assert _ans(q) == k * q1 * q2 * micro * micro / (r / 100) ** 2, s
        else:
            q1, q2, f = _q(rf"จุดประจุ {N} μC และ {N} μC ออกแรงต่อกัน {N} N", s)
            assert f * (_ans(q) / 100) ** 2 == k * q1 * q2 * micro * micro, s
        q = generate("phys.coulomb_force_foundation", Random(seed))
        s = _stem(q)
        if "แรงแบบใด" in s:
            signs = re.findall(r"([+−])\d+ μC", s)
            assert _answer(q) == ("แรงผลัก" if signs[0] == signs[1] else "แรงดึงดูด"), s
        q = generate("phys.coulomb_force_application", Random(seed))
        s = _stem(q)
        if "แนวเส้นตรง" in s:
            qa, qb, qt, d1, d2 = _q(rf"A = \+{N} μC และ B = \+{N} μC .*ประจุ \+{N} μC .*ห่าง A {N} cm และห่าง B {N} cm", s)
            fa = k * qa * qt * micro * micro / (d1 / 100) ** 2
            fb = k * qb * qt * micro * micro / (d2 / 100) ** 2
            assert _ans(q) == abs(fa - fb), s
        else:
            f1, f2 = _q(rf"ขนาด {N} N และ {N} N", s)
            assert _ans(q) ** 2 == f1 * f1 + f2 * f2, s
        q = generate("phys.electric_field_foundation", Random(seed))
        s = _stem(q)
        if "ได้รับแรงไฟฟ้า" in s:
            charge, e = _q(rf"ประจุ {N} μC .*ขนาด {N} N/C", s)
            assert _ans(q) == charge * micro * e, s
        q = generate("phys.electric_field_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("จุดประจุ"):
            charge, r = _q(rf"จุดประจุ {N} μC .*ห่างจากประจุ {N} cm", s)
            assert _ans(q) == k * charge * micro / (r / 100) ** 2, s
        else:
            r, e = _q(rf"ห่างจากจุดประจุ {N} cm สนามไฟฟ้ามีขนาด {N} N/C", s)
            assert _ans(q) * micro * k == e * (r / 100) ** 2, s
        q = generate("phys.electric_field_application", Random(seed))
        s = _stem(q)
        if "จุดกึ่งกลาง" in s:
            found = re.search(rf"A = \+{N} μC และ B = ([+−]){N} μC วางห่างกัน {N} m", s)
            qa, qb, d = Fraction(found.group(1)), Fraction(found.group(3)), Fraction(found.group(4))
            ea = k * qa * micro / (d / 2) ** 2
            eb = k * qb * micro / (d / 2) ** 2
            assert _ans(q) == (ea + eb if found.group(2) == "−" else abs(ea - eb)), s
        else:
            e1, e2 = _q(rf"ขนาด {N} N/C และ {N} N/C", s)
            assert _ans(q) ** 2 == e1 * e1 + e2 * e2, s


# ── Slices 11-12: ฟิสิกส์เพิ่มเติม 3 ม.5/5-/7, /10-/11, ม.6/1-/2 ──────────────────

def test_capacitor_answers():
    for seed in range(SEEDS):
        q = generate("phys.capacitor_foundation", Random(seed))
        s = _stem(q)
        if "เก็บประจุได้กี่ไมโครคูลอมบ์" in s:
            c, v = _q(rf"ความจุ {N} μF ต่อกับความต่างศักย์ {N} V", s)
            assert _ans(q) == c * v, s
        elif "มีความจุกี่ไมโครฟารัด" in s:
            charge, v = _q(rf"เก็บประจุ {N} μC เมื่อต่อกับความต่างศักย์ {N} V", s)
            assert _ans(q) == charge / v, s
        q = generate("phys.capacitor_fluency", Random(seed))
        s = _stem(q)
        if "ความจุ" in s:
            c, v = _q(rf"ความจุ {N} μF อัดประจุด้วยความต่างศักย์ {N} V", s)
            assert _ans(q) == c * v * v / 2 / 1000, s
        else:
            charge, v = _q(rf"มีประจุ {N} μC และความต่างศักย์ {N} V", s)
            assert _ans(q) == charge * v / 2 / 1000, s
        q = generate("phys.capacitor_application", Random(seed))
        s = _stem(q)
        caps = [Fraction(x) for x in re.findall(r"(\d+) μF", s)]
        if "แบบขนาน" in s:
            assert _ans(q) == sum(caps), s
        elif "ความจุสมมูล" in s:
            assert 1 / _ans(q) == sum(1 / c for c in caps), s
        else:
            (v,) = _q(rf"แบตเตอรี่ {N} V", s)
            caps = caps[:2]  # the stem names the asked capacitor a second time
            series = 1 / sum(1 / c for c in caps)
            assert _ans(q) == series * v / caps[0], s


def test_static_uses_pair_each_case_with_its_reason():
    from otk.sets.physics.m5.electrostatic_use import DEVICES, EVENTS, SAFETY
    how_of, why_of, action_of = dict(DEVICES), dict(EVENTS), dict(SAFETY)
    for seed in range(SEEDS):
        q = generate("phys.electrostatic_use_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("ทำงานโดยอาศัยหลักการใด"):
            assert _answer(q) == how_of[s.removesuffix("ทำงานโดยอาศัยหลักการใด")], s
        else:
            assert s == f"อุปกรณ์ใดทำงานโดย{how_of[_answer(q)]}", s
        q = generate("phys.electrostatic_use_fluency", Random(seed))
        s = _stem(q)
        assert _answer(q) == why_of[s.removesuffix(" อธิบายได้ด้วยข้อใด")], s
        q = generate("phys.electrostatic_use_application", Random(seed))
        s = _stem(q)
        assert _answer(q) == action_of[s], s


def test_drift_answers():
    for seed in range(SEEDS):
        q = generate("phys.drift_current_foundation", Random(seed))
        s = _stem(q)
        if "ผ่านภาคตัดขวางของลวดในเวลา" in s:
            charge, t = _q(rf"ประจุ {N} C .*ในเวลา {N} s", s)
            assert _ans(q) == charge / t, s
        elif "กี่ตัวในหนึ่งวินาที" in s:
            (current,) = _q(rf"กระแสไฟฟ้า {N} A", s)
            mantissa, exponent = re.search(r"^([\d.]+) × 10(\S+) ตัว", _answer(q)).groups()
            power = int(exponent.translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")))
            assert Fraction(mantissa) * Fraction(10) ** power * Fraction(16, 10) * Fraction(1, 10 ** 19) == current, s
        q = generate("phys.drift_current_fluency", Random(seed))
        s = _stem(q)
        if "ความเร็วลอยเลื่อนของอิเล็กตรอนกี่มิลลิเมตร" in s:
            area, current = _q(rf"พื้นที่หน้าตัด {N} mm² มีกระแสไฟฟ้า {N} A", s)
            assert current == 8 * area * _ans(q), s
        else:
            area, speed = _q(rf"พื้นที่หน้าตัด {N} mm² มีความเร็วลอยเลื่อน {N} mm/s", s)
            assert _ans(q) == 8 * area * speed, s
        q = generate("phys.drift_current_application", Random(seed))
        s = _stem(q)
        if "สองช่วง" in s:
            a1, v, a2 = _q(rf"พื้นที่หน้าตัด {N} mm² อิเล็กตรอนมีความเร็วลอยเลื่อน {N} mm/s ช่วงที่สองพื้นที่หน้าตัด {N} mm²", s)
            assert _ans(q) * a2 == v * a1, s
        else:
            (v,) = _q(rf"ความเร็วลอยเลื่อน {N} mm/s", s)
            found = re.search(r"เพิ่มเป็น (\d+) เท่า", s)
            factor = Fraction(found.group(1)) if found else Fraction(1, 2)
            assert _ans(q) == v * factor, s


def test_battery_answers():
    for seed in range(SEEDS):
        q = generate("phys.battery_emf_foundation", Random(seed))
        s = _stem(q)
        n, e, r = _q(rf"เหมือนกัน {N} ก้อน แต่ละก้อนมีอีเอ็มเอฟ {N} V ความต้านทานภายใน {N} Ω", s)
        series = "อนุกรม" in s
        if "อีเอ็มเอฟสมมูล" in s:
            assert _ans(q) == (n * e if series else e), s
        else:
            assert _ans(q) == (n * r if series else r / n), s
        q = generate("phys.battery_emf_fluency", Random(seed))
        s = _stem(q)
        e, r, big_r = _q(rf"อีเอ็มเอฟ {N} V ความต้านทานภายใน {N} Ω ต่อกับตัวต้านทาน {N} Ω", s)
        i = e / (big_r + r)
        assert _ans(q) == (i if "กระแสไฟฟ้าในวงจร" in s else i * big_r), s
        q = generate("phys.battery_emf_application", Random(seed))
        s = _stem(q)
        n, e, r, big_r = _q(rf"เหมือนกัน {N} ก้อน แต่ละก้อนมีอีเอ็มเอฟ {N} V ความต้านทานภายใน {N} Ω .*ตัวต้านทาน {N} Ω", s)
        e_eq, r_eq = (n * e, n * r) if "อนุกรม" in s else (e, r / n)
        assert _ans(q) == e_eq / (big_r + r_eq), s


def test_renewable_answers():
    from otk.sets.physics.m5.renewable_electricity import SOURCES
    how_of = dict(SOURCES)
    for seed in range(SEEDS):
        q = generate("phys.renewable_electricity_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("เปลี่ยนพลังงานอย่างไร"):
            assert _answer(q) == how_of[s.removesuffix("เปลี่ยนพลังงานอย่างไร")], s
        else:
            assert s == f"แหล่งผลิตไฟฟ้าใดเปลี่ยน{how_of[_answer(q)]}", s
        q = generate("phys.renewable_electricity_fluency", Random(seed))
        s = _stem(q)
        if "แผงเซลล์สุริยะ" in s:
            area, sun, eff = _q(rf"พื้นที่ {N} m² ได้รับแสงอาทิตย์ {N} W/m² มีประสิทธิภาพร้อยละ {N}", s)
            assert _ans(q) == area * sun * eff / 100, s
        else:
            flow, h, eff = _q(rf"เขื่อน {N} m³/s ตกจากความสูง {N} m ระบบมีประสิทธิภาพร้อยละ {N}", s)
            assert _ans(q) == flow * 1000 * 10 * h * eff / 100 / 1000, s
        q = generate("phys.renewable_electricity_application", Random(seed))
        s = _stem(q)
        if "หลอดไส้" in s:
            old, lamps, new, hours, days, price = _q(
                rf"หลอดไส้ {N} W จำนวน {N} หลอด เป็นหลอด LED {N} W .*วันละ {N} ชั่วโมง .*ใน {N} วัน \(ค่าไฟหน่วยละ {N} บาท\)", s)
            assert _ans(q) == (old - new) * lamps * hours * days / 1000 * price, s
        else:
            cost, units, price = _q(rf"ราคา {N} บาท ผลิตไฟฟ้าได้เดือนละ {N} หน่วย ถ้าค่าไฟหน่วยละ {N} บาท", s)
            assert _ans(q) == cost / (units * 12 * price), s


_PAGE = {"ไปทางขวา": (1, 0, 0), "ไปทางซ้าย": (-1, 0, 0), "ขึ้นด้านบนของหน้ากระดาษ": (0, 1, 0),
         "ลงด้านล่างของหน้ากระดาษ": (0, -1, 0), "พุ่งออกจากกระดาษ": (0, 0, 1), "พุ่งเข้าไปในกระดาษ": (0, 0, -1)}


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def test_magnetic_answers():
    sides = {"ด้านขวา": (1, 0, 0), "ด้านซ้าย": (-1, 0, 0), "ด้านบน": (0, 1, 0), "ด้านล่าง": (0, -1, 0)}
    cos = {37: Fraction(4, 5), 53: Fraction(3, 5), 60: Fraction(1, 2), 0: Fraction(1)}
    sin = {90: Fraction(1), 30: Fraction(1, 2), 37: Fraction(3, 5), 53: Fraction(4, 5)}
    for seed in range(SEEDS):
        q = generate("phys.magnetic_flux_foundation", Random(seed))
        s = _stem(q)
        if "ฟลักซ์แม่เหล็กผ่านพื้นผิว" in s:
            b, area = _q(rf"สม่ำเสมอ {N} T ตั้งฉากกับพื้นผิวพื้นที่ {N} m²", s)
            assert _ans(q) == b * area, s
        q = generate("phys.magnetic_flux_fluency", Random(seed))
        s = _stem(q)
        if "ทำมุม" in s:
            b, angle, area = _q(rf"สนามแม่เหล็ก {N} T ทำมุม {N}° กับเส้นแนวฉากของขดลวดพื้นที่ {N} m²", s)
            assert _ans(q) == b * area * cos[int(angle)], s
        elif "ขนานกับระนาบ" in s:
            assert _answer(q) == "0 Wb", s
        else:
            flux, area = _q(rf"ฟลักซ์แม่เหล็ก {N} Wb ผ่านขดลวดพื้นที่ {N} m²", s)
            assert _ans(q) == flux / area, s
        q = generate("phys.magnetic_flux_application", Random(seed))
        s = _stem(q)
        if "เส้นลวดตรง" in s:
            current = re.search(r"กระแสไฟฟ้าทิศ(\S+) สนาม", s).group(1)
            side = re.search(r"ที่จุด(\S+)ของเส้นลวด", s).group(1)
            assert _PAGE[_answer(q).removeprefix("ทิศ")] == _cross(_PAGE[current], sides[side]), s
        else:
            assert _answer(q) == ("ขั้วเหนือ" if "ทวนเข็มนาฬิกา" in s else "ขั้วใต้"), s
        q = generate("phys.magnetic_force_charge_foundation", Random(seed))
        s = _stem(q)
        if "ขนานกัน" in s:
            assert _answer(q) == ("ดึงดูดกัน" if "ทิศเดียวกัน" in s else "ผลักกัน"), s
        else:
            length, i, angle, b = _q(rf"ยาว {N} m มีกระแสไฟฟ้า {N} A วางทำมุม {N}° กับสนามแม่เหล็ก {N} T", s)
            assert _ans(q) == i * length * b * sin[int(angle)], s
        q = generate("phys.magnetic_force_charge_fluency", Random(seed))
        s = _stem(q)
        if "อนุภาคประจุ" in s:
            charge, v, b = _q(rf"ประจุ {N} μC เคลื่อนที่ด้วยความเร็ว {N} m/s ตั้งฉากกับสนามแม่เหล็ก {N} T", s)
            assert _ans(q) == charge * v * b / 1000, s
        else:
            mass, speed, b = _q(rf"มวล {N} × 10⁻²⁶ kg .*ความเร็ว {N} × 10⁵ m/s .*สนามแม่เหล็ก {N} T", s)
            # r = mv/(qB) in metres, reported in centimetres.
            radius = mass * Fraction(1, 10 ** 26) * speed * 10 ** 5 / (Fraction(16, 10) * Fraction(1, 10 ** 19) * b)
            assert _ans(q) == radius * 100, s
        q = generate("phys.magnetic_force_charge_application", Random(seed))
        s = _stem(q)
        motion = re.search(r"ทิศ(\S+) ในสนามแม่เหล็ก", s).group(1)
        field = re.search(r"สนามแม่เหล็กที่มีทิศ(\S+) ได้รับ", s).group(1)
        force = _cross(_PAGE[motion], _PAGE[field])
        if s.startswith("อิเล็กตรอน"):
            force = tuple(-x for x in force)
        assert _PAGE[_answer(q).removeprefix("ทิศ")] == force, s


# ── Slices 13-14: ฟิสิกส์เพิ่มเติม 3 ม.6/3-/8 and ฟิสิกส์เพิ่มเติม 4 ม.6/1 ────────────

def test_motor_and_meter_answers():
    for seed in range(SEEDS):
        q = generate("phys.motor_galvanometer_foundation", Random(seed))
        s = _stem(q)
        if "โมเมนต์ของแรงคู่ควบที่กระทำ" in s:
            n, area_cm, i, b = _q(rf"ขดลวดสี่เหลี่ยม {N} รอบ พื้นที่ {N} cm² มีกระแสไฟฟ้า {N} A .*สนามแม่เหล็ก {N} T", s)
            assert _ans(q) == n * i * area_cm / 10000 * b, s
        q = generate("phys.motor_galvanometer_fluency", Random(seed))
        s = _stem(q)
        rg, ig_ma = _q(rf"ความต้านทาน {N} Ω เข็มเบนเต็มสเกลที่กระแส {N} mA", s)
        ig = ig_ma / 1000
        if "ชันต์" in s:
            (full,) = _q(rf"วัดกระแสได้สูงสุด {N} A", s)
            assert _ans(q) * (full - ig) == ig * rg, s
        else:
            (volts,) = _q(rf"วัดความต่างศักย์ได้สูงสุด {N} V", s)
            assert ig * (_ans(q) + rg) == volts, s
        q = generate("phys.motor_galvanometer_application", Random(seed))
        s = _stem(q)
        if "ขณะเริ่มหมุน" in s:
            v, r = _q(rf"แหล่งจ่าย {N} V ขดลวดมีความต้านทาน {N} Ω", s)
            assert _ans(q) == v / r, s
        else:
            v, r, back = _q(rf"แหล่งจ่าย {N} V ขดลวดมีความต้านทาน {N} Ω ขณะหมุนมีอีเอ็มเอฟต้านกลับ {N} V", s)
            i = (v - back) / r
            assert _ans(q) == (i if "กระแสไฟฟ้าผ่าน" in s else back * i), s


def test_induction_answers():
    for seed in range(SEEDS):
        q = generate("phys.faraday_induction_fluency", Random(seed))
        s = _stem(q)
        if "สนามแม่เหล็กที่เปลี่ยนไป" in s:
            n, area, db, dt = _q(rf"ขดลวด {N} รอบ พื้นที่ {N} m² .*เปลี่ยนไป {N} T ในเวลา {N} s", s)
            assert _ans(q) == n * db * area / dt, s
        else:
            n, flux, dt = _q(rf"ขดลวด {N} รอบลดลงจาก {N} Wb เป็นศูนย์ในเวลา {N} s", s)
            assert flux > 0 and _ans(q) == n * flux / dt, s
        q = generate("phys.faraday_induction_application", Random(seed))
        s = _stem(q)
        length, v, b, r = _q(rf"ยาว {N} m เลื่อนบนรางด้วยความเร็ว {N} m/s ตั้งฉากกับสนามแม่เหล็ก {N} T วงจรมีความต้านทานรวม {N} Ω", s)
        emf = b * length * v
        expected = emf if "อีเอ็มเอฟ" in s.split("Ω")[1] else emf / r if "กระแส" in s.split("Ω")[1] else emf / r * length * b
        assert _ans(q) == expected, s


def test_rms_answers():
    for seed in range(SEEDS):
        q = generate("phys.ac_rms_foundation", Random(seed))
        s = _stem(q)
        if "สูงสุดเท่าใด" in s:
            (rms,) = _q(rf"อาร์เอ็มเอส {N} V", s)
            assert _answer(q) == f"{rms}√2 V", s
        elif "√2" in s:
            (peak,) = _q(rf"สูงสุด {N}√2", s)
            assert _ans(q) == peak, s
        q = generate("phys.ac_rms_fluency", Random(seed))
        s = _stem(q)
        r, v = _q(rf"ตัวต้านทาน {N} Ω กับไฟฟ้ากระแสสลับ {N} V", s)
        assert _ans(q) == (v / r if "กระแส" in s.split("(อาร์เอ็มเอส)")[1] else v * v / r), s
        q = generate("phys.ac_rms_application", Random(seed))
        s = _stem(q)
        (power,) = _q(rf" {N} W ใช้กับไฟบ้าน", s)
        if "กระแสอาร์เอ็มเอส" in s:
            assert _ans(q) == power / 220, s
        else:
            from otk.kit.answer_choices import show
            assert _answer(q) == f"{show(power / 220)}√2 A", s


def test_transformer_answers():
    for seed in range(SEEDS):
        q = generate("phys.transformer_threephase_foundation", Random(seed))
        s = _stem(q)
        if "เป็นหม้อแปลงชนิดใด" in s:
            np_, ns = _q(rf"ขดปฐมภูมิ {N} รอบ และขดทุติยภูมิ {N} รอบ", s)
            assert _answer(q).startswith("หม้อแปลงขึ้น" if ns > np_ else "หม้อแปลงลง"), s
        q = generate("phys.transformer_threephase_fluency", Random(seed))
        s = _stem(q)
        if "ความต่างศักย์ขาออก" in s:
            np_, ns, vp = _q(rf"ขดปฐมภูมิ {N} รอบ ขดทุติยภูมิ {N} รอบ ป้อนไฟกระแสสลับ {N} V", s)
            assert _ans(q) == vp * ns / np_, s
        else:
            vp, vs, np_ = _q(rf"แปลงไฟ {N} V เป็น {N} V ขดปฐมภูมิมี {N} รอบ", s)
            assert _ans(q) == np_ * vs / vp, s
        q = generate("phys.transformer_threephase_application", Random(seed))
        s = _stem(q)
        if "กระแสด้านปฐมภูมิ" in s:
            vp, vs, is_ = _q(rf"แปลงไฟ {N} V เป็น {N} V จ่ายกระแสด้านทุติยภูมิ {N} A", s)
            assert _ans(q) * vp == vs * is_, s
        elif "ประสิทธิภาพ" in s:
            p_in, eff = _q(rf"รับกำลังไฟฟ้า {N} W มีประสิทธิภาพร้อยละ {N}", s)
            assert _ans(q) == p_in * eff / 100, s
        else:
            loss, k = _q(rf"สูญเสียพลังงานในสาย {N} W .*เป็น {N} เท่า", s)
            assert _ans(q) == loss / (k * k), s


def test_em_polarisation_and_signal_answers():
    from otk.sets.physics.m6.polarisation_em import BANDS
    how_of = dict(BANDS)
    cos2 = {60: Fraction(1, 4), 37: Fraction(16, 25), 53: Fraction(9, 25), 0: Fraction(1)}
    scale = {"kHz": 10 ** 3, "MHz": 10 ** 6, "GHz": 10 ** 9}
    for seed in range(SEEDS):
        q = generate("phys.polarisation_em_foundation", Random(seed))
        s = _stem(q)
        if "ความยาวคลื่นเท่าใดในอากาศ" in s:
            f, unit = re.search(r"ความถี่ (\d+) (\S+Hz)", s).groups()
            assert _ans(q) == Fraction(3 * 10 ** 8, int(f) * scale[unit]), s
        q = generate("phys.polarisation_em_fluency", Random(seed))
        s = _stem(q)
        (i0,) = _q(rf"ความเข้ม {N} W/m²", s)
        if "แผ่นเดียว" in s:
            assert _ans(q) == i0 / 2, s
        elif "90°" in s:
            assert _answer(q) == "0 W/m²", s
        else:
            (angle,) = _q(rf"แกนทำมุม {N}°", s)
            assert _ans(q) == i0 / 2 * cos2[int(angle)], s
        q = generate("phys.polarisation_em_application", Random(seed))
        s = _stem(q)
        if s.endswith("ใช้คลื่นแม่เหล็กไฟฟ้าช่วงใดและทำงานอย่างไร"):
            assert _answer(q) == how_of[s.removesuffix("ใช้คลื่นแม่เหล็กไฟฟ้าช่วงใดและทำงานอย่างไร")], s
        else:
            assert s == f"อุปกรณ์ใดใช้{how_of[_answer(q)]}", s
        q = generate("phys.signal_communication_foundation", Random(seed))
        s = _stem(q)
        if "ความยาวคลื่นเท่าใด" in s:
            (khz,) = _q(rf"ความถี่ {N} kHz", s)
            assert _ans(q) == Fraction(3 * 10 ** 5) / khz, s
        elif "น่าจะเป็นสถานีระบบใด" in s:
            assert _answer(q).startswith("สถานี AM" if "kHz" in s else "สถานี FM"), s
        q = generate("phys.signal_communication_fluency", Random(seed))
        s = _stem(q)
        if "แทนระดับของสัญญาณได้กี่ระดับ" in s:
            (n,) = _q(rf"ข้อมูล {N} บิต", s)
            assert _ans(q) == 2 ** int(n), s
        else:
            (levels,) = _q(rf"แบ่งเป็น {N} ระดับ", s)
            bits = int(_ans(q))
            assert 2 ** bits >= levels > 2 ** (bits - 1), s
        q = generate("phys.signal_communication_application", Random(seed))
        s = _stem(q)
        if "ส่งไฟล์" in s:
            size, rate = _q(rf"ขนาด {N} เมกะไบต์ .*อัตรา {N} เมกะบิต", s)
            assert _ans(q) == size * 8 / rate, s
        else:
            khz, bits, seconds = _q(rf"ชักตัวอย่าง {N} kHz ค่าละ {N} บิต เป็นเวลา {N} s", s)
            assert _ans(q) == khz * 1000 * bits * seconds / 8 / 1000, s


def test_heat_answers():
    for seed in range(SEEDS):
        q = generate("phys.heat_calorimetry_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("ต้มน้ำ"):
            m, t1, t2 = _q(rf"มวล {N} kg จาก {N} °C เป็น {N} °C", s)
            assert _ans(q) == m * 4200 * (t2 - t1), s
        else:
            m, heat, c = _q(rf"มวล {N} kg ได้รับความร้อน {N} J .*= {N} J/kg·K", s)
            assert _ans(q) * m * c == heat, s
        q = generate("phys.heat_calorimetry_fluency", Random(seed))
        s = _stem(q)
        (m,) = _q(rf"มวล {N} kg", s)
        if "กลายเป็นน้ำที่" in s:
            (t,) = _q(rf"กลายเป็นน้ำที่ {N} °C", s)
            assert _ans(q) == m * 336000 + m * 4200 * t, s
        else:
            assert _ans(q) == m * (2260000 if "ไอน้ำ" in s else 336000), s
        q = generate("phys.heat_calorimetry_application", Random(seed))
        s = _stem(q)
        if s.startswith("ผสมน้ำร้อน"):
            m1, t1, m2, t2 = _q(rf"น้ำร้อน {N} kg อุณหภูมิ {N} °C กับน้ำเย็น {N} kg อุณหภูมิ {N} °C", s)
            final = _ans(q)
            assert m1 * (t1 - final) == m2 * (final - t2), s
        else:
            mm, tm, mw, tw, c = _q(rf"มวล {N} kg อุณหภูมิ {N} °C ใส่ลงในน้ำ {N} kg อุณหภูมิ {N} °C .*= {N} J/kg·K, c ของน้ำ", s)
            final = _ans(q)
            assert mm * c * (tm - final) == mw * 4200 * (final - tw), s


# ── Slices 15-16: ฟิสิกส์เพิ่มเติม 4 ม.6/2, /5-/10 ──────────────────────────────────

def test_elasticity_answers():
    for seed in range(SEEDS):
        q = generate("phys.elasticity_modulus_foundation", Random(seed))
        s = _stem(q)
        if "ความเค้นตามยาวในลวด" in s:
            force, area = _q(rf"น้ำหนัก {N} N ที่ปลายลวดพื้นที่หน้าตัด {N} mm²", s)
            assert _ans(q) == force / area, s
        q = generate("phys.elasticity_modulus_fluency", Random(seed))
        s = _stem(q)
        if "ความเครียดตามยาวเท่าใด" in s:
            length, stretch = _q(rf"ลวดยาว {N} m ยืดออก {N} mm", s)
            assert _ans(q) == stretch / length, s
        else:
            stress, strain = _q(rf"ความเค้น {N} MPa และความเครียด {N} × 10⁻³", s)
            assert _ans(q) == stress / strain, s
        q = generate("phys.elasticity_modulus_application", Random(seed))
        s = _stem(q)
        if "ยืดออกกี่มิลลิเมตร" in s:
            length, area, force, y = _q(rf"ยาว {N} m พื้นที่หน้าตัด {N} mm² รับแรงดึง {N} N .*= {N} GPa", s)
            assert _ans(q) == force * length / (area * y), s
        else:
            length, area, force, stretch = _q(rf"ยาว {N} m พื้นที่หน้าตัด {N} mm² ด้วยแรง {N} N ลวดยืดออก {N} mm", s)
            assert _ans(q) == (force / area) / (stretch / length), s


def test_surface_and_flow_answers():
    from otk.sets._support.science_wave_f4 import DROPS
    speed_of = {h: v for h, v in DROPS}
    for seed in range(SEEDS):
        q = generate("phys.surface_tension_foundation", Random(seed))
        s = _stem(q)
        if "ด้านเดียว" in s:
            gamma, length = _q(rf"ความตึงผิว {N} N/m ผิวของเหลวยาว {N} cm", s)
            assert _ans(q) == gamma * length / 100 * 1000, s
        q = generate("phys.surface_tension_fluency", Random(seed))
        s = _stem(q)
        if "ความตึงผิวของน้ำสบู่กี่" in s:
            length, force = _q(rf"โครงลวดยาว {N} cm .*ดึงได้ {N} mN", s)
            assert _ans(q) == force / (2 * length / 100), s
        else:
            gamma, length = _q(rf"ความตึงผิว {N} mN/m โครงลวดยาว {N} cm", s)
            assert _ans(q) == 2 * gamma * length / 100, s
        q = generate("phys.surface_tension_application", Random(seed))
        s = _stem(q)
        weight, edge, gamma = _q(rf"หนัก {N} mN .*ยาวรวม {N} cm .*ความตึงผิวของน้ำ {N} N/m", s)
        assert _ans(q) == weight + 2 * gamma * edge / 100 * 1000, s
        q = generate("phys.bernoulli_flow_foundation", Random(seed))
        s = _stem(q)
        if "พื้นที่หน้าตัด" in s:
            a1, v1, a2 = _q(rf"พื้นที่หน้าตัด {N} cm² ด้วยอัตราเร็ว {N} m/s .*พื้นที่หน้าตัด {N} cm²", s)
            assert _ans(q) * a2 == a1 * v1, s
        q = generate("phys.bernoulli_flow_fluency", Random(seed))
        s = _stem(q)
        if "เส้นผ่านศูนย์กลาง" in s:
            d1, d2, v1 = _q(rf"เส้นผ่านศูนย์กลาง {N} cm ต่อกับท่อเส้นผ่านศูนย์กลาง {N} cm .*อัตราเร็ว {N} m/s", s)
            assert _ans(q) == v1 * (d1 / d2) ** 2, s
        else:
            area, v = _q(rf"พื้นที่หน้าตัด {N} cm² ด้วยอัตราเร็ว {N} m/s", s)
            assert _ans(q) == area / 10000 * v * 1000, s
        q = generate("phys.bernoulli_flow_application", Random(seed))
        s = _stem(q)
        if "ระดับเดียวกัน" in s:
            v1, v2 = _q(rf"อัตราเร็ว {N} m/s ส่วนแคบไหลด้วยอัตราเร็ว {N} m/s", s)
            assert _ans(q) == 1000 * (v2 * v2 - v1 * v1) / 2, s
        else:
            (h,) = _q(rf"ต่ำกว่าผิวน้ำ {N} m", s)
            assert _ans(q) ** 2 == 2 * 10 * h and _ans(q) == speed_of[h], s


def test_gas_answers():
    for seed in range(SEEDS):
        q = generate("phys.ideal_gas_law_foundation", Random(seed))
        s = _stem(q)
        if "เคลวิน" in s:
            (c,) = _q(rf"อุณหภูมิ {N} °C", s)
            assert _ans(q) == c + 273, s
        else:
            p1, v1, v2 = _q(rf"ความดัน {N} kPa ปริมาตร {N} L .*ปริมาตรเป็น {N} L", s)
            assert _ans(q) * v2 == p1 * v1, s
        q = generate("phys.ideal_gas_law_fluency", Random(seed))
        s = _stem(q)
        if "ปริมาตรใหม่" in s:
            v1, t1, t2 = _q(rf"ปริมาตร {N} L ที่ {N} °C เปลี่ยนอุณหภูมิเป็น {N} °C", s)
            assert _ans(q) == v1 * (t2 + 273) / (t1 + 273), s
        else:
            p1, t1, t2 = _q(rf"ความดัน {N} kPa ที่ {N} °C .*เปลี่ยนเป็น {N} °C", s)
            assert _ans(q) == p1 * (t2 + 273) / (t1 + 273), s
        q = generate("phys.ideal_gas_law_application", Random(seed))
        s = _stem(q)
        if "โมล" in s:
            n, t, v = _q(rf"แก๊สอุดมคติ {N} โมล อุณหภูมิ {N} K บรรจุในภาชนะปริมาตร {N} m³", s)
            assert _ans(q) == n * Fraction(831, 100) * t / v, s
        else:
            p1, v1, t1, p2, t2 = _q(rf"ความดัน {N} kPa ปริมาตร {N} L อุณหภูมิ {N} K เปลี่ยนเป็นความดัน {N} kPa อุณหภูมิ {N} K", s)
            assert p1 * v1 / t1 == p2 * _ans(q) / t2, s
        q = generate("phys.kinetic_gas_fluency", Random(seed))
        s = _stem(q)
        if "พลังงานจลน์เฉลี่ย" in s:
            t1, t2 = _q(rf"แก๊สที่ {N} K เพิ่มอุณหภูมิเป็น {N} K", s)
            assert _ans(q) == t2 / t1, s
        elif "ถ้าอุณหภูมิเป็น" in s:
            t1, v1, t2 = _q(rf"แก๊สที่ {N} K มีอัตราเร็วอาร์เอ็มเอส {N} m/s ถ้าอุณหภูมิเป็น {N} K", s)
            assert (_ans(q) / v1) ** 2 == t2 / t1, s
        else:
            m_a, m_b = _q(rf"มวลโมเลกุล {N}\).*มวลโมเลกุล {N}\)", s)
            assert _ans(q) ** 2 == m_b / m_a, s
        q = generate("phys.kinetic_gas_application", Random(seed))
        s = _stem(q)
        if "ความดันกี่กิโลพาสคัล" in s:
            rho, v = _q(rf"ความหนาแน่น {N} kg/m³ .*อาร์เอ็มเอส {N} m/s", s)
            assert _ans(q) == rho * v * v / 3 / 1000, s
        elif "อัตราเร็วอาร์เอ็มเอสของโมเลกุลเท่าใด" in s:
            p, rho = _q(rf"ความดัน {N} kPa และความหนาแน่น {N} kg/m³", s)
            assert _ans(q) ** 2 == 3 * p * 1000 / rho, s
        else:
            p, v = _q(rf"ความดัน {N} kPa มีอัตราเร็วอาร์เอ็มเอส {N} m/s", s)
            assert _ans(q) == 3 * p * 1000 / (v * v), s
        q = generate("phys.kinetic_gas_foundation", Random(seed))
        s = _stem(q)
        if "ตอบในหน่วย" in s:
            t1, e1, t2 = _q(rf"ที่ {N} K มีพลังงานจลน์เฉลี่ย {N} × 10⁻²¹ J ที่อุณหภูมิ {N} K", s)
            assert _ans(q) == e1 * t2 / t1, s


def test_thermo_answers():
    for seed in range(SEEDS):
        q = generate("phys.thermo_first_law_foundation", Random(seed))
        s = _stem(q)
        if "ทำงานกี่จูล" in s:
            p, v1, v2 = _q(rf"ความดันคงตัว {N} kPa จากปริมาตร {N} L เป็น {N} L", s)
            assert _ans(q) == p * (v2 - v1), s
        q = generate("phys.thermo_first_law_fluency", Random(seed))
        s = _stem(q)
        heat, work = _q(rf"ความร้อน {N} J .* {N} J พลังงานภายใน", s)
        heat = heat if "ได้รับความร้อน" in s else -heat
        work = work if "ทำงานต่อสิ่งแวดล้อม" in s else -work
        assert _ans(q) == heat - work, s
        q = generate("phys.thermo_first_law_application", Random(seed))
        s = _stem(q)
        if s.startswith("ให้ความร้อน"):
            heat, dv, p = _q(rf"ให้ความร้อน {N} J .*เพิ่มขึ้น {N} L ที่ความดันคงตัว {N} kPa", s)
            assert _ans(q) == heat - p * dv, s
        else:
            dv, p, du = _q(rf"ขยายตัว {N} L ที่ความดันคงตัว {N} kPa และพลังงานภายในเพิ่มขึ้น {N} J", s)
            assert _ans(q) == du + p * dv, s


def test_bohr_answers():
    levels = {1: Fraction(-136, 10), 2: Fraction(-34, 10), 3: Fraction(-151, 100), 4: Fraction(-85, 100), 5: Fraction(-54, 100)}
    series = {1: "อนุกรมไลแมน", 2: "อนุกรมบัลเมอร์", 3: "อนุกรมพาสเชน"}
    band = {1: "รังสีอัลตราไวโอเลต", 2: "แสงที่มองเห็นได้", 3: "รังสีอินฟราเรด"}
    for seed in range(SEEDS):
        q = generate("phys.bohr_spectrum_fluency", Random(seed))
        s = _stem(q)
        if "ปล่อยโฟตอนพลังงาน" in s:
            high, low = _q(rf"ระดับ n = {N} ลงสู่ n = {N}", s)
            assert _ans(q) == levels[int(high)] - levels[int(low)], s
        elif "ดูดกลืนโฟตอน" in s:
            low, energy = _q(rf"ระดับ n = {N} ดูดกลืนโฟตอนพลังงาน {N} eV", s)
            high = int(_answer(q).removeprefix("n = "))
            assert levels[high] - levels[int(low)] == energy, s
        else:
            (n,) = _q(rf"ที่ระดับ n = {N}", s)
            assert _ans(q) == -levels[int(n)], s
        q = generate("phys.bohr_spectrum_application", Random(seed))
        s = _stem(q)
        if "กี่เส้น" in s:
            (top,) = _q(rf"ระดับ n = {N}", s)
            assert _ans(q) == top * (top - 1) / 2, s
        else:
            high, low = _q(rf"จาก n = {N} ลงสู่ n = {N}", s)
            expected = series[int(low)] if "อนุกรมใด" in s else band[int(low)]
            assert _answer(q) == expected, s


# ── Slices 17-18: ฟิสิกส์เพิ่มเติม 4 ม.6/11-/18 ─────────────────────────────────────

def test_photoelectric_and_de_broglie_answers():
    from otk.sets.physics.m6.de_broglie import BALLS
    from otk.sets.physics.m6.photoelectric import METALS
    work_of = dict(METALS)
    for seed in range(SEEDS):
        q = generate("phys.photoelectric_foundation", Random(seed))
        s = _stem(q)
        if "โฟตอนพลังงาน" in s:
            energy, work = _q(rf"โฟตอนพลังงาน {N} eV .*ฟังก์ชันงาน {N} eV", s)
            assert _ans(q) == energy - work, s
        q = generate("phys.photoelectric_fluency", Random(seed))
        s = _stem(q)
        (wl,) = _q(rf"ความยาวคลื่น {N} nm", s)
        if "ความต่างศักย์หยุดยั้ง" in s:
            (work,) = _q(rf"ฟังก์ชันงาน {N} eV", s)
            assert _ans(q) == 1240 / wl - work, s
        else:
            assert _ans(q) == 1240 / wl, s
        q = generate("phys.photoelectric_application", Random(seed))
        s = _stem(q)
        if "ไม่เกินกี่นาโนเมตร" in s:
            (work,) = _q(rf"ฟังก์ชันงาน {N} eV", s)
            assert _ans(q) == 1240 / work, s
        else:
            (wl,) = _q(rf"ความยาวคลื่น {N} nm", s)
            listed = re.findall(r"(\S+) \(([\d.]+) eV\)", s)
            emits = [name for name, w in listed if Fraction(w) < 1240 / wl]
            expected = ("ทุกโลหะ" if len(emits) == len(listed) else "ไม่มีโลหะใดเลย" if not emits else " ".join(emits))
            assert _answer(q) == expected, s
            assert all(work_of[name] == Fraction(w) for name, w in listed)
        q = generate("phys.de_broglie_foundation", Random(seed))
        s = _stem(q)
        if "โมเมนตัม" in s and "×" in s:
            p, sign = re.search(r"โมเมนตัม ([\d.]+) × 10(⁻²⁴|⁻²⁵)", s).groups()
            lam = Fraction(66, 10) / Fraction(p) * (10 if sign == "⁻²⁵" else 1)
            assert _ans(q) == lam, s
        q = generate("phys.de_broglie_fluency", Random(seed))
        s = _stem(q)
        m, v = _q(rf"มวล {N} g เคลื่อนที่ด้วยความเร็ว {N} m/s", s)
        mant, exponent = next((mm, e) for bm, bv, mm, e in BALLS if bm == m and bv == v)
        assert mant * Fraction(10) ** (exponent + 34) == Fraction(66, 10) / (m / 1000 * v), s
        q = generate("phys.de_broglie_application", Random(seed))
        s = _stem(q)
        if "อิเล็กตรอนมีความยาวคลื่น" in s:
            (lam,) = _q(rf"เดอบรอยล์ {N} nm", s)
            found = re.search(r"เพิ่มเป็น (\d+) เท่า", s)
            factor = Fraction(found.group(1)) if found else Fraction(1, 2)
            assert _ans(q) == lam / factor, s
        else:
            (ratio,) = _q(rf"ประมาณ {N} เท่า", s)
            assert _ans(q) == ratio, s


def test_radioactivity_answers():
    order = {"แอลฟา": 1, "บีตา": 2, "แกมมา": 3}
    for seed in range(SEEDS):
        q = generate("phys.alpha_beta_gamma_foundation", Random(seed))
        s = _stem(q)
        if "มากั้น" in s:
            emitted = re.search(r"ปล่อยรังสี(.+?) นำ", s).group(1).split()
            stops = 1 if "กระดาษ" in s else 2 if "อะลูมิเนียม" in s else 3
            passed = [r for r in emitted if order[r] > stops]
            assert _answer(q) == ("ไม่มีรังสีผ่าน" if not passed else "รังสี" + " และ".join(passed)), s
        q = generate("phys.alpha_beta_gamma_fluency", Random(seed))
        s = _stem(q)
        a, z = _q(rf"เลขมวล {N} และเลขอะตอม {N}", s)
        kind = re.search(r"สลายให้รังสี(\S+) ", s).group(1)
        na, nz = {"แอลฟา": (a - 4, z - 2), "บีตา": (a, z + 1), "แกมมา": (a, z)}[kind]
        assert _answer(q) == f"เลขมวล {na} เลขอะตอม {nz}", s
        q = generate("phys.alpha_beta_gamma_application", Random(seed))
        s = _stem(q)
        a, z, fa, fz = _q(rf"เลขมวล {N} เลขอะตอม {N} สลายต่อเนื่องจนได้นิวเคลียสเลขมวล {N} เลขอะตอม {N}", s)
        alphas = (a - fa) / 4
        betas = 2 * alphas - (z - fz)
        assert _ans(q) == (alphas if "รังสีแอลฟากี่ครั้ง" in s else betas), s
        q = generate("phys.half_life_decay_foundation", Random(seed))
        s = _stem(q)
        half, start, elapsed = _q(rf"ครึ่งชีวิต {N} \S+ มีอยู่ {N} mg เมื่อเวลาผ่านไป {N}", s)
        assert _ans(q) == start / 2 ** int(elapsed / half), s
        q = generate("phys.half_life_decay_fluency", Random(seed))
        s = _stem(q)
        if "มีครึ่งชีวิตเท่าใด" in s:
            denom, elapsed = _q(rf"เหลือ 1/{N} ของปริมาณเดิมเมื่อเวลาผ่านไป {N}", s)
            n = int(denom).bit_length() - 1
            assert _ans(q) == elapsed / n, s
        else:
            half, denom = _q(rf"ครึ่งชีวิต {N} \S+ .*เหลือ 1/{N}", s)
            assert _ans(q) == half * (int(denom).bit_length() - 1), s
        q = generate("phys.half_life_decay_application", Random(seed))
        s = _stem(q)
        if "คาร์บอน-14 เหลือ" in s:
            (pct,) = _q(rf"เหลือ {N}%", s)
            n = int(100 / pct).bit_length() - 1
            assert _ans(q) == 5730 * n, s
        else:
            half, a0, elapsed = _q(rf"ครึ่งชีวิต {N} \S+\) มีกัมมันตภาพ {N} MBq เมื่อเก็บไว้ {N}", s)
            assert _ans(q) == a0 / 2 ** int(elapsed / half), s


def test_nuclear_answers():
    for seed in range(SEEDS):
        q = generate("phys.binding_energy_foundation", Random(seed))
        s = _stem(q)
        if "มวลพร่อง" in s and " u " in s:
            (dm,) = _q(rf"มวลพร่อง {N} u", s)
            assert _ans(q) == dm * 931, s
        q = generate("phys.binding_energy_fluency", Random(seed))
        s = _stem(q)
        if "ต่อนิวคลีออนเท่าใด" in s:
            (total,) = _q(rf"พลังงานยึดเหนี่ยว {N} MeV", s)
            (a,) = _q(rf"(?:เลขมวล |-){N}", s)
            assert _ans(q) * a == total, s
        else:
            a, per = _q(rf"เลขมวล {N}\) มีพลังงานยึดเหนี่ยวต่อนิวคลีออน {N} MeV", s)
            assert _ans(q) == a * per, s
        q = generate("phys.binding_energy_application", Random(seed))
        s = _stem(q)
        items = [(ell, Fraction(a), Fraction(e.replace(",", "")))
                 for ell, a, e in re.findall(r"(\S) มีเลขมวล (\d+) และพลังงานยึดเหนี่ยว ([\d,.]+) MeV", s)]
        assert len(items) == 3, s
        best = max(items, key=lambda t: t[2] / t[1])[0]
        assert _answer(q) == f"นิวเคลียส {best}", s
        q = generate("phys.fission_fusion_fluency", Random(seed))
        s = _stem(q)
        if "นิวเคลียส Y" in s:
            a0, z0, a1, z1, n = _q(rf"\(A = {N}, Z = {N}\) เกิดฟิชชันได้นิวเคลียส \(A = {N}, Z = {N}\) นิวตรอน {N} ตัว", s)
            assert _ans(q) == (a0 + 1 - a1 - n if "Y มีเลขมวล" in s else z0 - z1), s
        elif "ปล่อยนิวตรอนออกมากี่ตัว" in s:
            z0, a1, z1, a2, z2 = _q(rf"\(Z = {N}\) ได้\S+-{N} \(Z = {N}\) และ\S+-{N} \(Z = {N}\)", s)
            a0 = 239 if "พลูโทเนียม" in s else 235
            assert _ans(q) == a0 + 1 - a1 - a2 and z0 == z1 + z2, s
        elif "มีเลขอะตอมเท่าใด" in s and "ฟิวชัน" not in s:
            z0, z1 = _q(rf"\(Z = {N}\) ได้\S+ \(Z = {N}\)", s)
            assert _ans(q) == z0 - z1, s
        elif "ฟิวชัน" in s:
            a_a, z_a, a_b, z_b = _q(rf"\(A = {N}, Z = {N}\) รวมกับ \(A = {N}, Z = {N}\)", s)
            other = {"นิวตรอน": (1, 0), "โปรตอน": (1, 1), "รังสีแกมมา": (0, 0)}[re.search(r"ได้(\S+?)และนิวเคลียส X", s).group(1)]
            expected = (a_a + a_b - other[0]) if "มีเลขมวล" in s else (z_a + z_b - other[1])
            assert _ans(q) == expected, s
        q = generate("phys.fission_fusion_application", Random(seed))
        s = _stem(q)
        if "มวลรวมก่อน" in s:
            before, after = _q(rf"ก่อนเกิดปฏิกิริยา {N} u และมวลรวมหลังเกิด {N} u", s)
            assert _ans(q) == (before - after) * 931, s
        else:
            (dm,) = _q(rf"มวลหายไป {N} u", s)
            assert _ans(q) == dm * 931, s


def test_radiation_and_particle_answers():
    from otk.sets.physics.m6.particle_standard_model import APPLICATIONS, PARTICLES
    from otk.sets.physics.m6.radiation_safety import USES
    use_of, how_of = dict(USES), dict(APPLICATIONS)
    charges = {"u": Fraction(2, 3), "d": Fraction(-1, 3), "s": Fraction(-1, 3), "c": Fraction(2, 3)}

    def charge_label(x):
        if x == 0:
            return "0"
        sign = "+" if x > 0 else "−"
        return f"{sign}{abs(x)}" if x.denominator == 1 else f"{sign}{abs(x.numerator)}/{x.denominator}"

    for seed in range(SEEDS):
        q = generate("phys.radiation_safety_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("ใช้ประโยชน์ด้านใด"):
            assert _answer(q) == use_of[s.removesuffix("ใช้ประโยชน์ด้านใด")], s
        else:
            assert s == f"ไอโซโทปกัมมันตรังสีใดใช้{use_of[_answer(q)]}", s
        q = generate("phys.radiation_safety_fluency", Random(seed))
        s = _stem(q)
        if "นาที" in s:
            rate, minutes = _q(rf"อัตราปริมาณรังสี {N} ไมโครซีเวิร์ตต่อชั่วโมง อยู่ในบริเวณนั้น {N} นาที", s)
            assert _ans(q) == rate * minutes / 60, s
        else:
            r1, rate, r2 = _q(rf"ขนาดเล็ก {N} m วัดอัตราปริมาณรังสีได้ {N} μSv/h ถ้าถอยไปอยู่ห่าง {N} m", s)
            assert _ans(q) == rate * (r1 / r2) ** 2, s
        q = generate("phys.radiation_safety_application", Random(seed))
        s = _stem(q)
        if "ลดความเข้มรังสีแกมมาลงครึ่งหนึ่ง" in s:
            hvl, thick, rate = _q(rf"หนา {N} cm ลดความเข้ม.*หนา {N} cm กั้นรังสีที่มีอัตรา {N} μSv/h", s)
            assert _ans(q) == rate / 2 ** int(thick / hvl), s
        q = generate("phys.particle_standard_model_foundation", Random(seed))
        s = _stem(q)
        group_of = {n: g for n, g, _ in PARTICLES}
        charge_of = {n: c for n, _, c in PARTICLES}
        if s.endswith("จัดเป็นอนุภาคกลุ่มใด"):
            assert _answer(q) == group_of[s.removesuffix("จัดเป็นอนุภาคกลุ่มใด")], s
        elif s.endswith("มีประจุไฟฟ้าเท่าใด (หน่วยประจุมูลฐาน)") and s.split("มีประจุ")[0] in charge_of:
            assert _answer(q) == charge_label(charge_of[s.split("มีประจุ")[0]]), s
        q = generate("phys.particle_standard_model_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("แบริออน"):
            quarks = re.findall(r"\((\w)\)", s)
            assert len(quarks) == 3, s
            assert _answer(q) == charge_label(sum(charges[x] for x in quarks)), s
        else:
            q1 = re.search(r"\((\w)\) กับปฏิควาร์ก", s).group(1)
            anti = re.search(r"\(แอนติ-(\w)\)", s).group(1)
            assert _answer(q) == charge_label(charges[q1] - charges[anti]), s
        q = generate("phys.particle_standard_model_application", Random(seed))
        s = _stem(q)
        if s.endswith("เกี่ยวข้องกับการค้นคว้าด้านฟิสิกส์อนุภาคอย่างไร"):
            assert _answer(q) == how_of[s.removesuffix("เกี่ยวข้องกับการค้นคว้าด้านฟิสิกส์อนุภาคอย่างไร")], s
        else:
            assert s == f"ข้อใด{how_of[_answer(q)]}", s


# ── Slices 19-20: เคมีเพิ่มเติม 1 ม.4/1, /3, /5-/9 ──────────────────────────────────

def test_atomic_models_pair_each_scientist_with_their_model():
    from otk.sets.chemistry.m4.atomic_model_history import EVIDENCE, MODELS, ORDER
    model_of = dict(MODELS)
    for seed in range(SEEDS):
        q = generate("chem.atomic_model_history_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("อธิบายอะตอมไว้อย่างไร"):
            who = s.removesuffix("อธิบายอะตอมไว้อย่างไร").removeprefix("แบบจำลองของ")
            assert _answer(q) == model_of[who], s
        else:
            who = _answer(q).removeprefix("แบบจำลองของ")
            assert s == f"แบบจำลองอะตอมใดกล่าวว่า{model_of[who]}", s
        q = generate("chem.atomic_model_history_fluency", Random(seed))
        s = _stem(q)
        observed = s.split("\"")[1]
        meaning, who = next((m, w) for o, m, w in EVIDENCE if o == observed)
        assert _answer(q) == (meaning if "ข้อสรุป" in s else who), s
        q = generate("chem.atomic_model_history_application", Random(seed))
        s = _stem(q)
        if "เรียงลำดับ" in s:
            names = _answer(q).split(" → ")
            assert names == sorted(names, key=ORDER.index), s


def test_electron_configurations_count_every_electron():
    from otk.sets.chemistry.m4.electron_config import main_levels, subshell_config
    assert subshell_config(24)[-2:] == [("4s", 1), ("3d", 5)]
    assert subshell_config(29)[-2:] == [("4s", 1), ("3d", 10)]
    digits = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
    for seed in range(SEEDS):
        q = generate("chem.electron_config_foundation", Random(seed))
        s = _stem(q)
        (z,) = _q(rf"เลขอะตอม {N}", s)
        levels = [int(x) for x in _answer(q).split(", ")]
        assert sum(levels) == z and levels == main_levels(int(z)), s
        q = generate("chem.electron_config_fluency", Random(seed))
        s = _stem(q)
        (z,) = _q(rf"เลขอะตอม {N}", s)
        total = sum(int(part[2:].translate(digits)) for part in _answer(q).split())
        assert total == z, s
        q = generate("chem.electron_config_application", Random(seed))
        s = _stem(q)
        parts = [(p[:2], int(p[2:].translate(digits))) for p in re.search(r"เป็น (.+?) (?:มี|อยู่)", s).group(1).split()]
        outer = max(int(n[0]) for n, _ in parts)
        valence = sum(c for n, c in parts if int(n[0]) == outer)
        if "เวเลนซ์" in s:
            assert _ans(q) == valence, s
        elif "คาบ" in s:
            assert _ans(q) == outer, s
        else:
            assert _ans(q) == (valence if valence <= 2 else valence + 10), s


def test_periodic_trends_follow_position():
    from otk.sets._support.science_wave_f19 import REPRESENTATIVE
    from otk.sets.chemistry.m4.periodic_trend import TRENDS
    by_symbol = {e[1]: e for e in REPRESENTATIVE}
    trend = {name: (down, right) for name, down, right in TRENDS}

    def value(element, prop):
        down, right = trend[prop]
        return (element[3] if down else -element[3], element[4] if right else -element[4])

    for seed in range(SEEDS):
        q = generate("chem.periodic_trend_fluency", Random(seed))
        s = _stem(q)
        a, b = (by_symbol[x] for x in re.findall(r"\((\w+)\) \(หมู่", s))
        prop = next(p for p in trend if f"มี{p}มากกว่า" in s)
        down, right = trend[prop]
        if a[4] == b[4]:
            bigger = a if (a[3] > b[3]) == down else b
        else:
            bigger = a if (a[4] > b[4]) == right else b
        assert _answer(q) == f"{bigger[2]} ({bigger[1]})", s
        q = generate("chem.periodic_trend_application", Random(seed))
        s = _stem(q)
        prop = next(p for p in trend if f"เรียงลำดับ{p}" in s)
        symbols = _answer(q).split(" < ")
        down, right = trend[prop]
        elements = [by_symbol[x] for x in symbols]
        key = [(e[3] if down else -e[3]) if len({x[4] for x in elements}) == 1 else (e[4] if right else -e[4]) for e in elements]
        assert key == sorted(key), s
        q = generate("chem.periodic_trend_foundation", Random(seed))
        s = _stem(q)
        if "จำนวนอิเล็กตรอนเท่ากัน" in s:
            zs = {m[0]: int(m[1]) for m in re.findall(r"(\S+) \(Z = (\d+)\)", s)}
            expected = min(zs, key=zs.get) if "ใหญ่ที่สุด" in s else max(zs, key=zs.get)
            assert _answer(q) == expected, s


def test_transition_metal_answers():
    from otk.sets.chemistry.m4.transition_metal import ION_COLOURS
    colour_of = dict(ION_COLOURS)
    known = {"O": -2, "Cl": -1, "K": 1, "SO₄": -2, "NO₃": -1}
    subscripts = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
    for seed in range(SEEDS):
        q = generate("chem.transition_metal_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("สารละลายที่มีไอออน"):
            ion = s.split()[1]
            assert _answer(q) == colour_of[ion], s
        else:
            assert s == f"สารละลาย{colour_of[_answer(q)]}น่าจะมีไอออนใด", s
        q = generate("chem.transition_metal_application", Random(seed))
        s = _stem(q)
        metal, formula = re.search(r"ของ (\w+) ใน (\S+) เท่าใด", s).groups()
        rest = 0
        body = formula.translate(subscripts)
        for group, count in re.findall(r"\((NO3|SO4)\)(\d*)", body):
            rest += known[group.replace("3", "₃").replace("4", "₄")] * int(count or 1)
        body = re.sub(r"\((NO3|SO4)\)\d*", "", body)
        for group in ("SO4", "NO3"):
            if group in body:
                rest += known[group.replace("3", "₃").replace("4", "₄")]
                body = body.replace(group, "")
        metal_count = 1
        for symbol, count in re.findall(r"([A-Z][a-z]?)(\d*)", body):
            if symbol == metal:
                metal_count = int(count or 1)
            else:
                rest += known[symbol] * int(count or 1)
        assert _ans(q) * metal_count + rest == 0, s


def test_half_life_and_element_answers():
    from otk.sets.chemistry.m4.element_application import ELEMENT_USES, SAFE_USE
    use_of = {e: u for e, u, _ in ELEMENT_USES}
    effect_of = {e: x for e, _, x in ELEMENT_USES}
    for seed in range(SEEDS):
        q = generate("chem.half_life_calc_foundation", Random(seed))
        s = _stem(q)
        if "จะเหลือกี่กรัม" in s:
            half, start, elapsed = _q(rf"ครึ่งชีวิต {N} \S+\) มวล {N} g เมื่อเวลาผ่านไป {N}", s)
            assert _ans(q) == start / 2 ** int(elapsed / half), s
        q = generate("chem.half_life_calc_fluency", Random(seed))
        s = _stem(q)
        if "มีครึ่งชีวิตเท่าใด" in s:
            start, left, elapsed = _q(rf"มวล {N} g สลายจนเหลือ {N} g ในเวลา {N}", s)
            n = int(start / left).bit_length() - 1
            assert _ans(q) == elapsed / n, s
        else:
            half, start, left = _q(rf"ครึ่งชีวิต {N} \S+ มวล {N} g .*จึงเหลือ {N} g", s)
            assert _ans(q) == half * (int(start / left).bit_length() - 1), s
        q = generate("chem.half_life_calc_application", Random(seed))
        s = _stem(q)
        if "สลายไปแล้วกี่กรัม" in s:
            half, start, elapsed = _q(rf"ครึ่งชีวิต {N} \S+\) มวล {N} g เมื่อผ่านไป {N}", s)
            assert _ans(q) == start - start / 2 ** int(elapsed / half), s
        else:
            elapsed, half = _q(rf"ผ่านไป {N} \S+ \S+ \(ครึ่งชีวิต {N}", s)
            assert _ans(q) == 100 / Fraction(2) ** int(elapsed / half), s
        q = generate("chem.element_application_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("นำไปใช้ประโยชน์ในข้อใด"):
            assert _answer(q) == use_of[s.removesuffix("นำไปใช้ประโยชน์ในข้อใด")], s
        else:
            assert s == f"ธาตุใดนำไปใช้{use_of[_answer(q)]}", s
        q = generate("chem.element_application_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ข้อใดเป็นผลกระทบของ"):
            assert _answer(q) == effect_of[s.removeprefix("ข้อใดเป็นผลกระทบของ")], s
        else:
            assert s == f"ผลกระทบ \"{effect_of[_answer(q)]}\" เกิดจากธาตุใด", s
        q = generate("chem.element_application_application", Random(seed))
        s = _stem(q)
        safe = {stem: correct for stem, correct, _ in SAFE_USE}
        if s in safe:
            assert _answer(q) == safe[s], s
        else:
            assert s == f"ธาตุที่ใช้{use_of[_answer(q)]} แต่ {effect_of[_answer(q)]} คือธาตุใด", s


def test_ionic_answers():
    from math import gcd
    from otk.sets._support.science_wave_f19 import REPRESENTATIVE
    by_name = {e[2]: e for e in REPRESENTATIVE}

    def valence(e):
        return e[4] if e[4] <= 2 else e[4] - 10

    def charge(e):
        v = valence(e)
        return v if v <= 3 else v - 8

    for seed in range(SEEDS):
        q = generate("chem.ionic_lewis_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("สัญลักษณ์แบบจุด"):
            name = re.search(r"ลิวอิสของ(\S+?) \(", s).group(1)
            assert _ans(q) == valence(by_name[name]), s
        else:
            (dots,) = _q(rf"ล้อมด้วย {N} จุด", s)
            name = _answer(q).split(" (")[0]
            assert valence(by_name[name]) == dots, s
        q = generate("chem.ionic_lewis_fluency", Random(seed))
        s = _stem(q)
        name = re.match(r"(\S+) \(", s).group(1)
        e = by_name[name]
        if "มีอิเล็กตรอนกี่ตัว" in s:
            assert _ans(q) == e[0] - charge(e), s
        elif "อิเล็กตรอนกี่ตัว" in s:
            assert _ans(q) == abs(charge(e)), s
        q = generate("chem.ionic_lewis_application", Random(seed))
        s = _stem(q)
        named = sorted((s.index(f"{n} ("), e) for n, e in by_name.items() if f"{n} (" in s)
        assert len(named) == 2, s
        m, x = named[0][1], named[1][1]
        p, qq = charge(m), -charge(x)
        k = gcd(p, qq)
        if "ถ่ายโอนอิเล็กตรอน" in s:
            assert _ans(q) == qq // k * p, s
        else:
            sub = lambda n: "" if n == 1 else str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            assert _answer(q) == f"{m[1]}{sub(qq // k)}{x[1]}{sub(p // k)}", s


# ── Slices 21-22: เคมีเพิ่มเติม 1 ม.4/10-/16 ───────────────────────────────────────

def test_ionic_formula_names_and_equations_agree():
    from otk.sets._support.science_wave_f21 import ANIONS, CATIONS, formula, name
    from otk.sets.chemistry.m4.net_ionic import insoluble, net_ionic
    by_name = {name(c, a): (c, a) for c in CATIONS for a in ANIONS}
    by_formula = {}
    for c in CATIONS:
        for a in ANIONS:
            by_formula.setdefault(formula(c, a), []).append((c, a))
    assert formula(next(c for c in CATIONS if c[1] == "อะลูมิเนียม"), next(a for a in ANIONS if a[0] == "SO₄")) == "Al₂(SO₄)₃"
    assert formula(next(c for c in CATIONS if c[1] == "เหล็ก(III)"), next(a for a in ANIONS if a[0] == "O")) == "Fe₂O₃"
    for seed in range(SEEDS):
        q = generate("chem.ionic_naming_foundation", Random(seed))
        s = _stem(q)
        c, a = by_name[s.split(" มีสูตรเคมีใด")[0]]
        assert _answer(q) == formula(c, a), s
        q = generate("chem.ionic_naming_fluency", Random(seed))
        s = _stem(q)
        f = s.split()[1]
        assert (_answer(q) in {name(c, a) for c, a in by_formula[f]}), s
        q = generate("chem.ionic_naming_application", Random(seed))
        s = _stem(q)
        if s.startswith("สารประกอบ"):
            f = s.split()[1]
            assert _answer(q) in {name(c, a) for c, a in by_formula[f]}, s
        else:
            c, a = by_name[s.split(" มีสูตรเคมีใด")[0]]
            assert _answer(q) == formula(c, a), s
        for key in ("chem.net_ionic_foundation", "chem.net_ionic_fluency", "chem.net_ionic_application"):
            q = generate(key, Random(seed))
            s = _stem(q)
            salts = re.search(r"ผสมสารละลาย (\S+) กับ(?:สารละลาย)? (\S+)", s).groups()
            pairs = [by_formula[x][0] for x in salts]
            (c1, a1), (c2, a2) = pairs
            precipitates = [(c, a) for c, a in ((c1, a2), (c2, a1)) if insoluble(c, a)]
            assert len(precipitates) == 1, s
            c, a = precipitates[0]
            if key.endswith("foundation"):
                assert _answer(q) == formula(c, a), s
            elif key.endswith("fluency"):
                assert _answer(q) == net_ionic(c, a), s
            else:
                spectators = [(c2, a1) if (c, a) == (c1, a2) else (c1, a2)][0]
                assert spectators[0][0] in _answer(q) and spectators[1][0] in _answer(q), s


def test_born_haber_cycles_add_up():
    labels = ("พลังงานการระเหิดของโลหะ", "พลังงานไอออไนเซชันของโลหะ", "พลังงานสลายพันธะของฮาโลเจน (ครึ่งโมล)",
              "พลังงานสัมพรรคภาพอิเล็กตรอน", "พลังงานโครงผลึก (รวมไอออนเป็นผลึก)")
    for seed in range(SEEDS):
        q = generate("chem.born_haber_fluency", Random(seed))
        s = _stem(q)
        steps = [int(re.search(re.escape(ell) + r" ([+-]\d+) kJ/mol", s).group(1)) for ell in labels]
        assert _ans(q) == sum(steps), s
        q = generate("chem.born_haber_application", Random(seed))
        s = _stem(q)
        total = int(re.search(r"การเกิดสารประกอบ ([+-]\d+) kJ/mol", s).group(1))
        known = [int(m.group(1)) for ell in labels if (m := re.search(re.escape(ell) + r" ([+-]\d+) kJ/mol", s))]
        assert len(known) == 4 and _ans(q) == total - sum(known), s


def test_ionic_properties_follow_charge_then_size():
    from otk.sets.chemistry.m4.ionic_property import LATTICE
    table = {x[0]: x for x in LATTICE}
    for seed in range(SEEDS):
        q = generate("chem.ionic_property_fluency", Random(seed))
        s = _stem(q)
        a, b = (table[x] for x in re.findall(r"(\S+) \(ประจุไอออน", s))
        key = lambda t: (t[1] * t[2], -t[3])
        assert _answer(q) == max(a, b, key=key)[0], s
        q = generate("chem.ionic_property_application", Random(seed))
        s = _stem(q)
        if s.startswith("เรียงลำดับ"):
            order = _answer(q).split(" > ")
            radii = [table[x][3] for x in order]
            assert radii == sorted(radii), s
        q = generate("chem.ionic_property_foundation", Random(seed))
        s = _stem(q)
        if "ในสถานะ" in s:
            assert _answer(q).startswith("ไม่นำไฟฟ้า" if "ของแข็ง" in s else "นำไฟฟ้าได้"), s


def test_covalent_answers():
    from otk.sets.chemistry.m4.bond_energy import BOND_ENERGY, REACTIONS
    from otk.sets.chemistry.m4.covalent_naming import COMPOUNDS, covalent_formula, covalent_name
    from otk.sets.chemistry.m4.covalent_lewis import MOLECULES
    mol = {m[0]: m for m in MOLECULES}
    by_name = {covalent_name(*c): c for c in COMPOUNDS}
    assert covalent_name("C", 1, "O", 1) == "คาร์บอนมอนอกไซด์"
    assert covalent_name("N", 2, "O", 5) == "ไดไนโตรเจนเพนตะออกไซด์"
    assert covalent_name("S", 1, "F", 6) == "ซัลเฟอร์เฮกซะฟลูออไรด์"
    for m in MOLECULES:
        # Every electron pair is counted once: a quick octet sanity check on the table.
        assert m[2] + 2 * m[3] + 3 * m[4] > 0
    for seed in range(SEEDS):
        q = generate("chem.covalent_lewis_fluency", Random(seed))
        s = _stem(q)
        m = mol[s.split("ของ ")[1].split(" ")[0]]
        bonding = m[2] + 2 * m[3] + 3 * m[4]
        assert _ans(q) == (bonding if "ร่วมพันธะ" in s else m[5]), s
        q = generate("chem.covalent_lewis_application", Random(seed))
        s = _stem(q)
        m = mol[re.search(r"(?:ของ |^)(\S+) \(", s).group(1)]
        bonding = m[2] + 2 * m[3] + 3 * m[4]
        assert _ans(q) == (2 * (bonding + m[5]) if "ทั้งหมดกี่ตัว" in s else m[5]), s
        q = generate("chem.covalent_naming_foundation", Random(seed))
        s = _stem(q)
        f = s.split()[1]
        assert covalent_formula(*by_name[_answer(q)]) == f, s
        q = generate("chem.covalent_naming_fluency", Random(seed))
        s = _stem(q)
        assert _answer(q) == covalent_formula(*by_name[s.split(" มีสูตรเคมีใด")[0]]), s
        q = generate("chem.covalent_naming_application", Random(seed))
        s = _stem(q)
        label = s.split(" ")[0]
        a, na, b, nb = by_name[label]
        if "อะตอมทั้งหมดกี่อะตอม" in s:
            assert _ans(q) == na + nb, s
        else:
            (count,) = _q(rf" {N} โมเลกุล", s)
            assert _ans(q) == count * nb, s
        q = generate("chem.bond_energy_fluency", Random(seed))
        s = _stem(q)
        eq = re.search(r"ปฏิกิริยา (.+?) (?:ตามสมการ|เมื่อ)", s).group(1)
        _, broken, formed = next(r for r in REACTIONS if r[0] == eq)
        found = re.search(r"เกิดปฏิกิริยา (\d+) เท่า", s)
        moles = int(found.group(1)) if found else 1
        energy = lambda bonds: sum(BOND_ENERGY[b] * n for b, n in bonds.items())
        assert _ans(q) == (energy(broken) - energy(formed)) * moles, s
        q = generate("chem.bond_energy_application", Random(seed))
        s = _stem(q)
        eq = re.search(r"ปฏิกิริยา (.+?) (?:มีพลังงาน|\()", s).group(1)
        _, broken, formed = next(r for r in REACTIONS if r[0] == eq)
        if "เป็นปฏิกิริยาแบบใด" in s:
            assert _answer(q) == ("คายพลังงาน" if energy(broken) < energy(formed) else "ดูดพลังงาน"), s
        else:
            hidden = re.search(r"พลังงานพันธะ (\S+) เท่าใด", s).group(1)
            assert _ans(q) == BOND_ENERGY[hidden], s


# ── Slices 23-24: เคมีเพิ่มเติม 1 ม.4/17-/21, ม.5/1-/2 ─────────────────────────────────

def _nums(stem: str) -> list[Fraction]:
    return [Fraction(x.replace(",", "")) for x in re.findall(N, stem)]


def test_vsepr_shapes_and_polarity():
    from otk.sets.chemistry.m4.vsepr_shape import (
        NONPOLAR_WHY,
        POLAR_WHY,
        SHAPE_MOLECULES,
        SHAPES,
        shape_of,
    )
    mol = {m[0]: m for m in SHAPE_MOLECULES}
    for m in SHAPE_MOLECULES:
        # Only the symmetrical shapes can cancel their bond dipoles.
        if not m[4]:
            assert (m[2], m[3]) in {(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (2, 3), (4, 2)}, m
        if m[3] and (m[2], m[3]) not in {(2, 3), (4, 2)}:
            assert m[4], m
    for seed in range(SEEDS):
        q = generate("chem.vsepr_shape_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("อะตอมกลาง"):
            bonded, = _q(r"อะตอมอื่น (\d+) อะตอม", s)
            lone = _q(r"คู่โดดเดี่ยว (\d+) คู่", s)[0] if "ไม่มีอิเล็กตรอนคู่โดดเดี่ยว" not in s else 0
            assert _answer(q) == SHAPES[(int(bonded), int(lone))], s
        else:
            m = mol[re.search(r"โมเลกุล (\S+) \(", s).group(1)]
            assert _ans(q) == m[2] + m[3], s
        q = generate("chem.vsepr_shape_fluency", Random(seed))
        s = _stem(q)
        m = mol[re.search(r"โมเลกุล (\S+) \(", s).group(1)]
        assert (_ans(q) == m[5]) if s.startswith("มุมพันธะ") else (_answer(q) == shape_of(m)), s
        q = generate("chem.vsepr_shape_application", Random(seed))
        s = _stem(q)
        if s.startswith("โมเลกุลใด"):
            assert mol[_answer(q)][4] == (s == "โมเลกุลใดมีขั้ว"), s
        else:
            m = mol[re.search(r"โมเลกุล (\S+) \(", s).group(1)]
            assert _answer(q) == (POLAR_WHY if m[4] else NONPOLAR_WHY), s


def test_boiling_points_follow_force_then_mass():
    from otk.sets.chemistry.m4.intermolecular_force import (
        FORCES,
        PAIRS,
        SUBSTANCES,
        TRIPLES,
        higher_boiling,
    )
    by = {x[0]: x for x in SUBSTANCES}
    assert len(PAIRS) > 100 and len(TRIPLES) > 20
    for a, b in PAIRS:
        pick = higher_boiling(a, b)
        assert pick[3] == max(a[3], b[3])
    for seed in range(SEEDS):
        q = generate("chem.intermolecular_force_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("แรงยึดเหนี่ยว"):
            assert _answer(q) == FORCES[by[re.search(r"ใน (\S+) \(", s).group(1)][4]], s
        q = generate("chem.intermolecular_force_fluency", Random(seed))
        s = _stem(q)
        names = re.findall(r"(\S+) \(มวลโมเลกุล", s)
        if s.startswith("เรียง"):
            assert _answer(q).split(" > ") == sorted(names, key=lambda n: -by[n][3]), s
        else:
            assert _answer(q) == higher_boiling(by[names[0]], by[names[1]])[0], s
        q = generate("chem.intermolecular_force_application", Random(seed))
        s = _stem(q)
        if "เหตุผลหลัก" in s:
            x, y = (by[n] for n in re.findall(r"(\S+) \(\S+, มวลโมเลกุล", s))
            assert higher_boiling(x, y) is x, s
            assert _answer(q).startswith(x[0]), s


def test_network_and_metal_answers():
    from otk.sets.chemistry.m4.metallic_bond import METAL_CHAINS, METALS
    from otk.sets.chemistry.m4.network_covalent import NETWORK_BONDS
    per = {n[0]: n[1] for n in NETWORK_BONDS}
    for chain in METAL_CHAINS:
        melts = [METALS[s][3] for s in chain]
        assert melts == sorted(melts), chain
    for seed in range(SEEDS):
        q = generate("chem.network_covalent_fluency", Random(seed))
        s = _stem(q)
        substance = next(n for n in per if s.startswith(n + "ที่") or s.startswith(n + "หนัก"))
        values = _nums(s)
        amount = values[0] / values[-1] if "กรัม" in s else values[0]
        assert _ans(q) == per[substance] * amount, s
        q = generate("chem.metallic_bond_fluency", Random(seed))
        s = _stem(q)
        symbol = re.search(r"\(([A-Z][a-z]?)\)", s).group(1)
        if "ทะเลอิเล็กตรอน" in s:
            values = _q(rf"\) {N} (?:โมล|กรัม)", s)
            moles = values[0] / METALS[symbol][2] if "กรัม" in s else values[0]
            assert _ans(q) == moles * METALS[symbol][1], s
        else:
            a, b = re.findall(r"\(([A-Z][a-z]?)\)", s)
            assert _answer(q).endswith(f"({max(a, b, key=lambda x: METALS[x][3])})"), s
        q = generate("chem.metallic_bond_application", Random(seed))
        s = _stem(q)
        if s.startswith("เรียง"):
            order = _answer(q).split(" > ")
            assert [METALS[x][3] for x in order] == sorted((METALS[x][3] for x in order), reverse=True), s


def test_bond_type_answers():
    from otk.sets.chemistry.m4.bond_type_compare import (
        MELT_IONIC,
        MELT_MOLECULAR,
        MELT_NETWORK,
        PROFILES,
        SAMPLES,
    )
    kinds = dict(SAMPLES)
    melt = dict(MELT_NETWORK + MELT_IONIC + MELT_MOLECULAR)
    assert min(dict(MELT_NETWORK).values()) > max(dict(MELT_IONIC).values())
    assert min(dict(MELT_IONIC).values()) > max(dict(MELT_MOLECULAR).values())
    for seed in range(SEEDS):
        q = generate("chem.bond_type_compare_foundation", Random(seed))
        s = _stem(q)
        assert _answer(q) == kinds[s.split(" จัดเป็น")[0]], s
        q = generate("chem.bond_type_compare_fluency", Random(seed))
        s = _stem(q)
        (m,) = _q(rf"จุดหลอมเหลว {N} °C", s)
        matches = [k for k, (key, _, (low, high)) in PROFILES.items() if key in s and low <= m <= high]
        assert matches == [_answer(q)], s
        q = generate("chem.bond_type_compare_application", Random(seed))
        s = _stem(q)
        if s.startswith("เรียง"):
            order = _answer(q).split(" > ")
            assert [melt[x] for x in order] == sorted((melt[x] for x in order), reverse=True), s


def test_gas_law_answers_recompute():
    for seed in range(SEEDS):
        q = generate("chem.gas_law_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("แก๊สปริมาตร"):
            v1, p1, other = _nums(s)[:3]
            assert _ans(q) == p1 * v1 / other, s
        q = generate("chem.gas_law_fluency", Random(seed))
        s = _stem(q)
        v1, c1, x = _nums(s)[:3]
        if "ต้องเปลี่ยนอุณหภูมิ" in s:
            v2 = _nums(s)[2]
            assert _ans(q) == v2 / v1 * (c1 + 273) - 273, s
        else:
            assert _ans(q) == v1 * (x + 273) / (c1 + 273), s
        q = generate("chem.gas_law_application", Random(seed))
        s = _stem(q)
        if s.startswith("ยาง"):
            p1, c1, c2 = _nums(s)[:3]
            assert _ans(q) == p1 * (c2 + 273) / (c1 + 273), s
        elif s.startswith("กระป๋อง"):
            p1, c1, p2 = _nums(s)[:3]
            assert _ans(q) == p2 / p1 * (c1 + 273) - 273, s
        q = generate("chem.combined_gas_foundation", Random(seed))
        s = _stem(q)
        v1, p1, c1, p2, c2 = _nums(s)[:5]
        assert _ans(q) == p1 * v1 * (c2 + 273) / (p2 * (c1 + 273)), s
        q = generate("chem.combined_gas_fluency", Random(seed))
        s = _stem(q)
        v1, p1, c1, v2, x = _nums(s)[:5]
        if "ต้องมีอุณหภูมิ" in s:
            assert _ans(q) == x * v2 * (c1 + 273) / (p1 * v1) - 273, s
        else:
            assert _ans(q) == p1 * v1 * (x + 273) / (v2 * (c1 + 273)), s
        q = generate("chem.combined_gas_application", Random(seed))
        s = _stem(q)
        if s.startswith("เก็บแก๊ส"):
            v1, p1, c1 = _nums(s)[:3]
            assert _ans(q) == p1 * v1 * 273 / (760 * (c1 + 273)), s
        else:
            v1, p1, c1, p2, c2 = _nums(s)[:5]
            assert p2 * 760 < p1 and c2 < c1, s
            assert _ans(q) == p1 / 760 * v1 * (c2 + 273) / (p2 * (c1 + 273)), s


# ── Slices 25-26: เคมีเพิ่มเติม 1 ม.5/3-/6, ม.6/1-/3 ──────────────────────────────────

def test_ideal_gas_dalton_and_graham_recompute():
    from otk.sets._support.science_wave_f25 import GASES
    from otk.sets.chemistry.m5.ideal_gas import R
    by_mass = {m: f for f, (_, m) in GASES.items()}
    for seed in range(SEEDS):
        q = generate("chem.ideal_gas_fluency", Random(seed))
        s = _stem(q)
        values = {}
        for key, pattern in (("n", rf"แก๊ส(?:ที่มี)? {N} โมล"), ("V", rf"ปริมาตร {N} L"),
                             ("T", rf"อุณหภูมิ {N} °C"), ("P", rf"ความดัน {N} atm")):
            found = re.search(pattern, s)
            if found:
                values[key] = Fraction(found.group(1).replace(",", ""))
        if "T" in values:
            values["T"] += 273
        if "มีความดันกี่" in s:
            assert _ans(q) == values["n"] * R * values["T"] / values["V"], s
        elif "มีปริมาตรกี่" in s:
            assert _ans(q) == values["n"] * R * values["T"] / values["P"], s
        elif "มีอุณหภูมิกี่" in s:
            assert _ans(q) == values["P"] * values["V"] / (values["n"] * R), s
        else:
            assert _ans(q) == values["P"] * values["V"] / (R * values["T"]), s
        q = generate("chem.ideal_gas_application", Random(seed))
        s = _stem(q)
        m, v, p, c = _q(rf"หนัก {N} กรัม มีปริมาตร {N} L ที่ความดัน {N} atm และอุณหภูมิ {N} °C", s)
        molar = m * R * (c + 273) / (p * v)
        if "มวลโมเลกุลของแก๊สนี้" in s:
            assert _ans(q) == molar, s
        else:
            assert _answer(q).startswith(by_mass[molar] + " "), s
        q = generate("chem.dalton_pressure_fluency", Random(seed))
        s = _stem(q)
        if "ประกอบด้วย" in s:
            na, nb, total = _q(rf"(?:\S+) {N} โมล และ (?:\S+) {N} โมล มีความดันรวม {N}", s)
            assert _ans(q) == na / (na + nb) * total, s
        else:
            total, nb, pa = _q(rf"ความดันรวม {N} \S+ มี \S+ {N} โมล และ \S+ มีความดันย่อย {N}", s)
            assert _ans(q) == nb * pa / (total - pa), s
        q = generate("chem.dalton_pressure_application", Random(seed))
        s = _stem(q)
        if s.startswith("ถัง"):
            va, pa, vb, pb = _q(rf"ปริมาตร {N} L บรรจุ \S+ ความดัน {N} atm ถัง B ปริมาตร {N} L บรรจุ \S+ ความดัน {N} atm", s)
            part = pa * va / (va + vb)
            assert _ans(q) == (part if "ความดันย่อย" in s else part + pb * vb / (va + vb)), s
        else:
            total, vapour = _q(rf"ความดันรวม {N} mmHg ถ้าความดันไอน้ำที่ \d+ °C เท่ากับ {N}", s)
            assert _ans(q) == total - vapour, s
        q = generate("chem.graham_diffusion_application", Random(seed))
        s = _stem(q)
        speed, known = _q(rf"กว่าแก๊ส\S+ \(\S+\) {N} เท่า \(มวลโมเลกุล \S+ = {N}\)", s)
        molar = known / speed ** 2 if "เร็วกว่า" in s else known * speed ** 2
        if "มวลโมเลกุลของ X" in s:
            assert _ans(q) == molar, s
        else:
            assert _answer(q).startswith(by_mass[molar] + " "), s
        q = generate("chem.graham_diffusion_fluency", Random(seed))
        s = _stem(q)
        m1, m2 = _q(rf"มวลโมเลกุล \S+ = {N}, \S+ = {N}\)", s)
        ratio = Fraction(round(float(m2 / m1) ** 0.5 * 100), 100)
        assert ratio * ratio == m2 / m1, s
        if "กี่เท่า" in s:
            assert _ans(q) == ratio, s
        else:
            (t,) = _q(rf"ใช้เวลา {N} วินาที", s)
            light_first = s.index(f"({[f for f in GASES if GASES[f][1] == m1][0]})") < s.index("ใช้เวลา")
            assert _ans(q) == (t * ratio if light_first else t / ratio), s


def test_gas_applications_recompute():
    for seed in range(SEEDS):
        q = generate("chem.gas_application_fluency", Random(seed))
        s = _stem(q)
        (depth,) = _q(rf"ความลึก {N} m", s)
        pressure = 1 + depth / 10
        if "ความดันย่อยของ O₂" in s:
            assert _ans(q) == Fraction(21, 100) * pressure, s
        elif "ความดันย่อยของ N₂" in s:
            assert _ans(q) == Fraction(79, 100) * pressure, s
        elif s.startswith("นักดำน้ำกลั้นหายใจ"):
            (v,) = _q(rf"ปริมาตร {N} L", s)
            assert _ans(q) == v * pressure, s
        else:
            (v,) = _q(rf"อากาศ {N} L", s)
            assert _ans(q) == v / pressure, s
        q = generate("chem.gas_application_application", Random(seed))
        s = _stem(q)
        if "ถุงลมนิรภัยใช้" in s:
            (grams,) = _q(rf"NaN₃ {N} กรัม", s)
            assert _ans(q) == grams / 65 * Fraction(3, 2) * Fraction(224, 10), s
        elif "ถุงลมนิรภัยต้องการ" in s:
            (litres,) = _q(rf"ไนโตรเจน {N} ลิตร", s)
            assert _ans(q) == litres / Fraction(224, 10) * Fraction(2, 3) * 65, s
        elif "ต้องทำให้" in s:
            cold, ratio = _q(rf"อุณหภูมิ {N} °C .*เหลือ {N} เท่า", s)
            assert _ans(q) == (cold + 273) / ratio - 273, s
        else:
            cold, hot = _q(rf"อุณหภูมิ {N} °C ถ้าอากาศในบอลลูนร้อน {N} °C", s)
            assert _ans(q) == (cold + 273) / (hot + 273), s


def test_organic_bond_table_balances_valence():
    from otk.sets.chemistry.m6.organic_bond import EVERYDAY, bond_kind
    from otk.sets._support.science_wave_f26 import VALENCE
    from otk.sets.chemistry.m6.structural_formula import chain
    by_formula = {e[1]: e for e in EVERYDAY}
    for e in EVERYDAY:
        # Every bond uses two valences: Σ valence / 2 = single + 2 double + 3 triple.
        assert sum(VALENCE[k] * n for k, n in e[3].items()) == 2 * (e[4] + 2 * e[5] + 3 * e[6]), e
    assert chain(4, 2) [0] == "CH₃CH(CH₃)CH₂CH₃"
    assert chain(3, None, None, True)[0] == "CH₂=CHCH₃"
    assert chain(6)[1] == "CH₃(CH₂)₄CH₃"
    assert chain(5, None, "OH")[1] == "CH₃(CH₂)₄OH"
    for seed in range(SEEDS):
        q = generate("chem.organic_bond_fluency", Random(seed))
        s = _stem(q)
        e = by_formula[re.search(r"\((\S+)\) มี", s).group(1)]
        if "พันธะเดี่ยว" in s:
            assert _ans(q) == e[4], s
        elif "ทั้งหมดกี่พันธะ (พันธะคู่" in s:
            assert _ans(q) == e[4] + e[5] + e[6], s
        else:
            assert _ans(q) == (e[6] if "พันธะสาม" in s else e[5]), s
        q = generate("chem.organic_bond_foundation", Random(seed))
        s = _stem(q)
        if "ในโมเลกุลมีพันธะแบบใด" in s:
            assert _answer(q) == bond_kind(by_formula[re.search(r"\((\S+)\) ใช้", s).group(1)]), s


def test_structural_formulas_count_atoms():
    from otk.sets.chemistry.m6.structural_formula import molecular
    sub = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

    def atoms(condensed: str) -> dict:
        plain = condensed.translate(sub).replace("=", "").replace("(", "").replace(")", "")
        found = {}
        for element, count in re.findall(r"(Cl|Br|C|H|O|N)(\d*)", plain):
            found[element] = found.get(element, 0) + int(count or 1)
        return found

    for seed in range(SEEDS):
        q = generate("chem.structural_formula_foundation", Random(seed))
        s = _stem(q)
        condensed = re.search(r"แบบย่อ (\S+) มี", s).group(1)
        assert _answer(q) == molecular(atoms(condensed)), s
        q = generate("chem.structural_formula_fluency", Random(seed))
        s = _stem(q)
        if "สั้นลง" in s:
            condensed = s.split(" ")[0]
            run = re.search(r"\(CH₂\)(\S)", _answer(q)).group(1).translate(sub)
            assert condensed.count("CH₂") == int(run), s
        else:
            condensed = re.search(r"ลิวอิสของ (\S+) จะ", s).group(1)
            found = atoms(condensed)
            extra = {"OH": 1, "NH₂": 2}
            tail = next((k for k in extra if condensed.endswith(k)), None)
            assert _ans(q) == found["H"] - (extra[tail] if tail else 0), s


def test_functional_group_classes():
    from otk.sets.chemistry.m6.functional_group import CLASSES, EXAMPLES
    cls = dict(EXAMPLES)
    assert len(cls) == len(EXAMPLES)
    for seed in range(SEEDS):
        q = generate("chem.functional_group_fluency", Random(seed))
        s = _stem(q)
        assert _answer(q) == cls[s.split(" ")[1]], s
        q = generate("chem.functional_group_application", Random(seed))
        s = _stem(q)
        if "ประเภทเดียวกับ" in s:
            given = s.split("ประเภทเดียวกับ ")[1]
            assert cls[_answer(q)] == cls[given] and _answer(q) != given, s
        else:
            assert cls[_answer(q)] == s.split("จัดเป็น")[1], s
        q = generate("chem.functional_group_foundation", Random(seed))
        s = _stem(q)
        if "จัดเป็นสารประเภทใด" in s:
            group = s.split("หมู่ฟังก์ชัน ")[1].split(" จัดเป็น")[0]
            assert CLASSES[_answer(q)][0] == group, s


# ── Slices 27-28: เคมีเพิ่มเติม 1 ม.6/4-/8, ม.6/10-/11 ───────────────────────────────

def test_organic_bank_is_consistent():
    from otk.sets.chemistry.m6.iupac_name import BY_NAME, MISNAMED
    from otk.sets._support.science_wave_f27 import COMPOUNDS, atoms_of, molecular
    from otk.sets.chemistry.m6.structural_isomer import ISOMER_COUNTS
    valence = {"C": 4, "H": 1, "O": 2, "N": 3, "Cl": 1}
    assert len(BY_NAME) == len(COMPOUNDS)
    assert len({c[1] for c in COMPOUNDS}) == len(COMPOUNDS)
    for c in COMPOUNDS:
        atoms = atoms_of(c[1])
        # Every bond uses two valences, and no open chain carries more than 2C + 2 + N monovalent atoms.
        assert sum(valence[k] * v for k, v in atoms.items()) % 2 == 0, c
        assert atoms.get("H", 0) + atoms.get("Cl", 0) <= 2 * atoms["C"] + 2 + atoms.get("N", 0), c
    assert atoms_of("CH₃C(CH₃)₂CH₃") == {"C": 5, "H": 12}
    for formula, classes, count in ISOMER_COUNTS:
        assert len([c for c in COMPOUNDS if molecular(c[1]) == formula and c[2] in classes]) == count
    for wrong, right in MISNAMED:
        assert right in BY_NAME and wrong not in BY_NAME


def test_iupac_and_isomer_answers():
    from otk.sets.chemistry.m6.iupac_name import BY_NAME
    from otk.sets._support.science_wave_f27 import COMPOUNDS, atoms_of, molecular
    from otk.sets.chemistry.m6.structural_isomer import ISOMER_COUNTS
    by_formula = {c[1]: c for c in COMPOUNDS}
    counts = {(f, tuple(cls)): n for f, cls, n in ISOMER_COUNTS}
    for seed in range(SEEDS):
        q = generate("chem.iupac_name_foundation", Random(seed))
        s = _stem(q)
        assert _answer(q) == by_formula[s.split(" ")[1]][0], s
        q = generate("chem.iupac_name_fluency", Random(seed))
        s = _stem(q)
        # Some names carry a space (กรด 2-เมทิลโพรพาโนอิก), so match the longest bank name.
        name = max((n for n in BY_NAME if s.startswith(n + " ")), key=len)
        if "สูตรโครงสร้างแบบย่อใด" in s:
            assert _answer(q) == BY_NAME[name][1], s
        else:
            label = re.search(r"มีอะตอม(\S+?)กี่อะตอม", s).group(1)
            element = {"คาร์บอน": "C", "ไฮโดรเจน": "H", "ออกซิเจน": "O", "ไนโตรเจน": "N", "คลอรีน": "Cl"}[label]
            assert _ans(q) == atoms_of(BY_NAME[name][1])[element], s
        q = generate("chem.structural_isomer_foundation", Random(seed))
        s = _stem(q)
        given = s.split("ของ ")[1]
        assert molecular(_answer(q)) == molecular(given) and _answer(q) != given, s
        q = generate("chem.structural_isomer_fluency", Random(seed))
        s = _stem(q)
        formula = re.search(r"สูตรโมเลกุล (\S+) ที่เป็น", s).group(1)
        if s.startswith("ข้อใด"):
            picked = re.search(r"\((\S+)\)$", _answer(q)).group(1)
            assert molecular(picked) == formula, s
        else:
            kinds = s.split("ที่เป็น")[1].split(" มีไอโซเมอร์")[0]
            assert _ans(q) == counts[(formula, tuple(kinds.split("และ")))], s
        q = generate("chem.structural_isomer_application", Random(seed))
        s = _stem(q)
        if s.startswith("สารใด"):
            given = BY_NAME[s.split("ของ ")[1].split(" (")[0]]
            picked = BY_NAME[_answer(q).split(" (")[0]]
            assert molecular(picked[1]) == molecular(given[1]) and picked[2] != given[2], s


def test_organic_boiling_points_follow_the_rules():
    from otk.sets.chemistry.m6.organic_property import BP_PAIRS, higher_boiling
    from otk.sets.chemistry.m6.iupac_name import BY_NAME
    assert len(BP_PAIRS) > 100
    for a, b in BP_PAIRS:
        assert higher_boiling(a, b)[4] == max(a[4], b[4])
    for seed in range(SEEDS):
        q = generate("chem.organic_property_fluency", Random(seed))
        s = _stem(q)
        names = "|".join(re.escape(n) for n in sorted(BY_NAME, key=len, reverse=True))
        a, b = (BY_NAME[n] for n in re.findall(rf"({names}) \(\S+, มวลโมเลกุล", s))
        assert _answer(q) == higher_boiling(a, b)[0], s
        q = generate("chem.organic_property_application", Random(seed))
        s = _stem(q)
        if s.startswith("เรียง"):
            order = [BY_NAME[n] for n in _answer(q).split(" > ")]
            assert [c[4] for c in order] == sorted((c[4] for c in order), reverse=True), s


def test_hydrocarbon_reactions_balance():
    from otk.sets._support.science_wave_f27 import atoms_of
    from otk.sets.chemistry.m6.hydrocarbon_reaction import HYDROCARBONS, TESTS, combustion
    for _, condensed, _ in HYDROCARBONS:
        atoms = atoms_of(condensed)
        fuel, oxygen, co2, water = combustion(atoms)
        assert fuel * atoms["C"] == co2 and fuel * atoms["H"] == 2 * water and 2 * oxygen == 2 * co2 + water
    by = {h[0]: h for h in HYDROCARBONS}
    for seed in range(SEEDS):
        q = generate("chem.hydrocarbon_reaction_fluency", Random(seed))
        s = _stem(q)
        name = re.search(r"(?:ของ|เผา) (.+?) \(", s).group(1)
        fuel, oxygen, co2, water = combustion(atoms_of(by[name][1]))
        if "สัมประสิทธิ์" in s:
            assert _ans(q) == oxygen, s
        elif "ออกซิเจนกี่โมล" in s:
            (moles,) = _q(rf"\) {N} โมล", s)
            assert _ans(q) == moles * Fraction(oxygen, fuel), s
        else:
            moles, mass = _q(rf"\) {N} โมล.*= {N}\)", s)
            per = Fraction(co2 if "CO₂ กี่กรัม" in s else water, fuel)
            assert _ans(q) == moles * per * mass, s
        q = generate("chem.hydrocarbon_reaction_foundation", Random(seed))
        s = _stem(q)
        if "จะสังเกตเห็นอะไร" in s:
            cls = by[re.match(r"(.+?) \(", s).group(1)][2]
            index = 2 if "KMnO₄" in s else 1 if "ที่สว่าง" in s else 0
            assert _answer(q) == TESTS[cls][index], s


def test_ester_and_amide_products():
    from otk.sets.chemistry.m6.ester_amide import ACIDS, ALCOHOLS, AMINES, amide, ester, salt
    assert ester(ACIDS[1], ALCOHOLS[1]) == ("เอทิลเอทาโนเอต", "CH₃COOCH₂CH₃")
    assert amide(ACIDS[1], AMINES[0]) == ("N-เมทิลเอทานาไมด์", "CH₃CONHCH₃")
    assert salt(ACIDS[2]) == ("โซเดียมโพรพาโนเอต", "CH₃CH₂COONa")
    acid_by = {a[0]: a for a in ACIDS}
    alcohol_by = {a[0]: a for a in ALCOHOLS}
    for seed in range(SEEDS):
        q = generate("chem.ester_amide_fluency", Random(seed))
        s = _stem(q)
        if "ได้เอสเทอร์ชื่อใด" in s:
            acid, alcohol = re.match(r"(\S+) ทำปฏิกิริยากับ(\S+) \(", s).groups()
            assert _answer(q) == ester(acid_by[acid], alcohol_by[alcohol])[0], s
        elif s.startswith("ไฮโดรลิซิส"):
            name = s.split(" ")[1]
            pair = next((a, b) for a in ACIDS for b in ALCOHOLS if ester(a, b)[0] == name)
            assert _answer(q) == f"{pair[0][0]} และ{pair[1][0]}", s
        q = generate("chem.ester_amide_application", Random(seed))
        s = _stem(q)
        if "ไตรกลีเซอไรด์" in s:
            (moles,) = _q(rf"\) {N} โมล", s)
            assert _ans(q) == (moles * 120 if "กรัม" in s else moles * 3), s


def test_polymer_answers():
    from otk.sets.chemistry.m6.polymerization import ADDITION, POLYMERS, REPEATS
    for p in POLYMERS:
        # An addition monomer shows its C=C; a condensation one loses water.
        assert ("=" in p[2]) == (p[3] == ADDITION) and (p[4] is None) == (p[3] == ADDITION), p
    kinds = {p[0]: p[3] for p in POLYMERS}
    mass = {r[0]: r[2] for r in REPEATS}
    for seed in range(SEEDS):
        q = generate("chem.polymerization_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("พอลิเมอร์ใด"):
            assert kinds[_answer(q)] == s.split("พอลิเมอร์")[-1], s
        q = generate("chem.polymerization_application", Random(seed))
        s = _stem(q)
        if "กี่โมเลกุล" in s:
            polymer = s.split("สายหนึ่ง")[0]
            (total,) = _q(rf"มวลโมเลกุล {N} ถ้า", s)
            assert _ans(q) == total / mass[polymer], s


# ── Slices 29-30: เคมีเพิ่มเติม 1 ม.6/12, /14, /15; เคมีเพิ่มเติม 2 ม.4/1-/4 ──────────────

def test_plastics_and_shape_answers():
    from otk.sets.chemistry.m6.polymer_modify import MODIFICATIONS
    from otk.sets.chemistry.m6.polymer_structure import (
        PLASTICS,
        SHAPE_EXAMPLES,
        SHAPE_PROPERTIES,
        SHAPES,
    )
    assert set(SHAPE_PROPERTIES) == set(SHAPES) and len(SHAPES) == 3
    assert [p[0] for p in PLASTICS] == [1, 2, 3, 4, 5, 6]
    by_code = {p[0]: p for p in PLASTICS}
    shape_of = dict(SHAPE_EXAMPLES)
    effect = dict(MODIFICATIONS)
    for seed in range(SEEDS):
        q = generate("chem.polymer_structure_fluency", Random(seed))
        s = _stem(q)
        if "หมายเลข" in s and s.startswith("ผลิตภัณฑ์"):
            (code,) = _q(r"หมายเลข (\d+)", s)
            assert _answer(q) == by_code[int(code)][1], s
        elif "รหัสรีไซเคิลหมายเลขใด" in s:
            name = s.split(" ที่ใช้ทำ")[0]
            assert _ans(q) == next(p[0] for p in PLASTICS if p[1] == name), s
        q = generate("chem.polymer_structure_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("พอลิเมอร์ใดมีโครงสร้าง"):
            assert shape_of[_answer(q)] == s.split("มีโครงสร้าง")[1], s
        elif s.endswith("มีสมบัติตามข้อใด"):
            shape = s.split("พอลิเมอร์")[1].split("มีสมบัติ")[0]
            assert _answer(q) == SHAPE_PROPERTIES[shape], s
        q = generate("chem.polymer_modify_foundation", Random(seed))
        s = _stem(q)
        if s.endswith("ทำให้พอลิเมอร์เปลี่ยนไปอย่างไร"):
            assert _answer(q) == effect[s.split(" ทำให้พอลิเมอร์")[0]], s
        else:
            assert effect[_answer(q)] in s, s
        q = generate("chem.polymer_modify_fluency", Random(seed))
        s = _stem(q)
        if "วัลคาไนซ์" in s:
            rubber, percent = _q(rf"ยาง {N} กรัม โดยใช้กำมะถัน {N}%", s)
            assert _ans(q) == rubber * percent / 100, s
        else:
            styrene, butadiene = _q(rf"มวล 104\) {N} หน่วย และหน่วยบิวทาไดอีน \(C₄H₆ มวล 54\) {N} หน่วย", s)
            assert _ans(q) == styrene * 104 + butadiene * 54, s
        q = generate("chem.polymer_waste_fluency", Random(seed))
        s = _stem(q)
        if "ขวด PET" in s:
            grams, bottles, percent = _q(rf"ใบละ {N} กรัม จำนวน {N} ใบ .*ได้เส้นใย {N}%", s)
            assert _ans(q) == grams * bottles * percent / 100 / 1000, s
        elif "ถุงพลาสติก" in s:
            people, bags, days = _q(rf"มี {N} คน ใช้ถุงพลาสติกคนละ {N} ใบต่อวัน .* ใน {N} วัน", s)
            assert _ans(q) == people * bags * days, s
        else:
            (grams,) = _q(rf"เผา PVC {N} กรัม", s)
            assert _ans(q) == grams / Fraction(125, 2), s


def test_equations_balance_and_stoichiometry_recomputes():
    from otk.sets._support.science_wave_f30 import (
        EQUATIONS,
        atoms,
        equation_text,
        mass_of,
        species,
    )
    for eq in EQUATIONS:
        left, right = {}, {}
        for side, count in ((eq[0], left), (eq[1], right)):
            for c, f, _ in side:
                for k, v in atoms(f):
                    count[k] = count.get(k, 0) + c * v
        assert left == right, equation_text(eq)
    assert mass_of("Pb(NO₃)₂") == 331 and mass_of("AgCl") == Fraction(287, 2) and mass_of("KClO₃") == Fraction(245, 2)
    by_text = {equation_text(eq): eq for eq in EQUATIONS}
    coef = lambda eq, f: next(c for c, x, _ in species(eq) if x == f)

    def eq_of(s):
        return next(eq for text, eq in by_text.items() if f"สมการ {text} " in s or f"ปฏิกิริยา {text} " in s)

    for seed in range(SEEDS):
        q = generate("chem.equation_balance_fluency", Random(seed))
        s = _stem(q)
        eq = next(e for e in EQUATIONS if equation_text(e, blanks=True) in s)
        if "ผลรวม" in s:
            assert _ans(q) == sum(c for c, _, _ in species(eq)), s
        else:
            formula = re.search(r"สัมประสิทธิ์ของ (\S+) เท่าใด", s).group(1)
            assert _ans(q) == coef(eq, formula), s
        q = generate("chem.equation_balance_application", Random(seed))
        assert _answer(q) in by_text
        q = generate("chem.stoich_mass_foundation", Random(seed))
        s = _stem(q)
        eq = eq_of(s)
        a, n_a, b = re.search(rf"ถ้า (\S+) \S+ {N} โมล (\S+) จะ", s).groups()
        assert _ans(q) == Fraction(n_a) * coef(eq, b) / coef(eq, a), s
        q = generate("chem.stoich_mass_fluency", Random(seed))
        s = _stem(q)
        eq = eq_of(s)
        a, m_a, b = re.search(rf"ถ้า (\S+) \S+ {N} กรัม (\S+) จะ", s).groups()
        n_a = Fraction(m_a.replace(",", "")) / mass_of(a)
        assert _ans(q) == n_a * coef(eq, b) / coef(eq, a) * mass_of(b), s
        q = generate("chem.stoich_solution_fluency", Random(seed))
        s = _stem(q)
        eq = eq_of(s)
        a, ca, va, b = re.search(rf"สารละลาย (\S+) {N} mol/dm³ ปริมาตร {N} cm³ ทำปฏิกิริยาพอดีกับสารละลาย (\S+) ", s).groups()
        moles_b = Fraction(ca) * Fraction(va) / 1000 * coef(eq, b) / coef(eq, a)
        if s.endswith("กี่ cm³"):
            (cb,) = _q(rf"{re.escape(b)} {N} mol/dm³ กี่ cm³", s)
            assert _ans(q) == moles_b / cb * 1000, s
        else:
            (vb,) = _q(rf"{re.escape(b)} {N} cm³ สารละลาย", s)
            assert _ans(q) == moles_b / vb * 1000, s
        q = generate("chem.stoich_solution_application", Random(seed))
        s = _stem(q)
        eq = eq_of(s)
        reagent, c, v, solid = re.search(rf"เติมสารละลาย (\S+) {N} mol/dm³ ปริมาตร {N} cm³ .*ได้ตะกอน (\S+) กี่กรัม", s).groups()
        assert _ans(q) == Fraction(c) * Fraction(v) / 1000 * coef(eq, solid) / coef(eq, reagent) * mass_of(solid), s
        q = generate("chem.stoich_gas_fluency", Random(seed))
        s = _stem(q)
        eq = eq_of(s)
        if "จะเกิดแก๊ส" in s:
            solid, grams, gas = re.search(rf"ใช้ (\S+) {N} กรัม จะเกิดแก๊ส (\S+) ", s).groups()
            moles = Fraction(grams.replace(",", "")) / mass_of(solid)
            assert _ans(q) == moles * coef(eq, gas) / coef(eq, solid) * Fraction(224, 10), s
        else:
            gas, volume, solid = re.search(rf"ต้องการแก๊ส (\S+) {N} dm³ ที่ STP ต้องใช้ (\S+) กี่กรัม", s).groups()
            moles = Fraction(volume.replace(",", "")) / Fraction(224, 10)
            assert _ans(q) == moles * coef(eq, solid) / coef(eq, gas) * mass_of(solid), s
        q = generate("chem.stoich_gas_application", Random(seed))
        s = _stem(q)
        eq = next(e for e in EQUATIONS if equation_text(e, states=True) in s)
        a, va, b = re.search(rf"แก๊ส (\S+) \S+ {N} cm³ แก๊ส (\S+) จะ", s).groups()
        assert _ans(q) == Fraction(va) * coef(eq, b) / coef(eq, a), s


# ── Slices 31-32: เคมีเพิ่มเติม 2 ม.4/5-/7, ม.5/2, /3, /5, /6 ───────────────────────────

def test_multistep_limiting_and_yield_recompute():
    from otk.sets._support.science_wave_f30 import EQUATIONS, atoms, equation_text, mass_of
    from otk.sets.chemistry.m4.stoich_multistep import CHAINS, chain_ratio, coef
    from otk.sets.chemistry.m4.limiting_reagent import TWO_REACTANTS
    for chain in CHAINS:
        for eq in chain[2]:
            left, right = {}, {}
            for side, count in ((eq[0], left), (eq[1], right)):
                for c, f, _ in side:
                    for k, v in atoms(f):
                        count[k] = count.get(k, 0) + c * v
            assert left == right, equation_text(eq)
    by_start = {(c[0], c[1]): c for c in CHAINS}
    for seed in range(SEEDS):
        q = generate("chem.stoich_multistep_foundation", Random(seed))
        s = _stem(q)
        start, n, end = re.search(rf"เริ่มจาก (\S+) {N} โมล .* จะได้ (\S+) กี่โมล", s).groups()
        assert _ans(q) == Fraction(n) * chain_ratio(by_start[(start, end)]), s
        q = generate("chem.stoich_multistep_fluency", Random(seed))
        s = _stem(q)
        chain = next(c for c in CHAINS if f"{c[0]} = " in s and f"{c[1]} = " in s and all(equation_text(e) in s for e in c[2]))
        if "ต้องการ" not in s:
            (m,) = _q(rf"เริ่มจาก \S+ {N} กรัม", s)
            assert _ans(q) == m / mass_of(chain[0]) * chain_ratio(chain) * mass_of(chain[1]), s
        else:
            (m,) = _q(rf"ต้องการ \S+ {N} กรัม", s)
            assert _ans(q) == m / mass_of(chain[1]) / chain_ratio(chain) * mass_of(chain[0]), s
        for key in ("chem.limiting_reagent_foundation", "chem.limiting_reagent_fluency", "chem.limiting_reagent_application"):
            q = generate(key, Random(seed))
            s = _stem(q)
            a, x, unit, b, y = re.search(rf"ผสม (\S+) {N} (กรัม|โมล) กับ (\S+) {N} ", s).groups()
            eq = next(e for e in TWO_REACTANTS if f"ตามสมการ {equation_text(e)}" in s)
            x, y = Fraction(x.replace(",", "")), Fraction(y.replace(",", ""))
            na, nb = (x / mass_of(a), y / mass_of(b)) if unit == "กรัม" else (x, y)
            runs = min(na / coef(eq, a), nb / coef(eq, b))
            limiting = a if na / coef(eq, a) < nb / coef(eq, b) else b
            if key.endswith("foundation"):
                assert _answer(q) == f"{limiting} เพราะหมดก่อน", s
            elif key.endswith("fluency"):
                product = re.search(r"จะได้ (\S+) มากที่สุด", s).group(1)
                amount = runs * coef(eq, product)
                assert _ans(q) == (amount * mass_of(product) if unit == "กรัม" else amount), s
            else:
                excess = b if limiting == a else a
                left = (nb if excess == b else na) - runs * coef(eq, excess)
                assert _ans(q) == (left * mass_of(excess) if unit == "กรัม" else left), s
        q = generate("chem.percent_yield_fluency", Random(seed))
        s = _stem(q)
        reactant, m_r, product, actual = re.search(rf"ใช้ (\S+) {N} กรัม .* ได้ (\S+) จริง {N} กรัม", s).groups()
        eq = next(e for e in EQUATIONS if f"ตามสมการ {equation_text(e)} " in s)
        theory = Fraction(m_r.replace(",", "")) / mass_of(reactant) * coef(eq, product) / coef(eq, reactant) * mass_of(product)
        assert _ans(q) == Fraction(actual.replace(",", "")) / theory * 100, s


def test_rate_answers_recompute():
    from otk.sets.chemistry.m5.rate_compare import FACTORS
    from otk.sets.chemistry.m5.rate_calc import RATE_EQUATIONS
    coefs = {eq: c for eq, c, _ in RATE_EQUATIONS}
    for seed in range(SEEDS):
        q = generate("chem.rate_calc_foundation", Random(seed))
        s = _stem(q)
        t1, a1, t2, a2 = _q(rf"ที่เวลา {N} s ได้ {N} \S+ ที่เวลา {N} s ได้ {N}", s)
        assert _ans(q) == (a2 - a1) / (t2 - t1), s
        q = generate("chem.rate_calc_fluency", Random(seed))
        s = _stem(q)
        eq = next(e for e in coefs if f"ปฏิกิริยา {e} " in s)
        a, rate, b = re.search(rf"ถ้า (\S+) \S+ด้วยอัตรา {N} mol/dm³·s (\S+) จะ", s).groups()
        assert _ans(q) == Fraction(rate) * coefs[eq][b] / coefs[eq][a], s
        q = generate("chem.rate_calc_application", Random(seed))
        s = _stem(q)
        if "กี่ mol/dm³" in s:
            eq = next(e for e in coefs if f"ปฏิกิริยา {e} " in s)
            a, change, b = re.search(rf"ความเข้มข้นของ (\S+) \S+ {N} mol/dm³ ในช่วงเดียวกันความเข้มข้นของ (\S+) ", s).groups()
            assert _ans(q) == Fraction(change) * coefs[eq][b] / coefs[eq][a], s
        q = generate("chem.collision_theory_fluency", Random(seed))
        s = _stem(q)
        r, peak, p = _q(rf"สารตั้งต้นมีพลังงาน {N} kJ ยอดของกราฟ \(สารเชิงซ้อนกัมมันต์\) {N} kJ ผลิตภัณฑ์ {N} kJ", s)
        if "ย้อนกลับ" in s:
            assert _ans(q) == peak - p, s
        elif "ΔH" in s:
            assert _ans(q) == p - r, s
        else:
            assert _ans(q) == peak - r, s
        q = generate("chem.collision_theory_foundation", Random(seed))
        s = _stem(q)
        if "ชนกันด้วยพลังงาน" in s:
            ea, energy = _q(rf"ก่อกัมมันต์ {N} kJ/mol อนุภาคคู่หนึ่งชนกันด้วยพลังงาน {N}", s)
            reacts = energy >= ea and "ไม่เหมาะสม" not in s
            assert _answer(q).startswith("เกิด" if reacts else "ไม่เกิด"), s
        q = generate("chem.rate_compare_application", Random(seed))
        s = _stem(q)
        if "จะใช้เวลา" in s:
            t1, time1, t2 = _q(rf"ที่ {N} °C ใช้เวลา {N} s .* ที่ {N} °C จะใช้เวลา", s)
            assert _ans(q) == time1 / Fraction(2) ** int((t2 - t1) / 10), s
        else:
            t1, t2 = _q(rf"จาก {N} °C เป็น {N} °C", s)
            assert _ans(q) == 2 ** int((t2 - t1) / 10), s
        q = generate("chem.rate_compare_fluency", Random(seed))
        s = _stem(q)
        runs = dict(re.findall(r"(\S): (Mg \S+ HCl \S+ mol/dm³ ที่ \S+ °C)", s))
        rank = lambda text: sum(opts.index(next(o for o in opts if o and o in text)) for _, opts in FACTORS[:3])
        order = _answer(q).split(" > ")
        assert [rank(runs[ell]) for ell in order] == sorted((rank(runs[ell]) for ell in order), reverse=True), s


# ── Slices 33-34: เคมีเพิ่มเติม 2 ม.5/1, /7-/12 ─────────────────────────────────────

def _table(s: str, pattern: str) -> list[tuple[Fraction, Fraction]]:
    return [(Fraction(t), Fraction(v.replace(",", ""))) for t, v in re.findall(pattern, s)]


def test_rate_graph_and_approach_tables():
    for seed in range(SEEDS):
        q = generate("chem.rate_graph_fluency", Random(seed))
        s = _stem(q)
        rows = _table(s, rf"(\d+) s: {N} cm³")
        if "ทั้งหมดกี่" in s:
            assert _ans(q) == rows[-1][1], s
        elif "สิ้นสุด" in s:
            assert _ans(q) == next(t for t, v in rows if v == rows[-1][1]), s
        else:
            rises = [(rows[i + 1][1] - rows[i][1], i) for i in range(len(rows) - 1)]
            best = max(rises)[1]
            assert _answer(q) == f"{rows[best][0]}-{rows[best + 1][0]} s", s
        q = generate("chem.rate_graph_application", Random(seed))
        s = _stem(q)
        rows = dict(_table(s, rf"(\d+) s: {N} cm³"))
        t1, t2 = _q(r"ช่วง (\d+)-(\d+) s", s)
        assert _ans(q) == (rows[t2] - rows[t1]) / (t2 - t1), s
        q = generate("chem.reversible_equilibrium_application", Random(seed))
        s = _stem(q)
        rows = [(Fraction(t), Fraction(a), Fraction(b)) for t, a, b in
                re.findall(r"(\d+) s: \[A\] = ([\d.]+), \[B\] = ([\d.]+)", s)]
        final = rows[-1][1:]
        assert _answer(q) == f"{next(t for t, a, b in rows if (a, b) == final)} s", s
        q = generate("chem.equilibrium_approach_application", Random(seed))
        s = _stem(q)
        rows = [Fraction(a) for a in re.findall(r"\[A\] = ([\d.]+)", s)]
        if "ร้อยละ" in s:
            assert _ans(q) == (rows[0] - rows[-1]) / rows[0] * 100, s
        else:
            assert _ans(q) == rows[0] - rows[-1], s


def test_equilibrium_constants_recompute():
    from otk.sets._support.science_wave_f34 import K_SYSTEMS, counted, k_value
    from otk.sets.chemistry.m5.equilibrium_constant import k_expression
    by_eq = {s[0]: s for s in K_SYSTEMS}
    assert k_expression(by_eq["CaCO₃(s) ⇌ CaO(s) + CO₂(g)"]) == "[CO₂]"
    assert k_expression(by_eq["N₂(g) + 3H₂(g) ⇌ 2NH₃(g)"]) == "[NH₃]² / [N₂][H₂]³"

    def system_of(s):
        return next(sys for eq, sys in by_eq.items() if f"ปฏิกิริยา {eq} " in s or f"ของ {eq} " in s)

    for seed in range(SEEDS):
        q = generate("chem.equilibrium_constant_fluency", Random(seed))
        s = _stem(q)
        system = system_of(s)
        conc = {f: Fraction(v) for f, v in re.findall(r"\[(\S+?)\] = ([\d.]+)", s)}
        assert _ans(q) == k_value(system, conc), s
        q = generate("chem.equilibrium_constant_foundation", Random(seed))
        s = _stem(q)
        system = system_of(s)
        if "นิพจน์ค่าคงที่สมดุล K ตามข้อใด" in s:
            assert _answer(q) == f"K = {k_expression(system)}", s
        elif "ไม่ปรากฏ" in s:
            f = _answer(q).split(" ")[0]
            assert f not in {x[0] for x in counted(system[1]) + counted(system[2])}, s
        q = generate("chem.equilibrium_constant_application", Random(seed))
        s = _stem(q)
        if "ในภาชนะปริมาตร" in s:
            system = system_of(s)
            (volume,) = _q(r"ปริมาตร (\d+) dm³", s)
            conc = {f: Fraction(v) / volume for f, v in re.findall(r"(\S+) ([\d.]+) mol", s)}
            assert _ans(q) == k_value(system, conc), s
        q = generate("chem.equilibrium_concentration_foundation", Random(seed))
        s = _stem(q)
        system = system_of(s)
        (k,) = _q(rf"K = {N} ", s)
        known = {f: Fraction(v) for f, v in re.findall(r"\[(\S+?)\] = ([\d.]+)", s)}
        hidden = re.search(r"\[(\S+?)\] ที่ภาวะสมดุลเท่าใด", s).group(1)
        assert k_value(system, {**known, hidden: _ans(q)}) == k, s


def test_multistep_k_and_le_chatelier():
    from otk.sets.chemistry.m5.le_chatelier import (
        CHANGES,
        LEFT,
        NONE,
        RIGHT,
        SHIFT_SYSTEMS,
        change_text,
        shift,
    )
    by_eq = {s[0]: s for s in SHIFT_SYSTEMS}
    haber = by_eq["N₂(g) + 3H₂(g) ⇌ 2NH₃(g)"]
    assert shift(haber, "pressure_up") == RIGHT and shift(haber, "heat") == LEFT and shift(haber, "catalyst") == NONE
    lime = by_eq["CaCO₃(s) ⇌ CaO(s) + CO₂(g)"]
    assert shift(lime, "add_reactant") == NONE and shift(lime, "heat") == RIGHT and shift(lime, "pressure_up") == LEFT
    assert shift(by_eq["H₂(g) + I₂(g) ⇌ 2HI(g)"], "pressure_up") == NONE
    for seed in range(SEEDS):
        q = generate("chem.equilibrium_multistep_fluency", Random(seed))
        s = _stem(q)
        k1, k2 = _q(rf"K₁ = {N} .* K₂ = {N} ", s)
        assert _ans(q) == k1 * k2, s
        q = generate("chem.equilibrium_multistep_application", Random(seed))
        s = _stem(q)
        if "ที่กลับทิศ" in s:
            k1, k2 = _q(rf"K₁ = {N} .* K₂ = {N} ", s)
            assert _ans(q) == k1 / k2, s
        else:
            k, k1 = _q(rf"มี K = {N} .* K₁ = {N} ", s)
            assert _ans(q) == k / k1, s
        q = generate("chem.le_chatelier_foundation", Random(seed))
        s = _stem(q)
        system = next(v for eq, v in by_eq.items() if eq in s)
        text = s.split("ถ้า")[1].split(" ภาวะสมดุลจะ")[0]
        change = next(c for c in CHANGES if change_text(system, c) == text)
        assert _answer(q) == shift(system, change), s


# ── Slices 35-36: เคมีเพิ่มเติม 2 ม.5/13-/19 ─────────────────────────────────────────

def _sci(text: str) -> Fraction:
    """'2.5 × 10⁻³' or a plain decimal back to a number."""
    sup = str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")
    if "×" in text:
        mantissa, power = text.split(" × 10")
        return Fraction(mantissa) * Fraction(10) ** int(power.translate(sup))
    return Fraction(text)


SCI = r"([\d.]+(?: × 10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)"


def test_acid_base_pairs_and_theories():
    from otk.sets.chemistry.m5.conjugate_pair import AMPHIPROTIC, CONJ_ACID, CONJ_BASE
    from otk.sets._support.science_wave_f35 import BL_REACTIONS
    from otk.sets.chemistry.m5.acid_base_theory import LEWIS
    for eq, acid, base, conj_acid, conj_base in BL_REACTIONS:
        # The acid loses the proton the base gains, on the right-hand side.
        assert CONJ_BASE[acid] == conj_base and CONJ_ACID[base] == conj_acid, eq
    assert {"H₂O", "HCO₃⁻", "HSO₄⁻", "H₂PO₄⁻"} <= set(AMPHIPROTIC)
    by_eq = {r[0]: r for r in BL_REACTIONS}
    for seed in range(SEEDS):
        q = generate("chem.acid_base_theory_fluency", Random(seed))
        s = _stem(q)
        r = next(v for k, v in by_eq.items() if f" {k} " in s)
        assert _answer(q) == (r[1] if "เป็นกรด" in s else r[2]), s
        q = generate("chem.conjugate_pair_foundation", Random(seed))
        s = _stem(q)
        x = s.split("ของ ")[1].split(" ")[0]
        assert _answer(q) == (CONJ_BASE[x] if s.startswith("คู่เบส") else CONJ_ACID[x]), s
        q = generate("chem.conjugate_pair_application", Random(seed))
        s = _stem(q)
        if s.startswith("สารใด"):
            assert _answer(q) in AMPHIPROTIC, s
        q = generate("chem.acid_base_theory_application", Random(seed))
        s = _stem(q)
        if "ทฤษฎีของลิวอิส" in s:
            eq, acid, base = next(ell for ell in LEWIS if ell[0] in s)
            assert _answer(q).split(" ")[0] == (acid if "เป็นกรด" in s else base), s


def test_ph_and_strength_recompute():
    from otk.sets._support.science_wave_f36 import LOGS

    def ph(conc: Fraction) -> Fraction:
        power = 0
        while conc < 1:
            conc *= 10
            power += 1
        return power - LOGS[int(conc)]

    for seed in range(SEEDS):
        q = generate("chem.ph_calc_foundation", Random(seed))
        s = _stem(q)
        conc = _sci(re.search(rf"\] = {SCI} mol", s).group(1))
        assert _ans(q) == (ph(conc) if "[H₃O⁺]" in s else 14 - ph(conc)), s
        q = generate("chem.ph_calc_fluency", Random(seed))
        s = _stem(q)
        name = s.split(" ")[1]
        c = _sci(re.search(rf"เข้มข้น {SCI} mol", s).group(1))
        per = 2 if name in ("H₂SO₄", "Ca(OH)₂", "Ba(OH)₂") else 1
        base = "OH" in name
        assert _ans(q) == (14 - ph(c * per) if base else ph(c * per)), s
        q = generate("chem.acid_strength_fluency", Random(seed))
        s = _stem(q)
        (c,) = _q(rf"เข้มข้น {N} mol", s)
        if "ร้อยละเท่าใด" in s:
            h = _sci(re.search(rf"\[H₃O⁺\] = {SCI} mol", s).group(1))
            assert _ans(q) == h / c * 100, s
        else:
            p, power = re.search(rf"แตกตัวได้ {N}% .* a × 10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)", s).groups()
            exponent = int(power.translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")))
            assert _ans(q) * Fraction(10) ** exponent == c * Fraction(p) / 100, s
        q = generate("chem.neutralization_application", Random(seed))
        s = _stem(q)
        ca, va, cb, vb = _q(rf"HCl {N} mol/dm³ ปริมาตร {N} cm³ กับ NaOH {N} mol/dm³ ปริมาตร {N} cm³", s)
        excess = ca * va - cb * vb
        value = ph(abs(excess) / (va + vb))
        assert _ans(q) == (value if excess > 0 else 14 - value), s
        q = generate("chem.neutralization_fluency", Random(seed))
        s = _stem(q)
        ca, va, cb, vb = _q(rf"{N} mol/dm³ ปริมาตร {N} cm³ กับ \S+ {N} mol/dm³ ปริมาตร {N} cm³", s)
        if ca * va != cb * vb:
            assert _answer(q) == ("เป็นกรด" if ca * va > cb * vb else "เป็นเบส"), s


def test_salt_hydrolysis_follows_parent_strength():
    from otk.sets.chemistry.m5.salt_hydrolysis import SALTS
    from otk.sets.chemistry.m5.acid_strength import STRONG_ACIDS, STRONG_BASES
    for salt, acid, base, nature, equation in SALTS:
        strong_a, strong_b = acid in STRONG_ACIDS, base in STRONG_BASES
        expected = "เป็นกลาง" if strong_a and strong_b else "เป็นเบส" if strong_b else "เป็นกรด"
        assert nature == expected, salt
        assert (equation is None) == (strong_a and strong_b), salt
        if equation:
            assert equation.endswith("OH⁻") == (nature == "เป็นเบส"), salt


# ── Slices 37-38: เคมีเพิ่มเติม 2 ม.5/20-/26 ─────────────────────────────────────────

def test_titration_and_buffer_answers():
    from otk.sets.chemistry.m5.titration_indicator import INDICATORS, TITRATIONS
    from otk.sets.chemistry.m5.titration_calc import PAIRS
    per_h = {a: n for a, n, _, _ in PAIRS}
    per_oh = {b: n for _, _, b, n in PAIRS}
    for _, _, eq_ph, best in TITRATIONS:
        _, low, high, _, _ = next(i for i in INDICATORS if i[0] == best)
        assert low <= eq_ph <= high, best
    for seed in range(SEEDS):
        q = generate("chem.titration_calc_foundation", Random(seed))
        s = _stem(q)
        acid, ca, va, base, cb = re.search(rf"ไทเทรต (\S+) {N} mol/dm³ ปริมาตร {N} cm³ ด้วย (\S+) {N} mol/dm³", s).groups()
        assert _ans(q) == Fraction(ca) * Fraction(va) * per_h[acid] / (Fraction(cb) * per_oh[base]), s
        q = generate("chem.titration_calc_application", Random(seed))
        s = _stem(q)
        sample, cb, vb = _q(rf"น้ำส้มสายชู {N} cm³ ด้วย NaOH {N} mol/dm³ ใช้ไป {N} cm³", s)
        grams = cb * vb / 1000 * 60
        assert _ans(q) == (grams if "กี่กรัม" in s else grams / sample * 100), s
        q = generate("chem.titration_indicator_fluency", Random(seed))
        s = _stem(q)
        if "ควรใช้อินดิเคเตอร์ใด" in s and "pH ที่จุดสมมูลเท่ากับ" in s:
            (point,) = _q(rf"จุดสมมูลเท่ากับ {N} ", s)
            _, low, high, _, _ = next(i for i in INDICATORS if i[0] == _answer(q))
            assert low <= point <= high, s
        q = generate("chem.buffer_application", Random(seed))
        s = _stem(q)
        acid, salt = _q(rf"กรดอ่อน \S+ {N} mol/dm³ กับเกลือ \S+ {N} mol/dm³", s)
        mantissa, power = re.search(r"Ka ของ \S+ = ([\d.]+) × 10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)", s).groups()
        ka = Fraction(mantissa) * Fraction(10) ** int(power.translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")))
        h = ka * acid / salt
        exponent = 0
        while h < 1:
            h *= 10
            exponent += 1
        logs = {1: 0, 2: Fraction(30, 100), 4: Fraction(60, 100), 5: Fraction(70, 100), 8: Fraction(90, 100)}
        assert _ans(q) == exponent - logs[int(h)], s


def test_oxidation_numbers_and_electrons():
    from otk.sets.chemistry.m5.redox_series import METALS, displaces
    from otk.sets.chemistry.m5.redox_agent import REDOX, coefficient, electrons_per_unit
    from otk.sets.chemistry.m5.oxidation_number import SPECIES
    from otk.sets._support.science_wave_f38 import oxidation_number
    for formula, element, value in SPECIES:
        assert oxidation_number(formula, element) == value, formula
    for eq, reducer, oxidiser, ox, red in REDOX:
        left = eq.split(" → ")[0]
        gained = int(re.search(r"(\d*)e⁻", red).group(1) or 1)
        taken = Fraction(gained, coefficient(red.split(" → ")[0], oxidiser))
        # Electrons given by the reducers equal electrons taken by the oxidisers.
        assert electrons_per_unit(ox, reducer) * coefficient(left, reducer) == taken * coefficient(left, oxidiser), eq
    by_eq = {r[0]: r for r in REDOX}
    for seed in range(SEEDS):
        q = generate("chem.redox_agent_foundation", Random(seed))
        s = _stem(q)
        r = by_eq[s.split("ในปฏิกิริยา ")[1].split(" สารใด")[0]]
        assert _answer(q) == (r[1] if "ตัวรีดิวซ์" in s else r[2]), s
        q = generate("chem.redox_series_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("จุ่มแผ่น"):
            metal, ion = re.search(r"จุ่มแผ่น (\S+) ลงในสารละลายที่มี (\S+) ", s).groups()
            other = next(m for m in METALS if ion.startswith(m))
            assert _answer(q).startswith("เกิด" if displaces(metal, other) else "ไม่เกิด"), s
        q = generate("chem.redox_series_fluency", Random(seed))
        s = _stem(q)
        beats = {tuple(x) for x in re.findall(r"(\S) ในสารละลายไอออนของ (\S): มีโลหะมาเกาะ", s)}
        order = _answer(q).split(" > ")
        assert (order[0], order[1]) in beats and (order[1], order[2]) in beats, s


# ── Slices 39-40: เคมีเพิ่มเติม 2 ม.5/27-/32, เคมีเพิ่มเติม 3 ม.4/1 ────────────────────────

def _atoms_and_charge(species: str) -> tuple[dict, int]:
    from otk.sets._support.science_wave_f38 import parse
    if species == "e⁻":
        return {}, -1
    return parse(species)


def _balanced(left, right) -> bool:
    def total(side):
        atoms, charge = {}, 0
        for coef, species in side:
            a, c = _atoms_and_charge(species)
            for k, v in a.items():
                atoms[k] = atoms.get(k, 0) + coef * v
            charge += coef * c
        return atoms, charge
    return total(left) == total(right)


def _side(text: str):
    out = []
    for part in text.split(" + "):
        m = re.fullmatch(r"(\d*)(.+)", part.strip())
        out.append((int(m.group(1) or 1), m.group(2)))
    return out


def test_redox_equations_and_halves_balance():
    from otk.sets.chemistry.m5.redox_balance import (
        HALVES,
        REDOX_EQUATIONS,
        electrons_moved,
        equation_text,
    )
    for eq in REDOX_EQUATIONS:
        assert _balanced(eq[0], eq[1]), equation_text(eq)
    for half, electrons, protons, water in HALVES:
        left, right = half.split(" → ")
        assert _balanced(_side(left), _side(right)), half
        assert f"{electrons if electrons > 1 else ''}e⁻" in half, half
    by_text = {equation_text(eq): eq for eq in REDOX_EQUATIONS}
    for seed in range(SEEDS):
        q = generate("chem.redox_balance_fluency", Random(seed))
        s = _stem(q)
        eq = next(e for e in REDOX_EQUATIONS if equation_text(e, blanks=True) in s)
        species = re.search(r"สัมประสิทธิ์ของ (\S+) เท่าใด", s).group(1)
        assert _ans(q) == dict((sp, c) for c, sp in [*eq[0], *eq[1]])[species], s
        q = generate("chem.redox_balance_application", Random(seed))
        s = _stem(q)
        if "ข้อใดดุลแล้ว" in s:
            assert _answer(q) in by_text, s
        elif "ถ่ายโอนอิเล็กตรอน" in s:
            eq = next(e for t, e in by_text.items() if f"สมการ {t} " in s)
            assert _ans(q) == electrons_moved(eq), s


def test_cell_potentials_recompute():
    from otk.sets._support.science_wave_f39 import COUPLES
    e0 = {ion: e for _, ion, e in COUPLES}
    for seed in range(SEEDS):
        for key in ("chem.cell_potential_foundation", "chem.cell_potential_fluency"):
            q = generate(key, Random(seed))
            s = _stem(q)
            if "E°cell เท่าใด" not in s:
                continue
            left, right = re.search(r"\| (\S+)\(aq\) \|\| (\S+)\(aq\)", s).groups()
            assert _ans(q) == e0[right] - e0[left], s
        q = generate("chem.electrochemical_cell_foundation", Random(seed))
        s = _stem(q)
        if "ข้อใดถูกต้อง" in s:
            ions = re.findall(r"E° ของ (\S+)/\S+ = ", s) + re.findall(r", (\S+)/\S+ = ", s)
            low = min(ions, key=e0.get)
            assert _answer(q).startswith(next(m for m, ion, _ in COUPLES if ion == low) + " เป็นแอโนด"), s


def test_electrochemistry_and_safety_tables():
    from otk.sets.chemistry.m5.battery_type import CELLS, PRIMARY, SECONDARY
    from otk.sets.chemistry.m5.electrolysis import ELECTROLYSES
    assert {c[1] for c in CELLS} == {PRIMARY, SECONDARY}
    for what, cathode, anode in ELECTROLYSES:
        # Reduction products at the cathode are metals or hydrogen; oxidation products are chlorine or oxygen.
        assert cathode.startswith("โลหะ") or "H₂" in cathode, what
        assert "Cl₂" in anode or "O₂" in anode, what
    for seed in range(SEEDS):
        q = generate("chem.electrolysis_foundation", Random(seed))
        s = _stem(q)
        assert "ต่อขั้วลบเป็นแคโทด" in _answer(q).split(" แท่ง")[0], s


# ── Slices 41-42: เคมีเพิ่มเติม 3 ม.4/2, /4-/9 ──────────────────────────────────────

def test_units_atomic_mass_and_moles_recompute():
    from otk.sets._support.science_wave_f30 import ATOMIC, atoms, mass_of
    from otk.sets.chemistry.m4.unit_conversion import CONVERSIONS
    factor = {(a, b): f for a, b, f, _ in CONVERSIONS}
    for seed in range(SEEDS):
        q = generate("chem.unit_conversion_fluency", Random(seed))
        s = _stem(q)
        value, src, dst = re.match(rf"{N} (\S+) เท่ากับกี่ (\S+)$", s).groups()
        assert _ans(q) == Fraction(value.replace(",", "")) * factor[(src, dst)], s
        q = generate("chem.atomic_mass_fluency", Random(seed))
        s = _stem(q)
        if "มวลอะตอมเฉลี่ยเท่าใด" in s:
            m1, p1, m2, p2 = _q(r"-(\d+) ร้อยละ (\d+) และ \S+-(\d+) ร้อยละ (\d+)", s)
            assert _ans(q) == (m1 * p1 + m2 * p2) / 100, s
        else:
            avg, m1, m2 = _q(rf"มวลอะตอมเฉลี่ย {N} ประกอบด้วยไอโซโทป \S+-(\d+) และ \S+-(\d+)", s)
            assert (m1 * _ans(q) + m2 * (100 - _ans(q))) / 100 == avg, s
        q = generate("chem.atomic_mass_application", Random(seed))
        s = _stem(q)
        formula = s.split(" ")[0]
        if "มีมวลของธาตุ" in s:
            element = re.search(r"มีมวลของธาตุ (\S+) รวม", s).group(1)
            assert _ans(q) == ATOMIC[element] * dict(atoms(formula))[element], s
        else:
            assert _ans(q) == mass_of(formula), s
        q = generate("chem.mole_relation_fluency", Random(seed))
        s = _stem(q)
        substance = s.split(" ")[0]
        amount = Fraction(s.split(" ")[1].replace(",", ""))
        assert _ans(q) == (amount / mass_of(substance) if "กรัม มีกี่โมล" in s else amount * mass_of(substance)), s


def test_formulas_ratios_and_concentrations_recompute():
    from otk.sets._support.science_wave_f30 import ATOMIC, atoms, mass_of
    from otk.sets.chemistry.m4.empirical_formula import EMPIRICAL, EXTRA_MASS, formula_of, reduce
    assert formula_of({"P": 4, "O": 10}) == "P₄O₁₀" and formula_of({"C": 6, "H": 12, "O": 6}) == "C₆H₁₂O₆"
    for empirical, molecules in EMPIRICAL:
        for molecule in molecules:
            assert reduce(molecule) == empirical, molecule
    for seed in range(SEEDS):
        q = generate("chem.definite_proportion_fluency", Random(seed))
        s = _stem(q)
        formula = s.split(" ")[0]
        if "อยู่ร้อยละโดยมวล" in s:
            element = re.search(r"มี (\S+) อยู่ร้อยละ", s).group(1)
            assert _ans(q) == ATOMIC[element] * dict(atoms(formula))[element] / mass_of(formula) * 100, s
        else:
            (sample,) = _q(rf"^\S+ {N} กรัม", s)
            element = re.search(r"มี (\S+) อยู่กี่กรัม", s).group(1)
            assert _ans(q) == sample * ATOMIC[element] * dict(atoms(formula))[element] / mass_of(formula), s
        q = generate("chem.empirical_formula_fluency", Random(seed))
        s = _stem(q)
        grams = {e: Fraction(g.replace(",", "")) for e, g in re.findall(rf"(\b[A-Z][a-z]?) {N} กรัม", s)}
        moles = {e: g / ATOMIC.get(e, EXTRA_MASS.get(e)) for e, g in grams.items()}
        low = min(moles.values())
        ratio = {e: m / low for e, m in moles.items()}
        k = 1
        while any((r * k).denominator != 1 for r in ratio.values()):
            k += 1
        assert _answer(q) == formula_of(reduce({e: int(r * k) for e, r in ratio.items()})), s
        q = generate("chem.solution_units_fluency", Random(seed))
        s = _stem(q)
        solute_g, molar, amount = _q(rf"ละลาย \S+ {N} กรัม \(มวลต่อโมล {N}\) ในน้ำ(?:จนได้สารละลาย)? {N}", s)
        assert _ans(q) == solute_g / molar / amount * 1000, s


# ── Slices 43-44: เคมีเพิ่มเติม 3 ม.4/10-/11, ชีววิทยาเพิ่มเติม 1 ม.4/1-/5 ─────────────────

def test_solution_prep_and_colligative_recompute():
    from otk.sets.chemistry.m4.colligative import SOLVENTS
    by_name = {s[0]: s for s in SOLVENTS}
    for seed in range(SEEDS):
        q = generate("chem.solution_prep_fluency", Random(seed))
        s = _stem(q)
        c, v, m = _q(rf"เข้มข้น {N} mol/dm³ ปริมาตร {N} cm³ .* \(มวลต่อโมล {N}\)", s)
        assert _ans(q) == c * v / 1000 * m, s
        q = generate("chem.solution_prep_application", Random(seed))
        s = _stem(q)
        if s.startswith("ต้องการ"):
            c2, v2, c1 = _q(rf"เข้มข้น {N} mol/dm³ ปริมาตร {N} cm³ จากสารละลายเข้มข้น {N} mol/dm³", s)
            assert _ans(q) == c2 * v2 / c1, s
        else:
            c1, v1, v2 = _q(rf"เข้มข้น {N} mol/dm³ มา {N} cm³ เติมน้ำจนได้ {N} cm³", s)
            assert _ans(q) == c1 * v1 / v2, s
        q = generate("chem.colligative_fluency", Random(seed))
        s = _stem(q)
        m, grams, solvent_g = _q(rf"\(มวลต่อโมล {N}\) {N} กรัม ใน\S+ {N} กรัม", s)
        solvent = by_name[re.search(r"กรัม ใน(\S+) \d", s).group(1)]
        molality = grams / m / solvent_g * 1000
        if "จุดเดือดกี่" in s:
            assert _ans(q) == solvent[1] + solvent[2] * molality, s
        else:
            assert _ans(q) == solvent[3] - solvent[4] * molality, s
        q = generate("chem.colligative_application", Random(seed))
        s = _stem(q)
        grams, solvent_g, t = _q(rf"สาร X {N} กรัม ใน\S+ {N} กรัม สารละลาย\S+ที่ {N} °C", s)
        solvent = by_name[re.search(r"กรัม ใน(\S+) \d", s).group(1)]
        change = (t - solvent[1]) / solvent[2] if "เดือด" in s.split("สารละลาย")[1][:6] else (solvent[3] - t) / solvent[4]
        assert _ans(q) == grams / (change * solvent_g / 1000), s


def test_biology_life_method_and_molecules():
    from otk.sets.biology.m4.life_property import LEVELS, LEVEL_EXAMPLES
    from otk.sets.biology.m4.carbohydrate import CARBS
    from otk.sets.biology.m4.scientific_method import EXPERIMENTS, ROLES
    level_of = dict(LEVEL_EXAMPLES)
    reducing = {c[0]: c[4] for c in CARBS}
    for seed in range(SEEDS):
        q = generate("biology.life_property_fluency", Random(seed))
        s = _stem(q)
        if s.startswith('"'):
            assert _answer(q) == level_of[s.split('"')[1]], s
        else:
            below = s.split('"')[1]
            assert LEVELS.index(_answer(q)) == LEVELS.index(below) + 1, s
        q = generate("biology.scientific_method_foundation", Random(seed))
        s = _stem(q)
        exp = next(e for e in EXPERIMENTS if f'"{e[0]}"' in s)
        role = s.split("ข้อใดเป็น")[1]
        assert _answer(q) == exp[ROLES[role]], s
        q = generate("biology.carbohydrate_application", Random(seed))
        s = _stem(q)
        if s.startswith("คาร์โบไฮเดรตใด"):
            assert reducing[_answer(q)] == ("ไม่ให้" not in s), s
        q = generate("biology.protein_fluency", Random(seed))
        s = _stem(q)
        if "สายพอลิเพปไทด์" in s:
            (n,) = _q(r"กรดอะมิโน (\d+) โมเลกุล", s)
            assert _ans(q) == n - 1, s
        elif "เรียงลำดับ" in s:
            (n,) = _q(r"กรดอะมิโน (\d+) หน่วย", s)
            assert _ans(q) == 20 ** n, s
        q = generate("biology.carbohydrate_fluency", Random(seed))
        s = _stem(q)
        if "กลูโคส" in s and "โมเลกุลเชื่อมกัน" in s:
            (n,) = _q(r"กลูโคส (\d+) โมเลกุล", s)
            assert _ans(q) == n - 1, s


# ── Slices 45-46: ชีววิทยาเพิ่มเติม 1 ม.4/6-/12 ─────────────────────────────────────

def test_nucleic_acids_enzymes_and_microscope_recompute():
    from otk.sets.biology.m4.nucleic_acid import PAIR, RNA_PAIR
    from otk.sets.biology.m4.enzyme import ENZYMES
    from otk.sets.biology.m4.organelle import ORGANELLES
    ph = {e[0]: e[3] for e in ENZYMES}
    membranes = {o[0]: o[2] for o in ORGANELLES}
    for seed in range(SEEDS):
        q = generate("biology.nucleic_acid_fluency", Random(seed))
        s = _stem(q)
        strand = re.search(r"5′-([ATCG]+)-3′", s).group(1)
        table = RNA_PAIR if s.startswith("สาย RNA") else PAIR
        assert _answer(q) == "".join(table[b] for b in strand), s
        q = generate("biology.nucleic_acid_application", Random(seed))
        s = _stem(q)
        if "ร้อยละเท่าใด" in s:
            given, value, want = re.search(r"มีเบส (\S) อยู่ร้อยละ (\d+) มีเบส (\S) ", s).groups()
            value = int(value)
            partner = {"A": "T", "T": "A", "C": "G", "G": "C"}
            assert _ans(q) == (value if partner[given] == want else 50 - value), s
        else:
            pairs, at = _q(r"ยาว (\d+) คู่เบส มีคู่ A-T ร้อยละ (\d+)", s)
            assert _ans(q) == pairs * at / 100 * 2 + pairs * (100 - at) / 100 * 3, s
        q = generate("biology.enzyme_fluency", Random(seed))
        s = _stem(q)
        if "pH ประมาณเท่าใด" in s:
            enzyme = next(e for e in ph if s.startswith(e))
            assert _ans(q) == ph[enzyme], s
        q = generate("biology.microscope_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ใช้เลนส์ใกล้ตา"):
            eye, obj = _q(r"(\d+)X กับเลนส์ใกล้วัตถุ (\d+)X", s)
            assert _ans(q) == eye * obj, s
        else:
            total, image = _q(rf"กำลังขยายรวม (\d+) เท่า .*ได้ยาว {N} mm", s)
            assert _ans(q) == image * 1000 / total, s
        q = generate("biology.microscope_application", Random(seed))
        s = _stem(q)
        if "เรียงเซลล์" in s:
            field, cells = _q(rf"กว้าง {N} mm เรียงเซลล์ได้เต็มแนวเส้นผ่านศูนย์กลาง (\d+) เซลล์", s)
            assert _ans(q) == field * 1000 / cells, s
        else:
            m1, d1, m2 = _q(r"กำลังขยาย (\d+) เท่า ขอบเขตภาพมีเส้นผ่านศูนย์กลาง (\d+) mm ถ้าเปลี่ยนเป็นกำลังขยาย (\d+)", s)
            assert _ans(q) == d1 * m1 / m2, s
        q = generate("biology.organelle_fluency", Random(seed))
        s = _stem(q)
        if s.endswith("มีเยื่อหุ้มกี่ชั้น"):
            name = s.replace("มีเยื่อหุ้มกี่ชั้น", "")
            text = {0: "ไม่มีเยื่อหุ้ม", 1: "มีเยื่อหุ้มชั้นเดียว", 2: "มีเยื่อหุ้มสองชั้น"}
            assert _answer(q) == text[membranes[name]], s


def test_lipid_and_metabolism_counts():
    from otk.sets.biology.m4.metabolism import REACTIONS
    kinds = {r[0]: r[1] for r in REACTIONS}
    for reaction, kind, energy in REACTIONS:
        assert (kind == "แอแนบอลิซึม") == (energy == "ดูดพลังงาน"), reaction
    for seed in range(SEEDS):
        q = generate("biology.lipid_fluency", Random(seed))
        s = _stem(q)
        if "ไตรกลีเซอไรด์" in s and "โมเลกุล จะมี" in s:
            (n,) = _q(r"สร้างไตรกลีเซอไรด์ (\d+) โมเลกุล", s)
            assert _ans(q) == 3 * n, s
        q = generate("biology.metabolism_foundation", Random(seed))
        s = _stem(q)
        if s.startswith("ข้อใดเป็นปฏิกิริยาแบบ"):
            assert kinds[_answer(q)] == s.split("แบบ")[1], s


# ── Slices 47-48: ชีววิทยาเพิ่มเติม 1 ม.4/13-/17, ชีววิทยาเพิ่มเติม 2 ม.4/1-/2 ──────────────

def test_cells_division_and_respiration_recompute():
    from otk.sets.biology.m4.membrane_transport import EXAMPLES, PROCESS_TRUTH
    process_of = dict(EXAMPLES)
    for truths in PROCESS_TRUTH.values():
        assert not ({"สารเคลื่อนที่จากความเข้มข้นสูงไปต่ำ", "สารเคลื่อนที่จากความเข้มข้นต่ำไปสูง"} <= set(truths))
    for seed in range(SEEDS):
        q = generate("biology.nucleus_fluency", Random(seed))
        s = _stem(q)
        (count,) = _q(r"(\d+) แท่ง", s)
        if "เซลล์สืบพันธุ์มีโครโมโซมกี่แท่ง" in s:
            assert _ans(q) == count / 2, s
        elif "กี่คู่" in s:
            assert _ans(q) == count, s
        else:
            assert _ans(q) == count * 2, s
        q = generate("biology.membrane_transport_fluency", Random(seed))
        s = _stem(q)
        if s.startswith('"'):
            assert _answer(q) == process_of[s.split('"')[1]], s
        else:
            assert process_of[_answer(q)] == s.split("ตัวอย่างของ")[1], s
        q = generate("biology.cell_division_application", Random(seed))
        s = _stem(q)
        (diploid,) = _q(r"มีโครโมโซม (\d+) แท่ง \(2n\)", s)
        stage = s.split(" ใน")[1].split(" มี")[0]
        expected = {"เมทาเฟสของไมโทซิส": diploid * 2, "แอนาเฟสของไมโทซิส (ทั้งเซลล์)": diploid * 2,
                    "เซลล์ลูกหลังไมโทซิส": diploid, "เมทาเฟส I ของไมโอซิส": diploid,
                    "เซลล์หลังไมโอซิส I": diploid / 2, "เซลล์หลังไมโอซิส II": diploid / 2,
                    "โพรเฟส I ของไมโอซิส": diploid / 2}[stage]
        assert _ans(q) == expected, s
        q = generate("biology.respiration_application", Random(seed))
        s = _stem(q)
        (glucose,) = _q(rf" {N} โมล ", s)
        per = 6 if "ใช้ออกซิเจน" in s else 2
        assert _ans(q) == glucose * per, s


def test_mendel_crosses_recompute():
    from otk.sets.biology.m4.mendel_experiment import TRAITS
    from otk.sets._support.science_wave_f48 import frac_text, gametes, offspring
    from otk.sets.biology.m4.mendel_law import phenotype
    assert offspring("Aa", "Aa") == {"AA": Fraction(1, 4), "Aa": Fraction(1, 2), "aa": Fraction(1, 4)}
    assert sorted(gametes("AaBb")) == ["AB", "Ab", "aB", "ab"]
    kids = offspring("AaBb", "AaBb")
    counts = {}
    for k, v in kids.items():
        counts[phenotype(k)] = counts.get(phenotype(k), 0) + v
    assert counts == {"AB": Fraction(9, 16), "Ab": Fraction(3, 16), "aB": Fraction(3, 16), "ab": Fraction(1, 16)}
    for seed in range(SEEDS):
        q = generate("biology.mendel_experiment_fluency", Random(seed))
        s = _stem(q)
        (total,) = _q(r"ได้ F₂ (\d+) ต้น", s)
        trait = next(t for t in s.split("คาดว่าจะมีต้นที่")[1:])
        dominant_asked = any(trait.startswith(f"{t}{d}") for t, d, r in TRAITS)
        assert _ans(q) == (total * 3 / 4 if dominant_asked else total / 4), s
        q = generate("biology.mendel_law_application", Random(seed))
        s = _stem(q)
        p1, p2 = re.search(r"ผสม (\S+) × (\S+) ", s).groups()
        kids = offspring(p1, p2)
        if "จีโนไทป์" in s:
            genotype = re.search(r"จีโนไทป์ (\S+) เท่ากับ", s).group(1)
            assert _answer(q) == frac_text(kids.get(genotype, Fraction(0))), s
        else:
            names = {"เด่นทั้งสองลักษณะ": "AB", "เด่นลักษณะแรก ด้อยลักษณะที่สอง": "Ab",
                     "ด้อยลักษณะแรก เด่นลักษณะที่สอง": "aB", "ด้อยทั้งสองลักษณะ": "ab"}
            target = next(v for k, v in names.items() if f"ฟีโนไทป์{k}" in s)
            assert _answer(q) == frac_text(sum((v for k, v in kids.items() if phenotype(k) == target), Fraction(0))), s


# ── Slices 49-50: ชีววิทยาเพิ่มเติม 2 ม.4/3-/9 ─────────────────────────────────────────

def test_blood_groups_and_sex_linkage_recompute():
    from otk.sets._support.science_wave_f48 import frac_text
    alleles = {"Iᴬ": "A", "Iᴮ": "B", "i": "O"}

    def split(genotype):
        out = []
        while genotype:
            head = next(a for a in alleles if genotype.startswith(a))
            out.append(alleles[head])
            genotype = genotype[len(head):]
        return out

    def group(a, b):
        s = {a, b} - {"O"}
        return "AB" if len(s) == 2 else (s.pop() if s else "O")

    for seed in range(SEEDS):
        q = generate("biology.mendel_extension_application", Random(seed))
        s = _stem(q)
        if s.startswith("พ่อมีจีโนไทป์"):
            g1, g2, target = re.search(r"พ่อมีจีโนไทป์ (\S+) แม่มีจีโนไทป์ (\S+) โอกาสที่ลูกมีหมู่เลือด (\S+) ", s).groups()
            kids = [group(a, b) for a in split(g1) for b in split(g2)]
            assert _answer(q) == frac_text(Fraction(kids.count(target), 4)), s
        q = generate("biology.chromosome_inheritance_fluency", Random(seed))
        s = _stem(q)
        m = re.search(r"แม่มีจีโนไทป์ (\S+) พ่อมีจีโนไทป์ (\S+) ", s)
        if m:
            mother, father = m.groups()
            moms = [mother[:2], mother[2:]]
            sons = [a for a in moms]
            daughters = [(a, father[:2]) for a in moms]
            if "ลูกชายคนนั้น" in s:
                want = Fraction(sum(a == "Xʰ" for a in sons), 2)
            elif "เป็นพาหะ" in s:
                want = Fraction(sum(set(d) == {"Xᴴ", "Xʰ"} for d in daughters), 2)
            elif "ลูกสาวคนนั้น" in s:
                want = Fraction(sum(d == ("Xʰ", "Xʰ") for d in daughters), 2)
            elif "เป็นลูกชายที่" in s:
                want = Fraction(sum(a == "Xʰ" for a in sons), 4)
            else:
                want = Fraction(sum(a == "Xʰ" for a in sons) + sum(d == ("Xʰ", "Xʰ") for d in daughters), 4)
            assert _answer(q) == frac_text(want), s


def test_polygenes_dna_and_translation_recompute():
    from otk.sets.biology.m4.gene_expression import STOPS
    for seed in range(SEEDS):
        q = generate("biology.variation_application", Random(seed))
        s = _stem(q)
        n, base, step = _q(rf"ยีน (\d+) คู่ .*สูง (\d+) cm และแอลลีลตัวใหญ่แต่ละตัวเพิ่มความสูง {N} cm", s)
        if "ต้นจีโนไทป์" in s:
            genotype = re.search(r"ต้นจีโนไทป์ (\S+) ", s).group(1)
            assert _ans(q) == base + step * sum(c.isupper() for c in genotype), s
        elif "กี่แบบ" in s:
            assert _ans(q) == 2 * n + 1, s
        elif "F₁" in s:
            assert _ans(q) == base + n * step, s
        else:
            (height,) = _q(rf"ต้นที่สูง {N} cm", s)
            assert _ans(q) == (height - base) / step, s
        q = generate("biology.dna_replication_application", Random(seed))
        s = _stem(q)
        if "¹⁵N จำนวน" in s:
            start, rounds = _q(r"จำนวน (\d+) โมเลกุล.* (\d+) รอบ", s)
            total = start * 2 ** rounds
            if "ทั้งหมดกี่" in s:
                assert _ans(q) == total, s
            elif "ร้อยละ" in s:
                assert _ans(q) == 200 * start / total * 1, s
            elif "มีแต่ ¹⁴N กี่" in s:
                assert _ans(q) == total - 2 * start, s
            else:
                assert _ans(q) == 2 * start, s
        elif "คู่เบส มีความยาว" in s:
            (pairs,) = _q(r"ยาว (\d+) คู่เบส", s)
            assert abs(_ans(q) - pairs * 0.34) < 1e-6, s
        q = generate("biology.gene_expression_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("mRNA"):
            mrna = re.search(r"5′-([AUCG]+)-3′", s).group(1)
            i, count = mrna.index("AUG"), 0
            while mrna[i:i + 3] not in STOPS:
                count += 1
                i += 3
            assert _ans(q) == count, s
        q = generate("biology.mutation_application", Random(seed))
        s = _stem(q)
        if "2n = " in s:
            (diploid,) = _q(r"2n = (\d+)", s)
            rules = {"ไทรโซมี": diploid + 1, "โมโนโซมี": diploid - 1, "นัลลิโซมี": diploid - 2,
                     "ทริปพลอยดี": diploid * 3 / 2, "เททระพลอยดี": diploid * 2,
                     "ไปทั้งสองแท่ง": diploid / 2 + 1, "ไม่ได้รับ": diploid / 2 - 1}
            assert _ans(q) == next(v for k, v in rules.items() if k in s), s


def test_mutation_sequences_match_their_kind():
    from otk.sets.biology.m4.mutation import chromosome_mutation, gene_mutation
    for seed in range(SEEDS):
        old, new, kind = gene_mutation(Random(seed))
        if kind == "การแทนที่คู่เบส":
            assert len(new) == len(old) and sum(a != b for a, b in zip(old, new)) == 1
        else:
            assert len(new) == len(old) + (1 if kind.startswith("การเพิ่ม") else -1)
        old, new, kind = chromosome_mutation(Random(seed))
        assert new != old and (("R" in new) == kind.startswith("การย้าย"))
        if "inversion" in kind:
            assert sorted(new) == sorted(old)


# ── Slices 51-52: ชีววิทยาเพิ่มเติม 2 ม.4/10-/15, ม.6/1 ─────────────────────────────────

def test_gene_technology_recompute():
    for seed in range(SEEDS):
        q = generate("biology.recombinant_dna_fluency", Random(seed))
        s = _stem(q)
        site = re.search(r"ที่ลำดับ 5′-([ATCG]+)-3′", s).group(1)
        seq = re.search(r"ลำดับเบส 5′-([ATCG]+)-3′", s).group(1)
        circular = "วงกลม" in s
        text = seq + seq[:len(site) - 1] if circular else seq
        sites = len(re.findall(f"(?={site})", text))
        if circular:
            sites = sum(text.startswith(site, i) for i in range(len(seq)))
        assert _ans(q) == (sites if "กี่ตำแหน่ง" in s else (sites if circular else sites + 1)), s
        q = generate("biology.recombinant_dna_application", Random(seed))
        s = _stem(q)
        if "ถูกเอนไซม์ตัดจำเพาะตัดที่" in s:
            (length,) = _q(r"(\d+) คู่เบส ถูก", s)
            cuts = [int(c) for c in re.search(r"คู่เบสที่ ([\d, ]+) ชิ้น", s).group(1).split(", ")]
            if "วงกลม" in s:
                pieces = [b - a for a, b in zip(cuts, cuts[1:])] + [length - cuts[-1] + cuts[0]]
            else:
                edges = [0, *cuts, length]
                pieces = [b - a for a, b in zip(edges, edges[1:])]
            assert sum(pieces) == length
            assert _ans(q) == (max(pieces) if "ยาวที่สุด" in s else min(pieces)), s
        q = generate("biology.dna_technology_use_application", Random(seed))
        s = _stem(q)
        if s.startswith("เริ่ม PCR"):
            start, cycles = _q(r"แม่แบบ (\d+) โมเลกุล ทำ PCR (\d+) รอบ", s)
            assert _ans(q) == start * 2 ** cycles, s
        elif "ของแม่" in s:
            bands = lambda text: {int(b) for b in text.split(", ")}
            mother = bands(re.search(r"ของแม่: ([\d, ]+) ลูก", s).group(1))
            child = bands(re.search(r"ลูก: ([\d, ]+) ชาย", s).group(1))
            fits = [ell for ell, b in re.findall(r"ชาย(\S): ([\d, ]+?)(?= ชาย| ชายคนใด)", s) if child - mother <= bands(b)]
            assert fits == [_answer(q).removeprefix("ชาย")], s


def test_evolution_and_population_recompute():
    for seed in range(SEEDS):
        q = generate("biology.evolution_evidence_application", Random(seed))
        s = _stem(q)
        if "ครึ่งชีวิต" in s:
            (half,) = _q(r"ครึ่งชีวิตของ\S+เท่ากับ ([\d,]+) ปี", s.replace(",", ""))
            m = re.search(r"เหลืออยู่ 1/(\d+)", s)
            left = Fraction(1, int(m.group(1))) if m else Fraction(re.search(r"ร้อยละ ([\d.]+)", s).group(1)) / 100
            n = 0
            while left < 1:
                left *= 2
                n += 1
            assert _ans(q) == n * half, s
        q = generate("biology.evolution_theory_application", Random(seed))
        s = _stem(q)
        a, b, la, lb = _q(r"(\d+) ตัว และ.* (\d+) ตัว ต่อมา.*ร้อยละ (\d+) ส่วน.*ร้อยละ (\d+)", s)
        left_a, left_b = a * (100 - la) / 100, b * (100 - lb) / 100
        if "ร้อยละเท่าใด" in s:
            assert abs(_ans(q) - 100 * left_a / (left_a + left_b)) < 1e-9, s
        else:
            assert _ans(q) == left_a + left_b, s
        q = generate("biology.hardy_weinberg_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ประชากรหนึ่งมีจีโนไทป์"):
            big, het, small = _q(r"AA (\d+) ตัว Aa (\d+) ตัว และ aa (\d+) ตัว", s)
            p = (2 * big + het) / (2 * (big + het + small))
            assert abs(_ans(q) - (p if "แอลลีล A " in s else 1 - p)) < 1e-9, s
        else:
            (given,) = _q(rf"เท่ากับ {N} ความถี่", s)
            p = given if "แอลลีล A " in s else 1 - given
            genotype = re.search(r"จีโนไทป์ (\S+) เท่ากับ", s).group(1)
            want = {"AA": p * p, "Aa": 2 * p * (1 - p), "aa": (1 - p) ** 2}[genotype]
            assert abs(_ans(q) - want) < 1e-9, s
        q = generate("biology.hardy_weinberg_application", Random(seed))
        s = _stem(q)
        people, per = _q(r"มี ([\d,]+) คน .*ทุก ([\d,]+) คน", s.replace(",", ""))
        qa = 1 / per ** 0.5
        if "พาหะ" in s:
            assert abs(_ans(q) - people * 2 * qa * (1 - qa)) < 1e-6, s
        elif "เด่นพันธุ์แท้" in s:
            assert abs(_ans(q) - people * (1 - qa) ** 2) < 1e-6, s
        else:
            assert abs(_ans(q) - 100 * qa) < 1e-9, s
        q = generate("biology.speciation_application", Random(seed))
        s = _stem(q)
        if "กี่แท่ง" in s:
            a, b = _q(r"2n = (\d+) ผสม.* 2n = (\d+)", s)
            hybrid = a / 2 + b / 2
            assert _ans(q) == (hybrid * 2 if "สปีชีส์ใหม่นี้" in s else hybrid), s


# ── Slices 53-54: ชีววิทยาเพิ่มเติม 2 ม.6/2-/5, ชีววิทยาเพิ่มเติม 3 ม.5/1-/3 ──────────────

def test_dichotomous_keys_walk_to_the_answer():
    from otk.sets.biology.m6.dichotomous_key import ANIMALS, ANIMAL_TRAITS, PLANTS, PLANT_TRAITS
    assert len(set(ANIMALS.values())) == len(ANIMALS) and len(set(PLANTS.values())) == len(PLANTS)
    tables = {**{n: dict(zip(ANIMAL_TRAITS, v)) for n, v in ANIMALS.items()},
              **{n: dict(zip(PLANT_TRAITS, v)) for n, v in PLANTS.items()}}

    def walk(key: str, name: str) -> tuple[str, list[str]]:
        couplets = {int(n): (trait, yes, no) for n, trait, yes, no in
                    re.findall(r"(\d+)ก (\S+) (ไปข้อ \d+|คือ\S+) / \d+ข \S+ (ไปข้อ \d+|คือ\S+)", key)}
        step, route = 1, []
        while True:
            trait, yes, no = couplets[step]
            has = tables[name][trait]
            route.append(f"{step}{'ก' if has else 'ข'}")
            target = yes if has else no
            if target.startswith("คือ"):
                return target.removeprefix("คือ"), route
            step = int(target.split()[1])

    for seed in range(SEEDS):
        q = generate("biology.dichotomous_key_application", Random(seed))
        s = _stem(q)
        key, name = re.search(r"ต่อไปนี้ (.*) การระบุ(\S+?)ต้องผ่าน", s).groups()
        found, route = walk(key, name)
        assert found == name and _answer(q) == " → ".join(route), s
        q = generate("biology.dichotomous_key_fluency", Random(seed))
        s = _stem(q)
        key = re.search(r"ต่อไปนี้ (.*) สิ่งมีชีวิตที่", s).group(1)
        assert walk(key, _answer(q))[0] == _answer(q), s


def test_ranks_timelines_and_rings_recompute():
    from otk.sets.biology.m6.taxonomy import LINEAGE
    for seed in range(SEEDS):
        q = generate("biology.taxonomy_application", Random(seed))
        s = _stem(q)
        ref = re.search(r"ใกล้ชิดกับ(\S+)มากที่สุด", s).group(1)
        depth = lambda other: next((i for i in range(3) if LINEAGE[ref][i] != LINEAGE[other][i]), 3)
        options = [n for n in LINEAGE if n != ref and f" {n} (" in s]
        assert max(options, key=depth) == _answer(q) and sorted(map(depth, options)).count(depth(_answer(q))) == 1, s
        q = generate("biology.first_cells_application", Random(seed))
        s = _stem(q)
        if "ล้านปีก่อน อยู่ห่าง" in s:
            (per,) = _q(r"ละ ([\d,]+) ล้านปี", s)
            (ago,) = _q(r"เมื่อประมาณ ([\d,]+) ล้านปีก่อน", s)
            assert _ans(q) == ago / per, s
        q = generate("biology.stem_structure_application", Random(seed))
        s = _stem(q)
        if "รัศมี" in s:
            radius, width = _q(rf"รัศมี {N} mm .*กว้างเฉลี่ย {N} mm", s)
            assert _ans(q) == radius / width, s
        elif "พ.ศ." in s:
            planted, cut = _q(r"พ\.ศ\. (\d+) และถูกตัดเมื่อ พ\.ศ\. (\d+)", s)
            assert _ans(q) == cut - planted, s


# ── Slices 55-56: ชีววิทยาเพิ่มเติม 3 ม.5/4-/10 ────────────────────────────────────────

def test_leaf_water_and_nutrient_rates_recompute():
    for seed in range(SEEDS):
        q = generate("biology.leaf_structure_application", Random(seed))
        s = _stem(q)
        if "นับปากใบได้" in s:
            area, count = _q(rf"พื้นที่ {N} mm² นับปากใบได้ {N} ปาก", s)
            assert _ans(q) == count / area, s
        elif "พื้นที่" in s:
            density, leaf = _q(rf"มีปากใบ {N} ปากต่อ mm² .*พื้นที่ {N} cm²", s)
            assert _ans(q) == density * leaf * 100, s
        else:
            upper, lower = _q(rf"ด้านบน {N} ปากต่อ mm² และด้านล่าง {N} ปากต่อ mm²", s)
            assert _ans(q) == lower / upper, s
        q = generate("biology.transpiration_application", Random(seed))
        s = _stem(q)
        if s.startswith("โพโตมิเตอร์"):
            section, travel, minutes = _q(rf"หน้าตัด {N} mm² .*ได้ {N} mm ในเวลา {N} นาที", s)
            assert _ans(q) == (travel * section if "ดูดน้ำไปกี่" in s else travel * section / minutes), s
        elif "เหลือหนัก" in s:
            start, hours, end = _q(rf"หนัก {N} g วางไว้ {N} ชั่วโมง เหลือหนัก {N} g", s)
            assert _ans(q) == (start - end) / hours, s
        else:
            loss, leaf = _q(rf"หายไป {N} g .*พื้นที่ {N} cm²", s)
            assert _ans(q) == loss * 1000 / leaf, s
        q = generate("biology.plant_nutrient_application", Random(seed))
        s = _stem(q)
        grade = [Fraction(x) for x in re.search(r"สูตร (\d+)-(\d+)-(\d+)", s).groups()]
        share = grade[0] if "ไนโตรเจน" in s else (grade[1] if "ฟอสฟอรัส" in s else grade[2])
        if s.startswith("ปุ๋ยสูตร"):
            (bag,) = _q(r"หนัก (\d+) kg", s)
            assert _ans(q) == bag * share / 100, s
        else:
            (need,) = _q(rf"\) {N} kg", s)
            assert _ans(q) == need * 100 / share, s


def test_phloem_and_calvin_cycle_recompute():
    for seed in range(SEEDS):
        q = generate("biology.food_transport_application", Random(seed))
        s = _stem(q)
        if "¹⁴C ในโฟลเอ็ม" in s:
            distance, minutes = _q(rf"ห่างจากใบ {N} cm หลังผ่านไป {N} นาที", s)
            assert _ans(q) == distance * 60 / minutes, s
        elif "ด้วยอัตรา" in s:
            speed, minutes = _q(rf"อัตรา {N} cm ต่อชั่วโมง ใน {N} นาที", s)
            assert _ans(q) == speed * minutes / 60, s
        q = generate("biology.photosynthesis_c3_application", Random(seed))
        s = _stem(q)
        if "กลูโคส" in s:
            (g,) = _q(r"กลูโคส (\d+) โมเลกุล", s)
            per = {"ตรึง CO₂ กี่": 6, "ATP": 18, "NADPH": 12}
            assert _ans(q) == g * next(v for k, v in per.items() if k in s), s
        else:
            (co2,) = _q(r"CO₂ ได้ (\d+) โมเลกุล", s)
            want = {"G3P": co2 / 3, "RuBP": co2, "PGA": 2 * co2}
            assert _ans(q) == next(v for k, v in want.items() if k in s), s


# ── Slices 57-58: ชีววิทยาเพิ่มเติม 3 ม.5/11-/17 ───────────────────────────────────────

def test_limiting_factor_tables_read_right():
    for seed in range(SEEDS):
        q = generate("biology.photosynthesis_factor_fluency", Random(seed))
        s = _stem(q)
        rows = {int(ell): (int(a), int(b)) for ell, a, b in re.findall(r"(\d+) ลักซ์ → (\d+) และ (\d+)", s)}
        light = int(re.search(r"ที่ความเข้มแสง (\d+) ลักซ์ และ", s).group(1))
        column = 0 if "ร้อยละ 0.04 ปัจจัย" in s else 1
        brighter = min((ell for ell in rows if ell > light), default=None)
        rises_with_light = brighter is not None and rows[brighter][column] > rows[light][column]
        if rises_with_light:
            assert _answer(q) == "ความเข้มของแสง", s
        else:
            assert column == 0 and rows[light][1] > rows[light][0] and _answer(q) == "ความเข้มข้นของ CO₂", s


def test_flower_counts_and_rates_recompute():
    from otk.sets.biology.m5.plant_life_cycle import STRUCTURE_PLOIDY
    ploidy = dict(STRUCTURE_PLOIDY)
    for seed in range(SEEDS):
        q = generate("biology.plant_life_cycle_application", Random(seed))
        s = _stem(q)
        (diploid,) = _q(r"2n = (\d+)", s)
        name = next(n for n in sorted(ploidy, key=len, reverse=True) if f" {n}มีโครโมโซม" in s)
        assert _ans(q) == diploid / 2 * ploidy[name], s
        q = generate("biology.photosynthesis_factor_application", Random(seed))
        s = _stem(q)
        if "ลักซ์ ถ้าเลื่อน" in s:
            d1, intensity, d2 = _q(rf"ห่างจากสาหร่ายหางกระรอก {N} cm ให้ความเข้มแสง {N} ลักซ์ ถ้าเลื่อนหลอดไฟไปห่าง {N} cm", s)
            assert _ans(q) == intensity * (d1 / d2) ** 2, s
        elif "รวมเป็นกี่" in s:
            net, resp = _q(rf"สุทธิ {N} หน่วย.*ใช้ O₂ {N} หน่วย", s)
            assert _ans(q) == net + resp, s
        q = generate("biology.c4_cam_application", Random(seed))
        s = _stem(q)
        if "ATP กี่" in s:
            per, glucose = _q(r"ใช้ ATP (\d+) โมเลกุลต่อ.*กลูโคส (\d+) โมเลกุล", s)
            assert _ans(q) == 6 * per * glucose, s
        q = generate("biology.germination_application", Random(seed))
        s = _stem(q)
        if s.startswith("เพาะเมล็ด"):
            total, grew = _q(r"(\d+) เมล็ด งอก (\d+) เมล็ด", s)
            assert _ans(q) == grew * 100 / total, s
        elif "ร้อยละการงอก" in s:
            share, total = _q(rf"ร้อยละการงอก {N} ถ้าเพาะ (\d+) เมล็ด", s)
            assert _ans(q) == share * total / 100, s


# ── Slices 59-60: ชีววิทยาเพิ่มเติม 3 ม.5/18, ชีววิทยาเพิ่มเติม 4 ม.5/1-/6 ─────────────────

def test_photoperiod_and_enzyme_tubes_decide_right():
    for seed in range(SEEDS):
        q = generate("biology.plant_response_application", Random(seed))
        s = _stem(q)
        critical, night = _q(r"ช่วงมืดวิกฤต (\d+) ชั่วโมง .*มืด (\d+) ชั่วโมง", s)
        dark = night / 2 if "เปิดไฟ" in s else night
        short_day = "พืชวันสั้น" in s
        assert _answer(q) == ("ออกดอก" if (dark > critical) == short_day else "ไม่ออกดอก"), s
        q = generate("biology.human_digestion_application", Random(seed))
        s = _stem(q)
        best = {"น้ำลาย": "น้ำกลั่น", "เพปซิน": "กรดไฮโดรคลอริก", "ไลเพสจากตับอ่อน": "โซเดียมไฮโดรเจนคาร์บอเนต"}
        enzyme = next(e for e in best if e in s)
        tubes = dict(re.findall(r"หลอด (\S): (.+?ที่ 37 °C)", s))
        good = [ell for ell, t in tubes.items() if "ต้มเดือด" not in t and "แทน" not in t and best[enzyme] in t]
        assert good == [_answer(q).removeprefix("หลอด ")], s


def test_gas_exchange_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.human_gas_exchange_fluency", Random(seed))
        s = _stem(q)
        pa, pb = _q(r"เท่ากับ (\d+) mmHg และใน.*เท่ากับ (\d+) mmHg", s)
        a = re.search(r"ใน(.+?)เท่ากับ", s).group(1)
        assert _answer(q).startswith(f"จาก{a}") == (pa > pb), s
        q = generate("biology.human_gas_exchange_application", Random(seed))
        s = _stem(q)
        if "ฮีโมโกลบิน" in s and "จับ O₂" in s:
            (hb,) = _q(r"ฮีโมโกลบิน (\d+) g", s)
            litres = _q(r"เลือด (\d+) ลิตร", s)[0] if re.search(r"เลือด \d+ ลิตร", s) else Fraction(1, 10)
            assert _ans(q) == hb * Fraction(134, 100) * 10 * litres, s
        q = generate("biology.mammal_lung_application", Random(seed))
        s = _stem(q)
        if s.startswith("ปอด"):
            millions, each = _q(rf"ประมาณ {N} ล้านถุง .*เฉลี่ย {N} mm²", s)
            assert _ans(q) == millions * each, s
        q = generate("biology.animal_gas_exchange_application", Random(seed))
        s = _stem(q)
        if "ลูกบาศก์" in s:
            (side,) = _q(r"ด้านละ (\d+) mm", s)
            assert _ans(q) == 6 / side, s
        else:
            dissolved, share, litres = _q(r"ละลายอยู่ (\d+) mg .*ร้อยละ (\d+) .*เหงือก (\d+) ลิตร", s)
            assert _ans(q) == dissolved * share * litres / 100, s


# ── Slices 61-62: ชีววิทยาเพิ่มเติม 4 ม.5/7-/13 ────────────────────────────────────────

def test_blood_groups_transfusion_and_typing_decide_right():
    antigens = {"A": {"A"}, "B": {"B"}, "AB": {"A", "B"}, "O": set()}
    for seed in range(SEEDS):
        q = generate("biology.blood_transfusion_application", Random(seed))
        s = _stem(q)
        a = "anti-A แล้วตกตะกอน" in s
        b = "anti-B แล้วตกตะกอน" in s
        d = "(Rh) แล้วตกตะกอน" in s
        group = {(True, True): "AB", (True, False): "A", (False, True): "B", (False, False): "O"}[(a, b)]
        assert _answer(q) == f"{group} Rh{'+' if d else '−'}", s
        q = generate("biology.blood_transfusion_fluency", Random(seed))
        s = _stem(q)
        if s.startswith("ผู้ป่วย"):
            rg, rr = re.search(r"หมู่เลือด (\S+) Rh(\S) ", s).groups()
            dg, dr = _answer(q).split(" Rh")
            assert antigens[dg] <= antigens[rg] and not (dr == "+" and rr == "−"), s
        else:
            dg, dr, rg, rr = re.search(r"หมู่เลือด (\S+) Rh(\S) ให้เลือดแก่คนหมู่เลือด (\S+) Rh(\S) ", s).groups()
            ok = antigens[dg] <= antigens[rg] and not (dr == "+" and rr == "−")
            assert _answer(q).startswith("ได้ เพราะ") == ok, s


def test_circulation_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.lung_volume_application", Random(seed))
        s = _stem(q)
        if s.startswith("ผลการวัด"):
            tidal, irv, erv, rv = _q(r"ปกติ (\d+) mL .*เข้า (\d+) mL .*ออก (\d+) mL .*ปอด (\d+) mL", s)
            vc = tidal + irv + erv
            assert _ans(q) == (vc + rv if "ทั้งหมดของปอด" in s else vc), s
        else:
            tidal, rate = _q(r"ครั้งละ (\d+) mL นาทีละ (\d+) ครั้ง", s)
            assert _ans(q) == tidal * rate / 1000, s
        q = generate("biology.fish_tail_blood_application", Random(seed))
        s = _stem(q)
        if "cm³" in s:
            flow, area = _q(r"เลือด (\d+) cm³ .*รวม (\d+) cm²", s)
            assert _ans(q) == flow / area, s
        else:
            dist, secs = _q(r"ได้ (\d+) μm ใน (\d+) วินาที", s)
            assert _ans(q) == dist / secs, s
        q = generate("biology.heart_vessel_application", Random(seed))
        s = _stem(q)
        if s.startswith("หัวใจเต้น"):
            rate, stroke = _q(r"เต้น (\d+) ครั้งต่อนาที บีบเลือดออกครั้งละ (\d+) mL", s)
            assert _ans(q) == rate * stroke / 1000, s
        elif s.startswith("หัวใจสูบฉีด"):
            output, rate = _q(rf"เลือด {N} ลิตรต่อนาที เต้น (\d+) ครั้ง", s)
            assert _ans(q) == output * 1000 / rate, s
        elif "ผลต่าง" in s:
            sys_, dia = _q(r"ได้ (\d+)/(\d+) mmHg", s)
            assert _ans(q) == sys_ - dia, s
        q = generate("biology.blood_component_application", Random(seed))
        s = _stem(q)
        if "น้ำหนักตัว" in s:
            mass, share = _q(r"หนักประมาณ (\d+) kg .*ร้อยละ (\d+)", s)
            assert _ans(q) == mass * share / 100, s
        elif "ฮีมาโทคริต" in s:
            blood, hct = _q(rf"เลือด {N} ลิตร .*ร้อยละ (\d+)", s)
            assert _ans(q) == blood * (100 - hct) / 100, s
        else:
            per, ml = _q(rf"ประมาณ {N} ล้านเซลล์ เลือด (\d+) mL", s)
            assert _ans(q) == per * 1000 * ml, s


# ── Slices 63-64: ชีววิทยาเพิ่มเติม 4 ม.5/14-/20 ───────────────────────────────────────

def test_immunity_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.lymph_application", Random(seed))
        s = _stem(q)
        if "ร้อยละ" in s:
            filtered, back = _q(r"หลอดเลือดฝอย (\d+) ลิตร .*ร้อยละ (\d+)", s)
            assert _ans(q) == filtered * (100 - back) / 100, s
        q = generate("biology.immunization_application", Random(seed))
        s = _stem(q)
        if "จะเหลือ" in s:
            start, half, days = _q(r"เริ่มต้น (\d+) หน่วย .*ทุก (\d+) วัน เมื่อผ่านไป (\d+) วัน", s)
            assert _ans(q) == start / 2 ** (days / half), s
        else:
            start, left, half = _q(rf"ลดจาก (\d+) หน่วยเหลือ {N} หน่วย .*ทุก (\d+) วัน", s)
            n = 0
            while start / 2 ** n > left:
                n += 1
            assert _ans(q) == half * n, s
        q = generate("biology.immune_defense_application", Random(seed))
        s = _stem(q)
        if "กี่เท่า" in s:
            first, second = _q(r"สูงสุด (\d+) หน่วยในวันที่ \d+ .*สูงสุด (\d+) หน่วย", s)
            assert _ans(q) == second / first, s
        elif "เร็วกว่ากี่วัน" in s:
            d1, d2 = _q(r"วันที่ (\d+) และครั้งที่สองในวันที่ (\d+)", s)
            assert _ans(q) == d1 - d2, s


def test_kidney_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.nephron_application", Random(seed))
        s = _stem(q)
        if "mL ต่อนาที" in s:
            (rate,) = _q(r"ได้ (\d+) mL ต่อนาที", s)
            assert _ans(q) == rate * 60 * 24 / 1000, s
        elif "ดูดกลับร้อยละ" in s and "ปัสสาวะที่ขับ" in s:
            filtrate, back = _q(rf"ได้ (\d+) ลิตรต่อวัน และดูดกลับร้อยละ {N}", s)
            assert _ans(q) == filtrate * (100 - back) / 100, s
        elif "ดูดกลับร้อยละเท่าใด" in s:
            filtrate, urine = _q(rf"ได้ (\d+) ลิตรต่อวัน ขับปัสสาวะ {N} ลิตร", s)
            assert _ans(q) == (filtrate - urine) * 100 / filtrate, s
        else:
            plasma, urine = _q(rf"ยูเรีย {N} g ต่อลิตร ปัสสาวะมียูเรีย {N} g", s)
            assert _ans(q) == urine / plasma, s
        q = generate("biology.kidney_structure_application", Random(seed))
        s = _stem(q)
        if "ร้อยละ" in s and "สูบฉีด" in s:
            output, share = _q(rf"เลือด {N} ลิตรต่อนาที ไตได้รับเลือดร้อยละ (\d+)", s)
            assert _ans(q) == output * share / 100, s
        elif "หนึ่งชั่วโมง" in s:
            (per_min,) = _q(rf"เลือด {N} ลิตรต่อนาที", s)
            assert _ans(q) == per_min * 60, s
        else:
            (per,) = _q(rf"ประมาณ {N} ล้านหน่วย", s)
            lost = _q(r"ร้อยละ (\d+)", s)[0] if "เสื่อม" in s else 0
            assert _ans(q) == per * 2 * (100 - lost) / 100, s


# ── Slices 65-66: ชีววิทยาเพิ่มเติม 4 ม.5/21, ม.6/1-/6 ─────────────────────────────────

def test_nerve_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.neuron_application", Random(seed))
        s = _stem(q)
        if "ใช้เวลากี่" in s:
            speed, length = _q(rf"อัตราเร็ว (\d+) m/s ระยะทาง {N} m", s)
            assert _ans(q) == length / speed * 1000, s
        else:
            length, ms = _q(rf"ได้ {N} m ในเวลา {N} ms", s)
            assert _ans(q) == length / ms * 1000, s
        q = generate("biology.nerve_impulse_application", Random(seed))
        s = _stem(q)
        if "mV" in s:
            rest, peak = _q(r"เท่ากับ (-\d+) mV และสูงสุดขณะดีโพลาไรเซชัน \+(\d+) mV", s)
            assert _ans(q) == peak - rest, s
        elif "ปั๊มทำงาน" in s:
            (cycles,) = _q(r"ทำงาน (\d+) รอบ", s)
            assert _ans(q) == cycles * (3 if "Na⁺" in s else 2), s
        else:
            (ref,) = _q(r"ระยะดื้อ \(refractory period\) (\d+) ms", s)
            assert _ans(q) == 1000 / ref, s
        q = generate("biology.kidney_disease_application", Random(seed))
        s = _stem(q)
        if "ร้อยละเท่าใด" in s:
            normal, measured = _q(rf"ประมาณ (\d+) mL ต่อนาที ผู้ป่วยรายหนึ่งกรองได้ {N} mL", s)
            assert _ans(q) == measured * 100 / normal, s


def test_autonomic_effects_match_their_side():
    from otk.sets.biology.m6.autonomic import ORGAN_EFFECTS
    for seed in range(SEEDS):
        q = generate("biology.autonomic_fluency", Random(seed))
        s = _stem(q)
        organ = next(o for o in ORGAN_EFFECTS if o in s)
        symp, para = ORGAN_EFFECTS[organ]
        if s.startswith("ระบบประสาท"):
            assert _answer(q) == (symp if "ซิมพาเทติกทำให้" in s and "พาราซิมพาเทติก" not in s else para), s
        else:
            assert _answer(q) == ("ระบบประสาทซิมพาเทติก" if symp in s else "ระบบประสาทพาราซิมพาเทติก"), s


# ── Slices 67-68: ชีววิทยาเพิ่มเติม 4 ม.6/7-/13 ────────────────────────────────────────

def test_senses_and_movement_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.blind_spot_fluency", Random(seed))
        s = _stem(q)
        values = {n: int(v) for n, v in re.findall(r"(\S+) (\d+) mm", s)}
        pick = min if "มากที่สุด" in s else max
        assert _answer(q) == pick(values, key=values.get), s
        q = generate("biology.blind_spot_application", Random(seed))
        s = _stem(q)
        if "ห่างจากโฟเวีย" in s:
            page, gap = _q(r"ห่างกระดาษ (\d+) cm .*ห่างกัน (\d+) cm", s)
            assert _ans(q) == gap * Fraction(17, 10) / page * 10, s
        else:
            retina, page = _q(rf"โฟเวีย {N} mm .*ห่างตา (\d+) cm", s)
            assert _ans(q) == retina / 10 * page / Fraction(17, 10), s
        q = generate("biology.joint_muscle_application", Random(seed))
        s = _stem(q)
        if s.startswith("ถือวัตถุ"):
            load, load_arm, muscle_arm = _q(r"หนัก (\d+) N .*ข้อศอก (\d+) cm .*ข้อศอก (\d+) cm", s)
            assert _ans(q) == load * load_arm / muscle_arm, s
        else:
            force, muscle_arm, load_arm = _q(rf"ออกแรง {N} N ที่ระยะ (\d+) cm .*ข้อศอก (\d+) cm", s)
            assert _ans(q) == force * muscle_arm / load_arm, s
        q = generate("biology.skeleton_muscle_application", Random(seed))
        s = _stem(q)
        if "หดสั้นลงเหลือ" in s:
            rest, short, count = _q(rf"ยาว {N} μm หดสั้นลงเหลือ {N} μm .*กัน (\d+) หน่วย", s)
            assert _ans(q) == (rest - short) * count, s
        elif "ยาวกี่มิลลิเมตร" in s:
            count, rest = _q(rf"ซาร์โคเมียร์ (\d+) หน่วย แต่ละหน่วยยาว {N} μm", s)
            assert _ans(q) == rest * count / 1000, s
        q = generate("biology.reproductive_system_application", Random(seed))
        s = _stem(q)
        if "มีนาคม" in s:
            cycle, start = _q(r"สม่ำเสมอ (\d+) วัน ประจำเดือนรอบนี้เริ่มวันที่ (\d+)", s)
            assert _ans(q) == start + cycle - 14 - 1, s
        elif "ตกไข่ในวันที่" in s:
            (day,) = _q(r"ตกไข่ในวันที่ (\d+)", s)
            assert _ans(q) == day + 14, s
        else:
            (cycle,) = _q(r"สม่ำเสมอ (\d+) วัน", s)
            assert _ans(q) == cycle - 14, s


# ── Slices 69-70: ชีววิทยาเพิ่มเติม 4 ม.6/14-/19, ชีววิทยาเพิ่มเติม 5 ม.6/1 ──────────────────

def test_gametes_bees_and_energy_recompute():
    from otk.sets.biology.m6.gametogenesis import PLOIDY
    ploidy = dict(PLOIDY)
    for seed in range(SEEDS):
        q = generate("biology.gametogenesis_application", Random(seed))
        s = _stem(q)
        if s.startswith("เซลล์ร่างกาย"):
            name = next(n for n in sorted(ploidy, key=len, reverse=True) if f" {n}มีโครโมโซม" in s)
            assert _ans(q) == 23 * ploidy[name], s
        else:
            (k,) = _q(r"(\d+) เซลล์", s)
            per = 4 if "ระยะแรก" in s and "อสุจิ" in s else 2 if "อสุจิ" in s or "โพลาร์บอดี" in s else 1
            assert _ans(q) == k * per, s
        q = generate("biology.animal_communication_application", Random(seed))
        s = _stem(q)
        if "วินาทีแทนระยะทาง" in s:
            per, secs = _q(rf"ประมาณ {N} เมตร ผึ้งส่ายท้องนาน (\d+) วินาที", s)
            assert _ans(q) == per * secs / 1000, s
        elif "ขึ้นตรง" in s:
            assert _answer(q) == "ไปทางเดียวกับดวงอาทิตย์", s
        elif "ลงตรง" in s:
            assert _answer(q) == "ไปทางตรงข้ามกับดวงอาทิตย์", s
        else:
            side, angle = re.search(r"ไปทาง(\S+)ของแนวดิ่งขึ้น (\d+) องศา", s).groups()
            assert _answer(q) == f"เบนไปทาง{side}ของทิศดวงอาทิตย์ {angle} องศา", s
        q = generate("biology.energy_flow_application", Random(seed))
        s = _stem(q)
        chain = re.search(r"โซ่อาหาร (.+?) \S+(?:ตรึง|ได้รับ)", s).group(1).split(" → ")
        (share,) = _q(r"ร้อยละ (\d+)", s)
        if "ตรึงพลังงานได้" in s:
            (base,) = _q(r"ได้ ([\d,]+) kJ", s)
            target = next(c for c in chain[1:] if f" {c}ได้รับ" in s)
            assert _ans(q) == base * (share / 100) ** chain.index(target), s
        else:
            (energy,) = _q(rf"ได้รับพลังงาน {N} kJ", s)
            target = next(c for c in chain[1:] if f" {c}ได้รับพลังงาน" in s)
            assert _ans(q) == energy / (share / 100) ** chain.index(target), s


# ── Slices 71-72: ชีววิทยาเพิ่มเติม 5 ม.6/2-/8 ─────────────────────────────────────────

def test_ecology_numbers_recompute():
    from otk.sets.biology.m6.biome import BIOMES
    bands = {b[0]: (b[1], b[2]) for b in BIOMES}
    for seed in range(SEEDS):
        q = generate("biology.biomagnification_application", Random(seed))
        s = _stem(q)
        chain = re.search(r"โซ่อาหาร (.+?) \S+มีสารพิษ", s).group(1).split(" → ") if "ในโซ่อาหาร" in s[:12] else None
        if chain:
            start, factor = _q(rf"มีสารพิษ {N} ppm ถ้าความเข้มข้นเพิ่มขึ้น (\d+) เท่า", s)
            target = next(c for c in chain[1:] if f" {c}มีสารพิษกี่" in s)
            assert _ans(q) == start * factor ** chain.index(target), s
        else:
            start, level = _q(rf"มีสารพิษ {N} ppm และ\S+มี {N} ppm", s)
            assert _ans(q) == level / start, s
        q = generate("biology.biome_application", Random(seed))
        s = _stem(q)
        rain, temp = _q(r"เฉลี่ย ([\d,]+) mm ต่อปี และอุณหภูมิเฉลี่ยทั้งปี (-?\d+) °C", s)
        fits = [n for n, ((r0, r1), (t0, t1)) in bands.items() if r0 <= rain <= r1 and t0 <= temp <= t1]
        assert fits == [_answer(q)], s
        q = generate("biology.population_trait_application", Random(seed))
        s = _stem(q)
        if "ติดเครื่องหมาย" in s:
            marked, second, recap = _q(r"เครื่องหมาย (\d+) ตัว.*จับใหม่ (\d+) ตัว พบที่มีเครื่องหมาย (\d+) ตัว", s)
            assert _ans(q) == marked * second / recap, s
        else:
            count, area = _q(r"(\d+) ต้น ในพื้นที่ (\d+) ตาราง", s)
            assert _ans(q) == count / area, s
        q = generate("biology.population_growth_application", Random(seed))
        s = _stem(q)
        if "แบ่งตัว" in s:
            start, doubling, total = _q(r"แบคทีเรีย (\d+) เซลล์ .*ทุก (\d+) นาที .*ผ่านไป (\d+) นาที", s)
            assert _ans(q) == start * 2 ** (total / doubling), s
        elif "อัตราการเพิ่มต่อหัว" in s:
            n, births, deaths = _q(r"ประชากร (\d+) ตัว ในหนึ่งปีมีการเกิด (\d+) ตัว และตาย (\d+) ตัว", s)
            assert _ans(q) == (births - deaths) * 100 / n, s
        else:
            r, k, n = _q(rf"r = {N} ต่อปี .*K = (\d+) ตัว ขณะที่ประชากรมี (\d+) ตัว", s)
            assert _ans(q) == r * n * (k - n) / k, s
        q = generate("biology.population_control_application", Random(seed))
        s = _stem(q)
        births, deaths, immig, emig = _q(r"เกิด (\d+) ตัว ตาย (\d+) ตัว อพยพเข้า (\d+) ตัว และอพยพออก (\d+) ตัว", s)
        change = births + immig - deaths - emig
        if "เมื่อสิ้นปี" in s:
            (start,) = _q(r"มี (\d+) ตัว ใน", s)
            assert _ans(q) == start + change, s
        else:
            assert _ans(q) == change, s


# ── Slices 73-74: ชีววิทยาเพิ่มเติม 5 ม.6/9-/13, โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/1-/2 ───

def test_environment_numbers_recompute():
    for seed in range(SEEDS):
        q = generate("biology.water_resource_application", Random(seed))
        s = _stem(q)
        if "ค่า BOD ของน้ำนี้" in s:
            start, end = _q(rf"ได้ {N} mg/L เก็บ.*วัดได้ {N} mg/L", s)
            assert _ans(q) == start - end, s
        elif "เกณฑ์ BOD" in s:
            start, end = _q(rf"เริ่มต้น {N} mg/L และหลัง 5 วันเหลือ {N} mg/L", s)
            bod = start - end
            assert _answer(q).startswith(f"BOD เท่ากับ {bod.numerator / bod.denominator:g}") or str(bod) in _answer(q), s
            assert ("อยู่ในเกณฑ์" in _answer(q)) == (bod <= Fraction(3, 2)), s
        else:
            per_min, people, minutes, days = _q(r"ไหล (\d+) ลิตรต่อนาที .*สมาชิก (\d+) คน.*คนละ (\d+) นาที.*ใน (\d+) วัน", s)
            assert _ans(q) == per_min * people * minutes * days, s
        q = generate("biology.air_pollution_application", Random(seed))
        s = _stem(q)
        if "เป็น" in s and "μg/m³ ค่าเฉลี่ย" in s:
            readings = [int(x) for x in re.search(r"เป็น ([\d, ]+) μg", s).group(1).split(", ")]
            assert _ans(q) == Fraction(sum(readings), len(readings)), s
        elif "กี่วันที่เกิน" in s:
            readings = [int(x) for x in re.search(r"เป็น ([\d, ]+) μg", s).group(1).split(", ")]
            assert _ans(q) == sum(r > 37.5 for r in readings), s
        elif "กี่เท่าของมาตรฐาน" in s:
            (worst,) = _q(r"เท่ากับ (\d+) μg", s)
            assert _ans(q) == worst / Fraction(75, 2), s
        q = generate("geo.drift_evidence_application", Random(seed))
        s = _stem(q)
        if "สันเขา" in s:
            km, ma = _q(r"สันเขากลางมหาสมุทร ([\d,]+) km มีอายุ (\d+) ล้านปี", s)
            assert _ans(q) == km * 100000 / (ma * 1000000), s
        else:
            rate, years = _q(rf"อัตรา {N} cm ต่อปี ใน ([\d,]+) ปี", s)
            assert _ans(q) == rate * years / 100, s
        q = generate("geo.layered_earth_application", Random(seed))
        s = _stem(q)
        if "หนากี่" in s:
            top, bottom = _q(r"ความลึก ([\d,]+) ถึง ([\d,]+) km", s)
            assert _ans(q) == bottom - top, s
        elif "ช้ากว่าคลื่น P" in s:
            dist, p, sv = _q(r"ห่างจุดเกิดแผ่นดินไหว ([\d,]+) km คลื่น P เร็ว (\d+) km/s คลื่น S เร็ว (\d+) km/s", s)
            assert _ans(q) == dist / sv - dist / p, s
        else:
            speed, dist = _q(r"เฉลี่ย (\d+) km/s ระยะทาง ([\d,]+) km", s)
            assert _ans(q) == dist / speed, s


# ── Slices 75-76: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/3-/9 ──────────────────────────────

def test_rock_sections_order_right():
    for seed in range(SEEDS):
        q = generate("geo.geologic_history_fluency", Random(seed))
        s = _stem(q)
        layers = re.search(r"บนเป็น ([A-E, ]+) มีพนัง", s).group(1).split(", ")
        cut = re.search(r"ตัดผ่านชั้น ([A-E, ]+) แต่", s).group(1).split(", ")
        order = cut + ["พนังหินอัคนี X"] + layers[len(cut):]
        assert layers[:len(cut)] == cut, s
        if "ก่อนสุด" in s:
            assert _answer(q) == order[0], s
        elif "หลังสุด" in s:
            assert _answer(q) == order[-1], s
        else:
            assert _answer(q) == " → ".join(order), s


def test_earth_numbers_recompute():
    from otk.sets.earth_science.m4.mineral_id import MOHS
    for seed in range(SEEDS):
        q = generate("geo.plate_margin_application", Random(seed))
        s = _stem(q)
        if "จะเคลื่อนที่ได้" in s:
            rate, ma = _q(rf"อัตรา {N} cm ต่อปี ใน (\d+) ล้านปี", s)
            assert _ans(q) == rate * ma * 10, s
        else:
            km, rate = _q(rf"กว้าง ([\d,]+) km .*อัตรารวม {N} cm", s)
            assert _ans(q) == km / (rate * 10), s
        q = generate("geo.geologic_history_application", Random(seed))
        s = _stem(q)
        (half,) = _q(r"เท่ากับ ([\d,]+) ล้านปี", s)
        if "เหลืออยู่" in s:
            (den,) = _q(r"เหลืออยู่ 1/(\d+)", s)
        else:
            daughter, parent = _q(r"เป็น (\d+) : (\d+)", s)
            den = (daughter + parent) / parent
        assert _ans(q) == half * (den.numerator.bit_length() - 1), s
        q = generate("geo.quake_magnitude_application", Random(seed))
        s = _stem(q)
        high, low = _q(rf"ขนาด {N} .*ขนาด {N} ", s)
        base = 10 if "แอมพลิจูด" in s else 32
        assert _ans(q) == base ** (high - low), s
        q = generate("geo.tsunami_wave_application", Random(seed))
        s = _stem(q)
        if "ทะเลลึก" in s:
            (depth,) = _q(r"ทะเลลึก ([\d,]+) m", s)
            assert _ans(q) ** 2 == 10 * depth, s
        else:
            km_h, dist = _q(rf"\(เท่ากับ {N} km/h\) .*ระยะ {N} km", s)
            assert _ans(q) == dist / km_h, s
        q = generate("geo.mineral_id_fluency", Random(seed))
        s = _stem(q)
        if "อยู่ในช่วงใด" in s:
            lo = next(i for i, m in enumerate(MOHS) if s.startswith(f"แร่ตัวอย่างขีด{m}เป็นรอย"))
            hi = next(i for i, m in enumerate(MOHS) if f"แต่ถูก{m}ขีด" in s)
            assert _answer(q) == f"มากกว่า {lo + 1} แต่น้อยกว่า {hi + 1}", s
        elif "จะเป็นรอย" in s:
            a, b = (next(i for i, m in enumerate(MOHS) if f"{tag}{m}" in s) for tag in ("นำ", "กับ"))
            assert _answer(q) == MOHS[min(a, b)], s


# ── Slices 77-78: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/10-/12, 2 ม.5/1-/4 ─────────────────

def test_maps_fuels_and_winds_recompute():
    for seed in range(SEEDS):
        q = generate("geo.petroleum_coal_application", Random(seed))
        s = _stem(q)
        if "อยู่ลึกกี่" in s:
            speed, time = _q(rf"อัตราเร็วเฉลี่ย ([\d,]+) m/s .*ในเวลา {N} วินาที", s)
            assert _ans(q) == speed * time / 2, s
        else:
            depth, speed = _q(rf"ลึก {N} m ถ้าคลื่นไหวสะเทือนเคลื่อนที่ด้วยอัตราเร็ว ([\d,]+) m/s", s)
            assert _ans(q) == 2 * depth / speed, s
        q = generate("geo.geologic_map_fluency", Random(seed))
        s = _stem(q)
        (scale,) = _q(r"1 : ([\d,]+)", s)
        if "วัดระยะ" in s:
            (cm,) = _q(rf"ได้ {N} cm", s)
            assert _ans(q) == cm * scale / 100000, s
        else:
            (km,) = _q(rf"จริง {N} km", s)
            assert _ans(q) == km * 100000 / scale, s
        q = generate("geo.geologic_map_application", Random(seed))
        s = _stem(q)
        if "ช่วงชั้นความสูง" in s:
            interval, base, gaps = _q(r"ช่วงชั้นความสูง (\d+) m จุด ก อยู่บนเส้น (\d+) m จุด ข อยู่สูงกว่าจุด ก ไป (\d+) เส้น", s)
            assert _ans(q) == base + interval * gaps, s
        else:
            run, rise = _q(r"แนวราบ ([\d,]+) m มีความสูงต่างกัน (\d+) m", s)
            assert _ans(q) == rise * 100 / run, s
        q = generate("geo.air_force_fluency", Random(seed))
        s = _stem(q)
        if "แรงคอริออลิสทำให้เบน" in s:
            heading = re.search(r"ไปทาง(ทิศ\S+) แรง", s).group(1)
            right_of = {"ทิศเหนือ": "ทิศตะวันออก", "ทิศใต้": "ทิศตะวันตก", "ทิศตะวันออก": "ทิศใต้", "ทิศตะวันตก": "ทิศเหนือ"}
            left_of = {v: k for k, v in right_of.items()}
            assert _answer(q) == (right_of[heading] if "ซีกโลกเหนือ" in s else left_of[heading]), s
        q = generate("geo.solar_heating_application", Random(seed))
        s = _stem(q)
        if "sin" in s:
            incoming, sine = _q(rf"พลังงาน (\d+) W/m² .*= {N}\)", s)
            assert _ans(q) == incoming * sine, s
        else:
            incoming, albedo = _q(r"(\d+) W/m² ซึ่งมีอัตราส่วนสะท้อนร้อยละ (\d+)", s)
            reflected = incoming * albedo / 100
            assert _ans(q) == (reflected if "สะท้อนพลังงานกลับ" in s else incoming - reflected), s


# ── Slices 79-80: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/5-/11 ──────────────────────────────

def test_oceans_air_and_climate_recompute():
    dirs = ("ทิศเหนือ", "ทิศตะวันออก", "ทิศใต้", "ทิศตะวันตก")
    for seed in range(SEEDS):
        q = generate("geo.ocean_layer_application", Random(seed))
        s = _stem(q)
        if "เทอร์โมไคลน์" in s:
            top, bottom, upper, lower = _q(rf"ความลึก {N} m ถึง {N} m อุณหภูมิที่ขอบบน {N} °C และที่ขอบล่าง {N} °C", s)
            assert _ans(q) == (upper - lower) / (bottom - top) * 100, s
        elif "มีเกลือละลาย" in s:
            salinity, mass = _q(rf"ความเค็ม {N} ส่วนในพันส่วน \(g/kg\) น้ำทะเล {N} kg", s)
            assert _ans(q) == salinity * mass, s
        else:
            mass, salt = _q(rf"ระเหยน้ำทะเล {N} kg จนแห้งได้เกลือ {N} g", s)
            assert _ans(q) == salt / mass, s
        q = generate("geo.ocean_current_application", Random(seed))
        s = _stem(q)
        if "ชายฝั่ง" in s:
            m = re.search(r"ซีกโลก(เหนือ|ใต้)มีแผ่นดินอยู่ทาง(ทิศ\S+?)ของทะเล ลมพัดขนานฝั่งไปทาง(ทิศ\S+?) ", s)
            land, heading = dirs.index(m.group(2)), dirs.index(m.group(3))
            transport = (heading + (1 if m.group(1) == "เหนือ" else 3)) % 4
            assert _answer(q).startswith("เกิดน้ำผุด" if transport == (land + 2) % 4 else "เกิดน้ำจม"), s
        elif "ในเวลา" in s:
            speed, days = _q(rf"อัตราเร็วเฉลี่ย {N} km ต่อวัน ในเวลา {N} วัน", s)
            assert _ans(q) == speed * days, s
        else:
            speed, dist = _q(rf"อัตราเร็วเฉลี่ย {N} km ต่อวัน .*ได้ {N} km", s)
            assert _ans(q) == dist / speed, s
        q = generate("geo.air_stability_application", Random(seed))
        s = _stem(q)
        temp, dew = _q(rf"อุณหภูมิ {N} °C จุดน้ำค้าง {N} °C", s)
        if "ฐานเมฆ" in s:
            assert _ans(q) == (temp - dew) * 100, s
        elif "ยกตัวขึ้นสูง" in s:
            (height,) = _q(rf"ยกตัวขึ้นสูง {N} m", s)
            assert _ans(q) == temp - 10 * height / 1000, s
        else:
            (top,) = _q(rf"ภูเขาสูง {N} m", s)
            base = (temp - dew) / 10
            assert _ans(q) == dew - 6 * (top / 1000 - base), s
        q = generate("geo.weather_front_application", Random(seed))
        s = _stem(q)
        if "ความลาดชัน" in s:
            slope, dist = _q(rf"1 : {N} .*อากาศเย็น {N} km", s)
            assert slope == (100 if s.startswith("แนวปะทะอากาศเย็น") else 200), s
            assert _ans(q) == dist / slope, s
        elif "km/h" in s:
            dist, speed = _q(rf"{N} km และเคลื่อนที่เข้าหาด้วยอัตราเร็ว {N} km/h", s)
            assert _ans(q) == dist / speed, s
        q = generate("geo.climate_factor_application", Random(seed))
        s = _stem(q)
        if "เพิ่มขึ้นเฉลี่ยปีละ" in s:
            c1, y1, c2, y2 = _q(rf"วัดได้ {N} ppm ในปี พ.ศ. {N} และ {N} ppm ในปี พ.ศ. {N}", s)
            assert _ans(q) == (c2 - c1) / (y2 - y1), s
        elif "อีก" in s:
            now, rate, years = _q(rf"ประมาณ {N} ppm ถ้ายังเพิ่มขึ้นปีละ {N} ppm อีก {N} ปี", s)
            assert _ans(q) == now + rate * years, s
        else:
            pre, now = _q(rf"ประมาณ {N} ppm ถ้าปัจจุบันวัดได้ {N} ppm", s)
            assert _ans(q) == (now - pre) / pre * 100, s
        q = generate("geo.climate_mitigation_application", Random(seed))
        s = _stem(q)
        if "หลอด" in s:
            old, new, count, hours, days = _q(rf"หลอดไฟ {N} W เป็นหลอด LED {N} W จำนวน {N} หลอด เปิดวันละ {N} ชั่วโมง เป็นเวลา {N} วัน", s)
            assert _ans(q) == (old - new) * count * hours * days / 1000 / 2, s
        elif "kWh" in s and "ใช้ไฟฟ้าเดือนละ" in s:
            (kwh,) = _q(rf"เดือนละ {N} kWh", s)
            assert _ans(q) == kwh / 2, s
        elif "ลิตร" in s:
            (litres,) = _q(rf"เดือนละ {N} ลิตร", s)
            assert _ans(q) == litres * Fraction(23, 10), s
        else:
            total, per_tree = _q(rf"ปีละ {N} kg ถ้าต้นไม้ 1 ต้นดูดซับ CO₂ ได้ปีละ {N} kg", s)
            assert _ans(q) == total / per_tree, s


def test_ocean_and_air_labels_follow_the_numbers():
    for seed in range(SEEDS):
        q = generate("geo.ocean_layer_fluency", Random(seed))
        s = _stem(q)
        if "ถึงลึก" in s:
            mixed, bottom, depth = _q(rf"ถึงลึก {N} m .*ลึกกว่า {N} m .*ที่ความลึก {N} m", s)
            want = "ชั้นน้ำผสม" if depth < mixed else "เทอร์โมไคลน์" if depth < bottom else "ชั้นน้ำลึก"
            assert _answer(q) == want, s
        else:
            rows = re.findall(r"ตัวอย่าง (\S) อุณหภูมิ (\d+) °C ความเค็ม (\d+)", s)
            best = [n for n, t, sal in rows if all(int(t) <= int(t2) and int(sal) >= int(s2) for _, t2, s2 in rows)]
            assert len(best) == 1 and _answer(q) == f"ตัวอย่าง {best[0]}", s
        q = generate("geo.air_stability_fluency", Random(seed))
        s = _stem(q)
        if "กลุ่มอากาศยกตัว" in s:
            parcel, around = _q(rf"มีอุณหภูมิ {N} °C ขณะที่อากาศรอบข้างที่ระดับเดียวกันมีอุณหภูมิ {N} °C", s)
            assert _answer(q).startswith("ไม่มีเสถียรภาพ" if parcel > around else "มีเสถียรภาพ"), s
        else:
            (rate,) = _q(rf"ลดลง {N} °C ต่อความสูง 1 km", s)
            assert _answer(q) == ("มีเสถียรภาพสัมบูรณ์" if rate < 6 else "ไม่มีเสถียรภาพสัมบูรณ์" if rate > 10 else "มีเสถียรภาพแบบมีเงื่อนไข"), s
        q = generate("geo.current_effect_application", Random(seed))
        s = _stem(q)
        if "เกณฑ์" in s:
            normal, measured = _q(rf"เฉลี่ยระยะยาว {N} °C ช่วงหลายเดือนนี้เฉลี่ย {N} °C", s)
            d = measured - normal
            assert _answer(q) == ("เอลนีโญ" if d > Fraction(1, 2) else "ลานีญา" if d < Fraction(-1, 2) else "สภาวะปกติ"), s
        elif "กว่าค่าเฉลี่ยกี่" in s:
            normal, measured = _q(rf"ระยะยาวเป็น {N} °C ปีนี้วัดได้ {N} °C", s)
            assert _ans(q) == abs(measured - normal), s


# ── Slices 81-82: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/12-/13, 3 ม.6/1-/5 ──────────────────

def test_weather_maps_and_early_universe_recompute():
    for seed in range(SEEDS):
        q = generate("geo.station_model_fluency", Random(seed))
        s = _stem(q)
        if "ก้านลมบนแผนที่อากาศมี" in s:
            count = lambda word: int(m.group(1)) if (m := re.search(rf"{word} (\d+)", s)) else 0
            assert _ans(q) == 50 * count("ธงสามเหลี่ยม") + 10 * count("ขีดยาว") + 5 * count("ขีดสั้น"), s
        elif "รหัสความกดอากาศ" in s:
            code = int(re.search(r"เป็น (\d{3}) ", s).group(1))
            assert _ans(q) == Fraction((9000 if code >= 500 else 10000) + code, 10), s
        else:
            where = re.search(r"ชี้ไปทาง(\S+) ลม", s).group(1)
            assert _answer(q) == f"ลมพัดมาจาก{where}", s
        q = generate("geo.station_model_application", Random(seed))
        s = _stem(q)
        if "นอต" in s:
            (knots,) = _q(rf"อัตราเร็ว {N} นอต", s)
            assert _ans(q) == knots * Fraction(1852, 1000), s
        elif "ผลต่างทั้งสองค่า" in s:
            temp, dew = _q(rf"อุณหภูมิอากาศ {N} °C และอุณหภูมิจุดน้ำค้าง {N} °C", s)
            assert _ans(q) == temp - dew, s
        elif "ความกดอากาศที่จุด ข" in s:
            interval, start, lines = _q(rf"ทุก ๆ {N} hPa จุด ก อยู่บนเส้น {N} hPa จุด ข อยู่ถัดไปอีก {N} เส้น", s)
            assert _ans(q) == (start + interval * lines if "ความกดอากาศสูง" in s else start - interval * lines), s
        elif "กี่ช่วง" in s:
            start, end, interval = _q(rf"ไอโซบาร์ {N} hPa จุด ข อยู่บนไอโซบาร์ {N} hPa และแผนที่ลากไอโซบาร์ทุก ๆ {N} hPa", s)
            assert _ans(q) == abs(end - start) / interval, s
        q = generate("geo.weather_outlook_application", Random(seed))
        s = _stem(q)
        if "ชายฝั่ง" in s:
            dist, speed = _q(rf"ห่างจากชายฝั่ง {N} km และเคลื่อนเข้าหาฝั่งด้วยอัตราเร็ว {N} km/h", s)
            assert _ans(q) == dist / speed, s
        elif "ร้อยละ" in s:
            share, units = _q(rf"ร้อยละ {N} ของพื้นที่ จังหวัดหนึ่งมี {N} ", s)
            assert _ans(q) == share * units / 100, s
        elif "ชั่วโมงละ" in s:
            start, end, hours = _q(rf"จาก {N} hPa เป็น {N} hPa ในเวลา {N} ชั่วโมง", s)
            assert _ans(q) == (start - end) / hours, s
        q = generate("astro.cosmic_timeline_application", Random(seed))
        s = _stem(q)
        if "ขยายขนาดเป็น" in s:
            temp, factor = _q(rf"อุณหภูมิเป็น {N} K เมื่อเอกภพขยายขนาดเป็น {N} เท่า", s)
            assert _ans(q) == temp / factor, s
        elif "ขยายขนาดขึ้นกี่เท่า" in s:
            before, after = _q(rf"ลดลงจาก {N} K เป็น {N} K", s)
            assert _ans(q) == before / after, s
        else:
            (mass,) = _q(rf"แก๊สดั้งเดิม {N} หน่วยมวล", s)
            assert _ans(q) == (mass / 4 if "มีฮีเลียม" in s else mass * 3 / 4), s
        q = generate("astro.hubble_law_application", Random(seed))
        s = _stem(q)
        if "อยู่ห่าง" in s and "Mpc) ถ้า" in s:
            d, h0 = _q(rf"อยู่ห่าง {N} ล้านพาร์เซก \(Mpc\) ถ้าค่าคงที่ฮับเบิลเป็น {N} ", s)
            assert _ans(q) == h0 * d, s
        elif "อยู่ห่างกี่ Mpc" in s:
            v, h0 = _q(rf"อัตราเร็ว {N} km/s ถ้าค่าคงที่ฮับเบิลเป็น {N} ", s)
            assert _ans(q) == v / h0, s
        else:
            rest, seen = _q(rf"ความยาวคลื่นปกติ {N} nm จากกาแล็กซีหนึ่งวัดได้ {N} nm", s)
            assert _ans(q) == 300000 * (seen - rest) / rest, s


def test_galaxy_star_birth_and_fusion_recompute():
    for seed in range(SEEDS):
        q = generate("astro.galaxy_structure_application", Random(seed))
        s = _stem(q)
        if "จะโคจรได้กี่รอบ" in s:
            period, age = _q(rf"รอบละประมาณ {N} ล้านปี ในเวลา {N} ล้านปี", s)
            assert _ans(q) == age / period, s
        elif "รอบละกี่ล้านปี" in s:
            laps, age = _q(rf"ได้ {N} รอบในเวลา {N} ล้านปี", s)
            assert _ans(q) == age / laps, s
        else:
            size, ly = _q(rf"กว้าง {N} m .* {N} ปีแสงจะยาว", s)
            assert _ans(q) == size * ly / 100000, s
        q = generate("astro.protostar_application", Random(seed))
        s = _stem(q)
        if "รัศมีลดลงเหลือ 1/" in s:
            (k,) = _q(rf"เหลือ 1/{N} ของเดิม", s)
            assert _ans(q) == k ** 3, s
        elif "รัศมีลดลงกี่เท่า" in s:
            (cube,) = _q(rf"เพิ่มขึ้น {N} เท่า", s)
            assert _ans(q) ** 3 == cube, s
        elif "เคลวิน" in s:
            (celsius,) = _q(rf"อุณหภูมิ {N} °C", s)
            assert _ans(q) == celsius + 273, s
        else:
            suns, share = _q(rf"มวล {N} เท่าของดวงอาทิตย์ ถ้าร้อยละ {N} ", s)
            assert _ans(q) == suns * share / 100, s
        q = generate("astro.fusion_chain_application", Random(seed))
        s = _stem(q)
        if "มวลหายไปร้อยละ 0.7" in s:
            (kg,) = _q(rf"ไฮโดรเจน {N} kg", s)
            assert _ans(q) == kg * 1000 * Fraction(7, 1000), s
        elif "E = mc²" in s:
            (grams,) = _q(rf"มวล {N} g", s)
            assert _ans(q) * 10 ** 13 == grams / 1000 * (3 * 10 ** 8) ** 2, s
        elif "โปรตอน" in s and "นิวเคลียสฮีเลียมกี่" in s:
            (protons,) = _q(rf"โปรตอน {N} อนุภาค", s)
            assert _ans(q) == protons / 4, s
        else:
            (helium,) = _q(rf"ให้ฮีเลียม {N} นิวเคลียส", s)
            assert _ans(q) == helium * 2, s
        q = generate("astro.fusion_chain_fluency", Random(seed))
        s = _stem(q)
        if "มวล" in s:
            (mass,) = _q(rf"มวล {N} เท่าของดวงอาทิตย์", s)
            assert _answer(q) == ("ปฏิกิริยาลูกโซ่โปรตอน-โปรตอน" if mass < Fraction(13, 10) else "วัฏจักรคาร์บอน-ไนโตรเจน-ออกซิเจน"), s
        q = generate("geo.weather_outlook_fluency", Random(seed))
        s = _stem(q)
        if "อุณหภูมิต่ำสุด" in s:
            (low,) = _q(rf"ยอดดอยเป็น {N} °C", s)
            assert _answer(q) == ("หนาวจัด" if low < 8 else "หนาว" if low < 16 else "เย็น"), s
        elif "คลื่นสูง" in s and "เกิน" in s:
            wave, limit = _q(rf"คลื่นสูง {N} เมตร ถ้ามีคำแนะนำให้เรือเล็กงดออกจากฝั่งเมื่อคลื่นสูงเกิน {N} เมตร", s)
            assert _answer(q).startswith("งดออกเรือ" if wave > limit else "ออกเรือได้"), s


# ── Slices 83-84: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/6-/12 ─────────────────────────────

def test_star_light_distance_and_life_recompute():
    for seed in range(SEEDS):
        q = generate("astro.magnitude_scale_application", Random(seed))
        s = _stem(q)
        if "สว่างกว่าดาว ข" in s:
            a, b = _q(rf"ดาว ก มีโชติมาตรปรากฏ {N} ดาว ข มีโชติมาตรปรากฏ {N} ", s)
            assert _ans(q) == 100 ** ((b - a) / 5), s
        elif "ระยะห่าง" in s and "ความสว่างปรากฏจะ" in s:
            (k,) = _q(rf"(?:1/|เพิ่มเป็น ){N}", s)
            assert _ans(q) == k * k, s
        elif "L ∝ R²T⁴" in s:
            r, t = _q(rf"รัศมี {N} เท่า และอุณหภูมิผิว {N} เท่า", s)
            assert _ans(q) == r ** 2 * t ** 4, s
        else:
            d, m_abs = _q(rf"ห่าง {N} พาร์เซก มีโชติมาตรสัมบูรณ์ {N} ", s)
            assert _ans(q) == m_abs + 5 * (len(str(int(d))) - 2), s
        q = generate("astro.magnitude_scale_fluency", Random(seed))
        s = _stem(q)
        if "สัมบูรณ์" in s:
            rows = [Fraction(x) for x in re.findall(r"โชติมาตรสัมบูรณ์ (-?[\d.]+)", s)]
            assert _answer(q) == ("ดาว ก", "ดาว ข", "ดาว ค", "ดาว ง")[rows.index(min(rows))], s
        else:
            rows = [Fraction(x) for x in re.findall(r"โชติมาตรปรากฏ (-?[\d.]+)", s)]
            pick = min(rows) if "สว่างที่สุด" in s else max(rows)
            assert _answer(q) == ("ดาว ก", "ดาว ข", "ดาว ค", "ดาว ง")[rows.index(pick)], s
        q = generate("astro.star_color_application", Random(seed))
        s = _stem(q)
        if "มีอุณหภูมิผิว" in s and "ความยาวคลื่นกี่" in s:
            (temp,) = _q(rf"อุณหภูมิผิว {N} K", s)
            assert _ans(q) == 2900000 / temp, s
        else:
            (lam,) = _q(rf"ความยาวคลื่น {N} nm", s)
            assert _ans(q) == 2900000 / lam, s
        q = generate("astro.parallax_application", Random(seed))
        s = _stem(q)
        if "ปีแสง" in s and "1 พาร์เซก = 3.26" in s:
            (p,) = _q(rf"แพรัลแลกซ์ {N} ฟิลิปดา", s)
            assert _ans(q) == Fraction(326, 100) / p, s
        elif "เลื่อนไปรวม" in s:
            (shift,) = _q(rf"เลื่อนไปรวม {N} ฟิลิปดา", s)
            assert _ans(q) == 2 / shift, s
        elif "มุมแพรัลแลกซ์เป็นกี่" in s:
            (d,) = _q(rf"ห่างจากโลก {N} พาร์เซก", s)
            assert _ans(q) == 1 / d, s
        else:
            (p,) = _q(rf"แพรัลแลกซ์ {N} ฟิลิปดา", s)
            assert _ans(q) == 1 / p, s
        q = generate("astro.hr_diagram_application", Random(seed))
        s = _stem(q)
        if "อยู่ในลำดับหลักได้" in s:
            (m,) = _q(rf"มวล {N} เท่า", s)
            assert _ans(q) == 10000 / m ** 3, s
        elif "L ∝ M⁴) มีความส่องสว่าง" in s:
            (m,) = _q(rf"มวล {N} เท่า", s)
            assert _ans(q) == m ** 4, s
        q = generate("astro.hr_diagram_fluency", Random(seed))
        s = _stem(q)
        if "มวลตั้งต้น" in s:
            (m,) = _q(rf"มวลตั้งต้น {N} เท่า", s)
            assert _answer(q) == ("ดาวแคระขาว" if m < 8 else "ดาวนิวตรอน" if m < 25 else "หลุมดำ"), s


def test_planets_orbits_and_the_sun_recompute():
    for seed in range(SEEDS):
        q = generate("astro.habitable_zone_application", Random(seed))
        s = _stem(q)
        if "ประมาณกี่หน่วยดาราศาสตร์" in s:
            (lum,) = _q(rf"ส่องสว่าง {N} เท่า", s)
            assert _ans(q) ** 2 == lum, s
        elif "พลังงานต่อพื้นที่" in s:
            d, lum = _q(rf"ห่างดาวฤกษ์ {N} AU ดาวฤกษ์ส่องสว่าง {N} เท่า", s)
            assert _ans(q) == lum / d ** 2, s
        else:
            inner, outer, d = _q(rf"ตั้งแต่ {N} ถึง {N} AU ดาวเคราะห์ที่อยู่ห่าง {N} AU", s)
            assert _answer(q).startswith("อยู่ในเขต" if inner <= d <= outer else "ใกล้" if d < inner else "ไกล"), s
        q = generate("astro.kepler_law_application", Random(seed))
        s = _stem(q)
        if "มีคาบการโคจรกี่ปี" in s:
            (a,) = _q(rf"ระยะทางเฉลี่ย {N} AU", s)
            assert _ans(q) ** 2 == a ** 3, s
        else:
            (t,) = _q(rf"คาบการโคจรรอบดวงอาทิตย์ {N} ปี", s)
            assert _ans(q) ** 3 == t ** 2, s
        q = generate("astro.kepler_law_fluency", Random(seed))
        s = _stem(q)
        if "ดาวหาง" in s:
            rows = [Fraction(x) for x in re.findall(r"ห่างดวงอาทิตย์ ([\d.]+) AU", s)]
            pick = min(rows) if "เร็วที่สุด" in s else max(rows)
            assert _answer(q) == ("ตำแหน่ง ก", "ตำแหน่ง ข", "ตำแหน่ง ค", "ตำแหน่ง ง")[rows.index(pick)], s
        q = generate("astro.solar_storm_application", Random(seed))
        s = _stem(q)
        if "km/s" in s:
            (speed,) = _q(rf"อัตราเร็ว {N} km/s", s)
            seconds = Fraction(150_000_000) / speed
            assert _ans(q) == (seconds / 60 if "กี่นาที" in s else seconds), s
        elif "ครั้งที่" in s:
            year, cycles = (int(x) for x in re.search(r"ปี ค.ศ. (\d+) .*ครั้งที่ (\d+)", s).groups())
            assert _answer(q) == f"ค.ศ. {year + 11 * cycles}", s
        elif "กี่วัฏจักร" in s:
            first, last = (int(x) for x in re.search(r"ค.ศ. (\d+) และ ค.ศ. (\d+)", s).groups())
            assert _ans(q) * 11 == last - first, s
        else:
            photo, spot = _q(rf"อุณหภูมิ {N} K จุดมืดที่อยู่ใกล้กันมีอุณหภูมิ {N} K", s)
            assert _ans(q) == photo - spot, s


# ── Slices 85-86: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/13-/19 ────────────────────────────

def _minutes(clock: str) -> int:
    hours, minutes = re.match(r"(\d\d):(\d\d)", clock).groups()
    return int(hours) * 60 + int(minutes)


def test_sky_coordinates_and_time_recompute():
    for seed in range(SEEDS):
        q = generate("astro.celestial_sphere_application", Random(seed))
        s = _stem(q)
        if "ผ่านเส้นเมริเดียน" in s:
            lat, dec = _q(rf"ละติจูดประมาณ {N}° เหนือ\) ดาวดวงหนึ่งมีเดคลิเนชัน \+?{N}°", s)
            assert _ans(q) == 90 - abs(lat - dec), s
        elif "จุดจอมฟ้า" in s:
            (lat,) = _q(rf"ละติจูดประมาณ {N}°", s)
            assert _ans(q) == lat, s
        elif "คิดเป็นมุมกี่องศา" in s:
            (hours,) = _q(rf"ไรต์แอสเซนชัน {N} ชั่วโมง", s)
            assert _ans(q) == hours * 15, s
        else:
            (deg,) = _q(rf"ไรต์แอสเซนชัน {N}°", s)
            assert _ans(q) == deg / 15, s
        q = generate("astro.star_path_fluency", Random(seed))
        s = _stem(q)
        lat, dec = _q(rf"ละติจูด {N}° เหนือ เห็นดาวที่มีเดคลิเนชัน \+?{N}°", s)
        limit = 90 - lat
        want = "เป็นดาวค้างฟ้า" if dec > limit else "ไม่ขึ้น" if dec < -limit else "ขึ้นและตก"
        assert _answer(q).startswith(want), s
        q = generate("astro.star_path_application", Random(seed))
        s = _stem(q)
        if "ขึ้นเวลา" in s and "จะขึ้นเวลาใด" in s:
            start = _minutes(re.search(r"ขึ้นเวลา (\d\d:\d\d)", s).group(1))
            (days,) = _q(rf"อีก {N} วัน", s)
            assert _minutes(_answer(q)) == (start - 4 * int(days)) % 1440, s
        elif "เร็วกว่าเดิมกี่นาที" in s:
            (days,) = _q(rf"ผ่านไป {N} วัน", s)
            assert _ans(q) == 4 * days, s
        else:
            (lat,) = _q(rf"ละติจูดประมาณ {N}°", s)
            assert _ans(q) == 90 - lat, s
        q = generate("astro.apparent_solar_time_fluency", Random(seed))
        s = _stem(q)
        (deg,) = _q(rf"ตะวัน(?:ตก|ออก) {N}°", s)
        sign = 1 if "ไปทางตะวันตก" in s else -1
        assert _minutes(_answer(q)) == 720 + sign * 4 * int(deg), s
        q = generate("astro.apparent_solar_time_application", Random(seed))
        s = _stem(q)
        clocks = [_minutes(c) for c in re.findall(r"(\d\d:\d\d) น\.", s)]
        if "ต่างกันกี่นาที" in s:
            assert _ans(q) == abs(clocks[1] - clocks[0]), s
        else:
            assert _minutes(_answer(q)) == 720 + clocks[1] - clocks[0], s
        q = generate("astro.time_zone_fluency", Random(seed))
        s = _stem(q)
        thai = _minutes(re.search(r"เป็น (\d\d:\d\d)", s).group(1))
        m = re.search(r"\(UTC([+−])(\d+)(?::(\d+))?\) เป็นเท่าใด", s)
        offset = (int(m.group(2)) * 60 + int(m.group(3) or 0)) * (1 if m.group(1) == "+" else -1)
        assert _minutes(_answer(q)) == (thai + offset - 420) % 1440, s
        q = generate("astro.time_zone_application", Random(seed))
        s = _stem(q)
        if "105° ตะวันออก) กี่นาที" in s:
            (lon,) = _q(rf"ลองจิจูด {N}° ตะวันออก เวลา", s)
            assert _ans(q) == (105 - lon) * 4, s
        elif "สถานที่ ก" in s:
            a, b = _q(rf"ลองจิจูด {N}° ตะวันออก สถานที่ ข อยู่ลองจิจูด {N}°", s)
            assert _ans(q) == abs(a - b) * 4, s
        else:
            (lon,) = _q(rf"อยู่ที่ {N}° ตะวันออก", s)
            assert _ans(q) == lon / 15, s


def test_planets_space_and_stargazing_recompute():
    for seed in range(SEEDS):
        q = generate("astro.elongation_application", Random(seed))
        s = _stem(q)
        if "คาบซินอดิก" in s:
            (period,) = _q(rf"คาบการโคจร {N} ปี", s)
            assert 1 / _ans(q) == abs(1 / period - 1), s
        else:
            (a,) = _q(rf"ห่างดวงอาทิตย์ {N} AU", s)
            assert _ans(q) == (a - 1 if "ตรงข้าม" in s else a + 1), s
        q = generate("astro.space_telescope_application", Random(seed))
        s = _stem(q)
        if "รวมแสง" in s:
            big, small = _q(rf"เส้นผ่านศูนย์กลาง {N} m กล้อง ข มีกระจก {N} m", s)
            assert _ans(q) == (big / small) ** 2, s
        elif "สัญญาณวิทยุ" in s:
            (dist,) = _q(rf"(?:ห่าง(?:ประมาณ)? |ความสูงประมาณ |รวม ){N} km", s)
            assert _ans(q) == dist / 300000, s
        else:
            (period,) = _q(rf"รอบละ {N} นาที", s)
            assert _ans(q) == 1440 / period, s
        q = generate("astro.stargazing_plan_application", Random(seed))
        s = _stem(q)
        if "ได้กำลังขยายกี่เท่า" in s:
            focal, eye = _q(rf"เลนส์ใกล้วัตถุ {N} mm ใช้เลนส์ตาความยาวโฟกัส {N} mm", s)
            assert _ans(q) == focal / eye, s
        elif "ควรใช้เลนส์ตา" in s:
            focal, mag = _q(rf"ความยาวโฟกัส {N} mm ต้องการกำลังขยาย {N} เท่า", s)
            assert _ans(q) == focal / mag, s
        elif "หน้ากล้องกว้าง" in s:
            (aperture,) = _q(rf"หน้ากล้องกว้าง {N} mm", s)
            assert _ans(q) == 2 * aperture, s
        else:
            start = _minutes(re.search(r"เวลาประมาณ (\d\d:\d\d)", s).group(1))
            (months,) = _q(rf"อีก {N} เดือน", s)
            assert _minutes(_answer(q)) == (start - 120 * int(months)) % 1440, s
        q = generate("astro.elongation_fluency", Random(seed))
        s = _stem(q)
        if "วงนอกดวงหนึ่งมีมุมห่าง" in s:
            (angle,) = _q(rf"มุมห่าง {N}°", s)
            east = "ทางตะวันออกของ" in s
            if angle < 90:
                assert _answer(q).startswith("เห็นทางท้องฟ้าด้านตะวันตก" if east else "เห็นทางท้องฟ้าด้านตะวันออก"), s
            else:
                assert _answer(q).startswith("เห็นตั้งแต่หัวค่ำ" if east else "เห็นตั้งแต่ก่อนเที่ยงคืน"), s


# ── Deliberate exceptions ─────────────────────────────────────────────────────

# Outcomes evidenced by a performance, a product, attendance or a lab test the
# student runs, rather than an answer. No multiple-choice item can assess them, so they stay open on purpose.
DELIBERATELY_OPEN = frozenset({
    "เคมีเพิ่มเติม 3 ม.4/3",
    "เคมีเพิ่มเติม 3 ม.6/1",
    "เคมีเพิ่มเติม 3 ม.6/2",
    "เคมีเพิ่มเติม 3 ม.6/3",
    "เคมีเพิ่มเติม 3 ม.6/4",
    # เคมีเพิ่มเติม 2 ม.5/4 and เคมีเพิ่มเติม 1 ม.6/9 and ม.6/13 (lab tests and a
    # rate experiment) were here until Wave I (2026-10-12) wrote sets for the
    # part of each that an answer can show: test_science_wave_i.py.
})


def test_performance_outcomes_stay_deliberately_unmapped():
    import csv
    from pathlib import Path

    mapped = {code for spec in SCIENCE_PLACEMENTS.values() for code in spec.indicator_codes}
    assert not DELIBERATELY_OPEN & mapped
    path = Path(__file__).resolve().parents[2] / "docs" / "for_admin" / "science_ipst_outcomes.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        state = {row["outcome_code"]: row["coverage_state"] for row in csv.DictReader(handle)}
    assert all(state[code] == "missing" for code in DELIBERATELY_OPEN)

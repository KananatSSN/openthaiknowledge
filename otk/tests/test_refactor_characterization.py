"""Frozen contracts for the retained domain layer.

What survives here is what the refactor promised not to change: a seeded
question's exact output, the PDF renderer's output shape, and the size and
filing of the published set registry. The rest of this module used to freeze
the pre-refactor FastAPI app — its route surface, its session signing, its coin
ledger and its role gates — and went with that app when the SvelteKit stack
replaced it. The EXP and mastery curves it also pinned now live with TutorRank,
in its ``services/generator/tests/legacy_reference.py``.
"""

from __future__ import annotations

import io
from random import Random

from otk.core import REGISTRY, generate
from otk.core.render import render_pdf
from otk.core.worksheet import Worksheet, build_worksheet
from otk.tools.sheetpipe import load_sheet, solver_modules
from otk.tools.sheetpipe.spec import sheet_ids


def test_seeded_question_has_golden_semantics():
    question = generate("math.one_digit_plus_with_carry", Random(20260824))
    assert question.model_dump() == {
        "type": "math.one_digit_plus_with_carry",
        "topic": "การบวก",
        "level": "ป.1",
        "stem": [{"kind": "math", "tex": "8 + 7"}],
        # Re-pinned when rank balancing landed (MCQ_GUESSABILITY.md): the old
        # draw offered 13, 10, 11 beside 15, so the answer was always the largest.
        "choices": [
            {"content": [{"kind": "math", "tex": "15"}]},
            {"content": [{"kind": "math", "tex": "17"}]},
            {"content": [{"kind": "math", "tex": "11"}]},
            {"content": [{"kind": "math", "tex": "10"}]},
        ],
        "answer": 0,
        # The set-level strategy hint (types/math_hints.py), shown after answering.
        "hint": [
            {'kind': 'text', 'text': 'เติมให้ครบ 10 ก่อน เช่น '},
            {'kind': 'math', 'tex': '9 + 3'},
            {'kind': 'text', 'text': ' คิดเป็น '},
            {'kind': 'math', 'tex': '9 + 1 = 10'},
            {'kind': 'text', 'text': ' แล้วบวกที่เหลืออีก 2 ได้ 12'},
        ],
    }


def test_pdf_output_contract_is_frozen():
    config = Worksheet(
        title="Phase 0",
        generators={"math.one_digit_plus_with_carry": 1},
        num_problems=6,
        problems_per_page=6,
        answer_key=True,
        seed=20260824,
    )
    questions = build_worksheet(config, Random(config.seed))
    output = io.BytesIO()
    render_pdf(config, questions, output)

    assert len(questions) == 6
    assert output.getvalue().startswith(b"%PDF-")
    assert len(output.getvalue()) > 1_000


def test_sheet_publication_manifest_is_frozen():
    expected = {
        "posn2561_math": (30, 30, 30, 6),
        "posn2562_math": (30, 30, 30, 2),
        "posn2564_math": (30, 30, 30, 5),
        "posn2565_math": (30, 30, 30, 2),
        "posn2566_math": (30, 30, 30, 4),
        "posn2567_math": (30, 30, 30, 7),
        "posn2568_math": (30, 30, 30, 9),
    }
    actual = {}
    for sheet_id in sheet_ids():
        sheet = load_sheet(sheet_id)
        actual[sheet_id] = (
            len(sheet.items),
            len(solver_modules(sheet)),
            sum(bool(item.generator) for item in sheet.items),
            sum(bool(item.figure_asset) for item in sheet.items),
        )
    assert actual == expected
    # The one deliberate literal total in the suite, and the only number a new
    # slice has to bump. Everything else about a set — its stage, its subject,
    # its filing — is derived and checked structurally, in
    # test_science_stage_registry.py and test_science_curriculum.py. This exists
    # so that a change in the registry's size is never invisible.
    #
    # 737 independently-authored generators, plus 11 curriculum-pinned science successors, 15 staged
    # Phase 3 science-pilot sets, 45 Phase 5 Wave A sets, 262 Wave B sets,
    # 27 sets closing ว 1.1, 228 Wave C sets, 309 Wave D sets, 57 Wave E sets,
    # 15 Wave F sets, 26 Wave G sets, 170 สสวท. ป.1–ม.3 sets (math_p1–p6,
    # math_m1–m3), 20 sets read off drawn diagrams (math_diagrams), and 45
    # สสวท. ม.4–ม.6 sets (math_m4–m6, math_diagrams_hi), 23 sets for book
    # chapters that had none (math_chapters), 14 geometry and chart sets
    # read off drawings (math_diagrams_geo), and 16 third sets for thin topics
    # (math_thin_topics), and 9 ป.1 sets read off pictures of things
    # (math_pictures), ป.1 subtraction within 20, and 5 ป.2–ป.3 picture sets
    # (math_pictures_p2), and 6 second formats for drill-only primary topics
    # (math_formats) and 9 for secondary ones (math_formats_hi), then a ป.3
    # growing-pattern picture and a ม.3 special-angle triangle, and 6 sets read
    # off instruments and icon pictographs (math_measure_pictures), and 6 more
    # picture sets (math_pictures_extra) and 6 in math_pictures_hi, then 10
    # picture sets for the เพิ่มเติม track (math_pictures_add) and 10 harder
    # application sets for it (math_apply_add), and 10 for the พื้นฐาน track
    # (math_apply_basic). Progression sets fell from 124 to 21 when fragmented
    # math topics were consolidated, and to none once every topic had three
    # authored sets. The content audit then added 15 sets for indicators no
    # set taught (math_gaps_primary) and 14 more for primary geometry,
    # fractions and data (math_gaps_shape_data), and 24 secondary sets
    # (math_gaps_secondary). An indicator-by-indicator check then added 8
    # primary and 5 additional-course sets whose topic existed
    # (math_gaps_indicators). 18 application sets then widened the last stage
    # of topics that ended in a bare computation (math_apply_stage), and a
    # three-digit multiplication set smoothed the step to four digits at ป.3.
    # Science Wave E slices 8-10 then added 21 ม.5 sets: chemical equations,
    # the rate of reaction, redox, radioactivity, and acceleration; slices
    # 11-12 added 24 more closing ว 2.2 ม.5: forces, motion and magnetism;
    # slices 13-14 added 21 for ว 2.3 ม.5/1-7: nuclear and renewable energy,
    # waves, resonance and sound; slice 15 added 15 closing ว 2.3 ม.5: uses
    # of sound, colour, electromagnetic waves and communication. Wave F
    # slices 3-4 added 21 ฟิสิกส์เพิ่มเติม 1 sets: motion, forces, work and energy;
    # slices 5-6 added 21 closing ฟิสิกส์เพิ่มเติม 1: centre of mass, momentum,
    # collisions, projectiles, circular motion, history and measurement;
    # slices 7-8 added 21 for ฟิสิกส์เพิ่มเติม 2 ม.5/1-7: oscillation, waves and sound;
    # slices 9-10 added 21 closing ฟิสิกส์เพิ่มเติม 2 (light and colour) and
    # opening ฟิสิกส์เพิ่มเติม 3 (charge, Coulomb's law, electric field);
    # slices 11-12 added 21 more ฟิสิกส์เพิ่มเติม 3: capacitors to magnetic force;
    # slices 13-14 added 21 closing ฟิสิกส์เพิ่มเติม 3 and opening ฟิสิกส์เพิ่มเติม 4 (heat);
    # slices 15-16 added 21 more ฟิสิกส์เพิ่มเติม 4: elasticity to Bohr's atom;
    # slices 17-18 added 24 closing ฟิสิกส์เพิ่มเติม: photoelectric to particle physics;
    # slices 19-20 added 21 opening เคมีเพิ่มเติม: atomic models to ionic bonds;
    # slices 21-22 added 21 more: ionic and covalent compounds and bond energy;
    # slices 23-24 added 21 more: shape, forces, network solids, metals, gas laws;
    # slices 25-26 added 21 more: the rest of the gas laws and opening organic chemistry;
    # slices 27-28 added 21 more: naming, isomers, properties, reactions and polymers;
    # slices 29-30 added 21 more: polymer structure and waste, and stoichiometry;
    # slices 31-32 added 21 more: limiting reagent, percent yield and reaction rates;
    # slices 33-34 added 21 more: rate graphs and chemical equilibrium;
    # slices 35-36 added 21 more: equilibrium at work and acids and bases;
    # slices 37-38 added 21 more: titration, buffers and redox;
    # slices 39-40 added 21 more: electrochemistry and lab safety;
    # slices 41-42 added 21 more: units, the mole, formulas and concentration;
    # slices 43-44 added 21 more: finishing chemistry and opening additional biology;
    # slices 45-46 added 21 more: biomolecules, enzymes, the microscope and cells;
    # slices 47-48 added 21 more: transport, cell division, respiration and Mendel;
    # slices 49-50 added 21 more: beyond Mendel, DNA, protein synthesis and mutation;
    # slices 51-52 added 21 more: gene technology, evolution, populations and biodiversity;
    # slices 53-54 added 21 more: early life, groups, naming, keys and plant anatomy;
    # slices 55-56 added 21 more: leaf, water, nutrients, phloem and photosynthesis;
    # slices 57-58 added 21 more: C4 and CAM, limiting factors, flowers, seeds and hormones;
    # slices 59-60 added 21 more: plant responses, digestion and gas exchange;
    # slices 61-62 added 21 more: breathing volumes, circulation, the heart and blood;
    # slices 63-64 added 21 more: lymph, immunity, excretion and the kidney;
    # slices 65-66 added 21 more: kidney disease and the nervous system;
    # slices 67-68 added 21 more: senses, movement, bones and muscles, reproduction;
    # slices 69-70 added 21 more: gametes, embryos, hormones, behaviour and energy flow;
    # slices 71-72 added 21 more: biomagnification, cycles, biomes, succession and populations;
    # slices 73-74 added 21 more: water, air, soil, forests, wildlife, the Earth's layers and drift;
    # slices 75-76 added 21 more: plate boundaries, rock history, volcanoes, quakes, tsunamis, minerals, rocks;
    # slices 77-78 added 21 more: fossil fuels, maps, sunlight, energy balance and the winds;
    # slices 79-80 added 21 more: ocean layers and currents, air stability, fronts and climate change;
    # slices 81-82 added 21 more: weather maps, forecasting, the early universe, the galaxy and star birth;
    # slices 83-84 added 21 more: magnitude, colour, parallax, the H-R diagram, orbits and solar storms;
    # slices 85-86 added 21 more: the celestial sphere, time, elongation, space exploration and stargazing.
    # The sheet bank's knowledge pass then added 91 math sets for units no set
    # practised (the 20 math_bank_* modules; see SHEET_DIGESTION_PLAN.md).
    # Wave I added 12 for the four indicators the task queue found with no set,
    # and the 2564 สอวน. sheet 30 more (one per question).
    # Geography (ส 5) then arrived as a subject of its own with 33 sets, and a
    # second wave added 16 (weather, seasons, Thailand's regions, continents),
    # and a third 11 (waste, livelihoods, economic location, landforms, population).
    # A fourth wave brought each geography unit to a full three stages: 20 more.
    # The coverage audit then added 54 for the 31 geography indicators no set
    # taught: 18 units of three stages, ป.1 to ม.4-6.
    # Process skills, until then only at ม.1, gained a three-stage unit at each
    # of ป.4, ป.5, ป.6, ม.2 and ม.3. Then three diagram sets: Earth's interior,
    # a food web and a cell, each read from a drawn picture; then four more:
    # a soil profile, the water cycle, a flower and a food chain; then the rock
    # cycle, plate boundaries, the heart and the digestive system; then the
    # airway and lungs, a plant's organs, and rock layers with their fossils.
    # Local math variety and original olympiad practice add another 118 sets.
    assert len(REGISTRY) == 3953

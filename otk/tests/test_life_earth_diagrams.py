"""Biology and Earth-science diagrams: drawable specs, and answers read back from them."""

from __future__ import annotations

import re
from itertools import permutations
from random import Random

from otk.core import generate
from otk.core.render.assets import is_diagram
from otk.sets._support.life_earth_diagrams import (
    CELL_DIAGRAMS,
    CHAIN_PLACES,
    EARTH_LAYERS,
    EARTH_SECTIONS,
    FLOWER_PART_NAMES,
    FLOWERS,
    FOOD_CHAIN_PICTURES,
    FOOD_WEBS,
    PLANT_PARTS,
    SOIL_HORIZONS,
    SOIL_PROFILES,
    WATER_CYCLES,
    WATER_STEPS,
    CHAMBERS,
    DIGESTIVE_NAMES,
    DIGESTIVE_PICTURES,
    HEARTS,
    PLATE_PICTURES,
    ROCK_CYCLES,
    ROCK_STAGES,
    BREATHING_PICTURES,
    PLANT_PICTURES,
    ROCK_LAYERS,
)
from otk.sets.biology.m2.blood_circulation import BLOOD_LOOP
from otk.sets.biology.p6.digestive_system import DIGESTIVE_ORGANS, FOOD_PATH
from otk.sets.earth_science.m6.plate_boundary import BOUNDARIES
from otk.sets.earth_science.p6.rocks_and_the_rock_cycle import ROCK_CYCLE_ARROWS
from otk.sets.biology.m2.respiratory import AIR_PATH
from otk.sets.biology.p4.organ_function import ORGAN_FAILURES, ORGAN_JOBS
from otk.sets.earth_science.p6.fossil import FINDS
from otk.sets.biology.m1.flowers_fruits_and_seeds import FLOWER_PARTS
from otk.sets.biology.p5.food_chains import FOOD_CHAINS, ROLES
from otk.sets.earth_science.m2.earth_interior import SHELLS
from otk.sets.earth_science.m2.soil_profile import HORIZONS
from otk.sets.earth_science.p5.water_cycle import STEPS

SEEDS = 300
SPECS = (*EARTH_SECTIONS, *FOOD_WEBS, *CELL_DIAGRAMS, *SOIL_PROFILES, *WATER_CYCLES,
         *FLOWERS, *FOOD_CHAIN_PICTURES, *ROCK_CYCLES, *PLATE_PICTURES, *HEARTS,
         *DIGESTIVE_PICTURES, *BREATHING_PICTURES, *PLANT_PICTURES, *ROCK_LAYERS)


def _stem(question) -> str:
    return " ".join(b.text for b in question.stem if b.kind == "text")


def _image(question) -> str:
    return next(b.asset_id for b in question.stem if b.kind == "image")


def _answer(question) -> str:
    return " ".join(b.text for b in question.choices[question.answer].content)


def test_every_spec_is_drawable_with_a_unique_ascii_id():
    ids = [spec.asset_id for spec in SPECS]
    assert len(set(ids)) == len(ids) and all(i.isascii() for i in ids)
    assert all(is_diagram(i) for i in ids)


def test_the_earth_layers_match_the_unit_and_every_numbering_is_used_once():
    assert tuple(shell.name for shell in SHELLS) == EARTH_LAYERS
    assert {spec.numbers for spec in EARTH_SECTIONS} == set(permutations((1, 2, 3)))


def test_the_layer_answer_is_read_from_the_numbering_in_the_picture():
    by_id = {spec.asset_id: spec for spec in EARTH_SECTIONS}
    elements = {shell.name: shell.elements for shell in SHELLS}
    for seed in range(SEEDS):
        question = generate("geo.earth_interior_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        number = re.search(r"หมายเลข (\d)", stem)
        if "คือชั้นใด" in stem:
            assert answer == spec.layer_of(int(number.group(1)))
        elif "คือหมายเลขใด" in stem:
            layer = next(name for name, e in elements.items() if f"ที่มี{e}เป็น" in stem)
            assert answer == f"หมายเลข {spec.numbers[EARTH_LAYERS.index(layer)]}"
        else:
            assert answer == elements[spec.layer_of(int(number.group(1)))]


def _chains_by_brute_force(web) -> int:
    """Count producer-to-top paths by trying every ordered run of organisms."""
    letters = [o.letter for o in web.organisms]
    eats = {o.letter: set(o.eats) for o in web.organisms}
    producers = {o.letter for o in web.organisms if not o.eats}
    tops = {o.letter for o in web.organisms if o.eats
            and not any(o.letter in eats[x] for x in letters)}
    count = 0
    for size in range(2, len(letters) + 1):
        for run in permutations(letters, size):
            if run[0] in producers and run[-1] in tops and all(
                    a in eats[b] for a, b in zip(run, run[1:])):
                count += 1
    return count


def test_every_web_answer_follows_its_arrows():
    by_id = {web.asset_id: web for web in FOOD_WEBS}
    for web in FOOD_WEBS:
        letters = {o.letter for o in web.organisms}
        assert all(set(o.eats) <= letters for o in web.organisms)
        assert web.producers() and web.tops()
        assert len(web.chains()) == _chains_by_brute_force(web)
    for seed in range(SEEDS):
        question = generate("ecology.food_web_diagram", Random(seed))
        web, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        if "ผู้ผลิตทั้งหมด" in stem:
            assert answer == " และ".join(o.name for o in web.producers())
        elif "เป็นอาหาร" in stem:
            food = next(o for o in web.organisms if f"กิน{o.name}เป็นอาหาร" in stem)
            assert answer == " และ".join(o.name for o in web.eaters_of(food.letter))
        elif "กี่โซ่" in stem:
            assert answer == f"{_chains_by_brute_force(web)} โซ่"
        else:
            assert answer == " และ".join(o.name for o in web.tops())


def test_every_cell_numbers_its_own_parts_only():
    for spec in CELL_DIAGRAMS:
        assert len(set(spec.labelled)) == len(spec.labelled)
        assert set(spec.labelled) <= set(PLANT_PARTS)
        if spec.kind == "animal":
            assert not {"ผนังเซลล์", "คลอโรพลาสต์"} & set(spec.labelled)


def test_the_cell_answer_is_read_from_the_numbering_in_the_picture():
    by_id = {spec.asset_id: spec for spec in CELL_DIAGRAMS}
    for seed in range(SEEDS):
        question = generate("cell.cell_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        if "คือส่วนใด" in stem:
            number = int(re.search(r"หมายเลข (\d)", stem).group(1))
            assert answer == spec.labelled[number - 1]
        elif "เซลล์พืชหรือเซลล์สัตว์" in stem:
            assert answer.startswith("เซลล์พืช" if spec.kind == "plant" else "เซลล์สัตว์")


def test_the_new_pictures_follow_their_units_tables():
    assert tuple(h.name for h in HORIZONS) == SOIL_HORIZONS
    assert tuple(s.name for s in STEPS) == WATER_STEPS
    assert tuple(p.name for p in FLOWER_PARTS) == FLOWER_PART_NAMES
    for spec in (*SOIL_PROFILES, *WATER_CYCLES):
        assert sorted(spec.numbers) == list(range(1, len(spec.numbers) + 1))
    for spec in FLOWERS:
        assert sorted(spec.labelled) == sorted(FLOWER_PART_NAMES)
    for spec in FOOD_CHAIN_PICTURES:
        assert sorted(spec.order) == sorted(CHAIN_PLACES)


def _numbered(question) -> int:
    return int(re.search(r"หมายเลข (\d)", _stem(question)).group(1))


def test_the_soil_and_water_answers_are_read_from_the_numbering():
    soil = {spec.asset_id: spec for spec in SOIL_PROFILES}
    for seed in range(SEEDS):
        question = generate("geo.soil_profile_diagram", Random(seed))
        spec, stem, answer = soil[_image(question)], _stem(question), _answer(question)
        if "คือชั้นใด" in stem:
            assert answer == spec.horizon_of(_numbered(question))
        elif "คือหมายเลขใด" in stem:
            horizon = next(h for h in HORIZONS if h.description in stem)
            assert answer == f"หมายเลข {spec.numbers[SOIL_HORIZONS.index(horizon.name)]}"
        else:
            name = spec.horizon_of(_numbered(question))
            assert answer == next(h.description for h in HORIZONS if h.name == name)
    water = {spec.asset_id: spec for spec in WATER_CYCLES}
    for seed in range(SEEDS):
        question = generate("geo.water_cycle_diagram", Random(seed))
        spec, stem, answer = water[_image(question)], _stem(question), _answer(question)
        if "แสดงกระบวนการใด" in stem:
            assert answer == spec.step_of(_numbered(question))
        elif "หมายเลขใดแสดง" in stem:
            step = next(name for name in WATER_STEPS if stem.endswith(name))
            assert answer == f"หมายเลข {spec.numbers[WATER_STEPS.index(step)]}"
        else:
            assert spec.step_of(int(answer.split()[1])) in WATER_STEPS


def test_the_flower_answer_is_read_from_the_numbering():
    flowers = {spec.asset_id: spec for spec in FLOWERS}
    job = {p.name: p.function for p in FLOWER_PARTS}
    for seed in range(SEEDS):
        question = generate("plant.flower_diagram", Random(seed))
        spec, stem, answer = flowers[_image(question)], _stem(question), _answer(question)
        if "คือส่วนใด" in stem:
            assert answer == spec.labelled[_numbered(question) - 1]
        elif "ทำหน้าที่ใด" in stem:
            assert answer == job[spec.labelled[_numbered(question) - 1]]
        else:
            part = "รังไข่" if stem.endswith("ผล") else "ออวุล"
            assert answer == f"หมายเลข {spec.number_of(part)}"


def test_the_chain_answer_follows_the_drawn_order():
    pictures = {spec.asset_id: spec for spec in FOOD_CHAIN_PICTURES}
    for seed in range(SEEDS):
        question = generate("ecology.food_chain_diagram", Random(seed))
        spec, stem, answer = pictures[_image(question)], _stem(question), _answer(question)
        key = dict(re.findall(r"([ABCD]) คือ(\S+)", stem))
        chain = [key[letter] for letter in spec.order]
        assert any(tuple(chain) == c.members for c in FOOD_CHAINS)
        if "มีบทบาทใด" in stem:
            member = next(m for m in chain if f"แผนภาพ {m}มีบทบาท" in stem)
            assert answer == ROLES[chain.index(member)]
        else:
            role = next(r for r in ROLES if stem.endswith(f"เป็น{r}"))
            assert answer == chain[ROLES.index(role)]


def test_the_rock_stage_is_found_by_following_the_arrows_from_magma():
    by_id = {spec.asset_id: spec for spec in ROCK_CYCLES}
    arrows = [(ROCK_STAGES.index(a), ROCK_STAGES.index(b)) for a, b, _ in ROCK_CYCLE_ARROWS]
    for seed in range(SEEDS):
        question = generate("geo.rock_cycle_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        if "ไล่ตามลูกศรจากแมกมา" in stem:
            letter = re.search(r"ตัวอักษร ([A-E]) คือ", stem).group(1)
            stage = spec.letters.index(letter)
            outgoing = [b for a, b in arrows if a == stage]
            incoming = [a for a, b in arrows if b == stage]
            # Igneous follows magma; metamorphic leads to it; the sediment pair is
            # told apart by which of them the igneous rock turns into.
            if 0 in incoming:
                expected = "หินอัคนี"
            elif 0 in outgoing:
                expected = "หินแปร"
            elif 1 in incoming:
                expected = "ตะกอน"
            else:
                expected = "หินตะกอน"
            assert answer == expected, (seed, stem)
        elif "แสดงกระบวนการใด" in stem:
            number = int(re.search(r"ลูกศรหมายเลข (\d)", stem).group(1))
            assert answer == ROCK_CYCLE_ARROWS[spec.numbers.index(number)][2]
        else:
            process = next(p for _, _, p in ROCK_CYCLE_ARROWS if stem.endswith(f"แสดง{p}"))
            index = next(i for i, (_, _, p) in enumerate(ROCK_CYCLE_ARROWS) if p == process)
            assert answer == f"หมายเลข {spec.numbers[index]}"


def test_the_plate_answers_belong_to_the_drawn_boundary():
    by_id = {spec.asset_id: spec for spec in PLATE_PICTURES}
    for seed in range(SEEDS):
        question = generate("geo.plate_boundary_diagram", Random(seed))
        boundary = next(b for b in BOUNDARIES if b.name == by_id[_image(question)].boundary)
        assert _answer(question) in (boundary.name, boundary.example, boundary.motion)


def test_the_heart_answers_follow_the_blood_loop():
    by_id = {spec.asset_id: spec for spec in HEARTS}
    for seed in range(SEEDS):
        question = generate("body.heart_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        if "คือห้องใด" in stem:
            number = int(re.search(r"ห้องหมายเลข (\d)", stem).group(1))
            assert answer == spec.chamber_of(number)
        elif "สูบฉีดเลือดออกไปยัง" in stem:
            place = "ปอด" if stem.endswith("ปอด") else "ส่วนต่าง ๆ ของร่างกาย"
            sender = BLOOD_LOOP[(BLOOD_LOOP.index(place) - 1) % len(BLOOD_LOOP)]
            assert answer == f"ห้องหมายเลข {spec.numbers[CHAMBERS.index(sender)]}"
        else:
            number = int(re.search(r"ห้องหมายเลข (\d)", stem).group(1))
            chamber = spec.chamber_of(number)
            after_lungs = BLOOD_LOOP.index("ปอด") < BLOOD_LOOP.index(chamber) < BLOOD_LOOP.index(
                "ส่วนต่าง ๆ ของร่างกาย")
            assert answer.startswith("เลือดที่มีออกซิเจนสูง" if after_lungs else "เลือดที่มีออกซิเจนต่ำ")


def test_the_digestive_answers_follow_the_food_path():
    by_id = {spec.asset_id: spec for spec in DIGESTIVE_PICTURES}
    assert tuple(o.name for o in DIGESTIVE_ORGANS) == DIGESTIVE_NAMES
    for seed in range(SEEDS):
        question = generate("body.digestive_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        if "เคลื่อนต่อไปยัง" in stem:
            source = spec.organ_of(int(re.search(r"หมายเลข (\d) จะ", stem).group(1)))
            nxt = FOOD_PATH[FOOD_PATH.index(source) + 1]
            assert answer == f"หมายเลข {spec.numbers[DIGESTIVE_NAMES.index(nxt)]}"
        elif "คืออวัยวะใด" in stem:
            assert answer == spec.organ_of(int(re.search(r"หมายเลข (\d)", stem).group(1)))


def test_the_breathing_answers_follow_the_air_path():
    by_id = {spec.asset_id: spec for spec in BREATHING_PICTURES}
    for seed in range(SEEDS):
        question = generate("body.breathing_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        numbers = [int(n) for n in re.findall(r"หมายเลข (\d)", stem)]
        if "คือส่วนใด" in stem:
            assert answer == spec.part_of(numbers[0])
        elif "ก่อน" in stem and len(numbers) == 2:
            parts = [spec.part_of(n) for n in numbers]
            first = min(parts, key=AIR_PATH.index)
            assert answer.startswith(f"ส่วนหมายเลข {numbers[parts.index(first)]} ก่อน")


def test_the_plant_answers_belong_to_the_numbered_organ():
    by_id = {spec.asset_id: spec for spec in PLANT_PICTURES}
    for seed in range(SEEDS):
        question = generate("plant.organ_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        organ = spec.organ_of(int(re.search(r"หมายเลข (\d)", stem).group(1)))
        if "คือส่วนใด" in stem:
            assert answer == organ
        elif "ทำหน้าที่ใด" in stem:
            assert answer in ORGAN_JOBS[organ]
        else:
            assert answer in ORGAN_FAILURES[organ]


def test_the_layer_answers_read_bottom_to_top():
    by_id = {spec.asset_id: spec for spec in ROCK_LAYERS}
    environment = {find.fossils: find.environment for find in FINDS}
    for seed in range(SEEDS):
        question = generate("geo.rock_layers_diagram", Random(seed))
        spec, stem, answer = by_id[_image(question)], _stem(question), _answer(question)
        found = dict(re.findall(r"ชั้น ([A-D]) พบ(.+?)(?= ชั้น [A-D] พบ| ชั้นหินใด| ขณะที่| เมื่อเวลา)", stem))
        envs = [environment[found[letter]] for letter in spec.letters]
        if "อายุมากที่สุด" in stem:
            assert answer == f"ชั้น {spec.letters[0]}"
        elif "อายุน้อยที่สุด" in stem:
            assert answer == f"ชั้น {spec.letters[-1]}"
        elif "กำลังเกิด" in stem:
            letter = re.search(r"ขณะที่ชั้น ([A-D])", stem).group(1)
            assert answer == envs[spec.letters.index(letter)]
        else:
            assert answer == f"จาก{envs[0]} เปลี่ยนเป็น{envs[-1]}"

"""Tests for the ฟิสิกส์ ไฟฟ้า numeric drills and circuit diagrams.

The classify types (ปริมาณไฟฟ้า, สิ่งที่มีผลต่อความต้านทาน, อนุกรม/ขนาน) and the two
concept banks are covered generically by ``test_classify_types.py`` and
``test_concept_types.py``. What is specific to ไฟฟ้า is the arithmetic, so these
re-derive each answer from the numbers in the stem: V = IR, R = ρL/A, P = VI,
P = I²R, W = Pt, and the kWh a bill is counted in. The circuit types are checked
against ``CIRCUIT_SPECS`` — the same table the schematics are drawn from — so a
picture that stops matching its answer fails here.
"""

from __future__ import annotations

import random
import re

import pytest

from otk.core import REGISTRY, catalog, generate
from otk.core.curriculum_science import SCIENCE_WAVE_D_KEYS
from otk.sets.physics.m3.series_and_parallel_circuits import CIRCUIT_SPECS, KIND_LABELS

# Wave D adds its own ``elec.``-prefixed sets (V-I graphs, meter use, resistor
# circuit diagrams) with their own curriculum-unit topics; only the legacy
# ม.3 study-sheet types below file under the shared "ไฟฟ้า" topic.
ELEC_KEYS = sorted(k for k in REGISTRY if k.startswith("elec.") and k not in SCIENCE_WAVE_D_KEYS)


def _stem(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _answer(q) -> str:
    b = q.choices[q.answer].content[0]
    return b.text if b.kind == "text" else b.tex


def _grab(pattern: str, s: str) -> float | None:
    m = re.search(pattern, s)
    return float(m.group(1)) if m else None


def _values(q) -> set[str]:
    return {b.tex for c in q.choices for b in c.content if b.kind == "math"}


# ── The formulas hold ────────────────────────────────────────────────────────

def test_ohms_law_relates_v_i_and_r():
    rng = random.Random(1)
    seen = set()
    for _ in range(900):
        q = generate("elec.ohms_law", rng)
        s, ans = _stem(q), float(_answer(q))
        v = _grab(r"([\d.]+) โวลต์", s)
        i = _grab(r"([\d.]+) แอมแปร์", s)
        r = _grab(r"([\d.]+) โอห์ม", s)
        if "จงหาความต่างศักย์" in s:
            v, tag = ans, "V"
        elif "จงหากระแสไฟฟ้า" in s:
            i, tag = ans, "I"
        else:
            r, tag = ans, "R"
        seen.add(tag)
        assert abs(v - i * r) < 1e-9, s
    assert seen == {"V", "I", "R"}              # asked every way round


def test_resistivity_is_rho_l_over_a():
    rng = random.Random(2)
    seen = set()
    for _ in range(900):
        q = generate("elec.resistivity", rng)
        s, ans = _stem(q), float(_answer(q))
        rho = _grab(r"สภาพต้านทาน ([\d.]+)×", s)
        area = _grab(r"พื้นที่หน้าตัด ([\d.]+)×", s)
        # "ยาว N เมตร" in both stems that give a length; the stem that *asks* for
        # one says "จงหาความยาวของลวด (เมตร)", with no number to match.
        length = _grab(r"ยาว ([\d.]+) เมตร", s)
        res = _grab(r"ความต้านทาน(?:ได้)? ([\d.]+) โอห์ม", s)
        if res is None:
            res, tag = ans, "R"
        elif rho is None:
            rho, tag = ans, "rho"
        else:
            length, tag = ans, "L"
        seen.add(tag)
        # ρ and A are both ×10⁻⁶ in their own units, so the powers cancel exactly.
        assert abs(res * area - rho * length) < 1e-9, s
    assert seen == {"R", "rho", "L"}


def test_resistance_ratio_scales_with_length_and_inversely_with_area():
    rng = random.Random(3)
    seen = set()
    for _ in range(600):
        q = generate("elec.resistance_ratio", rng)
        s, ans = _stem(q), float(_answer(q))
        lf = _grab(r"ยาวเป็น ([\d.]+) เท่า", s)
        grow = _grab(r"พื้นที่หน้าตัดเป็น ([\d.]+) เท่า", s)
        shrink = _grab(r"พื้นที่หน้าตัดเหลือ 1 ใน ([\d.]+)", s)
        if grow is not None:
            seen.add("grow")
            assert abs(ans - lf / grow) < 1e-9, s
        else:
            seen.add("shrink")
            assert abs(ans - lf * shrink) < 1e-9, s
    assert seen == {"grow", "shrink"}           # area both ways


def test_power_is_voltage_times_current():
    rng = random.Random(4)
    seen = set()
    for _ in range(900):
        q = generate("elec.power", rng)
        s, ans = _stem(q), float(_answer(q))
        p = _grab(r"([\d.]+) วัตต์", s)
        v = _grab(r"([\d.]+) โวลต์", s)
        i = _grab(r"([\d.]+) แอมแปร์", s)
        if "ใช้กำลังไฟฟ้าเท่าใด" in s:
            p, tag = ans, "P"
        elif "มีกระแสไฟฟ้าผ่านเท่าใด" in s:
            i, tag = ans, "I"
        else:
            v, tag = ans, "V"
        seen.add(tag)
        assert abs(p - v * i) < 1e-9, s
    assert seen == {"P", "I", "V"}


def test_power_forms_square_the_right_quantity():
    rng = random.Random(5)
    seen = set()
    for _ in range(900):
        q = generate("elec.power_forms", rng)
        s, ans = _stem(q), float(_answer(q))
        r = _grab(r"([\d.]+) โอห์ม", s)
        i = _grab(r"([\d.]+) แอมแปร์", s)
        v = _grab(r"([\d.]+) โวลต์", s)
        p = _grab(r"([\d.]+) วัตต์", s)
        if "จงหาความต้านทาน" in s:                # P, I → R = P/I²
            seen.add("R")
            assert abs(ans * i * i - p) < 1e-9, s
        elif v is not None:                       # V, R → P = V²/R
            seen.add("V2R")
            assert abs(ans * r - v * v) < 1e-9, s
        else:                                     # I, R → P = I²R
            seen.add("I2R")
            assert abs(ans - i * i * r) < 1e-9, s
    assert seen == {"R", "V2R", "I2R"}


def test_energy_is_power_times_time_in_seconds():
    rng = random.Random(6)
    seen = set()
    for _ in range(1200):
        q = generate("elec.energy", rng)
        s, ans = _stem(q), float(_answer(q))
        if "คูลอมบ์" in s:                        # W = QV
            seen.add("QV")
            charge = _grab(r"([\d.]+) คูลอมบ์", s)
            volts = _grab(r"([\d.]+) โวลต์", s)
            assert abs(ans - charge * volts) < 1e-9, s
            continue
        p = _grab(r"([\d.]+) วัตต์", s)
        # Match on the number, not the word: "วินาที" ends in "นาที".
        mins = _grab(r"([\d.]+) นาที", s)
        if mins is not None:                      # t เป็นนาที — ต้องแปลงเป็นวินาที
            seen.add("minutes")
            assert abs(ans - p * mins * 60) < 1e-9, s
            # The whole point of this variant: the unconverted value is offered.
            assert str(int(p * mins)) in _values(q), s
            continue
        secs = _grab(r"([\d.]+) วินาที", s)
        if "กำลังไฟฟ้าเท่าใด" in s:                # W, t → P
            seen.add("P")
            joules = _grab(r"([\d.]+) จูล", s)
            assert abs(ans * secs - joules) < 1e-9, s
        else:                                     # P, t → W
            seen.add("seconds")
            assert abs(ans - p * secs) < 1e-9, s
    assert seen == {"QV", "minutes", "seconds", "P"}


def test_electricity_bill_counts_kilowatt_hours():
    rng = random.Random(7)
    seen = set()
    for _ in range(900):
        q = generate("elec.electricity_bill", rng)
        s, ans = _stem(q), float(_answer(q))
        hours = _grab(r"วันละ ([\d.]+) ชั่วโมง", s)
        days = _grab(r"เป็นเวลา ([\d.]+) วัน", s)
        watts = _grab(r"ขนาด ([\d.]+) วัตต์", s)
        if watts is None:                         # หน่วย, ชั่วโมง → กำลังไฟฟ้า (วัตต์)
            seen.add("watts")
            units = _grab(r"ใช้ไฟฟ้าไป ([\d.]+) หน่วย", s)
            assert abs(ans * hours * days / 1000 - units) < 1e-9, s
            continue
        units = watts / 1000 * hours * days
        rate = _grab(r"หน่วยละ ([\d.]+) บาท", s)
        if rate is None:                          # จำนวนหน่วยไฟฟ้า
            seen.add("units")
            assert abs(ans - units) < 1e-9, s
        else:                                     # ค่าไฟเป็นบาท
            seen.add("baht")
            assert abs(ans - units * rate) < 1e-9, s
    assert seen == {"watts", "units", "baht"}


# ── The circuit diagrams agree with what is drawn ────────────────────────────

def test_circuit_specs_work_out_whole():
    # A student who reasons correctly must land on a value, not near one.
    for spec in CIRCUIT_SPECS:
        assert abs(spec.total - round(spec.total)) < 1e-9, spec
        assert abs(spec.current - round(spec.current)) < 1e-9, spec


def test_circuit_spec_asset_ids_are_unique_and_valid():
    from otk.core.render.assets import ASSET_ID_RE
    ids = [spec.asset_id for spec in CIRCUIT_SPECS]
    assert len(ids) == len(set(ids))
    assert all(ASSET_ID_RE.fullmatch(i) for i in ids)


@pytest.mark.parametrize("key,attr", [("elec.circuit_resistance", "total"),
                                      ("elec.circuit_current", "current")])
def test_circuit_answers_match_the_drawn_schematic(key, attr):
    specs = {s.asset_id: s for s in CIRCUIT_SPECS}
    rng = random.Random(8)
    seen = set()
    for _ in range(900):
        q = generate(key, rng)
        img = q.stem[0]
        assert img.kind == "image"
        spec = specs[img.asset_id]                # a real, shipped schematic
        seen.add(spec.kind)
        assert float(_answer(q)) == pytest.approx(getattr(spec, attr))
    assert seen == {"series", "parallel", "mixed"}


def test_circuit_type_names_the_connection_drawn():
    specs = {s.asset_id: s for s in CIRCUIT_SPECS}
    rng = random.Random(9)
    seen = set()
    for _ in range(600):
        q = generate("elec.circuit_type", rng)
        spec = specs[q.stem[0].asset_id]
        seen.add(spec.kind)
        assert _answer(q) == KIND_LABELS[spec.kind]
    assert seen == {"series", "parallel", "mixed"}


def test_circuit_alt_text_does_not_give_the_answer_away():
    # In a printed worksheet an image renders as its alt text alone, so naming
    # the connection there would answer elec.circuit_type outright.
    rng = random.Random(10)
    for key in ["elec.circuit_type", "elec.circuit_resistance", "elec.circuit_current"]:
        alt = generate(key, rng).stem[0].alt
        assert alt
        assert not any(word in alt for word in ("อนุกรม", "ขนาน", "ผสม"))


def test_every_circuit_asset_resolves():
    from otk.core.render.assets import shipped_asset
    for spec in CIRCUIT_SPECS:
        assert shipped_asset(spec.asset_id) is not None, spec.asset_id


# ── Catalog wiring ───────────────────────────────────────────────────────────

# The ไฟฟ้า sets written against the ม.5 ฟิสิกส์เพิ่มเติม course. Everything else
# under ``elec.`` came from the ม.3 study sheet and keeps that legacy grade.
UPPER_SECONDARY_KEYS = {
    "elec.energy_charge_voltage",
    "elec.resistance_network_application",
    "elec.electric_potential_foundation",
    "elec.electric_potential_application",
    "elec.power_emf_foundation",
    "elec.power_emf_application",
}


@pytest.mark.parametrize("key", ELEC_KEYS)
def test_catalog_places_them_under_physics_electricity(key):
    entry = {t["key"]: t for t in catalog()}[key]
    expected_level = "ม.5" if key in UPPER_SECONDARY_KEYS else "ม.3"
    assert (entry["subject"], entry["legacy_level"], entry["topic"]) == \
        ("ฟิสิกส์", expected_level, "ไฟฟ้า")
    assert entry["level"]


def test_electricity_is_a_second_topic_under_physics():
    # The Phase 5 waves add curriculum-unit topics of their own (forces, magnets,
    # friction coefficient, vector resultants, ...); the legacy physics sets still
    # file under exactly these two.
    from otk.core.curriculum_science import (
        SCIENCE_WAVE_D_KEYS,
        SCIENCE_WAVE_E_KEYS,
        SCIENCE_WAVE_F_KEYS,
        SCIENCE_WAVE_G_KEYS,
        SCIENCE_POSN_PHYSICS_KEYS,
    )
    later_waves = (SCIENCE_WAVE_D_KEYS | SCIENCE_WAVE_E_KEYS
                   | SCIENCE_WAVE_F_KEYS | SCIENCE_WAVE_G_KEYS
                   | SCIENCE_POSN_PHYSICS_KEYS)
    topics = {t["topic"] for t in catalog()
              if t["subject"] == "ฟิสิกส์" and t["key"] not in later_waves}
    assert topics == {"คลื่นและแสง", "ไฟฟ้า"}

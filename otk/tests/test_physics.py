"""Tests for the ฟิสิกส์ คลื่นและแสง numeric drills and concept banks.

The classify types (wave/spectrum/light/optics and the two image-nature sets) are
covered by ``test_classify_types.py``. These pin the parts specific to physics:
the numeric answers are the *right* value (reflection = incidence, f = R/2,
n·v = c, E = Φ/A), and each concept-bank item answers with its own correct choice.
"""

from __future__ import annotations

import random
import re

import pytest

from otk.core import REGISTRY, catalog, generate
from otk.kit.concept_bank import ConceptBankType
from otk.sets.physics.m3.waves import WAVE_SPECS

NUMERIC_KEYS = ["phys.reflection_law", "phys.plane_mirror_image",
                "phys.curved_mirror", "phys.refraction", "phys.illuminance",
                "phys.period_frequency", "phys.wave_speed"]
# Concept-bank behaviour is tested generically in test_concept_types.py; here we
# only keep the physics keys for the catalog-placement check below.
CONCEPT_KEYS = sorted(k for k, t in REGISTRY.items()
                      if isinstance(t, ConceptBankType) and k.startswith("phys."))


def _stem(q) -> str:
    return q.stem[0].text


def _answer(q) -> str:
    b = q.choices[q.answer].content[0]
    return b.text if b.kind == "text" else b.tex


# ── The numeric answers are physically correct ───────────────────────────────

def test_reflection_law_is_incidence_or_double():
    rng = random.Random(1)
    seen = set()
    for _ in range(400):
        q = generate("phys.reflection_law", rng)
        s = _stem(q)
        angle = int(re.search(r"(\d+)°", s).group(1))
        between = "มุมระหว่างรังสี" in s
        seen.add(between)
        assert _answer(q) == str(2 * angle if between else angle)
    assert seen == {True, False}                       # both variants come up


def test_plane_mirror_image_preserves_size_and_distance():
    rng = random.Random(2)
    for _ in range(400):
        q = generate("phys.plane_mirror_image", rng)
        s = _stem(q)
        val = int(re.search(r"(\d+) เซนติเมตร", s).group(1))
        expected = 2 * val if "ระยะจากวัตถุถึงภาพ" in s else val
        assert _answer(q) == str(expected)


def test_curved_mirror_focal_is_half_the_radius():
    rng = random.Random(3)
    for _ in range(400):
        q = generate("phys.curved_mirror", rng)
        s = _stem(q)
        val = int(re.search(r"(\d+) เซนติเมตร", s).group(1))
        if "จงหาความยาวโฟกัส" in s:                     # given R → f = R/2
            assert _answer(q) == str(val // 2)
        else:                                          # given f → R = 2f
            assert _answer(q) == str(2 * val)


def test_refraction_index_times_speed_is_c():
    rng = random.Random(4)
    for _ in range(400):
        q = generate("phys.refraction", rng)
        s = _stem(q)
        a = float(_answer(q))
        if "เป็นกี่เท่าของ" in s:                        # Wave H: speed ratio of two media
            n1, n2 = (float(x) for x in re.findall(r"ดัชนีหักเห ([\d.]+)", s))
            assert abs(a - n2 / n1) < 1e-9
        elif "จงหาดัชนีหักเห" in s:                      # given v → n
            v = float(re.search(r"เท่ากับ ([\d.]+)×10", s).group(1))
            assert abs(a * v - 3) < 1e-9
        else:                                          # given n → v
            n = float(re.search(r"ดัชนีหักเห ([\d.]+) จงหา", s).group(1))
            assert abs(a * n - 3) < 1e-9


def test_illuminance_is_flux_over_area():
    rng = random.Random(5)
    for _ in range(400):
        q = generate("phys.illuminance", rng)
        s = _stem(q)
        a = int(_answer(q))
        if "จงหาความสว่าง" in s:                         # E = Φ / A
            phi = int(re.search(r"ฟลักซ์ส่องสว่าง (\d+) ลูเมน", s).group(1))
            area = int(re.search(r"พื้นที่ (\d+) ตารางเมตร", s).group(1))
            assert a == phi // area
        else:                                          # Φ = E × A
            area = int(re.search(r"พื้นราบ (\d+) ตารางเมตร", s).group(1))
            e = int(re.search(r"ความสว่าง (\d+) ลักซ์", s).group(1))
            assert a == e * area


def test_period_and_frequency_are_reciprocal():
    rng = random.Random(6)
    seen = set()
    for _ in range(500):
        q = generate("phys.period_frequency", rng)
        s = _stem(q)
        val = float(_answer(q))
        asked_freq = "จงหาความถี่" in s
        seen.add(asked_freq)
        if "ครบ" in s:                                  # N cycles in t seconds
            n = int(re.search(r"ครบ (\d+) รอบ", s).group(1))
            t = int(re.search(r"ในเวลา (\d+) วินาที", s).group(1))
            expected = n / t if asked_freq else t / n
        elif asked_freq:                                # given T → f = 1/T
            period = float(re.search(r"คาบ ([\d.]+) วินาที", s).group(1))
            expected = 1 / period
        else:                                           # given f → T = 1/f
            freq = float(re.search(r"ความถี่ ([\d.]+) เฮิรตซ์", s).group(1))
            expected = 1 / freq
        assert abs(val - expected) < 1e-9
    assert seen == {True, False}                        # asks both directions


def _grab(pattern, s):
    m = re.search(pattern, s)
    return float(m.group(1)) if m else None


def test_wave_speed_relates_by_v_equals_f_lambda():
    rng = random.Random(8)
    seen = set()
    for _ in range(1200):
        q = generate("phys.wave_speed", rng)
        s = _stem(q)
        val = float(_answer(q))
        v = _grab(r"อัตราเร็ว ([\d.]+) เมตร", s)
        lam = _grab(r"ความยาวคลื่น ([\d.]+) เมตร", s)
        # frequency may be given directly, or as a period (f = 1/T) — same input.
        t = _grab(r"คาบ ([\d.]+) วินาที", s)
        f = _grab(r"ความถี่ ([\d.]+) เฮิรตซ์", s)
        freq = f if f is not None else (1 / t if t is not None else None)
        if t is not None:
            seen.add("period")                           # the คาบ variant shows up
        if "จงหาอัตราเร็ว" in s:                          # given f/T, λ → v = fλ
            seen.add("v")
            assert abs(val - freq * lam) < 1e-9
        elif "จงหาความถี่" in s:                          # given v, λ → f = v/λ
            seen.add("f")
            assert abs(val * lam - v) < 1e-9
        else:                                            # given v, f/T → λ = v/f
            seen.add("lam")
            assert abs(val * freq - v) < 1e-9
    assert seen == {"v", "f", "lam", "period"}           # all ways, incl. คาบ


# ── Reading a wave graph ─────────────────────────────────────────────────────

def test_wave_diagram_answer_matches_the_drawn_wave():
    specs = {s.asset_id: s for s in WAVE_SPECS}
    rng = random.Random(7)
    seen = set()
    for _ in range(600):
        q = generate("phys.wave_diagram", rng)
        img = q.stem[0]
        assert img.kind == "image"
        spec = specs[img.asset_id]                      # a real, shipped wave
        prompt = q.stem[1].text
        ans = int(_answer(q))
        if "กี่ลูก" in prompt:
            expected, tag = spec.cycles, "count"
        elif "ความยาวคลื่น" in prompt:
            expected, tag = spec.wavelength, "wavelength"
        else:
            expected, tag = spec.amp, "amplitude"
        seen.add(tag)
        assert ans == expected
    assert seen == {"count", "wavelength", "amplitude"}


def test_every_wave_asset_resolves():
    from otk.core.render.assets import shipped_asset
    for spec in WAVE_SPECS:
        assert shipped_asset(spec.asset_id) is not None, spec.asset_id


# ── Catalog wiring ───────────────────────────────────────────────────────────

# The คลื่นและแสง sets written against the ม.5 ฟิสิกส์เพิ่มเติม course. Everything
# else came from the ม.3 study sheet and keeps that legacy grade — including
# phys.curved_mirror and phys.refraction, which are filed at ม.5 but were authored
# at ม.3 and keep their legacy identity.
UPPER_SECONDARY_KEYS = {
    "phys.spherical_mirror_foundation",
    "phys.spherical_mirror_application",
    "phys.refraction_index_foundation",
    "phys.refraction_index_application",
}


@pytest.mark.parametrize("key", NUMERIC_KEYS + CONCEPT_KEYS + ["phys.wave_diagram"])
def test_catalog_places_them_under_physics_waves_and_light(key):
    entry = {t["key"]: t for t in catalog()}[key]
    expected_level = "ม.5" if key in UPPER_SECONDARY_KEYS else "ม.3"
    assert (entry["subject"], entry["legacy_level"], entry["topic"]) == \
        ("ฟิสิกส์", expected_level, "คลื่นและแสง")
    assert entry["level"]

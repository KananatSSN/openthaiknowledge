"""Tests for เคมี ม.2 — สารบริสุทธิ์และสารผสม and การแยกสาร.

The classify tables and the concept banks are covered generically by
``test_classify_types.py`` and ``test_concept_types.py``. What is specific here
is everything those cannot see:

* the two data-reading types answer from the numbers in their own stem;
* the chromatogram types agree with ``CHROMA_SPECS`` — the same table the
  pictures are drawn from — so a diagram that stops matching its answer fails
  here, and every distance stays readable off the drawn 5 mm scale;
* the ป.6 separation layer in ``chemistry.py`` is still where it was, because
  these sets were added *beside* it rather than replacing it.
"""

from __future__ import annotations

from otk.tests._origins import keys_from

import random
import re

import pytest

from otk.core import catalog, generate
from otk.sets.chemistry.m2.separating_solutions import APPARATUS_SPECS, CHROMA_SPECS
from otk.sets.chemistry.m1.density import _AQUEOUS, _ORGANIC

SUBST_KEYS = sorted(keys_from("substances"))

# The ป.6 types these ม.2 sets sit above; see the module docstring on overlap.
P6_SEPARATION = ["chem.separation", "chem.mixture_intro", "chem.separate_solids",
                 "chem.separate_solid_liquid", "chem.magnetic_separation",
                 "chem.separation_uses"]


def _stem(q) -> str:
    return " ".join(b.text for b in q.stem if b.kind == "text")


def _answer(q) -> str:
    b = q.choices[q.answer].content[0]
    return b.text if b.kind == "text" else b.tex


def _texts(q) -> list[str]:
    return [c.content[0].text for c in q.choices if c.content[0].kind == "text"]


def _spec_of(q):
    """The ``CHROMA_SPECS`` entry the drawn stem actually shows."""
    return {s.asset_id: s for s in CHROMA_SPECS}[q.stem[0].asset_id]


# ── Catalog wiring ───────────────────────────────────────────────────────────

def test_all_twentyone_sets_are_registered():
    assert len(SUBST_KEYS) == 21


@pytest.mark.parametrize("key", SUBST_KEYS)
def test_catalog_preserves_their_legacy_chemistry_m2_placement(key):
    entry = {t["key"]: t for t in catalog()}[key]
    assert (entry["subject"], entry["legacy_level"]) == ("เคมี", "ม.2")
    assert entry["level"]
    assert entry["topic"] in ("สารบริสุทธิ์และสารผสม", "การแยกสาร")


@pytest.mark.parametrize("key", P6_SEPARATION)
def test_the_legacy_p6_separation_layer_is_preserved(key):
    # The curriculum layer may refine the displayed grade, while retaining the
    # original registration for compatibility and auditability.
    entry = {t["key"]: t for t in catalog()}[key]
    assert (entry["subject"], entry["legacy_level"]) == ("เคมี", "ป.6")
    assert entry["level"]


def test_every_new_key_is_new():
    # chemistry.py owns chem.* too, so a name collision would silently replace
    # one of its types in the registry rather than raise.
    assert not set(SUBST_KEYS) & set(P6_SEPARATION)


# ── The data-reading types answer from their own numbers ─────────────────────

def test_purity_is_decided_by_whether_the_boiling_point_holds():
    rng = random.Random(1)
    seen = set()
    for _ in range(600):
        q = generate("chem.purity_from_boiling", rng)
        s, ans = _stem(q), _answer(q)
        if "สารใดเป็นสารบริสุทธิ์" in s:            # two substances, pick one
            seen.add("compare")
            pure = re.search(r"สาร (\S+) เดือดคงที่ที่", s).group(1)
            assert ans == f"สาร {pure}", s
        elif "คงที่ตลอด" in s:                      # one substance, fixed point
            seen.add("single-pure")
            assert ans == "สารบริสุทธิ์ เพราะมีจุดเดือดคงที่", s
        else:                                       # one substance, over a range
            seen.add("single-mixed")
            assert ans == "สารผสม เพราะจุดเดือดไม่คงที่", s
    assert seen == {"compare", "single-pure", "single-mixed"}


def test_density_decides_the_layer_and_what_drains_first():
    density = {liq.name: liq.density for liq in _AQUEOUS + _ORGANIC}
    rng = random.Random(2)
    seen = set()
    for _ in range(900):
        q = generate("chem.density_layers", rng)
        s, ans = _stem(q), _answer(q)
        shown = dict(re.findall(r"(\S+) = ([\d.]+)", s))
        assert len(shown) == 2, s
        # the stem's own printed numbers must be the table's
        for name, value in shown.items():
            assert float(value) == pytest.approx(density[name]), s
        heavier = max(shown, key=lambda n: float(shown[n]))
        lighter = min(shown, key=lambda n: float(shown[n]))
        assert heavier != lighter                   # never a tie to guess at
        if "ชั้นบน" in s:
            seen.add("top")
            assert ans == lighter, s
        elif "ชั้นล่าง" in s:
            seen.add("bottom")
            assert ans == heavier, s
        else:                                       # ไขก๊อก → the bottom layer
            seen.add("drain")
            assert ans == heavier, s
    assert seen == {"top", "bottom", "drain"}


def test_density_pairs_are_always_immiscible():
    # น้ำ กับ แอลกอฮอล์ would be a wrong question, not a hard one: liquids that
    # mix form no layers at all. One aqueous and one organic, always.
    aqueous = {liq.name for liq in _AQUEOUS}
    rng = random.Random(3)
    for _ in range(300):
        shown = re.findall(r"(\S+) = [\d.]+", _stem(generate("chem.density_layers", rng)))
        assert len([n for n in shown if n in aqueous]) == 1, shown


# ── The chromatograms agree with what is drawn ───────────────────────────────

def test_chroma_specs_stay_readable_off_the_drawn_scale():
    for spec in CHROMA_SPECS:
        assert spec.solvent % 5 == 0, spec
        assert list(spec.spots) == sorted(spec.spots), spec      # nearest first
        assert len(set(spec.spots)) == len(spec.spots), spec     # no tie
        assert max(spec.spots) < spec.solvent, spec              # below the front
        for d in spec.spots:
            assert d % 5 == 0, spec                  # lands on a gridline
            rf = d / spec.solvent
            assert round(rf, 2) == pytest.approx(rf), spec       # clean 2 dp


def test_chroma_asset_ids_are_unique_and_valid():
    from otk.core.render.assets import ASSET_ID_RE
    ids = [s.asset_id for s in CHROMA_SPECS]
    assert len(ids) == len(set(ids))
    assert all(ASSET_ID_RE.fullmatch(i) for i in ids)


def test_chromatogram_reads_the_spots_that_were_drawn():
    rng = random.Random(4)
    seen = set()
    for _ in range(1200):
        q = generate("chem.chromatogram_read", rng)
        spec, s, ans = _spec_of(q), _stem(q), _answer(q)
        far, held = f"สาร {spec.label(len(spec.spots) - 1)}", f"สาร {spec.label(0)}"
        if "กี่ชนิด" in s:
            seen.add("count")
            assert int(ans) == len(spec.spots), s
        elif "ไกลที่สุด" in s:
            seen.add("far")
            assert ans == far, s
        elif "ละลาย" in s:                          # ไปไกลที่สุด = ละลายดีที่สุด
            seen.add("soluble")
            assert ans == far, s
        else:                                       # ถูกดูดซับไว้มากที่สุด
            seen.add("held")
            assert ans == held, s
    assert seen == {"count", "far", "soluble", "held"}


def test_chromatogram_offers_four_choices_even_for_two_spots():
    # A two-spot picture has only two real names, so the padding choice
    # ("ทุกสารเคลื่อนที่ได้เท่ากัน") has to carry it to a full four.
    rng = random.Random(5)
    for _ in range(400):
        q = generate("chem.chromatogram_read", rng, ask=1)
        assert len(q.choices) == 4
        assert len({c.content[0].text for c in q.choices}) == 4


def test_rf_is_the_spot_distance_over_the_solvent_front():
    rng = random.Random(6)
    letters = set()
    for _ in range(900):
        q = generate("chem.rf_value", rng)
        spec = _spec_of(q)
        letter = re.search(r"ของสาร ([A-Z])", _stem(q)).group(1)
        i = ord(letter) - ord("A")
        letters.add(letter)
        assert float(_answer(q)) == pytest.approx(spec.rf(i))
        assert float(_answer(q)) < 1                 # Rf never reaches the front
        assert len(q.choices) == 4                   # even a two-spot picture
        # the inverted ratio is offered — the mistake the item exists to catch
        assert any(float(c.content[0].tex) > 1 for c in q.choices)
    assert letters == {"A", "B", "C", "D"}           # every spot gets asked


@pytest.mark.parametrize("spec", CHROMA_SPECS, ids=lambda s: s.asset_id)
def test_every_chroma_asset_resolves(spec):
    from otk.core.render.assets import shipped_asset
    assert shipped_asset(spec.asset_id) is not None


# ── The apparatus diagrams ───────────────────────────────────────────────────

def test_apparatus_answers_name_the_set_up_drawn():
    specs = {a.asset_id: a for a in APPARATUS_SPECS}
    rng = random.Random(7)
    seen = set()
    for _ in range(600):
        q = generate("chem.apparatus_id", rng)
        spec, ans = specs[q.stem[0].asset_id], _answer(q)
        if "วิธีใด" in _stem(q):
            seen.add("method")
            assert ans == spec.method
        else:
            seen.add("use")
            assert ans in spec.examples
        assert len(set(_texts(q))) == 4              # four distinct choices
    assert seen == {"method", "use"}
    assert len(specs) == 4


def test_apparatus_alt_text_does_not_name_the_method():
    # In a printed worksheet an image renders as its alt text alone, so naming
    # the method there would answer chem.apparatus_id outright.
    for spec in APPARATUS_SPECS:
        assert spec.alt
        for word in ("กลั่น", "กรอง", "ระเหย", "กรวยแยก"):
            assert word not in spec.alt, f"{spec.code} alt names {word}"


@pytest.mark.parametrize("spec", APPARATUS_SPECS, ids=lambda s: s.code)
def test_every_apparatus_asset_resolves(spec):
    from otk.core.render.assets import shipped_asset
    assert shipped_asset(spec.asset_id) is not None


# ── Prompts fit the printed page ─────────────────────────────────────────────

def test_no_prompt_runs_off_its_column():
    """Prompts must fit the printed cell they are drawn in.

    The PDF renderer neither wraps nor clips a stem: an over-long prompt is
    simply painted past its cell and over whatever is beside it. This measures
    the rendered width of the longest prompt each type can produce against the
    width the cell actually has.

    **One column is the bar, not two.** At two columns a cell holds only about
    0.35 of the page width, and 101 of the 280 registered types overrun it — 85
    of them shipped long before these. That is a renderer limitation (no
    wrapping), not something a Thai concept prompt can be written around: no
    real question about คอลลอยด์ fits in forty characters. One column is the
    layout every type is expected to survive, and there only six types overrun.

    A character budget would be the wrong test: Thai glyph widths vary, and
    "คาร์บอนเตตระคลอไรด์" costs far more than nineteen average characters.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from otk.core.render.pdf import (A4, MARGIN_L, MARGIN_R, _apply_font,
                                       _number_offset)
    from otk.core.worksheet import Worksheet

    # Measure in the font a worksheet actually prints in. The default DejaVu
    # Sans has no Thai glyphs at all, so it would measure tofu boxes, and so
    # would a machine without Tahoma (CI's Linux runner): skip there rather than
    # pass on boxes. The rc_context keeps the measurement independent of fonts
    # other tests in the same process have prepended (pytest-xdist workers).
    if "Tahoma" not in {f.name for f in font_manager.fontManager.ttflist}:
        pytest.skip("Tahoma is not installed; the widths would be measured in another font")
    with matplotlib.rc_context():
        _measure_prompts(plt, A4, MARGIN_L, MARGIN_R, _apply_font, _number_offset, Worksheet)


def _measure_prompts(plt, A4, MARGIN_L, MARGIN_R, _apply_font, _number_offset, Worksheet):
    _apply_font(Worksheet(font_family="Tahoma"))
    columns = 1
    cell_w = (MARGIN_R - MARGIN_L) / columns
    available = cell_w * 0.94 - _number_offset(99)   # what the prompt may use

    rng = random.Random(8)
    longest = {key: max((_stem(generate(key, rng)) for _ in range(300)), key=len)
               for key in SUBST_KEYS}

    fig = plt.figure(figsize=A4)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    try:
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        page_px = fig.bbox.width
        over = {}
        for key, prompt in longest.items():
            t = ax.text(0, 0.5, prompt, fontsize=8.5, ha="left", va="top")
            width = t.get_window_extent(r).width / page_px    # page fractions
            t.remove()
            if width > available:
                over[key] = f"{width:.3f} > {available:.3f} ({len(prompt)} ch)"
        assert not over, over
    finally:
        plt.close(fig)

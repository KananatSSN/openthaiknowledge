"""Worksheet build + PDF render tests.

Pixel-exact golden hashing is fragile across matplotlib/font versions, so these
assert *structure* and *valid output* (a real multi-page PDF / PNG, correct page
counts, params flowing through) rather than a byte hash.
"""

from __future__ import annotations

import io
import re
from random import Random

import matplotlib.pyplot as plt
import pytest

from otk.core.render import render_page_png, render_pdf
from otk.core.render.pdf import _build_figures
from otk.core.worksheet import Worksheet, build_worksheet


def _cfg(**kw) -> Worksheet:
    base = dict(title="ทดสอบ", font_family="Tahoma",
                generators={"math.one_digit_plus_with_carry": 1}, num_problems=20, seed=7)
    base.update(kw)
    return Worksheet(**base)


def test_build_is_deterministic():
    c = _cfg()
    a = build_worksheet(c, Random(7))
    b = build_worksheet(c, Random(7))
    assert len(a) == 20
    assert a[0].stem[0].tex == b[0].stem[0].tex


def test_unknown_type_raises():
    with pytest.raises(ValueError):
        build_worksheet(Worksheet(generators={"math.nope": 1}, num_problems=3))


def test_bad_param_raises():
    cfg = Worksheet(generators={"math.one_digit_plus_with_carry": {"weight": 1, "params": {"zzz": 1}}},
                    num_problems=3)
    with pytest.raises(ValueError):
        build_worksheet(cfg)


def test_params_flow_through():
    cfg = Worksheet(
        generators={"math.one_digit_plus_with_carry": {"weight": 1, "params": {"lo": 7, "hi": 7}}},
        num_problems=8, seed=3, answer_key=False)
    for q in build_worksheet(cfg, Random(3)):
        a = int(re.match(r"(\d+) \+", q.stem[0].tex).group(1))
        assert a == 7                          # lo == hi forces the addend


def test_render_pdf_is_a_pdf():
    c = _cfg()
    buf = io.BytesIO()
    render_pdf(c, build_worksheet(c, Random(1)), buf)
    data = buf.getvalue()
    assert data[:5] == b"%PDF-"
    assert len(data) > 1000


def test_render_page_png_is_a_png():
    c = _cfg()
    png = render_page_png(c, build_worksheet(c, Random(1)), page=0)
    assert png[:8] == b"\x89PNG\r\n\x1a\n"


def test_page_count_sheets_plus_key():
    c = _cfg(num_problems=45, problems_per_page=20,
             answer_key=True, answer_key_columns=4)
    figs = _build_figures(c, build_worksheet(c, Random(1)))
    try:
        assert len(figs) == 4                  # 3 sheet pages + 1 answer-key page
    finally:
        for f in figs:
            plt.close(f)


def test_answer_key_uses_correct_choice():
    c = _cfg(num_problems=5, answer_key=True)
    qs = build_worksheet(c, Random(2))
    # The answer-key value equals the question's correct choice content.
    for q in qs:
        assert q.choices[q.answer].content[0].kind == "math"


def test_pdf_renders_image_question(tmp_path):
    from PIL import Image
    from otk.core.worksheet import Worksheet
    img = tmp_path / "skeleton.png"
    Image.new("RGB", (200, 300), (220, 220, 210)).save(img)
    resolver = lambda aid: img if aid == "skeleton" else None   # noqa: E731
    c = Worksheet(title="กายวิภาค", font_family="Tahoma",
                  generators={"anatomy.skeleton": 1}, num_problems=4, seed=2)
    qs = build_worksheet(c, Random(2))
    buf = io.BytesIO()
    render_pdf(c, qs, buf, asset_resolver=resolver)
    assert buf.getvalue()[:5] == b"%PDF-"


@pytest.mark.parametrize("per_page,columns", [(20, 1), (12, 1), (8, 1),
                                              (20, 2), (6, 2)])
def test_image_problem_prompt_does_not_collide_with_the_diagram(tmp_path, per_page,
                                                                columns):
    """The prompt gets its own line; the diagram must not be drawn over it.

    Both used to be placed from the cell's midpoint, so the picture landed on
    top of the words at every density. Checked across grid shapes because the
    cell is what shrinks — the collision only showed up once a cell was short.

    Drawn in a real Thai font: asking for Tahoma on Linux falls back to DejaVu
    Sans, which has no Thai glyphs and so hid the taller Loma and Garuda lines.
    """
    from PIL import Image
    from otk.core.render.fonts import default_thai_font
    from otk.core.worksheet import Worksheet
    img = tmp_path / "circuit.png"
    Image.new("RGB", (540, 300), (250, 250, 250)).save(img)   # a wide schematic
    c = Worksheet(title="วงจรไฟฟ้า", font_family=default_thai_font() or "Tahoma",
                  generators={"elec.circuit_resistance": 1},
                  num_problems=per_page, problems_per_page=per_page,
                  columns=columns, answer_key=False, seed=4)
    qs = build_worksheet(c, Random(4))
    figs = _build_figures(c, qs, lambda aid: img)              # noqa: ARG005
    fig = figs[0]
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    diagrams = [a.get_window_extent(r) for a in fig.axes[1:]]  # the inset images
    prompts = [t for t in fig.axes[0].texts if t.get_fontsize() == 8.5]
    assert len(diagrams) == per_page
    assert len(prompts) == per_page                            # every stem prompts

    for t, box in ((t, t.get_window_extent(r)) for t in prompts):
        clash = [d for d in diagrams if box.overlaps(d)]
        assert not clash, f"{t.get_text()!r} overlaps {len(clash)} diagram(s)"
    for f in figs:
        plt.close(f)


def test_edit_preview_returns_regions():
    from otk.core.render import render_edit_preview
    c = _cfg(num_problems=6)
    png, regions = render_edit_preview(c, build_worksheet(c, Random(1)))
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    keys = {r["key"] for r in regions}
    assert {"title", "level"} <= keys
    for r in regions:                       # page fractions
        assert 0 <= r["x"] <= 1 and 0 <= r["y"] <= 1


def test_edit_preview_tolerates_no_generators():
    from otk.core.render import render_edit_preview
    from otk.core.worksheet import Worksheet
    c = Worksheet(title="", font_family="Tahoma", generators={})
    png, regions = render_edit_preview(c, [])   # header-only page
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert any(r["key"] == "title" for r in regions)


# ── Wrapping and printed choices ─────────────────────────────────────────────

def _thai_cfg(**kw):
    from otk.core.render.fonts import default_thai_font
    from otk.core.worksheet import Worksheet
    base = dict(title="วิทยาศาสตร์", font_family=default_thai_font() or "Tahoma",
                generators={"math.one_digit_plus_with_carry": 1}, seed=5)
    base.update(kw)
    return Worksheet(**base)


def _long_question(n_choices: int = 4):
    """A stem far wider than any column, with wordy Thai options."""
    from otk.core.content import TextBlock
    from otk.core.question import Choice, Question
    # Long enough to overflow even a full-width column, so both grid shapes
    # exercise the wrap rather than only the narrow one.
    stem = ("แรง 4 นิวตัน กระทำต่อกล่องไปทางซ้าย และแรง 8 นิวตัน ไปทางขวา "
            "ถ้าใช้ความยาว 1 ช่องแทนแรง 1 นิวตัน และวัดจากจุดเริ่มต้นเดียวกันทุกครั้ง "
            "โดยไม่คิดแรงเสียดทานระหว่างกล่องกับพื้น แผนภาพใดถูกต้อง")
    choices = [Choice(content=[TextBlock(
        text=f"แรง: ลูกศรยาว {i + 1} ช่องชี้ไปทางซ้าย และ ลูกศรยาว 8 ช่องชี้ไปทางขวา "
             f"/ แรงลัพธ์: ลูกศรยาว {i + 1} ช่องชี้ไปทางขวา")])
        for i in range(n_choices)]
    return Question(type="phys.force_diagram_fluency", topic="แผนภาพแสดงแรง",
                    level="ป.5", stem=[TextBlock(text=stem)], choices=choices,
                    answer=2)


def _column_right(config, col: int) -> float:
    """Right edge of ``col`` (0-based) as a page fraction."""
    from otk.core.render.pdf import MARGIN_L, MARGIN_R
    cell_w = (MARGIN_R - MARGIN_L) / config.columns
    return MARGIN_L + (col + 1) * cell_w


@pytest.mark.parametrize("columns", [1, 2])
def test_a_long_prompt_wraps_inside_its_column(columns):
    """A long Thai stem used to be drawn as one line: it crossed into the next
    column and ran off the page. Every line must now sit inside its own cell."""
    from otk.core.render.pdf import _PROMPT_FONTSIZE
    cfg = _thai_cfg(columns=columns, num_problems=columns, problems_per_page=columns,
                    answer_key=False)
    figs = _build_figures(cfg, [_long_question() for _ in range(columns)])
    fig = figs[0]
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    prompts = [t for t in fig.axes[0].texts if t.get_fontsize() == _PROMPT_FONTSIZE]
    assert len(prompts) == columns
    for col, t in enumerate(prompts):
        assert "\n" in t.get_text(), "the stem was not wrapped at all"
        box = t.get_window_extent(r)
        limit = _column_right(cfg, col) * fig.bbox.width
        assert box.x1 <= limit, f"column {col} prompt overflows by {box.x1 - limit:.0f}px"
    for f in figs:
        plt.close(f)


def test_choices_are_not_printed_by_default():
    cfg = _thai_cfg(num_problems=2, problems_per_page=2, answer_key=False)
    figs = _build_figures(cfg, [_long_question(), _long_question()])
    drawn = [t.get_text() for t in figs[0].axes[0].texts]
    assert not any(text.startswith("ก.") for text in drawn)
    for f in figs:
        plt.close(f)


def test_printed_choices_are_lettered_and_stay_in_the_column():
    from otk.core.render.pdf import _CHOICE_FONTSIZE, _CHOICE_LABELS
    cfg = _thai_cfg(show_choices=True, columns=1, num_problems=1, answer_key=False)
    figs = _build_figures(cfg, [_long_question()])
    fig = figs[0]
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    texts = [t for t in fig.axes[0].texts if t.get_fontsize() == _CHOICE_FONTSIZE]
    labels = [t.get_text() for t in texts if t.get_text().endswith(".")]
    assert labels == [f"{c}." for c in _CHOICE_LABELS[:4]]
    limit = _column_right(cfg, 0) * fig.bbox.width
    for t in texts:
        assert t.get_window_extent(r).x1 <= limit
    for f in figs:
        plt.close(f)


def test_printed_choices_do_not_overlap_the_diagram(tmp_path):
    """The picture has to give up room for the options, not sit on them."""
    from PIL import Image
    from otk.core.content import ImageBlock, TextBlock
    from otk.core.question import Choice, Question
    from otk.core.render.pdf import _CHOICE_FONTSIZE
    img = tmp_path / "circuit.png"
    Image.new("RGB", (540, 300), (250, 250, 250)).save(img)
    q = Question(type="phys.circuit_symbol_fluency", topic="วงจรไฟฟ้า", level="ป.6",
                 stem=[ImageBlock(asset_id="circuit", alt="แผนภาพวงจร"),
                       TextBlock(text="จากแผนภาพ วงจรนี้ประกอบด้วยอะไรบ้าง")],
                 choices=[Choice(content=[TextBlock(text=f"เซลล์ไฟฟ้า {i} เซลล์")])
                          for i in range(1, 5)],
                 answer=0)
    cfg = _thai_cfg(show_choices=True, num_problems=2, problems_per_page=2,
                    answer_key=False)
    figs = _build_figures(cfg, [q, q], lambda aid: img)        # noqa: ARG005
    fig = figs[0]
    fig.canvas.draw()
    r = fig.canvas.get_renderer()

    diagrams = [a.get_window_extent(r) for a in fig.axes[1:]]
    assert len(diagrams) == 2
    from otk.core.render.pdf import GRID_BOTTOM
    options = [t for t in fig.axes[0].texts
               if t.get_fontsize() == _CHOICE_FONTSIZE
               and t.get_position()[1] > GRID_BOTTOM]          # not the footer
    assert len(options) == 2 * 4 * 2                           # label + body, ×4, ×2
    for t in options:
        box = t.get_window_extent(r)
        assert not [d for d in diagrams if box.overlaps(d)], t.get_text()
    for f in figs:
        plt.close(f)


def test_answer_key_leads_with_the_option_letter():
    cfg = _thai_cfg(show_choices=True, num_problems=1)
    figs = _build_figures(cfg, [_long_question()])
    key = figs[-1]
    drawn = [t.get_text() for t in key.axes[0].texts]
    assert "ค." in drawn                                       # answer index 2
    assert any(t.endswith("…") for t in drawn)                 # wording cut to fit
    for f in figs:
        plt.close(f)


def test_flow_layout_packs_by_height_not_by_problems_per_page(tmp_path):
    """With options printed, every question is a different height. The fixed
    grid overlapped them; pages are now packed by measured height, and nothing
    may spill past the foot of the page."""
    from PIL import Image
    from otk.core.content import ImageBlock, TextBlock
    from otk.core.question import Choice, Question
    from otk.core.render.pdf import GRID_BOTTOM, _CHOICE_FONTSIZE
    img = tmp_path / "circuit.png"
    Image.new("RGB", (540, 300), (250, 250, 250)).save(img)
    q = Question(type="phys.circuit_symbol_fluency", topic="วงจรไฟฟ้า", level="ป.6",
                 stem=[ImageBlock(asset_id="circuit", alt="แผนภาพวงจร"),
                       TextBlock(text="จากแผนภาพ วงจรนี้ประกอบด้วยอะไรบ้าง")],
                 choices=[Choice(content=[TextBlock(
                     text=f"เซลล์ไฟฟ้า {i} เซลล์ต่ออนุกรม และหลอดไฟ {i} ดวง")])
                     for i in range(1, 5)],
                 answer=0)
    # 12 image questions cannot fit 6 to a page, whatever the config asks for.
    cfg = _thai_cfg(show_choices=True, num_problems=12, problems_per_page=6,
                    columns=1, answer_key=False)
    figs = _build_figures(cfg, [q] * 12, lambda aid: img)      # noqa: ARG005
    assert len(figs) > 2, "the page count still followed problems_per_page"

    for fig in figs:
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        floor = GRID_BOTTOM * fig.bbox.height
        boxes = [a.get_window_extent(r) for a in fig.axes[1:]]
        boxes += [t.get_window_extent(r) for t in fig.axes[0].texts
                  if t.get_fontsize() == _CHOICE_FONTSIZE
                  and t.get_position()[1] > GRID_BOTTOM]
        for box in boxes:
            assert box.y0 >= floor, "content ran below the footer rule"
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                assert not a.overlaps(b), "two questions were drawn on top of each other"
    for f in figs:
        plt.close(f)


@pytest.mark.parametrize("show_choices", [False, True])
def test_a_code_block_prints_in_monospace_with_its_indentation(show_choices):
    cfg = _cfg(generators={"comp.code_logic_fluency": 1}, num_problems=6, show_choices=show_choices)
    questions = build_worksheet(cfg, Random(4))
    figs = _build_figures(cfg, questions)
    printed = {t.get_text() for fig in figs for ax in fig.axes for t in ax.texts
               if "monospace" in t.get_fontfamily()}
    for q in questions:
        program = next(b.code for b in q.stem if b.kind == "code")
        assert program in printed
        assert "\n    return" in program
    for fig in figs:
        plt.close(fig)

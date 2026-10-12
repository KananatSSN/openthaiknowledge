"""Tests for hand transcripts of picture-maths sheets (``transcript.py``)."""

from __future__ import annotations

import pytest

from otk.tests._bank import needs_bank
from otk.tools.sheetpipe import transcript as tr

TEXT = """<!-- a note -->
# แบบฝึกหัด 3.3
@p1
1. ให้ p(x) = 3x⁴ + 2x² − ax + 3
   จงหา a, b และ c
   = a = 5, b = 3 และ c = 0
2. ให้ p(x) = x² − 1 จงหา
   1) p(x) + q(x)
      = 2x² − 2x + 2
   2) q(x) − p(x)
      = −2x + 4
# แบบฝึกหัดท้ายบท
@p3
1. ข้อใดถูกต้อง {figure} [O-NET (มี.ค. 61)/3]
   (1) 5   (2) 6
   (3) 7
   (4) 8
   = 3
"""


def test_items_subs_and_sections():
    items = tr.parse(TEXT)
    assert [it.section for it in items] == [
        "แบบฝึกหัด 3.3 1", "แบบฝึกหัด 3.3 2.1", "แบบฝึกหัด 3.3 2.2", "แบบฝึกหัดท้ายบท 1"]
    assert [it.number for it in items] == [1, 2, 3, 4]
    assert items[0].stem == "ให้ p(x) = 3x⁴ + 2x² − ax + 3\nจงหา a, b และ c"
    assert items[0].answer == "a = 5, b = 3 และ c = 0"
    assert items[2].stem == "ให้ p(x) = x² − 1 จงหา\nq(x) − p(x)"
    assert items[2].answer == "−2x + 4" and items[2].pages == [1]


def test_choices_tag_and_figure():
    it = tr.parse(TEXT)[-1]
    assert it.choices == {1: "5", 2: "6", 3: "7", 4: "8"}
    assert it.tag == "O-NET (มี.ค. 61)/3"
    assert it.figure and it.stem == "ข้อใดถูกต้อง"
    assert it.answer == "3" and it.pages == [3]


def test_a_lead_heads_every_item_of_its_section_only():
    items = tr.parse("# ก\n> จงหาเซตคำตอบ\n1. x > 1 [O-NET 61/2]\n   = (1, ∞)\n2. x < 2\n# ข\n1. y = 3\n")
    assert [it.stem for it in items] == ["จงหาเซตคำตอบ\nx > 1", "จงหาเซตคำตอบ\nx < 2", "y = 3"]
    assert items[0].tag == "O-NET 61/2"


def test_a_bracketed_interval_is_not_a_tag():
    it = tr.parse("1. แก้สมการบนช่วง [0, 2π]\n")[0]
    assert it.tag == "" and it.stem.endswith("[0, 2π]")


def test_text_before_an_item_is_an_error():
    with pytest.raises(tr.TranscriptError):
        tr.parse("# หัวข้อ\n   ข้อความลอย\n")


@needs_bank
def test_a_numbered_section_source_names_one_exercise_with_its_subs():
    from otk.tools.sheetpipe import knowledge as kn
    sheet = "rathcenter/3 จำนวนจริง/(สสวท) ท้ายบท จำนวนจริง🍒.pdf"
    assert len(kn.resolve({"sheet": sheet, "section": "แบบฝึกหัดท้ายบท", "number": 9})) == 10
    assert len(kn.resolve({"sheet": sheet, "section": "แบบฝึกหัดท้ายบท", "number": 2})) == 1
    assert len(kn.resolve({"sheet": sheet, "section": "แบบฝึกหัดท้ายบท"})) == 112


def test_todo_lists_picture_layouts_without_a_transcript():
    from dataclasses import replace

    from otk.tools.sheetpipe import bank as bk
    bank = bk.load_bank()
    for e in tr.todo(bank):
        assert e.layout in tr.PICTURE_LAYOUTS and not tr.path_for(e.path).is_file()
    # The bank itself is fully transcribed, so check the rule on synthetic entries.
    done = bank["rathcenter/9 เมทริกซ์/(สสวท) 1 ดีเทอร์มิแนนต์🥑.pdf"]
    fresh = replace(done, path="rathcenter/0 test/(สสวท) missing.pdf", stage="new")
    late = replace(fresh, path="rathcenter/0 test/(สสวท) generated.pdf", stage="generated")
    text = replace(fresh, path="rathcenter/0 test/(สสวท) text.pdf", layout="choice-block")
    todo = tr.todo({e.path: e for e in (done, fresh, late, text)})
    assert [e.path for e in todo] == [fresh.path]


@needs_bank
def test_check_counts_a_committed_transcript():
    n, answered = tr.check("rathcenter/9 เมทริกซ์/(สสวท) 1 ดีเทอร์มิแนนต์🥑.pdf")
    assert (n, answered) == (11, 11)


def test_page_kinds_and_render(tmp_path):
    from otk.tools.sheetpipe import bank as bk
    pdf = bk.default_root() / "rathcenter/9 เมทริกซ์/(สสวท) 2 อินเวอร์สการคูณ🥑.pdf"
    if not bk.present(pdf):
        pytest.skip("bank PDF not fetched (Git LFS)")
    assert tr.page_kinds(pdf) == [True, False]          # photo exercise page, text answer page
    out = tr.render_pages(pdf, tmp_path, 0.5, [1])
    assert [p.name for p in out] == ["p01.png"] and out[0].stat().st_size > 0


@needs_bank
def test_committed_transcripts_parse_and_are_answered():
    files = sorted(tr.ROOT.rglob("*.md"))
    assert files, "no transcripts committed"
    for f in files:
        items = tr.parse(f.read_text("utf-8"))
        assert items, f
        assert all(it.stem for it in items), f

"""Tests for per-document Thai font repair (:mod:`otk.tools.sheetpipe.fontfix`).

Building a PDF with a broken ToUnicode map is impractical, so these tests feed
:func:`fontfix.learn_spans` the same span shape that ``rawdict`` yields: lists
of ``(char, glyph width)``. The damaged strings are taken from real
rathcenter extractions.
"""

from __future__ import annotations

import pytest

from otk.tools.sheetpipe import fontfix

pytestmark = pytest.mark.skipif(not fontfix.available(), reason="PyThaiNLP not installed")

ZW = (" ", 0.0)          # the zero-width glyph that stands for nikhahit


def span(text: str) -> list[tuple[str, float]]:
    """Chars at a normal width; ``|`` marks a zero-width space."""
    return [ZW if c == "|" else (c, 5.0) for c in text]


def repaired(font: str, spans: list[list[tuple[str, float]]], learned) -> list[str]:
    split_am, marks = learned
    out = []
    for s in spans:
        text = fontfix._fix_am(s, font in split_am)
        for (f, ch), mark in marks.items():
            if f == font:
                text = fontfix._sub(text, ch, mark)
        out.append(fontfix.thai.normalize(text))
    return out


def test_learns_ascii_tone_marks_per_font():
    spans = [span(t) for t in (
        "คือพื้นทีLรวมของทั้งสองวง", "ซึLงใหญ่กว่า", "นัLนคือ", "ทีLเหลือ",
        "ตัUงฉาก", "ดังนัUน", "ทิUงได้", "ทัUงหมด", "ซืUอสบู่",
    )]
    learned = fontfix.learn_spans({"CordiaNew": spans})
    assert learned[1] == {("CordiaNew", "L"): "่", ("CordiaNew", "U"): "้"}
    assert repaired("CordiaNew", spans, learned)[:3] == [
        "คือพื้นที่รวมของทั้งสองวง", "ซึ่งใหญ่กว่า", "นั่นคือ"]


def test_frequency_beats_a_rarer_real_word():
    # ครั่ง (lac) and ทั่ง (anvil) are real words; ครั้ง and ทั้ง are far commoner.
    # ดังนั่น also splits into two real words, ดัง + นั่น.
    spans = [span(t) for t in ("ครั1ง", "ดังนั1น", "ทั1งหมด", "ครั1งที่สอง")]
    _, marks = fontfix.learn_spans({"CordiaNew": spans})
    assert marks == {("CordiaNew", "1"): "้"}


def test_split_am_font():
    # In this font า is read as ำ, and a real ำ is a zero-width space + ำ.
    spans = [span(t) for t in (
        "แทนเซตของจ|ำนวนคู่ที่น้อยกว่ำ", "ถ้ำ", "ที่มำกที่สุดที่เป็นไปได้เท่ำกับเท่ำใด",
        "ก|ำหนดให้", "มีสมำชิก", "แผนภำพ",
    )]
    learned = fontfix.learn_spans({"Cordia New": spans})
    assert learned[0] == {"Cordia New"}
    assert repaired("Cordia New", spans, learned) == [
        "แทนเซตของจำนวนคู่ที่น้อยกว่า", "ถ้า", "ที่มากที่สุดที่เป็นไปได้เท่ากับเท่าใด",
        "กำหนดให้", "มีสมาชิก", "แผนภาพ"]


def test_zero_width_nikhahit_before_a_correct_sara_aa():
    # Another variant: า is mapped right, but ำ's nikhahit is still a zero-width
    # space (ก าหนด = กำหนด). A real space is never zero-width, so this is safe
    # to fix without learning anything.
    assert fontfix._fix_am(span("ก|าหนดให้ จ|านวน"), split_am=False) == "กำหนดให้ จำนวน"
    assert fontfix._fix_am([("ก", 5.0), (" ", 2.6), ("า", 5.0)], split_am=False) == "ก า"
    # With a tone mark between them: น ้าตาล = น้ำตาล.
    assert fontfix._fix_am(span("ใส่น|้าตาล"), split_am=False) == "ใส่น้ำตาล"


def test_clean_font_is_left_alone():
    spans = [span(t) for t in ("กำหนดให้ 𝐴 เป็นเซต", "จำนวนสมาชิก", "ถ้ำหินปูน", "ม.4 ข้อ 5")]
    assert fontfix.learn_spans({"THSarabunPSK": spans}) == (set(), {})


def test_math_variable_is_not_a_tone_mark():
    # น3 is น cubed. A lone occurrence gains nothing from any mark.
    spans = [span("น3 + 3น2ล + 3นล2")]
    assert fontfix.learn_spans({"CordiaNew": spans})[1] == {}


def test_clean_pdf_extracts_as_plain_text(tmp_path):
    fitz = pytest.importorskip("fitz")
    pdf = tmp_path / "clean.pdf"
    with fitz.open() as doc:
        doc.new_page().insert_text((50, 72), "1. Find x.\n2. Find y.")
        doc.save(pdf)
    with fitz.open(pdf) as doc:
        assert fontfix.page_texts(doc) == [p.get_text() for p in doc]

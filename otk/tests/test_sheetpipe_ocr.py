"""Tests for Thai text repair and the OCR fallback for scanned sheets.

The OCR tests need Tesseract and skip without it. The repair tests use strings
seen in real bank extractions.
"""

from __future__ import annotations

import pytest

from otk.tools.sheetpipe import ocr, thai


@pytest.mark.parametrize("damaged, fixed", [
    ("ข้อใดต่อไปนี9ถูกต้อง", "ข้อใดต่อไปนี้ถูกต้อง"),       # 9 for ้ (rathcenter)
    ("ดังนั9น", "ดังนั้น"),
    ("ไม่มีส่วนซํ9ากัน", "ไม่มีส่วนซ้ำกัน"),                # 9 for ้ inside ำ
    ("ถา 5 ไม", "ถ้า 5 ไม่"),                   # private-use tone marks
    ("ก็ตอเมื่อ", "ก็ต่อเมื่อ"),
    ("คํานวณหาขนาด", "คำนวณหาขนาด"),                      # OCR's decomposed ำ
])
def test_normalize_repairs(damaged, fixed):
    assert thai.damage(damaged) >= 1
    assert thai.normalize(damaged) == fixed
    assert thai.damage(fixed) == 0


@pytest.mark.parametrize("clean", [
    "[กสพท คณิต1 (มี.ค. 2567/1)]",     # letter+digit that is not damage
    "ชั้น ม.4 ข้อ 5 นี้ถูกต้อง ปี 2567",
    "x² + 9 = 18, ครั้งที่ 9",
    "กลำง",                            # not table-repairable — left alone
])
def test_normalize_leaves_clean_text(clean):
    assert thai.normalize(clean) == clean
    assert thai.damage(clean) == 0


# ── OCR ──────────────────────────────────────────────────────────────────────

needs_ocr = pytest.mark.skipif(not ocr.available("eng"), reason="Tesseract not installed")


def scanned_pdf(path, lines):
    """A PDF whose only page is a picture of ``lines`` — no text layer."""
    fitz = pytest.importorskip("fitz")
    with fitz.open() as src:
        page = src.new_page()
        page.insert_text((50, 72), "\n".join(lines), fontsize=14)
        png = page.get_pixmap(dpi=200).tobytes("png")
    with fitz.open() as doc:
        page = doc.new_page()
        page.insert_image(page.rect, stream=png)
        doc.save(path)
    return path


@needs_ocr
def test_read_pages_ocrs_only_scanned_pages(tmp_path):
    fitz = pytest.importorskip("fitz")
    pdf = scanned_pdf(tmp_path / "scan.pdf", ["1. The box weighs 40 newtons.",
                                             "2. Find the friction force."])
    with fitz.open(pdf) as doc:
        assert doc[0].get_text().strip() == ""          # really a scan
        typed = doc.new_page()
        typed.insert_text((50, 72), "3. This page has a text layer.")
        doc.saveIncr()

    texts, sources = ocr.read_pages(pdf, lang="eng")
    assert sources == ["ocr", "text"]
    assert "40 newtons" in texts[0] and "friction" in texts[0]
    assert "text layer" in texts[1]


@needs_ocr
def test_split_items_works_on_ocr_text(tmp_path):
    from otk.tools.sheetpipe.extract import split_items
    lines = [f"{n}. Question number {n} asks about force." for n in range(1, 6)]
    texts, _ = ocr.read_pages(scanned_pdf(tmp_path / "s.pdf", lines), lang="eng")
    assert sorted(split_items(texts)) == [1, 2, 3, 4, 5]

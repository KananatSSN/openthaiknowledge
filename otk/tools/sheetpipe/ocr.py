"""OCR for scanned sheets, via Tesseract.

A scanned PDF has no text layer, so :func:`extract.page_texts` returns empty
pages. For those pages this module renders the page and hands it to Tesseract
with Thai + English. Two scans in the bank need this:
``Faii/ข้อสอบแรง.pdf`` and ``สอวน_math/posn1-64-math.pdf``.

**What it is good for.** Thai prose, numbers and choice letters come out
usable. ``--psm 6`` (one uniform block of text) keeps each line whole and
keeps two-column choices on one line. Expect small slips, such as ``ข้าย`` for
ซ้าย and ``A.`` for ``ง.``, so read the output before trusting a constant.

**What it is not good for.** Mathematics. Exponents, fractions and radicals
come out garbled. Transcribe those pages from the render, as
``openthaiknowledge-bank/สอวน_math/HANDOFF.md`` describes.

Setup (Windows)::

    winget install UB-Mannheim.TesseractOCR
    # Thai is not bundled; put tessdata_best's tha + eng (+ osd) in
    # %LOCALAPPDATA%\\tessdata, or point TESSDATA_PREFIX at a folder holding them.

``TESSERACT`` overrides the executable path.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

from . import fontfix, thai
from .extract import _fitz

LANG = "tha+eng"
DPI = 300
PSM = "6"

# A page whose text layer is shorter than this, and that carries an image, is
# treated as a scan.
SCAN_MAX_CHARS = 20

_WINDOWS_EXE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")


def tesseract_exe() -> str | None:
    exe = os.environ.get("TESSERACT") or shutil.which("tesseract")
    if exe:
        return exe
    return str(_WINDOWS_EXE) if _WINDOWS_EXE.is_file() else None


def tessdata_dir() -> str | None:
    """Where the language models live, if not Tesseract's own default."""
    if os.environ.get("TESSDATA_PREFIX"):
        return os.environ["TESSDATA_PREFIX"]
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "tessdata"
    return str(local) if (local / "tha.traineddata").is_file() else None


def _base_cmd() -> list[str]:
    exe = tesseract_exe()
    if exe is None:
        raise RuntimeError("OCR needs Tesseract — see otk/tools/sheetpipe/ocr.py")
    cmd = [exe]
    if tessdata_dir():
        cmd += ["--tessdata-dir", tessdata_dir()]
    return cmd


@lru_cache(maxsize=1)
def languages() -> frozenset[str]:
    """Language models Tesseract can load; empty if it is not installed."""
    try:
        out = subprocess.run(_base_cmd() + ["--list-langs"], capture_output=True,
                             check=True).stdout.decode("utf-8", "replace")
    except (RuntimeError, OSError, subprocess.CalledProcessError):
        return frozenset()
    return frozenset(line.strip() for line in out.splitlines()[1:] if line.strip())


def available(lang: str = LANG) -> bool:
    return set(lang.split("+")) <= languages()


def ocr_png(png: bytes, lang: str = LANG, psm: str = PSM) -> str:
    """Text of one page image (PNG bytes), repaired by :func:`thai.normalize`."""
    cmd = _base_cmd() + ["stdin", "stdout", "-l", lang, "--psm", psm,
                         "-c", "preserve_interword_spaces=1"]
    out = subprocess.run(cmd, input=png, capture_output=True, check=True).stdout
    return thai.normalize(out.decode("utf-8", "replace")).strip()


def is_scan(page) -> bool:
    return len(page.get_text().strip()) < SCAN_MAX_CHARS and bool(page.get_images())


def ocr_pages(pdf: str | Path, pages: list[int] | None = None, dpi: int = DPI,
              lang: str = LANG) -> dict[int, str]:
    """``{1-based page: text}`` by OCR, for ``pages`` (default: every page)."""
    out = {}
    with _fitz().open(str(pdf)) as doc:
        for pno in pages or range(1, doc.page_count + 1):
            png = doc[pno - 1].get_pixmap(dpi=dpi).tobytes("png")
            out[pno] = ocr_png(png, lang)
    return out


def read_pages(pdf: str | Path, lang: str = LANG) -> tuple[list[str], list[str]]:
    """Every page's text, OCR-ing only the scanned ones.

    Returns ``(texts, sources)``, where each source is ``"text"`` or ``"ocr"``.
    Text-layer pages get the font-damage repair of :mod:`.fontfix`. If
    Tesseract is missing, scanned pages stay empty and are marked ``"text"``.
    The bank probe will still show them as ``no-text``.
    """
    with _fitz().open(str(pdf)) as doc:
        texts = fontfix.page_texts(doc)
        scans = [i + 1 for i, p in enumerate(doc) if is_scan(p)]
    sources = ["text"] * len(texts)
    if scans and available(lang):
        for pno, text in ocr_pages(pdf, scans, lang=lang).items():
            texts[pno - 1], sources[pno - 1] = text, "ocr"
    return texts, sources

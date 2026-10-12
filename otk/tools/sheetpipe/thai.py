"""Repair the systematic damage Thai text picks up on its way out of a PDF.

Two sources, both mechanical and so both repairable by table:

* **Legacy Thai fonts** position their tone marks and upper vowels with
  private-use glyphs (``U+F700``–``U+F71A``), and some map ``้`` to the digit
  ``9`` in their ToUnicode table, so ``นี้`` extracts as ``นี9``. On the
  rathcenter sheets that is ~2,000 hits.
* **OCR** (Tesseract) writes ``ำ`` decomposed, as ``ํ`` + ``า``.

Damage that differs from one PDF to the next cannot be fixed by a table:
``ำ`` read for ``า``, and tone marks read as arbitrary ASCII letters. Those are
learned per document at glyph level by :mod:`.fontfix`, which calls this
module last.
"""

from __future__ import annotations

import re

NIKHAHIT, SARA_AA, SARA_AM, MAI_THO = "ํ", "า", "ำ", "้"
UPPER_VOWELS = "ัิีึืํ"   # ั ิ ี ึ ื ํ

#: Legacy positional glyphs → the character they position. The table is the
#: common one shipped by Thai fonts built for pre-OpenType renderers.
PUA = {
    0xF700: "ฐ", 0xF70F: "ญ",                  # ฐ ญ without descender
    0xF701: "ิ", 0xF702: "ี", 0xF703: "ึ", 0xF704: "ื",
    0xF705: "่", 0xF706: "้", 0xF707: "๊", 0xF708: "๋",
    0xF709: "์",
    0xF70A: "่", 0xF70B: "้", 0xF70C: "๊", 0xF70D: "๋",
    0xF70E: "์",
    0xF710: "ั", 0xF711: "ํ", 0xF712: "็",
    0xF713: "่", 0xF714: "้", 0xF715: "๊", 0xF716: "๋",
    0xF717: "์",
    0xF718: "ุ", 0xF719: "ู", 0xF71A: "ฺ",
}

#: What :func:`damage` counts — the forms :func:`normalize` repairs.
DAMAGE = re.compile(f"[{UPPER_VOWELS}]9|[-]|{NIKHAHIT}[่-๋]?{SARA_AA}")

_NINE_AS_MAI_THO = re.compile(f"([{UPPER_VOWELS}])9")
_SPLIT_SARA_AM = re.compile(f"{NIKHAHIT}([่-๋]?){SARA_AA}")


def normalize(text: str) -> str:
    """Undo the table-repairable damage; leave everything else alone."""
    text = text.translate(PUA)
    text = _NINE_AS_MAI_THO.sub(lambda m: m.group(1) + MAI_THO, text)
    # ซํ้า → ซ้ำ: the tone mark belongs before ำ, which absorbs the ํ.
    return _SPLIT_SARA_AM.sub(lambda m: m.group(1) + SARA_AM, text)


def damage(text: str) -> int:
    """How many repairable defects ``text`` carries."""
    return len(DAMAGE.findall(text))

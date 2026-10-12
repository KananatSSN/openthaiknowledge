"""Glyph-level repair for PDFs whose embedded Thai font has a broken ToUnicode map.

Some rathcenter PDFs embed subsets of Cordia New whose character map is wrong
in two ways. Neither can be fixed by a fixed table, because the damage differs
from one PDF to the next:

* **Tone marks read as ASCII.** The ASCII character differs per document:
  ``ทีL`` = ที่, ``เทQา`` = เท่า, ``ตัUง`` = ตั้ง, ``ครั1ง`` = ครั้ง, ``เปKน`` = เป็น,
  ``ประสิทธิf`` = ประสิทธิ์. The same letter can even stand for different marks
  in different PDFs (``U`` is ``่`` in some and ``้`` in others). So the
  mapping is *learned* per (document, font, character): each Thai mark is
  tried in every word the character sits in, and the one that makes the text
  most probable under a Thai word-frequency model wins.
* **``า`` read as ``ำ``.** The font draws a real ``ำ`` as a zero-width nikhahit
  glyph (mapped to a space) followed by the ``า`` glyph, and that glyph is
  mapped to ``ำ``. So in such a font, zero-width space + ``ำ`` means ``ำ``, and
  a bare ``ำ`` means ``า`` (``ถ้ำ`` = ถ้า, ``จ ำนวน`` = จำนวน). A zero-width
  space is visible only at glyph level, which is why this module reads
  ``rawdict`` rather than plain text.

Both repairs are applied to a font only when the dictionary agrees that they
improve it. A clean document is returned exactly as ``page.get_text()``
would return it.

Needs PyThaiNLP (``pip install pythainlp``) for the word list. Without it,
pages come back unrepaired apart from :func:`thai.normalize`.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache

from . import thai

#: Marks a stray ASCII character may stand for: tone marks, then the rest.
MARKS = "่้๊๋็์ัิีึืุูํ"
TONES = "่้๊๋"

_THAI = re.compile(r"[ก-๎]")
_RUN = re.compile(r"[ก-๎]+")
# An ASCII letter/digit wedged between two Thai characters.
_WEDGED = re.compile(r"(?<=[ก-๎])[A-Za-z0-9](?=[ก-๎])")

# A substitution must beat leaving the text alone by this much log-probability
# (in nats), so that one lucky word cannot decide a font.
MIN_GAIN = 8.0
ZERO_WIDTH = 0.1


@lru_cache(maxsize=1)
def _model():
    """``(log P(word), unknown-char penalty, tokenize)``, or None without PyThaiNLP.

    This is a unigram model over the Thai National Corpus frequencies. Plain
    dictionary membership is not enough, because both readings are often real
    words: ``นั่น``/``นั้น``, ``ครั่ง``/``ครั้ง``, ``ทั่ง``/``ทั้ง``. Frequency
    separates them (``ครั้ง`` 48,705 vs ``ครั่ง`` 118). A unigram model also
    prefers one long word to two short ones (``ดังนั้น`` over ``ดัง`` + ``นั่น``).
    """
    try:
        from pythainlp.corpus import thai_words, tnc
        from pythainlp.tokenize import word_tokenize
        from pythainlp.util import Trie
    except ImportError:
        return None
    freqs = dict(tnc.word_freqs())
    total = sum(freqs.values())
    floor = 0.5                                   # a dictionary word TNC never saw
    logp = {w: math.log(freqs.get(w, floor) / total) for w in set(thai_words()) | set(freqs)}
    unknown = math.log(floor / total) - 1.0       # per character, worse than any word
    trie = Trie(logp)
    return logp, unknown, (lambda text: word_tokenize(text, custom_dict=trie, engine="newmm"))


def available() -> bool:
    return _model() is not None


@lru_cache(maxsize=65536)
def score(text: str) -> float:
    """Log-probability of ``text``'s Thai runs under the unigram model.

    The text is normalized first, so that a candidate like ``นํ้า`` is scored as
    the ``น้ำ`` it will become.
    """
    logp, unknown, tokenize = _model()
    return sum(logp[tok] if tok in logp else unknown * len(tok)
               for run in _RUN.findall(thai.normalize(text)) for tok in tokenize(run))


def raw_damage(text: str) -> int:
    """Repairable-looking defects in plain extracted text.

    This counts the table-repairable forms, ASCII wedged between Thai
    characters, and a space before ``ำ``. It over-counts slightly, because a
    Thai variable with a digit (``น3``, n cubed) looks like damage too.
    """
    return thai.damage(text) + len(_WEDGED.findall(text)) + text.count(" ำ")




# ── Reading spans ────────────────────────────────────────────────────────────

Chars = list[tuple[str, float]]          # (character, glyph width)


def _chars(span) -> Chars:
    return [(c["c"], c["bbox"][2] - c["bbox"][0]) for c in span["chars"]]


def _zw(chars: Chars, i: int) -> bool:
    """Is ``chars[i]`` the zero-width space some fonts draw nikhahit as?"""
    return 0 <= i < len(chars) and chars[i][0] == " " and chars[i][1] < ZERO_WIDTH


def _fix_am(chars: Chars, split_am: bool) -> str:
    """Span text with the zero-width-nikhahit signatures resolved.

    Zero-width space + ``า`` or ``ำ`` is always ``ำ`` (``ก าหนด``, ``จ ำนวน``),
    because a real space is never zero-width. In a ``split_am`` font, a bare
    ``ำ`` is also ``า`` (``ถ้ำ`` = ถ้า).
    """
    out = []
    nikhahit = False                  # a zero-width space is waiting for its า
    for i, (c, _) in enumerate(chars):
        if _zw(chars, i) and _am_follows(chars, i):
            nikhahit = True                           # the nikhahit half of ำ
            continue
        if c in "าำ" and nikhahit:
            c, nikhahit = "ำ", False
        elif split_am and c == "ำ":
            c = "า"
        out.append(c)
    return "".join(out)


def _am_follows(chars: Chars, i: int, follow: str = "าำ") -> bool:
    """Does ``า``/``ำ`` follow position ``i``, perhaps after one tone mark (``น ้า``)?"""
    j = i + 1
    if j < len(chars) and chars[j][0] in TONES:
        j += 1
    return j < len(chars) and chars[j][0] in follow


def _has_zw(chars: Chars, follow: str = "าำ") -> bool:
    return any(_zw(chars, i) and _am_follows(chars, i, follow) for i in range(len(chars)))


# ── Learning a document's substitutions ──────────────────────────────────────

def learn(doc) -> tuple[set[str], dict[tuple[str, str], str]]:
    """Which fonts need the ``ำ``/``า`` fix, and what each wedged ASCII char means.

    Returns ``(split_am_fonts, {(font, ascii char): thai mark})``.
    """
    texts_by_font: dict[str, list[Chars]] = defaultdict(list)
    for page in doc:
        for block in page.get_text("rawdict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    chars = _chars(span)
                    if any(_THAI.match(c) for c, _ in chars):
                        texts_by_font[span["font"]].append(chars)
    return learn_spans(texts_by_font)


def learn_spans(texts_by_font: dict[str, list[Chars]]
                ) -> tuple[set[str], dict[tuple[str, str], str]]:
    """:func:`learn` over spans already read: ``{font: [[(char, width), …], …]}``."""
    split_am = set()
    for font, spans in texts_by_font.items():
        if not any(_has_zw(s, "ำ") for s in spans):
            continue
        before = sum(score(_fix_am(s, False)) for s in spans)
        after = sum(score(_fix_am(s, True)) for s in spans)
        if after - before >= MIN_GAIN:
            split_am.add(font)

    marks: dict[tuple[str, str], str] = {}
    for font, spans in texts_by_font.items():
        runs_by_char: dict[str, list[str]] = defaultdict(list)
        for s in spans:
            text = _fix_am(s, font in split_am)
            for m in _WEDGED.finditer(text):
                # The whole whitespace-free stretch around the character.
                lo = max((text.rfind(ch, 0, m.start()) for ch in " \n\t"), default=-1) + 1
                hi = min((i for i in (text.find(ch, m.end()) for ch in " \n\t") if i >= 0),
                         default=len(text))
                runs_by_char[m.group()].append(text[lo:hi])
        for ch, runs in runs_by_char.items():
            base = sum(score(r) for r in runs)
            scored = {mark: sum(score(_sub(r, ch, mark)) for r in runs) for mark in MARKS}
            best = max(scored, key=scored.get)
            # A digit next to Thai is often maths: น3 is n cubed, and a lone
            # น2ล happens to read as นิล. So a digit needs two different words
            # that improve, not just one.
            improved = {r for r in runs if score(_sub(r, ch, best)) > score(r)}
            if scored[best] - base >= MIN_GAIN and len(improved) >= (2 if ch.isdigit() else 1):
                marks[(font, ch)] = best
    return split_am, marks


def _sub(text: str, ch: str, mark: str) -> str:
    return re.sub(f"(?<=[\u0e01-\u0e4e]){re.escape(ch)}(?=[\u0e01-\u0e4e])", mark, text)


# ── Applying it ──────────────────────────────────────────────────────────────

@dataclass
class Repair:
    """One document's learned repair. :func:`repair_for` builds it."""

    split_am: set[str] = field(default_factory=set)
    marks: dict[tuple[str, str], str] = field(default_factory=dict)
    zero_width: bool = False             # the doc draws some ำ as zero-width + า/ำ

    @property
    def needed(self) -> bool:
        return bool(self.split_am or self.marks or self.zero_width)

    def span(self, font: str, chars: Chars) -> str:
        text = _fix_am(chars, font in self.split_am)
        for (f, ch), mark in self.marks.items():
            if f == font:
                text = _sub(text, ch, mark)
        return text


def repair_for(doc) -> Repair:
    zero_width = any(_has_zw(_chars(span))
                     for page in doc for block in page.get_text("rawdict")["blocks"]
                     for line in block.get("lines", []) for span in line["spans"])
    if not available():
        return Repair(zero_width=zero_width)
    split_am, marks = learn(doc)
    return Repair(split_am, marks, zero_width)


@dataclass
class Block:
    """A text or image block of one page, with repaired text."""

    page: int                            # 1-based
    bbox: tuple[float, float, float, float]
    text: str = ""
    image: bool = False
    top: float | None = None             # y of the first line that has text

    @property
    def y0(self) -> float:
        """Where the block's content starts. Leading blank lines don't count."""
        return self.bbox[1] if self.top is None else self.top


def page_blocks(page, repair: Repair) -> list[Block]:
    """The page's blocks in PDF order: text repaired, images kept as boxes."""
    out = []
    for block in page.get_text("rawdict")["blocks"]:
        bbox = tuple(block["bbox"])
        if block["type"] == 1:
            out.append(Block(page.number + 1, bbox, image=True))
            continue
        raw = block.get("lines", [])
        lines = ["".join(repair.span(s["font"], _chars(s)) for s in line["spans"])
                 for line in raw]
        top = next((line["bbox"][1] for line, text in zip(raw, lines) if text.strip()), None)
        out.append(Block(page.number + 1, bbox, thai.normalize("\n".join(lines)), top=top))
    return out


def page_texts(doc) -> list[str]:
    """Every page's text, with this document's font damage repaired.

    A document with nothing to repair gets plain ``page.get_text()``, so that
    clean sheets extract exactly as they always have.
    """
    repair = repair_for(doc)
    if not repair.needed:
        return [thai.normalize(p.get_text()) for p in doc]
    return ["".join(b.text + "\n" for b in page_blocks(p, repair) if not b.image)
            for p in doc]

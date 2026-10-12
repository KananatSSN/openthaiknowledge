"""ป.1 sets read off a picture of things: count them, compare two groups, join
two groups, take some away, find the hidden part, count bundles of ten.

The สสวท. ป.1 book starts every number idea with objects before symbols. Until
this module the catalog began at "“ห้าสิบสอง” เขียนเป็นตัวเลขได้อย่างไร". Each
family below is a finite tuple of specs;
``otk/pictures/counting_pictures.py`` draws one PNG per
spec, and a question computes its answer from the same spec, so the picture and
the answer cannot disagree.

Layouts come from a hash of the asset id rather than from ``random`` so the
specs, and therefore the shipped file names, never move between Python versions.
Alt text names the kind of thing but never how many.
"""

from __future__ import annotations

import hashlib
from typing import NamedTuple

from otk.core.content import image

LEVEL = {"th": "ป.1"}


class Kind(NamedTuple):
    key: str
    thai: str
    unit: str          # ลักษณนาม


KINDS = (
    Kind("apple", "แอปเปิล", "ผล"),
    Kind("orange", "ส้ม", "ผล"),
    Kind("banana", "กล้วย", "ผล"),
    Kind("fish", "ปลา", "ตัว"),
    Kind("flower", "ดอกไม้", "ดอก"),
    Kind("balloon", "ลูกโป่ง", "ลูก"),
    Kind("star", "ดาว", "ดวง"),
    Kind("ball", "ลูกบอล", "ลูก"),
)
BY_KEY = {k.key: k for k in KINDS}


def _order(seed: str, items: list) -> list:
    """A stable shuffle keyed on ``seed``."""
    return sorted(items, key=lambda item: hashlib.sha256(f"{seed}|{item}".encode()).digest())


# ══ Specs ════════════════════════════════════════════════════════════════════

class Scene(NamedTuple):
    """Objects at grid cells (kind, column, row)."""
    asset_id: str
    items: tuple[tuple[str, int, int], ...]

    def count(self, kind: str) -> int:
        return sum(1 for k, _, _ in self.items if k == kind)

    @property
    def kinds(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(k for k, _, _ in self.items))


def _scatter(asset_id: str, kinds: list[str], cols: int, rows: int) -> Scene:
    cells = _order(asset_id, [(c, r) for r in range(rows) for c in range(cols)])
    placed = sorted(zip(cells, _order(asset_id + "k", kinds)), key=lambda p: (p[0][1], p[0][0]))
    return Scene(asset_id, tuple((kind, c, r) for (c, r), kind in placed))


def _rows_of_five(asset_id: str, kind: str, n: int) -> Scene:
    return Scene(asset_id, tuple((kind, i % 5, i // 5) for i in range(n)))


# One kind, 1–10, scattered over a 5 × 3 grid.
SMALL_COUNTS = tuple(_scatter(f"pc1_{k.key}_{n}", [k.key] * n, 5, 3)
                     for k in KINDS for n in range(1, 11))
# One kind, 11–20, in rows of five so a learner can count on by fives.
LARGE_COUNTS = tuple(_rows_of_five(f"pc2_{k.key}_{n}", k.key, n)
                     for k in KINDS for n in range(11, 21))


def _mixed() -> tuple[Scene, ...]:
    scenes = []
    for i in range(96):
        seed = f"pcm_{i}"
        three = i % 3 == 0
        kinds = _order(seed, [k.key for k in KINDS])[:3 if three else 2]
        counts = [1 + int(hashlib.sha256(f"{seed}{k}".encode()).hexdigest(), 16) % (4 if three else 6)
                  for k in kinds]
        scenes.append(_scatter(seed, [k for k, n in zip(kinds, counts) for _ in range(n)], 5, 3))
    return tuple(scenes)


MIXED = _mixed()


def _lines() -> tuple[Scene, ...]:
    scenes = []
    for i in range(40):
        seed = f"pco_{i}"
        kinds = _order(seed, [k.key for k in KINDS])[:5 + i % 3]
        scenes.append(Scene(seed, tuple((k, c, 0) for c, k in enumerate(kinds))))
    return tuple(scenes)


LINES = _lines()
ALL_SCENES = SMALL_COUNTS + LARGE_COUNTS + MIXED + LINES


class TwoRows(NamedTuple):
    top: str
    top_n: int
    bottom: str
    bottom_n: int

    @property
    def asset_id(self) -> str:
        return f"pcr_{self.top}_{self.top_n}_{self.bottom}_{self.bottom_n}"


def _two_rows() -> tuple[TwoRows, ...]:
    out = []
    for i in range(80):
        seed = f"pcr{i}"
        top, bottom = _order(seed, [k.key for k in KINDS])[:2]
        a = 1 + i % 10
        b = 1 + (i * 7 + 3) % 10
        if a == b:
            b = b % 10 + 1
        out.append(TwoRows(top, a, bottom, b))
    return tuple(dict.fromkeys(out))


TWO_ROWS = _two_rows()


class Joined(NamedTuple):
    kind: str
    a: int
    b: int

    @property
    def asset_id(self) -> str:
        return f"pcj_{self.kind}_{self.a}_{self.b}"


class Crossed(NamedTuple):
    kind: str
    total: int
    gone: int

    @property
    def asset_id(self) -> str:
        return f"pcx_{self.kind}_{self.total}_{self.gone}"


class Hidden(NamedTuple):
    kind: str
    total: int
    inside: int

    @property
    def asset_id(self) -> str:
        return f"pch_{self.kind}_{self.total}_{self.inside}"


_PAIRS_TO_TEN = [(a, b) for a in range(1, 10) for b in range(1, 11 - a)]
JOINED = tuple(Joined(KINDS[i % len(KINDS)].key, a, b) for i, (a, b) in enumerate(_PAIRS_TO_TEN))
CROSSED = tuple(Crossed(KINDS[i % len(KINDS)].key, t, g)
                for i, (t, g) in enumerate((t, g) for t in range(2, 11) for g in range(1, t)))
HIDDEN = tuple(Hidden(KINDS[i % len(KINDS)].key, t, n)
               for i, (t, n) in enumerate((t, n) for t in range(3, 11) for n in range(1, t)))


class Bundles(NamedTuple):
    tens: int
    ones: int

    @property
    def asset_id(self) -> str:
        return f"pcb_{self.tens}_{self.ones}"

    @property
    def value(self) -> int:
        return 10 * self.tens + self.ones


BUNDLES = tuple(Bundles(t, o) for t in range(1, 10) for o in range(10))

ALL_PICTURE_IDS = tuple(s.asset_id for s in ALL_SCENES + TWO_ROWS + JOINED + CROSSED
                        + HIDDEN + BUNDLES)


# ══ Question helpers ═════════════════════════════════════════════════════════

def _img(asset_id: str, kinds: list[str] | tuple[str, ...]) -> object:
    names = " ".join(BY_KEY[k].thai for k in kinds)
    return image(asset_id, alt=f"ภาพ{names}")


def _near(n: int, *extra: int, lo: int = 0) -> list[str]:
    """Named mistakes first, then the neighbours a miscount lands on."""
    out = []
    for v in (*extra, n + 1, n - 1, n + 2, n - 2):
        if v >= lo and v != n and str(v) not in out:
            out.append(str(v))
    return out


# ══ Sets ═════════════════════════════════════════════════════════════════════



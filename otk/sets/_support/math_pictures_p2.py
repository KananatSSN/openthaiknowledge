"""ป.2–ป.3 sets read off a picture: rows and equal groups for × and ÷, Thai
coins and banknotes, base-ten blocks, and a fraction of a group.

Same contract as :mod:`.math_pictures`: finite specs, one PNG each drawn by
``otk/pictures/counting_pictures.py``, answers computed
from the spec, alt text that never gives the count or the value.
"""

from __future__ import annotations

from typing import NamedTuple

from otk.sets._support.math_pictures import KINDS, _order

P2 = {"th": "ป.2"}
P3 = {"th": "ป.3"}


# ══ Specs ════════════════════════════════════════════════════════════════════

class Array(NamedTuple):
    """``rows`` rows of ``cols`` things."""
    kind: str
    rows: int
    cols: int

    @property
    def asset_id(self) -> str:
        return f"pca_{self.kind}_{self.rows}_{self.cols}"


class Groups(NamedTuple):
    """``groups`` plates of ``size`` things each."""
    kind: str
    groups: int
    size: int

    @property
    def asset_id(self) -> str:
        return f"pcg_{self.kind}_{self.groups}_{self.size}"


ARRAYS = tuple(Array(KINDS[(r * 7 + c) % len(KINDS)].key, r, c)
               for r in range(2, 6) for c in range(2, 7))
GROUPS = tuple(Groups(KINDS[(g * 3 + s) % len(KINDS)].key, g, s)
               for g in range(2, 6) for s in range(2, 6))


# Thai money: coins 1, 2, 5, 10 baht; notes 20, 50, 100, 500.
COINS = (1, 2, 5, 10)
NOTES = (20, 50, 100, 500)
_MONEY_WORD = {1: "เหรียญหนึ่งบาท", 2: "เหรียญสองบาท", 5: "เหรียญห้าบาท", 10: "เหรียญสิบบาท",
               20: "ธนบัตรยี่สิบบาท", 50: "ธนบัตรห้าสิบบาท", 100: "ธนบัตรหนึ่งร้อยบาท",
               500: "ธนบัตรห้าร้อยบาท"}


class Money(NamedTuple):
    """(value, how many), notes first, largest first."""
    pieces: tuple[tuple[int, int], ...]

    @property
    def asset_id(self) -> str:
        return "pcy_" + "_".join(f"{v}x{n}" for v, n in self.pieces)

    @property
    def total(self) -> int:
        return sum(v * n for v, n in self.pieces)

    @property
    def count(self) -> int:
        return sum(n for _, n in self.pieces)


def _money() -> tuple[Money, ...]:
    out = []
    for i in range(160):
        seed = f"pcy{i}"
        notes = _order(seed, list(NOTES))[:i % 3]           # none, one or two kinds
        coins = _order(seed + "c", list(COINS))[:1 + (i // 3) % 3]
        pieces = [(v, 1 + (i + v) % 2) for v in notes] + [(v, 1 + (i * 5 + v) % 4) for v in coins]
        out.append(Money(tuple(sorted(pieces, reverse=True))))
    return tuple(m for m in dict.fromkeys(out) if m.total <= 1000 and len(m.pieces) >= 2)


MONEY = _money()


class Blocks(NamedTuple):
    hundreds: int
    tens: int
    ones: int

    @property
    def asset_id(self) -> str:
        return f"pct_{self.hundreds}_{self.tens}_{self.ones}"

    @property
    def value(self) -> int:
        return 100 * self.hundreds + 10 * self.tens + self.ones


# A zero in the tens place in one of every five, since 305 read as 35 is the
# mistake worth catching.
BLOCKS = tuple(dict.fromkeys(
    Blocks(1 + i % 9, 0 if i % 5 == 0 else (i * 7) % 10, (i * 3 + 1) % 10) for i in range(120)))


class Shaded(NamedTuple):
    """``n`` balloons of which ``k`` are red and the rest blue."""
    n: int
    k: int

    @property
    def asset_id(self) -> str:
        return f"pcf_{self.n}_{self.k}"


SHADED = tuple(Shaded(n, k) for n in range(2, 11) for k in range(1, n))

class Growing(NamedTuple):
    """Figure n is ``rows`` rows of ``start + n − 1`` tiles or dots: it gains one
    column, ``rows`` pieces, each time."""
    style: str           # tile | dot
    rows: int
    start: int

    @property
    def asset_id(self) -> str:
        return f"pcp_{self.style}_{self.rows}_{self.start}"

    def count(self, n: int) -> int:
        return self.rows * (self.start + n - 1)


GROWING = tuple(Growing(style, r, c) for style in ("tile", "dot")
                for r in (1, 2, 3) for c in (1, 2, 3))

ALL_PICTURE_IDS = tuple(s.asset_id for s in ARRAYS + GROUPS + MONEY + BLOCKS + SHADED + GROWING)


# ══ Sets ═════════════════════════════════════════════════════════════════════



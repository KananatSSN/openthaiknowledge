"""ข้อ 30 — ผังบ้านหมู่บ้าน "แสนสุข"

บ้านสองหลังเป็น "เพื่อนบ้านที่อยู่ติดกัน" หากติดกันในแนวตั้ง แนวนอน หรือแนวทแยงมุม
กำหนดจำนวนเพื่อนบ้านของนาย A = 5, นาย B = นาย C = 4, นาย D = 3, นาย G = 2
ให้ x, y เป็นจำนวนเพื่อนบ้านของนาย E และนาย F  จงหาค่ามากที่สุดที่เป็นไปได้ของ x + y

The plan is the data. It was read off the PDF with
``sheetpipe.extract.read_table_layout`` (icons become houses, ว่าง becomes known
empty land) — :data:`LAYOUT` is that reading, and the cells left blank in the
figure are the *unknowns*: the puzzle is that a blank may or may not hold a
house, and the five given neighbour counts are what narrows it down.

    x # # # .      x  known empty ("ว่าง")
    x A . B .      #  a house belonging to nobody named
    # C . D .      .  unknown — a house may or may not stand here
    # . . # .      A–G  the seven named houses
    E . . F .
    . . G . .

The fifth column is entirely blank, and was missed on the first reading — the
question names nothing in it, so only the figure says it is there. It is: the
ผัง is ruled by six vertical lines at 33.3-point spacing (``sheetpipe figures``
cuts the crop that shows them). It is not decorative either — those six cells
neighbour B, D and F, and including them moves the answer from 5 to 7.

Method: fifteen unknown cells, so 2¹⁵ assignments. ``solve`` walks them in an
order that lets each neighbour-count constraint be tested the moment its cell's
neighbourhood is fully decided, pruning most of the tree; ``check`` enumerates
all 32768 flat, with a separately written adjacency routine.
"""

from __future__ import annotations

from itertools import product

LAYOUT = (
    "x###.",
    "xA.B.",
    "#C.D.",
    "#..#.",
    "E..F.",
    "..G..",
)

PARAMS = {"deg_a": 5, "deg_b": 4, "deg_c": 4, "deg_d": 3, "deg_g": 2}
ANSWER = 7
VARIANTS = [
    {"deg_a": 4},
    {"deg_g": 3},
    {"deg_b": 5},
    {"deg_d": 4},
    {"deg_a": 5, "deg_b": 4, "deg_c": 4, "deg_d": 4, "deg_g": 2},
]

_ROWS, _COLS = len(LAYOUT), len(LAYOUT[0])


def _cells():
    return [(r, c) for r in range(_ROWS) for c in range(_COLS)]


def _neighbours(r: int, c: int):
    return [(r + dr, c + dc)
            for dr in (-1, 0, 1) for dc in (-1, 0, 1)
            if (dr or dc) and 0 <= r + dr < _ROWS and 0 <= c + dc < _COLS]


def _named() -> dict[str, tuple[int, int]]:
    return {LAYOUT[r][c]: (r, c) for r, c in _cells() if LAYOUT[r][c].isalpha()}


def _unknowns() -> list[tuple[int, int]]:
    return [(r, c) for r, c in _cells() if LAYOUT[r][c] == "."]


def _degree(at, houses: set) -> int:
    return sum(1 for n in _neighbours(*at) if n in houses)


def _fixed_houses() -> set:
    return {(r, c) for r, c in _cells() if LAYOUT[r][c] not in ("x", ".")}


def solve(deg_a=5, deg_b=4, deg_c=4, deg_d=3, deg_g=2):
    """Largest possible (neighbours of E) + (neighbours of F)."""
    named = _named()
    unknown = _unknowns()
    wanted = {"A": deg_a, "B": deg_b, "C": deg_c, "D": deg_d, "G": deg_g}
    base = _fixed_houses()

    # A constraint can be judged as soon as every neighbour of its cell is fixed.
    ready: dict[int, list[str]] = {}
    for name, at in named.items():
        if name not in wanted:
            continue
        pending = [i for i, cell in enumerate(unknown)
                   if cell in set(_neighbours(*at))]
        ready.setdefault(max(pending) if pending else -1, []).append(name)

    best = None

    def walk(i: int, houses: set):
        nonlocal best
        for name in ready.get(i - 1, []):
            if _degree(named[name], houses) != wanted[name]:
                return
        if i == len(unknown):
            best = max(best or 0, _degree(named["E"], houses)
                       + _degree(named["F"], houses))
            return
        walk(i + 1, houses)                       # leave this cell empty
        walk(i + 1, houses | {unknown[i]})        # put a house on it

    walk(0, base)
    return best


def check(deg_a=5, deg_b=4, deg_c=4, deg_d=3, deg_g=2):
    """Independent: all 2ⁿ assignments, flat, with adjacency recomputed."""
    named = _named()
    unknown = _unknowns()
    wanted = {"A": deg_a, "B": deg_b, "C": deg_c, "D": deg_d, "G": deg_g}
    base = _fixed_houses()

    def degree(at, houses) -> int:
        r, c = at
        return sum(1 for (hr, hc) in houses
                   if max(abs(hr - r), abs(hc - c)) == 1)

    best = None
    for bits in product((False, True), repeat=len(unknown)):
        houses = base | {cell for cell, on in zip(unknown, bits) if on}
        if any(degree(named[n], houses) != want for n, want in wanted.items()):
            continue
        total = degree(named["E"], houses) + degree(named["F"], houses)
        best = total if best is None else max(best, total)
    return best

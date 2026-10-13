"""Shared pieces of the geography (ส 5) sets.

* ``SUBJECT`` and the level dicts the unit files register under;
* ``stage`` — the learning stage a set sits at (foundation, fluency,
  application), set on the class because geography has no reviewed-stage map;
* the eight compass directions, clockwise from north, and how a step on a grid
  is named;
* ``GridMap`` — the drawn map of lettered places on a grid that the direction
  sets read. Like the block programs, the pictures carry no Thai: places are
  ``A``-``H`` and north is an arrow marked ``N``. Every family is a fixed
  tuple built from a seeded generator, so ``otk/pictures/registry.py`` knows
  every drawable id in advance;
* ``choices`` — a question whose choices are fixed strings, each wrong one
  optionally named for the mistake it stands for;
* ``clock`` — a time of day as Thai stems write it (``14.05 น.``).
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.distractors import fixed, length_matched_label_pool
from otk.core.mistakes import named
from otk.core.question import GeneratedQuestion

SUBJECT = "ภูมิศาสตร์"
P1, P2, P3, P6 = {"th": "ป.1"}, {"th": "ป.2"}, {"th": "ป.3"}, {"th": "ป.6"}
M1, M2, M3, M4 = {"th": "ม.1"}, {"th": "ม.2"}, {"th": "ม.3"}, {"th": "ม.4"}


# As science_stages names them. Not imported from there: that module applies the
# science stages when it loads, so it must load after every set.
STAGE_METADATA = {
    1: ("foundation", {"th": "ปูพื้นฐาน", "en": "Foundation"}),
    2: ("fluency", {"th": "ฝึกคล่อง", "en": "Fluency"}),
    3: ("application", {"th": "ประยุกต์", "en": "Application"}),
}


def stage(n: int):
    """Class decorator, inside ``@question_type``: file the set at stage ``n``."""
    def deco(cls):
        key, label = STAGE_METADATA[n]
        cls.learning_stage, cls.learning_stage_key, cls.learning_stage_label = n, key, dict(label)
        return cls
    return deco


# ── directions ───────────────────────────────────────────────────────────────

DIRECTIONS = ("ทิศเหนือ", "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออก", "ทิศตะวันออกเฉียงใต้",
              "ทิศใต้", "ทิศตะวันตกเฉียงใต้", "ทิศตะวันตก", "ทิศตะวันตกเฉียงเหนือ")
CARDINAL = DIRECTIONS[::2]
# (dx, dy) of one step in each direction, x to the east and y to the north.
STEPS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))


def turned(direction: str, eighths: int) -> str:
    """The direction ``eighths`` × 45° clockwise of ``direction`` (negative: anticlockwise)."""
    return DIRECTIONS[(DIRECTIONS.index(direction) + eighths) % 8]


def mirrored(direction: str) -> str:
    """East and west swapped, north and south kept: the left-right slip."""
    dx, dy = STEPS[DIRECTIONS.index(direction)]
    return DIRECTIONS[STEPS.index((-dx, dy))]


def bearing(dx: int, dy: int) -> str | None:
    """The direction from one square to another, or None unless they line up
    along a row, a column or a diagonal (only then is one direction exact)."""
    if (dx, dy) == (0, 0) or (dx and dy and abs(dx) != abs(dy)):
        return None
    step = ((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))
    return DIRECTIONS[STEPS.index(step)]


# ── the drawn grid map ───────────────────────────────────────────────────────

LETTERS = "ABCDEFGH"


class GridMap(NamedTuple):
    """Lettered places on a ``size`` × ``size`` grid, ``(x, y)`` from the
    bottom-left square. ``board`` marks the top edge as the front of a
    classroom (a plan); otherwise an ``N`` arrow marks north (a map)."""
    size: int
    places: tuple[tuple[int, int], ...]     # the square of A, B, C, ...
    board: bool = False

    @property
    def asset_id(self) -> str:
        kind = "geoplan" if self.board else "geomap"
        return f"{kind}{self.size}_" + "".join(f"{x}{y}" for x, y in self.places)

    def letter_at(self, pos: tuple[int, int]) -> str | None:
        return LETTERS[self.places.index(pos)] if pos in self.places else None

    def alt(self) -> str:
        what = ("แผนผังห้องเรียน ด้านบนของภาพคือหน้าห้องที่มีกระดาน"
                if self.board else "แผนที่ ลูกศร N ชี้ไปทางทิศเหนือซึ่งอยู่ด้านบนของภาพ")
        where = " ".join(f"{LETTERS[i]} อยู่คอลัมน์ที่ {x + 1} จากซ้าย แถวที่ {y + 1} จากล่าง"
                         for i, (x, y) in enumerate(self.places))
        return f"{what} เป็นตาราง {self.size} × {self.size} ช่อง {where}"


def _grid_maps(seed: int, count: int, size: int, places: int, board: bool,
               aligned: int) -> tuple[GridMap, ...]:
    """``count`` distinct maps, each with at least ``aligned`` pairs of places
    that line up exactly (so a direction question has an exact answer)."""
    rng = Random(seed)
    cells = [(x, y) for x in range(size) for y in range(size)]
    found: dict[str, GridMap] = {}
    while len(found) < count:
        spot = tuple(rng.sample(cells, places))
        pairs = sum(1 for a in spot for b in spot
                    if a < b and bearing(b[0] - a[0], b[1] - a[1]))
        if pairs >= aligned:
            spec = GridMap(size, spot, board)
            found.setdefault(spec.asset_id, spec)
    return tuple(found.values())


COMMUNITY_MAPS = _grid_maps(5101, 40, 6, 7, False, 6)
CLASSROOM_PLANS = _grid_maps(5102, 30, 5, 6, True, 5)
GRID_MAP_SPECS = (*COMMUNITY_MAPS, *CLASSROOM_PLANS)


def map_question(spec: GridMap, *, stem: str, correct: str, wrongs, hint: str,
                 topic: str) -> GeneratedQuestion:
    """A question that shows ``spec``'s picture, then asks in Thai."""
    q = choices(stem=stem, correct=correct, wrongs=wrongs, hint=hint, topic=topic)
    q.stem.insert(0, image(spec.asset_id, alt=spec.alt()))
    return q


# ── choices and times ────────────────────────────────────────────────────────

def choices(*, stem: str, correct: str, wrongs, hint: str, topic: str) -> GeneratedQuestion:
    """Fixed choices. ``wrongs`` are strings or ``(mistake, string)`` pairs, most
    diagnostic first; duplicates of the answer or of each other are dropped."""
    seen = {correct}
    picked = []
    for w in wrongs:
        mistake, value = w if isinstance(w, tuple) else (None, w)
        if value in seen:
            continue
        seen.add(value)
        picked.append([text(named(mistake, value) if mistake else value)])
    return GeneratedQuestion(stem=[text(stem)], correct=[text(correct)],
                             distractors=fixed(*picked), topic=topic, hint=[text(hint)])


def scenario(rng: Random, rows, *, ask: str, hint: str, topic: str) -> GeneratedQuestion:
    """An application question: a situation and the one response that fits it.

    ``rows`` are ``(situation, response, wrongs)``. The other rows' responses
    are right for their own situations, never for this one, so they join the
    row's own wrongs as distractors; the pool prefers ones near the answer's
    length, so length gives nothing away.
    """
    i = rng.randrange(len(rows))
    situation, right, wrongs = rows[i]
    others = [row[1] for j, row in enumerate(rows) if j != i]
    return GeneratedQuestion(
        stem=[text(f"{situation} {ask}")], correct=[text(right)],
        distractors=length_matched_label_pool([right, *wrongs, *others]),
        topic=topic, hint=[text(hint)])


def clock(minutes: int) -> str:
    """Minutes after midnight (any day) as a Thai time: ``865`` -> ``14.25 น.``"""
    minutes %= 24 * 60
    return f"{minutes // 60:02d}.{minutes % 60:02d} น."


def number(x) -> str:
    """A whole or two-place number with thousands grouped: 12500 -> 12,500."""
    value = float(x)
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


# ── continents ───────────────────────────────────────────────────────────────

# Landforms that lie wholly in one continent, as Thai textbooks name them. The
# Urals, the Caucasus and Elbrus are left out: books disagree on their side.
CONTINENTS = {
    "ทวีปเอเชีย": ("เทือกเขาหิมาลัย", "ที่ราบสูงทิเบต", "ทะเลทรายโกบี", "แม่น้ำแยงซี",
                   "แม่น้ำโขง", "ทะเลสาบไบคาล", "แม่น้ำคงคา"),
    "ทวีปออสเตรเลียและโอเชียเนีย": ("แนวปะการังเกรตแบร์ริเออร์รีฟ", "แม่น้ำเมอร์รี",
                                    "ทะเลทรายเกรตวิกตอเรีย", "เทือกเขาเกรตดิไวดิง", "หินอูลูรู"),
    "ทวีปยุโรป": ("เทือกเขาแอลป์", "แม่น้ำดานูบ", "แม่น้ำไรน์", "แม่น้ำวอลกา",
                  "ฟยอร์ดชายฝั่งนอร์เวย์", "เทือกเขาพิเรนีส"),
    "ทวีปแอฟริกา": ("ทะเลทรายสะฮารา", "แม่น้ำไนล์", "แม่น้ำคองโก", "ทะเลสาบวิกตอเรีย",
                    "ภูเขาคิลิมันจาโร", "ทะเลทรายคาลาฮารี"),
    "ทวีปอเมริกาเหนือ": ("เทือกเขาร็อกกี", "ทะเลสาบเกรตเลกส์", "แม่น้ำมิสซิสซิปปี",
                         "หุบผาแกรนด์แคนยอน", "เทือกเขาแอปพาเลเชียน"),
    "ทวีปอเมริกาใต้": ("เทือกเขาแอนดีส", "แม่น้ำแอมะซอน", "ทะเลทรายอาตากามา",
                       "ทะเลสาบติติกากา", "ทุ่งหญ้าปัมปัส"),
}


def continent_question(rng: Random, focus: tuple[str, ...], *, topic: str) -> GeneratedQuestion:
    """A landform of one of the ``focus`` continents: name its continent, or
    pick the landform that lies in it from ones of other continents."""
    continent = rng.choice(focus)
    hint = "นึกภาพแผนที่โลก แล้ววางลักษณะภูมิประเทศนั้นลงบนทวีปที่มันตั้งอยู่"
    if rng.random() < 0.5:
        feature = rng.choice(CONTINENTS[continent])
        return choices(stem=f"“{feature}” อยู่ในทวีปใด", correct=continent,
                       wrongs=rng.sample([c for c in CONTINENTS if c != continent], 3),
                       hint=hint, topic=topic)
    others = [f for c, fs in CONTINENTS.items() if c != continent for f in fs]
    return choices(stem=f"ลักษณะภูมิประเทศใดอยู่ใน{continent}",
                   correct=rng.choice(CONTINENTS[continent]), wrongs=rng.sample(others, 3),
                   hint=hint, topic=topic)

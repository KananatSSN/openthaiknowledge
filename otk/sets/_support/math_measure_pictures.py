"""Measurement and data read off a drawing: a ruler, a pictograph of real
icons, a dial scale, a measuring jug, a cuboid of unit cubes.

These are the instruments the สสวท. books teach from. The catalog described
them in words ("ไม้บรรทัดไม่ได้เริ่มที่ 0") or drew charts as rows of ● in text.
Specs are finite; ``otk/pictures/measure_pictures.py``
draws one PNG each, and the answer comes from the same spec.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.question import GeneratedQuestion
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_pictures import BY_KEY, KINDS, _near, _order

# ── ป.1 ไม้บรรทัด ─────────────────────────────────────────────────────────────

class Ruler(NamedTuple):
    start: int           # where the object's left end sits on the ruler
    length: int          # centimetres

    @property
    def asset_id(self) -> str:
        return f"prul_{self.start}_{self.length}"


RULERS = tuple(Ruler(s, n) for s in (0, 0, 1, 2, 3) for n in range(2, 13)
               if s + n <= 15)
RULERS = tuple(dict.fromkeys(RULERS))


# ── ป.1–ป.2 แผนภูมิรูปภาพ ─────────────────────────────────────────────────────

class Pictograph(NamedTuple):
    rows: tuple[tuple[str, int], ...]      # (kind, icons drawn)
    key: int                               # one icon stands for this many

    @property
    def asset_id(self) -> str:
        return f"ppg{self.key}_" + "_".join(f"{k}{n}" for k, n in self.rows)

    def value(self, kind: str) -> int:
        return self.key * dict(self.rows)[kind]


def _pictographs(key: int, count: int) -> tuple[Pictograph, ...]:
    out = []
    for i in range(count):
        seed = f"ppg{key}_{i}"
        kinds = _order(seed, [k.key for k in KINDS])[:3 + i % 2]
        icons = _order(seed + "n", list(range(1, 10)))[:len(kinds)]
        out.append(Pictograph(tuple(zip(kinds, icons)), key))
    return tuple(out)


PICTOGRAPHS_P1 = _pictographs(1, 40)
PICTOGRAPHS_P2 = _pictographs(2, 20) + _pictographs(5, 20) + _pictographs(10, 20)
PICTO_ALT = "แผนภูมิรูปภาพ แต่ละแถวเป็นสิ่งของหนึ่งชนิด"


def _picto_question(p: Pictograph, rng: Random, topic: str) -> GeneratedQuestion:
    img = image(p.asset_id, alt=PICTO_ALT)
    kinds = [k for k, _ in p.rows]
    key_line = [] if p.key == 1 else [text(f"กำหนดให้ 1 รูป แทน {p.key} หน่วย")]
    ask = rng.randrange(3)
    if ask == 0:
        kind = BY_KEY[rng.choice(kinds)]
        v = p.value(kind.key)
        icons = dict(p.rows)[kind.key]
        # Counting icons and forgetting the key.
        return _math_q([*key_line, text(f"จากแผนภูมิ มี{kind.thai}กี่{kind.unit}"), img],
                       str(v), _near(v, icons, v + p.key, v - p.key, lo=1), topic)
    if ask == 1:
        most = rng.random() < 0.5
        # Rows have distinct counts (see _pictographs), so there is one answer.
        pick = (max if most else min)(kinds, key=p.value)
        return _text_q([*key_line, text("จากแผนภูมิ สิ่งใดมีจำนวน" + ("มากที่สุด" if most else "น้อยที่สุด")),
                        img], BY_KEY[pick].thai,
                       [BY_KEY[k].thai for k in kinds if k != pick] + ["มีเท่ากันทุกชนิด"], topic)
    a, b = rng.sample(kinds, 2)
    if p.value(a) < p.value(b):
        a, b = b, a
    diff = p.value(a) - p.value(b)
    icon_diff = dict(p.rows)[a] - dict(p.rows)[b]
    ka, kb = BY_KEY[a], BY_KEY[b]
    return _math_q([*key_line, text(f"จากแผนภูมิ {ka.thai}มากกว่า{kb.thai}อยู่เท่าใด"), img],
                   str(diff), _near(diff, icon_diff, p.value(a) + p.value(b), p.value(a), lo=1), topic)


# ── ป.2 เครื่องชั่ง ───────────────────────────────────────────────────────────

class Scale(NamedTuple):
    top: int             # the dial reads 0 to ``top`` kilograms
    kg: int
    khit: int            # ขีด, tenths of a kilogram

    @property
    def asset_id(self) -> str:
        return f"pscl_{self.top}_{self.kg}_{self.khit}"


# A needle resting on 0 weighs nothing, so that reading is left out.
SCALES = tuple(s for s in dict.fromkeys(
    Scale(top, (i * 7) % top, (i * 3 + 1) % 10) for top in (3, 5) for i in range(24))
    if s.kg or s.khit)


# ── ป.3 ถ้วยตวง ───────────────────────────────────────────────────────────────

class Jug(NamedTuple):
    top: int             # millilitres at the top mark
    step: int            # millilitres between marks
    level: int

    @property
    def asset_id(self) -> str:
        return f"pjug_{self.top}_{self.step}_{self.level}"


JUGS = tuple(dict.fromkeys(
    [Jug(500, 50, 50 * k) for k in range(2, 10)]
    + [Jug(1000, 100, 100 * k) for k in range(1, 10)]
    + [Jug(1000, 50, 50 * k) for k in range(3, 20, 2)]
    + [Jug(2000, 200, 200 * k) for k in range(1, 10)]))


# ── ป.5 ลูกบาศก์หน่วย ─────────────────────────────────────────────────────────

class Cubes(NamedTuple):
    w: int
    d: int
    h: int

    @property
    def asset_id(self) -> str:
        return f"pcub_{self.w}_{self.d}_{self.h}"


CUBES = tuple(Cubes(w, d, h) for w in range(2, 6) for d in range(2, 5) for h in range(1, 5)
              if w * d * h <= 60)


ALL_PICTURE_IDS = tuple(s.asset_id for s in (*RULERS, *PICTOGRAPHS_P1, *PICTOGRAPHS_P2,
                                             *SCALES, *JUGS, *CUBES))

"""Free-body diagram specs — the drawn pictures behind the ``แผนภาพแสดงแรง`` sets.

``ว 2.2`` has four diagram indicators, and until now all four *described* their
diagram in words and asked the student to pick the right description. These
specs let the question show the drawing instead, the same way ``elec.circuit_*``
shows a schematic: a finite pool of specs, one PNG rendered per spec by
``otk/pictures/generate.py``, and the question type picking the spec
it wants and reading its answer off the same numbers the picture was drawn from.

**Nothing Thai is drawn into the PNG.** The bundled matplotlib font has no Thai
glyphs, so the arrows are labelled with the physics symbols a Thai textbook uses
anyway — ``W`` น้ำหนัก, ``N`` แรงตั้งฉาก, ``f`` แรงเสียดทาน, ``P`` แรงผลัก/ดึง,
``FB`` แรงพยุง, ``FE``/``FM`` แรงไฟฟ้า/แรงแม่เหล็ก — and the Thai lives in the
stem and the choices. This is the same rule ``CIRCUIT_SPECS`` follows.

Each pool holds a couple of dozen hand-picked cases covering the situations
its indicator names, including the degenerate ones (zero resultant, floating
at rest). Diagrams are rendered on demand, so a pool can grow without
committing PNGs.
"""

from __future__ import annotations

from typing import NamedTuple

UP, DOWN, LEFT, RIGHT = "up", "down", "left", "right"

# Arrow symbols, and the Thai name each one carries in a stem or a choice.
SYMBOL_NAMES = {
    "W": "น้ำหนัก",
    "N": "แรงที่พื้นดัน",
    "f": "แรงเสียดทาน",
    "P": "แรงผลัก",
    "FB": "แรงพยุง",
    "FE": "แรงไฟฟ้า",
    "FM": "แรงแม่เหล็ก",
    "F1": "แรงที่หนึ่ง",
    "F2": "แรงที่สอง",
    "F3": "แรงที่สาม",
}


class Arrow(NamedTuple):
    symbol: str                        # key of SYMBOL_NAMES — drawn on the picture
    newtons: int
    direction: str                     # UP / DOWN / LEFT / RIGHT

    @property
    def name(self) -> str:
        return SYMBOL_NAMES[self.symbol]


class ForceDiagramSpec(NamedTuple):
    """One drawn free-body diagram.

    ``scene`` picks what is drawn under the arrows: a box on the ground
    (``floor``), a block submerged in water (``water``), a box on a table
    (``table``), or the box alone (``plain``).
    """

    kind: str                          # netforce | friction | liquid | field
    scene: str                         # plain | floor | water | table
    arrows: tuple[Arrow, ...]

    @property
    def asset_id(self) -> str:
        parts = "_".join(f"{a.symbol}{a.newtons}{a.direction[0]}" for a in self.arrows)
        return f"fbd_{self.kind}_{parts}"

    def _sum(self, direction: str) -> int:
        return sum(a.newtons for a in self.arrows if a.direction == direction)

    @property
    def horizontal(self) -> int:
        """Rightwards resultant; negative means the resultant points left."""
        return self._sum(RIGHT) - self._sum(LEFT)

    @property
    def vertical(self) -> int:
        """Upwards resultant; negative means the resultant points down."""
        return self._sum(UP) - self._sum(DOWN)

    def of(self, symbol: str) -> Arrow:
        return next(a for a in self.arrows if a.symbol == symbol)


def _spec(kind: str, scene: str, *arrows: tuple[str, int, str]) -> ForceDiagramSpec:
    return ForceDiagramSpec(kind, scene, tuple(Arrow(*a) for a in arrows))


# ── ว 2.2 ม.2/2 — แรงลัพธ์ของแรงในแนวเดียวกัน ─────────────────────────────────
# Three horizontal forces on a box. The pool spans a resultant to the right, to
# the left, and exactly zero, because "no resultant arrow at all" is the case
# students get wrong most often.
NETFORCE_SPECS = [
    _spec("netforce", "plain", ("F1", 5, RIGHT), ("F2", 3, RIGHT), ("F3", 10, LEFT)),
    _spec("netforce", "plain", ("F1", 6, RIGHT), ("F2", 4, RIGHT), ("F3", 12, LEFT)),
    _spec("netforce", "plain", ("F1", 7, RIGHT), ("F2", 5, RIGHT), ("F3", 4, LEFT)),
    _spec("netforce", "plain", ("F1", 8, RIGHT), ("F2", 2, RIGHT), ("F3", 6, LEFT)),
    _spec("netforce", "plain", ("F1", 4, RIGHT), ("F2", 4, RIGHT), ("F3", 8, LEFT)),
    _spec("netforce", "plain", ("F1", 9, RIGHT), ("F2", 3, RIGHT), ("F3", 5, LEFT)),
    _spec("netforce", "plain", ("F1", 3, RIGHT), ("F2", 2, RIGHT), ("F3", 9, LEFT)),
    _spec("netforce", "plain", ("F1", 10, RIGHT), ("F2", 5, RIGHT), ("F3", 15, LEFT)),
    _spec("netforce", "plain", ("F1", 6, RIGHT), ("F2", 6, RIGHT), ("F3", 4, LEFT)),
    _spec("netforce", "plain", ("F1", 2, RIGHT), ("F2", 7, RIGHT), ("F3", 12, LEFT)),
    _spec("netforce", "plain", ("F1", 12, RIGHT), ("F2", 3, RIGHT), ("F3", 7, LEFT)),
    _spec("netforce", "plain", ("F1", 5, RIGHT), ("F2", 5, RIGHT), ("F3", 6, LEFT)),
    _spec("netforce", "plain", ("F1", 3, RIGHT), ("F2", 4, RIGHT), ("F3", 7, LEFT)),
    _spec("netforce", "plain", ("F1", 8, RIGHT), ("F2", 6, RIGHT), ("F3", 9, LEFT)),
    _spec("netforce", "plain", ("F1", 5, RIGHT), ("F2", 2, RIGHT), ("F3", 11, LEFT)),
    _spec("netforce", "plain", ("F1", 4, RIGHT), ("F2", 3, RIGHT), ("F3", 2, LEFT)),
    _spec("netforce", "plain", ("F1", 9, RIGHT), ("F2", 4, RIGHT), ("F3", 13, LEFT)),
    _spec("netforce", "plain", ("F1", 2, RIGHT), ("F2", 3, RIGHT), ("F3", 10, LEFT)),
    _spec("netforce", "plain", ("F1", 11, RIGHT), ("F2", 4, RIGHT), ("F3", 9, LEFT)),
    _spec("netforce", "plain", ("F1", 6, RIGHT), ("F2", 2, RIGHT), ("F3", 14, LEFT)),
    _spec("netforce", "plain", ("F1", 7, RIGHT), ("F2", 7, RIGHT), ("F3", 11, LEFT)),
    _spec("netforce", "plain", ("F1", 3, RIGHT), ("F2", 3, RIGHT), ("F3", 6, LEFT)),
    _spec("netforce", "plain", ("F1", 7, RIGHT), ("F2", 3, RIGHT), ("F3", 12, LEFT)),
    _spec("netforce", "plain", ("F1", 5, RIGHT), ("F2", 8, RIGHT), ("F3", 6, LEFT)),
    _spec("netforce", "plain", ("F1", 4, RIGHT), ("F2", 6, RIGHT), ("F3", 13, LEFT)),
    _spec("netforce", "plain", ("F1", 10, RIGHT), ("F2", 2, RIGHT), ("F3", 3, LEFT)),
    _spec("netforce", "plain", ("F1", 6, RIGHT), ("F2", 5, RIGHT), ("F3", 8, LEFT)),
    _spec("netforce", "plain", ("F1", 8, RIGHT), ("F2", 8, RIGHT), ("F3", 9, LEFT)),
]

# ── ว 2.2 ม.2/8 — แรงเสียดทานและแรงอื่น ๆ ─────────────────────────────────────
# A box on the ground with all four forces drawn. W and N always match (it never
# leaves the ground); f equals P where the box is still or moving steadily, and
# is smaller where the box speeds up.
FRICTION_SPECS = [
    _spec("friction", "floor", ("P", 6, RIGHT), ("f", 6, LEFT), ("W", 11, DOWN), ("N", 11, UP)),
    _spec("friction", "floor", ("P", 8, RIGHT), ("f", 8, LEFT), ("W", 14, DOWN), ("N", 14, UP)),
    _spec("friction", "floor", ("P", 5, RIGHT), ("f", 5, LEFT), ("W", 9, DOWN), ("N", 9, UP)),
    _spec("friction", "floor", ("P", 10, RIGHT), ("f", 4, LEFT), ("W", 12, DOWN), ("N", 12, UP)),
    _spec("friction", "floor", ("P", 12, RIGHT), ("f", 5, LEFT), ("W", 15, DOWN), ("N", 15, UP)),
    _spec("friction", "floor", ("P", 9, RIGHT), ("f", 3, LEFT), ("W", 10, DOWN), ("N", 10, UP)),
    _spec("friction", "floor", ("P", 7, RIGHT), ("f", 7, LEFT), ("W", 13, DOWN), ("N", 13, UP)),
    _spec("friction", "floor", ("P", 11, RIGHT), ("f", 6, LEFT), ("W", 14, DOWN), ("N", 14, UP)),
    _spec("friction", "floor", ("P", 4, RIGHT), ("f", 4, LEFT), ("W", 8, DOWN), ("N", 8, UP)),
    _spec("friction", "floor", ("P", 14, RIGHT), ("f", 8, LEFT), ("W", 16, DOWN), ("N", 16, UP)),
    _spec("friction", "floor", ("P", 6, RIGHT), ("f", 3, LEFT), ("W", 10, DOWN), ("N", 10, UP)),
    _spec("friction", "floor", ("P", 8, RIGHT), ("f", 5, LEFT), ("W", 12, DOWN), ("N", 12, UP)),
    _spec("friction", "floor", ("P", 9, RIGHT), ("f", 9, LEFT), ("W", 15, DOWN), ("N", 15, UP)),
    _spec("friction", "floor", ("P", 5, RIGHT), ("f", 2, LEFT), ("W", 8, DOWN), ("N", 8, UP)),
    _spec("friction", "floor", ("P", 10, RIGHT), ("f", 10, LEFT), ("W", 16, DOWN), ("N", 16, UP)),
    _spec("friction", "floor", ("P", 12, RIGHT), ("f", 8, LEFT), ("W", 14, DOWN), ("N", 14, UP)),
    _spec("friction", "floor", ("P", 7, RIGHT), ("f", 4, LEFT), ("W", 11, DOWN), ("N", 11, UP)),
    _spec("friction", "floor", ("P", 13, RIGHT), ("f", 13, LEFT), ("W", 17, DOWN), ("N", 17, UP)),
    _spec("friction", "floor", ("P", 6, RIGHT), ("f", 6, LEFT), ("W", 9, DOWN), ("N", 9, UP)),
    _spec("friction", "floor", ("P", 11, RIGHT), ("f", 9, LEFT), ("W", 13, DOWN), ("N", 13, UP)),
    _spec("friction", "floor", ("P", 8, RIGHT), ("f", 2, LEFT), ("W", 10, DOWN), ("N", 10, UP)),
    _spec("friction", "floor", ("P", 3, RIGHT), ("f", 3, LEFT), ("W", 7, DOWN), ("N", 7, UP)),
    _spec("friction", "floor", ("P", 15, RIGHT), ("f", 10, LEFT), ("W", 18, DOWN), ("N", 18, UP)),
    _spec("friction", "floor", ("P", 9, RIGHT), ("f", 5, LEFT), ("W", 12, DOWN), ("N", 12, UP)),
    _spec("friction", "floor", ("P", 12, RIGHT), ("f", 12, LEFT), ("W", 15, DOWN), ("N", 15, UP)),
    _spec("friction", "floor", ("P", 10, RIGHT), ("f", 7, LEFT), ("W", 13, DOWN), ("N", 13, UP)),
]

# ── ว 2.2 ม.2/5 — แรงที่กระทำต่อวัตถุในของเหลว ────────────────────────────────
# Weight down, buoyant force up. Equal arrows float at rest; a shorter buoyant
# arrow sinks.
LIQUID_SPECS = [
    _spec("liquid", "water", ("W", 6, DOWN), ("FB", 6, UP)),
    _spec("liquid", "water", ("W", 8, DOWN), ("FB", 8, UP)),
    _spec("liquid", "water", ("W", 10, DOWN), ("FB", 10, UP)),
    _spec("liquid", "water", ("W", 7, DOWN), ("FB", 7, UP)),
    _spec("liquid", "water", ("W", 9, DOWN), ("FB", 4, UP)),
    _spec("liquid", "water", ("W", 12, DOWN), ("FB", 5, UP)),
    _spec("liquid", "water", ("W", 10, DOWN), ("FB", 6, UP)),
    _spec("liquid", "water", ("W", 8, DOWN), ("FB", 3, UP)),
    _spec("liquid", "water", ("W", 14, DOWN), ("FB", 9, UP)),
    _spec("liquid", "water", ("W", 11, DOWN), ("FB", 7, UP)),
    _spec("liquid", "water", ("W", 5, DOWN), ("FB", 5, UP)),
    _spec("liquid", "water", ("W", 9, DOWN), ("FB", 9, UP)),
    _spec("liquid", "water", ("W", 11, DOWN), ("FB", 11, UP)),
    _spec("liquid", "water", ("W", 12, DOWN), ("FB", 12, UP)),
    _spec("liquid", "water", ("W", 4, DOWN), ("FB", 4, UP)),
    _spec("liquid", "water", ("W", 13, DOWN), ("FB", 13, UP)),
    _spec("liquid", "water", ("W", 5, DOWN), ("FB", 2, UP)),
    _spec("liquid", "water", ("W", 6, DOWN), ("FB", 3, UP)),
    _spec("liquid", "water", ("W", 7, DOWN), ("FB", 4, UP)),
    _spec("liquid", "water", ("W", 9, DOWN), ("FB", 6, UP)),
    _spec("liquid", "water", ("W", 11, DOWN), ("FB", 5, UP)),
    _spec("liquid", "water", ("W", 12, DOWN), ("FB", 8, UP)),
    _spec("liquid", "water", ("W", 13, DOWN), ("FB", 6, UP)),
    _spec("liquid", "water", ("W", 14, DOWN), ("FB", 10, UP)),
    _spec("liquid", "water", ("W", 7, DOWN), ("FB", 2, UP)),
    _spec("liquid", "water", ("W", 10, DOWN), ("FB", 3, UP)),
]

# ── ว 2.2 ม.2/12 — แรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง ────────────────────────
# An object resting on a table inside a field. W and N match; the field force is
# horizontal, and both magnetic and electric cases appear.
FIELD_SPECS = [
    _spec("field", "table", ("W", 8, DOWN), ("N", 8, UP), ("FM", 3, RIGHT)),
    _spec("field", "table", ("W", 10, DOWN), ("N", 10, UP), ("FM", 4, LEFT)),
    _spec("field", "table", ("W", 6, DOWN), ("N", 6, UP), ("FM", 5, RIGHT)),
    _spec("field", "table", ("W", 12, DOWN), ("N", 12, UP), ("FM", 6, LEFT)),
    _spec("field", "table", ("W", 9, DOWN), ("N", 9, UP), ("FE", 4, RIGHT)),
    _spec("field", "table", ("W", 7, DOWN), ("N", 7, UP), ("FE", 2, LEFT)),
    _spec("field", "table", ("W", 11, DOWN), ("N", 11, UP), ("FE", 5, RIGHT)),
    _spec("field", "table", ("W", 5, DOWN), ("N", 5, UP), ("FE", 3, LEFT)),
    _spec("field", "table", ("W", 8, DOWN), ("N", 8, UP), ("FM", 5, LEFT)),
    _spec("field", "table", ("W", 10, DOWN), ("N", 10, UP), ("FM", 2, RIGHT)),
    _spec("field", "table", ("W", 6, DOWN), ("N", 6, UP), ("FM", 3, LEFT)),
    _spec("field", "table", ("W", 12, DOWN), ("N", 12, UP), ("FM", 4, RIGHT)),
    _spec("field", "table", ("W", 9, DOWN), ("N", 9, UP), ("FM", 6, RIGHT)),
    _spec("field", "table", ("W", 7, DOWN), ("N", 7, UP), ("FM", 4, LEFT)),
    _spec("field", "table", ("W", 11, DOWN), ("N", 11, UP), ("FM", 3, RIGHT)),
    _spec("field", "table", ("W", 5, DOWN), ("N", 5, UP), ("FM", 2, LEFT)),
    _spec("field", "table", ("W", 14, DOWN), ("N", 14, UP), ("FM", 5, RIGHT)),
    _spec("field", "table", ("W", 13, DOWN), ("N", 13, UP), ("FM", 7, LEFT)),
    _spec("field", "table", ("W", 9, DOWN), ("N", 9, UP), ("FE", 3, LEFT)),
    _spec("field", "table", ("W", 7, DOWN), ("N", 7, UP), ("FE", 5, RIGHT)),
    _spec("field", "table", ("W", 11, DOWN), ("N", 11, UP), ("FE", 4, LEFT)),
    _spec("field", "table", ("W", 5, DOWN), ("N", 5, UP), ("FE", 2, RIGHT)),
    _spec("field", "table", ("W", 10, DOWN), ("N", 10, UP), ("FE", 6, LEFT)),
    _spec("field", "table", ("W", 8, DOWN), ("N", 8, UP), ("FE", 3, RIGHT)),
    _spec("field", "table", ("W", 12, DOWN), ("N", 12, UP), ("FE", 5, LEFT)),
    _spec("field", "table", ("W", 6, DOWN), ("N", 6, UP), ("FE", 4, RIGHT)),
]

ALL_FORCE_DIAGRAM_SPECS = (
    NETFORCE_SPECS + FRICTION_SPECS + LIQUID_SPECS + FIELD_SPECS
)


# ── Turning a spec into a question ───────────────────────────────────────────

def alt_text(spec: ForceDiagramSpec) -> str:
    """Thai description of the drawing, for screen readers and the PDF fallback.

    The picture itself carries no Thai (the bundled font has none), so this is
    where a reader who cannot see the image gets the same information.
    """
    where = {
        "water": "วัตถุจมอยู่ในของเหลว",
        "floor": "กล่องวางบนพื้นราบ",
        "table": "วัตถุวางนิ่งบนโต๊ะ",
        "plain": "วัตถุหนึ่งชิ้น",
    }[spec.scene]
    arrows = " ".join(
        f"{a.name} {a.newtons} นิวตัน ชี้{DIRECTION_WORDS[a.direction]}"
        for a in spec.arrows
    )
    return f"แผนภาพแสดงแรงที่กระทำต่อ{where} โดยความยาวลูกศรแปรตามขนาดของแรง — {arrows}"


DIRECTION_WORDS = {UP: "ขึ้น", DOWN: "ลง", LEFT: "ไปทางซ้าย", RIGHT: "ไปทางขวา"}


def diagram_question(spec: ForceDiagramSpec, *, stem: str, correct: str,
                     wrongs: tuple[str, ...], hint: str, topic: str):
    """A question whose stem *shows* ``spec``'s drawing, then asks in Thai."""
    from otk.core.content import image, text
    from otk.core.distractors import label_pool
    from otk.core.question import GeneratedQuestion

    return GeneratedQuestion(
        stem=[image(spec.asset_id, alt=alt_text(spec)), text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def magnitude_phrase(value: int) -> str:
    """How a resultant is said in Thai: its size and direction, or zero."""
    if value == 0:
        return "แรงลัพธ์เป็นศูนย์"
    return f"แรงลัพธ์ {abs(value)} นิวตัน ไปทาง{'ขวา' if value > 0 else 'ซ้าย'}"

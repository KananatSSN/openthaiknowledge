"""Drawn circuit diagrams for ป.6 ไฟฟ้าเบื้องต้น — ``ว 2.3 ป.6/1`` and ``ป.6/2``.

``ว 2.3 ป.6/2`` is *เขียนแผนภาพและต่อวงจรไฟฟ้าอย่างง่าย*. A multiple-choice item
cannot have a learner draw or wire anything, but it can put a real schematic in
front of them and ask what it says — which is the half of the indicator that
survives the format. Everything here exists so that half is answered from a
picture rather than from a sentence describing one.

Two pools:

* ``SYMBOL_CARDS`` — one symbol alone on a card, for *this symbol stands for
  which device*.
* ``P6_CIRCUIT_SPECS`` — a whole simple circuit drawn in those symbols: cells in
  series down the left edge, a switch on the bottom rail, bulbs in series along
  the top rail or in parallel as branches between the rails.

Nothing Thai is drawn into a PNG: the bundled matplotlib font (DejaVu Sans) has
no Thai glyphs, so Thai lives in the stem, the choices and the alt text. These
schematics carry no text at all — the symbols are the whole content. That is the
same rule ``CIRCUIT_SPECS`` and ``ALL_FORCE_DIAGRAM_SPECS`` follow.

**Two alt texts, on purpose.** ``layout_alt`` names what is drawn and refuses to
say how it is connected; ``full_alt`` says both. The rule is that the alt text
carries everything the picture shows *except the thing being asked*. Reading the
layout, or spotting the fault in it, therefore takes ``layout_alt`` — otherwise
the question answers itself for a screen reader, and in a printed worksheet,
where an image renders as its alt text alone. Only where the layout is given and
the answer is a *consequence* of it (one bulb of several burns out) may a set use
``full_alt``. ``elec.circuit_*`` settles the same question the same way.
"""

from __future__ import annotations

from typing import NamedTuple

# ── the symbol cards ─────────────────────────────────────────────────────────

class SymbolCard(NamedTuple):
    """One circuit symbol on its own, with the two things a question asks of it.

    ``shape`` describes the drawing without naming the device — it is what the
    alt text may say when the device name is the answer.
    """
    code: str        # ASCII, also the asset id suffix
    device: str      # ชื่ออุปกรณ์ — the answer to the Foundation set
    shape: str       # คำบรรยายรูปสัญลักษณ์ ที่ยังไม่บอกชื่ออุปกรณ์
    function: str    # หน้าที่ในวงจร

    @property
    def asset_id(self) -> str:
        return f"p6sym_{self.code}"


SYMBOL_CARDS = (
    SymbolCard(
        "cell", "เซลล์ไฟฟ้า",
        "เส้นตรงยาวหนึ่งเส้นและเส้นตรงสั้นหนึ่งเส้นวางขนานกัน โดยมีสายไฟต่อออกทั้งสองข้าง",
        "ให้พลังงานไฟฟ้าแก่วงจร",
    ),
    SymbolCard(
        "battery", "แบตเตอรี่ (เซลล์ไฟฟ้าหลายเซลล์ต่ออนุกรม)",
        "เส้นยาวสลับเส้นสั้นเรียงต่อกันหลายคู่ โดยมีสายไฟต่อออกทั้งสองข้าง",
        "ให้พลังงานไฟฟ้าแก่วงจรมากกว่าเซลล์เดียว",
    ),
    SymbolCard(
        "bulb", "หลอดไฟ",
        "วงกลมที่มีเส้นตรงสองเส้นตัดกันเป็นกากบาทอยู่ภายใน",
        "เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานแสงและความร้อน",
    ),
    SymbolCard(
        "switch_open", "สวิตช์ที่เปิดวงจรอยู่",
        "จุดต่อสองจุดบนสายไฟ โดยมีก้านเอียงขึ้นไม่แตะจุดต่ออีกด้านหนึ่ง",
        "ตัดวงจร ทำให้กระแสไฟฟ้าไหลผ่านไม่ได้",
    ),
    SymbolCard(
        "switch_closed", "สวิตช์ที่ปิดวงจรอยู่",
        "จุดต่อสองจุดบนสายไฟ โดยมีก้านวางแตะจุดต่อทั้งสองด้าน",
        "ต่อวงจรให้ครบ ทำให้กระแสไฟฟ้าไหลผ่านได้",
    ),
    SymbolCard(
        "wire", "สายไฟ",
        "เส้นตรงเส้นเดียวที่หักเป็นมุมฉาก ไม่มีสัญลักษณ์อื่นคั่นอยู่",
        "เป็นตัวนำไฟฟ้าเชื่อมส่วนประกอบต่าง ๆ เข้าด้วยกัน",
    ),
)


# ── whole circuits ───────────────────────────────────────────────────────────

WIRING_WORDS = {"series": "อนุกรม", "parallel": "ขนาน"}


class P6CircuitSpec(NamedTuple):
    """One drawn schematic at ป.6 level: cells, bulbs, a switch, maybe a break.

    ``gap`` is a wire drawn stopping short of the corner — the วงจรไม่ครบวงจร
    that ``ว 2.3 ป.6/2`` exists to catch. A single bulb is filed as ``series``
    because there is nothing yet to be parallel *to*; the sub-pools below keep
    it out of any question that asks how the bulbs are connected.
    """
    cells: int        # 1–3, always in series down the left edge
    bulbs: int        # 1–3
    wiring: str       # "series" | "parallel"
    switch: str       # "closed" | "open"
    gap: bool         # one wire drawn not reaching the corner

    @property
    def asset_id(self) -> str:
        tail = "_gap" if self.gap else ""
        return f"p6c_{self.cells}cell_{self.bulbs}{self.wiring}_{self.switch}{tail}"

    @property
    def complete(self) -> bool:
        """ครบวงจรหรือไม่ — every wire joined and the switch pressed closed."""
        return self.switch == "closed" and not self.gap

    @property
    def lights(self) -> bool:
        """หลอดไฟสว่างหรือไม่. A complete loop is the whole condition at ป.6."""
        return self.complete

    @property
    def wiring_word(self) -> str:
        return WIRING_WORDS[self.wiring]

    @property
    def one_bulb_burns_out(self) -> str:
        """ผลเมื่อหลอดไฟดวงหนึ่งขาด — the ป.6/5 comparison, read off the picture."""
        if self.wiring == "series":
            return "หลอดไฟดวงที่เหลือดับทั้งหมด เพราะวงจรอนุกรมขาดตอนเดียวก็ไม่ครบวงจร"
        return "หลอดไฟดวงที่เหลือยังสว่างตามปกติ เพราะแต่ละดวงมีเส้นทางของกระแสไฟฟ้าเป็นของตัวเอง"


# The specs shipped as built-in assets. Kept here so
# otk/pictures/generate.py draws exactly the set these types ask
# about — the picture and the answer come from one table.
P6_CIRCUIT_SPECS = tuple(P6CircuitSpec(*t) for t in (
    # complete and lit, one bulb — for counting cells and for "does it light"
    (1, 1, "series", "closed", False),
    (2, 1, "series", "closed", False),
    (3, 1, "series", "closed", False),
    # complete and lit, several bulbs — series against parallel
    (2, 2, "series", "closed", False),
    (2, 3, "series", "closed", False),
    (3, 2, "series", "closed", False),
    (2, 2, "parallel", "closed", False),
    (2, 3, "parallel", "closed", False),
    (3, 3, "parallel", "closed", False),
    # the switch left open
    (1, 2, "series", "open", False),
    (2, 1, "series", "open", False),
    (2, 2, "parallel", "open", False),
    # a wire that does not reach the corner
    (2, 1, "series", "closed", True),
    (2, 2, "parallel", "closed", True),
    # Wave H: every remaining lit multi-bulb layout, and more faults
    (1, 2, "series", "closed", False),
    (1, 3, "series", "closed", False),
    (3, 3, "series", "closed", False),
    (1, 2, "parallel", "closed", False),
    (1, 3, "parallel", "closed", False),
    (3, 2, "parallel", "closed", False),
    (1, 1, "series", "open", False),
    (3, 1, "series", "open", False),
    (3, 2, "series", "open", False),
    (2, 3, "parallel", "open", False),
    (1, 1, "series", "closed", True),
    (3, 2, "series", "closed", True),
    (2, 3, "series", "closed", True),
))

#: Circuits whose bulbs can be asked about — two or more, and all of them lit.
MULTI_BULB_CIRCUITS = tuple(
    s for s in P6_CIRCUIT_SPECS if s.bulbs >= 2 and s.lights
)
#: Circuits that are not complete, plus enough working ones that "ไม่สว่าง" is
#: never simply the right answer.
FAULT_CIRCUITS = P6_CIRCUIT_SPECS


# ── what a reader who cannot see the picture is told ─────────────────────────

def card_alt(card: SymbolCard) -> str:
    """Describes the symbol's *shape* only — its name is the answer."""
    return f"สัญลักษณ์ในแผนภาพวงจรไฟฟ้า: {card.shape}"


def layout_alt(spec: P6CircuitSpec) -> str:
    """Names what is drawn, never how it is connected.

    Used where the layout itself is the answer. Compare ``full_alt``.
    """
    return ("แผนภาพวงจรไฟฟ้าที่เขียนด้วยสัญลักษณ์ แสดงเซลล์ไฟฟ้าที่ขอบซ้าย "
            "สวิตช์บนสายไฟด้านล่าง และหลอดไฟในวงจร")


def full_alt(spec: P6CircuitSpec) -> str:
    """Says everything the picture shows, because the answer is a consequence."""
    switch = "สวิตช์ปิดวงจรอยู่" if spec.switch == "closed" else "สวิตช์เปิดวงจรอยู่"
    gap = " และมีสายไฟเส้นหนึ่งปลายไม่ต่อถึงมุมวงจร" if spec.gap else ""
    return (f"แผนภาพวงจรไฟฟ้าที่เขียนด้วยสัญลักษณ์ แสดงเซลล์ไฟฟ้า {spec.cells} เซลล์ต่ออนุกรม "
            f"หลอดไฟ {spec.bulbs} ดวงต่อแบบ{spec.wiring_word} โดย{switch}{gap}")


def diagram_question(asset_id: str, alt: str, *, stem: str, correct: str,
                     wrongs: tuple[str, ...], hint: str, topic: str):
    """A question whose stem *shows* the schematic, then asks in Thai."""
    from otk.core.content import image, text
    from otk.core.distractors import label_pool
    from otk.core.question import GeneratedQuestion

    return GeneratedQuestion(
        stem=[image(asset_id, alt=alt), text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )

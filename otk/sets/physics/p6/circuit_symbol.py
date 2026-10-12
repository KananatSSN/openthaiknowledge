"""สัญลักษณ์ไฟฟ้าและการอ่านแผนภาพวงจรไฟฟ้า

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/2

Sets moved here from: science_wave_g1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.circuit_symbols import (
    FAULT_CIRCUITS,
    MULTI_BULB_CIRCUITS,
    SYMBOL_CARDS,
    card_alt,
    diagram_question,
    layout_alt,
)
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_g1 import SIXTH

PROVENANCE = Provenance("original")


SYMBOL_TOPIC = "สัญลักษณ์ไฟฟ้าและการอ่านแผนภาพวงจรไฟฟ้า"


def _layout_words(spec) -> str:
    return (f"เซลล์ไฟฟ้า {spec.cells} เซลล์ต่ออนุกรม "
            f"และหลอดไฟ {spec.bulbs} ดวงต่อกันแบบ{spec.wiring_word}")


FIX_GAP = "ต่อปลายสายไฟที่ยังไม่เชื่อมถึงกันให้ครบเป็นวงปิด"


FIX_SWITCH = "กดสวิตช์ให้ก้านแตะจุดต่อทั้งสองด้าน เพื่อปิดวงจร"


FIX_NONE = "ไม่ต้องแก้ไข วงจรนี้ครบวงจรอยู่แล้ว หลอดไฟจึงสว่าง"


WRONG_CIRCUIT_FIXES = ("เพิ่มเซลล์ไฟฟ้าอีกหนึ่งเซลล์ เพราะพลังงานไฟฟ้าไม่พอ",
                       "เปลี่ยนหลอดไฟทุกดวงเป็นหลอดใหม่",
                       "สลับขั้วเซลล์ไฟฟ้าทุกเซลล์",
                       "ต่อสายไฟเพิ่มอีกเส้นขนานกับหลอดไฟ")


@question_type(
    "phys.circuit_symbol_foundation",
    display_name={"th": "บอกชื่ออุปกรณ์ไฟฟ้าจากสัญลักษณ์ที่ใช้ในแผนภาพวงจร"},
    level=SIXTH, subject=SUBJECT, topic=SYMBOL_TOPIC,
)
class CircuitSymbolFoundation(QuestionType):
    """One symbol on a card; which device it stands for.

    The alt text describes the symbol's shape and stops there — naming the
    device is the answer.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(SYMBOL_CARDS))
        card = SYMBOL_CARDS[index]
        others = [c.device for i, c in enumerate(SYMBOL_CARDS) if i != index]
        return diagram_question(
            card.asset_id, card_alt(card),
            stem="สัญลักษณ์ในภาพใช้แทนอุปกรณ์ใดในแผนภาพวงจรไฟฟ้า",
            correct=card.device,
            wrongs=tuple(rng.sample(others, 3)),
            hint="ดูรูปร่างของสัญลักษณ์ แล้วนึกถึงอุปกรณ์ที่ทำหน้าที่ตรงกับรูปนั้นในวงจรไฟฟ้า",
            topic=SYMBOL_TOPIC,
        )


@question_type(
    "phys.circuit_symbol_fluency",
    display_name={"th": "อ่านจำนวนเซลล์ไฟฟ้าและวิธีต่อหลอดไฟจากแผนภาพวงจร"},
    level=SIXTH, subject=SUBJECT, topic=SYMBOL_TOPIC,
)
class CircuitSymbolFluency(QuestionType):
    """A whole schematic; what it says.

    Distractors change one fact at a time — the cell count, or the way the bulbs
    are connected — so a student who reads only half the picture still lands on a
    wrong choice rather than on the right one by luck.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(MULTI_BULB_CIRCUITS)
        other_wiring = "ขนาน" if spec.wiring == "series" else "อนุกรม"
        # Each wrong reading changes the cell count, the bulb count or the
        # wiring (or two of them); three are drawn from every such misreading.
        readings = [
            (cells, bulbs, wiring)
            for cells in (1, 2, 3) for bulbs in (2, 3) for wiring in (spec.wiring_word, other_wiring)
            if (cells, bulbs, wiring) != (spec.cells, spec.bulbs, spec.wiring_word)
            and ((cells != spec.cells) + (bulbs != spec.bulbs) + (wiring != spec.wiring_word)) <= 2
        ]
        wrongs = tuple(f"เซลล์ไฟฟ้า {c} เซลล์ต่ออนุกรม และหลอดไฟ {b} ดวงต่อกันแบบ{w}"
                       for c, b, w in rng.sample(readings, 3))
        return diagram_question(
            spec.asset_id, layout_alt(spec),
            stem="จากแผนภาพ วงจรนี้ประกอบด้วยอะไรบ้าง และหลอดไฟต่อกันแบบใด",
            correct=_layout_words(spec),
            wrongs=wrongs,
            hint=("นับคู่เส้นยาว-เส้นสั้นเพื่อหาจำนวนเซลล์ไฟฟ้า แล้วดูว่าหลอดไฟเรียงอยู่บน"
                  "สายเส้นเดียวกัน (อนุกรม) หรือแยกคนละเส้นทาง (ขนาน)"),
            topic=SYMBOL_TOPIC,
        )


@question_type(
    "phys.circuit_symbol_application",
    display_name={"th": "ตรวจแผนภาพวงจรไฟฟ้าแล้วบอกวิธีทำให้หลอดไฟสว่าง"},
    level=SIXTH, subject=SUBJECT, topic=SYMBOL_TOPIC,
)
class CircuitSymbolApplication(QuestionType):
    """A schematic that may have a break, an open switch, or nothing wrong.

    All three answers appear as choices every time, so "something must be broken"
    is never a safe guess — one circuit in the pool is simply working.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(FAULT_CIRCUITS)
        if spec.gap:
            correct = FIX_GAP
        elif spec.switch == "open":
            correct = FIX_SWITCH
        else:
            correct = FIX_NONE
        wrongs = tuple(f for f in (FIX_GAP, FIX_SWITCH, FIX_NONE) if f != correct)
        return diagram_question(
            spec.asset_id, layout_alt(spec),
            stem="จากแผนภาพ ต้องทำอย่างไรหลอดไฟในวงจรนี้จึงจะสว่าง",
            correct=correct,
            wrongs=wrongs + (rng.choice(WRONG_CIRCUIT_FIXES),),
            hint=("ไล่สายไฟจากขั้วหนึ่งของเซลล์ไฟฟ้าไปรอบวงจรจนกลับมาอีกขั้วหนึ่ง "
                  "ถ้าไปได้ตลอดโดยไม่สะดุด วงจรนั้นครบวงจร"),
            topic=SYMBOL_TOPIC,
        )

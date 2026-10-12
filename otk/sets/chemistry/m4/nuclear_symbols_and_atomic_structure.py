"""สัญลักษณ์นิวเคลียร์และโครงสร้างอะตอม

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/2

Sets moved here from: chemistry, science_wave_a5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import Block, math, text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import (
    MAX_GROUP,
    MAX_Z,
    SUBJECT,
    TOPIC,
    TOPIC_ATOM,
    TRANSITION,
    ElementType,
    Item,
    element_pool,
    full_name,
    nuclide_tex,
    symbol_tex,
)
from otk.sets._support.science_wave_a5 import BY_Z, ISOTOPE_POOL, WRITEABLE, _nuclide

PROVENANCE = Provenance("original")


# What a type can ask about one item. Single-ask types use ONE_ASK.
MASS_NUMBER, ATOMIC_NUMBER = "mass", "z"


@question_type("chem.atomic_number",
               display_name={"th": "เลขอะตอมของธาตุ"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC)
class AtomicNumber(ElementType):
    def stem(self, it: Item) -> list[Block]:
        return [text(f"ธาตุ {full_name(it.el)} มีเลขอะตอมเท่าใด"),
                math(symbol_tex(it.el))]

    def answer(self, it: Item) -> list[Block]:
        return [math(str(it.el.z))]


@question_type("chem.nuclide",
               display_name={"th": "สัญลักษณ์นิวเคลียร์ (เลขมวล/เลขอะตอม)"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC_ATOM)
class NuclideRead(ElementType):
    """ᴬ_Z X → เลขมวล or เลขอะตอม.

    Both numbers are on show, so the exercise is knowing which is which — hence
    the other number is always among the choices.
    """

    ASKS = (MASS_NUMBER, ATOMIC_NUMBER)

    def stem(self, it: Item) -> list[Block]:
        what = "เลขมวล" if it.ask == MASS_NUMBER else "เลขอะตอม"
        return [text(f"จากสัญลักษณ์นิวเคลียร์ต่อไปนี้ {what}ของธาตุคือเท่าใด"),
                math(nuclide_tex(it.el))]

    def answer(self, it: Item) -> list[Block]:
        return [math(str(it.el.mass if it.ask == MASS_NUMBER else it.el.z))]

    def alternates(self, it: Item) -> list[list[Block]]:
        # The two classic misreadings: the number on the other corner, and the
        # difference between them (the neutron count).
        other = it.el.z if it.ask == MASS_NUMBER else it.el.mass
        return [[math(str(other))], [math(str(it.el.mass - it.el.z))]]

    def build(self, rng: Random, group_lo: int = TRANSITION,
              group_hi: int = MAX_GROUP, z_lo: int = 1, z_hi: int = MAX_Z,
              ask: int = 0) -> GeneratedQuestion:
        pool = element_pool(group_lo, group_hi, z_lo, z_hi)
        asked = self.ask_for(rng, ask)          # 1 = เลขมวล, 2 = เลขอะตอม
        return self.question(lambda: Item(rng.choice(pool), asked))


@question_type(
    "chem.nuclide_write_application",
    display_name={"th": "เขียนสัญลักษณ์นิวเคลียร์และระบุไอโซโทป"},
    level={"th": "ม.4"}, subject=SUBJECT, topic=TOPIC_ATOM,
)
class NuclideWriteApplication(QuestionType):
    """Build the nuclear symbol from particle counts, or pick a true isotope.

    Both halves are the ม.4/2 indicator read forwards rather than backwards: the
    older sets hand the learner a symbol and ask what it says, while these ask
    for the symbol itself.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return self._write(rng)
        return self._isotope(rng)

    def _write(self, rng: Random) -> GeneratedQuestion:
        el = rng.choice(WRITEABLE)
        neutrons = el.mass - el.z
        return GeneratedQuestion(
            stem=[text(f"อะตอมของธาตุ {full_name(el)} มีโปรตอน {el.z} อนุภาค "
                       f"และนิวตรอน {neutrons} อนุภาค "
                       "สัญลักษณ์นิวเคลียร์ของอะตอมนี้คือข้อใด")],
            correct=_nuclide(el.mass, el.z, el.symbol),
            distractors=fixed(
                # เลขมวลกับเลขอะตอมสลับมุมกัน
                _nuclide(el.z, el.mass, el.symbol),
                # นับเฉพาะนิวตรอนเป็นเลขมวล
                _nuclide(neutrons, el.z, el.symbol),
                # เขียนเลขอะตอมเป็นจำนวนนิวตรอน
                _nuclide(el.mass, neutrons, el.symbol),
            ),
            topic=TOPIC_ATOM,
            hint=[text("เลขมวลคือโปรตอนรวมกับนิวตรอน ส่วนเลขอะตอมคือจำนวนโปรตอนเพียงอย่างเดียว "
                       "และเลขมวลเขียนไว้ที่มุมบนซ้าย")],
        )

    def _isotope(self, rng: Random) -> GeneratedQuestion:
        el = rng.choice(ISOTOPE_POOL)
        return GeneratedQuestion(
            stem=[text("นิวไคลด์ในข้อใดเป็นไอโซโทปกับนิวไคลด์ต่อไปนี้")]
            + _nuclide(el.mass, el.z, el.symbol),
            # ไอโซโทปคือเลขอะตอมเท่ากัน เลขมวลต่างกัน
            correct=_nuclide(el.mass + 2, el.z, el.symbol),
            distractors=fixed(
                # เลขมวลเท่ากันแต่คนละธาตุ (ไอโซบาร์)
                _nuclide(el.mass, el.z + 1, BY_Z[el.z + 1].symbol),
                # ต่างกันทั้งเลขมวลและเลขอะตอม
                _nuclide(el.mass + 2, el.z + 2, BY_Z[el.z + 2].symbol),
                _nuclide(el.mass - 2, el.z - 1, BY_Z[el.z - 1].symbol),
            ),
            topic=TOPIC_ATOM,
            hint=[text("ไอโซโทปของธาตุเดียวกันมีจำนวนโปรตอนเท่าเดิม "
                       "ต่างกันที่จำนวนนิวตรอน เลขอะตอมจึงต้องเท่ากัน")],
        )

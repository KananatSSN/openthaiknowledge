"""ชุดรวมอนุภาคของอะตอมและไอออน (ความเข้ากันได้)

เคมี · ม.1 · เสริมทักษะ
Indicators: —

Sets moved here from: chemistry, science_successors.
"""

from __future__ import annotations

from random import Random

from otk.core.content import Block, math, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import question_type
from otk.sets._support.chemistry import (
    MAX_GROUP,
    MAX_Z,
    SUBJECT,
    TOPIC_ATOM,
    TRANSITION,
    ElementType,
    Item,
    common_charges,
    element_pool,
    nuclide_tex,
)
from otk.sets._support.science_successors import FluencyStage

PROVENANCE = Provenance("original")


PROTON, NEUTRON, ELECTRON = "proton", "neutron", "electron"


PARTICLE_TH = {PROTON: "โปรตอน", NEUTRON: "นิวตรอน", ELECTRON: "อิเล็กตรอน"}


def particle_count(it: Item) -> int:
    """โปรตอน = Z, นิวตรอน = A − Z, อิเล็กตรอน = Z − ประจุ."""
    if it.ask == PROTON:
        return it.el.z
    if it.ask == NEUTRON:
        return it.el.mass - it.el.z
    return it.el.z - it.charge


@question_type("chem.particles",
               display_name={"th": "โปรตอน นิวตรอน อิเล็กตรอน"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC_ATOM)
class ParticleCount(ElementType):
    """ᴬ_Z X (or its ion) → how many protons, neutrons or electrons."""

    ASKS = (PROTON, NEUTRON, ELECTRON)

    def stem(self, it: Item) -> list[Block]:
        what = "ไอออน" if it.charge else "อะตอม"
        return [text(f"{what}ต่อไปนี้มีจำนวน{PARTICLE_TH[it.ask]}เท่าใด"),
                math(nuclide_tex(it.el, it.charge))]

    def answer(self, it: Item) -> list[Block]:
        return [math(str(particle_count(it)))]

    def alternates(self, it: Item) -> list[list[Block]]:
        # The three counts sit one confusion apart, so offer the other two —
        # plus the mass number, which is "counted everything" by mistake.
        others = [particle_count(it._replace(ask=a))
                  for a in self.ASKS if a != it.ask]
        return [[math(str(v))] for v in (*others, it.el.mass)]

    def build(self, rng: Random, group_lo: int = TRANSITION,
              group_hi: int = MAX_GROUP, z_lo: int = 1, z_hi: int = MAX_Z,
              ask: int = 0, ion_chance: int = 60) -> GeneratedQuestion:
        pool = element_pool(group_lo, group_hi, z_lo, z_hi)
        asked = self.ask_for(rng, ask)      # 1 = โปรตอน, 2 = นิวตรอน, 3 = อิเล็กตรอน
        pct = max(0, min(100, int(ion_chance)))

        def draw() -> Item:
            el = rng.choice(pool)
            charges = common_charges(el)     # empty ⇒ always a neutral atom
            ion = rng.choice(charges) if charges and rng.randrange(100) < pct else 0
            return Item(el, asked, ion)

        return self.question(draw)


class _PinnedParticleCount(FluencyStage, ParticleCount):
    """Particle-count base that guarantees the requested charge state."""

    def _item_pool(self, group_lo: int, group_hi: int, z_lo: int, z_hi: int):
        return element_pool(group_lo, group_hi, z_lo, z_hi)

    def build(
        self, rng: Random, group_lo: int = TRANSITION,
        group_hi: int = MAX_GROUP, z_lo: int = 1, z_hi: int = MAX_Z,
        ask: int = 0,
    ) -> GeneratedQuestion:
        pool = self._item_pool(group_lo, group_hi, z_lo, z_hi)
        asked = self.ask_for(rng, ask)
        return self.question(lambda: self._draw_item(rng, pool, asked))

    def _draw_item(self, rng: Random, pool, asked: str) -> Item:
        raise NotImplementedError

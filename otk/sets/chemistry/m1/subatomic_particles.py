"""อนุภาคมูลฐานของอะตอม

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/8

Sets moved here from: science_successors, science_wave_a3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import Item
from otk.sets._support.science_wave_a3 import CHEMISTRY, MATTER, _distinct, _question
from otk.sets.chemistry.m1.particles import _PinnedParticleCount

PROVENANCE = Provenance("original")


PARTICLE_FACTS = (
    ("โปรตอน", "บวก", "นิวเคลียส"),
    ("นิวตรอน", "เป็นกลาง", "นิวเคลียส"),
    ("อิเล็กตรอน", "ลบ", "รอบนิวเคลียส"),
)


@question_type(
    "chem.atom_particles_foundation",
    display_name={"th": "อนุภาคมูลฐานของอะตอม: ระบุประจุและตำแหน่ง"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class AtomParticlesFoundation(QuestionType):
    """Name the charge or the location of one subatomic particle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        particle, charge, place = rng.choice(PARTICLE_FACTS)
        shape = rng.randrange(3)
        if shape == 2:
            wrongs = _distinct(particle, [name for name, _, _ in PARTICLE_FACTS] + [
                "โมเลกุล", "ไอออน", "นิวเคลียส",
            ], want=5)
            assert wrongs is not None
            return _question(
                stem=(f"อนุภาคใดในอะตอมมีประจุ{charge}และอยู่ที่{place}"),
                correct=particle,
                wrongs=wrongs,
                hint="จับคู่ทั้งประจุและตำแหน่งพร้อมกัน อนุภาคสองชนิดอยู่ในนิวเคลียสแต่ประจุต่างกัน",
            )
        if shape == 0:
            wrongs = _distinct(charge, ["บวก", "ลบ", "เป็นกลาง", "บวกและลบสลับกัน",
                                        "เปลี่ยนไปตามสถานะของสาร", "มีประจุเป็นสองเท่าของโปรตอน"], want=5)
            assert wrongs is not None
            return _question(
                stem=f"อนุภาค{particle}มีประจุไฟฟ้าชนิดใด",
                correct=charge,
                wrongs=wrongs,
                hint="โปรตอนมีประจุบวก อิเล็กตรอนมีประจุลบ และนิวตรอนเป็นกลาง",
            )
        wrongs = _distinct(place, [
            "นิวเคลียส", "รอบนิวเคลียส", "นอกอะตอมทั้งหมด", "กระจายอยู่ทั่วอะตอมอย่างสม่ำเสมอ",
            "ที่ผิวนอกสุดของนิวเคลียสเท่านั้น", "ระหว่างอะตอมสองอะตอมที่อยู่ติดกัน",
        ], want=5)
        assert wrongs is not None
        return _question(
            stem=f"ในแบบจำลองอะตอม อนุภาค{particle}อยู่ที่ตำแหน่งใด",
            correct=place,
            wrongs=wrongs,
            hint="โปรตอนและนิวตรอนรวมกันอยู่ที่ใจกลาง ส่วนอิเล็กตรอนเคลื่อนที่อยู่รอบ ๆ",
        )


@question_type(
    "chem.particles_neutral",
    display_name={"th": "โปรตอน นิวตรอน อิเล็กตรอนของอะตอม"},
    level={"th": "ม.1"}, subject="เคมี", topic="โครงสร้างอะตอม",
)
class NeutralParticleCount(_PinnedParticleCount):
    source_key = "chem.particles"

    def _draw_item(self, rng: Random, pool, asked: str) -> Item:
        return Item(rng.choice(pool), asked, 0)


@question_type(
    "chem.atom_particles_application",
    display_name={"th": "อนุภาคมูลฐานของอะตอม: ใช้แบบจำลองอธิบายอะตอมและไอออน"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class AtomParticlesApplication(QuestionType):
    """Reason from particle counts to neutrality, mass, or a claim."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        protons = rng.randrange(3, 21)
        neutrons = protons + rng.randrange(0, 4)
        if which == 0:
            correct = f"{protons} อนุภาค"
            # neutrons may equal protons, which collapses several candidates onto
            # each other; offer enough that three always survive deduplication.
            wrongs = _distinct(correct, [
                f"{neutrons} อนุภาค",
                f"{protons + neutrons} อนุภาค",
                f"{protons * 2} อนุภาค",
                f"{max(protons - 1, 1)} อนุภาค",
                f"{protons + 1} อนุภาค",
                f"{protons + neutrons + 1} อนุภาค",
            ])
            assert wrongs is not None
            return _question(
                stem=(f"อะตอมที่เป็นกลางทางไฟฟ้าชนิดหนึ่งมีโปรตอน {protons} อนุภาค "
                      f"และนิวตรอน {neutrons} อนุภาค จะมีอิเล็กตรอนกี่อนุภาค"),
                correct=correct,
                wrongs=wrongs,
                hint="อะตอมที่เป็นกลางมีประจุบวกและประจุลบเท่ากันพอดี",
            )
        if which == 1:
            correct = f"{protons + neutrons} อนุภาค"
            wrongs = _distinct(correct, [
                f"{protons} อนุภาค",
                f"{neutrons} อนุภาค",
                f"{protons + neutrons + protons} อนุภาค",
                f"{protons * 2} อนุภาค",
                f"{max(protons + neutrons - 1, 1)} อนุภาค",
            ])
            assert wrongs is not None
            return _question(
                stem=(f"อะตอมชนิดหนึ่งมีโปรตอน {protons} อนุภาค นิวตรอน {neutrons} อนุภาค "
                      f"และอิเล็กตรอน {protons} อนุภาค อนุภาคในนิวเคลียสมีทั้งหมดกี่อนุภาค"),
                correct=correct,
                wrongs=wrongs,
                hint="นิวเคลียสประกอบด้วยโปรตอนและนิวตรอน ส่วนอิเล็กตรอนอยู่รอบนิวเคลียส",
            )
        return _question(
            stem=("นักเรียนกล่าวว่า “มวลของอะตอมส่วนใหญ่มาจากอิเล็กตรอน "
                  "เพราะอิเล็กตรอนเคลื่อนที่เร็วมาก” ข้อใดประเมินคำกล่าวนี้ได้ถูกต้อง"),
            correct=("ไม่ถูกต้อง เพราะมวลของอะตอมเกือบทั้งหมดอยู่ที่นิวเคลียส "
                     "ซึ่งประกอบด้วยโปรตอนและนิวตรอน"),
            wrongs=(
                "ถูกต้อง เพราะอนุภาคที่เคลื่อนที่เร็วย่อมมีมวลมากที่สุด",
                "ไม่ถูกต้อง เพราะอิเล็กตรอนไม่มีมวลเลยและไม่เคลื่อนที่",
                "ถูกต้อง เพราะอิเล็กตรอนมีจำนวนมากกว่าโปรตอนเสมอ",
            ),
            hint="เทียบมวลของอนุภาคแต่ละชนิด ไม่ใช่ความเร็วหรือจำนวนของอนุภาค",
        )

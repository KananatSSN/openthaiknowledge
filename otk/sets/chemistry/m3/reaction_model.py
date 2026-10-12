"""การเกิดปฏิกิริยาเคมี

เคมี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.3/3

Sets moved here from: science_wave_d11.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d10 import SECONDARY_THREE

PROVENANCE = Provenance("original")


REACTION_TOPIC = "การเกิดปฏิกิริยาเคมี"


class Species(NamedTuple):
    name: str
    formula: str
    atoms: tuple[tuple[str, int], ...]


H2 = Species("ไฮโดรเจน", "H₂", (("H", 2),))


O2 = Species("ออกซิเจน", "O₂", (("O", 2),))


N2 = Species("ไนโตรเจน", "N₂", (("N", 2),))


CL2 = Species("คลอรีน", "Cl₂", (("Cl", 2),))


C = Species("คาร์บอน", "C", (("C", 1),))


H2O = Species("น้ำ", "H₂O", (("H", 2), ("O", 1)))


CO2 = Species("คาร์บอนไดออกไซด์", "CO₂", (("C", 1), ("O", 2)))


CH4 = Species("มีเทน", "CH₄", (("C", 1), ("H", 4)))


HCL = Species("ไฮโดรเจนคลอไรด์", "HCl", (("H", 1), ("Cl", 1)))


NH3 = Species("แอมโมเนีย", "NH₃", (("N", 1), ("H", 3)))


S = Species("กำมะถัน", "S", (("S", 1),))


SO2 = Species("ซัลเฟอร์ไดออกไซด์", "SO₂", (("S", 1), ("O", 2)))


CO = Species("คาร์บอนมอนอกไซด์", "CO", (("C", 1), ("O", 1)))


H2O2 = Species("ไฮโดรเจนเปอร์ออกไซด์", "H₂O₂", (("H", 2), ("O", 2)))


C3H8 = Species("โพรเพน", "C₃H₈", (("C", 3), ("H", 8)))


class Reaction(NamedTuple):
    reactants: tuple[tuple[int, Species], ...]
    products: tuple[tuple[int, Species], ...]


REACTIONS = (
    Reaction(((2, H2), (1, O2)), ((2, H2O),)),
    Reaction(((1, C), (1, O2)), ((1, CO2),)),
    Reaction(((1, CH4), (2, O2)), ((1, CO2), (2, H2O))),
    Reaction(((1, H2), (1, CL2)), ((2, HCL),)),
    Reaction(((1, N2), (3, H2)), ((2, NH3),)),
    Reaction(((1, S), (1, O2)), ((1, SO2),)),
    Reaction(((2, CO), (1, O2)), ((2, CO2),)),
    Reaction(((2, H2O2),), ((2, H2O), (1, O2))),
    Reaction(((1, C3H8), (5, O2)), ((3, CO2), (4, H2O))),
)


def count_atoms(side: tuple[tuple[int, Species], ...]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for n, species in side:
        for atom, k in species.atoms:
            totals[atom] = totals.get(atom, 0) + n * k
    return totals


def word_equation(reaction: Reaction, reverse: bool = False) -> str:
    left = " + ".join(s.name for _, s in reaction.reactants)
    right = " + ".join(s.name for _, s in reaction.products)
    return f"{right} → {left}" if reverse else f"{left} → {right}"


def model(side: tuple[tuple[int, Species], ...]) -> str:
    return " และ ".join(f"{s.name} ({s.formula}) {n} {'อนุภาค' if s in (C, S) else 'โมเลกุล'}" for n, s in side)


ARRANGEMENT_SLIPS = (
    "อะตอมของสารตั้งต้นเปลี่ยนเป็นอะตอมชนิดใหม่ จึงเกิดเป็นผลิตภัณฑ์",
    "อะตอมบางส่วนถูกทำลายระหว่างเกิดปฏิกิริยา ผลิตภัณฑ์จึงมีอะตอมน้อยกว่าเดิม",
    "โมเลกุลของสารตั้งต้นเพียงผสมปนกันอยู่ โดยไม่มีพันธะใดสลายหรือเกิดขึ้นใหม่",
)


def reaction_parts(reaction: Reaction, rng: Random | None = None) -> tuple[Part, ...]:
    """With ``rng``, the atom-count and arrangement slips are drawn from their alternatives."""
    totals = count_atoms(reaction.reactants)
    counts = " ".join(f"{atom} {n} อะตอม" for atom, n in totals.items())
    first_atom = max(totals, key=totals.get)
    shrunk = " ".join(f"{atom} {n - 1 if atom == first_atom else n} อะตอม" for atom, n in totals.items())
    miscount = f"ก่อนเกิดปฏิกิริยามี {counts} แต่หลังเกิดปฏิกิริยาเหลือ {shrunk}"
    arrangement = ARRANGEMENT_SLIPS[0]
    if rng is not None:
        grown = " ".join(f"{atom} {n + 1 if atom == first_atom else n} อะตอม" for atom, n in totals.items())
        miscount = rng.choice((miscount, f"ก่อนเกิดปฏิกิริยามี {counts} แต่หลังเกิดปฏิกิริยาเพิ่มเป็น {grown}"))
        arrangement = rng.choice(ARRANGEMENT_SLIPS)
    return (
        Part("สมการข้อความ", word_equation(reaction), word_equation(reaction, reverse=True)),
        Part("จำนวนอะตอม", f"ทั้งก่อนและหลังเกิดปฏิกิริยามี {counts} เท่ากัน", miscount),
        Part("การจัดเรียงอะตอม", "พันธะในสารตั้งต้นสลาย แล้วอะตอมเดิมจัดเรียงตัวใหม่เกิดเป็นโมเลกุลของผลิตภัณฑ์",
             arrangement),
    )


REACTION_SCENARIOS = (
    ("เมื่อเผาถ่าน (คาร์บอน) ในอากาศ ถ่านหายไปเหลือเพียงเถ้าเล็กน้อย นักเรียนคนหนึ่งสรุปว่าอะตอมคาร์บอนถูกทำลายไป ข้อใดโต้แย้งได้ถูกต้อง",
     "อะตอมคาร์บอนไม่ได้หายไป แต่รวมกับออกซิเจนเป็นแก๊สคาร์บอนไดออกไซด์ที่ลอยออกไปในอากาศ",
     ("อะตอมคาร์บอนเปลี่ยนเป็นอะตอมออกซิเจน",
      "อะตอมคาร์บอนถูกทำลายจริงเพราะมองไม่เห็นแล้ว",
      "อะตอมคาร์บอนกลายเป็นความร้อนทั้งหมด",
      "อะตอมคาร์บอนละลายหายไปในเถ้า",
      "อะตอมคาร์บอนแตกตัวเป็นอะตอมไฮโดรเจน")),
    ("ถ้ามีโมเลกุลไฮโดรเจน 4 โมเลกุลทำปฏิกิริยาพอดีกับออกซิเจนเกิดเป็นน้ำ จะได้น้ำกี่โมเลกุล",
     "4 โมเลกุล", ("2 โมเลกุล", "6 โมเลกุล", "8 โมเลกุล", "1 โมเลกุล", "12 โมเลกุล")),
    ("สมการข้อความ \"มีเทน + ออกซิเจน → คาร์บอนไดออกไซด์ + น้ำ\" อธิบายสิ่งใดในชีวิตประจำวัน",
     "การเผาไหม้แก๊สหุงต้มที่มีมีเทนเป็นส่วนประกอบ ซึ่งให้แก๊สคาร์บอนไดออกไซด์และไอน้ำ",
     ("การละลายน้ำตาลในน้ำ",
      "การกลั่นน้ำทะเลเป็นน้ำจืด",
      "การหลอมเหลวของน้ำแข็ง",
      "การเกิดสนิมของเหล็ก",
      "การสังเคราะห์ด้วยแสงของพืช")),
)


def molecule_count(rng: Random) -> GeneratedQuestion:
    """Scale a reaction's molecule numbers; how many of one product form."""
    reaction = rng.choice([r for r in REACTIONS
                           if len(r.reactants) == 2 and all(s not in (C, S) for _, s in r.reactants)])
    k = rng.randint(2, 6)
    (n0, first), (n1, second) = reaction.reactants
    target_n, target = rng.choice(reaction.products)
    answer = k * target_n
    pool = (k * n0, k * n1, k * (n0 + n1), 2 * answer, answer + k, answer + 1, 3 * answer)
    wrongs = tuple(dict.fromkeys(f"{w} โมเลกุล" for w in pool if w != answer))
    products = "และ".join(s.name for _, s in reaction.products)
    return _labelled(
        stem=(f"ถ้ามีโมเลกุล{first.name} {k * n0} โมเลกุล ทำปฏิกิริยาพอดีกับ{second.name} เกิดเป็น{products} "
              f"จะได้{target.name}กี่โมเลกุล"),
        correct=f"{answer} โมเลกุล",
        wrongs=wrongs,
        hint="เขียนแบบจำลองให้จำนวนอะตอมแต่ละชนิดเท่ากันทั้งสองข้าง แล้วขยายด้วยอัตราส่วนเดียวกัน",
        topic=REACTION_TOPIC,
    )


@question_type(
    "chem.reaction_model_foundation",
    display_name={"th": "ระบุสารตั้งต้นและผลิตภัณฑ์จากสมการข้อความ"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=REACTION_TOPIC,
)
class ReactionModelFoundation(QuestionType):
    """A word equation; which substances are reactants and which products."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction = rng.choice(REACTIONS)
        left = " และ ".join(s.name for _, s in reaction.reactants)
        right = " และ ".join(s.name for _, s in reaction.products)
        return _labelled(
            stem=f"จากสมการข้อความ \"{word_equation(reaction)}\" ข้อใดถูกต้อง",
            correct=f"สารตั้งต้นคือ {left} ผลิตภัณฑ์คือ {right}",
            wrongs=(f"สารตั้งต้นคือ {right} ผลิตภัณฑ์คือ {left}",
                    f"สารตั้งต้นคือ {left} และ {right} ไม่มีผลิตภัณฑ์",
                    f"ผลิตภัณฑ์คือ {left} และ {right} ไม่มีสารตั้งต้น",
                    f"สารตั้งต้นคือ {left} ผลิตภัณฑ์คือ {left}",
                    f"สารตั้งต้นคือ {right} ผลิตภัณฑ์คือ {right}"),
            hint="สารทางซ้ายของลูกศรคือสารตั้งต้น สารทางขวาคือผลิตภัณฑ์",
            topic=REACTION_TOPIC,
        )


@question_type(
    "chem.reaction_model_fluency",
    display_name={"th": "อธิบายการเกิดปฏิกิริยาเคมีและการจัดเรียงตัวใหม่ของอะตอมจากแบบจำลอง"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=REACTION_TOPIC,
)
class ReactionModelFluency(QuestionType):
    """A particle model before and after; the equation, the atom count and the rearrangement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction = rng.choice(REACTIONS)
        return parts_item(
            rng, reaction_parts(reaction, rng),
            stem=(f"แบบจำลองอนุภาคแสดงว่า ก่อนเกิดปฏิกิริยามี {model(reaction.reactants)} "
                  f"หลังเกิดปฏิกิริยามี {model(reaction.products)} "
                  "จากแบบจำลองนี้ ข้อใดอธิบายการเกิดปฏิกิริยาเคมีได้ถูกต้องทั้งหมด"),
            hint="นับอะตอมแต่ละชนิดทั้งสองข้าง แล้วดูว่าสารใดหายไปและสารใดเกิดขึ้นใหม่",
            topic=REACTION_TOPIC,
        )


@question_type(
    "chem.reaction_model_application",
    display_name={"th": "ใช้แบบจำลองอะตอมอธิบายปฏิกิริยาในชีวิตประจำวัน"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=REACTION_TOPIC,
)
class ReactionModelApplication(QuestionType):
    """Burning charcoal, counting water molecules, and cooking gas."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return molecule_count(rng)
        return _retopic(scenario_question(
            rng, REACTION_SCENARIOS,
            hint="อะตอมไม่หายไปและไม่เกิดใหม่ในปฏิกิริยาเคมี เพียงจัดเรียงตัวใหม่",
        ), REACTION_TOPIC)

"""สัญลักษณ์นิวเคลียร์และไอโซโทป

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/4

Sets moved here from: science_wave_e1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_a5 import BY_Z, ISOTOPE_POOL, WRITEABLE, _nuclide
from otk.sets._support.science_wave_e1 import SUBJECT

PROVENANCE = Provenance("original")


TOPIC_NUCLIDE = "สัญลักษณ์นิวเคลียร์และไอโซโทป"


@question_type(
    "chem.nuclide_isotope_foundation",
    display_name={"th": "เขียนสัญลักษณ์นิวเคลียร์จากจำนวนโปรตอนและนิวตรอน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_NUCLIDE,
)
class NuclideIsotopeFoundation(QuestionType):
    """เขียนสัญลักษณ์นิวเคลียร์ — the first of ม.5/4's two free verbs."""
    break_convergence = True  # one-part slips cluster round the answer

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(WRITEABLE)
        neutrons = el.mass - el.z
        return GeneratedQuestion(
            stem=[text(f"อะตอมของธาตุ {el.th} ({el.en}) มีโปรตอน {el.z} อนุภาค "
                       f"และนิวตรอน {neutrons} อนุภาค สัญลักษณ์นิวเคลียร์ของอะตอมนี้คือข้อใด")],
            correct=_nuclide(el.mass, el.z, el.symbol),
            distractors=fixed(
                _nuclide(el.z, el.mass, el.symbol),
                _nuclide(neutrons, el.z, el.symbol),
                _nuclide(el.mass, neutrons, el.symbol),
                # Both numbers wrong at once.
                *((_nuclide(neutrons, el.mass, el.symbol), _nuclide(el.z, neutrons, el.symbol))
                  if neutrons != el.z else ()),
            ),
            topic=TOPIC_NUCLIDE,
            hint=[text("เลขมวลคือโปรตอนรวมกับนิวตรอน เขียนไว้ที่มุมบนซ้าย "
                       "ส่วนเลขอะตอมคือจำนวนโปรตอนเพียงอย่างเดียว เขียนไว้ที่มุมล่างซ้าย")],
        )


@question_type(
    "chem.nuclide_isotope_fluency",
    display_name={"th": "ระบุนิวไคลด์ที่เป็นไอโซโทปกัน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_NUCLIDE,
)
class NuclideIsotopeFluency(QuestionType):
    """ระบุการเป็นไอโซโทป — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(ISOTOPE_POOL)
        return GeneratedQuestion(
            stem=[text("นิวไคลด์ในข้อใดเป็นไอโซโทปกับนิวไคลด์ต่อไปนี้")] + _nuclide(el.mass, el.z, el.symbol),
            correct=_nuclide(el.mass + 2, el.z, el.symbol),
            distractors=fixed(
                _nuclide(el.mass, el.z + 1, BY_Z[el.z + 1].symbol),
                _nuclide(el.mass + 2, el.z + 2, BY_Z[el.z + 2].symbol),
                _nuclide(el.mass - 2, el.z - 1, BY_Z[el.z - 1].symbol),
            ),
            topic=TOPIC_NUCLIDE,
            hint=[text("ไอโซโทปของธาตุเดียวกันมีจำนวนโปรตอนเท่าเดิม ต่างกันที่จำนวนนิวตรอน "
                       "เลขอะตอมจึงต้องเท่ากันเสมอ")],
        )


@question_type(
    "chem.nuclide_isotope_application",
    display_name={"th": "เขียนสัญลักษณ์นิวเคลียร์ของไอโซโทปที่มีนิวตรอนต่างกันตามที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_NUCLIDE,
)
class NuclideIsotopeApplication(QuestionType):
    """Combine both verbs: write the symbol of a specified isotope."""
    break_convergence = True  # one-part slips cluster round the answer

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(WRITEABLE)
        offset = rng.choice((2, 4, 6))
        target_mass = el.mass + offset
        return GeneratedQuestion(
            stem=[text(f"ไอโซโทปของธาตุ {el.th} ({el.en}) ที่มีนิวตรอนมากกว่าอะตอมนี้อยู่ {offset} อนุภาค "
                       "มีสัญลักษณ์นิวเคลียร์เป็นข้อใด")],
            correct=_nuclide(target_mass, el.z, el.symbol),
            distractors=fixed(
                _nuclide(el.mass, el.z, el.symbol),
                _nuclide(el.mass + offset // 2, el.z, el.symbol),
                _nuclide(target_mass, el.z + 1, BY_Z[el.z + 1].symbol),
                # Another element as well as the wrong mass: two slips.
                _nuclide(el.mass, el.z + 1, BY_Z[el.z + 1].symbol),
                _nuclide(el.mass + offset // 2, el.z + 1, BY_Z[el.z + 1].symbol),
            ),
            topic=TOPIC_NUCLIDE,
            hint=[text("บวกจำนวนนิวตรอนที่เพิ่มเข้าไปในเลขมวลเดิม แต่เลขอะตอมของไอโซโทปต้องเท่าเดิม")],
        )

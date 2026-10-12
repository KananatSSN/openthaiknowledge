"""ทฤษฎีการชนและพลังงานก่อกัมมันต์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/3

Sets moved here from: science_wave_f32.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f32 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_COLLISION = "ทฤษฎีการชนและพลังงานก่อกัมมันต์"


COLLISION_FACTS = (
    ("การชนที่ทำให้เกิดปฏิกิริยาต้องมีลักษณะอย่างไร", "อนุภาคชนกันในทิศทางที่เหมาะสมและมีพลังงานอย่างน้อยเท่ากับพลังงานก่อกัมมันต์",
     ("อนุภาคชนกันบ่อยเท่านั้นก็เพียงพอ", "อนุภาคชนกันในทิศทางใดก็ได้ถ้าอุณหภูมิสูง",
      "อนุภาคต้องมีพลังงานน้อยกว่าพลังงานก่อกัมมันต์")),
    ("พลังงานก่อกัมมันต์ (Ea) คืออะไร", "พลังงานต่ำสุดที่อนุภาคต้องมีเมื่อชนกันจึงจะเกิดปฏิกิริยา",
     ("พลังงานที่ปฏิกิริยาคายออกมาทั้งหมดเมื่อเกิดผลิตภัณฑ์", "พลังงานของผลิตภัณฑ์ที่เกิดขึ้นหลังปฏิกิริยา", "ผลต่างพลังงานของผลิตภัณฑ์กับสารตั้งต้นในปฏิกิริยา")),
    ("ตัวเร่งปฏิกิริยาทำให้ปฏิกิริยาเร็วขึ้นได้อย่างไร", "ทำให้เกิดปฏิกิริยาในกลไกที่มีพลังงานก่อกัมมันต์ต่ำลง",
     ("เพิ่มพลังงานของผลิตภัณฑ์", "เพิ่มพลังงานจลน์ของอนุภาคทุกตัว", "เปลี่ยนค่า ΔH ของปฏิกิริยา")),
    ("สารเชิงซ้อนกัมมันต์คืออะไร", "สารที่เกิดชั่วขณะที่ยอดของกราฟพลังงาน มีพลังงานสูงและไม่เสถียร",
     ("ผลิตภัณฑ์สุดท้ายที่เสถียรที่สุดซึ่งอยู่ปลายกราฟพลังงาน", "ตัวเร่งปฏิกิริยาที่ใส่ลงไปเพื่อลดพลังงานก่อกัมมันต์", "สารตั้งต้นที่เหลือจากปฏิกิริยาซึ่งมีพลังงานต่ำ")),
    ("เมื่อเพิ่มอุณหภูมิ อัตราการเกิดปฏิกิริยาเพิ่มขึ้นเพราะเหตุใด",
     "อนุภาคที่มีพลังงานถึงพลังงานก่อกัมมันต์มีสัดส่วนมากขึ้น และชนกันบ่อยขึ้น",
     ("พลังงานก่อกัมมันต์ลดลง", "ปฏิกิริยาเปลี่ยนจากดูดเป็นคายพลังงาน", "จำนวนโมลของสารตั้งต้นเพิ่มขึ้น")),
)


def energy_case(rng: Random):
    reactants = rng.randrange(20, 301, 10)
    products = rng.randrange(0, 401, 10)
    if products == reactants:
        products += 30
    peak = max(reactants, products) + rng.randrange(20, 201, 10)
    return reactants, products, peak


@question_type(
    "chem.collision_theory_foundation",
    display_name={"th": "ทฤษฎีการชนและพลังงานก่อกัมมันต์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class CollisionTheoryFoundation(QuestionType):
    """Enough energy and the right orientation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ปฏิกิริยาเกิดเมื่ออนุภาคชนกันด้วยทิศทางเหมาะสมและพลังงานไม่น้อยกว่า Ea"
        if rng.random() < 0.3:
            stem, right, wrongs = rng.choice(COLLISION_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_COLLISION, hint=hint)
        ea = rng.randrange(40, 201, 5)
        energy = ea + rng.choice((-1, 1)) * rng.randrange(5, 61, 5)
        aligned = rng.random() < 0.5
        outcomes = {
            (True, True): "เกิดปฏิกิริยา เพราะพลังงานถึง Ea และทิศทางการชนเหมาะสม",
            (False, True): "ไม่เกิดปฏิกิริยา เพราะแม้ทิศทางเหมาะสม แต่พลังงานไม่ถึง Ea",
            (True, False): "ไม่เกิดปฏิกิริยา เพราะแม้พลังงานถึง Ea แต่ทิศทางไม่เหมาะสม",
            (False, False): "ไม่เกิดปฏิกิริยา เพราะพลังงานไม่ถึง Ea และทิศทางไม่เหมาะสม",
        }
        right = outcomes[(energy >= ea, aligned)]
        return _labelled(stem=f"ปฏิกิริยาหนึ่งมีพลังงานก่อกัมมันต์ {ea} kJ/mol อนุภาคคู่หนึ่งชนกันด้วยพลังงาน {energy} kJ/mol "
                              f"ในทิศทางที่{'เหมาะสม' if aligned else 'ไม่เหมาะสม'} การชนครั้งนี้เป็นอย่างไร",
                         correct=right, wrongs=tuple(v for v in outcomes.values() if v != right), topic=TOPIC_COLLISION,
                         hint=hint)


@question_type(
    "chem.collision_theory_fluency",
    display_name={"th": "พลังงานก่อกัมมันต์และพลังงานของปฏิกิริยาจากแผนภาพพลังงาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class CollisionTheoryFluency(QuestionType):
    """Ea = peak − reactants; ΔH = products − reactants; reverse Ea = peak − products."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reactants, products, peak = energy_case(rng)
        stem = (f"แผนภาพพลังงานของปฏิกิริยาหนึ่ง: สารตั้งต้นมีพลังงาน {reactants} kJ ยอดของกราฟ (สารเชิงซ้อนกัมมันต์) "
                f"{peak} kJ ผลิตภัณฑ์ {products} kJ")
        kind = rng.randrange(3)
        hint = "Ea = พลังงานที่ยอด − พลังงานสารตั้งต้น ΔH = พลังงานผลิตภัณฑ์ − พลังงานสารตั้งต้น"
        if kind == 0:
            return numeric(stem=f"{stem} พลังงานก่อกัมมันต์ของปฏิกิริยาไปข้างหน้าเท่าใด", answer=peak - reactants,
                           wrongs=[peak - products, peak, abs(products - reactants)], unit="kJ", topic=TOPIC_COLLISION,
                           hint=hint)
        if kind == 1:
            dh = products - reactants
            return numeric(stem=f"{stem} พลังงานของปฏิกิริยา (ΔH) เท่าใด", answer=dh,
                           wrongs=[-dh, peak - reactants, peak - products], unit="kJ", topic=TOPIC_COLLISION,
                           allow_negative=True, hint=hint + " (ค่าลบคือคายพลังงาน)")
        return numeric(stem=f"{stem} พลังงานก่อกัมมันต์ของปฏิกิริยาย้อนกลับเท่าใด", answer=peak - products,
                       wrongs=[peak - reactants, peak, abs(products - reactants)], unit="kJ", topic=TOPIC_COLLISION,
                       hint="ปฏิกิริยาย้อนกลับเริ่มจากผลิตภัณฑ์: Ea ย้อนกลับ = พลังงานที่ยอด − พลังงานผลิตภัณฑ์")


@question_type(
    "chem.collision_theory_application",
    display_name={"th": "ผลของตัวเร่งปฏิกิริยาต่อแผนภาพพลังงาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLLISION,
)
class CollisionTheoryApplication(QuestionType):
    """A catalyst lowers the peak; ΔH and both end levels stay put."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reactants, products, peak = energy_case(rng)
        lowered = peak - rng.randrange(10, peak - max(reactants, products), 10) if peak - max(reactants, products) > 10 else peak - 5
        stem = (f"ปฏิกิริยาหนึ่งมีพลังงานสารตั้งต้น {reactants} kJ ผลิตภัณฑ์ {products} kJ และยอดของกราฟ {peak} kJ "
                f"เมื่อเติมตัวเร่งปฏิกิริยา ยอดของกราฟลดลงเหลือ {lowered} kJ")
        kind = rng.randrange(3)
        if kind == 0:
            return numeric(stem=f"{stem} พลังงานก่อกัมมันต์ใหม่เท่าใด", answer=lowered - reactants,
                           wrongs=[peak - reactants, peak - lowered, lowered - products if lowered != products else lowered],
                           unit="kJ", topic=TOPIC_COLLISION, hint="Ea ใหม่ = ยอดใหม่ − พลังงานสารตั้งต้น")
        if kind == 1:
            return numeric(stem=f"{stem} พลังงานก่อกัมมันต์ลดลงกี่ kJ", answer=peak - lowered,
                           wrongs=[lowered - reactants, peak - reactants, abs(products - reactants) or 5], unit="kJ",
                           topic=TOPIC_COLLISION, hint="Ea ที่ลดลง = ยอดเดิม − ยอดใหม่ (สารตั้งต้นอยู่ที่ระดับเดิม)")
        dh = products - reactants
        return _labelled(stem=f"{stem} ค่า ΔH ของปฏิกิริยาเป็นอย่างไร", correct=f"เท่าเดิม คือ {dh:+d} kJ",
                         wrongs=(f"ลดลง {peak - lowered} kJ", f"เพิ่มขึ้น {peak - lowered} kJ", f"กลายเป็น {-dh:+d} kJ"),
                         topic=TOPIC_COLLISION,
                         hint="ตัวเร่งปฏิกิริยาเปลี่ยนเฉพาะเส้นทาง (ยอดของกราฟ) ไม่เปลี่ยนพลังงานของสารตั้งต้นหรือผลิตภัณฑ์")

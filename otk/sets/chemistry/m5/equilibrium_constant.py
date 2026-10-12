"""ค่าคงที่สมดุล

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/9

Sets moved here from: science_wave_f34.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f34 import (
    K_SYSTEMS,
    SUBJECT,
    UPPER_FIVE,
    conc_text,
    counted,
    k_case,
    k_value,
)

PROVENANCE = Provenance("original")


TOPIC_K = "ค่าคงที่สมดุล"


SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _term(formula: str, power: int) -> str:
    return f"[{formula}]" + (str(power).translate(SUP) if power > 1 else "")


def _side(species) -> str:
    return "".join(_term(f, c) for f, c, _ in species) or "1"


def k_expression(system, include_all: bool = False, powers: bool = True) -> str:
    _, reactants, products = system
    pick = (lambda side: list(side)) if include_all else counted
    fix = (lambda side: side) if powers else (lambda side: [(f, 1, st) for f, _, st in side])
    top, bottom = _side(fix(pick(products))), _side(fix(pick(reactants)))
    return top if bottom == "1" else f"{top} / {bottom}"


@question_type(
    "chem.equilibrium_constant_foundation",
    display_name={"th": "เขียนนิพจน์ค่าคงที่สมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_K,
)
class EquilibriumConstantFoundation(QuestionType):
    """Products over reactants, each to the power of its coefficient; no solids or pure liquids."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system = rng.choice(K_SYSTEMS)
        hint = "K = [ผลิตภัณฑ์] ÷ [สารตั้งต้น] ยกกำลังด้วยสัมประสิทธิ์ ไม่นำของแข็ง (s) และของเหลวบริสุทธิ์ (l) มาเขียน"
        roll = rng.random()
        if roll < 0.3:
            f, c, _ = rng.choice(counted(system[1]) + counted(system[2]))
            place = "ส่วน" if any(f == x[0] for x in counted(system[1])) else "เศษ"
            right = f"อยู่ใน{place} ยกกำลัง {c}"
            options = [f"อยู่ใน{p} ยกกำลัง {n}" for p in ("เศษ", "ส่วน") for n in sorted({c, c + 1, 1, 2})]
            return _labelled(stem=f"ในนิพจน์ค่าคงที่สมดุลของ {system[0]} [{f}] อยู่ตำแหน่งใดและยกกำลังเท่าใด", correct=right,
                             wrongs=tuple([o for o in options if o != right]), topic=TOPIC_K, hint=hint)
        excluded = [x for x in system[1] + system[2] if x[2] in ("s", "l")]
        if roll < 0.5 and excluded:
            f, _, st = rng.choice(excluded)
            kind = "ของแข็ง" if st == "s" else "ของเหลวบริสุทธิ์"
            wrongs = [f"{x[0]} เพราะเป็น{'แก๊ส' if x[2] == 'g' else 'สารละลาย'}" for x in counted(system[1]) + counted(system[2])]
            wrongs += [f"{f} เพราะเป็นตัวเร่งปฏิกิริยา", "ทุกสารปรากฏในนิพจน์"]
            return _labelled(stem=f"สารใดในปฏิกิริยา {system[0]} ไม่ปรากฏในนิพจน์ค่าคงที่สมดุล", correct=f"{f} เพราะเป็น{kind}",
                             wrongs=tuple(wrongs), topic=TOPIC_K, hint=hint)
        right = k_expression(system)
        _, reactants, products = system
        flipped = k_expression((system[0], products, reactants))
        pool = {flipped, k_expression(system, include_all=True), k_expression(system, powers=False),
                k_expression((system[0], products, reactants), powers=False)}
        pool.discard(right)
        pool = sorted(pool)
        while len(pool) < 3:
            pool.append(f"{right} × 2" if f"{right} × 2" not in pool else f"2 × {right}")
        return _labelled(stem=f"ปฏิกิริยา {system[0]} มีนิพจน์ค่าคงที่สมดุล K ตามข้อใด", correct=f"K = {right}",
                         wrongs=tuple(f"K = {w}" for w in rng.sample(pool, 3)), topic=TOPIC_K,
                         hint="K = [ผลิตภัณฑ์] ÷ [สารตั้งต้น] ยกกำลังด้วยสัมประสิทธิ์ ไม่นำของแข็ง (s) และของเหลวบริสุทธิ์ (l) มาเขียน")


@question_type(
    "chem.equilibrium_constant_fluency",
    display_name={"th": "คำนวณค่าคงที่สมดุลจากความเข้มข้นที่ภาวะสมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_K,
)
class EquilibriumConstantFluency(QuestionType):
    """Put the equilibrium concentrations into the expression."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system, conc, k = k_case(rng)
        flat = Fraction(1)
        for f, _, _ in counted(system[2]):
            flat *= conc[f]
        for f, _, _ in counted(system[1]):
            flat /= conc[f]
        return numeric(stem=f"ปฏิกิริยา {system[0]} ที่ภาวะสมดุลมี {conc_text(conc)} mol/dm³ ค่าคงที่สมดุลเท่าใด",
                       answer=k, wrongs=[1 / k if exact(1 / k) else k * 2, flat if exact(flat) and flat != k else k + 1, k * 2],
                       unit="", topic=TOPIC_K, hint="แทนความเข้มข้นที่ภาวะสมดุลในนิพจน์ K อย่าลืมยกกำลังตามสัมประสิทธิ์")


@question_type(
    "chem.equilibrium_constant_application",
    display_name={"th": "ค่าคงที่สมดุลจากจำนวนโมลและปริมาตรภาชนะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_K,
)
class EquilibriumConstantApplication(QuestionType):
    """Moles ÷ volume first, then K; and what the size of K says."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            big = rng.random() < 0.5
            value = rng.choice(("1.0 × 10⁵", "2.5 × 10⁸", "6.0 × 10¹²")) if big else rng.choice(("1.0 × 10⁻⁵", "4.0 × 10⁻⁸", "2.0 × 10⁻¹²"))
            right = "ที่ภาวะสมดุลมีผลิตภัณฑ์มากกว่าสารตั้งต้นมาก" if big else "ที่ภาวะสมดุลมีสารตั้งต้นมากกว่าผลิตภัณฑ์มาก"
            other = "ที่ภาวะสมดุลมีสารตั้งต้นมากกว่าผลิตภัณฑ์มาก" if big else "ที่ภาวะสมดุลมีผลิตภัณฑ์มากกว่าสารตั้งต้นมาก"
            system = rng.choice(K_SYSTEMS)
            return _labelled(stem=f"ปฏิกิริยา {system[0]} มีค่า K = {value} ที่อุณหภูมิหนึ่ง ข้อใดสรุปได้ถูกต้อง", correct=right,
                             wrongs=(other, "ปฏิกิริยาเกิดเร็วมาก", "ความเข้มข้นของทุกสารเท่ากัน"), topic=TOPIC_K,
                             hint="K มากกว่า 1 มาก สมดุลอยู่ทางผลิตภัณฑ์ K น้อยกว่า 1 มาก สมดุลอยู่ทางสารตั้งต้น K ไม่บอกความเร็ว")

        def draw():
            system, conc, k = k_case(rng)
            volume = rng.choice((1, 2, 4, 5, 10))
            moles = {f: v * volume for f, v in conc.items()}
            return (system, conc, k, volume, moles) if all(exact(m) for m in moles.values()) else None

        system, conc, k, volume, moles = _find(rng, draw)
        mole_text = ", ".join(f"{f} {show(m)} mol" for f, m in moles.items())
        wrong_k = k_value(system, moles)
        return numeric(stem=f"ปฏิกิริยา {system[0]} ในภาชนะปริมาตร {volume} dm³ ที่ภาวะสมดุลมี {mole_text} ค่าคงที่สมดุลเท่าใด",
                       answer=k, wrongs=[wrong_k if exact(wrong_k) and wrong_k != k else k * 2, k * volume if volume > 1 else k + 1,
                                         1 / k if exact(1 / k) and 1 / k != k else k * 3],
                       unit="", topic=TOPIC_K, hint="เปลี่ยนจำนวนโมลเป็นความเข้มข้นก่อน (โมล ÷ ปริมาตร dm³) แล้วแทนในนิพจน์ K")

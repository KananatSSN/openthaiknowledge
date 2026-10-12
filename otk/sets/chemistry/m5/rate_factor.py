"""ผลของความเข้มข้น พื้นที่ผิว อุณหภูมิ และตัวเร่งปฏิกิริยาต่ออัตราการเกิดปฏิกิริยาเคมี

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/21

Sets moved here from: science_wave_e8.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple, Optional

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e8 import (
    CATALYST,
    CONCENTRATION,
    FACTORS,
    FASTER,
    SLOWER,
    SUBJECT,
    SURFACE,
    TEMPERATURE,
    UPPER_FIVE,
    _labelled,
)

PROVENANCE = Provenance("original")


TOPIC_RATE_FACTOR = "ผลของความเข้มข้น พื้นที่ผิว อุณหภูมิ และตัวเร่งปฏิกิริยาต่ออัตราการเกิดปฏิกิริยาเคมี"


RATE_ANSWERS = (FASTER, SLOWER, "เกิดเร็วเท่าเดิม", "หยุดเกิดปฏิกิริยาทันที")


# Collision theory, by factor and direction (True = the change speeds it up).
EXPLAIN = {
    (CONCENTRATION, True): "อนุภาคของสารตั้งต้นมีจำนวนต่อหน่วยปริมาตรมากขึ้น จึงชนกันบ่อยขึ้น",
    (CONCENTRATION, False): "อนุภาคของสารตั้งต้นมีจำนวนต่อหน่วยปริมาตรน้อยลง จึงชนกันน้อยลง",
    (SURFACE, True): "ของแข็งมีพื้นที่ผิวสัมผัสกับสารอื่นมากขึ้น อนุภาคจึงชนกันได้มากขึ้น",
    (SURFACE, False): "ของแข็งมีพื้นที่ผิวสัมผัสกับสารอื่นน้อยลง อนุภาคจึงชนกันได้น้อยลง",
    (TEMPERATURE, True): ("อนุภาคมีพลังงานจลน์สูงขึ้น ชนกันบ่อยขึ้น "
                          "และมีอนุภาคที่มีพลังงานถึงพลังงานก่อกัมมันต์มากขึ้น"),
    (TEMPERATURE, False): ("อนุภาคมีพลังงานจลน์ต่ำลง ชนกันน้อยลง "
                           "และมีอนุภาคที่มีพลังงานถึงพลังงานก่อกัมมันต์น้อยลง"),
    (CATALYST, True): "ตัวเร่งปฏิกิริยาทำให้ปฏิกิริยาเกิดผ่านทางที่มีพลังงานก่อกัมมันต์ต่ำลง",
}


MISCONCEPTION = {
    True: ("สารตั้งต้นถูกใช้หมดไปเร็วขึ้นโดยอนุภาคไม่จำเป็นต้องชนกัน",
           "ตัวเร่งปฏิกิริยาถูกใช้หมดไปและกลายเป็นผลิตภัณฑ์เพิ่มขึ้น"),
    False: ("อนุภาคของสารตั้งต้นหยุดเคลื่อนที่ทั้งหมด",
            "ผลิตภัณฑ์ที่เกิดขึ้นย้อนกลับไปเป็นสารตั้งต้นทันที"),
}


class RateReaction(NamedTuple):
    name: str                          # "A กับ B"
    solution: str                      # whose concentration changes
    solid: Optional[tuple[str, str]]   # (lump, powder) or None
    catalyst: Optional[str]            # a real catalyst for this reaction, or None
    measure: str                       # what the learner watches


RATE_REACTIONS: tuple[RateReaction, ...] = (
    RateReaction("ลวดแมกนีเซียมกับสารละลายกรดไฮโดรคลอริก", "สารละลายกรดไฮโดรคลอริก",
                 ("ลวดแมกนีเซียมขดใหญ่", "ผงแมกนีเซียม"), None, "แก๊สไฮโดรเจน"),
    RateReaction("หินปูนกับสารละลายกรดไฮโดรคลอริก", "สารละลายกรดไฮโดรคลอริก",
                 ("หินปูนก้อนใหญ่", "ผงหินปูน"), None, "แก๊สคาร์บอนไดออกไซด์"),
    RateReaction("สังกะสีกับสารละลายกรดซัลฟิวริก", "สารละลายกรดซัลฟิวริก",
                 ("เม็ดสังกะสี", "ผงสังกะสี"), "สารละลายคอปเปอร์(II)ซัลเฟตเล็กน้อย", "แก๊สไฮโดรเจน"),
    RateReaction("การสลายตัวของสารละลายไฮโดรเจนเพอร์ออกไซด์", "สารละลายไฮโดรเจนเพอร์ออกไซด์",
                 None, "ผงแมงกานีส(IV)ออกไซด์", "แก๊สออกซิเจน"),
    RateReaction("สารละลายโซเดียมไทโอซัลเฟตกับสารละลายกรดไฮโดรคลอริก",
                 "สารละลายโซเดียมไทโอซัลเฟต", None, None, "ตะกอนกำมะถัน"),
    RateReaction("ชิ้นเหล็กกับสารละลายกรดไฮโดรคลอริก", "สารละลายกรดไฮโดรคลอริก",
                 ("แผ่นเหล็ก", "ผงเหล็ก"), None, "แก๊สไฮโดรเจน"),
)


def _changes(r: RateReaction) -> list[tuple[str, bool, str]]:
    """Every (factor, speeds_up, how the change is made) this reaction allows."""
    out = [
        (CONCENTRATION, True, f"ใช้{r.solution}ที่มีความเข้มข้นสูงขึ้น"),
        (CONCENTRATION, False, f"เติมน้ำให้{r.solution}เจือจางลง"),
        (TEMPERATURE, True, "อุ่นสารละลายให้มีอุณหภูมิสูงขึ้น"),
        (TEMPERATURE, False, "แช่ภาชนะในน้ำเย็นให้สารละลายมีอุณหภูมิต่ำลง"),
    ]
    if r.solid:
        lump, powder = r.solid
        out += [(SURFACE, True, f"เปลี่ยนจาก{lump}เป็น{powder}ที่มีมวลเท่ากัน"),
                (SURFACE, False, f"เปลี่ยนจาก{powder}เป็น{lump}ที่มีมวลเท่ากัน")]
    if r.catalyst:
        out.append((CATALYST, True, f"เติม{r.catalyst}ลงไป"))
    return out


# How each factor is set out across the four runs of an experiment.
LEVELS = {
    CONCENTRATION: ("ความเข้มข้นของ{solution}", ("0.5", "1.0", "1.5", "2.0"), "mol/dm³"),
    TEMPERATURE: ("อุณหภูมิของสารละลาย", ("20", "30", "40", "50"), "°C"),
}


@question_type(
    "chem.rate_factor_foundation",
    display_name={"th": "ผลของการเปลี่ยนปัจจัยต่ออัตราการเกิดปฏิกิริยาเคมี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_FACTOR,
)
class RateFactorFoundation(QuestionType):
    """One change at a time: which factor it is, and which way the rate goes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction = rng.choice(RATE_REACTIONS)
        factor, faster, change = rng.choice(_changes(reaction))
        if rng.random() < 0.5:
            correct = FASTER if faster else SLOWER
            return _labelled(
                stem=(f"ในการทดลองปฏิกิริยาระหว่าง{reaction.name} ถ้า{change} "
                      "ปฏิกิริยาจะเกิดเร็วขึ้นหรือช้าลง"),
                correct=correct, wrongs=tuple(a for a in RATE_ANSWERS if a != correct),
                topic=TOPIC_RATE_FACTOR,
                hint=("ความเข้มข้นสูง พื้นที่ผิวมาก อุณหภูมิสูง และการเติมตัวเร่งปฏิกิริยา "
                      "ทำให้ปฏิกิริยาเกิดเร็วขึ้น"),
            )
        return _labelled(
            stem=(f"ในการทดลองปฏิกิริยาระหว่าง{reaction.name} การ{change} "
                  "เป็นการเปลี่ยนปัจจัยใด"),
            correct=factor, wrongs=tuple(f for f in FACTORS if f != factor),
            topic=TOPIC_RATE_FACTOR,
            hint="ดูว่าสิ่งที่เปลี่ยนคือปริมาณสารในสารละลาย ขนาดของของแข็ง ความร้อน หรือสารที่เติมเพิ่ม",
        )


@question_type(
    "chem.rate_factor_fluency",
    display_name={"th": "อธิบายผลของปัจจัยต่ออัตราการเกิดปฏิกิริยาด้วยการชนของอนุภาค"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_FACTOR,
)
class RateFactorFluency(QuestionType):
    """The indicator's verb, อธิบาย: why the change moves the rate."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction = rng.choice(RATE_REACTIONS)
        factor, faster, change = rng.choice(_changes(reaction))
        correct = EXPLAIN[(factor, faster)]
        others = [text_ for (f, d), text_ in EXPLAIN.items() if d == faster and f != factor]
        wrongs = [*rng.sample(others, min(2, len(others))), *MISCONCEPTION[faster]]
        return _labelled(
            stem=(f"เมื่อ{change} ปฏิกิริยาระหว่าง{reaction.name}"
                  f"{FASTER if faster else SLOWER} ข้อใดอธิบายเหตุผลได้ถูกต้อง"),
            correct=correct, wrongs=tuple(wrongs[:3]),
            topic=TOPIC_RATE_FACTOR,
            hint="ปฏิกิริยาเกิดเมื่ออนุภาคชนกันด้วยพลังงานมากพอ ถามตัวเองว่าการเปลี่ยนนี้ทำให้การชนแบบนั้นมากขึ้นหรือน้อยลง",
        )


@question_type(
    "chem.rate_factor_application",
    display_name={"th": "แปลผลการทดลองอัตราการเกิดปฏิกิริยาเคมี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_FACTOR,
)
class RateFactorApplication(QuestionType):
    """Read a four-run experiment: the fastest run, the conclusion, the
    variables, and an average rate from a gas volume and a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.3:
            return self._average_rate(rng)
        reaction = rng.choice(RATE_REACTIONS)
        factor = rng.choice((CONCENTRATION, TEMPERATURE))
        label, values, unit = LEVELS[factor]
        label = label.format(solution=reaction.solution)
        # Times fall strictly as the factor rises; the run order is shuffled.
        times = sorted(rng.sample(range(20, 240, 5), 4), reverse=True)
        runs = list(zip(values, times))
        rng.shuffle(runs)
        table = " / ".join(f"ชุดที่ {i} {label} {v} {unit} ใช้เวลา {t} วินาที"
                           for i, (v, t) in enumerate(runs, start=1))
        stem = (f"นักเรียนทดลองปฏิกิริยาระหว่าง{reaction.name} โดยเปลี่ยน{label} "
                f"และจับเวลาจนเกิด{reaction.measure}ในปริมาณที่เท่ากัน ได้ผลดังนี้ {table} ")
        if shape < 0.55:
            fastest = min(range(4), key=lambda i: runs[i][1]) + 1
            correct = f"ชุดที่ {fastest}"
            return _labelled(
                stem=stem + "ชุดใดเกิดปฏิกิริยาเร็วที่สุด",
                correct=correct,
                wrongs=tuple(f"ชุดที่ {i}" for i in range(1, 5) if i != fastest),
                topic=TOPIC_RATE_FACTOR,
                hint="เวลาที่ใช้น้อยที่สุดคือปฏิกิริยาที่เกิดเร็วที่สุด",
            )
        if shape < 0.8:
            return _labelled(
                stem=stem + "ข้อสรุปใดถูกต้องตามผลการทดลองนี้",
                correct=f"เมื่อ{label}สูงขึ้น ปฏิกิริยาเกิดเร็วขึ้น",
                wrongs=(f"เมื่อ{label}สูงขึ้น ปฏิกิริยาเกิดช้าลง",
                        f"{label}ไม่มีผลต่ออัตราการเกิดปฏิกิริยา",
                        f"เมื่อ{label}สูงขึ้น ต้องใช้เวลานานขึ้น"),
                topic=TOPIC_RATE_FACTOR,
                hint="เรียงชุดการทดลองตามค่าที่เปลี่ยน แล้วดูว่าเวลาที่ใช้เพิ่มหรือลด เวลาน้อยหมายถึงเกิดเร็ว",
            )
        controlled = "อุณหภูมิของสารละลาย" if factor == CONCENTRATION else f"ความเข้มข้นของ{reaction.solution}"
        role = rng.choice(("ตัวแปรต้น", "ตัวแปรตาม", "ตัวแปรควบคุม"))
        answers = {"ตัวแปรต้น": label, "ตัวแปรตาม": "เวลาที่ใช้ในการเกิดปฏิกิริยา",
                   "ตัวแปรควบคุม": controlled}
        return _labelled(
            stem=stem + f"ข้อใดเป็น{role}ของการทดลองนี้",
            correct=answers[role],
            wrongs=(*[v for k, v in answers.items() if k != role], "จำนวนนักเรียนที่ทำการทดลอง"),
            topic=TOPIC_RATE_FACTOR,
            hint="ตัวแปรต้นคือสิ่งที่ผู้ทดลองจงใจเปลี่ยน ตัวแปรตามคือผลที่วัด ตัวแปรควบคุมคือสิ่งที่ต้องทำให้เท่ากันทุกชุด",
        )

    @staticmethod
    def _average_rate(rng):
        reaction = rng.choice([r for r in RATE_REACTIONS if r.measure.startswith("แก๊ส")])
        rate = Fraction(rng.choice((1, 2, 3, 4, 5, 6, 8, 10)), rng.choice((1, 2)))
        seconds = rng.choice((10, 20, 30, 40, 50, 60, 80, 100, 120))
        volume = rate * seconds

        def show(x: Fraction) -> str:
            return f"{float(x):.2f}".rstrip("0").rstrip(".")

        wrongs = [rate * 2, rate / 2, rate + 1, Fraction(seconds) / volume, rate * 3]
        return GeneratedQuestion(
            stem=[text(f"ปฏิกิริยาระหว่าง{reaction.name} เก็บ{reaction.measure}ได้ "
                       f"{show(volume)} cm³ ในเวลา {seconds} วินาที "
                       f"อัตราการเกิด{reaction.measure}เฉลี่ยเท่ากับเท่าใด")],
            correct=[text(f"{show(rate)} cm³/s")],
            distractors=fixed(*[[text(f"{show(w)} cm³/s")] for w in wrongs if w > 0]),
            topic=TOPIC_RATE_FACTOR,
            hint=[text("อัตราการเกิดปฏิกิริยาเฉลี่ย = ปริมาณผลิตภัณฑ์ที่เกิดขึ้น ÷ เวลาที่ใช้")],
        )

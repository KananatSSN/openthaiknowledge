"""ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/5

Sets moved here from: science_wave_f32.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f32 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_COMPARE = "ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี"


# (factor, low setting, high setting): the high setting is faster.
FACTORS = (
    ("ความเข้มข้นของ HCl", ("0.5 mol/dm³", "1.0 mol/dm³", "2.0 mol/dm³")),
    ("อุณหภูมิ", ("25 °C", "35 °C", "45 °C")),
    ("ลักษณะของ Mg", ("แท่งหนา", "แถบบาง", "ผง")),
    ("ตัวเร่งปฏิกิริยา", ("ไม่ใส่", "ใส่", None)),
)


def _describe(setting: dict) -> str:
    parts = [f"Mg {setting['ลักษณะของ Mg']}", f"HCl {setting['ความเข้มข้นของ HCl']}", f"ที่ {setting['อุณหภูมิ']}"]
    return " ".join(parts)


@question_type(
    "chem.rate_compare_foundation",
    display_name={"th": "เปรียบเทียบอัตราการเกิดปฏิกิริยาเมื่อเปลี่ยนปัจจัยเดียว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class RateCompareFoundation(QuestionType):
    """Change one factor; the more concentrated, finer, hotter or catalysed run is faster."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        base = {name: rng.choice([v for v in values if v][:2]) for name, values in FACTORS[:3]}
        factor, values = rng.choice(FACTORS[:3])
        options = [v for v in values if v]
        low, high = sorted(rng.sample(range(len(options)), 2))
        a, b = dict(base), dict(base)
        a[factor], b[factor] = options[low], options[high]
        runs = [a, b]
        rng.shuffle(runs)
        pair = [("ก", runs[0]), ("ข", runs[1])]
        fast = next(label for label, s in pair if s is b)
        slow = next(label for label, s in pair if s is a)
        reason = {"ความเข้มข้นของ HCl": "ความเข้มข้นสูงกว่า อนุภาคชนกันบ่อยกว่า",
                  "อุณหภูมิ": "อุณหภูมิสูงกว่า อนุภาคมีพลังงานถึง Ea มากกว่าและชนกันบ่อยกว่า",
                  "ลักษณะของ Mg": "พื้นที่ผิวมากกว่า อนุภาคชนกันได้มากกว่า"}[factor]
        return _labelled(stem=f"การทดลอง {pair[0][0]}: {_describe(pair[0][1])} การทดลอง {pair[1][0]}: {_describe(pair[1][1])} "
                              "(ใช้ Mg มวลเท่ากันและ HCl ปริมาตรเท่ากัน) การทดลองใดเกิดปฏิกิริยาเร็วกว่า และเพราะเหตุใด",
                         correct=f"การทดลอง {fast} เพราะ{reason}",
                         wrongs=(f"การทดลอง {slow} เพราะ{reason}", f"การทดลอง {slow} เพราะใช้สารน้อยกว่าจึงหมดเร็วกว่า",
                                 "เร็วเท่ากัน เพราะใช้สารชนิดเดียวกัน"),
                         topic=TOPIC_COMPARE,
                         hint="หาปัจจัยที่ต่างกันเพียงอย่างเดียว: เข้มข้นกว่า ผิวมากกว่า ร้อนกว่า หรือมีตัวเร่ง จะเร็วกว่า")


@question_type(
    "chem.rate_compare_fluency",
    display_name={"th": "เรียงลำดับอัตราการเกิดปฏิกิริยาของหลายการทดลอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class RateCompareFluency(QuestionType):
    """Each run is at least as fast as the last on every factor, so the order is certain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        runs = []
        levels = [0, 0, 0]
        for _ in range(3):
            runs.append(tuple(levels))
            bump = rng.randrange(3)
            levels[bump] = min(levels[bump] + 1, 2)
            if tuple(levels) == runs[-1]:
                bump = next(i for i in range(3) if levels[i] < 2)
                levels[bump] += 1
        settings = [{FACTORS[i][0]: FACTORS[i][1][lv] for i, lv in enumerate(r)} for r in runs]
        labels = ["ก", "ข", "ค"]
        order = list(range(3))
        rng.shuffle(order)
        shown = {labels[i]: settings[order[i]] for i in range(3)}
        fastest_first = sorted(labels, key=lambda ell: -order[labels.index(ell)])
        right = " > ".join(fastest_first)
        others = [" > ".join(p) for p in (fastest_first[::-1], [fastest_first[1], fastest_first[0], fastest_first[2]],
                                          [fastest_first[0], fastest_first[2], fastest_first[1]],
                                          # Both rotations: every run misplaced.
                                          fastest_first[1:] + fastest_first[:1], fastest_first[2:] + fastest_first[:2])]
        return _labelled(stem="เรียงอัตราการเกิดปฏิกิริยาของ Mg มวลเท่ากันกับ HCl ปริมาตรเท่ากันจากเร็วไปช้า: "
                              + " ".join(f"{ell}: {_describe(s)}" for ell, s in shown.items()),
                         correct=right, wrongs=tuple(others), topic=TOPIC_COMPARE,
                         hint="การทดลองที่เข้มข้นกว่า ผิวมากกว่า และร้อนกว่าในทุกด้าน จะเร็วที่สุด")


@question_type(
    "chem.rate_compare_application",
    display_name={"th": "ผลของอุณหภูมิต่อเวลาที่ใช้ในการเกิดปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMPARE,
)
class RateCompareApplication(QuestionType):
    """The textbook rule of thumb: every 10 °C doubles the rate, halving the time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        steps = rng.randint(1, 3)
        t1 = rng.choice((20, 25, 30, 35, 40))
        time1 = rng.choice((40, 60, 80, 120, 160, 240, 320, 480))
        hotter = rng.random() < 0.6
        t2 = t1 + 10 * steps if hotter else t1 - 10 * steps
        time2 = Fraction(time1, 2 ** steps) if hotter else time1 * 2 ** steps
        if rng.random() < 0.5:
            return numeric(stem=f"ปฏิกิริยาหนึ่งที่ {t1} °C ใช้เวลา {time1} s ถ้าอัตราเพิ่มเป็น 2 เท่าทุกครั้งที่อุณหภูมิเพิ่ม 10 °C "
                                f"ที่ {t2} °C จะใช้เวลากี่วินาที",
                           answer=time2, wrongs=[time1 * 2 ** steps if hotter else Fraction(time1, 2 ** steps),
                                                 Fraction(time1, 2 * steps) if hotter else time1 * 2 * steps if steps > 1 else time1 * 3,
                                                 time1], unit="s", topic=TOPIC_COMPARE,
                           hint="อุณหภูมิเปลี่ยน 10 °C กี่ช่วง อัตราเปลี่ยน 2 เท่าต่อช่วง และเวลาที่ใช้แปรผกผันกับอัตรา")
        return numeric(stem=f"ปฏิกิริยาหนึ่งมีอัตราเพิ่มเป็น 2 เท่าทุกครั้งที่อุณหภูมิเพิ่ม 10 °C ถ้าเพิ่มอุณหภูมิจาก {t1} °C "
                            f"เป็น {t1 + 10 * steps} °C อัตราการเกิดปฏิกิริยาจะเป็นกี่เท่าของเดิม",
                       answer=2 ** steps, wrongs=[2 * steps if steps != 2 else 3, steps + 1 if steps != 1 else 3, 10 * steps],
                       unit="เท่า", topic=TOPIC_COMPARE, hint="ทุก 10 °C คูณ 2 เช่น 30 °C = 3 ช่วง อัตรา 2 × 2 × 2 = 8 เท่า")

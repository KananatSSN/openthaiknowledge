"""ความเร่งจากข้อมูลความเร็วกับเวลา

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/1

Sets moved here from: science_wave_e10.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type

PROVENANCE = Provenance("original")


SUBJECT = "ฟิสิกส์"


UPPER_FIVE = {"th": "ม.5"}


TOPIC = "ความเร่งจากข้อมูลความเร็วกับเวลา"


MOVERS = ("รถยนต์คันหนึ่ง", "รถไฟขบวนหนึ่ง", "นักปั่นจักรยานคนหนึ่ง", "เรือยนต์ลำหนึ่ง",
          "รถจักรยานยนต์คันหนึ่ง", "เครื่องบินที่กำลังวิ่งบนทางวิ่ง")


SPEEDING, STEADY, SLOWING = ("ความเร่งมีทิศเดียวกับความเร็ว วัตถุเคลื่อนที่เร็วขึ้น",
                             "ความเร่งเป็นศูนย์ วัตถุเคลื่อนที่ด้วยความเร็วคงตัว",
                             "ความเร่งมีทิศตรงข้ามกับความเร็ว วัตถุเคลื่อนที่ช้าลง")


KINDS = (SPEEDING, STEADY, SLOWING)


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=TOPIC,
        hint=[text(hint)],
    )


def _a(value: float) -> str:
    return f"{value:g} m/s²"


def _accel(*, stem: str, answer: float, wrongs: list[float], hint: str) -> GeneratedQuestion:
    """Four distinct accelerations; the obvious slips first, then neighbours."""
    seen = [answer]
    for w in [*wrongs, answer + 1, answer - 1, answer * 2, answer / 2, answer + 2, answer - 2]:
        if w not in seen:
            seen.append(w)
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(_a(answer))],
        distractors=fixed(*[[text(_a(w))] for w in seen[1:]]),
        topic=TOPIC, hint=[text(hint)],
    )


def record(rng: Random, *, sign: int | None = None, rows: int = 5):
    """(times, velocities, acceleration): a uniformly accelerated record.

    ``sign`` forces speeding up (+1), steady (0) or slowing down (-1). A slowing
    record never passes through zero, so the object keeps its direction.
    """
    step = rng.choice((1, 2, 5))
    sign = rng.choice((1, 0, -1)) if sign is None else sign
    size = rng.choice((1, 2, 3, 4)) if sign else 0
    change = size * step                        # velocity change per row, whole m/s
    a = sign * size
    if sign < 0:
        v0 = change * (rows - 1) + rng.randint(1, 10)
    else:
        v0 = rng.randint(0, 20)
    times = [i * step for i in range(rows)]
    velocities = [v0 + sign * change * i for i in range(rows)]
    return times, velocities, a


def table(times, velocities) -> str:
    return " / ".join(f"t = {t} s ความเร็ว {v} m/s" for t, v in zip(times, velocities))


@question_type(
    "phys.acceleration_vt_foundation",
    display_name={"th": "ความหมายของความเร่งและทิศของความเร่ง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class AccelerationVtFoundation(QuestionType):
    """What acceleration is, and reading its sign off a short record."""

    DEFINITIONS = (
        ("ความเร่งของวัตถุหมายถึงข้อใด", "ความเร็วที่เปลี่ยนไปในหนึ่งหน่วยเวลา",
         ("ระยะทางที่วัตถุเคลื่อนที่ได้ในหนึ่งหน่วยเวลา", "ความเร็วสูงสุดของวัตถุ",
          "เวลาที่วัตถุใช้ในการหยุดนิ่ง")),
        ("ความเร่งมีหน่วยในระบบเอสไอเป็นข้อใด", "เมตรต่อวินาทีกำลังสอง (m/s²)",
         ("เมตรต่อวินาที (m/s)", "เมตร (m)", "นิวตัน (N)")),
        ("วัตถุที่เคลื่อนที่ด้วยความเร็วคงตัวในแนวตรงมีความเร่งเท่าใด", "ศูนย์",
         ("เท่ากับความเร็วของวัตถุ", "มีค่าคงตัวที่ไม่เป็นศูนย์", "มีค่าเพิ่มขึ้นตลอดเวลา")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ความเร่ง = ความเร็วที่เปลี่ยนไป ÷ เวลาที่ใช้ ถ้าความเร็วเพิ่มขึ้น ความเร่งมีทิศเดียวกับความเร็ว"
        shape = rng.random()
        if shape < 0.25:
            stem, correct, wrongs = rng.choice(self.DEFINITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, hint=hint)
        if shape < 0.6:
            times, velocities, a = record(rng, rows=4)
            kind = SPEEDING if a > 0 else STEADY if a == 0 else SLOWING
            return _labelled(
                stem=(f"{rng.choice(MOVERS)}เคลื่อนที่ในแนวตรงทิศเดียว บันทึกความเร็วได้ดังนี้ "
                      f"{table(times, velocities)} ข้อใดอธิบายความเร่งได้ถูกต้อง"),
                correct=kind,
                wrongs=(*[k for k in KINDS if k != kind],
                        "ความเร่งเท่ากับความเร็วสุดท้ายที่บันทึกได้"),
                hint=hint,
            )
        # "gains 3 m/s every second" read as a number.
        size = rng.randint(1, 9)
        step = rng.choice((1, 2, 4, 5))
        change = size * step
        sign = rng.choice((1, -1))
        verb = "เพิ่มขึ้น" if sign > 0 else "ลดลง"
        return _accel(
            stem=(f"{rng.choice(MOVERS)}เคลื่อนที่ในแนวตรง ความเร็ว{verb} {change} m/s "
                  f"ทุก ๆ {step} วินาที ความเร่งมีค่าเท่าใด (ให้ทิศการเคลื่อนที่เป็นบวก)"),
            answer=sign * size,
            wrongs=[-sign * size, sign * change, sign * change * step],
            hint=hint,
        )


@question_type(
    "phys.acceleration_vt_fluency",
    display_name={"th": "หาความเร่งจากข้อมูลความเร็วกับเวลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class AccelerationVtFluency(QuestionType):
    """The indicator: work out the acceleration from a velocity-time record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        times, velocities, a = record(rng, sign=rng.choice((1, 1, -1)))
        i, j = sorted(rng.sample(range(len(times)), 2))
        dv = velocities[j] - velocities[i]
        mover = rng.choice(MOVERS)
        if rng.random() < 0.5:
            stem = (f"{mover}เคลื่อนที่ในแนวตรง บันทึกความเร็วได้ดังนี้ {table(times, velocities)} "
                    "ความเร่งของการเคลื่อนที่นี้เท่ากับเท่าใด (ให้ทิศการเคลื่อนที่เป็นบวก)")
        else:
            stem = (f"{mover}เคลื่อนที่ในแนวตรง ที่เวลา {times[i]} s มีความเร็ว {velocities[i]} m/s "
                    f"และที่เวลา {times[j]} s มีความเร็ว {velocities[j]} m/s "
                    "ถ้าความเร่งคงตัว ความเร่งเท่ากับเท่าใด (ให้ทิศการเคลื่อนที่เป็นบวก)")
        # The slips: forgetting to divide, dividing the final velocity by the
        # end time, and losing the sign.
        end_ratio = velocities[j] / times[j] if times[j] else dv
        return _accel(stem=stem, answer=a,
                      wrongs=[dv, -a, round(end_ratio, 2)],
                      hint="ความเร่ง = (ความเร็วปลาย − ความเร็วต้น) ÷ (เวลาปลาย − เวลาต้น) "
                           "ถ้าความเร็วลดลง ความเร่งเป็นลบ")


@question_type(
    "phys.acceleration_vt_application",
    display_name={"th": "วิเคราะห์การเคลื่อนที่หลายช่วงจากข้อมูลความเร็วกับเวลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class AccelerationVtApplication(QuestionType):
    """A trip in three stretches — speeding up, cruising, braking — and a
    velocity predicted from a constant acceleration."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.3:
            # Predict: v = u + at.
            u = rng.randint(0, 20)
            a = rng.choice((1, 2, 3, 4, 5, -1, -2, -3))
            t = rng.randint(2, 8)
            if u + a * t <= 0:
                a = -a
            v = u + a * t
            wrongs = [u + a, a * t, u - a * t, v + a]
            seen = [v]
            for w in [*wrongs, v + 1, v - 1, v + 2, v - 2]:
                if w >= 0 and w not in seen:
                    seen.append(w)
            verb = "เร่ง" if a > 0 else "ลดความเร็ว"
            return GeneratedQuestion(
                stem=[text(f"{rng.choice(MOVERS)}มีความเร็ว {u} m/s แล้ว{verb}ด้วยความเร่งขนาด {abs(a)} m/s² "
                           f"คงตัวเป็นเวลา {t} วินาที ความเร็วเมื่อสิ้นสุดช่วงเวลานี้เท่ากับเท่าใด")],
                correct=[text(f"{v} m/s")],
                distractors=fixed(*[[text(f"{w} m/s")] for w in seen[1:]]),
                topic=TOPIC,
                hint=[text("ความเร็วปลาย = ความเร็วต้น + ความเร่ง × เวลา (ถ้าลดความเร็ว ความเร่งเป็นลบ)")],
            )
        # Three stretches, each a whole number of seconds.
        a1 = rng.randint(1, 4)
        t1 = rng.randint(2, 5)
        t2 = rng.randint(2, 5)
        top = a1 * t1
        # A braking size that divides the top speed and differs from a1, so the
        # comparison below never ties. 1 and top itself always divide.
        a3_size = rng.choice([d for d in (1, 2, 3, 4, 5, 6) if top % d == 0 and d != a1])
        t3 = top // a3_size
        marks = [0, t1, t1 + t2, t1 + t2 + t3]
        record_text = (f"t = {marks[0]} s ความเร็ว 0 m/s / t = {marks[1]} s ความเร็ว {top} m/s / "
                       f"t = {marks[2]} s ความเร็ว {top} m/s / t = {marks[3]} s ความเร็ว 0 m/s")
        stretches = (f"ช่วง {marks[0]}–{marks[1]} s", f"ช่วง {marks[1]}–{marks[2]} s",
                     f"ช่วง {marks[2]}–{marks[3]} s")
        stem = (f"{rng.choice(MOVERS[:2])}ออกจากจุดหยุดนิ่ง เคลื่อนที่ในแนวตรง "
                f"และความเร็วเปลี่ยนอย่างสม่ำเสมอในแต่ละช่วง บันทึกได้ดังนี้ {record_text} ")
        hint = "แต่ละช่วงใช้ความเร่ง = ความเร็วที่เปลี่ยนไป ÷ เวลาของช่วงนั้น ความเร็วไม่เปลี่ยนแปลว่าความเร่งเป็นศูนย์"
        if shape < 0.55:
            which = rng.choice(("เป็นศูนย์", "มีค่าเป็นลบ", "มีค่าเป็นบวก"))
            index = {"มีค่าเป็นบวก": 0, "เป็นศูนย์": 1, "มีค่าเป็นลบ": 2}[which]
            return _labelled(
                stem=stem + f"ช่วงใดที่ความเร่ง{which}",
                correct=stretches[index],
                wrongs=(*[s for k, s in enumerate(stretches) if k != index],
                        f"ช่วง {marks[0]}–{marks[3]} s ตลอดการเคลื่อนที่"),
                hint=hint,
            )
        if shape < 0.8:
            index = rng.randrange(3)
            answer = (a1, 0, -a3_size)[index]
            return _accel(
                stem=stem + f"ความเร่งใน{stretches[index]}เท่ากับเท่าใด (ให้ทิศการเคลื่อนที่เป็นบวก)",
                answer=answer,
                wrongs=[-answer, (a1, 0, -a3_size)[(index + 1) % 3], top],
                hint=hint,
            )
        faster = "ช่วงเร่ง" if a1 > a3_size else "ช่วงเบรก"
        return _labelled(
            stem=stem + "ข้อใดเปรียบเทียบขนาดของความเร่งในช่วงแรกกับช่วงสุดท้ายได้ถูกต้อง",
            correct=(f"ขนาดของความเร่งใน{faster}มากกว่า เพราะความเร็วเปลี่ยนไปเท่ากันในเวลาที่สั้นกว่า"),
            wrongs=(f"ขนาดของความเร่งใน{'ช่วงเบรก' if faster == 'ช่วงเร่ง' else 'ช่วงเร่ง'}มากกว่า "
                    "เพราะความเร็วเปลี่ยนไปเท่ากันในเวลาที่สั้นกว่า",
                    "ขนาดของความเร่งเท่ากัน เพราะความเร็วเปลี่ยนไปเท่ากัน",
                    "ขนาดของความเร่งเท่ากัน เพราะความเร็วสูงสุดเท่ากัน"),
            hint="ความเร็วเปลี่ยนไปเท่ากัน ช่วงที่ใช้เวลาน้อยกว่ามีขนาดของความเร่งมากกว่า",
        )

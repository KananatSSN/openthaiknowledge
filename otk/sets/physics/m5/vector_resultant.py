"""ปริมาณเวกเตอร์และการรวมแรงในระนาบเดียวกัน

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/2

Sets moved here from: science_wave_e7.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type

PROVENANCE = Provenance("adapted", sources=('sheet_database/outputs/teaching_plan/ข้อสอบแรง.md',))


SUBJECT = "ฟิสิกส์"


UPPER_FIVE = {"th": "ม.5"}


TOPIC = "ปริมาณเวกเตอร์และการรวมแรงในระนาบเดียวกัน"


VECTOR, SCALAR = "ปริมาณเวกเตอร์", "ปริมาณสเกลาร์"


# Physics quantities as IPST classifies them, not as a maths vector space.
VECTOR_QUANTITIES = ("แรง", "ความเร็ว", "การกระจัด", "ความเร่ง", "น้ำหนัก", "โมเมนตัม",
                     "แรงเสียดทาน", "สนามไฟฟ้า", "แรงลอยตัว")


SCALAR_QUANTITIES = ("มวล", "อัตราเร็ว", "ระยะทาง", "เวลา", "อุณหภูมิ", "พลังงาน",
                     "ปริมาตร", "ความหนาแน่น", "งาน", "กำลัง", "ความยาว", "พื้นที่")


# (a statement, whether it states a vector quantity)
QUANTITY_STATEMENTS = (
    ("รถแล่นด้วยความเร็ว 60 กิโลเมตรต่อชั่วโมง ไปทางทิศเหนือ", True),
    ("นักวิ่งวิ่งได้ระยะทาง 400 เมตร", False),
    ("ลมพัดด้วยความเร็ว 20 กิโลเมตรต่อชั่วโมง จากทิศตะวันตก", True),
    ("กล่องมีมวล 12 กิโลกรัม", False),
    ("ผลักรถเข็นด้วยแรง 50 นิวตัน ไปทางขวา", True),
    ("น้ำในแก้วมีอุณหภูมิ 25 องศาเซลเซียส", False),
    ("เครื่องบินมีการกระจัด 300 กิโลเมตร ไปทางทิศตะวันออกเฉียงใต้", True),
    ("หลอดไฟใช้พลังงาน 3,600 จูล", False),
    ("ลูกบอลตกด้วยความเร่ง 10 เมตรต่อวินาทีกำลังสอง ในทิศลง", True),
    ("การเดินทางใช้เวลา 3 ชั่วโมง", False),
)


# The pairs students most often merge into one idea.
CONFUSABLE_PAIRS = (
    ("อัตราเร็ว", "ความเร็ว", "อัตราเร็วบอกเพียงว่าเร็วเท่าใด ส่วนความเร็วบอกทั้งความเร็วและทิศทางของการเคลื่อนที่"),
    ("ระยะทาง", "การกระจัด", "ระยะทางวัดตามเส้นทางจริง ส่วนการกระจัดวัดตรงจากจุดเริ่มถึงจุดสุดท้ายพร้อมทิศทาง"),
    ("มวล", "น้ำหนัก", "มวลคือเนื้อสารซึ่งคงที่ ส่วนน้ำหนักคือแรงโน้มถ่วงที่กระทำต่อมวล มีทิศลง"),
)


# (a, b, c) with a² + b² = c², so a perpendicular resultant is a whole number.
TRIPLES = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17),
           (12, 16, 20), (7, 24, 25), (10, 24, 26), (15, 20, 25), (20, 21, 29))


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...],
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=TOPIC,
        hint=[text(hint)],
    )


def _newtons(*, stem: str, answer: int, wrongs: tuple[int, ...],
             hint: str) -> GeneratedQuestion:
    """Four distinct newton values, the correct one first."""
    seen = [answer]
    for value in wrongs:
        if value > 0 and value not in seen:
            seen.append(value)
        if len(seen) == 4:
            break
    padding = 1
    while len(seen) < 4:
        if answer + padding not in seen:
            seen.append(answer + padding)
        padding += 1
    return _labelled(stem=stem, correct=f"{answer} นิวตัน",
                     wrongs=tuple(f"{value} นิวตัน" for value in seen[1:]),
                     hint=hint)


# (the vector statement, the wrong choices offered against it)
VECTOR_STATEMENTS = (
    ("เรือแล่นจากท่าไปทางทิศตะวันออกเป็นระยะ 12 กิโลเมตร",
     ("นักเรียนวิ่งได้ระยะทางรวม 400 เมตร", "การแข่งขันใช้เวลา 2 ชั่วโมง",
      "อุณหภูมิของน้ำเท่ากับ 30 องศาเซลเซียส")),
    ("น้ำหนักของกล่องใบนี้เท่ากับ 25 นิวตัน",
     ("นักเรียนวิ่งได้ระยะทางรวม 400 เมตร", "มวลของกล่องใบนี้เท่ากับ 2.5 กิโลกรัม",
      "รถใช้น้ำมัน 8 ลิตร")),
)


@question_type(
    "phys.vector_resultant_foundation",
    display_name={"th": "จำแนกปริมาณเวกเตอร์กับปริมาณสเกลาร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class VectorResultantFoundation(QuestionType):
    """The prerequisite tier: what a vector is, and which quantities are vectors."""

    DEFINITIONS = (
        ("ปริมาณเวกเตอร์หมายถึงข้อใด",
         "ปริมาณที่มีทั้งขนาดและทิศทาง",
         ("ปริมาณที่มีขนาดเพียงอย่างเดียว",
          "ปริมาณที่มีทิศทางเพียงอย่างเดียว",
          "ปริมาณที่วัดค่าไม่ได้"),
         "เวกเตอร์ต้องบอกทั้ง \"เท่าใด\" และ \"ไปทางไหน\""),
        ("ปริมาณสเกลาร์หมายถึงข้อใด",
         "ปริมาณที่มีขนาดเพียงอย่างเดียว",
         ("ปริมาณที่มีทั้งขนาดและทิศทาง",
          "ปริมาณที่มีทิศทางเพียงอย่างเดียว",
          "ปริมาณที่มีหน่วยเป็นนิวตันเสมอ"),
         "สเกลาร์บอกเพียงว่า \"เท่าใด\" ไม่ต้องบอกทิศทาง"),
        ("การรวมปริมาณเวกเตอร์ต่างจากการรวมปริมาณสเกลาร์อย่างไร",
         "การรวมเวกเตอร์ต้องคิดทิศทางด้วย จะบวกกันตรง ๆ ไม่ได้เสมอไป",
         ("การรวมเวกเตอร์บวกกันตรง ๆ ได้เสมอเหมือนสเกลาร์",
          "การรวมสเกลาร์ต้องคิดทิศทางด้วย ส่วนเวกเตอร์บวกตรง ๆ ได้",
          "เวกเตอร์รวมกันไม่ได้ ต้องแยกคิดทีละปริมาณเสมอ"),
         "แรง 3 นิวตันกับ 4 นิวตัน รวมกันได้ตั้งแต่ 1 ถึง 7 นิวตัน ขึ้นกับทิศ"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.34:
            stem, correct, wrongs, hint = rng.choice(self.DEFINITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, hint=hint)
        if shape < 0.5:
            said, vector = rng.choice(QUANTITY_STATEMENTS)
            return _labelled(
                stem=f"\"{said}\" ข้อความนี้กล่าวถึงปริมาณชนิดใด",
                correct=(f"{VECTOR} เพราะระบุทั้งขนาดและทิศทาง" if vector else f"{SCALAR} เพราะระบุเพียงขนาด"),
                wrongs=((f"{SCALAR} เพราะระบุเพียงขนาด" if vector else f"{VECTOR} เพราะระบุทั้งขนาดและทิศทาง"),
                        (f"{SCALAR} เพราะมีหน่วยกำกับชัดเจน" if vector else f"{VECTOR} เพราะมีหน่วยกำกับชัดเจน"),
                        "ไม่จัดเป็นปริมาณทางฟิสิกส์เพราะวัดไม่ได้"),
                hint="ปริมาณเวกเตอร์ต้องบอกทิศทางด้วย ส่วนสเกลาร์บอกเพียงขนาด",
            )
        if shape < 0.67:
            # Classify one named quantity.
            if rng.random() < 0.5:
                name, correct = rng.choice(VECTOR_QUANTITIES), VECTOR
            else:
                name, correct = rng.choice(SCALAR_QUANTITIES), SCALAR
            other = SCALAR if correct == VECTOR else VECTOR
            return _labelled(
                stem=f"\"{name}\" จัดเป็นปริมาณชนิดใด",
                correct=correct,
                wrongs=(other, "เป็นได้ทั้งเวกเตอร์และสเกลาร์", "ไม่จัดเป็นปริมาณทางฟิสิกส์"),
                hint="ถามตัวเองว่าปริมาณนี้ต้องบอกทิศทางด้วยหรือไม่",
            )
        # The confusable pairs — the sheet's ข้อ 1 and ข้อ 4 shape.
        scalar, vector, why = rng.choice(CONFUSABLE_PAIRS)
        return _labelled(
            stem=f"\"{scalar}\" กับ \"{vector}\" ต่างกันอย่างไร",
            correct=why,
            wrongs=(f"{scalar}เป็นปริมาณเวกเตอร์ที่มีทิศทาง ส่วน{vector}เป็นปริมาณสเกลาร์ที่บอกเพียงขนาด",
                    f"ทั้ง{scalar}และ{vector}เป็นปริมาณเวกเตอร์ ต่างกันเพียงหน่วยที่ใช้วัด",
                    f"ทั้ง{scalar}และ{vector}มีค่าเท่ากันเสมอ เพียงแต่เรียกชื่อต่างกัน"),
            hint=f"{vector}เป็นปริมาณเวกเตอร์ ส่วน{scalar}เป็นปริมาณสเกลาร์",
        )


@question_type(
    "phys.vector_resultant_fluency",
    display_name={"th": "หาแรงลัพธ์ของแรงในระนาบเดียวกันด้วยแผนภาพการรวมแบบเวกเตอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class VectorResultantFluency(QuestionType):
    """The indicator's own verb: combine two coplanar forces into a resultant."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.34:                     # same direction — resultant adds
            f1 = rng.randint(3, 40)
            f2 = rng.randint(3, 40)
            direction = rng.choice(("ไปทางขวา", "ไปทางทิศเหนือ", "ไปทางทิศตะวันออก"))
            return _newtons(
                stem=(f"แรง {f1} นิวตัน และแรง {f2} นิวตัน กระทำต่อวัตถุเดียวกัน "
                      f"โดยทั้งสองแรงมีทิศ{direction}เหมือนกัน แรงลัพธ์มีขนาดเท่าใด"),
                answer=f1 + f2,
                wrongs=(abs(f1 - f2), max(f1, f2), f1 * f2),
                hint="แรงทิศเดียวกัน เขียนเวกเตอร์ต่อหัวต่อหาง ขนาดจึงบวกกัน",
            )
        if shape < 0.67:                     # opposite — resultant subtracts
            f1, f2 = sorted(rng.sample(range(5, 45), 2), reverse=True)
            return _newtons(
                stem=(f"แรง {f1} นิวตัน มีทิศไปทางขวา และแรง {f2} นิวตัน มีทิศไปทางซ้าย "
                      f"กระทำต่อวัตถุเดียวกัน แรงลัพธ์มีขนาดเท่าใด"),
                answer=f1 - f2,
                wrongs=(f1 + f2, f1, f2),
                hint="แรงทิศตรงข้าม ขนาดของแรงลัพธ์คือผลต่าง และมีทิศตามแรงที่มากกว่า",
            )
        # Perpendicular — the case the indicator's diagram exists for.
        a, b, c = rng.choice(TRIPLES)
        if rng.random() < 0.5:
            a, b = b, a
        return _newtons(
            stem=(f"แรง {a} นิวตัน มีทิศไปทางทิศตะวันออก และแรง {b} นิวตัน มีทิศไปทางทิศเหนือ "
                  f"กระทำต่อวัตถุเดียวกันที่จุดเดียวกัน จงหาขนาดของแรงลัพธ์"),
            answer=c,
            # Adding as if the forces were in line is the mistake this item exists
            # to catch; the difference is the same mistake with the other sign.
            wrongs=(a + b, abs(a - b), max(a, b)),
            hint="แรงตั้งฉากกัน เขียนแผนภาพเป็นสี่เหลี่ยมมุมฉาก แล้วใช้ทฤษฎีบทพีทาโกรัสกับเส้นทแยงมุม",
        )


@question_type(
    "phys.vector_resultant_application",
    display_name={"th": "ใช้การรวมแบบเวกเตอร์อธิบายสถานการณ์จริง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC,
)
class VectorResultantApplication(QuestionType):
    """Two people pulling, a boat crossing a current, and reading a stated quantity."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.34:
            # Work backwards: the resultant and one force are given.
            a, b, c = rng.choice(TRIPLES)
            return _newtons(
                stem=(f"คนสองคนออกแรงลากเรือที่จุดเดียวกันโดยแนวแรงตั้งฉากกัน "
                      f"คนแรกออกแรง {a} นิวตัน และวัดแรงลัพธ์ได้ {c} นิวตัน "
                      f"คนที่สองออกแรงเท่าใด"),
                answer=b,
                wrongs=(c - a, c + a, a),
                hint="แรงตั้งฉากกัน ใช้พีทาโกรัสย้อนกลับ: กำลังสองของแรงลัพธ์ลบด้วยกำลังสองของแรงที่ทราบ",
            )
        if shape < 0.67:
            # Why the resultant of perpendicular forces is not the plain sum.
            a, b, c = rng.choice(TRIPLES)
            return _labelled(
                stem=(f"นักเรียนคนหนึ่งบอกว่า \"แรง {a} นิวตัน ทางทิศตะวันออก รวมกับแรง {b} นิวตัน "
                      f"ทางทิศเหนือ ได้แรงลัพธ์ {a + b} นิวตัน\" ข้อใดอธิบายได้ถูกต้องที่สุด"),
                correct=(f"ไม่ถูกต้อง เพราะแรงทั้งสองไม่ได้อยู่ในแนวเดียวกัน ต้องรวมแบบเวกเตอร์ "
                         f"ได้แรงลัพธ์ {c} นิวตัน"),
                wrongs=("ถูกต้อง เพราะแรงทุกแรงที่กระทำต่อวัตถุเดียวกันบวกกันได้เสมอ",
                        f"ไม่ถูกต้อง เพราะต้องนำแรงมาลบกัน ได้แรงลัพธ์ {abs(a - b)} นิวตัน",
                        "ไม่ถูกต้อง เพราะแรงตั้งฉากกันหักล้างกันหมด แรงลัพธ์จึงเป็นศูนย์"),
                hint="บวกขนาดกันตรง ๆ ได้เฉพาะเมื่อแรงอยู่ในแนวเดียวกันและทิศเดียวกันเท่านั้น",
            )
        if shape < 0.84:
            a, b = rng.sample(range(2, 21), 2)
            same = rng.random() < 0.5
            big, small = max(a, b), min(a, b)
            return _labelled(
                stem=(f"แรง {a} นิวตัน และแรง {b} นิวตัน กระทำต่อวัตถุในแนวเดียวกัน "
                      f"{'ทิศเดียวกัน' if same else 'ทิศตรงข้ามกัน'} แรงลัพธ์มีขนาดเท่าใด"),
                correct=f"{a + b if same else big - small} นิวตัน",
                wrongs=tuple(f"{w} นิวตัน" for w in dict.fromkeys(
                    (big - small if same else a + b, big, round((a * a + b * b) ** 0.5) if (a * a + b * b) ** 0.5 % 1 == 0 else a + b + 1,
                     a + b + 2, small)) if w != (a + b if same else big - small))[:3],
                hint="แรงในแนวเดียวกัน ทิศเดียวกันนำมาบวก ทิศตรงข้ามนำมาลบ",
            )
        # The sheet's ข้อ 4 shape: which statement reports a vector quantity?
        correct, wrongs = rng.choice(VECTOR_STATEMENTS)
        return _labelled(
            stem="ข้อความในข้อใดกล่าวถึงปริมาณเวกเตอร์",
            correct=correct, wrongs=wrongs,
            hint="ข้อความที่เป็นเวกเตอร์ต้องระบุทั้งขนาดและทิศทาง หรือเป็นปริมาณที่มีทิศทางในตัวเอง เช่น น้ำหนัก",
        )

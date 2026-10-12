"""สมบัติของสารกัมมันตรังสี ครึ่งชีวิต และปริมาณของสารกัมมันตรังสี

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/24

Sets moved here from: science_wave_e9.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e9 import (
    ALPHA,
    BETA,
    GAMMA,
    ISOTOPES,
    RAYS,
    SUBJECT,
    UPPER_FIVE,
    _labelled,
    _show,
)

PROVENANCE = Provenance("original")


TOPIC_DECAY = "สมบัติของสารกัมมันตรังสี ครึ่งชีวิต และปริมาณของสารกัมมันตรังสี"


ALL_EQUAL = "รังสีทั้งสามชนิดมีสมบัตินี้เท่ากัน"


# (what the ray does or is, the ray)
RAY_PROPERTIES = (
    ("เป็นนิวเคลียสของฮีเลียม มีประจุไฟฟ้า +2", ALPHA),
    ("มีอำนาจทะลุผ่านต่ำที่สุด กั้นได้ด้วยกระดาษเพียงแผ่นเดียว", ALPHA),
    ("เบนเข้าหาแผ่นประจุลบเมื่อผ่านสนามไฟฟ้า และมีมวลมากที่สุด", ALPHA),
    ("เป็นอนุภาคอิเล็กตรอน มีประจุไฟฟ้า -1", BETA),
    ("ทะลุผ่านกระดาษได้ แต่กั้นได้ด้วยแผ่นอะลูมิเนียมบาง ๆ", BETA),
    ("เบนเข้าหาแผ่นประจุบวกเมื่อผ่านสนามไฟฟ้า", BETA),
    ("เป็นคลื่นแม่เหล็กไฟฟ้า ไม่มีประจุและไม่มีมวล", GAMMA),
    ("มีอำนาจทะลุผ่านสูงที่สุด ต้องกั้นด้วยตะกั่วหนาหรือคอนกรีตหนา", GAMMA),
    ("ไม่เบนเมื่อผ่านสนามไฟฟ้า", GAMMA),
)


DECAY_FACTS = (
    ("สารกัมมันตรังสีคือสารแบบใด",
     "สารที่นิวเคลียสไม่เสถียร จึงสลายตัวและแผ่รังสีออกมาได้เอง",
     ("สารที่แผ่รังสีออกมาเฉพาะเมื่อได้รับความร้อน",
      "สารที่อิเล็กตรอนหลุดออกจากอะตอมเมื่อถูกแสง",
      "สารทุกชนิดที่มีประจุไฟฟ้า")),
    ("ครึ่งชีวิตของสารกัมมันตรังสีหมายถึงข้อใด",
     "เวลาที่นิวเคลียสของสารกัมมันตรังสีสลายตัวจนเหลือครึ่งหนึ่งของปริมาณเดิม",
     ("ครึ่งหนึ่งของเวลาที่สารสลายตัวจนหมด",
      "เวลาที่สารแผ่รังสีได้แรงที่สุด",
      "เวลาที่สารกัมมันตรังสีใช้ในการละลายน้ำครึ่งหนึ่ง")),
    ("ถ้าเพิ่มอุณหภูมิหรือความดันให้สารกัมมันตรังสี ครึ่งชีวิตจะเป็นอย่างไร",
     "ไม่เปลี่ยนแปลง เพราะครึ่งชีวิตขึ้นกับชนิดของไอโซโทปเท่านั้น",
     ("สั้นลง เพราะนิวเคลียสสลายตัวเร็วขึ้นเมื่อร้อน",
      "ยาวขึ้น เพราะความดันทำให้นิวเคลียสเสถียรขึ้น",
      "สั้นลงเมื่ออุณหภูมิสูง แต่ยาวขึ้นเมื่อความดันสูง")),
    ("สารกัมมันตรังสีชนิดเดียวกันที่อยู่ในรูปธาตุและในรูปสารประกอบ มีครึ่งชีวิตต่างกันหรือไม่",
     "ไม่ต่างกัน เพราะการสลายตัวเกิดที่นิวเคลียส ไม่เกี่ยวกับการเกิดพันธะเคมี",
     ("ต่างกัน เพราะสารประกอบเสถียรกว่าธาตุ",
      "ต่างกัน เพราะธาตุสลายตัวเร็วกว่าสารประกอบเสมอ",
      "บอกไม่ได้ จนกว่าจะทราบสถานะของสาร")),
)


AMOUNT_UNITS = ("กรัม", "มิลลิกรัม", "ไมโครกรัม")


# Isotopes a patient is given, for the dose-remaining story.
MEDICAL = frozenset({"ไอโอดีน-131", "เทคนีเชียม-99m"})


def wrong_counts(n: int) -> list[int]:
    """Three wrong numbers of half-lives: one too many, one too few, and 2n —
    counting the halvings as doublings — topped up if any of those collide."""
    out = []
    for k in (n + 1, n - 1, 2 * n, n + 2, n + 3):
        if k > 0 and k != n and k not in out:
            out.append(k)
    return out[:3]


def _amount_choices(answer, wrongs, unit: str):
    seen = [answer]
    for w in wrongs:
        if w > 0 and w not in seen:
            seen.append(w)
    # Slips on both sides; the registry's rank balancing picks among them.
    for w in (answer / 2, answer * 2, answer / 4, answer * 3, answer * 4):
        if w > 0 and w not in seen and _show(w) not in {_show(s) for s in seen}:
            seen.append(w)
    return [text(f"{_show(answer)} {unit}")], [[text(f"{_show(w)} {unit}")] for w in seen[1:]]


@question_type(
    "chem.radioactive_decay_foundation",
    display_name={"th": "สมบัติของรังสีและสารกัมมันตรังสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DECAY,
)
class RadioactiveDecayFoundation(QuestionType):
    """The first free verb, อธิบายสมบัติ: the three rays and what a half-life is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("แอลฟาเป็นนิวเคลียสฮีเลียม (+2) ทะลุผ่านน้อยที่สุด บีตาเป็นอิเล็กตรอน (-1) "
                "แกมมาเป็นคลื่นแม่เหล็กไฟฟ้า ไม่มีประจุ ทะลุผ่านมากที่สุด")
        shape = rng.random()
        if shape < 0.45:
            description, ray = rng.choice(RAY_PROPERTIES)
            return _labelled(
                stem=f"รังสีชนิดใด{description}",
                correct=ray, wrongs=(*[r for r in RAYS if r != ray], ALL_EQUAL),
                topic=TOPIC_DECAY, hint=hint,
            )
        if shape < 0.7:
            ray = rng.choice(RAYS)
            mine = [d for d, r in RAY_PROPERTIES if r == ray]
            others = [d for d, r in RAY_PROPERTIES if r != ray]
            return _labelled(
                stem=f"ข้อใดเป็นสมบัติของ{ray}",
                correct=rng.choice(mine), wrongs=tuple(others),
                topic=TOPIC_DECAY, hint=hint,
            )
        stem, correct, wrongs = rng.choice(DECAY_FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_DECAY,
                         hint="การสลายตัวเกิดที่นิวเคลียส อัตราการสลายตัวจึงขึ้นกับชนิดของไอโซโทปเท่านั้น")


@question_type(
    "chem.radioactive_decay_fluency",
    display_name={"th": "คำนวณครึ่งชีวิตและปริมาณของสารกัมมันตรังสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DECAY,
)
class RadioactiveDecayFluency(QuestionType):
    """The second free verb, คำนวณ: the amount left, the time taken, the
    half-life itself, and how much has decayed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        iso = rng.choice(ISOTOPES)
        n = rng.randint(1, 5)
        left = Fraction(rng.randint(1, 12))
        start = left * 2 ** n
        unit = rng.choice(AMOUNT_UNITS)
        t = iso.half_life * n
        T = iso.half_life
        hint = [text("ทุก ๆ หนึ่งครึ่งชีวิต ปริมาณจะเหลือครึ่งหนึ่ง: เหลือ = เริ่มต้น ÷ 2ⁿ "
                     "เมื่อ n = เวลาที่ผ่านไป ÷ ครึ่งชีวิต")]
        shape = rng.random()
        if shape < 0.35:
            correct, wrongs = _amount_choices(
                left, [start - left, start / (n + 1), start / (2 * n), left * 2, left / 2], unit)
            stem = (f"{iso.name} มีครึ่งชีวิต {_show(T)} {iso.unit} ถ้าเริ่มต้นมี {_show(start)} {unit} "
                    f"เมื่อเวลาผ่านไป {_show(t)} {iso.unit} จะเหลือ{iso.name}กี่{unit}")
        elif shape < 0.6:
            correct = [text(f"{_show(t)} {iso.unit}")]
            wrongs = [[text(f"{_show(T * k)} {iso.unit}")] for k in wrong_counts(n)]
            stem = (f"{iso.name} มีครึ่งชีวิต {_show(T)} {iso.unit} ต้องใช้เวลานานเท่าใด "
                    f"สาร {_show(start)} {unit} จึงจะเหลือ {_show(left)} {unit}")
        elif shape < 0.8:
            correct = [text(f"{_show(T)} {iso.unit}")]
            # Dividing by the wrong number of halvings, or not dividing at all.
            wrongs = [[text(f"{_show(t / k)} {iso.unit}")] for k in wrong_counts(n)]
            stem = (f"สารกัมมันตรังสีชนิดหนึ่ง {_show(start)} {unit} สลายตัวจนเหลือ {_show(left)} {unit} "
                    f"ในเวลา {_show(t)} {iso.unit} สารนี้มีครึ่งชีวิตเท่าใด")
        else:
            decayed = start - left
            correct, wrongs = _amount_choices(decayed, [left, start / 2, start - start / (n + 1), decayed / 2], unit)
            stem = (f"{iso.name} มีครึ่งชีวิต {_show(T)} {iso.unit} ถ้าเริ่มต้นมี {_show(start)} {unit} "
                    f"เมื่อเวลาผ่านไป {_show(t)} {iso.unit} สารนี้สลายตัวไปแล้วกี่{unit}")
        return GeneratedQuestion(stem=[text(stem)], correct=correct, distractors=fixed(*wrongs),
                                 topic=TOPIC_DECAY, hint=hint)


@question_type(
    "chem.radioactive_decay_application",
    display_name={"th": "ใช้ครึ่งชีวิตหาอายุวัตถุโบราณ ปริมาณยา และเวลาเก็บกากกัมมันตรังสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DECAY,
)
class RadioactiveDecayApplication(QuestionType):
    """Half-life at work: dating, a dose after treatment, storing waste, and
    choosing between two isotopes."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    FRACTIONS = {1: "ครึ่งหนึ่ง", 2: "หนึ่งในสี่", 3: "หนึ่งในแปด", 4: "หนึ่งในสิบหก", 5: "หนึ่งในสามสิบสอง"}

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        n = rng.randint(1, 5)
        if shape < 0.3:
            c14 = next(i for i in ISOTOPES if i.name == "คาร์บอน-14")
            thing = rng.choice(("ซากไม้", "กระดูกสัตว์", "เมล็ดข้าวที่ขุดพบ", "ผ้าโบราณ"))
            age = c14.half_life * n
            wrongs = [c14.half_life * k for k in wrong_counts(n)]
            return GeneratedQuestion(
                stem=[text(f"{thing}ชิ้นหนึ่งมีคาร์บอน-14 เหลืออยู่{self.FRACTIONS[n]}ของที่พบในสิ่งมีชีวิตปัจจุบัน "
                           f"ถ้าคาร์บอน-14 มีครึ่งชีวิต {_show(c14.half_life)} ปี {thing}นี้มีอายุประมาณกี่ปี")],
                correct=[text(f"{_show(age)} ปี")],
                distractors=fixed(*[[text(f"{_show(w)} ปี")] for w in wrongs]),
                topic=TOPIC_DECAY,
                hint=[text("หาว่าปริมาณลดลงครึ่งหนึ่งกี่ครั้ง แล้วคูณด้วยครึ่งชีวิต")],
            )
        if shape < 0.55:
            iso = rng.choice([i for i in ISOTOPES if i.name in MEDICAL])
            left = Fraction(rng.randint(1, 10))
            start = left * 2 ** n
            unit = rng.choice(("มิลลิกรัม", "ไมโครกรัม"))
            correct, wrongs = _amount_choices(left, [start - left, start / (n + 1), left * 2, left / 2], unit)
            return GeneratedQuestion(
                stem=[text(f"ผู้ป่วยได้รับ{iso.name} {_show(start)} {unit} เพื่อ{iso.use} "
                           f"{iso.name}มีครึ่งชีวิต {_show(iso.half_life)} {iso.unit} "
                           f"หลังจากนั้น {_show(iso.half_life * n)} {iso.unit} "
                           f"จะเหลือ{iso.name}ในร่างกายกี่{unit} (ไม่คิดส่วนที่ขับออกจากร่างกาย)")],
                correct=correct, distractors=fixed(*wrongs),
                topic=TOPIC_DECAY,
                hint=[text("นับจำนวนครึ่งชีวิตที่ผ่านไป แล้วหารปริมาณเริ่มต้นด้วย 2 ทีละครั้ง")],
            )
        if shape < 0.8:
            iso = rng.choice(ISOTOPES)
            target = 2 ** n
            t = iso.half_life * n
            # Taking 1/16 to mean sixteen half-lives is the mistake worth offering.
            counts = [target] if target != n else []
            counts += [k for k in wrong_counts(n) if k not in counts]
            wrongs = [iso.half_life * k for k in counts[:3]]
            return GeneratedQuestion(
                stem=[text(f"กากสารกัมมันตรังสีที่มี{iso.name} (ครึ่งชีวิต {_show(iso.half_life)} {iso.unit}) "
                           f"ต้องเก็บไว้จนปริมาณเหลือ 1/{target} ของปริมาณเดิม ต้องเก็บไว้อย่างน้อยนานเท่าใด")],
                correct=[text(f"{_show(t)} {iso.unit}")],
                distractors=fixed(*[[text(f"{_show(w)} {iso.unit}")] for w in wrongs]),
                topic=TOPIC_DECAY,
                hint=[text(f"1/{target} คือการลดลงครึ่งหนึ่งติดต่อกันกี่ครั้ง นับแล้วคูณด้วยครึ่งชีวิต")],
            )
        # Two isotopes, the same start and the same wait: which has more left?
        a, b = rng.sample([i for i in ISOTOPES if i.unit == "วัน"], 2)
        days = rng.choice((8, 14, 16, 28, 30))
        longer = a if a.half_life > b.half_life else b
        return _labelled(
            stem=(f"เริ่มต้นมี{a.name} (ครึ่งชีวิต {_show(a.half_life)} วัน) และ{b.name} "
                  f"(ครึ่งชีวิต {_show(b.half_life)} วัน) อย่างละ 100 กรัม เมื่อเวลาผ่านไป {days} วัน "
                  "ข้อใดถูกต้อง"),
            correct=f"{longer.name}เหลืออยู่มากกว่า เพราะมีครึ่งชีวิตยาวกว่า",
            wrongs=(f"{(b if longer == a else a).name}เหลืออยู่มากกว่า เพราะมีครึ่งชีวิตสั้นกว่า",
                    "เหลืออยู่เท่ากัน เพราะเริ่มต้นมีปริมาณเท่ากัน",
                    "สลายตัวหมดทั้งคู่ เพราะเวลาผ่านไปนานกว่าครึ่งชีวิต"),
            topic=TOPIC_DECAY,
            hint="ครึ่งชีวิตยาวหมายถึงสลายตัวช้า ในเวลาเท่ากันจึงเหลืออยู่มากกว่า",
        )

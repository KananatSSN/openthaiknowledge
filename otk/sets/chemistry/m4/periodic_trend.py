"""แนวโน้มสมบัติของธาตุเรพรีเซนเททีฟ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/5

Sets moved here from: science_wave_f19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f19 import REPRESENTATIVE, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_TREND = "แนวโน้มสมบัติของธาตุเรพรีเซนเททีฟ"


def _label(element) -> str:
    return f"{element[2]} ({element[1]})"


# Each property: (name, larger down a group?, larger across a period to the right?)
TRENDS = (
    ("ขนาดอะตอม", True, False),
    ("พลังงานไอออไนเซชันลำดับที่ 1", False, True),
    ("ค่าอิเล็กโทรเนกาติวิตี", False, True),
    ("ความเป็นโลหะ", True, False),
)


TREND_FACTS = (
    ("ธาตุในหมู่เดียวกัน เมื่อเลขอะตอมเพิ่มขึ้น ขนาดอะตอมเป็นอย่างไร", "ใหญ่ขึ้น เพราะจำนวนระดับพลังงานเพิ่มขึ้น",
     ("เล็กลง เพราะประจุนิวเคลียสเพิ่มขึ้น", "เท่าเดิม", "ไม่มีแนวโน้มแน่นอน")),
    ("ธาตุในคาบเดียวกันจากซ้ายไปขวา ขนาดอะตอมเป็นอย่างไร", "เล็กลง เพราะประจุนิวเคลียสที่ดึงอิเล็กตรอนเพิ่มขึ้น",
     ("ใหญ่ขึ้น เพราะอิเล็กตรอนเพิ่มขึ้น", "เท่าเดิม", "ใหญ่ขึ้นแล้วเล็กลง")),
    ("ไอออนบวกมีขนาดเทียบกับอะตอมเดิมอย่างไร", "เล็กกว่า เพราะเสียอิเล็กตรอนไป",
     ("ใหญ่กว่า", "เท่ากัน", "ใหญ่กว่าเฉพาะโลหะหมู่ 1")),
    ("ไอออนลบมีขนาดเทียบกับอะตอมเดิมอย่างไร", "ใหญ่กว่า เพราะอิเล็กตรอนเพิ่มขึ้นและผลักกันมากขึ้น",
     ("เล็กกว่า", "เท่ากัน", "เล็กกว่าเฉพาะฮาโลเจน")),
    ("ธาตุในหมู่ 17 เมื่อเลขอะตอมเพิ่มขึ้น ความว่องไวในการเกิดปฏิกิริยาเป็นอย่างไร", "ลดลง",
     ("เพิ่มขึ้น", "เท่าเดิม", "เป็นศูนย์")),
    ("ธาตุในหมู่ 1 เมื่อเลขอะตอมเพิ่มขึ้น ความว่องไวในการเกิดปฏิกิริยาเป็นอย่างไร", "เพิ่มขึ้น",
     ("ลดลง", "เท่าเดิม", "เป็นศูนย์")),
)


def _larger(a, b, prop) -> bool | None:
    """Whether a has the larger value of prop, or None when position alone cannot tell."""
    _, down, right = prop
    if a[4] == b[4] and a[3] != b[3]:
        return (a[3] > b[3]) == down
    if a[3] == b[3] and a[4] != b[4]:
        return (a[4] > b[4]) == right
    return None


@question_type(
    "chem.periodic_trend_foundation",
    display_name={"th": "แนวโน้มขนาดอะตอม พลังงานไอออไนเซชัน และอิเล็กโทรเนกาติวิตี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TREND,
)
class PeriodicTrendFoundation(QuestionType):
    """The rules down a group and across a period."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            # Isoelectronic ions: more protons pull the same electrons in tighter.
            series = rng.choice(((("N", 7, -3), ("O", 8, -2), ("F", 9, -1), ("Na", 11, 1), ("Mg", 12, 2), ("Al", 13, 3)),
                                 (("P", 15, -3), ("S", 16, -2), ("Cl", 17, -1), ("K", 19, 1), ("Ca", 20, 2))))
            three = rng.sample(series, 3)
            biggest = rng.random() < 0.5
            pick = min(three, key=lambda t: t[1]) if biggest else max(three, key=lambda t: t[1])
            ion = lambda t: t[0] + (("" if abs(t[2]) == 1 else str(abs(t[2]))) + ("+" if t[2] > 0 else "-")).translate(
                str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"))
            return _labelled(
                stem=(f"ไอออน {' '.join(ion(t) + f' (Z = {t[1]})' for t in three)} มีจำนวนอิเล็กตรอนเท่ากัน "
                      f"ไอออนใดมีขนาด{'ใหญ่' if biggest else 'เล็ก'}ที่สุด"),
                correct=ion(pick), wrongs=tuple(ion(t) for t in three if t is not pick) + ("ขนาดเท่ากันทั้งสาม",),
                topic=TOPIC_TREND, hint="ไอออนที่มีอิเล็กตรอนเท่ากัน ตัวที่มีโปรตอนมากกว่าดึงอิเล็กตรอนแน่นกว่า จึงเล็กกว่า")
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(TREND_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_TREND,
                             hint="ลงตามหมู่: เพิ่มระดับพลังงาน อะตอมใหญ่ขึ้น ไปทางขวาของคาบ: ประจุนิวเคลียสเพิ่ม อะตอมเล็กลง")
        prop = rng.choice(TRENDS)
        way = rng.choice(("down", "right"))
        grows = prop[1] if way == "down" else prop[2]
        return _labelled(
            stem=f"{'ธาตุในหมู่เดียวกันจากบนลงล่าง' if way == 'down' else 'ธาตุในคาบเดียวกันจากซ้ายไปขวา'} {prop[0]}มีแนวโน้มอย่างไร",
            correct="เพิ่มขึ้น" if grows else "ลดลง", wrongs=("ลดลง" if grows else "เพิ่มขึ้น", "คงที่", "ไม่มีแนวโน้ม"),
            topic=TOPIC_TREND, hint="ขนาดอะตอมและความเป็นโลหะเพิ่มลงตามหมู่ ส่วน IE และ EN เพิ่มไปทางขวาของคาบ")


@question_type(
    "chem.periodic_trend_fluency",
    display_name={"th": "เปรียบเทียบสมบัติของธาตุสองธาตุจากตำแหน่งในตารางธาตุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TREND,
)
class PeriodicTrendFluency(QuestionType):
    """Two elements in one group or one period: which has more of the property."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        prop = rng.choice(TRENDS)
        a, b = rng.choice([(x, y) for x in REPRESENTATIVE for y in REPRESENTATIVE
                           if x != y and _larger(x, y, prop) is not None])
        winner = a if _larger(a, b, prop) else b
        loser = b if winner is a else a
        return _labelled(
            stem=f"ระหว่าง{_label(a)} (หมู่ {a[4]} คาบ {a[3]}) กับ{_label(b)} (หมู่ {b[4]} คาบ {b[3]}) ธาตุใดมี{prop[0]}มากกว่า",
            correct=_label(winner), wrongs=(_label(loser), "เท่ากัน", "บอกไม่ได้จากตำแหน่งในตารางธาตุ"),
            topic=TOPIC_TREND, hint="ดูว่าทั้งสองอยู่หมู่เดียวกัน (เทียบคาบ) หรือคาบเดียวกัน (เทียบหมู่) แล้วใช้แนวโน้ม")


@question_type(
    "chem.periodic_trend_application",
    display_name={"th": "เรียงลำดับสมบัติของธาตุในหมู่หรือคาบเดียวกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TREND,
)
class PeriodicTrendApplication(QuestionType):
    """Put three elements of one group or period in increasing order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        prop = rng.choice(TRENDS)
        if rng.random() < 0.5:
            group = rng.choice((1, 2, 17))
            pool = [e for e in REPRESENTATIVE if e[4] == group]
            key = lambda e: e[3] if prop[1] else -e[3]
        else:
            period = rng.choice((2, 3, 4))
            pool = [e for e in REPRESENTATIVE if e[3] == period]
            key = lambda e: e[4] if prop[2] else -e[4]
        three = rng.sample(pool, 3)
        ordered = sorted(three, key=key)
        right = " < ".join(e[1] for e in ordered)
        wrongs = set()
        while len(wrongs) < 3:
            shuffled = three[:]
            rng.shuffle(shuffled)
            text = " < ".join(e[1] for e in shuffled)
            if text != right:
                wrongs.add(text)
        listed = " ".join(f"{e[1]} (หมู่ {e[4]} คาบ {e[3]})" for e in three)
        return _labelled(stem=f"เรียงลำดับ{prop[0]}ของธาตุ {listed} จากน้อยไปมาก", correct=right,
                         wrongs=tuple(sorted(wrongs)), topic=TOPIC_TREND,
                         hint="ขนาดอะตอมและความเป็นโลหะเพิ่มลงตามหมู่และลดไปทางขวา IE และ EN กลับกัน")

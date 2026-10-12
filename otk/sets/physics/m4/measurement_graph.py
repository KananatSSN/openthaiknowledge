"""การวัด ความคลาดเคลื่อน และการวิเคราะห์กราฟเส้นตรง

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/2

Sets moved here from: science_wave_f6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f6 import SUBJECT, UPPER_FOUR, _exact

PROVENANCE = Provenance("original")


TOPIC_MEASURE = "การวัด ความคลาดเคลื่อน และการวิเคราะห์กราฟเส้นตรง"


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


PREFIXES = (("k", "กิโล", 3), ("M", "เมกะ", 6), ("G", "จิกะ", 9), ("c", "เซนติ", -2),
            ("m", "มิลลิ", -3), ("µ", "ไมโคร", -6), ("n", "นาโน", -9))


UNITS = (("m", "เมตร"), ("g", "กรัม"), ("s", "วินาที"), ("Hz", "เฮิรตซ์"), ("W", "วัตต์"))


def _power(value: int, exponent: int) -> str:
    return f"{value} × 10{str(exponent).translate(SUPERSCRIPT)}"


def _figures(rng: Random) -> tuple[str, int]:
    """A reading and its significant-figure count, never ambiguous about zeros."""
    n = rng.randint(1, 5)
    digits = str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(n - 1))
    form = rng.randrange(3)
    if form == 0:
        # Leading zeros only place the point.
        return "0." + "0" * rng.randint(0, 3) + digits, n
    if n == 1:
        return digits, n
    # A decimal point in the reading makes every trailing zero count.
    cut = 1 if form == 1 else rng.randint(1, n - 1)
    return digits[:cut] + "." + digits[cut:], n


GRAPHS = (
    # (y, y unit, x, x unit, what the slope is, slope unit)
    ("แรงที่ดึงสปริง", "N", "ระยะยืดของสปริง", "m", "ค่านิจของสปริง", "N/m"),
    ("ความเร็ว", "m/s", "เวลา", "s", "ความเร่ง", "m/s²"),
    ("ความต่างศักย์", "V", "กระแสไฟฟ้า", "A", "ความต้านทาน", "Ω"),
    ("มวล", "g", "ปริมาตร", "cm³", "ความหนาแน่น", "g/cm³"),
    ("ตำแหน่ง", "m", "เวลา", "s", "ความเร็ว", "m/s"),
)


@question_type(
    "phys.measurement_graph_foundation",
    display_name={"th": "เลขนัยสำคัญและคำอุปสรรคของหน่วย SI"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MEASURE,
)
class MeasurementGraphFoundation(QuestionType):
    """Counting significant figures, and turning a prefix into a power of ten."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            reading, count = _figures(rng)
            wrongs = [c for c in (len(reading.replace(".", "")), count + 1, count - 1, count + 2, count + 3)
                      if c > 0 and c != count]
            wrongs = list(dict.fromkeys(wrongs))[:3]
            unit = rng.choice(("cm", "m", "kg", "s", "N"))
            return _labelled(stem=f"ค่าที่วัดได้ {reading} {unit} มีเลขนัยสำคัญกี่ตัว",
                             correct=f"{count} ตัว", wrongs=tuple(f"{w} ตัว" for w in wrongs),
                             topic=TOPIC_MEASURE,
                             hint="เลขศูนย์หน้าตัวเลขแรกที่ไม่ใช่ศูนย์ไม่นับ ศูนย์ระหว่างตัวเลขและศูนย์ท้ายหลังจุดทศนิยมนับ")
        symbol, name, exponent = rng.choice(PREFIXES)
        unit, _ = rng.choice(UNITS)
        if unit == "g" and symbol in ("M", "G"):
            unit = "W"
        value = rng.randint(1, 9) * rng.choice((1, 1, 10, 100)) + rng.choice((0, 0, rng.randint(1, 9)))
        base = unit
        wrong_exponents = [e for e in (-exponent, exponent + 3, exponent - 3, exponent + 1, exponent - 1)
                           if e != exponent]
        return _labelled(
            stem=f"{value} {symbol}{unit} ({name}) เท่ากับกี่ {base}",
            correct=f"{_power(value, exponent)} {base}",
            wrongs=tuple(f"{_power(value, e)} {base}" for e in wrong_exponents[:3]),
            topic=TOPIC_MEASURE,
            hint="กิโล = 10³ เมกะ = 10⁶ จิกะ = 10⁹ เซนติ = 10⁻² มิลลิ = 10⁻³ ไมโคร = 10⁻⁶ นาโน = 10⁻⁹")


@question_type(
    "phys.measurement_graph_fluency",
    display_name={"th": "รายงานผลการวัดพร้อมความคลาดเคลื่อน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MEASURE,
)
class MeasurementGraphFluency(QuestionType):
    """Adding readings with their uncertainties, percentage uncertainty, and percent error."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            a = Fraction(rng.randint(100, 900), 10)
            b = Fraction(rng.randint(100, 900), 10)
            da, db = (Fraction(rng.randint(1, 5), 10) for _ in range(2))
            if da == db:
                db += Fraction(1, 10)
            add = rng.random() < 0.5
            total = a + b if add else abs(a - b)
            return _labelled(
                stem=(f"วัดความยาวได้ ({show(a)} ± {show(da)}) cm และ ({show(b)} ± {show(db)}) cm "
                      f"{'ผลรวม' if add else 'ผลต่าง'}ของความยาวทั้งสองควรรายงานอย่างไร"),
                correct=f"({show(total)} ± {show(da + db)}) cm",
                wrongs=(f"({show(total)} ± {show(abs(da - db))}) cm", f"({show(total)} ± {show(max(da, db))}) cm",
                        f"({show(a + b if not add else abs(a - b))} ± {show(da + db)}) cm"),
                topic=TOPIC_MEASURE,
                hint="เมื่อบวกหรือลบปริมาณ ความคลาดเคลื่อนสัมบูรณ์นำมาบวกกันเสมอ")
        if shape == 1:
            p1, p2 = rng.choice((1, 2, 4, 5)), rng.choice((1, 2, 3, 5))
            length = rng.choice([x for x in range(20, 201, 10) if _exact(Fraction(x * p1, 100))])
            width = rng.choice([x for x in range(10, 101, 10) if _exact(Fraction(x * p2, 100))])
            return numeric(
                stem=(f"วัดด้านของแผ่นไม้ได้ ({length} ± {show(Fraction(length * p1, 100))}) cm และ "
                      f"({width} ± {show(Fraction(width * p2, 100))}) cm พื้นที่ของแผ่นไม้มีความคลาดเคลื่อนร้อยละเท่าใด"),
                answer=p1 + p2, wrongs=[p1 * p2, abs(p1 - p2) or p1 + p2 + 1, Fraction(p1 + p2, 2)],
                unit="%", topic=TOPIC_MEASURE,
                hint="เมื่อคูณหรือหารปริมาณ ความคลาดเคลื่อนร้อยละ (ความคลาดเคลื่อน ÷ ค่าที่วัด × 100) นำมาบวกกัน")
        standard, what, unit = rng.choice(((340, "อัตราเร็วเสียงในอากาศ", "m/s"), (1000, "ความหนาแน่นของน้ำ", "kg/m³"),
                                           (200, "ความยาวของโต๊ะ", "cm"), (500, "มวลของตุ้มน้ำหนักมาตรฐาน", "g"),
                                           (250, "ปริมาตรของขวดมาตรฐาน", "mL")))
        pct = rng.choice([p for p in (1, 2, 3, 4, 5, 6, 8, 10) if _exact(Fraction(standard * p, 100))])
        measured = standard * (1 + Fraction(pct, 100) * rng.choice((1, -1)))
        return numeric(
            stem=(f"{what}มีค่ามาตรฐาน {standard:,} {unit} นักเรียนทดลองวัดได้ {show(measured)} {unit} "
                  "ความคลาดเคลื่อนร้อยละเท่าใด"),
            answer=pct, wrongs=[abs(measured - standard), pct * 2, Fraction(pct, 2)], unit="%", topic=TOPIC_MEASURE,
            hint="ความคลาดเคลื่อนร้อยละ = |ค่าที่วัด − ค่ามาตรฐาน| ÷ ค่ามาตรฐาน × 100")


@question_type(
    "phys.measurement_graph_application",
    display_name={"th": "วิเคราะห์และแปลความหมายกราฟเส้นตรงจากผลการทดลอง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MEASURE,
)
class MeasurementGraphApplication(QuestionType):
    """Slope and intercept of an experiment's straight line, and what each means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        y, yu, x, xu, meaning, su = rng.choice(GRAPHS)
        shape = rng.randrange(3)
        if shape == 2:
            return _labelled(
                stem=f"กราฟเส้นตรงระหว่าง{y} ({yu}) บนแกนตั้ง กับ{x} ({xu}) บนแกนนอน ความชันของกราฟบอกปริมาณใด",
                correct=meaning,
                wrongs=tuple([m for _, _, _, _, m, _ in GRAPHS if m != meaning]),
                topic=TOPIC_MEASURE, hint="ความชัน = การเปลี่ยนแปลงของแกนตั้ง ÷ การเปลี่ยนแปลงของแกนนอน ดูหน่วยประกอบ")
        slope = Fraction(rng.randint(1, 40), rng.choice((1, 2, 4, 5, 10)))
        intercept = rng.randint(1, 20) if meaning in ("ความเร่ง", "ความเร็ว") else 0
        x1 = rng.randint(1, 5)
        x2 = x1 + rng.randint(2, 8)
        y1, y2 = slope * x1 + intercept, slope * x2 + intercept
        if shape == 0 or intercept == 0:
            return numeric(
                stem=(f"กราฟเส้นตรงระหว่าง{y}กับ{x} ผ่านจุด ({x1} {xu}, {show(y1)} {yu}) และ ({x2} {xu}, {show(y2)} {yu}) "
                      f"{meaning}มีค่าเท่าใด"),
                # Reading one point instead of a change, the slope upside down, and the rise alone.
                answer=slope, wrongs=[Fraction(y2) / x2, Fraction(x2 - x1) / (y2 - y1), y2 - y1, (y2 - y1) / 2],
                unit=su, topic=TOPIC_MEASURE,
                hint="ความชัน = (y₂ − y₁) ÷ (x₂ − x₁) ความชันของกราฟนี้คือ" + meaning)
        start = "ความเร็วต้น" if meaning == "ความเร่ง" else "ตำแหน่งเริ่มต้น"
        return numeric(
            stem=(f"กราฟเส้นตรงระหว่าง{y}กับ{x} ผ่านจุด ({x1} {xu}, {show(y1)} {yu}) และ ({x2} {xu}, {show(y2)} {yu}) "
                  f"{start} (ค่าที่ {x} = 0) เท่าใด"),
            answer=intercept, wrongs=[y1, slope, y1 - slope * (x1 - 1) if x1 > 1 else y1 + slope],
            unit=yu, topic=TOPIC_MEASURE,
            hint="หาความชันก่อน แล้วค่าตัดแกนตั้ง = y₁ − ความชัน × x₁")

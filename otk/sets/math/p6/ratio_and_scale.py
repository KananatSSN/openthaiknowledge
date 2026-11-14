"""อัตราส่วนและมาตราส่วน

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_gaps_indicators, math_p6.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_RATIO_PAIRS = (
    ("นักเรียนชาย", "นักเรียนหญิง", "คน", "นักเรียนทั้งหมด"),
    ("ดินสอ", "ปากกา", "แท่ง", "เครื่องเขียนทั้งหมด"),
    ("ส้ม", "มะม่วง", "ผล", "ผลไม้ทั้งหมด"),
    ("ไก่", "เป็ด", "ตัว", "สัตว์ทั้งหมด"),
    ("ลูกแก้วสีแดง", "ลูกแก้วสีฟ้า", "ลูก", "ลูกแก้วทั้งหมด"),
)


_RATIO_TOPIC = "อัตราส่วนและมาตราส่วน"


@question_type("math.write_ratio_p6", display_name={"th": "เขียนอัตราส่วนจากสถานการณ์"},
               level={"th": "ป.6"}, topic="อัตราส่วนและมาตราส่วน")
class WriteRatioP6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        x, y, unit, whole = rng.choice(_RATIO_PAIRS)
        while True:
            a, b = rng.randint(2, 15), rng.randint(2, 15)
            if a != b and math.gcd(a, b) == 1:
                break
        stem_start = f"มี{x} {a} {unit} และ{y} {b} {unit}"
        asks = [
            (f"อัตราส่วนของจำนวน{x}ต่อจำนวน{y}", f"{a} : {b}"),
            (f"อัตราส่วนของจำนวน{y}ต่อจำนวน{x}", f"{b} : {a}"),
            (f"อัตราส่วนของจำนวน{x}ต่อจำนวน{whole}", f"{a} : {a + b}"),
            (f"อัตราส่วนของจำนวน{whole}ต่อจำนวน{y}", f"{a + b} : {b}"),
        ]
        ask, right = rng.choice(asks)
        # The other orders and the other part–whole pairs. a and b are
        # coprime and different, so no two are the same ratio.
        wrongs = [r for _, r in asks if r != right] + [f"{b} : {a + b}", f"{a + b} : {a}"]
        rng.shuffle(wrongs)
        flipped = right.split(" : ")[::-1]
        wrongs.insert(0, " : ".join(flipped))
        return _choices([text(f"{stem_start} {ask}เขียนได้อย่างไร")], right, wrongs, self.topic)


@question_type("math.equivalent_ratio_p6",
               display_name={"th": "อัตราส่วนที่เท่ากัน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class EquivalentRatioP6(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.sample(range(1, 10), 2)
        k = rng.randint(2, 9)
        sq = r"\square"
        prompt = rng.choice(("จงหาจำนวนที่ทำให้อัตราส่วนเท่ากัน",
                             "ผสมน้ำหวานกับน้ำ (ช้อน : แก้ว) ในอัตราส่วนเดิมทุกครั้ง จงหาจำนวนแทน □",
                             "แผนที่กับระยะจริง (ซม. : กม.) เป็นอัตราส่วนเดียวกัน จงหาจำนวนแทน □"))
        if rng.random() < 0.5:
            return MathDraw(rf"{a} : {b} = {a * k} : {sq}", str(b * k),
                            prompt=prompt,
                            # Adding the same amount instead of multiplying.
                            distractors=_story.keep(b + a * k - a, a * k, b * k + b, b + k,
                                                    answer=b * k, lo=1))
        return MathDraw(rf"{a * k} : {b * k} = {sq} : {b}", str(a),
                        prompt=prompt,
                        distractors=_story.keep(a * k - b * k + b if a * k - b * k + b > 0 else a + b,
                                                a * k, k, a + 1, answer=a, lo=1))


@question_type("math.map_scale",
               display_name={"th": "มาตราส่วน (ระยะจริง)"}, level={"th": "ป.6"},
               topic="อัตราส่วนและมาตราส่วน")
class MapScale(WordProblem):
    def expr(self, rng: Random):
        back = rng.choice([100, 1000])
        map_len = rng.randint(2, 30)
        real = map_len * back                       # in centimetres
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"มาตราส่วน 1:{back} ระยะในแผนที่ {map_len} ซม. คิดเป็นระยะจริงกี่เซนติเมตร?",
            f"แผนที่ใช้มาตราส่วน 1:{back} ระยะจากบ้าน{p}ถึงโรงเรียนในแผนที่ยาว {map_len} ซม. "
            f"ระยะจริงยาวกี่เซนติเมตร",
            f"แบบแปลนบ้านใช้มาตราส่วน 1:{back} ผนังห้องหนึ่งในแบบแปลนยาว {map_len} ซม. "
            f"ผนังจริงยาวกี่เซนติเมตร",
        ))
        return MathDraw("", str(real), prompt=prompt,
                        distractors=[str(map_len), str(real // 10), str(real * 10)])


@question_type("math.ratio_word_problem_p6",
               display_name={"th": "โจทย์ปัญหาอัตราส่วน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class RatioWordProblemP6(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.sample(range(1, 10), 2)
        k = rng.randint(2, 12)
        kind = rng.randrange(6)
        if kind == 3:
            return MathDraw("", str(a * k),
                            prompt=(f"สูตรผสมปูนใช้ปูนซีเมนต์ต่อทรายในอัตราส่วน {a} : {b} ถ้าใช้ทราย {b * k} ถัง "
                                    f"ต้องใช้ปูนซีเมนต์กี่ถัง"),
                            distractors=_story.keep(b * k, a * b * k, a + k, answer=a * k, lo=1))
        if kind == 4:
            return MathDraw("", str((a + b) * k),
                            prompt=(f"อัตราส่วนของนักเรียนชายต่อนักเรียนหญิงเป็น {a} : {b} ถ้ามีนักเรียนหญิง "
                                    f"{b * k} คน มีนักเรียนทั้งหมดกี่คน"),
                            distractors=_story.keep(a * k, b * k + a, (a + b) * b * k, answer=(a + b) * k,
                                                    lo=1))
        if kind == 5:
            return MathDraw("", str(a * k),
                            prompt=(f"ขนมปัง {a} ก้อนใช้ไข่ {b} ฟอง ถ้าใช้ไข่ {b * k} ฟอง "
                                    f"จะทำขนมปังได้กี่ก้อน"),
                            distractors=_story.keep(b * k * a, b * k - b + a, a + k, answer=a * k, lo=1))
        if kind == 0:
            return MathDraw("", str(b * k),
                            prompt=(f"อัตราส่วนของจำนวนแมวต่อจำนวนสุนัขในสถานพักพิงสัตว์เป็น {a} : {b} "
                                    f"ถ้ามีแมว {a * k} ตัว จะมีสุนัขกี่ตัว"),
                            distractors=_story.keep(a * k + b - a if a * k + b - a > 0 else b + k,
                                                    a * b * k, b + k, answer=b * k, lo=1))
        if kind == 1:
            price = rng.randint(3, 25)
            return MathDraw("", str(b * price),
                            prompt=(f"ดินสอ {a} แท่ง ราคา {a * price} บาท อัตราส่วนจำนวนดินสอต่อราคา"
                                    f"คงที่ ดินสอ {b} แท่ง ราคากี่บาท"),
                            distractors=_story.keep(a * price + b - a if a * price + b > a else price,
                                                    a * b * price, price, answer=b * price, lo=1))
        return MathDraw("", str(a * k + b * k),
                        prompt=(f"อัตราส่วนของน้ำหวานต่อน้ำเปล่าเป็น {a} : {b} ถ้าใช้น้ำหวาน {a * k} "
                                f"มิลลิลิตร จะได้เครื่องดื่มทั้งหมดกี่มิลลิลิตร"),
                        distractors=_story.keep(b * k, a * k + b, (a + b) * k * a,
                                                answer=(a + b) * k, lo=1))


@question_type("math.ratio_share_p6",
               display_name={"th": "แบ่งตามอัตราส่วน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class RatioShareP6(WordProblem):
    def expr(self, rng: Random):
        p, q = _story.names(rng)
        a, b = rng.sample(range(1, 8), 2)
        while math.gcd(a, b) != 1:
            a, b = rng.sample(range(1, 8), 2)
        unit = rng.randint(5, 60) * 5
        total = (a + b) * unit
        kind = rng.randrange(3)
        if kind == 0:
            ans = a * unit
            prompt = (f"{p}และ{q}แบ่งเงิน {grouped(total)} บาท ในอัตราส่วน {a} : {b} "
                      f"{p}ได้เงินกี่บาท")
            wrongs = [total // a if total % a == 0 else b * unit, b * unit, total - a, unit]
        elif kind == 1:
            ans = b * unit
            prompt = (f"ห้องเรียนมีนักเรียน {total} คน อัตราส่วนนักเรียนชายต่อนักเรียนหญิงเป็น "
                      f"{a} : {b} มีนักเรียนหญิงกี่คน")
            wrongs = [a * unit, total // b if total % b == 0 else total - b, unit, total - b]
        else:
            ans = abs(a - b) * unit
            prompt = (f"ขนมชั้นใช้แป้งกับน้ำตาลในอัตราส่วน {a} : {b} ถ้าใช้ทั้งสองอย่างรวมกัน "
                      f"{total} กรัม ปริมาณของทั้งสองอย่างต่างกันกี่กรัม")
            wrongs = [a * unit, b * unit, abs(a - b), total - abs(a - b)]
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(*wrongs, ans + unit, answer=ans, lo=1))

from fractions import Fraction  # noqa: E402
from math import gcd  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More ratio and scale (2026-11): a real distance in kilometres, a map distance, a ratio in lowest terms,
# the other part from a ratio, and sharing in three parts ──


@question_type("math.scale_to_km_p6", display_name={"th": "มาตราส่วน (ระยะจริงเป็นกิโลเมตร)"},
               level=LEVEL, topic="อัตราส่วนและมาตราส่วน")
class ScaleToKmP6(WordProblem):
    def expr(self, rng: Random):
        km_per_cm = rng.choice((1, 2, 5, 10, 20))
        scale = km_per_cm * 100_000
        cm = rng.randint(2, 25)
        right = cm * km_per_cm
        prompt = f"แผนที่ใช้มาตราส่วน 1 : {scale:,} ระยะในแผนที่ {cm} เซนติเมตร คิดเป็นระยะจริงกี่กิโลเมตร"
        # Metres instead of kilometres; ten times off; the centimetres themselves.
        return MathDraw("", _g6(right), prompt=prompt,
                        distractors=_gk6(right * 1000, right * 10, cm, right + km_per_cm, answer=right, lo=1))


@question_type("math.scale_to_map_p6", display_name={"th": "มาตราส่วน (ระยะในแผนที่)"},
               level=LEVEL, topic="อัตราส่วนและมาตราส่วน")
class ScaleToMapP6(WordProblem):
    def expr(self, rng: Random):
        m_per_cm = rng.choice((10, 20, 50, 100, 200, 500))
        scale = m_per_cm * 100
        right = rng.randint(2, 20)
        metres = right * m_per_cm
        prompt = f"แบบแปลนใช้มาตราส่วน 1 : {scale:,} ระยะจริง {metres:,} เมตร ในแบบแปลนยาวกี่เซนติเมตร"
        # The scale in metres not centimetres; multiplied instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right * 100, right * 10, metres // 10 if metres >= 100 else right + 5,
                                                right + 1, answer=right, lo=1))


@question_type("math.ratio_lowest_terms_p6", display_name={"th": "อัตราส่วนอย่างต่ำ"},
               level=LEVEL, topic="อัตราส่วนและมาตราส่วน")
class RatioLowestTermsP6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            a, b = rng.sample(range(1, 10), 2)
            if gcd(a, b) == 1:
                break
        k = rng.randint(2, 9)
        right = f"{a} : {b}"
        # Not reduced all the way; the parts swapped; one part reduced only.
        half = f"{a * k // 2} : {b * k // 2}" if k % 2 == 0 and k > 2 else f"{a * k} : {b}"
        wrongs = [half, f"{b} : {a}", f"{a + 1} : {b + 1}"]
        return f"อัตราส่วน {a * k} : {b * k} เขียนเป็นอัตราส่วนอย่างต่ำได้อย่างไร", right, wrongs


@question_type("math.ratio_other_part_p6", display_name={"th": "หาอีกส่วนจากอัตราส่วน"},
               level=LEVEL, topic="อัตราส่วนและมาตราส่วน")
class RatioOtherPartP6(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b = rng.sample(range(1, 10), 2)
            if gcd(a, b) == 1:
                break
        k = rng.randint(2, 12)
        boys, right = a * k, b * k
        prompt = f"อัตราส่วนของนักเรียนชายต่อนักเรียนหญิงเป็น {a} : {b} ถ้ามีนักเรียนชาย {boys} คน มีนักเรียนหญิงกี่คน"
        # Everyone; the boys and the step added; the ratio read upside down.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(boys + right, boys + (b - a), boys * a // b if boys * a % b == 0 else boys + b,
                                                right + k, answer=right, lo=1))


@question_type("math.share_three_ways_p6", display_name={"th": "แบ่งตามอัตราส่วนสามส่วน"},
               level=LEVEL, topic="อัตราส่วนและมาตราส่วน")
class ShareThreeWaysP6(WordProblem):
    def expr(self, rng: Random):
        parts = rng.sample(range(1, 8), 3)
        unit = rng.randint(5, 80) * 10
        total = sum(parts) * unit
        i = rng.randrange(3)
        right = parts[i] * unit
        names = _story.names(rng, 3)
        ratio = " : ".join(str(p) for p in parts)
        prompt = f"แบ่งเงิน {total:,} บาท ให้{names[0]} {names[1]} และ{names[2]}ในอัตราส่วน {ratio} {names[i]}ได้เงินกี่บาท"
        # One part's worth; split three ways evenly; the part times the total over ten.
        return MathDraw("", _g6(right), prompt=prompt,
                        distractors=_gk6(unit, total // 3, total - right, right + unit, answer=right, lo=1))

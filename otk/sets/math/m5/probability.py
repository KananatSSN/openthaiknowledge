"""ความน่าจะเป็น

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/2

Sets moved here from: math, math_bank_probability, math_data, math_m5.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_m4 import maths as _maths_math_m5
from otk.sets._support.math_p2 import _maths

M6 = {"th": "ม.6"}


TOPIC = "ความน่าจะเป็น"


NL = chr(10)


def _choices(stem: list, p: Fraction, named: list[Fraction], topic: str) -> GeneratedQuestion:
    """A fraction answer with its named mistakes first, then padding.

    Only values strictly between 0 and 1 (or exactly 1) are offered. A
    probability outside that range gives itself away.
    """
    wrongs: list[str] = []
    right = frac_tex(p)
    pads = [p / 2, 1 - p, p * 2, p + Fraction(1, p.denominator), p - Fraction(1, p.denominator)]
    for w in [*named, *pads]:
        t = frac_tex(w)
        if 0 < w <= 1 and w != p and t not in wrongs:
            wrongs.append(t)
        if len(wrongs) == 3:
            break
    return _maths(stem, right, wrongs, topic)


def _decimal(v: Fraction) -> str:
    return f"{float(v):.2f}"


def divisible_either(n: int, a: int, b: int) -> Fraction:
    """P(a | k or b | k) for k drawn from 1..n: inclusion–exclusion."""
    lcm = a * b // math.gcd(a, b)
    return Fraction(n // a + n // b - n // lcm, n)


_TABLES = (
    ("จำนวนนักเรียนในแต่ละชมรม (คน)", "ชั้น", ("ม.4", "ม.5", "ม.6"),
     ("กีฬา", "ดนตรี", "วิทยาศาสตร์"), "นักเรียน", "คน"),
    ("จำนวนแบบฟอร์มชิงรางวัลที่ลูกค้าส่งมา (ใบ)", "สินค้า", ("โทรทัศน์", "ตู้เย็น", "เครื่องซักผ้า"),
     ("เชียงใหม่", "ภูเก็ต", "น่าน"), "แบบฟอร์ม", "ใบ"),
    ("จำนวนนักศึกษาจำแนกตามวันที่ออกกำลังกายต่อสัปดาห์ (คน)", "ระดับ", ("ปริญญาตรี", "ปริญญาโท"),
     ("น้อยกว่า 3 วัน", "3–5 วัน", "มากกว่า 5 วัน"), "นักศึกษา", "คน"),
)


def draw_sequence(counts: dict[str, int], seq: list[str]) -> Fraction:
    """P(the draws come out exactly as ``seq``), one at a time, no replacement."""
    left = dict(counts)
    n = sum(left.values())
    p = Fraction(1)
    for colour in seq:
        p *= Fraction(left[colour], n)
        left[colour] -= 1
        n -= 1
    return p


def digit_probability(digits: int, condition: str, k: int = 0) -> Fraction:
    """P(condition) for a number drawn from all ``digits``-digit numbers.

    ``condition``: ``all_odd``, ``even_product`` (product of digits is even),
    ``has_k`` (the digit k ≥ 1 appears at least once), ``distinct``.
    """
    total = 9 * 10 ** (digits - 1)
    if condition == "all_odd":
        good = 5 ** digits
    elif condition == "even_product":
        good = total - 5 ** digits
    elif condition == "has_k":
        good = total - 8 * 9 ** (digits - 1)
    elif condition == "distinct":
        good = 9 * math.perm(9, digits - 1)
    else:
        raise ValueError(condition)
    return Fraction(good, total)


def derangements(n: int) -> int:
    """Arrangements of n things with none in its own place: D(n) = (n−1)(D(n−1) + D(n−2))."""
    d = [1, 0]
    for k in range(2, n + 1):
        d.append((k - 1) * (d[-1] + d[-2]))
    return d[n]


def grouped_together(a: int, b: int) -> Fraction:
    """P(a things of one kind and b of another, in a random row, form two blocks)."""
    return Fraction(2 * math.factorial(a) * math.factorial(b), math.factorial(a + b))


def route_through(m: int, n: int, p: int, q: int) -> Fraction:
    """P(a uniformly random shortest grid route (0,0)→(m,n) passes (p,q))."""
    via = math.comb(p + q, p) * math.comb(m - p + n - q, m - p)
    return Fraction(via, math.comb(m + n, m))


@question_type("math.simple_probability",
               display_name={"th": "ความน่าจะเป็นเบื้องต้น"}, level={"th": "ม.3"},
               topic="ความน่าจะเป็น")
class SimpleProbability(WordProblem):
    def expr(self, rng: Random):
        while True:
            total = rng.randint(4, 12)
            fav = rng.randint(1, total - 1)
            if total != 2 * fav:                    # keep complement distinct
                break
        ans = frac_tex(Fraction(fav, total))
        prompt = rng.choice((
            f"สุ่มจาก {total} ผลลัพธ์ที่เท่ากัน มีเหตุการณ์ที่ต้องการ {fav} แบบ ความน่าจะเป็นเท่าใด?",
            f"ในกล่องมีสลาก {total} ใบ เป็นสลากที่มีรางวัล {fav} ใบ สุ่มหยิบ 1 ใบ "
            f"ความน่าจะเป็นที่จะได้รางวัลเท่าใด?",
            f"ห้องเรียนมีนักเรียน {total} คน ใส่แว่นตา {fav} คน สุ่มเรียกนักเรียน 1 คน "
            f"ความน่าจะเป็นที่จะได้คนใส่แว่นตาเท่าใด?",
            f"ถุงมีลูกอม {total} เม็ด เป็นรสส้ม {fav} เม็ด สุ่มหยิบ 1 เม็ด "
            f"ความน่าจะเป็นที่จะได้รสส้มเท่าใด?",
        ))
        return MathDraw(
            "", ans, prompt=prompt,
            distractors=[frac_tex(Fraction(total - fav, total)),
                         rf"\frac{{{total}}}{{{fav}}}",
                         rf"\frac{{{fav}}}{{{total - 1}}}"])
SimpleProbability.PROVENANCE = Provenance("original")


@question_type("math.probability_two_way_table_m5",
               display_name={"th": "ความน่าจะเป็นจากตารางสองทาง"},
               level=M6, topic=TOPIC)
class ProbabilityTwoWayTableM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        title, row_head, rows, cols, who, unit = rng.choice(_TABLES)
        cells = [[rng.randint(5, 60) for _ in cols] for _ in rows]
        total = sum(map(sum, cells))
        r, c = rng.randrange(len(rows)), rng.randrange(len(cols))
        cell = cells[r][c]
        row_sum = sum(cells[r])
        col_sum = sum(row[c] for row in cells)
        table = NL.join([f"ตารางแสดง{title}",
                         " | ".join([row_head, *cols]),
                         *(" | ".join([name, *map(str, vals)]) for name, vals in zip(rows, cells))])
        kind = rng.randrange(4)
        if kind == 0:
            ask = f"ความน่าจะเป็นที่จะได้{who}ที่อยู่ใน {rows[r]} และ {cols[c]}"
            p = Fraction(cell, total)
            named = [Fraction(cell, row_sum), Fraction(cell, col_sum), Fraction(col_sum, total)]
            pool = f"ถ้าสุ่ม{who}จากตารางนี้มา 1 {unit}"
        elif kind == 1:
            ask = f"ความน่าจะเป็นที่จะได้{who}ในกลุ่ม {cols[c]}"
            p = Fraction(col_sum, total)
            named = [Fraction(cell, total), Fraction(1, len(cols)), Fraction(col_sum, total - col_sum)]
            pool = f"ถ้าสุ่ม{who}จากตารางนี้มา 1 {unit}"
        elif kind == 2:
            # The sample space is one row only — the trap the O-NET item sets.
            ask = f"ความน่าจะเป็นที่จะได้{who}ในกลุ่ม {cols[c]}"
            p = Fraction(cell, row_sum)
            named = [Fraction(cell, total), Fraction(col_sum, total), Fraction(cell, col_sum)]
            pool = f"ถ้าสุ่ม{who}เฉพาะจาก {rows[r]} มา 1 {unit}"
        else:
            ask = f"ความน่าจะเป็นที่จะได้{who}ที่อยู่ใน {rows[r]} หรือ {cols[c]}"
            p = Fraction(row_sum + col_sum - cell, total)
            named = [Fraction(row_sum + col_sum, total), Fraction(cell, total), Fraction(row_sum, total)]
            pool = f"ถ้าสุ่ม{who}จากตารางนี้มา 1 {unit}"
        return _choices([text(table), text(f"{pool} {ask} เท่ากับเท่าใด")], p, named, self.topic)
ProbabilityTwoWayTableM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_complement",
               display_name={"th": "ความน่าจะเป็นของเหตุการณ์ตรงข้าม"},
               level={"th": "ม.3"}, topic="ความน่าจะเป็น")
class ProbabilityComplement(MathType):
    def expr(self, rng: Random, total_lo: int = 5, total_hi: int = 20):
        total = rng.randint(total_lo, total_hi)
        favourable = rng.randint(1, total - 1)
        p = Fraction(favourable, total)
        who = rng.choice(_story.NAMES)
        prompt = rng.choice((
            "ถ้าเหตุการณ์หนึ่งมีความน่าจะเป็นดังนี้ เหตุการณ์ตรงข้ามมีความน่าจะเป็นเท่าใด",
            "ความน่าจะเป็นที่ฝนจะตกในวันพรุ่งนี้เป็นดังนี้ ความน่าจะเป็นที่ฝนจะไม่ตกเป็นเท่าใด",
            f"ความน่าจะเป็นที่{who}จะยิงลูกโทษเข้าประตูเป็นดังนี้ "
            f"ความน่าจะเป็นที่{who}จะยิงไม่เข้าเป็นเท่าใด",
            "ความน่าจะเป็นที่จะจับสลากได้รางวัลเป็นดังนี้ ความน่าจะเป็นที่จะไม่ได้รางวัลเป็นเท่าใด",
        ))
        return MathDraw(
            frac_tex(p), frac_tex(1 - p), prompt=prompt,
            distractors=[frac_tex(p), frac_tex(1 / p) if p else "1",
                         frac_tex(Fraction(1, total))])
ProbabilityComplement.PROVENANCE = Provenance("original")


@question_type("math.probability",
               display_name={"th": "ความน่าจะเป็น (ลูกเต๋า, เหรียญ)"}, level={"th": "ม.6"},
               topic="ความน่าจะเป็น")
class Probability(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["two_dice", "coins", "one_die"])
        if kind == "two_dice":
            s = rng.randint(3, 11)
            p = Fraction(6 - abs(s - 7), 36)
            return MathDraw(rf"P(X = {s})", frac_tex(p),
                            prompt="ทอดลูกเต๋า 2 ลูก ให้ X เป็นผลรวมของแต้ม")
        if kind == "coins":
            n = rng.randint(2, 4)
            k = rng.randint(0, n)
            p = Fraction(math.comb(n, k), 2 ** n)
            return MathDraw(rf"P(X = {k})", frac_tex(p),
                            prompt=f"โยนเหรียญ {n} ครั้ง ให้ X เป็นจำนวนครั้งที่ออกหัว")
        k = rng.randint(2, 6)
        return MathDraw(rf"P(X \geq {k})", frac_tex(Fraction(7 - k, 6)),
                        prompt="ให้ X เป็นแต้มจากการทอดลูกเต๋า 1 ลูก")
Probability.PROVENANCE = Provenance("original")


@question_type("math.probability_union_m5",
               display_name={"th": "ความน่าจะเป็นของเหตุการณ์ A หรือ B"},
               level=M6, topic=TOPIC)
class ProbabilityUnionM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind in (0, 1):
            # Hundredths, so every value prints exactly.
            pa, pb = rng.randint(10, 60), rng.randint(10, 60)
            both = rng.randint(max(1, pa + pb - 95), min(pa, pb) - 1)
            either = pa + pb - both
            h = Fraction(1, 100)
            a, b, name = rng.choice((("เครื่อง A เสีย", "เครื่อง B เสีย", "เครื่องถ่ายเอกสาร"),
                                     ("ฝนตกในวันเสาร์", "ฝนตกในวันอาทิตย์", "พยากรณ์อากาศ"),
                                     ("นักเรียนชอบคณิตศาสตร์", "นักเรียนชอบวิทยาศาสตร์", "การสำรวจ")))
            given = (f"จากข้อมูล{name} ความน่าจะเป็นที่{a} เท่ากับ {_decimal(pa * h)} "
                     f"ความน่าจะเป็นที่{b} เท่ากับ {_decimal(pb * h)}")
            if kind == 0:
                stem = (given + f" และความน่าจะเป็นที่ทั้งสองเหตุการณ์เกิดขึ้นพร้อมกัน เท่ากับ "
                        f"{_decimal(both * h)} ความน่าจะเป็นที่{a}หรือ{b} (อย่างน้อยหนึ่งเหตุการณ์) เท่ากับเท่าใด")
                right = either
                # Adding without the overlap; exactly one of them; the product rule.
                named = [pa + pb, either - both, round(pa * pb / 100)]
            else:
                stem = (given + f" และความน่าจะเป็นที่{a}หรือ{b} เท่ากับ {_decimal(either * h)} "
                        f"ความน่าจะเป็นที่ทั้งสองเหตุการณ์ไม่เกิดขึ้นพร้อมกัน (อย่างน้อยหนึ่งเหตุการณ์ไม่เกิด) เท่ากับเท่าใด")
                right = 100 - both
                # 1 − P(A ∪ B) answers "neither"; P(A ∩ B) forgets the complement.
                named = [100 - either, both, 100 - pa * pb // 100]
            wrongs = []
            for w in named:
                if 0 < w < 100 and w != right and _decimal(w * h) not in wrongs:
                    wrongs.append(_decimal(w * h))
            for d in (5, -5, 10, -10):
                if len(wrongs) == 3:
                    break
                w = right + d
                if 0 < w < 100 and _decimal(w * h) not in wrongs:
                    wrongs.append(_decimal(w * h))
            return _maths([text(stem)], _decimal(right * h), wrongs, self.topic)

        if kind == 2:
            a, b = rng.sample((2, 3, 4, 5, 6, 7), 2)
            n = rng.choice((20, 24, 25, 30, 36, 40, 50, 60))
            p = divisible_either(n, a, b)
            lcm = a * b // math.gcd(a, b)
            stem = (f"สลาก {n} ใบ มีหมายเลข 1 ถึง {n} ใบละหนึ่งหมายเลข สุ่มหยิบสลาก 1 ใบ "
                    f"ความน่าจะเป็นที่จะได้หมายเลขที่หารด้วย {a} หรือ {b} ลงตัว เท่ากับเท่าใด")
            # Counting the common multiples twice; only one divisor; only the overlap.
            named = [Fraction(n // a + n // b, n), Fraction(n // a, n), Fraction(n // lcm, n)]
            return _choices([text(stem)], p, named, self.topic)

        total = rng.randint(30, 60)
        x = rng.randint(total // 3, total * 2 // 3)
        y = rng.randint(total // 4, total // 2)
        both = rng.randint(max(1, x + y - total + 2), min(x, y) - 1)
        neither = total - (x + y - both)
        p = Fraction(neither, total)
        who, unit, has_x, has_y = rng.choice((
            ("ครัวเรือน", "ครัวเรือน", "มีรถกระบะ", "มีจักรยานยนต์"),
            ("นักเรียน", "คน", "เรียนพิเศษคณิตศาสตร์", "เรียนพิเศษภาษาอังกฤษ"),
            ("ลูกค้า", "คน", "ใส่น้ำตาลในกาแฟ", "ใส่นมในกาแฟ")))
        stem = (f"จากการสำรวจ{who} {total} {unit} พบว่า {x} {unit}{has_x} "
                f"{y} {unit}{has_y} และ {both} {unit}{has_x}และ{has_y} "
                f"ถ้าสุ่ม{who}มา 1 {unit} ความน่าจะเป็นที่จะได้{who}ที่ไม่{has_x}และไม่{has_y} "
                f"เท่ากับเท่าใด")
        # Subtracting x and y without adding the overlap back; the overlap; A ∪ B itself.
        named = [Fraction(total - x - y, total), Fraction(both, total), Fraction(x + y - both, total)]
        return _choices([text(stem)], p, named, self.topic)
ProbabilityUnionM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_digit_numbers_m5",
               display_name={"th": "ความน่าจะเป็นของจำนวนที่มีเงื่อนไขของเลขโดด"},
               level=M6, topic=TOPIC)
class ProbabilityDigitNumbersM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        d = rng.choice((2, 3))
        lo, hi = 10 ** (d - 1), 10 ** d - 1
        total = hi - lo + 1
        cond = rng.choice(("all_odd", "even_product", "has_k", "distinct"))
        k = rng.randint(1, 9)
        p = digit_probability(d, cond, k)
        ask = {"all_odd": "เลขโดดทุกหลักเป็นจำนวนคี่",
               "even_product": "ผลคูณของเลขโดดทุกหลักเป็นจำนวนคู่",
               "has_k": f"มีเลขโดด {k} ปรากฏอย่างน้อยหนึ่งหลัก",
               "distinct": "เลขโดดทุกหลักแตกต่างกัน"}[cond]
        stem = (f"สุ่มจำนวนเต็มหนึ่งจำนวนจาก {lo}, {lo + 1}, {lo + 2}, …, {hi} "
                f"(ทุกจำนวนมีโอกาสเท่ากัน) ความน่าจะเป็นที่จำนวนนั้น{ask} เท่ากับเท่าใด")
        good = p * total
        # A leading zero allowed (10^d outcomes); the complement; one digit's chance.
        if cond == "all_odd":
            named = [Fraction(5 ** d, 10 ** d), 1 - p, Fraction(1, 2)]
        elif cond == "even_product":
            named = [1 - Fraction(5 ** d, 10 ** d), 1 - p, Fraction(1, 2)]
        elif cond == "has_k":
            named = [Fraction(d, 10), 1 - Fraction(9 ** d, 10 ** d), 1 - p]
        else:
            named = [Fraction(math.perm(10, d), 10 ** d), Fraction(math.perm(10, d), total), 1 - p]
        named = [w for w in named if w * total != good]
        return _choices([text(stem)], p, named, self.topic)
ProbabilityDigitNumbersM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_marbles", display_name={"th": "ความน่าจะเป็นจากการหยิบลูกแก้ว"},
               level={"th": "ม.3"}, topic="ความน่าจะเป็น")
class ProbabilityMarbles(WordProblem):
    _BAGS = (("ในถุงมีลูกแก้ว", "ลูก", ("สีแดง", "สีน้ำเงิน", "สีเขียว")),
             ("ในโหลมีลูกอม", "เม็ด", ("รสส้ม", "รสองุ่น", "รสมะนาว")),
             ("ในกล่องมีบัตร", "ใบ", ("สีเหลือง", "สีชมพู", "สีฟ้า")),
             ("ในตะกร้ามีผลไม้ ได้แก่", "ผล", ("ส้ม", "มังคุด", "เงาะ")),
             ("ในกล่องมีปากกา", "ด้าม", ("หมึกน้ำเงิน", "หมึกแดง", "หมึกดำ")))

    def expr(self, rng: Random, lo: int = 2, hi: int = 9):
        counts = [rng.randint(lo, hi) for _ in range(3)]
        total = sum(counts)
        where, unit, kinds = rng.choice(self._BAGS)
        i = rng.randrange(3)
        count = counts[i]
        listed = " ".join(f"{k} {c} {unit}" for k, c in zip(kinds, counts))
        return MathDraw(
            "", frac_tex(Fraction(count, total)),
            prompt=(f"{where}{listed} สุ่มหยิบ 1 {unit} "
                    f"ความน่าจะเป็นที่จะได้{kinds[i]}เป็นเท่าใด"),
            distractors=[frac_tex(Fraction(count, total - count)),
                         frac_tex(Fraction(total - count, total)),
                         frac_tex(Fraction(1, total))])
ProbabilityMarbles.PROVENANCE = Provenance("original")


@question_type("math.probability_two_dice", display_name={"th": "ความน่าจะเป็นจากลูกเต๋าสองลูก"},
               level={"th": "ม.6"}, topic="ความน่าจะเป็น")
class ProbabilityTwoDice(WordProblem):
    _EVENTS = (("แต้มเท่ากันทั้งสองลูก", lambda a, b: a == b),
               ("ผลคูณของแต้มเป็นจำนวนคู่", lambda a, b: a * b % 2 == 0),
               ("แต้มของลูกหนึ่งมากกว่าอีกลูก 2", lambda a, b: abs(a - b) == 2),
               ("ผลรวมแต้มมากกว่า 9", lambda a, b: a + b > 9),
               ("มีลูกใดลูกหนึ่งขึ้นแต้ม 6", lambda a, b: 6 in (a, b)))

    def expr(self, rng: Random, target_lo: int = 4, target_hi: int = 10):
        if rng.random() < 0.5:
            target = rng.randint(target_lo, target_hi)
            count = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == target)
            prompt = (f"ทอดลูกเต๋าสองลูกพร้อมกัน ความน่าจะเป็นที่ผลรวมแต้ม "
                      f"เท่ากับ {target} เป็นเท่าใด")
        else:
            name, test = rng.choice(self._EVENTS)
            count = sum(1 for a in range(1, 7) for b in range(1, 7) if test(a, b))
            prompt = f"ทอดลูกเต๋าสองลูกพร้อมกัน ความน่าจะเป็นที่{name}เป็นเท่าใด"
        return MathDraw(
            "", frac_tex(Fraction(count, 36)), prompt=prompt,
            # Twelve outcomes (6 + 6) instead of 36, one outcome, one miscounted.
            distractors=[frac_tex(Fraction(count, 12)) if count < 12 else frac_tex(Fraction(1, 2)),
                         frac_tex(Fraction(1, 36)), frac_tex(Fraction(count + 1, 36))])
ProbabilityTwoDice.PROVENANCE = Provenance("original")


@question_type("math.probability_without_replacement_m5",
               display_name={"th": "ความน่าจะเป็นของการหยิบทีละชิ้นแบบไม่ใส่คืน"},
               level=M6, topic=TOPIC)
class ProbabilityWithoutReplacementM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        colours = rng.sample(("แดง", "ขาว", "ฟ้า", "เหลือง", "เขียว"), 3)
        counts = {c: rng.randint(2, 8) for c in colours}
        n = sum(counts.values())
        box = " ".join(f"สี{c} {k} ลูก" for c, k in counts.items())
        x, y = colours[0], colours[1]
        kind = rng.randrange(4)
        if kind == 0:
            seq, ask = [x, y], f"ครั้งแรกได้สี{x} และครั้งที่สองได้สี{y}"
            p = draw_sequence(counts, seq)
            # With replacement; forgetting the order is fixed (×2); one draw only.
            named = [Fraction(counts[x] * counts[y], n * n), 2 * p, Fraction(counts[x], n)]
        elif kind == 1:
            seq, ask = [x, x], f"ได้สี{x}ทั้งสองครั้ง"
            p = draw_sequence(counts, seq)
            named = [Fraction(counts[x], n) ** 2, Fraction(counts[x], n),
                     Fraction(counts[x] - 1, n - 1)]
        elif kind == 2:
            ask = f"ได้สี{x} 1 ลูก และสี{y} 1 ลูก (ลำดับใดก็ได้)"
            p = draw_sequence(counts, [x, y]) + draw_sequence(counts, [y, x])
            # One order only; with replacement.
            named = [draw_sequence(counts, [x, y]), Fraction(2 * counts[x] * counts[y], n * n),
                     Fraction(counts[x] + counts[y], n)]
        else:
            seq, ask = [x, x, x], f"ได้สี{x}ทั้งสามครั้ง"
            if counts[x] < 3:
                counts[x] = 3
                n = sum(counts.values())
                box = " ".join(f"สี{c} {k} ลูก" for c, k in counts.items())
            p = draw_sequence(counts, seq)
            named = [Fraction(counts[x], n) ** 3, Fraction(counts[x], n),
                     Fraction(counts[x] - 2, n - 2)]
        times = 3 if kind == 3 else 2
        stem = (f"กล่องใบหนึ่งมีลูกบอล{box} สุ่มหยิบลูกบอลทีละลูก {times} ครั้ง "
                f"โดยไม่ใส่คืนก่อนหยิบครั้งถัดไป ความน่าจะเป็นที่{ask} เท่ากับเท่าใด")
        return _choices([text(stem)], p, named, self.topic)
ProbabilityWithoutReplacementM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_random_arrangement_m5",
               display_name={"th": "ความน่าจะเป็นของการจัดเรียงแบบสุ่ม"},
               level=M6, topic=TOPIC)
class ProbabilityRandomArrangementM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            n = rng.randint(3, 5)
            p = Fraction(derangements(n), math.factorial(n))
            stem = (f"นักเรียน {n} คน ฝากโทรศัพท์คนละเครื่องไว้ในตะกร้า แล้วแต่ละคนสุ่มหยิบโทรศัพท์คืนคนละ 1 เครื่อง "
                    f"ความน่าจะเป็นที่ไม่มีใครได้โทรศัพท์ของตัวเองเลย เท่ากับเท่าใด")
            # Everyone wrong one at a time ((n−1)/n)^n; exactly the one "all right" case; 1 − 1/n.
            named = [Fraction(n - 1, n) ** n, Fraction(1, math.factorial(n)), 1 - Fraction(1, n)]
        elif kind == 1:
            a, b = rng.randint(2, 4), rng.randint(2, 4)
            p = grouped_together(a, b)
            stem = (f"นำจาน {a} ใบ และชาม {b} ใบ ที่แตกต่างกันทั้งหมด มาวางเรียงเป็นแถวแบบสุ่ม "
                    f"ความน่าจะเป็นที่ภาชนะประเภทเดียวกันวางติดกันทั้งหมด เท่ากับเท่าใด")
            # Forgetting the two blocks can swap; forgetting the order inside each
            # block; one fixed position for the whole row. (Treating like items as
            # identical is NOT a mistake here: 2/C(a+b, a) is the same number.)
            named = [p / 2, Fraction(2, math.factorial(a + b)), Fraction(1, a + b)]
        elif kind == 2:
            groups = sorted(rng.sample((1, 2, 2, 3, 3), 3), reverse=True)
            n = sum(groups)
            ways = math.factorial(n) // math.prod(math.factorial(g) for g in groups)
            p = Fraction(1, ways)
            places = ("เชียงใหม่", "ระยอง", "น่าน")
            detail = " ".join(f"มีบ้านเกิดที่{pl} {g} คน" for pl, g in zip(places, groups))
            stem = (f"เพื่อน {n} คน {detail} ถ้าทายจังหวัดบ้านเกิดของทุกคนพร้อมกันแบบสุ่ม "
                    f"(ทายตามจำนวนคนของแต่ละจังหวัด) ความน่าจะเป็นที่ทายถูกครบทุกคน เท่ากับเท่าใด")
            # Treating everyone as distinct; one guess per person among the provinces.
            named = [Fraction(1, math.factorial(n)), Fraction(1, 3 ** n), Fraction(1, n)]
        else:
            k = rng.randint(2, 4)
            p = Fraction(math.perm(6, k), 6 ** k)
            stem = (f"ทอดลูกเต๋า {k} ลูกพร้อมกัน ความน่าจะเป็นที่ลูกเต๋าทุกลูกขึ้นแต้มไม่ซ้ำกัน เท่ากับเท่าใด")
            named = [Fraction(math.comb(6, k), 6 ** k), 1 - p, Fraction(1, 6 ** (k - 1))]
        return _choices([text(stem)], p, named, self.topic)
ProbabilityRandomArrangementM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_grid_route_m5",
               display_name={"th": "ความน่าจะเป็นของเส้นทางที่สุ่มเลือก"},
               level=M6, topic=TOPIC)
class ProbabilityGridRouteM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        m, n = rng.randint(2, 5), rng.randint(2, 4)
        while True:
            p, q = rng.randint(0, m), rng.randint(0, n)
            if (p, q) not in ((0, 0), (m, n)) and 0 < p + q < m + n:
                break
        prob = route_through(m, n, p, q)
        stem = (f"ถนนในเมืองหนึ่งตัดกันเป็นตารางสี่เหลี่ยม จุด A อยู่ที่ (0, 0) และจุด B อยู่ที่ ({m}, {n}) "
                f"เดินได้เฉพาะไปทางขวาหรือขึ้นข้างบนครั้งละ 1 ช่อง "
                f"ถ้าสุ่มเลือกเส้นทางที่สั้นที่สุดจาก A ไป B หนึ่งเส้นทาง โดยทุกเส้นทางมีโอกาสถูกเลือกเท่ากัน "
                f"ความน่าจะเป็นที่เส้นทางนั้นผ่านจุด H ({p}, {q}) เท่ากับเท่าใด")
        total = math.comb(m + n, m)
        # Only the leg to H; only the leg from H; a coin flip at every corner.
        named = [Fraction(math.comb(p + q, p), total),
                 Fraction(math.comb(m - p + n - q, m - p), total),
                 Fraction(math.comb(p + q, p), 2 ** (p + q))]
        return _choices([text(stem)], prob, named, self.topic)
ProbabilityGridRouteM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/13 ความน่าจะเป็น',))


@question_type("math.probability_independent",
               display_name={"th": "ความน่าจะเป็นของเหตุการณ์อิสระ"},
               level={"th": "ม.6"}, topic="ความน่าจะเป็น")
class ProbabilityIndependent(MathType):
    _STORIES = (("ฝนตกในวันพรุ่งนี้", "รถติดในวันพรุ่งนี้"),
                ("นักกีฬาคนแรกยิงลูกโทษเข้า", "นักกีฬาคนที่สองยิงลูกโทษเข้า"),
                ("เครื่องจักรเครื่องแรกทำงานปกติ", "เครื่องจักรเครื่องที่สองทำงานปกติ"))

    def expr(self, rng: Random, den_hi: int = 8):
        qa, qb = rng.randint(2, den_hi), rng.randint(2, den_hi)
        pa = Fraction(rng.randint(1, qa - 1), qa)
        pb = Fraction(rng.randint(1, qb - 1), qb)
        wrongs = [frac_tex(pa + pb) if pa + pb <= 1 else frac_tex(pa * pb / 2),
                  frac_tex(pa + pb - pa * pb), frac_tex(min(pa / pb, pb / pa))]
        if rng.random() < 0.5:
            return MathDraw(
                rf"P(A) = {frac_tex(pa)}, \quad P(B) = {frac_tex(pb)}",
                frac_tex(pa * pb),
                prompt="ถ้า A และ B เป็นเหตุการณ์อิสระกัน จงหา P(A ∩ B)",
                distractors=wrongs)
        x, y = rng.choice(self._STORIES)
        if rng.random() < 0.5:
            return MathDraw(
                rf"P(A) = {frac_tex(pa)}, \quad P(B) = {frac_tex(pb)}", frac_tex(pa * pb),
                prompt=(f"ให้ A คือเหตุการณ์ที่{x} และ B คือเหตุการณ์ที่{y} ซึ่งเป็นอิสระกัน "
                        f"ความน่าจะเป็นที่ทั้งสองเหตุการณ์เกิดขึ้นเป็นเท่าใด"),
                distractors=wrongs)
        both_fail = (1 - pa) * (1 - pb)
        return MathDraw(
            rf"P(A) = {frac_tex(pa)}, \quad P(B) = {frac_tex(pb)}", frac_tex(both_fail),
            prompt=(f"ให้ A คือเหตุการณ์ที่{x} และ B คือเหตุการณ์ที่{y} ซึ่งเป็นอิสระกัน "
                    f"ความน่าจะเป็นที่ทั้งสองเหตุการณ์ไม่เกิดขึ้นเลยเป็นเท่าใด"),
            distractors=[frac_tex(1 - pa * pb), frac_tex(pa * pb),
                         frac_tex(pa + pb - pa * pb)])
ProbabilityIndependent.PROVENANCE = Provenance("original")


@question_type("math.probability_counting_m5",
               display_name={"th": "ความน่าจะเป็นโดยใช้การนับ"},
               level=M6, topic="ความน่าจะเป็น")
class ProbabilityCountingM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            r, b = rng.randint(2, 7), rng.randint(2, 7)
            p = Fraction(math.comb(r, 2), math.comb(r + b, 2))
            stem = (f"ถุงใบหนึ่งมีลูกบอลสีแดง {r} ลูก และสีน้ำเงิน {b} ลูก สุ่มหยิบพร้อมกัน 2 ลูก "
                    f"ความน่าจะเป็นที่จะได้สีแดงทั้งสองลูกเป็นเท่าใด")
            # With replacement, and one ball only.
            wrongs = [Fraction(r * r, (r + b) ** 2), Fraction(r, r + b), Fraction(2 * r, r + b)
                      if 2 * r < r + b else Fraction(r - 1, r + b)]
        elif kind == 1:
            g, bo = rng.randint(3, 7), rng.randint(3, 7)
            k = rng.randint(2, 3)
            p = Fraction(math.comb(g, k), math.comb(g + bo, k))
            stem = (f"ห้องเรียนมีนักเรียนหญิง {g} คน ชาย {bo} คน สุ่มเลือกตัวแทน {k} คน "
                    f"ความน่าจะเป็นที่ตัวแทนเป็นนักเรียนหญิงทั้งหมดเป็นเท่าใด")
            wrongs = [Fraction(g, g + bo) ** k, Fraction(g, g + bo), Fraction(k, g + bo)]
        else:
            n = rng.randint(4, 6)
            p = Fraction(2 * math.factorial(n - 1), math.factorial(n))
            stem = (f"จัดคน {n} คนยืนเรียงแถวแบบสุ่ม ความน่าจะเป็นที่สองคนที่กำหนดยืนติดกันเป็นเท่าใด")
            wrongs = [Fraction(1, n), Fraction(1, n - 1), Fraction(2, n * (n - 1))]
        wrongs = [frac_tex(w) for w in wrongs if w != p and 0 < w <= 1]
        wrongs += [frac_tex(p / 2), frac_tex(min(1, p * 2))]
        return _maths_math_m5([text(stem)], frac_tex(p), [w for w in wrongs if w != frac_tex(p)], self.topic)
ProbabilityCountingM5.PROVENANCE = Provenance("original")

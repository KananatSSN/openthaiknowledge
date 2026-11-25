"""จำนวนเต็ม

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_diagrams, math_m1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import NUMBER_LINES, _img, _math_q, _nums
from otk.sets._support.math_m1 import LEVEL
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


def paren(n: int) -> str:
    """Wrap negative operands in parentheses: (-3), but 4 stays bare."""
    return f"({n})" if n < 0 else str(n)


NUMBER_LINE_ALT = "เส้นจำนวนจาก -10 ถึง 10 ที่มีขีดทุก 1 หน่วย กำกับเฉพาะ -5, 0 และ 5 และมีจุด A"


_INT_TOPIC = "จำนวนเต็ม"


@question_type("math.number_line_picture_m1", display_name={"th": "อ่านจำนวนเต็มจากเส้นจำนวน"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class NumberLinePictureM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(NUMBER_LINES)
        p = s.p
        # The sign lost, one tick off, and counting from 5 the wrong way.
        wrongs = _nums(-p, p + 1, p - 1, (10 - p) if p > 0 else (-10 - p), answer=p, lo=-10)
        return _math_q([text("จุด A บนเส้นจำนวนแทนจำนวนใด"), _img(s.asset_id, NUMBER_LINE_ALT)],
                       str(p), wrongs, self.topic)


@question_type("math.integer_distance_m1",
               display_name={"th": "ระยะห่างบนเส้นจำนวนและค่าสัมบูรณ์"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerDistanceM1(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(-25, -1), rng.randint(-20, 25)
        if rng.random() < 0.5:
            ans = abs(a - b)
            return MathDraw(rf"{a},\ {b}", str(ans), prompt="บนเส้นจำนวน จำนวนสองจำนวนนี้อยู่ห่างกันกี่หน่วย",
                            distractors=_story.keep(abs(a + b), a + b, ans + 1, answer=ans,
                                                    lo=-99))
        ans = abs(a) + abs(b)
        return MathDraw(rf"|{a}| + |{b}|", str(ans), prompt="จงหาค่า",
                        distractors=_story.keep(a + b, abs(a + b), -ans, answer=ans, lo=-99))


@question_type("math.integer_addsub",
               display_name={"th": "บวก-ลบจำนวนเต็ม (มีจำนวนลบ)"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerAddSub(MathType):
    def expr(self, rng: Random, lo: int = -12, hi: int = 12):
        while True:
            a, b = rng.randint(lo, hi), rng.randint(lo, hi)
            if a < 0 or b < 0:
                break
        op = rng.choice("+-")
        return rf"{a} {op} {paren(b)}", rf"{a + b if op == '+' else a - b}"


@question_type("math.integer_muldiv",
               display_name={"th": "คูณ-หารจำนวนเต็ม (มีจำนวนลบ)"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerMulDiv(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        if rng.random() < 0.5:
            while True:
                a, b = rng.randint(lo, hi), rng.randint(lo, hi)
                if a and b and (a < 0 or b < 0):
                    break
            return MathDraw(rf"{paren(a)} \times {paren(b)}", rf"{a * b}",
                            topic="คูณจำนวนเต็ม")
        while True:
            q, d = rng.randint(lo, hi), rng.randint(2, 9)
            if q and (q < 0 or rng.random() < 0.5):
                break
        if rng.random() < 0.5:
            d = -d
        return MathDraw(rf"{paren(q * d)} \div {paren(d)}", rf"{q}",
                        topic="หารจำนวนเต็ม")


@question_type("math.integer_four_ops",
               display_name={"th": "จำนวนเต็ม: โจทย์สองขั้นตอน"},
               level={"th": "ม.1"}, topic="จำนวนเต็ม")
class IntegerFourOps(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        while True:
            a, b, c = (rng.randint(lo, hi) for _ in range(3))
            if a and b and c and (a < 0 or b < 0):
                break
        op = rng.choice("+-")
        prod = a * b
        if rng.random() < 0.5:
            tex = rf"{paren(a)} \times {paren(b)} {op} {paren(c)}"
            val = prod + c if op == "+" else prod - c
        else:
            tex = rf"{a} {op} {paren(b)} \times {paren(c)}"
            val = a + b * c if op == "+" else a - b * c
        return MathDraw(tex, rf"{val}", hint=r"\text{multiply first}")


@question_type("math.integer_word_problem_m1",
               display_name={"th": "โจทย์ปัญหาจำนวนเต็ม (อุณหภูมิ ระดับน้ำทะเล บัญชี)"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerWordProblemM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            start, rise = rng.randint(-15, -1), rng.randint(3, 25)
            city = rng.choice(("กรุงโซล", "โตเกียว", "มอสโก", "ปักกิ่ง"))
            ans = start + rise
            return MathDraw("", str(ans),
                            prompt=(f"ตอนเช้าอุณหภูมิที่{city}เป็น {start} องศาเซลเซียส ตอนบ่ายอุณหภูมิ"
                                    f"สูงขึ้น {rise} องศาเซลเซียส ตอนบ่ายอุณหภูมิเป็นกี่องศาเซลเซียส"),
                            # The sign of the start dropped, and the rise taken away.
                            distractors=_story.keep(-start + rise, start - rise, -ans, rise,
                                                    answer=ans, lo=-99))
        if kind == 1:
            high, low = rng.randint(200, 3000), -rng.randint(50, 900)
            ans = high - low
            return MathDraw("", str(ans),
                            prompt=(f"ยอดเขาสูงจากระดับน้ำทะเล {grouped(high)} เมตร เรือดำน้ำอยู่ที่ระดับ "
                                    f"{low} เมตร เทียบกับระดับน้ำทะเล ทั้งสองอยู่สูงต่างกันกี่เมตร"),
                            distractors=_story.keep(high + low, -ans, high, answer=ans, lo=-9999))
        if kind == 2:
            bal, spend, dep = rng.randint(100, 900), rng.randint(500, 1500), rng.randint(100, 800)
            ans = bal - spend + dep
            return MathDraw("", str(ans),
                            prompt=(f"บัญชีของร้านค้ามีเงิน {bal} บาท จ่ายค่าสินค้า {grouped(spend)} บาท "
                                    f"(ยอดติดลบได้) แล้วฝากเพิ่ม {dep} บาท ยอดเงินในบัญชีเป็นเท่าใด"),
                            distractors=_story.keep(bal + spend + dep, spend - bal + dep,
                                                    bal - spend - dep, answer=ans, lo=-9999))
        a, b = rng.randint(-20, -2), rng.randint(-20, -2)
        if a == b:
            b -= 3
        higher = max(a, b)
        x, y = rng.sample(("ห้องแช่แข็งช่องที่หนึ่ง", "ห้องแช่แข็งช่องที่สอง"), 2)
        return MathDraw("", str(abs(a - b)),
                        prompt=(f"{x}มีอุณหภูมิ {a} องศาเซลเซียส {y}มีอุณหภูมิ {b} องศาเซลเซียส "
                                f"อุณหภูมิของสองช่องต่างกันกี่องศาเซลเซียส"),
                        distractors=_story.keep(abs(a + b), a + b, higher, answer=abs(a - b),
                                                lo=-99))


# ── More integers (2026-11): ordering, absolute value, the order of operations with negatives, and the
# properties of addition and multiplication ──

from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.sets._support.math_p2 import _maths  # noqa: E402


@question_type("math.integer_order_m1", display_name={"th": "เปรียบเทียบและเรียงลำดับจำนวนเต็ม"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerOrderM1(QuestionType):
    """On the number line the further left, the smaller: −12 < −3. The four choices are the four numbers."""

    def build(self, rng: Random) -> GeneratedQuestion:
        values = rng.sample([v for v in range(-20, 21) if v], 4)
        if not any(v < 0 for v in values):
            values[0] = -values[0]
        smallest = rng.random() < 0.5
        right = min(values) if smallest else max(values)
        return _maths([text(f"จำนวนในข้อใด{'น้อยที่สุด' if smallest else 'มากที่สุด'}")], str(right),
                      [str(v) for v in values if v != right], self.topic)


@question_type("math.absolute_value_m1", display_name={"th": "ค่าสัมบูรณ์"},
               level=LEVEL, topic=_INT_TOPIC)
class AbsoluteValueM1(WordProblem):
    """|a| is a's distance from 0: never negative."""

    def expr(self, rng: Random):
        a, b = rng.randint(2, 20), rng.randint(2, 20)
        kind = rng.randrange(4)
        if kind == 0:
            tex, right = rf"|-{a}| + |{b}|", a + b
            wrongs = (b - a, -a + b, -(a + b))
        elif kind == 1:
            tex, right = rf"|{b} - {a + b + 3}|", a + 3
            wrongs = (-(a + 3), b + a + b + 3, a)
        elif kind == 2:
            tex, right = rf"-|-{a}|", -a
            wrongs = (a, 0, -a - 1)
        else:
            tex, right = rf"|-{a}| \times |-{b}|", a * b
            wrongs = (-a * b, a + b, -(a + b))
        return MathDraw(tex, str(right), prompt="จงหาค่าของ",
                        distractors=[str(w) for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.integer_order_of_operations_m1", display_name={"th": "ลำดับการดำเนินการของจำนวนเต็ม"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerOrderOfOperationsM1(WordProblem):
    """Brackets and powers first, then × and ÷, then + and −; and −3² is −(3²)."""

    def expr(self, rng: Random):
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
        kind = rng.randrange(4)
        if kind == 0:
            tex, right, wrongs = rf"-{a} + {b} \times (-{c})", -a - b * c, ((-a + b) * -c, -a + b * c, a - b * c)
        elif kind == 1:
            tex, right, wrongs = rf"-{a}^{{2}}", -a * a, (a * a, -2 * a, 2 * a)
        elif kind == 2:
            tex, right, wrongs = rf"(-{a})^{{2}} - {b}", a * a - b, (-a * a - b, a * a + b, -2 * a - b)
        else:
            tex, right, wrongs = (rf"{a * b} \div (-{b}) - {c}", -a - c, (a - c, -a + c, a * b // (b + c) if b + c else 0))
        return MathDraw(tex, str(right), prompt="จงหาค่าของ",
                        distractors=[str(w) for w in dict.fromkeys(wrongs) if w != right])


_PROPS = ("สมบัติการสลับที่การบวก", "สมบัติการเปลี่ยนหมู่การคูณ", "สมบัติการแจกแจง",
          "สมบัติการมีตัวผกผันการบวก", "สมบัติการมีเอกลักษณ์การคูณ", "สมบัติการมีเอกลักษณ์การบวก")


def _prop(stem: str, right: int, *wrong: int) -> Concept:
    return Concept(f"{stem} ใช้สมบัติใด", _PROPS[right], tuple(_PROPS[w] for w in wrong))


@question_type("math.integer_properties_m1", display_name={"th": "สมบัติของการบวกและการคูณจำนวนเต็ม"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerPropertiesM1(ConceptBankType):
    ITEMS = [
        _prop("(−3) + 5 = 5 + (−3)", 0, 1, 2, 5),
        _prop("[2 × (−3)] × 4 = 2 × [(−3) × 4]", 1, 0, 2, 4),
        _prop("(−4) × (2 + 5) = (−4) × 2 + (−4) × 5", 2, 1, 0, 3),
        _prop("(−7) + 7 = 0", 3, 5, 0, 4),
        _prop("(−9) × 1 = −9", 4, 5, 3, 1),
        _prop("0 + (−6) = −6", 5, 4, 3, 0),
    ]


# ── To fifteen (2026-11): a run of consecutive integers, a missing number, a product of four, the largest of
# four expressions, and moves along the number line ──


@question_type("math.integer_run_sum_m1", display_name={"th": "ผลบวกของจำนวนเต็มที่เรียงติดกัน"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerRunSumM1(WordProblem):
    """−a + … + b: the pairs −k and k cancel, leaving the numbers past a."""

    def expr(self, rng: Random):
        a, b = rng.randint(2, 9), rng.randint(2, 12)
        while a == b:
            b = rng.randint(2, 12)
        right = sum(range(-a, b + 1))
        tex = rf"(-{a}) + (-{a - 1}) + \cdots + {b - 1} + {b}"
        # The negatives treated as positives; the endpoints only; the count of terms.
        return MathDraw(tex, str(right), prompt="จงหาผลบวก",
                        distractors=_story.keep(sum(range(0, a + 1)) + sum(range(0, b + 1)), b - a, a + b + 1,
                                                -right if right else 1, answer=right, lo=-200))


@question_type("math.integer_missing_number_m1", display_name={"th": "หาจำนวนที่หายไปในประโยคสัญลักษณ์"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerMissingNumberM1(WordProblem):
    def expr(self, rng: Random):
        a = rng.choice([v for v in range(-12, 13) if v])
        b = rng.choice([v for v in range(-12, 13) if v])
        kind = rng.randrange(4)
        show = lambda v: f"({v})" if v < 0 else str(v)
        if kind == 0:
            tex, right, wrongs = rf"{show(a)} + \square = {a + b}", b, (-b, a + b - a * 2, a + (a + b))
        elif kind == 1:
            tex, right, wrongs = rf"\square - {show(a)} = {b}", a + b, (b - a, a - b, -(a + b))
        elif kind == 2:
            tex, right, wrongs = rf"\square \times {show(a)} = {a * b}", b, (-b, a * b + a, a * b - a)
        else:
            tex, right, wrongs = rf"{show(a * b)} \div \square = {a}", b, (-b, a * b * a, a)
        return MathDraw(tex, str(right), prompt="จงหาจำนวนที่แทน □",
                        distractors=[str(w) for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.integer_product_four_m1", display_name={"th": "ผลคูณของจำนวนเต็มหลายจำนวน"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerProductFourM1(WordProblem):
    """An even count of negatives makes the product positive; an odd count makes it negative."""

    def expr(self, rng: Random):
        values = [rng.choice((-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)) for _ in range(4)]
        right = values[0] * values[1] * values[2] * values[3]
        tex = r" \times ".join(f"({v})" if v < 0 else str(v) for v in values)
        # The sign wrong; the numbers added; one factor left out.
        return MathDraw(tex, str(right), prompt="จงหาผลคูณ",
                        distractors=_story.keep(-right, sum(values), right // values[3] if values[3] else 0,
                                                abs(right) + 1, answer=right, lo=-1000))


@question_type("math.integer_largest_expression_m1", display_name={"th": "นิพจน์ใดมีค่ามากที่สุด"},
               level=LEVEL, topic=_INT_TOPIC)
class IntegerLargestExpressionM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b = rng.randint(2, 9), rng.randint(2, 9)
            exprs = [(rf"(-{a}) \times (-{b})", a * b), (rf"(-{a}) + (-{b})", -a - b),
                     (rf"(-{a}) - (-{b})", -a + b), (rf"(-{a}) \times {b}", -a * b)]
            if len({v for _, v in exprs}) == 4:
                break
        rng.shuffle(exprs)
        largest = rng.random() < 0.5
        pick = max(exprs, key=lambda e: e[1]) if largest else min(exprs, key=lambda e: e[1])
        return _maths([text(f"นิพจน์ในข้อใดมีค่า{'มากที่สุด' if largest else 'น้อยที่สุด'}")], pick[0],
                      [t for t, _ in exprs if t != pick[0]], self.topic)


@question_type("math.number_line_moves_m1", display_name={"th": "เลื่อนบนเส้นจำนวน"},
               level=LEVEL, topic=_INT_TOPIC)
class NumberLineMovesM1(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(-10, 10)
        right_steps, left_steps = rng.randint(2, 15), rng.randint(2, 15)
        end = start + right_steps - left_steps
        prompt = (f"เริ่มที่ {start} บนเส้นจำนวน เลื่อนไปทางขวา {right_steps} หน่วย แล้วเลื่อนไปทางซ้าย "
                  f"{left_steps} หน่วย จะอยู่ที่จำนวนใด").replace("-", "−")
        # The directions swapped; the second move only; both added.
        return MathDraw("", str(end), prompt=prompt,
                        distractors=_story.keep(start - right_steps + left_steps, start - left_steps,
                                                start + right_steps + left_steps, end + 1, answer=end, lo=-60))


from otk.kit.math_problems import ChoiceType  # noqa: E402


@question_type("math.consecutive_product_m1", display_name={"th": "หาจำนวนเรียงกันจากผลคูณ"},
               level={"th": "ม.1"}, topic=_INT_TOPIC)
class ConsecutiveProductM1(ChoiceType):
    """The k-th root of the product sits next to the middle number; check the run around it."""
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/exam-venue/mahidol-wittayanusorn/11349-MWIT.pdf, ข้อ 2",
        "openthaiknowledge-bank/mathematics/exam-venue/kvis/8515-KVIS-2566-Luckdee.pdf, PART II ข้อ 5"))

    def compose(self, rng: Random):
        step = rng.choice((1, 2))
        count = rng.choice((2, 3))
        first = rng.randint(12, 60) * (2 if step == 2 else 1)
        run = [first + step * i for i in range(count)]
        product = 1
        for n in run:
            product *= n
        answer = sum(run)
        kind = "จำนวนคู่" if step == 2 else "จำนวนเต็มบวก"
        # The run shifted one step either way; the middle (or larger) number alone; the count times the first.
        pool = (answer + step * count, answer - step * count, run[-1], count * first + step)
        wrongs = [w for w in dict.fromkeys(pool) if w != answer and w > 0]
        stem = f"{kind} {count} จำนวนที่เรียงติดกันคูณกันได้ {product:,} ผลบวกของจำนวนเหล่านั้นเท่ากับเท่าใด"
        return stem, str(answer), [str(w) for w in wrongs]


_HEX = "0123456789ABCDEF"


@question_type("math.number_base_m1", display_name={"th": "แปลงฐานสิบกับฐานสิบหกและฐานสอง (RGB/HEX)"},
               level={"th": "ม.1"}, topic=_INT_TOPIC)
class NumberBaseM1(ChoiceType):
    """A colour channel 0–255 is two base-16 digits: 16·high + low. Binary counts the 1s
    of the base-2 digits."""
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/exam-venue/mahidol-wittayanusorn/8353-2567-MWIT-MATH-R1_67-by-Lucky-KVIS10.pdf, ข้อ 25-26",
        "openthaiknowledge-bank/mathematics/exam-venue/mahidol-wittayanusorn/8519-MWIT35_R1.pdf, ข้อ 18"))

    def compose(self, rng: Random):
        rgb = [rng.randint(16, 255) for _ in range(3)]
        hexes = "".join(f"{_HEX[v // 16]}{_HEX[v % 16]}" for v in rgb)
        kind = rng.randrange(3)
        if kind == 0:
            answer = sum(_HEX.index(h) for h in hexes)
            # Letters A–F counted as 1; the decimal digits of the RGB values summed; base 10 split of each channel.
            pool = (sum(_HEX.index(h) if h.isdigit() else 1 for h in hexes),
                    sum(int(c) for v in rgb for c in str(v)),
                    sum(v // 10 + v % 10 for v in rgb))
            stem = (f"สีที่มีค่า RGB เป็น ({rgb[0]}, {rgb[1]}, {rgb[2]}) เขียนเป็นค่า HEX ได้ #abcdef "
                    "(แต่ละคู่คือฐานสิบหกของค่าหนึ่งช่อง และ A–F แทน 10–15) จงหา a + b + c + d + e + f")
        elif kind == 1:
            answer = rgb[0] - rgb[1] + rgb[2]
            # Hex digit pairs read as base 10 where possible; the digits swapped in each pair; a + b + c.
            swap = [16 * (v % 16) + v // 16 for v in rgb]
            pool = (swap[0] - swap[1] + swap[2], rgb[0] + rgb[1] + rgb[2], rgb[0] - rgb[1] - rgb[2])
            stem = f"สีที่มีค่า HEX เป็น #{hexes} เขียนเป็นค่า RGB ได้ (a, b, c) จงหาค่า a − b + c"
        else:
            value = rgb[0]
            answer = bin(value).count("1")
            # The 0s counted; the number of binary digits; the 1s of the next number.
            pool = (bin(value).count("0") - 1, len(bin(value)) - 2, bin(value + 1).count("1"), answer + 1)
            stem = f"เมื่อเขียน {value} ในเลขฐานสอง จะมีเลขโดด 1 กี่ตัว"
        wrongs = [w for w in dict.fromkeys(pool) if w != answer]
        for extra in (answer + 1, answer - 1, answer + 2):   # off by one when a pool value repeats
            if len(wrongs) >= 3:
                break
            if extra not in wrongs and extra != answer:
                wrongs.append(extra)
        return stem, str(answer), [str(w) for w in wrongs]

"""ระบบสมการ

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.3/3

Sets moved here from: math, math_algebra, math_m3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_m3 import LEGACY
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


@question_type("math.simultaneous_2var",
               display_name={"th": "ระบบสมการสองตัวแปร"}, level={"th": "ม.2"},
               topic="ระบบสมการ")
class Simultaneous2Var(MathType):
    def expr(self, rng: Random, aligned: int = 1):
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        if aligned:
            b = rng.randint(1, 4)
            a1, a2 = rng.sample(range(1, 10), 2)
            b1 = b2 = b
        else:
            while True:
                a1, b1, a2, b2 = (rng.choice([1, -1]) * rng.randint(1, 5)
                                  for _ in range(4))
                if a1 * b2 - a2 * b1 != 0:
                    break
        e1 = rf"{poly_tex((a1, 'x'), (b1, 'y'))} = {a1 * x + b1 * y}"
        e2 = rf"{poly_tex((a2, 'x'), (b2, 'y'))} = {a2 * x + b2 * y}"
        return MathDraw(rf"{e1}, \;\; {e2}", rf"(x, y) = ({x}, {y})",
                        prompt="จงแก้ระบบสมการ")


@question_type("math.system_substitution", display_name={"th": "ระบบสมการ (แทนค่า)"},
               level={"th": "ม.2"}, topic="ระบบสมการ")
class SystemSubstitution(MathType):
    def expr(self, rng: Random, root_hi: int = 8, coef_hi: int = 6):
        x, y = (_nonzero(rng, -root_hi, root_hi) for _ in range(2))
        a, b = rng.randint(1, coef_hi), rng.randint(1, coef_hi)
        c, d = rng.randint(1, coef_hi), -rng.randint(1, coef_hi)
        if a * d - b * c == 0:                     # keep the system independent
            d -= 1
        e, f = a * x + b * y, c * x + d * y
        return MathDraw(
            rf"\begin{{cases}} {poly_tex((a, 'x'), (b, 'y'))} = {e} \\ "
            rf"{poly_tex((c, 'x'), (d, 'y'))} = {f} \end{{cases}}",
            f"({x}, {y})", prompt="จงหาคำตอบของระบบสมการ",
            distractors=[f"({y}, {x})", f"({-x}, {-y})", f"({x}, {-y})"])


@question_type("math.system_setup_m3",
               display_name={"th": "เขียนระบบสมการจากโจทย์ปัญหา"},
               level=LEGACY, topic="ระบบสมการ")
class SystemSetupM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(6)
        if kind == 3:
            ad, ch = rng.randint(2, 40), rng.randint(2, 40)
            pa, pc = rng.choice(((120, 60), (100, 50), (150, 80), (80, 40)))
            money = pa * ad + pc * ch
            story = (f"ขายบัตรเข้าชมได้ {ad + ch} ใบ เป็นเงิน {money} บาท บัตรผู้ใหญ่ราคา {pa} บาท "
                     f"บัตรเด็กราคา {pc} บาท ให้ x แทนจำนวนบัตรผู้ใหญ่ และ y แทนจำนวนบัตรเด็ก")
            right = rf"x + y = {ad + ch},\quad {pa}x + {pc}y = {money}"
            wrongs = [rf"x + y = {ad + ch},\quad {pc}x + {pa}y = {money}",
                      rf"x + y = {money},\quad {pa}x + {pc}y = {ad + ch}",
                      rf"{pa}x + {pc}y = {ad + ch},\quad x - y = {money}"]
        elif kind == 4:
            child = rng.randint(5, 15)
            times = rng.choice((3, 4, 5))
            story = (f"ผลบวกของอายุพ่อกับอายุลูกเท่ากับ {child * (times + 1)} ปี อายุพ่อเป็น {times} เท่า"
                     f"ของอายุลูก ให้ x แทนอายุพ่อ และ y แทนอายุลูก")
            right = rf"x + y = {child * (times + 1)},\quad x = {times}y"
            wrongs = [rf"x + y = {child * (times + 1)},\quad y = {times}x",
                      rf"x - y = {child * (times + 1)},\quad x = {times}y",
                      rf"x + y = {child * (times + 1)},\quad x = y + {times}"]
        elif kind == 5:
            w, extra = rng.randint(4, 20), rng.randint(2, 12)
            per = 2 * (2 * w + extra)
            story = (f"รูปสี่เหลี่ยมผืนผ้ายาวรอบรูป {per} เซนติเมตร ด้านยาวยาวกว่าด้านกว้าง {extra} เซนติเมตร "
                     f"ให้ x แทนความยาว และ y แทนความกว้าง")
            right = rf"2x + 2y = {per},\quad x - y = {extra}"
            wrongs = [rf"x + y = {per},\quad x - y = {extra}",
                      rf"2x + 2y = {per},\quad y - x = {extra}",
                      rf"xy = {per},\quad x - y = {extra}"]
        elif kind == 0:
            x, y = rng.randint(5, 30), rng.randint(5, 30)
            story = (f"ในฟาร์มมีไก่และกระต่ายรวมกัน {x + y} ตัว นับขาได้ {2 * x + 4 * y} ขา "
                     f"ให้ x แทนจำนวนไก่ และ y แทนจำนวนกระต่าย")
            right = rf"x + y = {x + y},\quad 2x + 4y = {2 * x + 4 * y}"
            wrongs = [rf"x + y = {x + y},\quad 4x + 2y = {2 * x + 4 * y}",
                      rf"2x + 4y = {x + y},\quad x + y = {2 * x + 4 * y}",
                      rf"x + y = {x + y},\quad x + 4y = {2 * x + 4 * y}"]
        elif kind == 1:
            a, b = rng.randint(10, 60), rng.randint(5, 50)
            big, small = max(a, b), min(a, b)
            if big == small:
                big += 3
            story = (f"จำนวนสองจำนวนมีผลบวกเท่ากับ {big + small} และผลต่างเท่ากับ {big - small} "
                     f"ให้ x แทนจำนวนที่มากกว่า และ y แทนจำนวนที่น้อยกว่า")
            right = rf"x + y = {big + small},\quad x - y = {big - small}"
            wrongs = [rf"x + y = {big + small},\quad y - x = {big - small}",
                      rf"x - y = {big + small},\quad x + y = {big - small}",
                      rf"xy = {big + small},\quad x - y = {big - small}"]
        else:
            n5, n10 = rng.randint(3, 20), rng.randint(3, 20)
            story = (f"กระปุกมีเหรียญห้าบาทและเหรียญสิบบาทรวม {n5 + n10} เหรียญ คิดเป็นเงิน {5 * n5 + 10 * n10} บาท "
                     f"ให้ x แทนจำนวนเหรียญห้าบาท และ y แทนจำนวนเหรียญสิบบาท")
            right = rf"x + y = {n5 + n10},\quad 5x + 10y = {5 * n5 + 10 * n10}"
            wrongs = [rf"x + y = {n5 + n10},\quad 10x + 5y = {5 * n5 + 10 * n10}",
                      rf"5x + 10y = {n5 + n10},\quad x + y = {5 * n5 + 10 * n10}",
                      rf"x + y = {5 * n5 + 10 * n10},\quad 5x + 10y = {n5 + n10}"]
        return _maths([text(story), text("ระบบสมการใดแสดงความสัมพันธ์ในโจทย์นี้")], right, wrongs,
                      self.topic)


@question_type("math.system_word_problem", display_name={"th": "โจทย์ปัญหาระบบสมการ"},
               level={"th": "ม.2"}, topic="ระบบสมการ")
class SystemWordProblem(WordProblem):
    def expr(self, rng: Random, count_lo: int = 3, count_hi: int = 20):
        x = rng.randint(count_lo, count_hi)
        y = rng.randint(count_lo, count_hi)
        kind = rng.randrange(4)
        if kind == 0:
            adult_price = rng.randrange(40, 121, 10)
            child_price = rng.randrange(10, adult_price, 10)
            prompt = (f"ผู้ใหญ่และเด็กรวม {x + y} คน เข้าชมนิทรรศการ "
                      f"ค่าเข้าชมผู้ใหญ่คนละ {adult_price} บาท เด็กคนละ "
                      f"{child_price} บาท รวมเป็นเงิน {x * adult_price + y * child_price} บาท "
                      "มีผู้ใหญ่กี่คน")
        elif kind == 1:
            prompt = (f"ในฟาร์มมีไก่และกระต่ายรวมกัน {x + y} ตัว นับขาได้ {2 * y + 4 * x} ขา "
                      "มีกระต่ายกี่ตัว")
        elif kind == 2:
            prompt = (f"กระปุกมีเหรียญสิบบาทและเหรียญห้าบาทรวม {x + y} เหรียญ คิดเป็นเงิน "
                      f"{10 * x + 5 * y} บาท มีเหรียญสิบบาทกี่เหรียญ")
        else:
            if x == y:
                y += 1
            x, y = max(x, y), min(x, y)
            prompt = (f"จำนวนสองจำนวนมีผลบวกเท่ากับ {x + y} และผลต่างเท่ากับ {x - y} "
                      "จำนวนที่มากกว่าคือจำนวนใด")
        # The other unknown, the total, and the difference of the two.
        return MathDraw("", str(x), prompt=prompt,
                        distractors=[str(v) for v in dict.fromkeys((y, x + y, abs(x - y) or x + 1,
                                                                    x + 1)) if v != x])

from fractions import Fraction  # noqa: E402

from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More systems of equations (2026-11): a sum and a difference, x + y straight from the equations, coins,
# ages, which pair solves the system, and two prices ──


@question_type("math.system_sum_difference_m3", display_name={"th": "สองจำนวนเมื่อรู้ผลบวกและผลต่าง"},
               level=LEVEL, topic="ระบบสมการ")
class SystemSumDifferenceM3(WordProblem):
    def expr(self, rng: Random):
        y = rng.randint(2, 40)
        x = y + rng.randint(1, 30)
        s, d = x + y, x - y
        bigger = rng.random() < 0.5
        right = x if bigger else y
        prompt = (f"จำนวนสองจำนวนรวมกันได้ {s} และผลต่างของสองจำนวนนั้นเท่ากับ {d} "
                  f"จำนวนที่{'มากกว่า' if bigger else 'น้อยกว่า'}คือจำนวนใด")
        # The other number; the sum halved; the difference.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(y if bigger else x, s // 2 if s // 2 != right else s // 2 + 1, d,
                                                right + 1, answer=right, lo=1))


@question_type("math.system_x_plus_y_m3", display_name={"th": "หาค่า x + y จากระบบสมการ"},
               level=LEVEL, topic="ระบบสมการ")
class SystemXPlusYM3(MathType):
    def expr(self, rng: Random):
        a, b = rng.sample(range(1, 8), 2)
        x, y = rng.randint(-8, 10), rng.randint(-8, 10)
        e1, e2 = a * x + b * y, b * x + a * y
        right = x + y
        # The sum of the right sides; x alone; y alone.
        return MathDraw(rf"{poly_tex((a, 'x'), (b, 'y'))} = {e1}, \;\; {poly_tex((b, 'x'), (a, 'y'))} = {e2}", str(right),
                        prompt="จากระบบสมการ ค่าของ x + y เท่ากับเท่าใด",
                        distractors=_tk3(str(e1 + e2), str(x), str(y), str(right + 1), answer=str(right)))


@question_type("math.system_coins_m3", display_name={"th": "นับเหรียญสองชนิด"},
               level=LEVEL, topic="ระบบสมการ")
class SystemCoinsM3(WordProblem):
    def expr(self, rng: Random):
        small, big = rng.choice(((1, 5), (2, 10), (5, 10), (1, 10)))
        m, k = rng.randint(2, 30), rng.randint(2, 30)
        count, total = m + k, small * m + big * k
        p = rng.choice(_story.NAMES)
        prompt = (f"{p}มีเหรียญ {small} บาท และเหรียญ {big} บาท รวม {count} เหรียญ คิดเป็นเงิน {total} บาท "
                  f"{p}มีเหรียญ {big} บาทกี่เหรียญ")
        # The other coin; the money over the larger coin; half the coins.
        return MathDraw("", str(k), prompt=prompt,
                        distractors=_story.keep(m, total // big, count // 2 if count // 2 != k else count // 2 + 1, k + 1,
                                                answer=k, lo=1))


@question_type("math.system_ages_m3", display_name={"th": "อายุพ่อและลูก"},
               level=LEVEL, topic="ระบบสมการ")
class SystemAgesM3(WordProblem):
    def expr(self, rng: Random):
        child = rng.randint(5, 15)
        times = rng.randint(3, 5)
        parent = times * child
        prompt = f"ปัจจุบันพ่ออายุเป็น {times} เท่าของอายุลูก และอายุรวมกันเท่ากับ {parent + child} ปี พ่ออายุกี่ปี"
        # The child's age; the total over the multiple; the total less the multiple.
        return MathDraw("", str(parent), prompt=prompt,
                        distractors=_story.keep(child, (parent + child) // times, parent + child - times, parent - child,
                                                answer=parent, lo=1))


@question_type("math.system_which_pair_m3", display_name={"th": "คู่อันดับใดเป็นคำตอบของระบบสมการ"},
               level=LEVEL, topic="ระบบสมการ")
class SystemWhichPairM3(QuestionType):
    """Fixed choices: a pair from another draw could also solve this system."""

    def build(self, rng: Random, **params):
        x, y = rng.randint(-6, 9), rng.randint(-6, 9)
        while x == y:
            y = rng.randint(-6, 9)
        a, b = rng.randint(1, 5), rng.randint(1, 5)
        s, d = a * x + b * y, x - y
        right = f"({x}, {y})"
        # The coordinates swapped; one satisfying the first only; one satisfying the second only.
        first_only = next(f"({x + b * t}, {y - a * t})" for t in (1, 2, 3) if (x + b * t) - (y - a * t) != d)
        second_only = f"({x + 1}, {y + 1})"
        wrongs = [f"({y}, {x})", first_only, second_only]
        system = rf"\begin{{cases}} {poly_tex((a, 'x'), (b, 'y'))} = {s} \\ x - y = {d} \end{{cases}}"
        return _fixed_maths([_text_block("คู่อันดับ (x, y) ใดเป็นคำตอบของระบบสมการ"), _math_block(system)], right,
                            _tk3(*wrongs, answer=right), self.topic)


@question_type("math.system_two_prices_m3", display_name={"th": "หาราคาสินค้าจากการซื้อสองครั้ง"},
               level=LEVEL, topic="ระบบสมการ")
class SystemTwoPricesM3(WordProblem):
    def expr(self, rng: Random):
        pen, book = rng.randint(5, 30), rng.randint(20, 90)
        n1, m1 = rng.randint(2, 6), rng.randint(1, 4)
        n2 = rng.randint(1, n1 - 1)
        m2 = m1
        a, b = n1 * pen + m1 * book, n2 * pen + m2 * book
        prompt = (f"ซื้อปากกา {n1} ด้าม และสมุด {m1} เล่ม จ่าย {a} บาท ซื้อปากกา {n2} ด้าม และสมุด {m2} เล่ม จ่าย {b} บาท "
                  "ปากการาคาด้ามละกี่บาท")
        # The difference in money not divided; the price of a book; the first bill over the pens.
        return MathDraw("", str(pen), prompt=prompt,
                        distractors=_story.keep(a - b, book, a // n1, pen + 5, answer=pen, lo=1))

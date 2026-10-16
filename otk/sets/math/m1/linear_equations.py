"""สมการเชิงเส้น

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.1/*

Sets moved here from: math, math_algebra, math_m1, math_pictures_hi.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_m1 import LEVEL
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_hi import BALANCES

PROVENANCE = Provenance("original")


_EQ_TOPIC = "สมการเชิงเส้น"


def _equation_story(rng: Random):
    """``(story, answer, equation, wrong equations)``; the equation's unknown
    is x and its solution is not always the answer (consecutive numbers)."""
    kind = rng.randrange(8)
    p, q = _story.names(rng)
    if kind == 0:
        k, c = rng.randint(2, 9), rng.randint(3, 40)
        x = rng.randint(3, 30)
        return (f"{k} เท่าของจำนวนหนึ่งบวกด้วย {c} ได้ผลลัพธ์เท่ากับ {k * x + c} จำนวนนั้นคืออะไร",
                x, rf"{k}x + {c} = {k * x + c}",
                [rf"{k}(x + {c}) = {k * x + c}", rf"x + {k} + {c} = {k * x + c}",
                 rf"{k}x = {k * x + c} + {c}"])
    if kind == 1:
        n = rng.randint(3, 60)
        total = 3 * n + 3
        return (f"จำนวนเต็มสามจำนวนเรียงติดกันมีผลบวกเท่ากับ {total} จำนวนที่มากที่สุดคือจำนวนใด",
                n + 2, rf"x + (x + 1) + (x + 2) = {total}",
                [rf"x + 2x + 3x = {total}", rf"3x = {total} + 3", rf"x + (x + 2) + (x + 4) = {total}"])
    if kind == 2:
        n = 2 * rng.randint(2, 40)
        total = 2 * n + 2
        return (f"จำนวนคู่สองจำนวนเรียงติดกันมีผลบวกเท่ากับ {total} จำนวนที่น้อยกว่าคือจำนวนใด",
                n, rf"x + (x + 2) = {total}",
                [rf"x + (x + 1) = {total}", rf"2x + 2x = {total}", rf"x + 2x = {total}"])
    if kind == 3:
        # Built backwards so the ages are whole: gap = (k − 1)(child + years).
        while True:
            k, child, years = rng.choice((2, 3, 4)), rng.randint(3, 20), rng.randint(1, 12)
            gap = (k - 1) * (child + years)
            if 18 <= gap <= 45:
                break
        return (f"ปัจจุบันพ่ออายุมากกว่า{p} {gap} ปี อีก {years} ปีข้างหน้า พ่อจะมีอายุเป็น {k} เท่าของ{p} "
                f"ปัจจุบัน{p}อายุกี่ปี", child,
                rf"x + {gap} + {years} = {k}(x + {years})",
                [rf"x + {gap} = {k}x", rf"x + {gap} + {years} = {k}x + {years}",
                 rf"x + {gap} = {k}(x + {years})"])
    if kind == 4:
        n10, n5 = rng.randint(3, 25), rng.randint(3, 25)
        total_coins, value = n10 + n5, 10 * n10 + 5 * n5
        return (f"{p}มีเหรียญห้าบาทและเหรียญสิบบาทรวมกัน {total_coins} เหรียญ คิดเป็นเงิน {value} บาท "
                f"{p}มีเหรียญสิบบาทกี่เหรียญ", n10,
                rf"10x + 5({total_coins} - x) = {value}",
                [rf"10x + 5x = {value}", rf"5x + 10({total_coins} - x) = {value}",
                 rf"x + ({total_coins} - x) = {value}", rf"10x + 5({total_coins} + x) = {value}",
                 rf"15x = {value} - {total_coins}"])
    if kind == 5:
        w, d = rng.randint(3, 25), rng.randint(2, 15)
        per = 2 * (2 * w + d)
        return (f"รูปสี่เหลี่ยมผืนผ้ามีความยาวมากกว่าความกว้าง {d} เซนติเมตร ยาวรอบรูป {per} เซนติเมตร "
                f"ด้านกว้างยาวกี่เซนติเมตร", w, rf"2(x + x + {d}) = {per}",
                [rf"x + (x + {d}) = {per}", rf"x(x + {d}) = {per}", rf"4x + {d} = {per}"])
    if kind == 6:
        # Angles x, 2x, 3x (or similar) of a triangle.
        m = rng.choice(((1, 2, 3), (1, 1, 2), (2, 3, 4), (1, 2, 6), (1, 3, 5), (2, 3, 7)))
        x = Fraction(180, sum(m))
        if x.denominator != 1:
            m = (1, 2, 3)
            x = Fraction(30)
        a, b, c = m
        terms = " + ".join(f"{t}x" if t != 1 else "x" for t in m)
        return (f"มุมภายในทั้งสามของรูปสามเหลี่ยมมีขนาด {'x' if a == 1 else f'{a}x'}, "
                f"{'x' if b == 1 else f'{b}x'} และ {c}x องศา มุมที่ใหญ่ที่สุดมีขนาดกี่องศา",
                int(c * x), rf"{terms} = 180",
                [rf"{terms} = 360", rf"{terms} = 90", rf"{c}x = 180", rf"{terms} = 100"])
    adult, child = rng.randrange(60, 201, 10), rng.randrange(20, 60, 5)
    n = rng.randint(3, 20)
    more = rng.randint(1, 6)
    kids = n + more
    total = adult * n + child * kids
    return (f"ครอบครัวหนึ่งซื้อบัตรเข้าชมสวนสัตว์ บัตรผู้ใหญ่ใบละ {adult} บาท บัตรเด็กใบละ {child} บาท "
            f"ซื้อบัตรเด็กมากกว่าบัตรผู้ใหญ่ {more} ใบ จ่ายเงินทั้งหมด {grouped(total)} บาท "
            f"ซื้อบัตรผู้ใหญ่กี่ใบ", n, rf"{adult}x + {child}(x + {more}) = {total}",
            [rf"{adult}x + {child}x = {total}", rf"{adult}(x + {more}) + {child}x = {total}",
             rf"({adult} + {child})x + {more} = {total}"])


def _solve_linear(eq: str) -> Fraction | None:
    """Solve the story equations in x by evaluating both sides at two points."""
    def side(s: str, x: Fraction) -> Fraction:
        import re
        s = re.sub(r"(\d)x", r"\1*x", s)
        s = re.sub(r"(\d)\(", r"\1*(", s)
        s = s.replace(")(", ")*(")
        return eval(s, {"x": x, "__builtins__": {}})  # otk: allow eval (authored equations, no builtins)
    left, right = eq.split("=")
    f0 = side(left, Fraction(0)) - side(right, Fraction(0))
    f1 = side(left, Fraction(1)) - side(right, Fraction(1))
    slope = f1 - f0
    if slope == 0:
        return None
    return -f0 / slope


BAL_ALT = "ภาพตาชั่งสองแขนที่สมดุล มีกล่องและลูกตุ้มบนจานทั้งสองข้าง"


def _side(n_x: int, n: int) -> str:
    terms = []
    if n_x:
        terms.append("x" if n_x == 1 else f"{n_x}x")
    if n or not terms:
        terms.append(str(n))
    return " + ".join(terms)


@question_type("math.linear_equation",
               display_name={"th": "สมการเชิงเส้นตัวแปรเดียว"}, level={"th": "ม.1"},
               topic="สมการเชิงเส้น")
class LinearEquation(MathType):
    def expr(self, rng: Random, sol_lo: int = -9, sol_hi: int = 9):
        x = rng.randint(sol_lo, sol_hi)
        a = rng.randint(2, 9)
        c = rng.choice([n for n in range(-5, 6) if n != a])
        if rng.random() < 0.5:
            c = 0
        b = rng.randint(-15, 15)
        d = b + (a - c) * x
        lhs = poly_tex((a, "x"), (b, ""))
        rhs = poly_tex((c, "x"), (d, ""))
        return MathDraw(rf"{lhs} = {rhs}", rf"x = {x}", prompt="จงแก้หา x")


@question_type("math.balance_equation_m1", display_name={"th": "สมการจากตาชั่งสมดุล"},
               level={"th": "ม.1"}, topic="สมการเชิงเส้น")
class BalanceEquationM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(BALANCES)
        lead = text("ตาชั่งสมดุล กล่องแต่ละใบหนัก x กิโลกรัม ลูกตุ้มแต่ละลูกหนัก 1 กิโลกรัม")
        img = image(s.asset_id, alt=BAL_ALT)
        if rng.random() < 0.5:
            right = f"{_side(s.a, s.b)} = {_side(s.c, s.d)}"
            wrongs = [f"{_side(s.a, s.d)} = {_side(s.c, s.b)}",       # weights swapped
                      f"{_side(s.a + s.c, s.b)} = {s.d}",            # boxes moved without care
                      f"{_side(s.a, s.b + s.d)} = {_side(s.c, 0)}" if s.c else f"{s.a + s.b} = {s.d}",
                      f"{_side(s.a, s.b)} = {_side(s.c, s.d + 1)}"]
            return _math_q([lead, text("สมการใดแสดงภาพนี้"), img], right,
                           [w for w in dict.fromkeys(wrongs) if w != right], self.topic)
        # Adding the weights instead of taking them away; dividing by the left boxes only.
        return _math_q([lead, text("กล่องแต่ละใบหนักกี่กิโลกรัม"), img], str(s.x),
                       _near(s.x, (s.d + s.b) // max(s.a - s.c, 1), s.d // s.a or s.x + 3,
                             s.x + 2, lo=1), self.topic)


@question_type("math.linear_equation_brackets",
               display_name={"th": "สมการเชิงเส้นที่มีวงเล็บ"},
               level={"th": "ม.1"}, topic="สมการเชิงเส้น")
class LinearEquationBrackets(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, root_hi: int = 9, coef_hi: int = 6):
        x = _nonzero(rng, -root_hi, root_hi)
        a, b = rng.randint(2, coef_hi), _nonzero(rng, -coef_hi, coef_hi)
        c = rng.randint(1, coef_hi)
        # a(x + b) + c·x = rhs, solved by construction.
        rhs = a * (x + b) + c * x
        return MathDraw(
            rf"{a}({poly_tex((1, 'x'), (b, ''))}) + {c}x = {rhs}", f"x = {x}",
            prompt="จงแก้สมการ",
            # Not distributing a over b is the classic failure here.
            distractors=[f"x = {-x}",
                         f"x = {Fraction(rhs - b, a + c)}",
                         f"x = {Fraction(rhs, a + c)}"])


@question_type("math.linear_equation_both_sides",
               display_name={"th": "สมการที่มีตัวแปรทั้งสองข้าง"},
               level={"th": "ม.1"}, topic="สมการเชิงเส้น")
class LinearEquationBothSides(MathType):
    def expr(self, rng: Random, root_hi: int = 9, coef_hi: int = 9):
        x = _nonzero(rng, -root_hi, root_hi)
        a = rng.randint(2, coef_hi)
        c = rng.choice([n for n in range(1, coef_hi + 1) if n != a])
        b = rng.randint(-12, 12)
        d = (a - c) * x + b                        # ax + b = cx + d
        return MathDraw(
            rf"{poly_tex((a, 'x'), (b, ''))} = {poly_tex((c, 'x'), (d, ''))}",
            f"x = {x}", prompt="จงแก้สมการ",
            distractors=[f"x = {-x}", f"x = {Fraction(d + b, a + c)}",
                         f"x = {Fraction(d - b, a + c)}"])


@question_type("math.linear_word_problem_m1",
               display_name={"th": "โจทย์ปัญหาสมการเชิงเส้นตัวแปรเดียว"},
               level=LEVEL, topic=_EQ_TOPIC)
class LinearWordProblemM1(WordProblem):
    def expr(self, rng: Random):
        story, ans, _, wrong_eqs = _equation_story(rng)
        # What the tempting wrong equations would have given, where whole.
        wrongs = []
        for w in wrong_eqs:
            try:
                v = _solve_linear(w)
            except Exception:              # a product like x(x + d) is not linear
                v = None
            if v is not None and v.denominator == 1 and v > 0:
                wrongs.append(int(v))
        return MathDraw("", str(ans), prompt=story,
                        distractors=_story.keep(*wrongs, ans + 1, ans + 2, ans - 1,
                                                answer=ans, lo=1))


@question_type("math.linear_equation_setup_m1",
               display_name={"th": "เขียนสมการจากโจทย์ปัญหา"},
               level=LEVEL, topic=_EQ_TOPIC)
class LinearEquationSetupM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        story, _, eq, wrongs = _equation_story(rng)
        right_x = _solve_linear(eq)
        keep = []
        for w in wrongs:
            try:
                v = _solve_linear(w)
            except Exception:
                v = None
            if v != right_x:
                keep.append(w)
        return _maths([text(story), text("ถ้าให้ x แทนจำนวนที่ไม่ทราบค่า สมการใดใช้แก้โจทย์นี้ได้")],
                      eq, keep, self.topic)


def _fee_parameters(rng: Random) -> tuple[int, int, int, int]:
    low_rate, extra_rate = rng.randint(2, 12), rng.randint(2, 8)
    units = rng.randint(5, 40)
    low_fee = rng.randrange(10, 101, 5)
    return low_fee + extra_rate * units, low_rate, low_fee, low_rate + extra_rate


@question_type("math.linear_fee_comparison_m1",
               display_name={"th": "สมการเปรียบเทียบค่าใช้จ่ายสองแบบ"},
               level=LEVEL, topic=_EQ_TOPIC)
class LinearFeeComparisonM1(WordProblem):
    def expr(self, rng: Random):
        fee_a, rate_a, fee_b, rate_b = _fee_parameters(rng)
        answer = Fraction(fee_a - fee_b, rate_b - rate_a)
        service, fee, unit = rng.choice((
            ("ร้านเช่าจักรยาน", "ค่าบริการเริ่มต้น", "ชั่วโมง"),
            ("ร้านพิมพ์เอกสาร", "ค่าเตรียมงาน", "หน้า"),
            ("บริการส่งพัสดุ", "ค่าบริการเริ่มต้น", "กิโลกรัม"),
        ))
        return MathDraw("", frac_tex(answer), prompt=(
            f"{service}มีบริการสองแบบ แบบ A คิด{fee} {fee_a} บาท และเพิ่ม{unit}ละ {rate_a} บาท "
            f"แบบ B คิด{fee} {fee_b} บาท และเพิ่ม{unit}ละ {rate_b} บาท "
            f"ใช้บริการกี่{unit}จึงจะเสียค่าใช้จ่ายเท่ากัน"),
            distractors=[
                named("operation.reversed", frac_tex(Fraction(fee_a + fee_b, rate_b - rate_a))),
                named("steps.missed_a_step", frac_tex(Fraction(fee_a, rate_b - rate_a))),
                named("operation.reversed", frac_tex(Fraction(fee_a - fee_b, rate_a + rate_b))),
                named("steps.missed_a_step", frac_tex(Fraction(fee_a - fee_b, rate_b))),
            ])


def _remaining_parameters(rng: Random) -> tuple[int, int, int, int]:
    denominator = rng.randint(3, 9)
    numerator = rng.randint(1, denominator - 1)
    initial = denominator * rng.randint(8, 40)
    after_fraction = initial * (denominator - numerator) // denominator
    extra = rng.randint(2, after_fraction - 2)
    return numerator, denominator, extra, after_fraction - extra


@question_type("math.linear_remaining_fraction_m1",
               display_name={"th": "สมการย้อนหาจำนวนเดิมจากส่วนที่เหลือ"},
               level=LEVEL, topic=_EQ_TOPIC)
class LinearRemainingFractionM1(WordProblem):
    def expr(self, rng: Random):
        numerator, denominator, extra, remaining = _remaining_parameters(rng)
        kept = Fraction(denominator - numerator, denominator)
        answer = Fraction(remaining + extra, 1) / kept
        subject, first, second, unit = rng.choice((
            ("ร้านค้ามีสมุดจำนวนหนึ่ง", "ขายไป", "ขายเพิ่มอีก", "เล่ม"),
            ("ชมรมมีเงินจำนวนหนึ่ง", "ใช้ไป", "จ่ายเพิ่มอีก", "บาท"),
            ("ถังมีน้ำอยู่จำนวนหนึ่ง", "ใช้น้ำไป", "ใช้น้ำเพิ่มอีก", "ลิตร"),
        ))
        return MathDraw("", frac_tex(answer), prompt=(
            f"{subject} {first} {numerator}/{denominator} ของจำนวนเดิม "
            f"แล้ว{second} {extra} {unit} เหลือ {remaining} {unit} เดิมมีทั้งหมดกี่{unit}"),
            distractors=[
                named("steps.missed_a_step", frac_tex(Fraction(remaining, 1) / kept)),
                named("steps.wrong_order", frac_tex(Fraction(remaining, 1) / kept + extra)),
                named("part.complement", frac_tex(Fraction(remaining + extra) /
                                                  Fraction(numerator, denominator))),
                named("fraction.not_worked_back", frac_tex((remaining + extra) * kept)),
                named("operation.reversed", frac_tex(Fraction(remaining - extra, 1) / kept)),
            ])


def _transfer_parameters(rng: Random) -> tuple[int, int, int]:
    multiplier, transferred = rng.randint(2, 5), rng.randint(2, 15)
    final_first = rng.randint(transferred + 1, transferred + 30)
    second = multiplier * final_first - transferred
    return second, transferred, multiplier


@question_type("math.linear_transfer_m1",
               display_name={"th": "สมการหาจำนวนก่อนย้ายสิ่งของ"},
               level=LEVEL, topic=_EQ_TOPIC)
class LinearTransferM1(WordProblem):
    def expr(self, rng: Random):
        second, transferred, multiplier = _transfer_parameters(rng)
        answer = Fraction(second + transferred, multiplier) + transferred
        item, unit, container = rng.choice((
            ("ลูกบอล", "ลูก", "กล่อง"),
            ("หนังสือ", "เล่ม", "ชั้น"),
            ("ดินสอ", "แท่ง", "กล่อง"),
        ))
        return MathDraw("", frac_tex(answer), prompt=(
            f"{container}ที่สองมี{item} {second} {unit} ย้าย{item} {transferred} {unit} "
            f"จาก{container}แรกไป{container}ที่สอง ทำให้{container}ที่สองมี{item}เป็น "
            f"{multiplier} เท่าของ{container}แรก เดิม{container}แรกมี{item}กี่{unit}"),
            distractors=[
                named("steps.missed_a_step", frac_tex(Fraction(second + transferred, multiplier))),
                named("steps.missed_a_step", frac_tex(Fraction(second, multiplier) + transferred)),
                named("operation.reversed", frac_tex(Fraction(second + transferred, multiplier) - transferred)),
                named("operation.reversed", frac_tex(Fraction(second - transferred, multiplier) + transferred)),
            ])

"""อสมการเชิงเส้น

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.3/1

Sets moved here from: math, math_algebra, math_bank_real, math_m3.
"""

from __future__ import annotations

import functools
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_bank_real import M3, _tex_q
from otk.sets._support.math_m3 import LEGACY
from otk.sets._support.math_p2 import _maths

_GRID = [Fraction(n, 2) for n in range(-12, 13)]


#: Premises over (a, b, c): (Thai-free TeX parts joined by "และ", predicate).
_ORDER_PREMISES = (
    ((r"a < b",), lambda a, b, c: a < b),
    ((r"a < b", r"c < 0"), lambda a, b, c: a < b and c < 0),
    ((r"0 < a < b",), lambda a, b, c: 0 < a < b),
    ((r"a < b < 0",), lambda a, b, c: a < b < 0),
)


_ORDER_CLAIMS = (
    (r"a + c < b + c", lambda a, b, c: a + c < b + c),
    (r"ac > bc", lambda a, b, c: a * c > b * c),
    (r"ac < bc", lambda a, b, c: a * c < b * c),
    (r"a^{2} < b^{2}", lambda a, b, c: a * a < b * b),
    (r"a^{2} > b^{2}", lambda a, b, c: a * a > b * b),
    (r"|a| < |b|", lambda a, b, c: abs(a) < abs(b)),
    (r"\frac{1}{a} > \frac{1}{b}", lambda a, b, c: a != 0 and b != 0 and 1 / a > 1 / b),
    (r"-a > -b", lambda a, b, c: -a > -b),
    (r"b - a > 0", lambda a, b, c: b - a > 0),
    (r"a^{3} < b^{3}", lambda a, b, c: a ** 3 < b ** 3),
)


@functools.cache          # 4 premises × 10 claims, each a 25³ scan: decide each pair once
def always_order(premise, claim) -> bool:
    """No counterexample on a grid of halves from −6 to 6 (zero included)."""
    return all(claim(a, b, c) for a in _GRID for b in _GRID for c in _GRID if premise(a, b, c))


_INEQ_TOPIC = "อสมการเชิงเส้น"


def _inequality_story(rng: Random):
    """``(story, answer, inequality, wrong inequalities)``."""
    p = rng.choice(_story.NAMES)
    kind = rng.randrange(4)
    if kind == 0:
        money, fixed, per = rng.randrange(300, 1001, 50), rng.randrange(20, 120, 5), rng.randint(15, 60)
        n = (money - fixed) // per
        return (f"{p}มีเงิน {money} บาท ต้องจ่ายค่าเดินทาง {fixed} บาท ที่เหลือใช้ซื้อสมุดเล่มละ {per} บาท "
                f"{p}ซื้อสมุดได้มากที่สุดกี่เล่ม", n, rf"{fixed} + {per}x \le {money}",
                [rf"{fixed} + {per}x \ge {money}", rf"{per}x \le {money}", rf"{fixed}x + {per} \le {money}"])
    if kind == 1:
        known = [rng.randint(45, 90) for _ in range(3)]
        need = rng.choice((60, 65, 70, 75))
        least = 4 * need - sum(known)
        if not 0 < least <= 100:
            return _inequality_story(rng)
        return (f"{p}สอบย่อย 3 ครั้งได้ {', '.join(map(str, known))} คะแนน ต้องการคะแนนเฉลี่ย 4 ครั้งไม่น้อยกว่า "
                f"{need} คะแนน ครั้งที่ 4 ต้องได้อย่างน้อยกี่คะแนน", least,
                rf"\frac{{{sum(known)} + x}}{{4}} \ge {need}",
                [rf"\frac{{{sum(known)} + x}}{{4}} \le {need}", rf"{sum(known)} + x \ge {need}",
                 rf"\frac{{{sum(known)} + x}}{{3}} \ge {need}"])
    if kind == 2:
        limit, person, box = rng.choice((500, 600, 800, 1000)), rng.randint(55, 90), rng.randint(15, 40)
        n = (limit - person) // box
        return (f"ลิฟต์ขนของรับน้ำหนักได้ไม่เกิน {limit} กิโลกรัม พนักงานหนัก {person} กิโลกรัม "
                f"ต้องการขนกล่องหนักกล่องละ {box} กิโลกรัม ขึ้นไปพร้อมกัน ขนได้มากที่สุดกี่กล่อง", n,
                rf"{person} + {box}x \le {limit}",
                [rf"{person} + {box}x \ge {limit}", rf"{box}x \le {limit}", rf"{person}x + {box} \le {limit}"])
    cap = rng.randint(40, 300)
    n = (cap - 3) // 3
    return (f"จำนวนเต็มบวกสามจำนวนเรียงติดกันมีผลบวกไม่เกิน {cap} จำนวนที่มากที่สุดในสามจำนวนนั้น"
            f"มีค่ามากที่สุดได้เท่าใด", n + 2, rf"x + (x + 1) + (x + 2) \le {cap}",
            [rf"x + (x + 1) + (x + 2) \ge {cap}", rf"3x \le {cap}", rf"x + 2x + 3x \le {cap}"])


@question_type("math.inequality",
               display_name={"th": "อสมการเชิงเส้น"}, level={"th": "ม.2"},
               topic="อสมการเชิงเส้น")
class Inequality(MathType):
    def expr(self, rng: Random, sol_lo: int = -9, sol_hi: int = 9):
        s = rng.randint(sol_lo, sol_hi)
        diff = rng.choice([1, -1]) * rng.randint(1, 5)
        c = rng.randint(-4, 4)
        a = c + diff
        b = rng.randint(-9, 9)
        d = b + diff * s
        rel = rng.choice(["<", ">"])
        ans_rel = rel if diff > 0 else (">" if rel == "<" else "<")
        lhs = poly_tex((a, "x"), (b, ""))
        rhs = poly_tex((c, "x"), (d, ""))
        return MathDraw(rf"{lhs} {rel} {rhs}", rf"x {ans_rel} {s}",
                        hint=r"\text{dividing by a negative flips the sign}",
                        prompt="จงแก้หา x")
Inequality.PROVENANCE = Provenance("original")


@question_type("math.inequality_negative_coefficient",
               display_name={"th": "อสมการที่ต้องกลับเครื่องหมาย"},
               level={"th": "ม.2"}, topic="อสมการเชิงเส้น")
class InequalityNegativeCoefficient(MathType):
    """Dividing by a negative flips the inequality — the one rule that makes
    inequalities different from equations."""

    def expr(self, rng: Random, coef_hi: int = 9, const_hi: int = 20):
        a = -rng.randint(2, coef_hi)               # always negative
        b = rng.randint(-const_hi, const_hi)
        c = rng.randint(-const_hi, const_hi)
        bound = Fraction(c - b, a)
        rel, flipped = rng.choice([(r"\le", r"\ge"), (r"<", r">"),
                                   (r"\ge", r"\le"), (r">", r"<")])
        return MathDraw(
            rf"{poly_tex((a, 'x'), (b, ''))} {rel} {c}",
            rf"x {flipped} {frac_tex(bound)}",
            prompt="จงหาคำตอบของอสมการ",
            distractors=[rf"x {rel} {frac_tex(bound)}",
                         rf"x {flipped} {frac_tex(-bound)}",
                         rf"x {rel} {frac_tex(Fraction(c + b, a))}"])
InequalityNegativeCoefficient.PROVENANCE = Provenance("original")


@question_type("math.inequality_setup_m3",
               display_name={"th": "เขียนอสมการจากโจทย์ปัญหา"},
               level=LEGACY, topic=_INEQ_TOPIC)
class InequalitySetupM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        story, _, ineq, wrongs = _inequality_story(rng)
        return _maths([text(story), text("ถ้าให้ x แทนจำนวนที่ต้องการหา อสมการใดใช้แก้โจทย์นี้ได้")],
                      ineq, wrongs, self.topic)
InequalitySetupM3.PROVENANCE = Provenance("original")


@question_type("math.inequality_compound", display_name={"th": "อสมการประกอบ"},
               level={"th": "ม.2"}, topic="อสมการเชิงเส้น")
class InequalityCompound(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6, bound_hi: int = 20):
        a = rng.randint(2, coef_hi)
        b = rng.randint(-10, 10)
        lo_v, hi_v = sorted(rng.sample(range(-bound_hi, bound_hi), 2))
        # lo ≤ ax + b ≤ hi  ⟺  (lo−b)/a ≤ x ≤ (hi−b)/a, with a > 0.
        left, right = Fraction(lo_v - b, a), Fraction(hi_v - b, a)
        shown = rf"{lo_v} \le {poly_tex((a, 'x'), (b, ''))} \le {hi_v}"
        return MathDraw(
            shown, rf"{frac_tex(left)} \le x \le {frac_tex(right)}",
            prompt="จงหาคำตอบของอสมการ",
            distractors=[rf"{frac_tex(right)} \le x \le {frac_tex(left)}",
                         rf"{frac_tex(Fraction(lo_v + b, a))} \le x \le "
                         rf"{frac_tex(Fraction(hi_v + b, a))}",
                         rf"x \le {frac_tex(right)}"])
InequalityCompound.PROVENANCE = Provenance("original")


@question_type("math.inequality_order_properties_m3",
               display_name={"th": "สมบัติการไม่เท่ากันของจำนวนจริง"},
               level=M3, topic="อสมการเชิงเส้น")
class InequalityOrderPropertiesM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            parts, prem = rng.choice(_ORDER_PREMISES)
            true = [t for t, c in _ORDER_CLAIMS if always_order(prem, c)]
            false = [t for t, c in _ORDER_CLAIMS if not always_order(prem, c)]
            ask_true = rng.random() < 0.7
            pool_right, pool_wrong = (true, false) if ask_true else (false, true)
            if pool_right and len(pool_wrong) >= 3:
                break
        right = rng.choice(pool_right)
        rng.shuffle(pool_wrong)
        premise = [content_math(parts[0])]
        for p in parts[1:]:
            premise += [text("และ"), content_math(p)]
        ask = "ข้อใดเป็นจริงเสมอ" if ask_true else "ข้อใดไม่จำเป็นต้องเป็นจริง"
        stem = [text("กำหนดให้ a, b และ c เป็นจำนวนจริง โดยที่"), *premise, text(ask)]
        return _tex_q(stem, right, pool_wrong[:3], self.topic)
InequalityOrderPropertiesM3.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/3 จำนวนจริง',))


@question_type("math.inequality_word_problem_m3",
               display_name={"th": "โจทย์ปัญหาอสมการเชิงเส้นตัวแปรเดียว"},
               level=LEGACY, topic=_INEQ_TOPIC)
class InequalityWordProblemM3(WordProblem):
    def expr(self, rng: Random):
        story, ans, _, _ = _inequality_story(rng)
        # One past the boundary, the boundary rounded the wrong way, and one short.
        return MathDraw("", str(ans), prompt=story,
                        distractors=_story.keep(ans + 1, ans - 1, ans + 2, ans * 2, answer=ans, lo=1))
InequalityWordProblemM3.PROVENANCE = Provenance("original")

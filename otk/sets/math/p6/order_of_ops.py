"""ลำดับการดำเนินการ

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_apply_basic, math_number.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    WordProblem,
    frac_answer_tex,
    frac_tex,
    rand_proper,
)
from otk.sets._support.math_apply_add import _c

PROVENANCE = Provenance("original")


@question_type("math.order_of_ops_integers",
               display_name={"th": "ลำดับการดำเนินการ (จำนวนเต็ม)"},
               level={"th": "ป.6"}, topic="ลำดับการดำเนินการ")
class OrderOfOpsIntegers(MathType):
    def expr(self, rng: Random, lo: int = 2, hi: int = 12):
        a, b = rng.randint(lo, hi), rng.randint(lo, hi)
        # Distinct, so the bracket never collapses to zero and the item stops
        # testing anything.
        c, d = rng.sample(range(lo, hi + 1), 2)
        hi_, lo_ = max(c, d), min(c, d)
        value = a + b * (hi_ - lo_)
        # Left-to-right is the mistake this item exists to catch.
        naive = (a + b) * (hi_ - lo_)
        return MathDraw(rf"{a} + {b} \times ({hi_} - {lo_})", str(value),
                        prompt="จงหาค่าของนิพจน์",
                        distractors=[str(naive), str(a + b * hi_ - lo_),
                                     str(a + b + hi_ - lo_)])


@question_type("math.order_of_ops_powers",
               display_name={"th": "ลำดับการดำเนินการ (มีเลขยกกำลัง)"},
               level={"th": "ป.6"}, topic="ลำดับการดำเนินการ")
class OrderOfOpsPowers(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 6):
        a = rng.randint(base_lo, base_hi)
        b, c = rng.randint(2, 9), rng.randint(2, 9)
        value = b + a ** 2 * c
        return MathDraw(rf"{b} + {a}^2 \times {c}", str(value),
                        prompt="จงหาค่าของนิพจน์",
                        distractors=[str((b + a ** 2) * c), str(b + (a * c) ** 2),
                                     str(b + a * 2 * c)])


@question_type("math.order_of_ops",
               display_name={"th": "ลำดับการดำเนินการ (เศษส่วน)"},
               level={"th": "ป.6"}, topic="ลำดับการดำเนินการ")
class OrderOfOps(MathType):
    def expr(self, rng: Random, brackets: int = 1):
        while True:
            f1, f2 = rand_proper(rng, 2, 10), rand_proper(rng, 2, 10)
            f3 = (Fraction(rng.randint(2, 5)) if rng.random() < 0.3
                  else rand_proper(rng, 2, 10))
            plus = rng.random() < 0.5
            mul = rng.random() < 0.5
            use_brackets = bool(brackets) and rng.random() < 0.5
            try:
                if use_brackets:
                    t = f1 + f2 if plus else f1 - f2
                    if t <= 0:
                        continue
                    result = t * f3 if mul else t / f3
                else:
                    t = f2 * f3 if mul else f2 / f3
                    result = f1 + t if plus else f1 - t
            except ZeroDivisionError:
                continue
            if result < 0 or result.denominator > 24 or abs(result.numerator) > 60:
                continue
            break
        op1 = "+" if plus else "-"
        op2 = r"\times" if mul else r"\div"
        inner = rf"{frac_tex(f1)} {op1} {frac_tex(f2)}"
        if use_brackets:
            tex = rf"\left({inner}\right) {op2} {frac_tex(f3)}"
            hint = r"\text{brackets first}"
        else:
            tex = rf"{inner} {op2} {frac_tex(f3)}"
            hint = r"\text{multiply/divide first}"
        return MathDraw(tex, frac_answer_tex(result), hint=hint)


@question_type("math.order_of_ops_word_p6",
               display_name={"th": "เขียนประโยคสัญลักษณ์หลายขั้นตอนและหาคำตอบ"},
               level={"th": "ป.6"}, topic="ลำดับการดำเนินการ")
class OrderOfOpsWordP6(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(5)
        a, x, b, y = rng.randint(2, 6), rng.randint(15, 60), rng.randint(2, 5), rng.randint(20, 90)
        note = 500 if a * x + b * y < 500 else 1000
        if kind == 0:
            change = note - (a * x + b * y)
            return MathDraw("", str(change),
                            prompt=(f"{p}ซื้อสมุด {a} เล่ม เล่มละ {x} บาท และซื้อปากกา {b} ด้าม ด้ามละ {y} บาท "
                                    f"จ่ายเงินด้วยธนบัตร {note} บาท จะได้เงินทอนกี่บาท"),
                            distractors=_story.keep(note - a * x + b * y, a * x + b * y, note - a * x,
                                                    change + 10, answer=change, lo=0))
        if kind == 1:
            # The number sentence itself: which one has the brackets in the right place.
            return MathDraw("", rf"{note} - ({a} \times {x} + {b} \times {y})",
                            prompt=(f"{p}ซื้อสมุด {a} เล่ม เล่มละ {x} บาท และปากกา {b} ด้าม ด้ามละ {y} บาท "
                                    f"จ่ายด้วยธนบัตร {note} บาท ประโยคสัญลักษณ์ใดใช้หาเงินทอนได้ถูกต้อง"),
                            distractors=[rf"{note} - {a} \times {x} + {b} \times {y}",
                                         rf"({note} - {a}) \times {x} + {b} \times {y}",
                                         rf"{note} - ({a} + {b}) \times ({x} + {y})"])
        if kind == 2:
            n, keep = rng.randint(3, 8), rng.randint(2, 9) * 10
            share = rng.randint(20, 120)
            total = keep + n * share
            return MathDraw("", str(share),
                            prompt=(f"{p}มีเงิน {total} บาท เก็บไว้เอง {keep} บาท ที่เหลือแบ่งให้น้อง {n} คน คนละเท่า ๆ กัน "
                                    f"น้องได้คนละกี่บาท"),
                            distractors=_story.keep(total // n if total % n == 0 else share + keep // n,
                                                    total - keep // n, share + 1, answer=share, lo=1))
        if kind == 3:
            adults, kids, price, disc = rng.randint(2, 5), rng.randint(2, 6), rng.choice((80, 100, 120, 160)), rng.choice((20, 50, 100))
            total = adults * price + kids * (price // 2) - disc
            return MathDraw("", _c(total),
                            prompt=(f"บัตรชมการแสดงราคาผู้ใหญ่ใบละ {price} บาท เด็กจ่ายครึ่งราคา ครอบครัวหนึ่งมีผู้ใหญ่ {adults} คน "
                                    f"เด็ก {kids} คน และมีคูปองส่วนลด {disc} บาท ครอบครัวนี้ต้องจ่ายกี่บาท"),
                            distractors=[_c((adults + kids) * price - disc), _c(adults * price + kids * (price // 2)),
                                         _c((adults + kids) * (price // 2) - disc)])
        s1, s2 = rng.randint(55, 90), rng.randint(55, 90)
        target = rng.randint(70, 85)
        need = 3 * target - s1 - s2
        if not 40 <= need <= 100:
            need = max(40, min(100, need))
            target = (s1 + s2 + need) // 3
            need = 3 * target - s1 - s2
        return MathDraw("", str(need),
                        prompt=(f"{p}สอบสองครั้งได้ {s1} และ {s2} คะแนน ครั้งที่สามต้องได้กี่คะแนน "
                                f"คะแนนเฉลี่ยทั้งสามครั้งจึงจะเท่ากับ {target} คะแนน"),
                        # the target itself; averaging the two scores with the target; the two-score mean
                        distractors=_story.keep(target, 2 * target - (s1 + s2) // 2, (s1 + s2) // 2,
                                                need + 3, answer=need, lo=0))


from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
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


# ── More order of operations (2026-11): with decimals, division before addition, nested brackets, the true
# statement, a missing number, and change from a payment ──


@question_type("math.ooo_decimal_p6", display_name={"th": "ลำดับการดำเนินการกับทศนิยม"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class OooDecimalP6(MathType):
    def expr(self, rng: Random):
        a = rng.randint(11, 99)
        b = rng.randint(11, 49)
        k = rng.randint(2, 5)
        plus = rng.random() < 0.5
        if not plus:
            a = b * k + rng.randint(1, 60)
        right = a + b * k if plus else a - b * k
        left = (a + b) * k if plus else (a - b) * k
        op = "+" if plus else "-"
        # Worked left to right; the multiplier missed; a point slipped.
        return MathDraw(f"{_d6(a, 1)} {op} {_d6(b, 1)} \\times {k}", _d6(right, 1), prompt="จงหาค่าของนิพจน์",
                        distractors=_dk6(left, a + b if plus else a - b, right * 10, right + 10,
                                         answer=right, places=1, lo=1))


@question_type("math.ooo_division_first_p6", display_name={"th": "หารก่อนบวกลบ"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class OooDivisionFirstP6(MathType):
    def expr(self, rng: Random):
        c = rng.randint(2, 9)
        q = rng.randint(2, 12)
        b = c * q
        a = rng.randint(5, 60)
        d = rng.randint(2, 5)
        right = a + q * d
        # Left to right; the multiplication first and then the division; the division only.
        ltr = (a + b) // c * d if (a + b) % c == 0 else (a + b) * d // c
        return MathDraw(f"{a} + {b} \\div {c} \\times {d}", str(right), prompt="จงหาค่าของนิพจน์",
                        distractors=_story.keep(ltr, a + b // (c * d) if b % (c * d) == 0 else a + q + d, a + q,
                                                right + d, answer=right, lo=1))


@question_type("math.ooo_nested_p6", display_name={"th": "วงเล็บซ้อนกัน"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class OooNestedP6(MathType):
    def expr(self, rng: Random):
        c, d = rng.randint(1, 9), rng.randint(1, 9)
        b = c + d + rng.randint(1, 15)
        a = rng.randint(2, 9)
        right = a * (b - (c + d))
        # The inner bracket ignored (b - c + d); the outer one ignored (a × b - c - d); added instead of multiplied.
        return MathDraw(f"{a} \\times [{b} - ({c} + {d})]", str(right), prompt="จงหาค่าของนิพจน์",
                        distractors=_story.keep(a * (b - c + d), a * b - c - d, a + b - c - d, right + a,
                                                answer=right, lo=1))


@question_type("math.ooo_true_statement_p6", display_name={"th": "ประโยคใดถูกต้องตามลำดับการดำเนินการ"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class OooTrueStatementP6(ChoiceType):
    def compose(self, rng: Random):
        a, b, c = rng.randint(2, 20), rng.randint(2, 9), rng.randint(2, 9)
        right_v = a + b * c
        ltr = (a + b) * c
        right = f"{a} + {b} × {c} = {right_v}"
        wrongs = [f"{a} + {b} × {c} = {ltr}", f"{a} × {b} + {c} = {a * (b + c)}", f"({a} + {b}) × {c} = {a + b * c + 1}"]
        return "ข้อใดถูกต้อง", right, wrongs


@question_type("math.ooo_missing_number_p6", display_name={"th": "หาจำนวนที่หายไปในนิพจน์"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class OooMissingNumberP6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 9)
        right = rng.randint(2, 15)
        c = rng.randint(1, 30)
        total = k * right + c
        # Undone in the wrong order; the constant left in; one off.
        wrong_order = total // k - c if total // k > c else c + right
        return MathDraw(f"{k} \\times \\square + {c} = {total}", str(right),
                        prompt="จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_story.keep(wrong_order, total - c, (total + c) // k, right + 1,
                                                answer=right, lo=1))


@question_type("math.change_after_shopping_p6", display_name={"th": "เงินทอนหลังซื้อของสองชนิด"},
               level=LEVEL, topic="ลำดับการดำเนินการ")
class ChangeAfterShoppingP6(WordProblem):
    def expr(self, rng: Random):
        n1, p1 = rng.randint(2, 6), rng.randint(8, 45)
        n2, p2 = rng.randint(2, 6), rng.randint(5, 30)
        cost = n1 * p1 + n2 * p2
        paid = next(v for v in (100, 200, 500, 1000) if v > cost)
        right = paid - cost
        x, y = rng.sample(("สมุด", "ปากกา", "ดินสอ", "ไม้บรรทัด", "ยางลบ"), 2)
        prompt = (f"ซื้อ{x} {n1} ชิ้น ชิ้นละ {p1} บาท และ{y} {n2} ชิ้น ชิ้นละ {p2} บาท "
                  f"จ่ายเงิน {paid:,} บาท ได้เงินทอนกี่บาท")
        # One price per kind; the cost; the counts added before multiplying.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(paid - p1 - p2, cost, paid - (n1 + n2) * p1, right + 10,
                                                answer=right, lo=1))

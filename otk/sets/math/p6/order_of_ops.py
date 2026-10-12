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

"""จำนวนตรรกยะ

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_apply_basic, math_number, math_pictures_hi.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_answer_tex, frac_tex
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_apply_add import _fr as _fr_math_apply_basic
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_pictures_hi import FRAC_LINES

PROVENANCE = Provenance("original")


def _signed(v) -> str:
    if isinstance(v, Fraction):
        return _fr_math_apply_basic(v)
    return str(v)


def _fr(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f < 0 else ""
    return rf"{sign}\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"


FRAC_ALT = "ภาพเส้นจำนวนตั้งแต่ -2 ถึง 2 แบ่งช่องเท่า ๆ กัน และมีจุด A"


@question_type("math.largest_rational", display_name={"th": "จำนวนตรรกยะที่มากที่สุด"},
               level={"th": "ม.1"}, topic="จำนวนตรรกยะ")
class LargestRational(MathType):
    """Comparing signed fractions — the place where "bigger digits" stops working."""

    def expr(self, rng: Random, den_hi: int = 8):
        vals: list[Fraction] = []
        while len(vals) < 4:
            f = Fraction(rng.randint(1, 9), rng.randint(2, den_hi))
            f = -f if rng.random() < 0.5 else f
            if f not in vals:
                vals.append(f)
        best = max(vals)
        shown = r",\quad ".join(frac_tex(v) for v in vals)
        return MathDraw(shown, frac_tex(best),
                        prompt="จำนวนใดมีค่ามากที่สุด",
                        distractors=[frac_tex(v) for v in vals if v != best])


@question_type("math.fraction_number_line_m1", display_name={"th": "อ่านจำนวนตรรกยะจากเส้นจำนวน"},
               level={"th": "ม.1"}, topic="จำนวนตรรกยะ")
class FractionNumberLineM1(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(FRAC_LINES)
        v = f.value
        # The wrong sign; counting ticks as whole units; a tick off.
        wrongs = [_fr(-v), _fr(Fraction(f.k, f.d + 1)), _fr(v + Fraction(1, f.d)),
                  _fr(v - Fraction(1, f.d)), str(f.k)]
        right = _fr(v)
        return _math_q([text("จุด A บนเส้นจำนวนแทนจำนวนใด"), image(f.asset_id, alt=FRAC_ALT)],
                       right, [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.signed_fraction_muldiv",
               display_name={"th": "คูณ/หารเศษส่วนมีเครื่องหมาย"},
               level={"th": "ม.1"}, topic="จำนวนตรรกยะ")
class SignedFractionMulDiv(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, den_hi: int = 9, num_hi: int = 9):
        def pick() -> Fraction:
            f = Fraction(rng.randint(1, num_hi), rng.randint(2, den_hi))
            return -f if rng.random() < 0.5 else f

        a, b = pick(), pick()
        if rng.random() < 0.5:
            ans, op = a * b, r"\times"
        else:
            ans, op = a / b, r"\div"
        return MathDraw(rf"\left({frac_tex(a)}\right) {op} \left({frac_tex(b)}\right)",
                        frac_tex(ans),
                        prompt="จงหาผลลัพธ์",
                        distractors=[frac_tex(-ans), frac_tex(abs(ans)),
                                     frac_tex(a * b if op == r"\div" else a / b)])


@question_type("math.signed_fraction_ops",
               display_name={"th": "บวก/ลบเศษส่วนมีเครื่องหมาย"}, level={"th": "ม.1"},
               topic="จำนวนตรรกยะ")
class SignedFractionOps(MathType):
    def expr(self, rng: Random):
        while True:
            f1 = Fraction(rng.choice([1, -1]) * rng.randint(1, 7), rng.randint(2, 9))
            f2 = Fraction(rng.choice([1, -1]) * rng.randint(1, 7), rng.randint(2, 9))
            op = rng.choice("+-")
            res = f1 + f2 if op == "+" else f1 - f2
            wrong = f1 - f2 if op == "+" else f1 + f2   # sign-of-op mistake
            if res != wrong and res.denominator <= 24 and abs(res.numerator) <= 40:
                break
        return MathDraw(rf"{frac_tex(f1)} {op} {frac_tex(f2)}",
                        frac_answer_tex(res),
                        distractors=[frac_answer_tex(wrong), frac_answer_tex(-res)])


@question_type("math.signed_number_context_m1",
               display_name={"th": "โจทย์ปัญหาจำนวนเต็มและจำนวนตรรกยะที่เป็นลบ"},
               level={"th": "ม.1"}, topic="จำนวนตรรกยะ")
class SignedNumberContextM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            start, up, down = -rng.randint(3, 15), rng.randint(5, 20), rng.randint(4, 18)
            end = start + up - down
            return MathDraw("", str(end),
                            prompt=(f"ตอนเช้าอุณหภูมิ {start} องศาเซลเซียส ตอนบ่ายสูงขึ้น {up} องศา "
                                    f"ตอนกลางคืนลดลง {down} องศา ตอนกลางคืนอุณหภูมิกี่องศาเซลเซียส"),
                            distractors=[str(-start + up - down), str(start - up + down), str(start + up + down)])
        if kind == 1:
            peak, depth = rng.randint(200, 900), rng.randint(20, 90)
            return MathDraw("", _c(peak + depth),
                            prompt=(f"ยอดเขาสูงจากระดับน้ำทะเล {peak} เมตร นักดำน้ำอยู่ที่ระดับ -{depth} เมตร "
                                    f"ยอดเขาอยู่สูงกว่านักดำน้ำกี่เมตร"),
                            distractors=[_c(peak - depth), _c(peak), _c(depth)])
        if kind == 2:
            bal, w1, dep, w2 = rng.randint(2, 9) * 100, rng.randint(5, 15) * 100, rng.randint(2, 8) * 100, rng.randint(1, 6) * 100
            end = bal - w1 + dep - w2
            return MathDraw("", _c(end) if end >= 0 else "-" + _c(-end),
                            prompt=(f"บัญชีมีเงิน {bal} บาท ถอนเงิน {_c(w1)} บาท (ใช้วงเงินเบิกเกินบัญชีได้) ฝากเงิน {dep} บาท "
                                    f"แล้วถอนอีก {w2} บาท ยอดเงินในบัญชีเป็นเท่าใด (ติดลบหมายถึงเป็นหนี้)"),
                            distractors=[str(bal + w1 + dep - w2), str(-end) if end else "100",
                                         str(bal - w1 - dep - w2)])
        if kind == 3:
            while True:
                temps = [rng.randint(-12, 6) for _ in range(5)]
                if sum(temps) % 5 == 0:
                    break
            mean = sum(temps) // 5
            shown = ", ".join(str(t) for t in temps)
            return MathDraw("", str(mean),
                            prompt=(f"อุณหภูมิต่ำสุดของเมืองหนึ่งใน 5 วัน คือ {shown} องศาเซลเซียส "
                                    f"อุณหภูมิเฉลี่ยของ 5 วันนี้เป็นกี่องศาเซลเซียส"),
                            distractors=[str(sum(abs(t) for t in temps) // 5), str(-mean) if mean else "1",
                                         str(sum(temps))])
        per = Fraction(rng.choice((1, 3)), 4)
        days = rng.randint(3, 9)
        start = Fraction(rng.randint(2, 6))
        end = start - per * days
        return MathDraw("", _signed(end),
                        prompt=(f"ระดับน้ำในอ่างเก็บน้ำอยู่สูงกว่าระดับปกติ {start} เมตร ลดลงวันละ {per.numerator}/{per.denominator} เมตร "
                                f"เป็นเวลา {days} วัน ระดับน้ำเทียบกับระดับปกติเป็นกี่เมตร (ต่ำกว่าระดับปกติให้ตอบเป็นจำนวนลบ)"),
                        distractors=[_signed(start + per * days), _signed(per * days), _signed(-end) if end else "1"])


# ── More rational numbers (2026-11): a number between two, mixed operations, opposites and reciprocals,
# fractions of an amount, and powers of fractions ──

from otk.kit import story as _story  # noqa: E402
from otk.sets._support.math_m1 import LEVEL  # noqa: E402

_RAT_TOPIC = "จำนวนตรรกยะ"


@question_type("math.rational_between_m1", display_name={"th": "จำนวนตรรกยะที่อยู่ระหว่างสองจำนวน"},
               level=LEVEL, topic=_RAT_TOPIC)
class RationalBetweenM1(WordProblem):
    def expr(self, rng: Random):
        while True:
            b, d = rng.randint(2, 9), rng.randint(2, 9)
            p, q = Fraction(rng.randint(-9, 9), b), Fraction(rng.randint(-9, 9), d)
            lo, hi = min(p, q), max(p, q)
            if hi - lo >= Fraction(1, 4) and lo.denominator > 1 and hi.denominator > 1:
                break
        mid = (lo + hi) / 2
        # Outside on either side, and one end itself.
        wrongs = [lo - Fraction(1, 2), hi + Fraction(1, 2), lo if lo != mid else hi + 1]
        return MathDraw("", frac_tex(mid),
                        prompt=f"จำนวนในข้อใดอยู่ระหว่าง {_plain_frac(lo)} และ {_plain_frac(hi)}",
                        distractors=[frac_tex(w) for w in dict.fromkeys(wrongs) if w != mid])


def _plain_frac(f: Fraction) -> str:
    return str(f.numerator).replace("-", "−") + (f"/{f.denominator}" if f.denominator > 1 else "")


@question_type("math.rational_mixed_ops_m1", display_name={"th": "บวก ลบ คูณ หารจำนวนตรรกยะหลายขั้น"},
               level=LEVEL, topic=_RAT_TOPIC)
class RationalMixedOpsM1(WordProblem):
    def expr(self, rng: Random):
        a = Fraction(rng.choice([-1, 1]) * rng.randint(1, 5), rng.choice((2, 3, 4)))
        b = Fraction(rng.choice([-1, 1]) * rng.randint(1, 5), rng.choice((2, 4, 6)))
        k = rng.choice((-6, -4, -3, 2, 3, 4, 6))
        right = (a + b) * k
        k_tex = f"({k})" if k < 0 else str(k)
        b_tex = rf"\left({frac_tex(b)}\right)" if b < 0 else frac_tex(b)
        tex = rf"\left({frac_tex(a)} + {b_tex}\right) \times {k_tex}"
        # Only b multiplied; the sign of k dropped; the fractions added by tops and bottoms.
        tops = Fraction(a.numerator + b.numerator, a.denominator + b.denominator) * k
        wrongs = [a + b * k, (a + b) * abs(k) if k < 0 else -(a + b) * k, tops]
        return MathDraw(tex, frac_tex(right), prompt="จงหาค่าของ",
                        distractors=[frac_tex(w) for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.rational_inverse_m1", display_name={"th": "ตัวผกผันการบวกและการคูณของจำนวนตรรกยะ"},
               level=LEVEL, topic=_RAT_TOPIC)
class RationalInverseM1(WordProblem):
    def expr(self, rng: Random):
        while True:
            q = Fraction(rng.choice([-1, 1]) * rng.randint(1, 9), rng.randint(2, 9))
            if q.denominator > 1 and abs(q.numerator) > 1:
                break
        if rng.random() < 0.5:
            right = 1 / q
            # The opposite instead; the sign flipped too; the number itself.
            return MathDraw("", frac_tex(right), prompt=f"ตัวผกผันการคูณของ {_plain_frac(q)} คือข้อใด",
                            distractors=[frac_tex(w) for w in (-q, -right, q)])
        right = -q
        return MathDraw("", frac_tex(right), prompt=f"ตัวผกผันการบวกของ {_plain_frac(q)} คือข้อใด",
                        distractors=[frac_tex(w) for w in (1 / q, -1 / q, q)])


@question_type("math.fraction_of_amount_m1", display_name={"th": "โจทย์ปัญหาเศษส่วนของปริมาณ"},
               level=LEVEL, topic=_RAT_TOPIC)
class FractionOfAmountM1(WordProblem):
    """Used a fraction, then a fraction of what was left."""

    def expr(self, rng: Random):
        a, b = rng.choice(((1, 4), (1, 3), (2, 5), (1, 2), (3, 8))), rng.choice(((1, 3), (1, 2), (2, 3), (1, 4)))
        first, second = Fraction(*a), Fraction(*b)
        unit = (first.denominator * second.denominator)
        total = unit * rng.randint(2, 8)
        left = total * (1 - first) * (1 - second)
        prompt = (f"มีเงิน {total} บาท ใช้ไป {a[0]}/{a[1]} ของเงินทั้งหมด แล้วใช้อีก {b[0]}/{b[1]} ของเงินที่เหลือ "
                  f"เหลือเงินกี่บาท")
        # The second fraction taken of the whole; the fractions added first; only the first step.
        wrongs = [total * (1 - first - second), total * (1 - first) * second, total * (1 - first)]
        return MathDraw("", str(int(left)), prompt=prompt,
                        distractors=_story.keep(*[int(w) for w in wrongs if w == int(w)], answer=int(left), lo=1))


@question_type("math.fraction_power_m1", display_name={"th": "เลขยกกำลังของเศษส่วน"},
               level=LEVEL, topic=_RAT_TOPIC)
class FractionPowerM1(WordProblem):
    def expr(self, rng: Random):
        n, d = rng.randint(1, 5), rng.randint(2, 6)
        while n == d or Fraction(n, d).denominator == 1:
            n, d = rng.randint(1, 5), rng.randint(2, 6)
        sign = rng.choice((1, -1))
        e = rng.choice((2, 3))
        base = Fraction(sign * n, d)
        right = base ** e
        tex = rf"\left({frac_tex(base)}\right)^{{{e}}}"
        # The sign kept positive; only the top raised; multiplied by the exponent.
        wrongs = [abs(right), Fraction((sign * n) ** e, d), base * e]
        return MathDraw(tex, frac_tex(right), prompt="จงหาค่าของ",
                        distractors=[frac_tex(w) for w in dict.fromkeys(wrongs) if w != right])

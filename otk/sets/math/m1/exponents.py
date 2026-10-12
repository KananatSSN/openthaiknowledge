"""เลขยกกำลัง

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_apply_basic, math_formats_hi, math_number.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q

PROVENANCE = Provenance("original")


def _sci(m: Decimal, e: int) -> tuple[Decimal, int]:
    while m >= 10:
        m, e = m / 10, e + 1
    while m < 1:
        m, e = m * 10, e - 1
    return m.normalize(), e


def _sci_tex(m: Decimal, e: int) -> str:
    m, e = _sci(m, e)
    return rf"{m} \times 10^{{{e}}}"


_SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _sup(n: int) -> str:
    return str(n).translate(_SUP)


def _sci_math_formats_hi(m: float, e: int) -> str:
    return rf"{m:g} \times 10^{{{e}}}"


@question_type("math.power_of_2",
               display_name={"th": "กำลังของ 2"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class PowerOf2(MathType):
    def expr(self, rng: Random, n_lo: int = 2, n_hi: int = 10):
        n = rng.randint(n_lo, n_hi)
        return rf"2^{{{n}}}", rf"{2 ** n}"


@question_type("math.zero_exponent",
               display_name={"th": "เลขชี้กำลังศูนย์"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class ZeroExponent(MathType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random, lo: int = 10, hi: int = 99):
        base = rng.randint(lo, hi)
        return MathDraw(rf"{base}^{{0}}", "1", hint=r"a^0 = 1")


@question_type("math.power_of_negative",
               display_name={"th": "กำลังของจำนวนลบ"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class PowerOfNegative(MathType):
    def expr(self, rng: Random, base_lo: int = 1, base_hi: int = 3,
             n_lo: int = 2, n_hi: int = 6):
        base = rng.randint(base_lo, base_hi)
        n = rng.randint(n_lo, n_hi)
        if rng.random() < 0.5:
            val = (-base) ** n
            problem = rf"\left(-{base}\right)^{{{n}}}"
        else:
            val = -((-base) ** n)
            problem = rf"-\left(-{base}\right)^{{{n}}}"
        return MathDraw(problem, rf"{val}",
                        hint=r"\text{odd} \Rightarrow -, \ \text{even} \Rightarrow +")


@question_type("math.product_rule",
               display_name={"th": "เลขยกกำลัง: คูณฐานเดียวกัน"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class ProductRule(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 9,
             exp_lo: int = 1, exp_hi: int = 7):
        base = rng.randint(base_lo, base_hi)
        m, n = rng.randint(exp_lo, exp_hi), rng.randint(exp_lo, exp_hi)
        return MathDraw(rf"{base}^{{{m}}} \cdot {base}^{{{n}}}", rf"{base}^{{{m + n}}}",
                        hint=r"a^m \cdot a^n = a^{m+n}")


@question_type("math.power_rule",
               display_name={"th": "เลขยกกำลัง: กำลังซ้อนกำลัง"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class PowerRule(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 5,
             m_lo: int = 2, m_hi: int = 5, n_lo: int = 2, n_hi: int = 4):
        base = rng.randint(base_lo, base_hi)
        m, n = rng.randint(m_lo, m_hi), rng.randint(n_lo, n_hi)
        return MathDraw(rf"\left({base}^{{{m}}}\right)^{{{n}}}", rf"{base}^{{{m * n}}}",
                        hint=r"(a^m)^n = a^{m \cdot n}")


@question_type("math.scientific_notation",
               display_name={"th": "สัญกรณ์วิทยาศาสตร์"}, level={"th": "ม.1"},
               topic="เลขยกกำลัง")
class ScientificNotation(WordProblem):
    def expr(self, rng: Random):
        while True:
            c = rng.randint(11, 99999)
            if c % 10:                              # no trailing zero → clean form
                break
        e = len(str(c)) - 1
        m = f"{c / 10 ** e:g}"
        form = "ในรูป a × 10ⁿ (1 ≤ a < 10)"
        prompt = rng.choice((
            f"เขียน {c} {form} ได้เท่าใด?",
            f"อำเภอหนึ่งมีประชากร {c} คน เขียนจำนวนประชากร{form} ได้เท่าใด",
            f"ห้องสมุดมีหนังสือ {c} เล่ม เขียนจำนวนหนังสือ{form} ได้เท่าใด",
            f"รถยนต์คันหนึ่งวิ่งมาแล้ว {c} กิโลเมตร เขียนระยะทางนี้{form} ได้เท่าใด",
        ))
        return MathDraw(
            "", rf"{m} \times 10^{{{e}}}", prompt=prompt,
            distractors=[rf"{m} \times 10^{{{e + 1}}}",
                         rf"{m} \times 10^{{{e - 1}}}",
                         rf"{c / 10 ** (e - 1):g} \times 10^{{{e - 1}}}"])


@question_type("math.scientific_compare_m1", display_name={"th": "เปรียบเทียบจำนวนในรูปสัญกรณ์วิทยาศาสตร์"},
               level={"th": "ม.1"}, topic="เลขยกกำลัง")
class ScientificCompareM1(QuestionType):
    """The exponent decides first; a big front number with a smaller exponent
    is the trap."""

    def build(self, rng: Random) -> GeneratedQuestion:
        e = rng.choice((rng.randint(3, 9), -rng.randint(2, 7)))
        largest = rng.random() < 0.5
        mants = rng.sample([x / 10 for x in range(11, 100)], 4)
        mants.sort()
        top = e + 1 if largest else e - 1
        # The winner has the smallest front number; the trap has the largest.
        exps = [top, e, e, e - 1 if largest else e + 1]
        values = list(zip(mants, exps))
        answer = values[0]
        return _math_q([text("จำนวนใดมีค่า" + ("มากที่สุด" if largest else "น้อยที่สุด"))],
                       _sci_math_formats_hi(*answer), [_sci_math_formats_hi(m, x) for m, x in values[1:]], self.topic)


@question_type("math.scientific_to_decimal",
               display_name={"th": "สัญกรณ์วิทยาศาสตร์เป็นจำนวนเต็ม"},
               level={"th": "ม.1"}, topic="เลขยกกำลัง")
class ScientificToDecimal(MathType):
    def expr(self, rng: Random, exp_lo: int = 2, exp_hi: int = 6):
        lead = rng.randint(10, 99) / 10          # one digit before the point
        e = rng.randint(exp_lo, exp_hi)
        value = int(round(lead * 10 ** e))
        shown = f"{lead:g}"
        return MathDraw(rf"{shown} \times 10^{{{e}}}", str(value),
                        prompt="เขียนจำนวนนี้ในรูปจำนวนเต็ม",
                        distractors=[str(int(round(lead * 10 ** (e + 1)))),
                                     str(int(round(lead * 10 ** (e - 1)))),
                                     str(int(round(lead * 10)) * e)])


@question_type("math.scientific_notation_word_m1",
               display_name={"th": "โจทย์ปัญหาสัญกรณ์วิทยาศาสตร์"},
               level={"th": "ม.1"}, topic="เลขยกกำลัง")
class ScientificNotationWordM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            t_m, t_e = rng.choice((2, 4, 5, 6)), rng.randint(1, 3)
            m, e = Decimal(3) * t_m, 8 + t_e
            return MathDraw("", _sci_tex(m, e),
                            prompt=(f"แสงเดินทางด้วยอัตราเร็ว 3 × 10⁸ เมตรต่อวินาที ในเวลา {t_m} × 10{_sup(t_e)} วินาที "
                                    f"แสงเดินทางได้กี่เมตร"),
                            # exponents multiplied; the product left unnormalised; mantissas added
                            distractors=[_sci_tex(m, 8 * t_e),
                                         rf"{m} \times 10^{{{e}}}" if m >= 10 else _sci_tex(m, e + 1),
                                         _sci_tex(Decimal(3 + t_m), e)])
        if kind == 1:
            n_m, n_e = rng.choice((2, 4, 5, 8)), rng.randint(9, 13)
            w_m, w_e = rng.choice((Decimal("1.5"), Decimal(2), Decimal("2.5"), Decimal(3))), -rng.randint(9, 12)
            return MathDraw("", _sci_tex(n_m * w_m, n_e + w_e),
                            prompt=(f"อวัยวะหนึ่งมีเซลล์ประมาณ {n_m} × 10{_sup(n_e)} เซลล์ แต่ละเซลล์มีมวลประมาณ "
                                    f"{w_m} × 10{_sup(w_e)} กรัม เซลล์ทั้งหมดมีมวลรวมประมาณกี่กรัม"),
                            distractors=[_sci_tex(n_m * w_m, n_e - w_e), _sci_tex(n_m + w_m, n_e + w_e),
                                         _sci_tex(n_m * w_m, n_e + w_e + 1)])
        if kind == 2:
            body, d_m, d_e = rng.choice((("ดวงอาทิตย์", Decimal("1.5"), 11), ("ดวงจันทร์", Decimal("3.84"), 8),
                                         ("ดาวอังคาร (ขณะอยู่ใกล้โลก)", Decimal("2.25"), 11),
                                         ("ดาวศุกร์ (ขณะอยู่ใกล้โลก)", Decimal("4.2"), 10)))
            s_m, s_e = Decimal(3), 8
            return MathDraw("", _sci_tex(d_m / s_m, d_e - s_e),
                            prompt=(f"{body}อยู่ห่างจากโลกประมาณ {d_m} × 10{_sup(d_e)} เมตร แสงเดินทางด้วยอัตราเร็ว "
                                    f"3 × 10⁸ เมตรต่อวินาที แสงจาก{body.split(' ')[0]}ใช้เวลากี่วินาทีจึงมาถึงโลก"),
                            distractors=[_sci_tex(s_m / d_m, d_e - s_e), _sci_tex(d_m / s_m, d_e + s_e),
                                         _sci_tex(d_m * s_m, d_e - s_e)])
        if kind == 3:
            n_m, n_e = rng.choice((2, 3, 4, 5)), rng.randint(3, 6)
            k = rng.randint(2, 4)
            return MathDraw("", _sci_tex(Decimal(n_m), n_e + k),
                            prompt=(f"เดิมมีแบคทีเรีย {n_m} × 10{_sup(n_e)} เซลล์ ต่อมาจำนวนเพิ่มขึ้นเป็น 10{_sup(k)} เท่า "
                                    f"มีแบคทีเรียกี่เซลล์"),
                            distractors=[_sci_tex(Decimal(n_m), n_e * k), _sci_tex(Decimal(n_m * 10), n_e + k),
                                         _sci_tex(Decimal(n_m), n_e + k - 1)])
        return self._files(rng)

    def _files(self, rng: Random):
        size_m, size_e = rng.choice((Decimal("2.5"), Decimal(4), Decimal("1.2"), Decimal(5))), rng.randint(6, 8)
        n_m, n_e = rng.choice((2, 3, 4, 6)), rng.randint(2, 4)
        return MathDraw("", _sci_tex(size_m * n_m, size_e + n_e),
                        prompt=(f"ไฟล์ภาพหนึ่งไฟล์มีขนาด {size_m} × 10{_sup(size_e)} ไบต์ ถ้ามีไฟล์ภาพ "
                                f"{n_m} × 10{_sup(n_e)} ไฟล์ ขนาดรวมเป็นกี่ไบต์"),
                        distractors=[_sci_tex(size_m * n_m, size_e * n_e), _sci_tex(size_m + n_m, size_e + n_e),
                                     _sci_tex(size_m * n_m, size_e + n_e + 1)])


@question_type("math.scientific_multiply",
               display_name={"th": "คูณในสัญกรณ์วิทยาศาสตร์"},
               level={"th": "ม.1"}, topic="เลขยกกำลัง")
class ScientificMultiply(MathType):
    def expr(self, rng: Random, exp_lo: int = 2, exp_hi: int = 8):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        p, q = rng.randint(exp_lo, exp_hi), rng.randint(exp_lo, exp_hi)
        prod, e = a * b, p + q
        if prod >= 10:                            # renormalize to 1 ≤ m < 10
            mantissa, e = f"{prod / 10:g}", e + 1
        else:
            mantissa = str(prod)
        return MathDraw(
            rf"({a} \times 10^{{{p}}})({b} \times 10^{{{q}}})",
            rf"{mantissa} \times 10^{{{e}}}",
            prompt="จงหาผลคูณในรูปสัญกรณ์วิทยาศาสตร์",
            # The classic slips: forgetting to renormalize, and multiplying the
            # exponents instead of adding them.
            distractors=[rf"{prod} \times 10^{{{p + q}}}",
                         rf"{mantissa} \times 10^{{{p * q}}}",
                         rf"{a + b} \times 10^{{{p + q}}}"])

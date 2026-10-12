"""ฟังก์ชันเชิงเส้น

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: —

Sets moved here from: math, math_algebra, math_apply_basic, math_diagrams.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_diagrams import LINE_FN_ALT, LINE_FNS, _img, _math_q

PROVENANCE = Provenance("original")


def _line_tex(m: int, c: int) -> str:
    mx = "x" if m == 1 else "-x" if m == -1 else f"{m}x"
    return f"y = {mx}" + (f" + {c}" if c > 0 else f" - {-c}" if c < 0 else "")


@question_type("math.linear_function_graph_m2", display_name={"th": "หาสมการของเส้นตรงจากกราฟ"},
               level={"th": "ม.2"}, topic="ฟังก์ชันเชิงเส้น")
class LinearFunctionGraphM2(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        fn = rng.choice(LINE_FNS)
        img = _img(fn.asset_id, LINE_FN_ALT)
        m, c = fn.m, fn.c
        if rng.random() < 0.5:
            # Slope and intercept swapped, the slope's sign lost, rise over run inverted.
            wrongs = [_line_tex(c, m) if c else _line_tex(m, 1), _line_tex(-m, c),
                      _line_tex(m, -c) if c else _line_tex(m, 2), _line_tex(m + 1, c),
                      _line_tex(m, c + 1), _line_tex(m - 1, c) if m != 1 else _line_tex(2, c)]
            return _math_q([text("สมการของเส้นตรงในกราฟคือข้อใด"), img], _line_tex(m, c), wrongs,
                           self.topic)
        inv = frac_tex(Fraction(1, m))
        return _math_q([text("เส้นตรงในกราฟมีความชันเท่าใด"), img], str(m),
                       [str(-m), inv, str(c) if c != m else str(m + 1), str(m + 1)], self.topic)


@question_type("math.linear_function",
               display_name={"th": "หาสมการเส้นตรงจากสองจุด"}, level={"th": "ม.2"},
               topic="ฟังก์ชันเชิงเส้น")
class LinearFunction(MathType):
    def expr(self, rng: Random):
        m = rng.choice([1, -1]) * rng.randint(1, 4)
        c = rng.randint(-9, 9)
        x1, x2 = rng.sample(range(-5, 6), 2)
        return MathDraw(
            rf"({x1}, {m * x1 + c}), \;\; ({x2}, {m * x2 + c})",
            rf"y = {poly_tex((m, 'x'), (c, ''))}",
            hint=r"m = \frac{y_2 - y_1}{x_2 - x_1}",
            prompt="จงหาสมการเส้นตรงที่ผ่านจุดทั้งสอง")


@question_type("math.linear_function_from_table",
               display_name={"th": "หาสมการเส้นตรงจากตารางค่า"},
               level={"th": "ม.2"}, topic="ฟังก์ชันเชิงเส้น")
class LinearFunctionFromTable(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, slope_hi: int = 6, intercept_hi: int = 10):
        m = _nonzero(rng, -slope_hi, slope_hi)
        b = rng.randint(-intercept_hi, intercept_hi)
        xs = sorted(rng.sample(range(-5, 6), 3))
        rows = r",\quad ".join(f"({x}, {m * x + b})" for x in xs)
        return MathDraw(
            rows, f"y = {poly_tex((m, 'x'), (b, ''))}",
            prompt="จุดเหล่านี้อยู่บนเส้นตรงเดียวกัน จงหาสมการของเส้นตรง",
            distractors=[f"y = {poly_tex((-m, 'x'), (b, ''))}",
                         f"y = {poly_tex((m, 'x'), (-b, ''))}",
                         f"y = {poly_tex((b, 'x'), (m, ''))}"])


@question_type("math.linear_model_compare_m2",
               display_name={"th": "เปรียบเทียบสองแบบจำลองเชิงเส้น (โปรโมชัน ค่าโดยสาร)"},
               level={"th": "ม.2"}, topic="ฟังก์ชันเชิงเส้น")
class LinearModelCompareM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            r1, r2 = rng.choice(((1, 3), (2, 4), (1, 2), (2, 5), (1, 4)))
            n = rng.randint(20, 80)
            a = rng.randint(1, 9) * 10
            b = a + (r2 - r1) * n
            return MathDraw("", str(n),
                            prompt=(f"โปรโมชันโทรศัพท์แบบ A ค่าบริการรายเดือน {b} บาท บวกนาทีละ {r1} บาท "
                                    f"แบบ B ค่าบริการรายเดือน {a} บาท บวกนาทีละ {r2} บาท "
                                    f"โทรกี่นาทีต่อเดือนค่าใช้จ่ายทั้งสองแบบจะเท่ากัน"),
                            distractors=_story.keep((b - a) // r2, (a + b) // (r1 + r2), n + 10, answer=n, lo=1))
        if kind == 1:
            start, per = rng.choice((35, 40)), rng.choice((5, 6, 7, 8))
            km = rng.randint(4, 20)
            fare = start + per * (km - 1)
            return MathDraw("", str(km),
                            prompt=(f"ค่าแท็กซี่กิโลเมตรแรก {start} บาท กิโลเมตรต่อไปกิโลเมตรละ {per} บาท "
                                    f"ถ้าจ่ายค่าโดยสาร {fare} บาท เดินทางไปกี่กิโลเมตร"),
                            distractors=_story.keep(km - 1, (fare - start) // per + 2, fare // per, answer=km, lo=1))
        if kind == 2:
            h0, rate = rng.randint(20, 40), rng.choice((2, 3, 4))
            t = rng.randint(2, h0 // rate - 1)
            left = h0 - rate * t
            return MathDraw("", str(t),
                            prompt=(f"เทียนเล่มหนึ่งสูง {h0} เซนติเมตร เมื่อจุดแล้วสั้นลงชั่วโมงละ {rate} เซนติเมตร "
                                    f"ผ่านไปกี่ชั่วโมงเทียนจะเหลือสูง {left} เซนติเมตร"),
                            distractors=_story.keep(left // rate, h0 // rate, t + 1, answer=t, lo=1))
        if kind == 3:
            member, per_member, walk_in = rng.choice((300, 500, 600, 800)), rng.choice((20, 30, 40)), rng.choice((80, 100, 120))
            n = member // (walk_in - per_member) + 1
            return MathDraw("", str(n),
                            prompt=(f"ฟิตเนสมีสองแบบ แบบสมาชิกจ่ายค่าสมัคร {member} บาท แล้วจ่ายครั้งละ {per_member} บาท "
                                    f"แบบไม่เป็นสมาชิกจ่ายครั้งละ {walk_in} บาท ต้องไปอย่างน้อยกี่ครั้ง "
                                    f"แบบสมาชิกจึงจะถูกกว่า"),
                            distractors=_story.keep(n - 1, member // walk_in, member // per_member, answer=n, lo=1))
        a0, a_in, b_out = rng.randint(50, 200), rng.choice((5, 10, 15)), rng.choice((5, 10, 20))
        t = rng.randint(5, 20)
        b0 = a0 + (a_in + b_out) * t
        return MathDraw("", str(t),
                        prompt=(f"ถัง A มีน้ำ {a0} ลิตร เติมน้ำเข้านาทีละ {a_in} ลิตร ถัง B มีน้ำ {b0} ลิตร "
                                f"ปล่อยน้ำออกนาทีละ {b_out} ลิตร ผ่านไปกี่นาทีน้ำในสองถังจะเท่ากัน"),
                        distractors=_story.keep((b0 - a0) // a_in if (b0 - a0) % a_in == 0 else t + 5,
                                                (b0 - a0) // b_out if (b0 - a0) % b_out == 0 else t + 2,
                                                t - 1, answer=t, lo=1))

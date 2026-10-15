"""เรนจ์ของฟังก์ชันกำลังสอง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/2

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.quadratic_max_min_word",
               display_name={"th": "ค่าสูงสุด/ต่ำสุดของฟังก์ชันกำลังสอง"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticMaxMinWord(WordProblem):
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 8):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = rng.randint(-h_hi, h_hi)
        k = rng.randint(-15, 15)
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        word = "ต่ำสุด" if a > 0 else "สูงสุด"
        return MathDraw(
            shown, str(k),
            prompt=f"ฟังก์ชัน f(x) ต่อไปนี้มีค่า{word}เท่าใด",
            distractors=[str(h), str(c), str(-k)])


@question_type("math.quadratic_range_open_interval",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนทุกจำนวนจริง"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRangeAllReals(MathType):
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 6):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = rng.randint(-h_hi, h_hi)
        k = rng.randint(-12, 12)
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        answer = rf"[{k}, \infty)" if a > 0 else rf"(-\infty, {k}]"
        return MathDraw(
            f"f(x) = {shown}", answer,
            prompt="จงหาเรนจ์ของฟังก์ชันนี้ เมื่อโดเมนเป็นจำนวนจริงทั้งหมด",
            distractors=[rf"(-\infty, {k}]" if a > 0 else rf"[{k}, \infty)",
                         rf"[{h}, \infty)", r"(-\infty, \infty)"])


@question_type("math.quadratic_range",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนโดเมนปิด"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRange(MathType):
    def expr(self, rng: Random):
        p, q = rng.randint(-3, 3), rng.randint(-6, 4)
        d1 = p - rng.randint(0, 3)
        d2 = d1 + rng.randint(2, 5)
        f = lambda x: (x - p) ** 2 + q
        v1, v2 = f(d1), f(d2)
        lo = q if d1 <= p <= d2 else min(v1, v2)
        hi = max(v1, v2)
        tex = poly_tex((1, "x^{2}"), (-2 * p, "x"), (p * p + q, ""))
        return MathDraw(rf"y = {tex} \;\; ({d1} \leq x \leq {d2})",
                        rf"{lo} \leq y \leq {hi}",
                        hint=rf"\text{{vertex at }} x = {p}",
                        prompt="จงหาเรนจ์ของฟังก์ชัน")


def _half_line_parameters(rng: Random) -> tuple[int, int, int, int, bool]:
    lead = rng.choice((-3, -2, -1, 1, 2, 3))
    vertex = rng.randint(-6, 6)
    height = rng.randint(-15, 15)
    boundary = vertex + rng.choice((-5, -4, -3, -2, -1, 1, 2, 3, 4, 5))
    return lead, vertex, height, boundary, rng.random() < 0.5


@question_type("math.quadratic_range_half_line_m4",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนโดเมนครึ่งเส้นตรง"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRangeHalfLineM4(MathType):
    def expr(self, rng: Random):
        a, h, k, boundary, rightward = _half_line_parameters(rng)
        has_vertex = boundary <= h if rightward else boundary >= h
        edge = a * (boundary - h) ** 2 + k
        extreme = k if has_vertex else edge
        other = edge if has_vertex else k
        shown = poly_tex((a, "x^{2}"), (-2 * a * h, "x"), (a * h * h + k, ""))
        domain = rf"x \geq {boundary}" if rightward else rf"x \leq {boundary}"
        if a > 0:
            answer = rf"[{extreme}, \infty)"
            open_end = rf"({extreme}, \infty)"
            opposite = rf"(-\infty, {extreme}]"
            wrong_edge = rf"[{other}, \infty)"
        else:
            answer = rf"(-\infty, {extreme}]"
            open_end = rf"(-\infty, {extreme})"
            opposite = rf"[{extreme}, \infty)"
            wrong_edge = rf"(-\infty, {other}]"
        return MathDraw(rf"f(x) = {shown}, \quad {domain}", answer,
                        prompt="จงหาเรนจ์ของฟังก์ชันเมื่อโดเมนเป็นไปตามที่กำหนด",
                        distractors=[
                            named("domain.excluded_attained_extremum", open_end),
                            named("domain.curvature_reversed", opposite),
                            named("domain.wrong_extremum", wrong_edge),
                        ])


def _open_interval_parameters(rng: Random) -> tuple[int, int, int, int, int]:
    lead = rng.choice((-3, -2, -1, 1, 2, 3))
    vertex = rng.randint(-5, 5)
    height = rng.randint(-12, 12)
    left = vertex - rng.randint(1, 5) if rng.random() < 0.5 else vertex + rng.randint(1, 4)
    right = left + rng.randint(2, 7)
    return lead, vertex, height, left, right


def _range_interval(lo: int, hi: int, left_closed: bool, right_closed: bool) -> str:
    return f"{'[' if left_closed else '('}{lo}, {hi}{']' if right_closed else ')'}"


@question_type("math.quadratic_range_open_domain_m4",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนช่วงเปิด"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRangeOpenDomainM4(MathType):
    def expr(self, rng: Random):
        a, h, k, left, right = _open_interval_parameters(rng)
        edge_left, edge_right = (a * (x - h) ** 2 + k for x in (left, right))
        vertex_inside = left < h < right
        values = [edge_left, edge_right, *([k] if vertex_inside else [])]
        lo, hi = min(values), max(values)
        lo_closed = vertex_inside and k == lo
        hi_closed = vertex_inside and k == hi
        shown = poly_tex((a, "x^{2}"), (-2 * a * h, "x"), (a * h * h + k, ""))
        answer = _range_interval(lo, hi, lo_closed, hi_closed)
        wrongs = [
            _range_interval(lo, hi, True, True),
            _range_interval(lo, hi, False, False),
            _range_interval(lo, hi, not lo_closed, not hi_closed),
            _range_interval(lo, hi, True, False),
            _range_interval(lo, hi, False, True),
        ]
        if wrongs[0] != answer:
            named("domain.included_excluded_endpoint", wrongs[0])
        if wrongs[1] != answer:
            named("domain.excluded_attained_extremum", wrongs[1])
        return MathDraw(rf"f(x) = {shown}, \quad {left} < x < {right}", answer,
                        prompt="จงหาเรนจ์ของฟังก์ชันเมื่อโดเมนเป็นช่วงเปิดที่กำหนด",
                        distractors=list(dict.fromkeys(w for w in wrongs if w != answer)))


def _integer_optimum_parameters(rng: Random) -> tuple[int, int, int, int, int]:
    lead = rng.randint(1, 3)
    twice_vertex = 2 * rng.randint(2, 9) + 1
    left = twice_vertex // 2 - rng.randint(0, 3)
    right = twice_vertex // 2 + 1 + rng.randint(0, 3)
    farthest = max(abs(2 * left - twice_vertex), abs(2 * right - twice_vertex))
    height = rng.randint(30, 100) + lead * farthest * farthest
    return lead, twice_vertex, left, right, height


@question_type("math.quadratic_integer_optimum_m4",
               display_name={"th": "ค่าสูงสุดของฟังก์ชันกำลังสองเมื่อ x เป็นจำนวนเต็ม"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticIntegerOptimumM4(WordProblem):
    def expr(self, rng: Random):
        a, twice_vertex, left, right, height = _integer_optimum_parameters(rng)
        answer = height - a
        item = rng.choice(("สมุด", "เสื้อ", "กระเป๋า"))
        return MathDraw(rf"P(x) = -{a}(2x - {twice_vertex})^{{2}} + {height}", str(answer),
                        prompt=(f"ร้านค้าขาย{item}ได้ x ชิ้น โดย {left} ≤ x ≤ {right} และ x เป็นจำนวนเต็ม "
                                "กำไร P(x) บาทเป็นไปตามฟังก์ชันต่อไปนี้ กำไรสูงสุดกี่บาท"),
                        distractors=[
                            named("domain.noninteger_vertex", str(height)),
                            str(height - 9 * a),
                            str(height - 4 * a),
                            str(height + a),
                        ])

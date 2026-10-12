"""การแจกแจงความน่าจะเป็น

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.6/1

Sets moved here from: math_bank_random, math_diagrams_hi, math_gaps_secondary, math_m6.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sets._support.math_diagrams import _img
from otk.sets._support.math_diagrams_hi import NORMAL_AREAS, NORMALS
from otk.sets._support.math_m4 import maths as _math_q
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m6 import _dec
from otk.sets._support.math_p4 import as_mixed

M6 = {"th": "ม.6"}


TOPIC = "การแจกแจงความน่าจะเป็น"


def phi(z: Decimal) -> Decimal:
    """P(Z ≤ z) rounded to four places, as a standard table prints it."""
    v = 0.5 * (1 + math.erf(float(z) / math.sqrt(2)))
    return Decimal(repr(v)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def dstr(v: Decimal) -> str:
    return format(Decimal(v).normalize(), "f")


def table_tex(zs) -> str:
    zs = sorted(set(zs))
    head = " & ".join(dstr(z) for z in zs)
    vals = " & ".join(dstr(phi(z)) for z in zs)
    return rf"\begin{{array}}{{c|{'c' * len(zs)}}} z & {head} \\ \hline P(Z \le z) & {vals} \end{{array}}"


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def between(z1: Decimal, z2: Decimal) -> Decimal:
    """P(z1 < Z < z2) from the table, using Φ(−z) = 1 − Φ(z) for negative z."""
    f = lambda z: phi(z) if z >= 0 else 1 - phi(-z)
    return f(z2) - f(z1)


def equal_z_score(m1: int, s1: int, m2: int, s2: int, d: int) -> Fraction:
    """Score x₁ in subject 1 when z is equal in both and x₂ − x₁ = d: (m₂ − m₁) + z(s₂ − s₁) = d."""
    z = Fraction(d - (m2 - m1), s2 - s1)
    return m1 + z * s1


def mean_sd_from_tails(a: Decimal, b: Decimal, z: Decimal) -> tuple[Decimal, Decimal]:
    """μ, σ when P(X < a) = P(X > b) = p and Φ(z) = 1 − p: symmetric, so μ = (a + b)/2 and σ = (b − μ)/z."""
    mu = (a + b) / 2
    return mu, (b - mu) / z


Z_STEPS = [Decimal(k) / 100 for k in range(10, 205, 5)]


def even_product_probability(n: int) -> Fraction:
    """Two tickets drawn together from 1..n: P(product even) = 1 − C(odd, 2)/C(n, 2)."""
    odd = (n + 1) // 2
    return 1 - Fraction(math.comb(odd, 2), math.comb(n, 2))


def expected_profit(n: int, cost: int, prize: int) -> Fraction:
    return prize * even_product_probability(n) - cost


def profit_text(v: Fraction) -> str:
    if v == 0:
        return "โดยเฉลี่ยแล้ว เท่าทุน"
    word = "ได้กำไร" if v > 0 else "ขาดทุน"
    return f"โดยเฉลี่ยแล้ว {word}ครั้งละ {abs(v)} บาท"


def mean_var(dist: dict[int, Fraction]) -> tuple[Fraction, Fraction]:
    """E(X) and Var(X) = E(X²) − E(X)² of a finite distribution {x: P(X = x)}."""
    mu = sum(x * p for x, p in dist.items())
    return mu, sum(x * x * p for x, p in dist.items()) - mu * mu


def from_counts(counts: dict[int, int]) -> dict[int, Fraction]:
    n = sum(counts.values())
    return {x: Fraction(f, n) for x, f in counts.items()}


def _dist_table(head: str, xs, row_head: str, cells) -> str:
    return (rf"\begin{{array}}{{c|{'c' * len(xs)}}} {head} & {' & '.join(map(str, xs))} \\ \hline "
            rf"{row_head} & {' & '.join(cells)} \end{{array}}")


# Three-point symmetric laws μ − d, μ, μ + d with P = p, 1 − 2p, p, so Var = 2pd² is a whole square.
SQUARE_SPREADS = [(Fraction(1, 8), 2), (Fraction(1, 8), 4), (Fraction(1, 8), 6), (Fraction(2, 9), 3),
                  (Fraction(2, 9), 6), (Fraction(1, 18), 3), (Fraction(1, 18), 6), (Fraction(9, 32), 4)]


NORMAL_ALT = ("เส้นโค้งปกติมาตรฐาน แกนนอนกำกับค่ามาตรฐาน z จาก -3 ถึง 3 "
              "และมีพื้นที่ใต้เส้นโค้งส่วนหนึ่งถูกแรเงา")


def _pct(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{float(v):g}"


_DIST_TOPIC = "การแจกแจงความน่าจะเป็น"


@question_type("math.random_variable_variance_m6",
               display_name={"th": "ค่าคาดหมายและความแปรปรวนของตัวแปรสุ่มไม่ต่อเนื่อง"},
               level=M6, topic=TOPIC)
class RandomVariableVarianceM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 2:
            p, d = rng.choice(SQUARE_SPREADS)
            mu = rng.randint(d, 12)
            dist = {mu - d: p, mu: 1 - 2 * p, mu + d: p}
            _, var = mean_var(dist)
            sd = Fraction(math.isqrt(var.numerator), math.isqrt(var.denominator))
            stem = [text("ตัวแปรสุ่ม X มีการแจกแจงความน่าจะเป็นดังตาราง ส่วนเบี่ยงเบนมาตรฐานของ X เท่ากับเท่าใด"),
                    content_math(_dist_table("x", list(dist), "P(X = x)", [frac_tex(v) for v in dist.values()]))]
            # Var given as σ; the unweighted spread d; E(X²) − E(X) under the root forgotten (Var/2).
            wrongs = [frac_tex(var), str(d), frac_tex(sd * 2), frac_tex(var / 2), frac_tex(sd + 1)]
            return _tex_q(stem, frac_tex(sd), [w for w in wrongs if w != "0"], self.topic)
        while True:
            xs = sorted(rng.sample(range(0, 9), rng.choice((3, 4))))
            if kind == 0:
                den = rng.choice((5, 8, 10))
                cuts = sorted(rng.sample(range(1, den), len(xs) - 1))
                ws = [b - a for a, b in zip([0] + cuts, cuts + [den])]
                dist = {x: Fraction(w, den) for x, w in zip(xs, ws)}
                n = den
            else:
                counts = {x: rng.randint(1, 12) for x in xs}
                n = sum(counts.values())
                dist = from_counts(counts)
            mu, var = mean_var(dist)
            ex2 = var + mu * mu
            if var.denominator <= 100 and var != 0 and n > 1:
                break
        if kind == 0:
            stem = [text("ตัวแปรสุ่ม X มีการแจกแจงความน่าจะเป็นดังตาราง ความแปรปรวนของ X เท่ากับเท่าใด"),
                    content_math(_dist_table("x", xs, "P(X = x)", [frac_tex(dist[x]) for x in xs]))]
            # E(X²) with μ² forgotten; E(X²) − μ; the plain variance of the listed values.
            plain = Fraction(sum(x * x for x in xs), len(xs)) - Fraction(sum(xs), len(xs)) ** 2
            wrongs = [ex2, ex2 - mu, plain, var + 1]
        else:
            stem = [text(f"สุ่มนักเรียน 1 คน จาก {n} คน ให้ X เป็นจำนวนข้อที่นักเรียนคนนั้นตอบถูก "
                         "ตารางแสดงจำนวนข้อที่ตอบถูก x และจำนวนนักเรียน f ความแปรปรวนของ X เท่ากับเท่าใด"),
                    content_math(_dist_table("x", xs, "f", [str(counts[x]) for x in xs]))]
            # E(X²) with μ² forgotten; the sample variance (divide by n − 1); E(X²) − μ.
            wrongs = [ex2, var * n / (n - 1), ex2 - mu, var + 1]
        return _tex_q(stem, frac_tex(var), [frac_tex(w) for w in wrongs if w > 0], self.topic)
RandomVariableVarianceM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/17 ตัวแปรสุ่ม',))


@question_type("math.uniform_distribution_m6", display_name={"th": "การแจกแจงเอกรูป"},
               level={"th": "ม.6"}, topic="การแจกแจงความน่าจะเป็น")
class UniformDistributionM6(WordProblem):
    """X uniform on 1..n: P(X = k) = 1/n, P(a ≤ X ≤ b) = (b − a + 1)/n and
    E(X) = (n + 1)/2."""

    def expr(self, rng: Random):
        n = rng.choice((4, 5, 6, 8, 10, 12, 20))
        what = {6: "ทอดลูกเต๋าที่เที่ยงตรง", 4: "หมุนวงล้อที่แบ่งเป็น 4 ช่องเท่ากัน หมายเลข 1 ถึง 4"}.get(
            n, f"สุ่มบัตร 1 ใบจากบัตรหมายเลข 1 ถึง {n}")
        kind = rng.randrange(3)
        if kind == 0:
            a = rng.randint(1, n - 2)
            b = rng.randint(a + 1, n)
            value = Fraction(b - a + 1, n)
            prompt = f"{what} ให้ X เป็นผลที่ได้ ซึ่งมีการแจกแจงเอกรูป จงหา P({a} ≤ X ≤ {b})"
            wrongs = [Fraction(b - a, n), Fraction(1, n), Fraction(b, n)]
        elif kind == 1:
            k = rng.randint(1, n)
            value = Fraction(1, n)
            prompt = f"{what} ให้ X เป็นผลที่ได้ ซึ่งมีการแจกแจงเอกรูป จงหา P(X = {k})"
            wrongs = [Fraction(k, n), Fraction(1, n + 1), Fraction(1, 2)]
        else:
            value = Fraction(n + 1, 2)
            prompt = f"{what} ให้ X เป็นผลที่ได้ ซึ่งมีการแจกแจงเอกรูป จงหาค่าคาดหมาย E(X)"
            wrongs = [Fraction(n, 2), Fraction(n), Fraction(n + 1)]
        return MathDraw("", as_mixed(value), prompt=prompt,
                        distractors=[as_mixed(w) for w in dict.fromkeys(wrongs) if w != value and w > 0])
UniformDistributionM6.PROVENANCE = Provenance("original")


@question_type("math.binomial_mean_variance_m6",
               display_name={"th": "การแจกแจงทวินาม: ค่าคาดหมายและความแปรปรวน"},
               level=M6, topic=_DIST_TOPIC)
class BinomialMeanVarianceM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice((10, 20, 30, 40, 50, 60, 100))
        p = rng.choice((Fraction(1, 2), Fraction(1, 5), Fraction(1, 4), Fraction(2, 5), Fraction(3, 10)))
        mean, var = n * p, n * p * (1 - p)
        head = [text("ให้ X มีการแจกแจงทวินาม"), content_math(rf"X \sim B({n},\ {frac_tex(p)})")]
        if rng.random() < 0.5:
            return _maths(head + [text("ค่าคาดหมาย E(X) เท่ากับเท่าใด")], frac_tex(mean),
                          [frac_tex(var), frac_tex(n * (1 - p)), frac_tex(p), frac_tex(mean + 1)], self.topic)
        return _maths(head + [text("ความแปรปรวน Var(X) เท่ากับเท่าใด")], frac_tex(var),
                      [frac_tex(mean), frac_tex(n * p * p), frac_tex(var + 1), frac_tex(mean * (1 + p))],
                      self.topic)
BinomialMeanVarianceM6.PROVENANCE = Provenance("original")


@question_type("math.expected_game_value_m6",
               display_name={"th": "ค่าคาดหมายของกำไรจากเกม"},
               level=M6, topic=TOPIC)
class ExpectedGameValueM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            n = rng.randint(5, 10)
            p = even_product_probability(n)
            prize = p.denominator * rng.randint(1, 20)
            cost = rng.randint(1, prize // 10 + 5) * 10
            e = expected_profit(n, cost, prize)
            if e.denominator == 1 and e != 0 and abs(e) < prize:
                break
        stem = [text(f"กล่องใบหนึ่งมีสลาก {n} ใบ หมายเลข 1 ถึง {n} ผู้เล่นจ่ายเงิน {cost} บาท แล้วจับสลากพร้อมกันสองใบ "
                     f"ถ้าผลคูณของหมายเลขเป็นจำนวนคู่จะได้เงินรางวัล {prize} บาท ถ้าเป็นจำนวนคี่ไม่ได้รางวัล ข้อสรุปใดถูกต้อง")]
        # The cost forgotten; the odd-product probability used; the prize not netted against the cost on a loss.
        wrongs = [profit_text(prize * p), profit_text(prize * (1 - p) - cost), profit_text(-e),
                  profit_text(prize * p - cost * p)]
        right = profit_text(e)
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
        return GeneratedQuestion(stem=stem, correct=[text(right)], distractors=fixed(*[[text(w)] for w in wrongs]),
                                 topic=self.topic)
ExpectedGameValueM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/17 ตัวแปรสุ่ม',))


@question_type("math.normal_curve_picture_m6",
               display_name={"th": "หาพื้นที่ใต้เส้นโค้งปกติจากรูป (กฎ 68–95–99.7)"},
               level={"th": "ม.6"}, topic="การแจกแจงความน่าจะเป็น")
class NormalCurvePictureM6(QuestionType):
    _POOL = (Fraction(68), Fraction(95), Fraction(997, 10), Fraction(34), Fraction(95, 2),
             Fraction(27, 2), Fraction(50), Fraction(16), Fraction(5, 2), Fraction(163, 2))

    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice(NORMALS)
        area = NORMAL_AREAS[(n.lo, n.hi)]
        wrongs = [_pct(v) for v in self._POOL if v != area]
        rng.shuffle(wrongs)
        return _math_q([text("พื้นที่ส่วนที่แรเงาใต้เส้นโค้งปกติมาตรฐานคิดเป็นประมาณร้อยละเท่าใด "
                             "(ใช้กฎ 68–95–99.7)"), _img(n.asset_id, NORMAL_ALT)],
                       _pct(area), wrongs[:3], self.topic)
NormalCurvePictureM6.PROVENANCE = Provenance("original")


@question_type("math.binomial_probability_m6", display_name={"th": "การแจกแจงทวินาม: ความน่าจะเป็น"},
               level=M6, topic=_DIST_TOPIC)
class BinomialProbabilityM6(QuestionType):
    _STORIES = (("โยนเหรียญที่เที่ยงตรง", "ออกหัว", Fraction(1, 2)),
                ("ทอดลูกเต๋าที่เที่ยงตรง", "ขึ้นแต้ม 6", Fraction(1, 6)),
                ("นักบาสเกตบอลยิงลูกโทษ (ยิงลงห่วงครั้งละความน่าจะเป็น 3/4)", "ยิงลง", Fraction(3, 4)),
                ("ตอบข้อสอบปรนัย 4 ตัวเลือกแบบเดาทุกข้อ", "ตอบถูก", Fraction(1, 4)))

    def build(self, rng: Random) -> GeneratedQuestion:
        what, success, p = rng.choice(self._STORIES)
        n = rng.randint(3, 5)
        k = rng.randint(1, n - 1)
        prob = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        # Forgetting C(n,k), forgetting the failures, and C(n,k)·p^k alone.
        wrongs = [p ** k * (1 - p) ** (n - k), math.comb(n, k) * p ** k, p ** k, Fraction(k, n),
                  1 - prob, prob / 2]
        return _maths([text(f"{what} {n} ครั้ง ความน่าจะเป็นที่จะ{success} พอดี {k} ครั้ง เท่ากับเท่าใด")],
                      frac_tex(prob), [frac_tex(w) for w in wrongs if w != prob and w <= 1], self.topic)
BinomialProbabilityM6.PROVENANCE = Provenance("original")


@question_type("math.normal_z_table_m6",
               display_name={"th": "การแจกแจงปกติโดยใช้ตารางค่ามาตรฐาน"},
               level=M6, topic=TOPIC)
class NormalZTableM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            mu, sd = rng.randint(40, 80), rng.choice((2, 4, 5, 8, 10))
            z1, z2 = sorted(rng.sample(Z_STEPS[:25], 2))
            if rng.random() < 0.5:
                z1 = -z1
            a, b = mu + z1 * sd, mu + z2 * sd
            right = between(z1, z2)
            stem = [text(f"คะแนนสอบมีการแจกแจงปกติ ค่าเฉลี่ยเลขคณิต {mu} คะแนน ส่วนเบี่ยงเบนมาตรฐาน {sd} คะแนน "
                         "สัดส่วนของผู้ที่ได้คะแนนระหว่าง"), content_math(dstr(a)), text("ถึง"), content_math(dstr(b)),
                    text("เท่ากับเท่าใด กำหนดตาราง"), content_math(table_tex([abs(z1), z2]))]
            # Φ(z₂) alone; the sign of z₁ ignored; Φ(z₂) + Φ(|z₁|) − 1; the complement.
            cands = [phi(z2), phi(z2) - phi(abs(z1)), phi(z2) + phi(abs(z1)) - 1, 1 - right]
            wrongs = [dstr(w) for w in cands if w > 0]
            return _tex_q(stem, dstr(right), wrongs, self.topic)
        if kind == 1:
            mu, var = rng.randint(50, 90), rng.choice((4, 9, 16, 25, 36))
            sd = int(math.isqrt(var))
            z = rng.choice(Z_STEPS[:30])
            q = phi(z)
            decoy = rng.choice([s for s in Z_STEPS[:30] if s != z])
            cut = mu + z * sd
            stem = [text(f"คะแนนสอบมีการแจกแจงปกติ ค่าเฉลี่ยเลขคณิต {mu} คะแนน ความแปรปรวน {var} คะแนนยกกำลังสอง "
                         f"ผู้สอบผ่านต้องมีคะแนนตั้งแต่เปอร์เซ็นไทล์ที่ {dstr(q * 100)} ขึ้นไป "
                         "ผู้สอบผ่านต้องได้คะแนนอย่างน้อยเท่าใด กำหนดตาราง"), content_math(table_tex([z, decoy]))]
            # Variance used as σ; the decoy row; subtracting.
            wrongs = [dstr(mu + z * var), dstr(mu + decoy * sd), dstr(mu - z * sd), dstr(mu + z)]
            return _tex_q(stem, dstr(cut), wrongs, self.topic)
        if kind == 2:
            while True:                 # even s₁, s₂ always give whole scores
                m1, s1 = rng.randint(50, 70), rng.randint(4, 10)
                m2, s2 = rng.randint(50, 75), rng.randint(4, 10)
                zz = Fraction(rng.choice((-2, -1, 1, 2, 3)), 2)
                x1, x2 = m1 + zz * s1, m2 + zz * s2
                if s1 != s2 and x1.denominator == 1 and x2.denominator == 1:
                    d = int(x2 - x1)
                    break
            right = equal_z_score(m1, s1, m2, s2, d)
            stem = [text(f"คะแนนสอบวิชาคณิตศาสตร์มีค่าเฉลี่ย {m1} และส่วนเบี่ยงเบนมาตรฐาน {s1} คะแนน วิชาวิทยาศาสตร์มีค่าเฉลี่ย "
                         f"{m2} และส่วนเบี่ยงเบนมาตรฐาน {s2} คะแนน ถ้านักเรียนคนหนึ่งมีคะแนนมาตรฐานของทั้งสองวิชาเท่ากัน "
                         f"และคะแนนวิทยาศาสตร์{'มากกว่า' if d >= 0 else 'น้อยกว่า'}คะแนนคณิตศาสตร์อยู่ {abs(d)} คะแนน "
                         "แล้วนักเรียนคนนี้ได้คะแนนคณิตศาสตร์เท่าใด")]
            # The science score; z itself; the difference of means ignored.
            wrongs = [str(right + d), str(m1 + zz), str(m1 + Fraction(d, s2 - s1) * s1), str(right + 2), str(right - 2)]
            fmt = lambda v: str(Fraction(v)) if Fraction(v).denominator == 1 else f"{float(Fraction(v)):.2f}"
            return _tex_q(stem, fmt(right), [fmt(Fraction(w)) for w in wrongs], self.topic)
        z = rng.choice(Z_STEPS[:20])
        p = 1 - phi(z)
        mu = Decimal(rng.randint(500, 1500)) / 100
        sd = Decimal(rng.choice((1, 2, 4, 5))) / 100 * rng.choice((1, 10))
        a, b = mu - z * sd, mu + z * sd
        k = rng.choice((1, 2, 3))
        stem = [text("น้ำหนักของสินค้ามีการแจกแจงปกติ ค่าเฉลี่ย μ และส่วนเบี่ยงเบนมาตรฐาน σ ถ้า"),
                content_math(rf"P(X < {dstr(a)}) = P(X > {dstr(b)}) = {dstr(p)}"), text("แล้ว"),
                content_math(rf"\mu + {k}\sigma"), text("เท่ากับเท่าใด กำหนดตาราง"), content_math(table_tex([z]))]
        m, s = mean_sd_from_tails(a, b, z)
        right = m + k * s
        # σ read as the half-gap (z forgotten); μ alone; the gap as σ.
        wrongs = [dstr(m + k * (b - m)), dstr(m), dstr(m + k * (b - a)), dstr(m - k * s)]
        return _tex_q(stem, dstr(right), wrongs, self.topic)
NormalZTableM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/17 ตัวแปรสุ่ม',))


@question_type("math.normal_distribution_m6",
               display_name={"th": "การแจกแจงปกติ: สัดส่วนจากกฎ 68–95–99.7"},
               level=M6, topic=_DIST_TOPIC)
class NormalDistributionM6(QuestionType):
    # Proportion (%) of a normal distribution between two whole z-scores.
    _AREA = {(-1, 1): Fraction(68), (-2, 2): Fraction(95), (-3, 3): Fraction(997, 10),
             (0, 1): Fraction(34), (0, 2): Fraction(95, 2), (-1, 0): Fraction(34), (-2, 0): Fraction(95, 2),
             (1, 2): Fraction(27, 2), (-2, -1): Fraction(27, 2), (0, 3): Fraction(997, 20)}

    # (measure, who, counter, verb, unit, means, standard deviations)
    _CONTEXTS = (
        ("คะแนนสอบ", "ผู้สอบ", "คน", "ได้คะแนน", "คะแนน", range(40, 85, 5), (5, 8, 10, 12)),
        ("น้ำหนัก", "นักเรียน", "คน", "หนัก", "กิโลกรัม", range(40, 80, 5), (5, 8, 10, 12)),
        ("ส่วนสูง", "นักเรียน", "คน", "สูง", "เซนติเมตร", range(150, 175, 5), (4, 5, 6, 8)),
        ("อายุการใช้งาน", "หลอดไฟ", "หลอด", "ใช้งานได้", "ชั่วโมง", range(800, 1250, 50), (50, 100)),
        ("เวลาที่ใช้เดินทางมาโรงเรียน", "นักเรียน", "คน", "ใช้เวลา", "นาที", range(25, 50, 5), (3, 4, 5)),
    )

    def build(self, rng: Random) -> GeneratedQuestion:
        (lo, hi), pct = rng.choice(list(self._AREA.items()))
        what, who, counter, verb, unit, means, sds = rng.choice(self._CONTEXTS)
        mean, sd = rng.choice(list(means)), rng.choice(sds)
        n = rng.choice((200, 400, 500, 1000, 2000))
        a, b = mean + lo * sd, mean + hi * sd
        if rng.random() < 0.5:
            return _maths([text(f"{what}ของ{who}กลุ่มหนึ่งมีการแจกแจงปกติ ค่าเฉลี่ย {mean} {unit} "
                                f"ส่วนเบี่ยงเบนมาตรฐาน {sd} {unit} มี{who}ที่{verb}ระหว่าง {a} ถึง {b} {unit} "
                                f"ประมาณร้อยละเท่าใด (ใช้กฎ 68–95–99.7)")], _dec(pct),
                          [_dec(v) for v in {Fraction(68), Fraction(95), Fraction(34), Fraction(47, 1),
                                             Fraction(27, 2), Fraction(16), Fraction(50)} if v != pct][:4],
                          self.topic)
        count = pct * n / 100
        if count.denominator != 1:
            return self.build(rng)
        return _maths([text(f"{what}ของ{who} {n} {counter}มีการแจกแจงปกติ ค่าเฉลี่ย {mean} {unit} "
                            f"ส่วนเบี่ยงเบนมาตรฐาน {sd} {unit} มี{who}ที่{verb}ระหว่าง {a} ถึง {b} {unit} "
                            f"ประมาณกี่{counter} (ใช้กฎ 68–95–99.7)")], str(int(count)),
                      [str(int(pct)), str(n - int(count)), str(int(count) // 2), str(int(count) * 2)
                       if int(count) * 2 <= n else str(int(count) + 10)], self.topic)
NormalDistributionM6.PROVENANCE = Provenance("original")

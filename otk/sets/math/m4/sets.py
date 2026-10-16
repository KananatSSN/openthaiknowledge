"""เซต

คณิตศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.4/1, ค เพิ่มเติม จำนวนและพีชคณิต 1 ม.4/1

Sets moved here from: math, math_bank_sets, math_data, math_diagrams_hi, math_m4.
"""

from __future__ import annotations

import math
from itertools import combinations
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img
from otk.sets._support.math_diagrams_hi import VENNS
from otk.sets._support.math_m4 import maths as _math_q
from otk.sets._support.math_m4 import maths as _num_maths

M4 = {"th": "ม.4"}


TOPIC = "เซต"


def set_tex(s) -> str:
    return r"\{" + ", ".join(map(str, sorted(s))) + r"\}" if s else r"\varnothing"


def set_plain(s) -> str:
    return "{" + ", ".join(map(str, sorted(s))) + "}" if s else "∅"


def _choice_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]),
                             topic=topic)


#: (TeX, evaluator over sets A, B, C, universe U). The pool that both the
#: evaluating and the matching sets draw from.
EXPRESSIONS: tuple[tuple[str, object], ...] = (
    (r"A \cup B", lambda A, B, C, U: A | B),
    (r"A \cap B", lambda A, B, C, U: A & B),
    (r"A - B", lambda A, B, C, U: A - B),
    (r"B - A", lambda A, B, C, U: B - A),
    (r"B \cap (A \cup C)", lambda A, B, C, U: B & (A | C)),
    (r"(B \cap A) \cup C", lambda A, B, C, U: (B & A) | C),
    (r"(A \cup B) - C", lambda A, B, C, U: (A | B) - C),
    (r"A \cup (B - C)", lambda A, B, C, U: A | (B - C)),
    (r"(A \cup B) - (A \cap B)", lambda A, B, C, U: (A | B) - (A & B)),
    (r"A - (B \cap C)", lambda A, B, C, U: A - (B & C)),
    (r"(A - B) \cup (A - C)", lambda A, B, C, U: (A - B) | (A - C)),
    (r"B - (A - C)", lambda A, B, C, U: B - (A - C)),
    (r"B - (C - A)", lambda A, B, C, U: B - (C - A)),
    (r"B \cap (A - C)", lambda A, B, C, U: B & (A - C)),
    (r"B \cap (C - A)", lambda A, B, C, U: B & (C - A)),
    (r"(A \cup B \cup C)'", lambda A, B, C, U: U - (A | B | C)),
    (r"A' \cap B", lambda A, B, C, U: (U - A) & B),
    (r"(A \cap C)'", lambda A, B, C, U: U - (A & C)),
)


# Set-builder definitions over an integer universe: (Thai condition, predicate).
_CONDITIONS = (
    ("x เป็นจำนวนคี่", lambda x: x % 2 != 0),
    ("x เป็นจำนวนคู่", lambda x: x % 2 == 0),
    ("x² < 9", lambda x: x * x < 9),
    ("x² ≤ 16", lambda x: x * x <= 16),
    ("x หารด้วย 3 ลงตัว", lambda x: x % 3 == 0),
    ("x เป็นจำนวนเฉพาะ", lambda x: x > 1 and all(x % d for d in range(2, x))),
    ("x > 4", lambda x: x > 4),
    ("|x| ≤ 2", lambda x: abs(x) <= 2),
    ("(x + 1)(x − 4) = 0", lambda x: (x + 1) * (x - 4) == 0),
)


def evaluate(tex: str, A: set, B: set, C: set, U: set) -> frozenset:
    for t, f in EXPRESSIONS:
        if t == tex:
            return frozenset(f(A, B, C, U))
    raise KeyError(tex)


#: Premises over (A, B) or (A, B, C): (TeX parts joined by "และ", predicate).
#: Thai never goes inside TeX, so a two-part premise is two math blocks.
_PREMISES = (
    ((r"A - B = \varnothing",), lambda A, B, C: not (A - B)),
    ((r"A \cap B = \varnothing",), lambda A, B, C: not (A & B)),
    ((r"A \cup B = B",), lambda A, B, C: A | B == B),
    ((r"B \subset C", r"A \cap C = \varnothing"), lambda A, B, C: B <= C and not (A & C)),
    ((r"A \cap B = A",), lambda A, B, C: A & B == A),
)


_CONCLUSIONS = (
    (r"B = A \cup B", lambda A, B, C: B == A | B),
    (r"B = A \cap B", lambda A, B, C: B == A & B),
    (r"A = A \cap B", lambda A, B, C: A == A & B),
    (r"A \subset B", lambda A, B, C: A <= B),
    (r"B \subset A", lambda A, B, C: B <= A),
    (r"A - B = A", lambda A, B, C: A - B == A),
    (r"B - A = \varnothing", lambda A, B, C: not (B - A)),
    (r"(A \cup B) \cap C = B", lambda A, B, C: (A | B) & C == B),
    (r"A \cap B = B \cap C", lambda A, B, C: A & B == B & C),
    (r"A - B = C - B", lambda A, B, C: A - B == C - B),
    (r"A \cup B = A", lambda A, B, C: A | B == A),
)


_WORLD = [frozenset(s) for r in range(4) for s in combinations(range(3), r)]


def always(premise, conclusion) -> bool:
    """Does the conclusion hold for every A, B, C ⊆ {0, 1, 2} meeting the premise?

    Nonempty sets only, as the exam's "เป็นเซตที่ไม่ว่าง" states. A small
    universe is enough: every Venn region of three sets fits in three elements
    plus its absence.
    """
    worlds = [(A, B, C) for A in _WORLD for B in _WORLD for C in _WORLD
              if A and B and C and premise(A, B, C)]
    return bool(worlds) and all(conclusion(*w) for w in worlds)


def _agree(solved: int, truth: int) -> int:
    if solved != truth:                                    # pragma: no cover
        raise AssertionError(f"solver gave {solved}, the regions say {truth}")
    return solved


def solve_b_from_only_a(total: int, a_only: int, neither: int) -> int:
    """n(B) given the total, n(A − B) and n(A′ ∩ B′)."""
    return total - neither - a_only


def solve_b_from_difference(union: int, both: int, a_minus_b: int) -> int:
    """n(B) given n(A ∪ B), n(A ∩ B) and n(A) − n(B) (which may be negative)."""
    return (union + both - a_minus_b) // 2


def solve_only_when_equal(union: int, both: int) -> int:
    """n(A − B) when n(A) = n(B), given n(A ∪ B) and n(A ∩ B)."""
    return (union - both) // 2


def solve_both(total: int, n_a: int, n_b: int, neither: int) -> int:
    """n(A ∩ B) given the total, n(A), n(B) and n(A′ ∩ B′)."""
    return n_a + n_b - (total - neither)


def _join(x: str, word: str, y: str) -> str:
    """``x`` + ``word`` + ``y`` the Thai way (no spaces), except after a Latin
    letter: "โรงพยาบาล A และ…", not "โรงพยาบาล Aและ…"."""
    gap = " " if x[-1].isascii() and not word.startswith(" ") else ""
    return f"{x}{gap}{word}{y}"


_TWO_SET_THEMES = (
    ("นักเรียน", "คน", "เลือกคณะรัฐศาสตร์", "เลือกคณะนิเทศศาสตร์"),
    ("ผู้ป่วย", "คน", "ใช้บริการโรงพยาบาล A", "ใช้บริการโรงพยาบาล B"),
    ("เด็ก", "คน", "ชอบรสวนิลา", "ชอบรสส้ม"),
    ("นักเรียน", "คน", "เรียนพิเศษคณิตศาสตร์", "เรียนพิเศษภาษาอังกฤษ"),
)


def solve_exactly_two(total: int, neither: int, singles: list[int], e3: int) -> int:
    """E₂ from Σ n(single sets) = E₁ + 2E₂ + 3E₃ and n(∪) = E₁ + E₂ + E₃."""
    return sum(singles) - (total - neither) - 2 * e3


def solve_exactly_one(total: int, neither: int, singles: list[int], e3: int) -> int:
    return (total - neither) - solve_exactly_two(total, neither, singles, e3) - e3


def solve_third_set(total: int, neither: int, e2: int, e3: int, n1: int, n2: int) -> int:
    """n(C) given the total, the exactly-2 and exactly-3 counts, n(A) and n(B)."""
    e1 = total - neither - e2 - e3
    return e1 + 2 * e2 + 3 * e3 - n1 - n2


def solve_all_three(total: int, neither: int, a_not_b: int, b_not_c: int, c_not_a: int) -> int:
    """n(A ∩ B ∩ C): A − B, B − C and C − A cover every region of the union
    except A ∩ B ∩ C, each exactly once."""
    return total - neither - a_not_b - b_not_c - c_not_a


def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


def count_either(n: int, a: int, b: int) -> int:
    return n // a + n // b - n // lcm(a, b)


def count_only_first(n: int, a: int, b: int) -> int:
    return n // a - n // lcm(a, b)


def count_either_not_both(n: int, a: int, b: int) -> int:
    return n // a + n // b - 2 * (n // lcm(a, b))


def max_b(n_u: int, both: int, neither: int, a_min: int) -> int:
    """Largest n(B) when n(A) ≥ a_min: n(B) = n(U) − neither − (n(A) − both)."""
    return n_u - neither - (a_min - both)


def min_x(total: int, only_z: int, both_xy: int, y_max: int) -> int:
    """Smallest n(X) when everyone outside "Z only" is in X or Y and n(Y) ≤ y_max:
    n(X ∪ Y) = total − only_z, so n(X) = n(X ∪ Y) − n(Y) + n(X ∩ Y)."""
    return total - only_z - y_max + both_xy


VENN_ALT = ("แผนภาพเวนน์ของเซต A และ B ในเอกภพสัมพัทธ์ U "
            "มีจำนวนสมาชิกเขียนไว้ในแต่ละส่วน")


@question_type("math.set_operations",
               display_name={"th": "ยูเนียน/อินเตอร์เซกชัน/ผลต่างของเซต"},
               level={"th": "ม.4"}, topic="เซต")
class SetOperations(QuestionType):
    @staticmethod
    def _tex(s) -> str:
        return r"\{" + ", ".join(map(str, sorted(s))) + r"\}" if s else r"\varnothing"

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            a = set(rng.sample(range(1, 10), rng.randint(3, 5)))
            b = set(rng.sample(range(1, 10), rng.randint(3, 5)))
            results = {"∪": a | b, "∩": a & b, "−": a - b}
            texs = {k: self._tex(v) for k, v in results.items()}
            if a & b and a - b and len(set(texs.values())) == 3:
                break
        op = rng.choice(list(results))
        wrong = [texs[k] for k in results if k != op] + [self._tex(b - a)]
        plain = lambda s: "{" + ", ".join(map(str, sorted(s))) + "}"
        return GeneratedQuestion(
            stem=[text(f"ให้ A = {plain(a)}, B = {plain(b)}  จงหา A {op} B")],
            correct=[content_math(texs[op])],
            distractors=fixed(*[[content_math(w)] for w in wrong]),
            topic=self.topic,
        )
SetOperations.PROVENANCE = Provenance("original")


@question_type("math.set_expression_eval_m4",
               display_name={"th": "เซตแบบบอกเงื่อนไขและนิพจน์ของเซตหลายขั้น"},
               level=M4, topic=TOPIC)
class SetExpressionEvalM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return self._recover(rng)
        lo, hi = rng.choice(((-3, 9), (-2, 9), (1, 12), (0, 10)))
        U = set(range(lo, hi + 1))
        while True:
            conds = rng.sample(_CONDITIONS, 3)
            A, B, C = ({x for x in U if f(x)} for _, f in conds)
            tex = rng.choice([t for t, _ in EXPRESSIONS[4:15]])
            right = evaluate(tex, A, B, C, U)
            # Named mistakes: the same sets under neighbouring expressions.
            others = {evaluate(t, A, B, C, U) for t, _ in EXPRESSIONS if t != tex}
            others.discard(right)
            if right and len(others) >= 3 and A and B and C:
                break
        wrongs = sorted(others, key=lambda s: (abs(len(s) - len(right)), sorted(s)))[:3]
        u_text = "{" + f"{lo}, {lo + 1}, {lo + 2}, …, {hi}" + "}"
        stem = [text(f"กำหนดให้ U = {u_text} และ"),
                text(" ".join(f"{n} = {{ x ∈ U | {c} }}" for n, (c, _) in zip("ABC", conds))),
                text("เซตในข้อใดเท่ากับ"), content_math(tex)]
        return _choice_q(stem, set_tex(right), [set_tex(w) for w in wrongs], self.topic)

    def _recover(self, rng: Random) -> GeneratedQuestion:
        while True:
            A = set(rng.sample(range(1, 13), rng.randint(3, 5)))
            B = set(rng.sample(range(1, 13), rng.randint(3, 5)))
            if A & B and B - A and A - B:
                break
        union, inter = A | B, A & B
        stem = [text(f"กำหนดให้ A = {set_plain(A)} ถ้า A ∪ B = {set_plain(union)} "
                     f"และ A ∩ B = {set_plain(inter)} แล้ว B คือเซตในข้อใด")]
        # Forgetting the overlap; the whole union; the symmetric difference.
        wrongs = [union - A, union, union - inter, A]
        return _choice_q(stem, set_tex(B), [set_tex(w) for w in wrongs if w != B], self.topic)
SetExpressionEvalM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.count_subsets",
               display_name={"th": "จำนวนสับเซต"}, level={"th": "ม.4"},
               topic="เซต")
class CountSubsets(WordProblem):
    _THINGS = (("ผลไม้", ("ส้ม", "มะม่วง", "กล้วย", "เงาะ", "มังคุด", "ลำไย")),
               ("สี", ("แดง", "เขียว", "น้ำเงิน", "เหลือง", "ม่วง", "ขาว")),
               ("วิชา", ("คณิตศาสตร์", "วิทยาศาสตร์", "ภาษาไทย", "ศิลปะ", "ดนตรี", "พลศึกษา")))

    def expr(self, rng: Random):
        n = rng.randint(2, 6)
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(2 ** n),
                            prompt=f"เซตที่มีสมาชิก {n} ตัว มีสับเซตทั้งหมดกี่เซต?",
                            distractors=[str(2 ** n - 1), str(n * n), str(2 * n)])
        if kind == 1:
            return MathDraw("", str(2 ** n - 1),
                            prompt=f"เซตที่มีสมาชิก {n} ตัว มีสับเซตแท้ทั้งหมดกี่เซต?",
                            # Every subset, and every subset but ∅ and the set.
                            distractors=[str(2 ** n), str(2 ** n - 2), str(n)])
        if kind == 2:
            what, pool = rng.choice(self._THINGS)
            items = rng.sample(pool, n)
            return MathDraw("", str(2 ** n),
                            prompt=(f"ร้านมี{what}ให้เลือก {n} ชนิด คือ {', '.join(items)} "
                                    f"ถ้าเลือกกี่ชนิดก็ได้ (ไม่เลือกเลยก็ได้) จะเลือกได้กี่แบบ"),
                            distractors=[str(2 ** n - 1), str(n * n), str(2 * n)])
        k = rng.randint(1, n - 1)
        return MathDraw("", str(2 ** (n - k)),
                        prompt=(f"เซต A มีสมาชิก {n} ตัว สับเซตของ A ที่มีสมาชิก {k} ตัวที่กำหนดไว้"
                                f"อยู่ด้วยทุกตัว มีทั้งหมดกี่เซต"),
                        distractors=[str(2 ** n), str(2 ** k), str(2 ** (n - k) - 1)
                                     if 2 ** (n - k) > 2 else str(n - k)])
CountSubsets.PROVENANCE = Provenance("original")


@question_type("math.set_expression_match_m4",
               display_name={"th": "นิพจน์ของเซตที่เท่ากับเซตที่กำหนด"},
               level=M4, topic=TOPIC)
class SetExpressionMatchM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        U = set(range(1, 11))
        while True:
            A, B, C = (set(rng.sample(sorted(U), rng.randint(3, 6))) for _ in range(3))
            values = {t: evaluate(t, A, B, C, U) for t, _ in EXPRESSIONS}
            tex = rng.choice(list(values))
            target = values[tex]
            wrong = [t for t, v in values.items() if v != target]
            # The four offered expressions must have four different values.
            rng.shuffle(wrong)
            picked, seen = [], {target}
            for t in wrong:
                if values[t] not in seen:
                    picked.append(t)
                    seen.add(values[t])
                if len(picked) == 3:
                    break
            if target and len(picked) == 3:
                break
        stem = [text(f"กำหนดให้ U = {set_plain(U)}, A = {set_plain(A)}, "
                     f"B = {set_plain(B)} และ C = {set_plain(C)}"),
                text(f"เซตในข้อใดเท่ากับ {set_plain(target)}")]
        return _choice_q(stem, tex, picked, self.topic)
SetExpressionMatchM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_always_true_m4",
               display_name={"th": "ข้อความเกี่ยวกับเซตที่เป็นจริงเสมอ"},
               level=M4, topic=TOPIC)
class SetAlwaysTrueM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            ptex, prem = rng.choice(_PREMISES)
            true = [t for t, c in _CONCLUSIONS if always(prem, c)]
            false = [t for t, c in _CONCLUSIONS if not always(prem, c)]
            if true and len(false) >= 3:
                break
        right = rng.choice(true)
        rng.shuffle(false)
        premise = [content_math(ptex[0])]
        for part in ptex[1:]:
            premise += [text("และ"), content_math(part)]
        stem = [text("ให้ A, B และ C เป็นเซตที่ไม่เป็นเซตว่าง ถ้า"), *premise,
                text("แล้วข้อใดต่อไปนี้เป็นจริงเสมอ")]
        return _choice_q(stem, right, false[:3], self.topic)
SetAlwaysTrueM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_multiples_count_m4",
               display_name={"th": "นับจำนวนที่หารด้วย a หรือ b ลงตัว"},
               level=M4, topic=TOPIC)
class SetMultiplesCountM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice((50, 60, 80, 100, 120, 150, 200))
        a, b = sorted(rng.sample((2, 3, 4, 5, 6, 7), 2))
        m = lcm(a, b)
        na, nb, nab = n // a, n // b, n // m
        u = f"กำหนดให้ U = {{1, 2, 3, …, {n}}}"
        kind = rng.randrange(3)
        if kind == 0:
            ask = f"จำนวนสมาชิกของ {{ x ∈ U | x หารด้วย {a} หรือ {b} ลงตัว }} เท่ากับเท่าใด"
            right = count_either(n, a, b)
            wrongs = [na + nb, na + nb - 2 * nab, nab]
        elif kind == 1:
            ask = (f"ถ้า A คือเซตของจำนวนใน U ที่หารด้วย {a} ลงตัว และ B คือเซตของจำนวนใน U "
                   f"ที่หารด้วย {b} ลงตัว แล้ว n(A − (A ∩ B)) เท่ากับเท่าใด")
            right = count_only_first(n, a, b)
            wrongs = [na - nb, na, nab]
        else:
            ask = (f"จำนวนสมาชิกของ {{ x ∈ U | x หารด้วย {a} หรือ {b} ลงตัว "
                   f"แต่หารด้วย {m} ไม่ลงตัว }} เท่ากับเท่าใด")
            right = count_either_not_both(n, a, b)
            wrongs = [na + nb - nab, na + nb - 3 * nab, na + nb]
        return _num_maths([text(f"{u} {ask}")], str(right),
                          [str(w) for w in wrongs if w > 0], self.topic)
SetMultiplesCountM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.venn_picture_m4", display_name={"th": "อ่านจำนวนสมาชิกจากแผนภาพเวนน์"},
               level={"th": "ม.4"}, topic="เซต")
class VennPictureM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        v = rng.choice(VENNS)
        A, B = v.a_only + v.both, v.b_only + v.both
        U = A + v.b_only + v.neither
        asks = ((r"n(A \cup B)", A + v.b_only, [A + B, v.both, U]),
                (r"n(A \cap B)", v.both, [A + v.b_only, A, v.neither]),
                (r"n(A - B)", v.a_only, [A, v.b_only, A - v.b_only if A > v.b_only else U - A]),
                (r"n(B')", U - B, [v.a_only, B, v.neither]),
                (r"n(A' \cap B')", v.neither, [U - v.both, v.both, U - A]),
                (r"n(A)", A, [v.a_only, A + v.b_only, v.both]))
        ask, ans, wrongs = rng.choice(asks)
        return _math_q([text("จากแผนภาพเวนน์ จงหา"), content_math(ask), _img(v.asset_id, VENN_ALT)],
                       str(ans), [str(w) for w in wrongs], self.topic)
VennPictureM4.PROVENANCE = Provenance("original")


@question_type("math.set_two_set_word_m4",
               display_name={"th": "โจทย์ปัญหาสองเซตแบบย้อนหาค่าที่ไม่รู้"},
               level=M4, topic=TOPIC)
class SetTwoSetWordM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        who, unit, x, y = rng.choice(_TWO_SET_THEMES)
        kind = rng.randrange(4)
        a_only, both, b_only = rng.randint(5, 40), rng.randint(3, 30), rng.randint(5, 40)
        neither = rng.randint(1, 20)
        if kind == 2:
            b_only, neither = a_only, 0
        n_a, n_b = a_only + both, b_only + both
        union = a_only + both + b_only
        total = union + neither
        survey = f"จากการสำรวจ{who} {total} {unit} พบว่า"
        if kind == 0:
            stem = (f"{survey} {both} {unit}{_join(x, 'และ', y)} {a_only} {unit}{_join(x, ' แต่', 'ไม่' + y)} "
                    f"และ {neither} {unit}{_join('ไม่' + x, 'และ', 'ไม่' + y)} มี{who}ที่{y}ทั้งหมดกี่{unit}")
            right = _agree(solve_b_from_only_a(total, a_only, neither), n_b)
            # Only the B-only part; forgetting the "neither" group; the whole minus A only.
            wrongs = [b_only, n_b + neither, total - a_only]
        elif kind == 1:
            diff = n_a - n_b
            if diff == 0:
                said = f"จำนวน{who}ที่{x}เท่ากับจำนวนที่{y}"
            elif diff > 0:
                said = f"จำนวน{who}ที่{x}มากกว่าจำนวนที่{y}อยู่ {diff} {unit}"
            else:
                said = f"จำนวน{who}ที่{y}มากกว่าจำนวนที่{x}อยู่ {-diff} {unit}"
            stem = (f"กำหนดให้ A คือเซตของ{who}ที่{x} และ B คือเซตของ{who}ที่{y} "
                    f"ถ้า n(A ∪ B) = {union}, n(A ∩ B) = {both} และ{said} "
                    f"แล้ว n(B) เท่ากับเท่าใด")
            right = _agree(solve_b_from_difference(union, both, diff), n_b)
            # n(A) instead; halving without the overlap; B only.
            wrongs = [n_a, (union - diff) // 2, b_only]
        elif kind == 2:
            stem = (f"{who}ทุก{unit}{_join(x, 'หรือ', y)}อย่างน้อยหนึ่งอย่าง มี {both} {unit}{_join(x, 'และ', y)} "
                    f"จำนวนที่{x}เท่ากับจำนวนที่{y} และมี{who}ทั้งหมด {union} {unit} "
                    f"มี{who}ที่{x}อย่างเดียวกี่{unit}")
            right = _agree(solve_only_when_equal(union, both), a_only)
            wrongs = [n_a, union // 2, both]
        else:
            stem = (f"{survey} {n_a} {unit}{x} {n_b} {unit}{y} และ {neither} {unit}{_join('ไม่' + x, 'และ', 'ไม่' + y)} "
                    f"มีกี่{unit}ที่{_join(x, 'และ', y)}")
            right = _agree(solve_both(total, n_a, n_b, neither), both)
            # Forgetting the "neither" group; counting it twice; the group itself.
            wrongs = [n_a + n_b - total, n_a + n_b - total + 2 * neither, neither]
        return _num_maths([text(stem)], str(right), [str(w) for w in wrongs if w > 0], self.topic)
SetTwoSetWordM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_exactly_k_m4",
               display_name={"th": "จำนวนที่อยู่ในเซตพอดีหนึ่ง สอง หรือสามเซต"},
               level=M4, topic=TOPIC)
class SetExactlyKM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        only = [rng.randint(3, 25) for _ in range(3)]
        pairs = [rng.randint(1, 12) for _ in range(3)]          # AB, BC, AC (not the third)
        e3 = rng.choice((0, rng.randint(1, 6)))
        e1, e2 = sum(only), sum(pairs)
        n = [only[0] + pairs[0] + pairs[2] + e3, only[1] + pairs[0] + pairs[1] + e3,
             only[2] + pairs[1] + pairs[2] + e3]
        neither = rng.randint(0, 12)
        total = e1 + e2 + e3 + neither
        names = rng.choice((("วิ่ง", "ว่ายน้ำ", "ปั่นจักรยาน"), ("แก้วกาแฟ", "พวงกุญแจ", "โปสการ์ด"),
                            ("เลี้ยงสุนัข", "เลี้ยงแมว", "เลี้ยงกระต่าย")))
        each = " ".join(f"{k} คนเลือก{nm}" for nm, k in zip(names, n))
        rule = (" (แต่ละคนเลือกได้ไม่เกิน 2 อย่าง)" if e3 == 0
                else f" และ {e3} คนเลือกครบทั้งสามอย่าง")
        intro = f"จากการสำรวจคน {total} คน เกี่ยวกับ{names[0]} {names[1]} และ{names[2]} พบว่า"
        kind = rng.randrange(3)
        if kind == 0:
            stem = f"{intro} {each}{rule} และ {neither} คนไม่เลือกเลย มีกี่คนที่เลือกพอดี 2 อย่าง"
            right = _agree(solve_exactly_two(total, neither, n, e3), e2)
            # Σn − n(∪) without the E₃ correction; with it once; E₁.
            wrongs = [e2 + 2 * e3, e2 + e3, e1]
        elif kind == 1:
            stem = f"{intro} {each}{rule} และ {neither} คนไม่เลือกเลย มีกี่คนที่เลือกเพียงอย่างเดียว"
            right = _agree(solve_exactly_one(total, neither, n, e3), e1)
            wrongs = [e1 + e2, total - neither - e3, e2]
        else:
            three = f" {e3} คนเลือกครบทั้งสามอย่าง" if e3 else " ไม่มีใครเลือกครบทั้งสามอย่าง"
            stem = (f"{intro} {neither} คนไม่เลือกเลย {e2} คนเลือกพอดี 2 อย่าง{three} "
                    f"{n[0]} คนเลือก{names[0]} และ {n[1]} คนเลือก{names[1]} มีกี่คนที่เลือก{names[2]}")
            right = _agree(solve_third_set(total, neither, e2, e3, n[0], n[1]), n[2])
            # The exactly-two group counted once; the all-three counted once; the "only" part.
            wrongs = [n[2] - e2, n[2] - 2 * e3, only[2]]
        return _num_maths([text(stem)], str(right), [str(w) for w in wrongs if w > 0], self.topic)
SetExactlyKM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_region_algebra_m4",
               display_name={"th": "ตั้งตัวแปรแทนส่วนของแผนภาพเวนน์เพื่อหาค่าที่ไม่รู้"},
               level=M4, topic=TOPIC)
class SetRegionAlgebraM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        # A only, B only, C only, A∩B only, B∩C only, A∩C only, all three.
        a, b, c, ab, bc, ac = (rng.randint(5, 60) for _ in range(6))
        abc, neither = rng.randint(5, 90), rng.randint(5, 40)
        a_not_b, b_not_c, c_not_a = a + ac, b + ab, c + bc
        total = a + b + c + ab + bc + ac + abc + neither
        said = (f"{a_not_b} คนเข้าร่วม A แต่ไม่เข้าร่วม B, {b_not_c} คนเข้าร่วม B แต่ไม่เข้าร่วม C, "
                f"{c_not_a} คนเข้าร่วม C แต่ไม่เข้าร่วม A")
        intro = f"จากการสำรวจนักเรียน {total} คน เรื่องการเข้าร่วมกิจกรรม A, B และ C พบว่า {said}"
        if rng.random() < 0.5:
            stem = f"{intro} และ {neither} คนไม่เข้าร่วมกิจกรรมใดเลย มีนักเรียนที่เข้าร่วมทั้งสามกิจกรรมกี่คน"
            right = _agree(solve_all_three(total, neither, a_not_b, b_not_c, c_not_a), abc)
            # Forgetting the non-participants; subtracting them twice.
            wrongs = [abc + neither, abc - neither, total - a_not_b - b_not_c - c_not_a]
        else:
            stem = f"{intro} และ {abc} คนเข้าร่วมทั้งสามกิจกรรม มีนักเรียนที่ไม่เข้าร่วมกิจกรรมใดเลยกี่คน"
            right = _agree(solve_all_three(total, abc, a_not_b, b_not_c, c_not_a), neither)
            wrongs = [neither + abc, total - a_not_b - b_not_c - c_not_a, abs(abc - neither)]
        return _num_maths([text(stem)], str(right), [str(w) for w in wrongs if w > 0], self.topic)
SetRegionAlgebraM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_extremal_m4",
               display_name={"th": "ค่ามากที่สุดหรือน้อยที่สุดของจำนวนสมาชิกของเซต"},
               level=M4, topic=TOPIC)
class SetExtremalM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            n_u = rng.choice((60, 80, 100, 120))
            both = rng.randint(10, n_u // 3)
            neither = rng.randint(2, n_u // 8)
            a_min = rng.randint(both + 5, n_u - neither - 10)
            right = max_b(n_u, both, neither, a_min)
            stem = (f"กำหนดให้ U เป็นเอกภพสัมพัทธ์ และ A, B เป็นสับเซตของ U โดยที่ n(U) = {n_u}, "
                    f"n(A ∩ B) = {both} และ n(A′ ∩ B′) = {neither} ถ้า n(A) ≥ {a_min} "
                    f"แล้ว n(B) ที่มากที่สุดที่เป็นไปได้เท่ากับเท่าใด")
            # Forgetting the overlap; forgetting the "neither" group; the bound itself.
            wrongs = [right - both, right + neither, n_u - a_min]
        else:
            total = rng.choice((200, 300, 400, 500))
            only_z = rng.randint(total // 5, total // 2)
            both = rng.randint(10, total // 6)
            y_max = rng.randint(both + 10, (total - only_z) // 2)
            right = min_x(total, only_z, both, y_max)
            stem = (f"นักเรียน {total} คน แต่ละคนเป็นสมาชิกชมรม X ชมรม Y หรือชมรม Z อย่างน้อยหนึ่งชมรม "
                    f"มี {only_z} คนเป็นสมาชิกชมรม Z อย่างเดียว มี {both} คนเป็นสมาชิกทั้งชมรม X และชมรม Y "
                    f"และชมรม Y มีสมาชิกไม่เกิน {y_max} คน ชมรม X มีสมาชิกอย่างน้อยที่สุดกี่คน")
            wrongs = [right - both, right + both, total - only_z - both]
        return _num_maths([text(stem)], str(right), [str(w) for w in wrongs if w > 0], self.topic)
SetExtremalM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/1 เซต',))


@question_type("math.set_cardinality", display_name={"th": "จำนวนสมาชิกของยูเนียน"},
               level={"th": "ม.4"}, topic="เซต")
class SetCardinality(WordProblem):
    """|A ∪ B| = |A| + |B| − |A ∩ B| — inclusion–exclusion at its smallest,
    as bare notation or in a survey."""

    _SURVEYS = (("เล่นฟุตบอล", "เล่นบาสเกตบอล"), ("ชอบอ่านนิยาย", "ชอบอ่านการ์ตูน"),
                ("เรียนภาษาจีน", "เรียนภาษาญี่ปุ่น"), ("ดื่มชา", "ดื่มกาแฟ"))

    def expr(self, rng: Random, size_lo: int = 5, size_hi: int = 30):
        a = rng.randint(size_lo, size_hi)
        b = rng.randint(size_lo, size_hi)
        both = rng.randint(1, min(a, b))
        union = a + b - both
        wrongs = [str(a + b), str(a + b + both), str(abs(a - b))]
        if rng.random() < 0.4:
            return MathDraw(
                rf"n(A) = {a}, \quad n(B) = {b}, \quad n(A \cap B) = {both}",
                str(union), prompt="จงหา n(A ∪ B)", distractors=wrongs)
        x, y = rng.choice(self._SURVEYS)
        neither = rng.randint(0, 15)
        total = union + neither
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(union),
                            prompt=(f"สำรวจนักเรียนกลุ่มหนึ่ง มีคน{x} {a} คน {y} {b} คน และทั้งสองอย่าง "
                                    f"{both} คน มีนักเรียนที่{x}หรือ{y}อย่างน้อยหนึ่งอย่างกี่คน"),
                            distractors=wrongs)
        if kind == 1:
            return MathDraw("", str(a - both),
                            prompt=(f"สำรวจนักเรียนกลุ่มหนึ่ง มีคน{x} {a} คน {y} {b} คน และทั้งสองอย่าง "
                                    f"{both} คน มีนักเรียนที่{x}อย่างเดียวกี่คน"),
                            distractors=[str(a), str(union - b + both), str(b - both)
                                         if b - both != a - both else str(a + 1)])
        return MathDraw("", str(neither),
                        prompt=(f"นักเรียน {total} คน มีคน{x} {a} คน {y} {b} คน และทั้งสองอย่าง {both} คน "
                                f"มีนักเรียนที่ไม่{x}และไม่{y}กี่คน"),
                        distractors=[str(total - a - b) if total - a - b >= 0 else str(neither + both),
                                     str(neither + both), str(total - union + 1)])
SetCardinality.PROVENANCE = Provenance("original")


@question_type("math.three_set_counting_m4",
               display_name={"th": "โจทย์ปัญหาจำนวนสมาชิกของเซตสามเซต"},
               level=M4, topic="เซต")
class ThreeSetCountingM4(WordProblem):
    _CLUBS = (("ฟุตบอล", "ว่ายน้ำ", "บาสเกตบอล"), ("ภาษาอังกฤษ", "ภาษาจีน", "ภาษาญี่ปุ่น"),
              ("กาแฟ", "ชา", "นม"))

    def expr(self, rng: Random):
        x, y, z = rng.choice(self._CLUBS)
        # Build the eight Venn regions first; every count below is a sum of them.
        abc = rng.randint(1, 6)
        ab, bc, ac = (rng.randint(1, 8) for _ in range(3))
        oa, ob, oc = (rng.randint(3, 20) for _ in range(3))
        none = rng.randint(0, 12)
        A, B, C = oa + ab + ac + abc, ob + ab + bc + abc, oc + ac + bc + abc
        AB, BC, AC = ab + abc, bc + abc, ac + abc
        union = A + B + C - AB - BC - AC + abc
        total = union + none
        facts = (f"ชอบ{x} {A} คน ชอบ{y} {B} คน ชอบ{z} {C} คน ชอบ{x}และ{y} {AB} คน "
                 f"ชอบ{y}และ{z} {BC} คน ชอบ{x}และ{z} {AC} คน และชอบทั้งสามอย่าง {abc} คน")
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(union),
                            prompt=f"สำรวจนักเรียนกลุ่มหนึ่งพบว่า {facts} มีนักเรียนที่ชอบอย่างน้อยหนึ่งอย่างกี่คน",
                            # Forgetting to add back the triple, and simply adding.
                            distractors=_story.keep(union - abc, A + B + C, A + B + C - AB - BC - AC,
                                                    union + abc, answer=union, lo=1))
        if kind == 1:
            return MathDraw("", str(oa),
                            prompt=f"สำรวจนักเรียนกลุ่มหนึ่งพบว่า {facts} มีนักเรียนที่ชอบ{x}อย่างเดียวกี่คน",
                            distractors=_story.keep(A - AB - AC, A - AB - AC + 2 * abc, A - ab - ac,
                                                    A, answer=oa, lo=0))
        return MathDraw("", str(none),
                        prompt=(f"นักเรียน {total} คน {facts} มีนักเรียนที่ไม่ชอบทั้งสามอย่างกี่คน"),
                        distractors=_story.keep(total - (A + B + C) if total >= A + B + C else none + abc,
                                                none + abc, total - union + AB, answer=none, lo=0))
ThreeSetCountingM4.PROVENANCE = Provenance("original")

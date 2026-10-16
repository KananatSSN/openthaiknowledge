"""ตรรกศาสตร์

คณิตศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.4/1, ค เพิ่มเติม จำนวนและพีชคณิต 1 ม.4/2

Sets moved here from: math, math_bank_logic, math_bank_textbook_logic, math_data, math_m4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType
from otk.sets._support.math_bank_logic import assignments, evaluate, table
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p2 import _texts

TOPIC = "ตรรกศาสตร์"


BINARY = ("and", "or", "imp", "iff")


_TEX = {"and": r"\land", "or": r"\lor", "imp": r"\to", "iff": r"\leftrightarrow"}


def var(name: str) -> tuple:
    return ("var", name)


def neg(f: tuple) -> tuple:
    return ("not", f)


def variables(f: tuple) -> list[str]:
    if f[0] == "var":
        return [f[1]]
    return sorted(set().union(*(variables(g) for g in f[1:])))


def tex(f: tuple) -> str:
    kind = f[0]
    if kind == "var":
        return f[1]
    if kind == "not":
        inner = tex(f[1])
        return r"\sim " + (inner if f[1][0] in ("var", "not") else f"({inner})")
    parts = [tex(g) if g[0] in ("var", "not") else f"({tex(g)})" for g in f[1:]]
    return f"{parts[0]} {_TEX[kind]} {parts[1]}"


def random_formula(rng: Random, names: list[str], depth: int) -> tuple:
    if depth == 0 or rng.random() < 0.25:
        leaf = var(rng.choice(names))
        return neg(leaf) if rng.random() < 0.35 else leaf
    left = random_formula(rng, names, depth - 1)
    right = random_formula(rng, names, depth - 1)
    while tex(right) == tex(left):           # no degenerate p ∧ p
        right = random_formula(rng, names, depth - 1)
    f = (rng.choice(BINARY), left, right)
    return neg(f) if rng.random() < 0.1 else f


def _tf(b: bool) -> str:
    return "จริง" if b else "เท็จ"


def _pick_split(rng: Random, envs: list[dict], names: list[str], want: bool,
                depth: int = 2, tries: int = 4000) -> tuple[tuple, list[tuple]] | None:
    """One formula with value ``want`` on every env, three with ``not want`` on every env.

    All four have distinct TeX. Returns None if not found within ``tries``.
    """
    right = None
    wrongs: list[tuple] = []
    seen: set[str] = set()
    for _ in range(tries):
        f = random_formula(rng, names, depth)
        if f[0] not in BINARY or tex(f) in seen or len(variables(f)) < 2:
            continue
        vals = {evaluate(f, env) for env in envs}
        if vals == {want} and right is None:
            right = f
            seen.add(tex(f))
        elif vals == {not want} and len(wrongs) < 3:
            wrongs.append(f)
            seen.add(tex(f))
        if right is not None and len(wrongs) == 3:
            return right, wrongs
    return None


def _math_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]),
                             topic=topic)


def _text_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    return GeneratedQuestion(stem=stem, correct=[text(right)],
                             distractors=fixed(*[[text(w)] for w in wrongs]), topic=topic)


def forced(premise: tuple, value: bool, names: list[str]) -> list[dict]:
    """Every assignment under which ``premise`` has ``value``."""
    return [env for env in assignments(names) if evaluate(premise, env) == value]


def draw_deduce(rng: Random):
    """``(premise, its value, asked value, right, wrongs)``. The premise pins
    every variable, and the options split cleanly on that one assignment."""
    names = ["p", "q", "r"]
    while True:
        premise = random_formula(rng, names, 2)
        if premise[0] not in BINARY or len(variables(premise)) < 3:
            continue
        value = rng.random() < 0.5
        envs = forced(premise, value, names)
        if len(envs) != 1:
            continue                          # the premise must pin every value
        want = rng.random() < 0.5
        found = _pick_split(rng, envs, names, want)
        if found:
            return premise, value, want, *found


_PEOPLE = ("ปิติ", "มานี", "ชูใจ", "โต้ง", "จ้อย")


_VERBS = ("กวาดบ้าน", "รดน้ำต้นไม้", "ซักผ้า", "อ่านหนังสือ", "ดูทีวี", "เล่นเกม",
          "ทำการบ้าน", "ใส่แว่นตา", "ใส่นาฬิกาข้อมือ")


def thai(f: tuple, who: str, verbs: dict[str, str]) -> str:
    """A binary-of-literals formula as a Thai sentence ("ถ้า…แล้ว…", "…ก็ต่อเมื่อ…")."""
    def lit(g: tuple) -> str:
        if g[0] == "not":
            return f"{who}ไม่ได้{verbs[g[1][1]]}"
        return f"{who}{verbs[g[1]]}"
    op, a, b = f
    a, b = lit(a), lit(b)
    return {"and": f"{a}และ{b}", "or": f"{a}หรือ{b}", "imp": f"ถ้า{a} แล้ว{b}",
            "iff": f"{a}ก็ต่อเมื่อ{b}"}[op]


def _literal_binary(rng: Random, names: list[str]) -> tuple:
    a, b = rng.sample(names, 2)
    lits = [var(a) if rng.random() < 0.6 else neg(var(a)),
            var(b) if rng.random() < 0.6 else neg(var(b))]
    return (rng.choice(BINARY), *lits)


def draw_verbal(rng: Random, who: str, verbs: dict[str, str]):
    """``(premises [(formula, value)], asked value, right, wrongs)``: two
    premises that pin every variable, and options that split cleanly."""
    names = ["p", "q", "r"]
    while True:
        premises = [(_literal_binary(rng, names), rng.random() < 0.5) for _ in range(2)]
        envs = [env for env in assignments(names)
                if all(evaluate(f, env) == v for f, v in premises)]
        if len(envs) != 1:
            continue
        want = rng.random() < 0.5
        options: list[tuple] = []
        right = None
        seen = {thai(f, who, verbs) for f, _ in premises}
        for _ in range(400):
            f = _literal_binary(rng, names)
            s = thai(f, who, verbs)
            if s in seen:
                continue
            val = evaluate(f, envs[0])
            if val == want and right is None:
                right = f
                seen.add(s)
            elif val != want and len(options) < 3:
                options.append(f)
                seen.add(s)
            if right is not None and len(options) == 3:
                return premises, want, right, options


_ROWS = ((True, True), (True, False), (False, True), (False, False))


_TRIVIAL = {(True, True, False, False), (False, False, True, True),     # p, ~p
            (True, False, True, False), (False, True, False, True)}     # q, ~q


#: (TeX, predicate) open sentences in x.
_PREDICATES = (
    (r"x + 1 \le 5", lambda x: x + 1 <= 5),
    (r"2x > 5", lambda x: 2 * x > 5),
    (r"x^2 > 4", lambda x: x * x > 4),
    (r"x - 3 > 0", lambda x: x - 3 > 0),
    (r"x^2 < 10", lambda x: x * x < 10),
    (r"x + 2 = x^2", lambda x: x + 2 == x * x),
    (r"x^2 - 1 \ge 0", lambda x: x * x - 1 >= 0),
    (r"3x \le 9", lambda x: 3 * x <= 9),
)


def quantified(rng: Random) -> tuple[str, object]:
    """A random closed statement: (TeX, evaluator over a universe)."""
    (pt, p), (qt, q) = rng.sample(_PREDICATES, 2)
    op = rng.choice(("imp", "iff", "and", "or"))
    comb = {"imp": lambda x: (not p(x)) or q(x), "iff": lambda x: p(x) == q(x),
            "and": lambda x: p(x) and q(x), "or": lambda x: p(x) or q(x)}[op]
    inner = f"{pt} {_TEX[op]} {qt}"
    shape = rng.randrange(4)
    if shape == 0:
        return rf"\forall x\,[{inner}]", lambda U: all(comb(x) for x in U)
    if shape == 1:
        return rf"\exists x\,[{inner}]", lambda U: any(comb(x) for x in U)
    if shape == 2:
        return (rf"\forall x\,[{pt}] \to \exists x\,[{qt}]",
                lambda U: (not all(p(x) for x in U)) or any(q(x) for x in U))
    return (rf"\exists x\,[{pt}] \land \forall x\,[{qt}]",
            lambda U: any(p(x) for x in U) and all(q(x) for x in U))


PROP, OPEN, NONE = "prop", "open", "none"


#: (sentence, kind, truth for a proposition, Python check for a mathematical one)
SENTENCES: tuple[tuple[str, str, bool | None, str], ...] = (
    ("7 เป็นจำนวนเฉพาะ", PROP, True, "all(7 % d for d in range(2, 7))"),
    ("9 เป็นจำนวนเฉพาะ", PROP, False, "all(9 % d for d in range(2, 9))"),
    ("12 หารด้วย 5 ลงตัว", PROP, False, "12 % 5 == 0"),
    ("15 หารด้วย 3 ลงตัว", PROP, True, "15 % 3 == 0"),
    ("2 + 3 = 6", PROP, False, "2 + 3 == 6"),
    ("4 × 5 = 20", PROP, True, "4 * 5 == 20"),
    ("−20 + 5 > −17", PROP, True, "-20 + 5 > -17"),
    ("π > 3", PROP, True, "3.14159 > 3"),
    ("√2 เป็นจำนวนเต็ม", PROP, False, "int(2 ** 0.5) ** 2 == 2"),
    ("7 เป็นตัวประกอบของ 217", PROP, True, "217 % 7 == 0"),
    ("35% = 0.35", PROP, True, "35 / 100 == 0.35"),
    ("ตัวประกอบที่เป็นจำนวนเต็มบวกของ 12 มี 6 ตัว", PROP, True,
     "sum(12 % d == 0 for d in range(1, 13)) == 6"),
    ("3 ∈ {1, 2, 3}", PROP, True, "3 in {1, 2, 3}"),
    ("{1, 2} ⊂ {1, 3}", PROP, False, "{1, 2} <= {1, 3}"),
    ("เดือนสิงหาคมมี 30 วัน", PROP, False, ""),
    ("ช้างเป็นสัตว์เลี้ยงลูกด้วยน้ำนม", PROP, True, ""),
    ("ดาวพุธเป็นดาวเคราะห์", PROP, True, ""),
    ("จังหวัดเชียงใหม่อยู่ในภาคใต้ของประเทศไทย", PROP, False, ""),
    ("x + 2 = 5", OPEN, None, ""),
    ("x² − 1 ≥ 0", OPEN, None, ""),
    ("2x + 1 เป็นจำนวนคี่", OPEN, None, ""),
    ("เขาเป็นนักกีฬาของโรงเรียน", OPEN, None, ""),
    ("เธอเรียนอยู่ชั้นมัธยมศึกษาปีที่ 4", OPEN, None, ""),
    ("ถ้า x เป็นจำนวนคู่ แล้ว x² เป็นจำนวนคู่", OPEN, None, ""),
    ("กรุณารักษาความสะอาด", NONE, None, ""),
    ("ห้ามเดินลัดสนาม", NONE, None, ""),
    ("จงตอบคำถามต่อไปนี้", NONE, None, ""),
    ("ฝนตกหรือเปล่า", NONE, None, ""),
    ("ทำไมมาโรงเรียนสาย", NONE, None, ""),
    ("ช่วยด้วย", NONE, None, ""),
    ("ยินดีต้อนรับ", NONE, None, ""),
    ("x² − 1", NONE, None, ""),
    ("3 + 4", NONE, None, ""),
)


ASKS = (
    ("ข้อใดเป็นประพจน์", lambda k, t: k == PROP),
    ("ข้อใดไม่เป็นประพจน์", lambda k, t: k != PROP),
    ("ข้อใดเป็นประโยคเปิด", lambda k, t: k == OPEN),
    ("ข้อใดเป็นประพจน์ที่มีค่าความจริงเป็นจริง", lambda k, t: k == PROP and t is True),
    ("ข้อใดเป็นประพจน์ที่มีค่าความจริงเป็นเท็จ", lambda k, t: k == PROP and t is False),
)


@question_type("math.truth_value",
               display_name={"th": "ค่าความจริงของประพจน์เชิงประกอบ"},
               level={"th": "ม.4"}, topic="ตรรกศาสตร์")
class TruthValue(ChoiceType):
    def compose(self, rng: Random):
        p, q = rng.choice([True, False]), rng.choice([True, False])
        sym, val = rng.choice([
            ("∧", p and q), ("∨", p or q),
            ("→", (not p) or q), ("↔", p == q)])
        tf = lambda b: "จริง" if b else "เท็จ"
        stem = f"ถ้า p เป็น{tf(p)} และ q เป็น{tf(q)} แล้ว p {sym} q มีค่าความจริงใด?"
        return stem, tf(val), [tf(not val)]
TruthValue.PROVENANCE = Provenance("original")


@question_type("math.logic_negation", display_name={"th": "นิเสธของประพจน์"},
               level={"th": "ม.4"}, topic="ตรรกศาสตร์")
class LogicNegation(ChoiceType):
    """De Morgan, and the quantifier swap that trips everyone up."""

    ITEMS = [
        ("นิเสธของ “p และ q” คือข้อใด", "~p หรือ ~q",
         ["~p และ ~q", "p หรือ q", "~p → ~q"]),
        ("นิเสธของ “p หรือ q” คือข้อใด", "~p และ ~q",
         ["~p หรือ ~q", "p และ q", "q → p"]),
        ("นิเสธของ “สำหรับทุก x, P(x)” คือข้อใด", "มีบาง x ที่ ~P(x)",
         ["สำหรับทุก x, ~P(x)", "มีบาง x ที่ P(x)", "ไม่มี x ใดที่ P(x)"]),
        ("นิเสธของ “มีบาง x ที่ P(x)” คือข้อใด", "สำหรับทุก x, ~P(x)",
         ["มีบาง x ที่ ~P(x)", "สำหรับทุก x, P(x)", "ไม่มีนิเสธ"]),
        ("นิเสธของ “ถ้า p แล้ว q” คือข้อใด", "p และ ~q",
         ["~p และ q", "ถ้า ~p แล้ว ~q", "~p หรือ q"]),
        ("นิเสธของ “p ↔ q” สมมูลกับข้อใด", "p ↔ ~q",
         ["~p ↔ ~q", "q ↔ p", "~p ∧ ~q"]),
        ("นิเสธของ “นักเรียนทุกคนชอบคณิตศาสตร์” คือข้อใด", "มีนักเรียนบางคนไม่ชอบคณิตศาสตร์",
         ["นักเรียนทุกคนไม่ชอบคณิตศาสตร์", "มีนักเรียนบางคนชอบคณิตศาสตร์",
          "ไม่มีนักเรียนคนใดชอบคณิตศาสตร์"]),
        ("นิเสธของ “มีจำนวนจริง x ที่ x² < 0” คือข้อใด", "สำหรับจำนวนจริง x ทุกตัว x² ≥ 0",
         ["สำหรับจำนวนจริง x ทุกตัว x² < 0", "มีจำนวนจริง x ที่ x² ≥ 0",
          "มีจำนวนจริง x ที่ x² > 0"]),
        ("นิเสธของ “x > 3” คือข้อใด", "x ≤ 3", ["x < 3", "x ≥ 3", "x < −3"]),
    ]
    # (p, not p, q, not q) in words.
    _CLAUSES = [
        ("ฝนตก", "ฝนไม่ตก", "ฟ้าร้อง", "ฟ้าไม่ร้อง"),
        ("นิดไปโรงเรียน", "นิดไม่ไปโรงเรียน", "นิดทำการบ้าน", "นิดไม่ทำการบ้าน"),
        ("วันนี้อากาศร้อน", "วันนี้อากาศไม่ร้อน", "ร้านขายไอศกรีมได้มาก",
         "ร้านขายไอศกรีมได้ไม่มาก"),
        ("x เป็นจำนวนคู่", "x ไม่เป็นจำนวนคู่", "x มากกว่า 10", "x ไม่มากกว่า 10"),
    ]

    def compose(self, rng: Random):
        if rng.random() < 0.4:
            p, np, q, nq = rng.choice(self._CLAUSES)
            form = rng.randrange(3)
            if form == 0:
                return (f"นิเสธของ “{p}และ{q}” คือข้อใด", f"{np}หรือ{nq}",
                        [f"{np}และ{nq}", f"{p}หรือ{q}", f"ถ้า{np} แล้ว{nq}"])
            if form == 1:
                return (f"นิเสธของ “{p}หรือ{q}” คือข้อใด", f"{np}และ{nq}",
                        [f"{np}หรือ{nq}", f"{p}และ{q}", f"ถ้า{q} แล้ว{p}"])
            return (f"นิเสธของ “ถ้า{p} แล้ว{q}” คือข้อใด", f"{p}และ{nq}",
                    [f"{np}และ{q}", f"ถ้า{np} แล้ว{nq}", f"{np}หรือ{q}"])
        return rng.choice(self.ITEMS)
LogicNegation.PROVENANCE = Provenance("original")


@question_type("math.valid_argument",
               display_name={"th": "การอ้างเหตุผลสมเหตุสมผลหรือไม่"},
               level={"th": "ม.4"}, topic="ตรรกศาสตร์")
class ValidArgument(ChoiceType):
    _FORMS = [
        ("p → q และ p ดังนั้น q", "สมเหตุสมผล"),
        ("p → q และ ¬q ดังนั้น ¬p", "สมเหตุสมผล"),
        ("p → q และ q ดังนั้น p", "ไม่สมเหตุสมผล"),
        ("p → q และ ¬p ดังนั้น ¬q", "ไม่สมเหตุสมผล"),
        ("p → q และ q → r ดังนั้น p → r", "สมเหตุสมผล"),
        ("p ∨ q และ ¬p ดังนั้น q", "สมเหตุสมผล"),
        ("p ∨ q และ p ดังนั้น ¬q", "ไม่สมเหตุสมผล"),
        ("p ∧ q ดังนั้น p", "สมเหตุสมผล"),
        ("p ดังนั้น p ∨ q", "สมเหตุสมผล"),
        ("p → q ดังนั้น q → p", "ไม่สมเหตุสมผล"),
        ("p → q ดังนั้น ¬q → ¬p", "สมเหตุสมผล"),
        ("p ↔ q และ ¬p ดังนั้น ¬q", "สมเหตุสมผล"),
        ("p → q, q → r และ ¬r ดังนั้น ¬p", "สมเหตุสมผล"),
        ("p → r, q → r และ r ดังนั้น p", "ไม่สมเหตุสมผล"),
    ]
    # (p, not p, q, not q) in words.
    _CLAUSES = [
        ("ฝนตก", "ฝนไม่ตก", "ถนนเปียก", "ถนนไม่เปียก"),
        ("นิดตั้งใจเรียน", "นิดไม่ตั้งใจเรียน", "นิดสอบผ่าน", "นิดสอบไม่ผ่าน"),
        ("วันนี้เป็นวันเสาร์", "วันนี้ไม่เป็นวันเสาร์", "โรงเรียนปิด", "โรงเรียนไม่ปิด"),
        ("n หารด้วย 4 ลงตัว", "n หารด้วย 4 ไม่ลงตัว", "n เป็นจำนวนคู่", "n ไม่เป็นจำนวนคู่"),
        ("รูปนี้เป็นรูปสี่เหลี่ยมจัตุรัส", "รูปนี้ไม่เป็นรูปสี่เหลี่ยมจัตุรัส",
         "รูปนี้มีมุมฉาก", "รูปนี้ไม่มีมุมฉาก"),
    ]
    # Modus ponens and tollens, and their two look-alikes.
    _WORDED = [("{p}", "{q}", "สมเหตุสมผล"), ("{nq}", "{np}", "สมเหตุสมผล"),
               ("{q}", "{p}", "ไม่สมเหตุสมผล"), ("{np}", "{nq}", "ไม่สมเหตุสมผล")]

    def compose(self, rng: Random):
        if rng.random() < 0.4:
            p, np, q, nq = rng.choice(self._CLAUSES)
            given, then, label = rng.choice(self._WORDED)
            words = dict(p=p, np=np, q=q, nq=nq)
            other = "ไม่สมเหตุสมผล" if label == "สมเหตุสมผล" else "สมเหตุสมผล"
            return (f"เหตุ 1) ถ้า{p} แล้ว{q}  2) {given.format(**words)}  "
                    f"ผล: {then.format(**words)}  การอ้างเหตุผลนี้สมเหตุสมผลหรือไม่?"), label, [other]
        form, label = rng.choice(self._FORMS)
        other = "ไม่สมเหตุสมผล" if label == "สมเหตุสมผล" else "สมเหตุสมผล"
        return f"การอ้างเหตุผล “{form}” สมเหตุสมผลหรือไม่?", label, [other]
ValidArgument.PROVENANCE = Provenance("original")


M4 = {"th": "ม.4"}


M4 = {"th": "ม.4"}


@question_type("math.logic_compound_value_m4",
               display_name={"th": "ค่าความจริงของประพจน์เชิงประกอบหลายชั้น"},
               level=M4, topic=TOPIC)
class LogicCompoundValueM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        names = ["p", "q", "r"]
        while True:
            env = {n: rng.random() < 0.5 for n in names}
            want = rng.random() < 0.5
            found = _pick_split(rng, [env], names, want)
            if found:
                break
        right, wrongs = found
        given = " ".join(f"{n} มีค่าความจริงเป็น{_tf(env[n])}" for n in names)
        stem = [text(f"กำหนดให้ {given} ประพจน์ในข้อใดมีค่าความจริงเป็น{_tf(want)}")]
        return _math_q(stem, tex(right), [tex(w) for w in wrongs], self.topic)
LogicCompoundValueM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.proposition_identify_m4",
               display_name={"th": "ประพจน์ ประโยคเปิด และข้อความที่ไม่เป็นประพจน์"},
               level=M4, topic="ตรรกศาสตร์")
class PropositionIdentifyM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        ask, fits = rng.choice(ASKS)
        right = [s for s, k, t, _ in SENTENCES if fits(k, t)]
        wrong = [s for s, k, t, _ in SENTENCES if not fits(k, t)]
        # Mix the kinds among the wrong choices: one of each kind first.
        by_kind: dict[str, list[str]] = {}
        for s, k, t, _ in SENTENCES:
            if not fits(k, t):
                by_kind.setdefault(f"{k}{t}", []).append(s)
        picks = [rng.choice(v) for v in by_kind.values()]
        rng.shuffle(picks)
        rest = [s for s in wrong if s not in picks]
        rng.shuffle(rest)
        wrongs = (picks + rest)[:3]
        answer = rng.choice(right)
        return GeneratedQuestion(stem=[text(ask)], correct=[text(answer)],
                                 distractors=fixed(*[[text(w)] for w in wrongs]), topic=self.topic)
PropositionIdentifyM4.PROVENANCE = Provenance("original")


@question_type("math.logic_deduce_values_m4",
               display_name={"th": "ย้อนหาค่าความจริงจากค่าของประพจน์เชิงประกอบ"},
               level=M4, topic=TOPIC)
class LogicDeduceValuesM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        premise, value, want, right, wrongs = draw_deduce(rng)
        stem = [text("ให้ p, q และ r เป็นประพจน์ ถ้า"), content_math(tex(premise)),
                text(f"มีค่าความจริงเป็น{_tf(value)} ประพจน์ในข้อใดมีค่าความจริงเป็น{_tf(want)}")]
        return _math_q(stem, tex(right), [tex(w) for w in wrongs], self.topic)
LogicDeduceValuesM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.logic_verbal_deduction_m4",
               display_name={"th": "หาค่าความจริงของข้อความจากข้อความที่กำหนด"},
               level=M4, topic=TOPIC)
class LogicVerbalDeductionM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        who = rng.choice(_PEOPLE)
        verbs = dict(zip(["p", "q", "r"], rng.sample(_VERBS, 3)))
        premises, want, right, options = draw_verbal(rng, who, verbs)
        given = " และ ".join(f"“{thai(f, who, verbs)}” มีค่าความจริงเป็น{_tf(v)}"
                             for f, v in premises)
        stem = [text(f"กำหนดให้ประพจน์ {given} ประพจน์ในข้อใดมีค่าความจริงเป็น{_tf(want)}")]
        return _text_q(stem, thai(right, who, verbs), [thai(f, who, verbs) for f in options],
                       self.topic)
LogicVerbalDeductionM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.logic_quantifier_finite_m4",
               display_name={"th": "ค่าความจริงของตัวบ่งปริมาณบนเอกภพสัมพัทธ์จำกัด"},
               level=M4, topic=TOPIC)
class LogicQuantifierFiniteM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            lo = rng.randint(-2, 3)
            U = list(range(lo, lo + rng.randint(3, 4)))
            want = rng.random() < 0.5
            right, wrongs, seen = None, [], set()
            for _ in range(300):
                s, ev = quantified(rng)
                if s in seen:
                    continue
                v = ev(U)
                if v == want and right is None:
                    right = s
                elif v != want and len(wrongs) < 3:
                    wrongs.append(s)
                else:
                    continue
                seen.add(s)
                if right and len(wrongs) == 3:
                    break
            if right and len(wrongs) == 3:
                break
        u = "{" + ", ".join(map(str, U)) + "}"
        stem = [text(f"ให้เอกภพสัมพัทธ์ U = {u} ข้อความในข้อใดมีค่าความจริงเป็น{_tf(want)}")]
        return _math_q(stem, right, wrongs, self.topic)
LogicQuantifierFiniteM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.quantifier_truth_m4",
               display_name={"th": "ค่าความจริงของประโยคที่มีตัวบ่งปริมาณ"},
               level=M4, topic="ตรรกศาสตร์")
class QuantifierTruthM4(QuestionType):
    # (statement, truth) over the real numbers unless stated.
    _BANK = (
        (r"\forall x\,[x^{2} \ge 0]", True), (r"\forall x\,[x^{2} > 0]", False),
        (r"\exists x\,[x^{2} = 0]", True), (r"\exists x\,[x^{2} < 0]", False),
        (r"\forall x\,[x + 0 = x]", True), (r"\forall x\,[2x > x]", False),
        (r"\exists x\,[2x = x]", True), (r"\forall x\,[|x| \ge x]", True),
        (r"\forall x\,[|x| = x]", False), (r"\exists x\,[x^{2} + 1 = 0]", False),
        (r"\exists x\,[x^{2} = 2x]", True), (r"\forall x\,[x^{2} \ge x]", False),
        (r"\forall x\,[(x - 1)^{2} \ge 0]", True), (r"\exists x\,[|x| < 0]", False),
        (r"\exists x\,[\tfrac{1}{x} = x]", True), (r"\forall x\,[x^{3} \ge x]", False),
    )

    def build(self, rng: Random) -> GeneratedQuestion:
        want = rng.random() < 0.5
        good = [s for s, t in self._BANK if t == want]
        bad = [s for s, t in self._BANK if t != want]
        return maths([text(f"เมื่อเอกภพสัมพัทธ์คือเซตของจำนวนจริง ข้อใดมีค่าความจริงเป็น"
                            f"{'จริง' if want else 'เท็จ'}")],
                      rng.choice(good), rng.sample(bad, 3), self.topic)
QuantifierTruthM4.PROVENANCE = Provenance("original")


@question_type("math.logic_tautology_m4",
               display_name={"th": "สัจนิรันดร์"},
               level=M4, topic=TOPIC)
class LogicTautologyM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        names = ["p", "q", "r"]
        contingent_asked = rng.random() < 0.3
        right, wrongs, seen = None, [], set()
        while right is None or len(wrongs) < 3:
            f = ("imp", random_formula(rng, names, 1), random_formula(rng, names, 1))
            vs = variables(f)
            if len(vs) < 2 or tex(f) in seen:
                continue
            values = set(table(f, names))
            constant = len(values) == 1          # a tautology or a contradiction
            is_taut = values == {True}
            if contingent_asked:
                if not constant and right is None:
                    right = f
                elif constant and len(wrongs) < 3:
                    wrongs.append(f)
                else:
                    continue
            else:
                if is_taut and right is None:
                    right = f
                elif not is_taut and len(wrongs) < 3:
                    wrongs.append(f)
                else:
                    continue
            seen.add(tex(f))
        ask = ("ข้อใดต่อไปนี้สามารถมีค่าความจริงได้มากกว่า 1 ค่า" if contingent_asked
               else "ข้อใดต่อไปนี้เป็นสัจนิรันดร์")
        stem = [text(f"ให้ p, q และ r เป็นประพจน์ {ask}")]
        return _math_q(stem, tex(right), [tex(w) for w in wrongs], self.topic)
LogicTautologyM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.logic_custom_connective_m4",
               display_name={"th": "ตัวเชื่อมที่นิยามด้วยตารางค่าความจริง"},
               level=M4, topic=TOPIC)
class LogicCustomConnectiveM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        names = ["p", "q"]
        while True:
            star = tuple(rng.random() < 0.5 for _ in _ROWS)
            if len(set(star)) == 2 and star not in _TRIVIAL:
                break
        negated = rng.random() < 0.4
        target = tuple(not v for v in star) if negated else star
        right, wrongs, seen = None, [], set()
        while right is None or len(wrongs) < 3:
            f = random_formula(rng, names, 2)
            if f[0] not in BINARY and f[0] != "not" or tex(f) in seen or len(variables(f)) < 2:
                continue
            t = table(f, names)
            if t == target and right is None:
                right = f
            elif t != target and len(set(t)) == 2 and len(wrongs) < 3 \
                    and t not in {table(w, names) for w in wrongs}:
                wrongs.append(f)
            else:
                continue
            seen.add(tex(f))
        rows = ["p | q | p ∗ q"] + [f"{'T' if a else 'F'} | {'T' if b else 'F'} | {'T' if v else 'F'}"
                                    for (a, b), v in zip(_ROWS, star)]
        ask = "นิเสธของ p ∗ q สมมูลกับข้อใด" if negated else "p ∗ q สมมูลกับข้อใด"
        stem = [text("กำหนดให้ p และ q เป็นประพจน์ และ p ∗ q มีค่าความจริงดังตาราง"),
                text("\n".join(rows)), text(ask)]
        return _math_q(stem, tex(right), [tex(w) for w in wrongs], self.topic)
LogicCustomConnectiveM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์',))


@question_type("math.logic_equivalence_m4",
               display_name={"th": "รูปแบบของประพจน์ที่สมมูลกัน"},
               level=M4, topic="ตรรกศาสตร์")
class LogicEquivalenceM4(QuestionType):
    # (form, equivalent, three non-equivalents) — checked by truth table in the tests.
    _FORMS = (
        (r"p \to q", r"{\sim}q \to {\sim}p", (r"q \to p", r"{\sim}p \to {\sim}q", r"p \land {\sim}q")),
        (r"p \to q", r"{\sim}p \lor q", (r"p \lor {\sim}q", r"{\sim}p \land q", r"q \to p")),
        (r"{\sim}(p \land q)", r"{\sim}p \lor {\sim}q", (r"{\sim}p \land {\sim}q", r"p \lor q",
                                                         r"{\sim}p \land q")),
        (r"{\sim}(p \lor q)", r"{\sim}p \land {\sim}q", (r"{\sim}p \lor {\sim}q", r"p \land q",
                                                          r"{\sim}p \lor q")),
        (r"{\sim}(p \to q)", r"p \land {\sim}q", (r"{\sim}p \to {\sim}q", r"{\sim}p \land q",
                                                   r"q \to p")),
        (r"p \leftrightarrow q", r"(p \to q) \land (q \to p)", (r"(p \to q) \lor (q \to p)",
                                                                r"p \land q", r"p \to q")),
        (r"p \lor q", r"{\sim}p \to q", (r"p \to q", r"{\sim}p \land q", r"{\sim}q \to {\sim}p")),
        (r"p \to {\sim}q", r"q \to {\sim}p", (r"{\sim}p \to q", r"{\sim}q \to p", r"p \land q")),
        (r"{\sim}p \to {\sim}q", r"q \to p", (r"p \to q", r"{\sim}q \to {\sim}p", r"p \land {\sim}q")),
        (r"p \leftrightarrow q", r"{\sim}p \leftrightarrow {\sim}q",
         (r"p \leftrightarrow {\sim}q", r"p \land q", r"{\sim}p \land {\sim}q")),
        (r"{\sim}(p \leftrightarrow q)", r"p \leftrightarrow {\sim}q",
         (r"{\sim}p \leftrightarrow {\sim}q", r"{\sim}p \land {\sim}q", r"p \lor q")),
    )
    # (p, not p, q, not q)
    _WORDS = (("ฝนตก", "ฝนไม่ตก", "ถนนเปียก", "ถนนไม่เปียก"),
              ("นักเรียนขยันเรียน", "นักเรียนไม่ขยันเรียน", "นักเรียนสอบผ่าน", "นักเรียนสอบไม่ผ่าน"),
              ("วันนี้เป็นวันเสาร์", "วันนี้ไม่ใช่วันเสาร์", "โรงเรียนปิด", "โรงเรียนไม่ปิด"),
              ("สามเหลี่ยมมีมุมฉาก", "สามเหลี่ยมไม่มีมุมฉาก", "ใช้ทฤษฎีบทพีทาโกรัสได้",
               "ใช้ทฤษฎีบทพีทาโกรัสไม่ได้"),
              ("n หารด้วย 6 ลงตัว", "n หารด้วย 6 ไม่ลงตัว", "n หารด้วย 3 ลงตัว", "n หารด้วย 3 ไม่ลงตัว"),
              ("เก่งออกกำลังกายทุกวัน", "เก่งไม่ได้ออกกำลังกายทุกวัน", "เก่งแข็งแรง", "เก่งไม่แข็งแรง"),
              ("น้ำถูกทำให้เย็นลงต่ำกว่า 0 องศาเซลเซียส", "น้ำไม่ถูกทำให้เย็นลงต่ำกว่า 0 องศาเซลเซียส",
               "น้ำกลายเป็นน้ำแข็ง", "น้ำไม่กลายเป็นน้ำแข็ง"))

    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.6:
            form, right, wrongs = rng.choice(self._FORMS)
            return maths([text("ประพจน์ใดสมมูลกับประพจน์ต่อไปนี้"), content_math(form)], right,
                          list(wrongs), self.topic)
        p, np_, q, nq = rng.choice(self._WORDS)
        # The contrapositive; then the converse, the inverse, and the negation.
        return _texts([text(f"ข้อความ “ถ้า{p} แล้ว{q}” สมมูลกับข้อความใด")], f"ถ้า{nq} แล้ว{np_}",
                      [f"ถ้า{q} แล้ว{p}", f"ถ้า{np_} แล้ว{nq}", f"{p} และ{nq}"], self.topic)
LogicEquivalenceM4.PROVENANCE = Provenance("original")

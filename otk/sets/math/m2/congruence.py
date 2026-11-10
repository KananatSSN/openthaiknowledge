"""ความเท่ากันทุกประการ

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math, math_formats_hi, math_geometry.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import _text_q

PROVENANCE = Provenance("original")


class CongruentPair(NamedTuple):
    case: str            # sss | sas | asa | aas | rhs | aaa
    variant: int

    @property
    def asset_id(self) -> str:
        return f"mcong_{self.case}_{self.variant}"


CASE_THAI = {"sss": "ด.ด.ด.", "sas": "ด.ม.ด.", "asa": "ม.ด.ม.", "aas": "ม.ม.ด.",
             "rhs": "ฉ.ด.ด.", "aaa": "สรุปไม่ได้ว่าเท่ากันทุกประการ"}


CONGRUENT_PAIRS = tuple(CongruentPair(c, v) for c in CASE_THAI for v in range(2))


CONG_ALT = "รูปสามเหลี่ยมสองรูป มีเครื่องหมายแสดงด้านและมุมที่เท่ากัน"


@question_type("math.congruence_case",
               display_name={"th": "กรณีความเท่ากันทุกประการของสามเหลี่ยม"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruenceCase(ConceptBankType):
    ITEMS = [
        Concept("ถ้าทราบด้านสองด้านและมุมระหว่างด้าน ใช้กรณีใด?", "ด.ม.ด.",
                ("ม.ด.ม.", "ด.ด.ด.", "ม.ม.ด.")),
        Concept("ถ้าทราบมุมสองมุมและด้านระหว่างมุม ใช้กรณีใด?", "ม.ด.ม.",
                ("ด.ม.ด.", "ด.ด.ด.", "ม.ม.ด.")),
        Concept("ถ้าทราบด้านทั้งสามด้าน ใช้กรณีใด?", "ด.ด.ด.",
                ("ด.ม.ด.", "ม.ด.ม.", "ม.ม.ด.")),
        Concept("ถ้าทราบมุมสองมุมและด้านที่ไม่ใช่ด้านระหว่างมุม ใช้กรณีใด?",
                "ม.ม.ด.", ("ด.ม.ด.", "ม.ด.ม.", "ด.ด.ด.")),
    ]


@question_type("math.congruence_picture_m2", display_name={"th": "บอกกรณีความเท่ากันทุกประการจากรูป"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruencePictureM2(QuestionType):
    _NEAR = {"sss": ("ด.ม.ด.", "ฉ.ด.ด."), "sas": ("ม.ด.ม.", "ด.ด.ด."), "asa": ("ม.ม.ด.", "ด.ม.ด."),
             "aas": ("ม.ด.ม.", "สรุปไม่ได้ว่าเท่ากันทุกประการ"), "rhs": ("ด.ม.ด.", "ด.ด.ด."),
             "aaa": ("ม.ม.ด.", "ม.ด.ม.")}

    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(CONGRUENT_PAIRS)
        right = CASE_THAI[p.case]
        others = [v for v in CASE_THAI.values() if v not in (right, *self._NEAR[p.case])]
        rng.shuffle(others)
        return _text_q([text("จากเครื่องหมายที่กำหนด รูปสามเหลี่ยมสองรูปนี้เท่ากันทุกประการ"
                             "ด้วยความสัมพันธ์แบบใด"), image(p.asset_id, alt=CONG_ALT)],
                       right, [*self._NEAR[p.case], *others], self.topic)


@question_type("math.congruent_sides", display_name={"th": "ด้านที่สมนัยกัน"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruentSides(WordProblem):
    """Congruence transfers measurements — the point of proving it at all."""

    def expr(self, rng: Random, lo: int = 4, hi: int = 25):
        ab, bc, ca = (rng.randint(lo, hi) for _ in range(3))
        # Three lengths make a triangle only when the longest is shorter than the other two together.
        # Otherwise shorten the longest to one less than their sum: still in range, no extra draw.
        sides = [ab, bc, ca]
        longest = max(range(3), key=lambda i: sides[i])
        rest = sum(sides) - sides[longest]
        if sides[longest] >= rest:
            sides[longest] = rest - 1
        ab, bc, ca = sides
        which = rng.choice([("DE", ab), ("EF", bc), ("FD", ca)])
        name, value = which
        return MathDraw(
            "", str(value),
            prompt=(f"รูปสามเหลี่ยม ABC เท่ากันทุกประการกับรูปสามเหลี่ยม DEF "
                    f"ถ้า AB = {ab}, BC = {bc} และ CA = {ca} เซนติเมตร "
                    f"แล้ว {name} ยาวกี่เซนติเมตร"),
            distractors=[str(v) for _, v in
                         [("DE", ab), ("EF", bc), ("FD", ca)] if v != value]
            + [str(ab + bc + ca)])


@question_type("math.congruent_angles", display_name={"th": "มุมที่สมนัยกัน"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruentAngles(WordProblem):
    def expr(self, rng: Random, lo: int = 25, hi: int = 110):
        a = rng.randint(lo, hi)
        b = rng.randint(lo, max(lo + 1, 175 - a))
        c = 180 - a - b
        which = rng.choice(["D", "E", "F"])
        value = {"D": a, "E": b, "F": c}[which]
        return MathDraw(
            "", str(value),
            prompt=(f"รูปสามเหลี่ยม ABC เท่ากันทุกประการกับรูปสามเหลี่ยม DEF "
                    f"ถ้ามุม A = {a} องศา และมุม B = {b} องศา "
                    f"แล้วมุม {which} มีขนาดกี่องศา"),
            distractors=[str(v) for k, v in {"D": a, "E": b, "F": c}.items()
                         if v != value] + ["180"])


# ── More congruence (สสวท. ม.2 เล่ม 1 บทที่ 2): reading a correspondence, the condition a case still
# needs, conditions that are not enough, corresponding parts written in x, and the reasons in a proof ──

_TOPIC = "ความเท่ากันทุกประการ"
_PERMS = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0))


def _named(rng: Random) -> tuple[str, str]:
    """ABC and a second triangle written in a shuffled order, so the correspondence is ABC → second."""
    other = rng.choice(("DEF", "PQR", "XYZ"))
    order = rng.choice(_PERMS)
    return "ABC", "".join(other[i] for i in order)


@question_type("math.congruence_correspondence_m2", display_name={"th": "ด้านและมุมที่สมนัยกันจากชื่อรูป"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceCorrespondenceM2(ChoiceType):
    """△ABC ≅ △QRP pairs letters by position in the name, not by the alphabet."""

    def compose(self, rng: Random):
        first, second = _named(rng)
        alpha = "".join(sorted(second))
        if rng.random() < 0.5:
            i, j = sorted(rng.sample(range(3), 2))
            k = 3 - i - j
            right = second[i] + second[j]
            # The letters matched by the alphabet; the other two sides; the same side's name copied.
            wrongs = [alpha[i] + alpha[j], second[i] + second[k] if i < k else second[k] + second[i],
                      second[j] + second[k] if j < k else second[k] + second[j], first[i] + first[j]]
            seen, unique = {frozenset(right)}, []
            for w in wrongs:
                if frozenset(w) not in seen:
                    seen.add(frozenset(w))
                    unique.append(w)
            wrongs = unique
            stem = f"ถ้า △{first} ≅ △{second} แล้วด้าน {first[i]}{first[j]} สมนัยกับด้านใด"
            return stem, f"ด้าน {right}", [f"ด้าน {w}" for w in wrongs]
        i = rng.randrange(3)
        right = second[i]
        wrongs = [alpha[i], *(second[k] for k in range(3) if k != i), first[i]]
        stem = f"ถ้า △{first} ≅ △{second} แล้ว ∠{first[i]} สมนัยกับมุมใด"
        return stem, f"∠{right}", [f"∠{w}" for w in dict.fromkeys(wrongs) if w != right]


def _element(kind: str, i: int, j: int, first: str, second: str) -> str:
    if kind == "a":
        return f"∠{first[i]} = ∠{second[i]}"
    i, j = min(i, j), max(i, j)
    return f"{first[i]}{first[j]} = {second[i]}{second[j]}"


@question_type("math.congruence_missing_condition_m2", display_name={"th": "เงื่อนไขที่ยังขาดเพื่อให้เท่ากันทุกประการ"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceMissingConditionM2(ChoiceType):
    """Two parts are given; which third part makes the named case?"""

    def compose(self, rng: Random):
        second = rng.choice(("DEF", "PQR", "XYZ"))
        case = rng.choice(("ด.ม.ด.", "ม.ด.ม.", "ด.ด.ด."))
        v = rng.randrange(3)
        a, b = (v + 1) % 3, (v + 2) % 3
        if case == "ด.ม.ด.":    # the angle at v between the sides va and vb
            parts = [("a", v, v), ("s", v, a), ("s", v, b)]
        elif case == "ม.ด.ม.":  # the angles at v and a with the side va between them
            parts = [("a", v, v), ("a", a, a), ("s", v, a)]
        else:
            parts = [("s", v, a), ("s", a, b), ("s", v, b)]
        missing = rng.randrange(3)
        given = [p for n, p in enumerate(parts) if n != missing]
        everything = [("s", 0, 1), ("s", 1, 2), ("s", 0, 2), ("a", 0, 0), ("a", 1, 1), ("a", 2, 2)]

        def same(p, q):
            return p[0] == q[0] and {p[1], p[2]} == {q[1], q[2]}

        others = [p for p in everything if not any(same(p, g) for g in parts)]
        if len(others) > 3:
            rng.shuffle(others)
        stated = " และ ".join(_element(*p, "ABC", second) for p in given)
        stem = (f"รูปสามเหลี่ยม ABC และ {second} มี {stated} ถ้าต้องการสรุปว่า △ABC ≅ △{second} "
                f"ด้วยกรณี {case} ต้องทราบเพิ่มอีกข้อใด")
        return stem, _element(*parts[missing], "ABC", second), [_element(*p, "ABC", second) for p in others[:3]]


@question_type("math.congruence_not_enough_m2", display_name={"th": "เงื่อนไขที่สรุปความเท่ากันทุกประการไม่ได้"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceNotEnoughM2(ChoiceType):
    """Three angles (ม.ม.ม.) or two sides with an angle not between them (ด.ด.ม.) do not prove congruence."""

    def compose(self, rng: Random):
        second = rng.choice(("DEF", "PQR", "XYZ"))
        v = rng.randrange(3)
        a, b = (v + 1) % 3, (v + 2) % 3

        def say(*parts):
            return ", ".join(_element(*p, "ABC", second) for p in parts)

        valid = [say(("s", v, a), ("s", a, b), ("s", v, b)),              # ด.ด.ด.
                 say(("s", v, a), ("a", v, v), ("s", v, b)),              # ด.ม.ด.
                 say(("a", v, v), ("s", v, a), ("a", a, a)),              # ม.ด.ม.
                 say(("a", v, v), ("a", a, a), ("s", a, b))]              # ม.ม.ด.
        invalid = [say(("a", 0, 0), ("a", 1, 1), ("a", 2, 2)),            # ม.ม.ม.
                   say(("s", v, a), ("s", a, b), ("a", v, v)),            # ด.ด.ม., the angle not between
                   say(("s", v, a), ("a", v, v))]                         # only two parts
        rng.shuffle(valid)
        rng.shuffle(invalid)
        if rng.random() < 0.5:
            stem = f"ข้อมูลในข้อใดไม่เพียงพอที่จะสรุปว่า △ABC ≅ △{second}"
            return stem, invalid[0], valid[:3]
        stem = f"ข้อมูลในข้อใดเพียงพอที่จะสรุปว่า △ABC ≅ △{second}"
        return stem, valid[0], invalid


def _x_expr(m: int, c: int) -> str:
    """mx + c as sentence text: 2x + 3, 5x − 9, x."""
    return ("x" if m == 1 else f"{m}x") + (f" + {c}" if c > 0 else f" − {-c}" if c < 0 else "")


def _two_in_x(rng: Random, x: int, lo: int, hi: int) -> tuple[int, int, int, int]:
    """Two expressions m1x + c1 and m2x + c2, m1 ≠ m2, both equal to a value from lo to hi at x."""
    while True:
        m1, m2 = rng.sample(range(1, 6), 2)
        value = rng.randint(lo, hi)
        c1, c2 = value - m1 * x, value - m2 * x
        if c1 and c2 and abs(c1) <= 60 and abs(c2) <= 60:
            return m1, c1, m2, c2


@question_type("math.congruence_sides_algebra_m2", display_name={"th": "ด้านที่สมนัยกันเขียนในรูปตัวแปร"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceSidesAlgebraM2(WordProblem):
    """Corresponding sides are equal, so their expressions in x can be set equal and solved."""

    def expr(self, rng: Random):
        first, second = _named(rng)
        i, j = sorted(rng.sample(range(3), 2))
        x = rng.randint(2, 9)
        m1, c1, m2, c2 = _two_in_x(rng, x, 8, 40)
        side = m1 * x + c1
        lead = (f"△{first} ≅ △{second} ถ้า {first[i]}{first[j]} = {_x_expr(m1, c1)} เซนติเมตร "
                f"และ {second[i]}{second[j]} = {_x_expr(m2, c2)} เซนติเมตร ")
        if rng.random() < 0.5:
            # The constants added instead of subtracted; the side's length offered as x.
            slips = [(c1 + c2) // abs(m1 - m2) if (c1 + c2) % abs(m1 - m2) == 0 else 0, side, x + 1, x - 1, x + 2]
            return MathDraw("", str(x), prompt=lead + "แล้ว x มีค่าเท่าใด",
                            distractors=_story.keep(*slips, answer=x, lo=1))
        # x itself; the x-terms alone; the other expression with x read as 1 more.
        slips = [x, m1 * x, m2 * (x + 1) + c2, side + m1, side - m1]
        return MathDraw("", str(side), prompt=lead + f"แล้ว {first[i]}{first[j]} ยาวกี่เซนติเมตร",
                        distractors=_story.keep(*slips, answer=side, lo=1))


@question_type("math.congruence_angles_algebra_m2", display_name={"th": "มุมที่สมนัยกันเขียนในรูปตัวแปร"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceAnglesAlgebraM2(WordProblem):
    """Corresponding angles are equal; with the other two angles known, the third follows from 180°."""

    def expr(self, rng: Random):
        first, second = _named(rng)
        i = rng.randrange(3)
        x = rng.randint(5, 25)
        m1, c1, m2, c2 = _two_in_x(rng, x, 30, 110)
        angle = m1 * x + c1
        pair = f"∠{first[i]} = ({_x_expr(m1, c1)})°", f"∠{second[i]} = ({_x_expr(m2, c2)})°"
        lead = f"△{first} ≅ △{second} ถ้า {pair[0]} และ {pair[1]} "
        if rng.random() < 0.5:
            slips = [(c1 + c2) // abs(m1 - m2) if (c1 + c2) % abs(m1 - m2) == 0 else 0, angle, x + 1, x - 1, x + 5]
            return MathDraw("", str(x), prompt=lead + "แล้ว x มีค่าเท่าใด",
                            distractors=_story.keep(*slips, answer=x, lo=1))
        # One more angle given; find the third, which needs the corresponding angle first.
        j = (i + rng.choice((1, 2))) % 3
        k = 3 - i - j
        other = rng.randint(20, 160 - angle - 10)
        third = 180 - angle - other
        prompt = f"△{first} ≅ △{second} ถ้า {pair[0]}, {pair[1]} และ ∠{first[j]} = {other}° แล้ว ∠{second[k]} มีขนาดกี่องศา"
        # The x-angle itself; 180° less the given one; the sum of the two.
        return MathDraw("", str(third), prompt=prompt,
                        distractors=_story.keep(angle, 180 - other, angle + other, x, answer=third, lo=1, hi=179))


_PROOF_REASONS = (
    "กำหนดให้",
    "เป็นด้านร่วม",
    "ถ้าเส้นตรงสองเส้นตัดกัน แล้วมุมตรงข้ามมีขนาดเท่ากัน",
    "ถ้าเส้นตรงสองเส้นขนานกันและมีเส้นตัด แล้วมุมแย้งมีขนาดเท่ากัน",
    "ด้านคู่ที่สมนัยกันของรูปสามเหลี่ยมที่เท่ากันทุกประการยาวเท่ากัน",
    "มุมคู่ที่สมนัยกันของรูปสามเหลี่ยมที่เท่ากันทุกประการมีขนาดเท่ากัน",
    "มุมฉากทุกมุมมีขนาดเท่ากัน",
)


def _proof(stem: str, right: int, *wrong: int) -> Concept:
    return Concept(stem, _PROOF_REASONS[right], tuple(_PROOF_REASONS[w] for w in wrong))


@question_type("math.congruence_proof_reason_m2", display_name={"th": "เหตุผลในการพิสูจน์ความเท่ากันทุกประการ"},
               level={"th": "ม.2"}, topic=_TOPIC)
class CongruenceProofReasonM2(ConceptBankType):
    """The reason a proof step cites, as the สสวท. book sets out a proof in two columns."""

    ITEMS = [
        _proof("รูปสามเหลี่ยม ABD และ ACD มีด้าน AD ร่วมกัน ในการพิสูจน์ ข้อความ AD = AD มีเหตุผลว่าอย่างไร",
               1, 0, 4, 2),
        _proof("AC และ BD ตัดกันที่จุด O ในการพิสูจน์ว่า △AOB ≅ △COD ข้อความ ∠AOB = ∠COD มีเหตุผลว่าอย่างไร",
               2, 3, 5, 0),
        _proof("AB ขนานกับ CD และมี BC เป็นเส้นตัด ในการพิสูจน์ ข้อความ ∠ABC = ∠DCB มีเหตุผลว่าอย่างไร",
               3, 2, 5, 0),
        _proof("พิสูจน์ได้แล้วว่า △ABC ≅ △DEF ข้อความ AC = DF มีเหตุผลว่าอย่างไร", 4, 5, 0, 1),
        _proof("พิสูจน์ได้แล้วว่า △ABC ≅ △DEF ข้อความ ∠C = ∠F มีเหตุผลว่าอย่างไร", 5, 4, 0, 2),
        _proof("กำหนดให้ M เป็นจุดกึ่งกลางของ BC ในการพิสูจน์ ข้อความ BM = CM มีเหตุผลว่าอย่างไร", 0, 1, 4, 2),
        _proof("AD ตั้งฉากกับ BC ที่จุด D ในการพิสูจน์ว่า △ABD ≅ △ACD ข้อความ ∠ADB = ∠ADC มีเหตุผลว่าอย่างไร",
               6, 2, 5, 3),
    ]


"""Mathematics (คณิตศาสตร์) question types — the platform's home subject.

Consolidated from the former ``types/math/`` subpackage into one module: shared
TeX/fraction/polynomial builders, the :class:`MathType` base, then the level
families in curriculum order (ป.1 → เทคนิคคิดเลขเร็ว). Importing the module
self-registers every type via ``@question_type``; registration order is the
section order below, which the catalog uses to break ties within a level.

Ported from hw_generator/generators/. All algebra is string-built from chosen
integer roots/solutions — no CAS. Vertical column/long-division layouts render
inline here (a KaTeX concern); the stacked figure is deferred to the PDF stage.
"""

from __future__ import annotations

import math
from abc import abstractmethod
from dataclasses import dataclass, field
from fractions import Fraction
from random import Random

from otk.core.content import image as content_image
from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import (
    combine,
    fixed,
    label_pool,
    numeric_neighbors,
    rank_balanced,
    sibling_answers,
)
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType
from otk.kit import story as _story

# ── Shared TeX builders (fractions, polynomials, roots) ──────────────────────

# ── Fractions ────────────────────────────────────────────────────────────────

def frac_tex(fr: Fraction) -> str:
    """TeX for a fraction: plain integer when whole, sign in front otherwise."""
    if fr.denominator == 1:
        return str(fr.numerator)
    sign = "-" if fr < 0 else ""
    return rf"{sign}\frac{{{abs(fr.numerator)}}}{{{fr.denominator}}}"


def frac_answer_tex(fr: Fraction) -> str:
    """Reduced fraction; improper values also get their mixed-number form."""
    if fr.denominator != 1 and abs(fr.numerator) > fr.denominator:
        whole, rem = divmod(abs(fr.numerator), fr.denominator)
        sign = "-" if fr < 0 else ""
        return rf"{frac_tex(fr)} = {sign}{whole}\frac{{{rem}}}{{{fr.denominator}}}"
    return frac_tex(fr)


def proper(rng: Random, q: int) -> Fraction:
    """Random fully-reduced proper fraction with denominator q."""
    p = rng.choice([n for n in range(1, q) if math.gcd(n, q) == 1])
    return Fraction(p, q)


def rand_proper(rng: Random, den_lo: int = 2, den_hi: int = 12) -> Fraction:
    return proper(rng, rng.randint(den_lo, den_hi))


# ── Polynomials (string-built from chosen integer roots — no CAS) ────────────

def coef_term(c: int, sym: str, first: bool = False) -> str:
    """One signed polynomial term: 3x^2, -x, + 5 … ; '' when c == 0."""
    if c == 0:
        return ""
    mag = "" if abs(c) == 1 and sym else str(abs(c))
    body = f"{mag}{sym}"
    if first:
        return f"-{body}" if c < 0 else body
    return f" - {body}" if c < 0 else f" + {body}"


def poly_tex(*terms: tuple[int, str]) -> str:
    """Join (coefficient, symbol) pairs into a polynomial string; '0' if empty."""
    out = ""
    for c, sym in terms:
        out += coef_term(c, sym, first=not out)
    return out or "0"


def binomial_tex(r: int, sym: str = "x") -> str:
    """(x + r) with the sign folded in; (x) never occurs because r != 0."""
    return rf"({sym} {'+' if r >= 0 else '-'} {abs(r)})"


def mono_tex(c: int, px: int, py: int) -> str:
    """Monomial like -6x^3y^4; coefficient 1/-1 drops the digit."""
    parts = ""
    if abs(c) != 1 or (px == 0 and py == 0):
        parts += str(abs(c))
    if px:
        parts += "x" if px == 1 else f"x^{{{px}}}"
    if py:
        parts += "y" if py == 1 else f"y^{{{py}}}"
    return ("-" if c < 0 else "") + parts


def sqrt_tex(n: int) -> str:
    """sqrt(n) with square factors pulled out: sqrt(50) -> 5 sqrt(2)."""
    out, k = 1, 2
    while k * k <= n:
        while n % (k * k) == 0:
            out *= k
            n //= k * k
        k += 1
    if n == 1:
        return str(out)
    return rf"\sqrt{{{n}}}" if out == 1 else rf"{out}\sqrt{{{n}}}"


# ── Base class for math question types ───────────────────────────────────────

@dataclass
class MathDraw:
    problem_tex: str
    answer_tex: str
    topic: str = ""            # per-item topic (overrides the type default)
    prompt: str = ""           # plain Thai line shown above the expression
    hint: str = ""             # optional solving aid (math)
    # Hand-picked "mistake" distractors (TeX), offered before the sampled ones.
    # Empty → the type falls back to sibling + numeric-neighbour distractors.
    distractors: list[str] = field(default_factory=list)
    # Diagram shown under the stem, as an asset id. Three states: an id shows
    # that diagram, ``""`` leaves the type's own default (see
    # :meth:`MathType.default_figure`) in place, and ``None`` suppresses it —
    # for a draw that asks something the type's usual figure does not depict.
    figure: str | None = ""
    figure_alt: str = ""       # what the diagram shows, for screen readers/print
    # Which story a draw tells, for a type that mixes several. When set, spare
    # choices are borrowed only from sibling draws of the same variant: a 12 cm
    # cube's volume beside "6,000,000", the answer of a cubic-metre conversion,
    # is a wrong choice nobody would pick. Empty: any sibling will do.
    variant: str = ""


def _as_draw(result) -> MathDraw:
    return result if isinstance(result, MathDraw) else MathDraw(*result)


class MathType(QuestionType):
    _param_fn = lambda self: self.expr          # tunable ranges live on expr

    @abstractmethod
    def expr(self, rng: Random, **params):
        """Return (problem_tex, answer_tex) or a MathDraw."""

    def default_figure(self) -> tuple[str, str]:
        """``(asset id, alt text)`` shown by every draw of this type, if any.

        For a type whose diagram is part of the statement rather than of the
        particular numbers — a digested sheet's geometry figure — this beats
        repeating the id in every ``MathDraw``.
        """
        return "", ""

    def _figure_block(self, d: MathDraw):
        asset, alt = ((d.figure, d.figure_alt) if d.figure
                      else ("", "") if d.figure is None
                      else self.default_figure())
        return [content_image(asset, alt=alt)] if asset else []

    # Tries before giving up on a same-variant sibling; numeric neighbours and
    # invented near values then fill the choices instead.
    _VARIANT_TRIES = 12

    def _sibling_sampler(self, rng: Random, params: dict, draw: MathDraw):
        """Answers of other draws, for spare choices: of the same variant as
        ``draw`` when it names one, else of any. Draws without a variant consume
        exactly one ``expr`` call per sample, as they always have."""
        def sample():
            for _ in range(self._VARIANT_TRIES if draw.variant else 1):
                sibling = _as_draw(self.expr(rng, **params))
                if not draw.variant or sibling.variant == draw.variant:
                    return [content_math(sibling.answer_tex)]
            return None
        return sample

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        d = _as_draw(self.expr(rng, **params))
        sample = self._sibling_sampler(rng, params, d)

        stem = (([text(d.prompt)] if d.prompt else [])
                + ([content_math(d.problem_tex)] if d.problem_tex else [])
                + self._figure_block(d))
        strat = combine(sibling_answers(sample), numeric_neighbors())
        if d.distractors:
            strat = combine(
                fixed(*[[content_math(t)] for t in d.distractors]), strat)
        strat = rank_balanced(strat, invent=True)
        return GeneratedQuestion(
            stem=stem,
            correct=[content_math(d.answer_tex)],
            distractors=strat,
            topic=d.topic or self.topic,
            hint=[content_math(d.hint)] if d.hint else [],
        )

class WordProblem(MathType):
    """A Thai โจทย์ปัญหา: the ``prompt`` sentence is the stem, the answer is a
    number, and no bare expression is shown (``problem_tex`` is usually empty).

    Hand-picked ``distractors`` (as TeX strings) come first, then sibling answers
    and numeric neighbours fill any remainder — so a full four choices survives
    even when two of the picked mistakes collide.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        d = _as_draw(self.expr(rng, **params))
        sample = self._sibling_sampler(rng, params, d)

        strat = combine(sibling_answers(sample), numeric_neighbors())
        if d.distractors:
            strat = combine(
                fixed(*[[content_math(t)] for t in d.distractors]), strat)
        strat = rank_balanced(strat, invent=True)
        stem = [text(d.prompt)]
        if d.problem_tex:
            stem.append(content_math(d.problem_tex))
        stem += self._figure_block(d)
        return GeneratedQuestion(
            stem=stem,
            correct=[content_math(d.answer_tex)],
            distractors=strat,
            topic=d.topic or self.topic,
            hint=[content_math(d.hint)] if d.hint else [],
        )


class ChoiceType(QuestionType):
    """Concept MCQ with Thai-word choices, generated per item rather than drawn
    from a fixed bank. ``compose`` returns ``(stem, correct, wrongs)``; the wrong
    labels become the distractor pool (deduped and shuffled by ``label_pool``)."""

    @abstractmethod
    def compose(self, rng: Random):
        """Return (stem_text, correct_label, wrong_labels)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = self.compose(rng)
        return GeneratedQuestion(
            stem=[text(stem)],
            correct=[text(correct)],
            distractors=label_pool(list(wrongs)),
            topic=self.topic,
        )


# ══ Level families (registration order) ══════════════════════════════════════
# ───────────────────────────── ระดับ ป.1 ─────────────────────────────

# จำนวนนับ 1 ถึง 10 และ 0
    # การนับ 1-10
    # การแสดงตัวเลขด้วยกรอบสิบ
    # การเขียนในรูปกระจาย
    # ตัวเลขและตัวหนังสือ
    # การเปรียบเทียบจำนวนนับ
    # การเรียงลำดับ


# การบวก
    # การบวกเลข 1 หลัก
    # การสลับที่การบวก
    # โจทย์ปัญหาการบวก


# การลบ
    # การลบเลข 1 หลัก    
    # การลบโดยใช้เส้นจำนวน
    # การหาค่าของตัวไม่ทราบค่า ในประโยคสัญลักษณ์การบวกและประโยคสัญลักษณ์การลบ 
    # โจทย์ปัญหาการลบ


def _no_carry_sum(a: int, b: int) -> int:
    """a + b with the carry forgotten: 38 + 25 -> 53."""
    return (a // 10 + b // 10) * 10 + (a % 10 + b % 10) % 10


def _add_story(rng: Random, a: int, b: int) -> str:
    """One addition situation from the สสวท. ป.1 range: adding to, putting
    together, and the totals of two days, two groups or two colours."""
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    sc = rng.choice(_story.SCENES)
    shop = rng.choice(_story.STOCK)
    c1, c2 = rng.sample(_story.COLOURS, 2)
    stories = (
        f"{p}มี{t.noun} {a} {t.cl} {rng.choice(_story.GIVERS)}ให้{p}อีก {b} {t.cl} "
        f"ตอนนี้{p}มี{t.noun}ทั้งหมดกี่{t.cl}",
        f"{p}มี{t.noun} {a} {t.cl} {q}มี{t.noun} {b} {t.cl} "
        f"ทั้งสองคนมี{t.noun}รวมกันกี่{t.cl}",
        f"{sc.place}มี{sc.animal} {a} ตัว {sc.animal}{sc.arrive} {b} ตัว "
        f"ตอนนี้{sc.place}มี{sc.animal}ทั้งหมดกี่ตัว",
        f"ห้องเรียนหนึ่งมีนักเรียนชาย {a} คน นักเรียนหญิง {b} คน "
        f"ห้องเรียนนี้มีนักเรียนทั้งหมดกี่คน",
        f"{p}อ่านหนังสือวันแรกได้ {a} หน้า วันที่สองอ่านได้ {b} หน้า "
        f"สองวัน{p}อ่านหนังสือได้ทั้งหมดกี่หน้า",
        f"ร้านค้าขาย{shop.noun}ตอนเช้าได้ {a} {shop.cl} ตอนบ่ายขายได้ {b} {shop.cl} "
        f"วันนี้ร้านค้าขาย{shop.noun}ได้ทั้งหมดกี่{shop.cl}",
        f"{p}มีเงิน {a} บาท {rng.choice(_story.GIVERS)}ให้เงินเพิ่มอีก {b} บาท "
        f"{p}มีเงินทั้งหมดกี่บาท",
        f"ในกล่องมีลูกบอล{c1} {a} ลูก และลูกบอล{c2} {b} ลูก "
        f"ในกล่องมีลูกบอลทั้งหมดกี่ลูก",
        f"{p}เก็บ{t.noun}ได้ {a} {t.cl} {q}เก็บได้ {b} {t.cl} "
        f"นำมารวมกันได้กี่{t.cl}",
        f"บนรถโดยสารมีผู้โดยสาร {a} คน ถึงป้ายรถมีคนขึ้นมาอีก {b} คน "
        f"ตอนนี้บนรถมีผู้โดยสารกี่คน",
    )
    return rng.choice(stories)


def _sub_story(rng: Random, a: int, b: int) -> str:
    """One subtraction situation: taking away, eating or selling, a part of a
    whole, and money left after buying."""
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    food, used = rng.choice(_story.CONSUMABLES)
    sc = rng.choice(_story.SCENES)
    shop = rng.choice(_story.STOCK)
    c1, c2 = rng.sample(_story.COLOURS, 2)
    stories = (
        f"{p}มี{t.noun} {a} {t.cl} แบ่งให้{q} {b} {t.cl} "
        f"{p}เหลือ{t.noun}กี่{t.cl}",
        f"{p}มี{food.noun} {a} {food.cl} {used} {b} {food.cl} "
        f"เหลือ{food.noun}กี่{food.cl}",
        f"{sc.place}มี{sc.animal} {a} ตัว {sc.leave} {b} ตัว "
        f"{sc.place}เหลือ{sc.animal}กี่ตัว",
        f"ในกล่องมีลูกบอล{c1}และลูกบอล{c2}รวมกัน {a} ลูก เป็นลูกบอล{c1} {b} ลูก "
        f"เป็นลูกบอล{c2}กี่ลูก",
        f"{p}มีเงิน {a} บาท ซื้อ{rng.choice(_story.SNACKS)}ไป {b} บาท "
        f"{p}เหลือเงินกี่บาท",
        f"หนังสือเล่มหนึ่งมี {a} หน้า {p}อ่านไปแล้ว {b} หน้า "
        f"เหลืออีกกี่หน้าจึงจะอ่านจบเล่ม",
        f"แม่ค้ามี{shop.noun} {a} {shop.cl} ขายไป {b} {shop.cl} "
        f"แม่ค้าเหลือ{shop.noun}กี่{shop.cl}",
        f"บนรถโดยสารมีผู้โดยสาร {a} คน ถึงป้ายรถมีคนลงไป {b} คน "
        f"บนรถเหลือผู้โดยสารกี่คน",
        f"ห้องเรียนหนึ่งมีนักเรียน {a} คน วันนี้ขาดเรียน {b} คน "
        f"วันนี้มีนักเรียนมาเรียนกี่คน",
        f"{p}เป่าลูกโป่งได้ {a} ลูก ลูกโป่งแตกไป {b} ลูก "
        f"{p}เหลือลูกโป่งกี่ลูก",
    )
    return rng.choice(stories)


# ── ระดับ B (บวก/ลบแนวตั้ง) — ป.2 ──────────────────────────────────


# ── ระดับ C (สูตรคูณและการหาร) — ป.3 ───────────────────────────────


# ── ระดับ D (คูณ/หารหลายหลัก) — ป.4 ────────────────────────────────


# ── ระดับ E (เศษส่วน) — ป.5 ────────────────────────────────────────


# ── ระดับ F (ทศนิยมและลำดับการดำเนินการ) — ป.6 ────────────────────


# ── ระดับ G (จำนวนเต็มและสมการเชิงเส้น) — ม.1 ─────────────────────
# รูปสี่เหลี่ยม
# เศษส่วนและทศนิยม
# เลขยกกำลัง
# จำนวนเต็ม จำนวนเฉพาะ จำนวนประกอบ
# คู่อันดับและกราฟ
# ลำดับ


# ── ระดับ H (ระบบสมการ อสมการ ฟังก์ชันเชิงเส้น) — ม.2 ─────────────


# ── ระดับ J (พีชคณิตขั้นสูง) — ม.4 ─────────────────────────────────


# ── ระดับ K (ฟังก์ชันกำลังสองและเลขชี้กำลัง) — ม.4 ────────────────


# ── ระดับ L (ลอการิทึมและแคลคูลัสเบื้องต้น) — ม.5 ─────────────────


# ── ระดับ M (เรขาคณิตวิเคราะห์และตรีโกณมิติ) — ม.5 ────────────────


# ── ระดับ N (ลำดับ อนุกรม ลิมิต อนุพันธ์) ──────────────────────────


# ── ระดับ O (อินทิเกรตและพื้นที่) ──────────────────────────────────


# ── วิชาเสริม XP (ความน่าจะเป็น) ───────────────────────────────────


# ── วิชาเสริม XV (เวกเตอร์) ────────────────────────────────────────


# ── Arithmetic / quick math ──────────────────────────────────────────────────


# ── Fractions, ratios, percentages ───────────────────────────────────────────


# ── Number theory ────────────────────────────────────────────────────────────


# ── Exponent rules ───────────────────────────────────────────────────────────


# ── Hard mode (multi-rule) ───────────────────────────────────────────────────


# ── Geometry ─────────────────────────────────────────────────────────────────


# ══ Primary curriculum ป.1–ป.6 (spec: sheet_database/specs/math_questions.md) ════════
#
# Two extra bases carry the shapes the curriculum needs that a bare expression
# cannot: WordProblem (a Thai narrative whose answer is a number — the sentence
# is the whole stem) and ChoiceType (Thai-word choices generated per item). Thai
# never lands in a MathBlock: narratives live in the stem's TextBlock, word
# answers in TextBlock choices; only notation/numbers use content_math.


# ── ป.1 ───────────────────────────────────────────────────────────────────────


# ── ป.2 ───────────────────────────────────────────────────────────────────────


# ── ป.3 ───────────────────────────────────────────────────────────────────────


# ── ป.4 ───────────────────────────────────────────────────────────────────────


# ── ป.5 ───────────────────────────────────────────────────────────────────────


# ── ป.6 ───────────────────────────────────────────────────────────────────────


# ══ Lower secondary ม.1–ม.3 (spec gaps beyond the computational core above) ════
# The algebra/exponent/factoring core already lives in ระดับ G–I above; this fills
# the curriculum's concept, word-problem, geometry-solid and statistics items.

# ── ม.1 ───────────────────────────────────────────────────────────────────────


# ── ม.2 ───────────────────────────────────────────────────────────────────────


# ── เอกนามและพหุนาม — one ladder, registered in teaching order ────────────
# จำแนกเอกนาม/พหุนาม → สัมประสิทธิ์และดีกรี →
# บวก/ลบเอกนาม → เครื่องหมายลบหน้าวงเล็บ → รวมพจน์ → บวก/ลบพหุนาม →
# คูณเอกนาม → คูณเอกนามกับพหุนาม → หารเอกนาม → หารพหุนามด้วยเอกนาม →
# กระจายแล้วจัดรูป. The progression layer stages a topic's sets by
# registration order, so this order *is* the learning curve.


# ── ระดับ I (พหุนามและสมการกำลังสอง) — ม.3 ────────────────────────


# ── ม.3 ───────────────────────────────────────────────────────────────────────


# ══ Upper secondary ม.4–ม.6 (spec gaps beyond the computational core) ══════════


# ── ม.4 ───────────────────────────────────────────────────────────────────────


# ── ม.5 ───────────────────────────────────────────────────────────────────────


# ── ม.6 ───────────────────────────────────────────────────────────────────────


# ══ University Calculus 1 (แคลคูลัส 1) ═════════════════════════════════════════
# Mostly formula-recall / concept items: MathType carries the notation choices,
# ChoiceType/ConceptBankType the Thai-worded conclusions.

# ── Limits & Continuity ───────────────────────────────────────────────────────


# ── Derivatives ───────────────────────────────────────────────────────────────


# ── Applications of derivatives ───────────────────────────────────────────────


# ── Integration ───────────────────────────────────────────────────────────────


# ══ University Calculus 2 (แคลคูลัส 2) ═════════════════════════════════════════

# ── Advanced integration ──────────────────────────────────────────────────────


# ── Applications of integration ───────────────────────────────────────────────


# ── Differential equations ────────────────────────────────────────────────────


# ── Parametric & polar ────────────────────────────────────────────────────────


# ── Series ────────────────────────────────────────────────────────────────────



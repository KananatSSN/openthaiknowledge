"""โจทย์ปัญหา

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/5

Sets moved here from: math, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, _add_story, _no_carry_sum, _sub_story
from otk.sets._support.math_p1 import LEVEL

PROVENANCE = Provenance("original")


def _no_borrow_diff(a: int, b: int) -> int:
    """a - b taking the smaller digit from the larger in each place: 52 - 17 -> 45."""
    return abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)


def _compare_story(rng: Random, hi: int):
    """A comparison: how many more or fewer, or the other quantity from one.

    Returns ``(prompt, answer, the opposite-operation mistake)``.
    """
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    big = rng.randint(6, hi)
    small = rng.randint(1, big - 1)
    gap = big - small
    kind = rng.randrange(8)
    if kind == 0:
        return (f"{p}มี{t.noun} {big} {t.cl} {q}มี{t.noun} {small} {t.cl} "
                f"{p}มี{t.noun}มากกว่า{q}กี่{t.cl}", gap, big + small)
    if kind == 1:
        return (f"{p}มี{t.noun} {big} {t.cl} {q}มี{t.noun} {small} {t.cl} "
                f"{q}มี{t.noun}น้อยกว่า{p}กี่{t.cl}", gap, big + small)
    if kind == 2:
        return (f"{p}มี{t.noun} {small} {t.cl} {q}มี{t.noun}มากกว่า{p} {gap} {t.cl} "
                f"{q}มี{t.noun}กี่{t.cl}", big, abs(small - gap))
    if kind == 3:
        return (f"{p}มี{t.noun} {big} {t.cl} {q}มี{t.noun}น้อยกว่า{p} {gap} {t.cl} "
                f"{q}มี{t.noun}กี่{t.cl}", small, big + gap)
    if kind == 4:
        # "ซึ่งมากกว่า" names the *other* person's amount: the classic trap is
        # to add because the sentence says มากกว่า.
        return (f"{p}มี{t.noun} {big} {t.cl} ซึ่งมากกว่า{q} {gap} {t.cl} "
                f"{q}มี{t.noun}กี่{t.cl}", small, big + gap)
    if kind == 5:
        return (f"{p}มี{t.noun} {small} {t.cl} ซึ่งน้อยกว่า{q} {gap} {t.cl} "
                f"{q}มี{t.noun}กี่{t.cl}", big, abs(small - gap))
    if kind == 6:
        c1, c2 = rng.sample(_story.COLOURS, 2)
        return (f"ริบบิ้น{c1}ยาว {big} เซนติเมตร ริบบิ้น{c2}ยาว {small} เซนติเมตร "
                f"ริบบิ้น{c1}ยาวกว่าริบบิ้น{c2}กี่เซนติเมตร", gap, big + small)
    return (f"ห้องเรียนหนึ่งมีนักเรียนหญิง {big} คน นักเรียนชาย {small} คน "
            f"นักเรียนหญิงมากกว่านักเรียนชายกี่คน", gap, big + small)


def _missing_part_story(rng: Random, hi: int):
    """The start or the change is unknown. Returns ``(prompt, answer, sentence,
    opposite-operation mistake)`` where ``sentence`` is the number sentence the
    story describes, with ``\\square`` for the unknown."""
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    total = rng.randint(8, hi)
    part = rng.randint(2, total - 2)
    rest = total - part
    sq = r"\square"
    kind = rng.randrange(6)
    if kind == 0:     # start unknown, then gave some away
        return (f"{p}แบ่ง{t.noun}ให้{q}ไป {part} {t.cl} {p}ยังเหลือ{t.noun}อีก {rest} {t.cl} "
                f"เดิม{p}มี{t.noun}กี่{t.cl}", total, rf"{sq} - {part} = {rest}",
                abs(part - rest))
    if kind == 1:     # start unknown, then received some
        return (f"{rng.choice(_story.GIVERS)}ให้{t.noun}แก่{p}อีก {part} {t.cl} "
                f"ทำให้ตอนนี้{p}มี{t.noun} {total} {t.cl} เดิม{p}มี{t.noun}กี่{t.cl}",
                rest, rf"{sq} + {part} = {total}", total + part)
    if kind == 2:     # change unknown, received
        return (f"{p}มี{t.noun} {rest} {t.cl} ได้มาเพิ่มอีกจำนวนหนึ่ง "
                f"ตอนนี้มี{t.noun} {total} {t.cl} {p}ได้{t.noun}มาเพิ่มกี่{t.cl}",
                part, rf"{rest} + {sq} = {total}", total + rest)
    if kind == 3:     # change unknown, gave away
        return (f"{p}มี{t.noun} {total} {t.cl} แบ่งให้{q}ไปจำนวนหนึ่ง "
                f"เหลือ{t.noun} {rest} {t.cl} {p}แบ่งให้{q}ไปกี่{t.cl}",
                part, rf"{total} - {sq} = {rest}", total + rest)
    if kind == 4:     # how many more are needed
        return (f"{p}อยากสะสมสติกเกอร์ให้ครบ {total} แผ่น ตอนนี้มีอยู่ {rest} แผ่น "
                f"{p}ต้องสะสมสติกเกอร์เพิ่มอีกกี่แผ่น",
                part, rf"{rest} + {sq} = {total}", total + rest)
    toy = rng.choice(_story.TOYS)
    return (f"{toy}ราคา {total} บาท {p}มีเงินอยู่ {rest} บาท "
            f"{p}ต้องเก็บเงินเพิ่มอีกกี่บาทจึงจะซื้อ{toy}ได้",
            part, rf"{rest} + {sq} = {total}", total + rest)


# The six ways a ป.1 sentence can place two numbers and a box. Each entry
# solves for the box, or returns None when no whole number fits.
_SENTENCE_FORMS = {
    "{a} + {b} = \\square": lambda a, b: a + b,
    "{a} - {b} = \\square": lambda a, b: a - b if a >= b else None,
    "{a} + \\square = {b}": lambda a, b: b - a if b >= a else None,
    "{a} - \\square = {b}": lambda a, b: a - b if a >= b else None,
    "\\square + {a} = {b}": lambda a, b: b - a if b >= a else None,
    "\\square - {a} = {b}": lambda a, b: a + b,
}


def _sentence_distractors(rng: Random, x: int, y: int, answer: int) -> list[str]:
    """Sentences over the story's own two numbers whose box is not the answer.

    An equivalent sentence (□ − 5 = 7 for 5 + 7 = □) solves to the same number
    and is never offered: it would be a second right answer.
    """
    out = []
    for form, solve in _SENTENCE_FORMS.items():
        for a, b in ((x, y), (y, x)):
            value = solve(a, b)
            if value is not None and value != answer:
                out.append(form.format(a=a, b=b))
    rng.shuffle(out)
    return list(dict.fromkeys(out))


@question_type("math.add_word_problem",
               display_name={"th": "โจทย์ปัญหาการบวก"}, level={"th": "ป.1"},
               topic="โจทย์ปัญหา")
class AddWordProblem(WordProblem):
    def expr(self, rng: Random, hi: int = 50):
        a, b = rng.randint(1, hi), rng.randint(1, hi)
        total = a + b
        return MathDraw(
            "", rf"{total}",
            prompt=_add_story(rng, a, b),
            # Subtracting instead of adding, then the forgotten carry.
            distractors=_story.keep(abs(a - b), _no_carry_sum(a, b), total + 10,
                                    total + 1, answer=total, lo=1))


@question_type("math.sub_word_problem",
               display_name={"th": "โจทย์ปัญหาการลบ"}, level={"th": "ป.1"},
               topic="โจทย์ปัญหา")
class SubWordProblem(WordProblem):
    def expr(self, rng: Random, lo: int = 5, hi: int = 100):
        a = rng.randint(lo, hi)
        b = rng.randint(1, a - 1) if a > 1 else 1
        diff = a - b
        return MathDraw(
            "", rf"{diff}",
            prompt=_sub_story(rng, a, b),
            # Adding instead of subtracting, then the smaller-from-larger slip.
            distractors=_story.keep(a + b, _no_borrow_diff(a, b), diff + 1,
                                    diff - 1, answer=diff))


@question_type("math.compare_word_problem",
               display_name={"th": "โจทย์ปัญหาการเปรียบเทียบ (มากกว่า/น้อยกว่า)"},
               level=LEVEL, topic="โจทย์ปัญหา")
class CompareWordProblem(WordProblem):
    def expr(self, rng: Random, hi: int = 60):
        prompt, answer, flipped = _compare_story(rng, max(7, min(int(hi), 99)))
        return MathDraw("", str(answer), prompt=prompt,
                        distractors=_story.keep(flipped, answer + 1, answer - 1,
                                                answer + 10, answer=answer, lo=1))


@question_type("math.word_problem_number_sentence",
               display_name={"th": "เขียนประโยคสัญลักษณ์จากโจทย์ปัญหา"},
               level=LEVEL, topic="โจทย์ปัญหา")
class WordProblemNumberSentence(QuestionType):
    """Pick the ประโยคสัญลักษณ์ a story describes — the step the books ask for
    before any arithmetic."""

    def build(self, rng: Random, hi: int = 50) -> GeneratedQuestion:
        hi = max(10, min(int(hi), 99))
        kind = rng.randrange(3)
        if kind == 0:
            x, y = rng.randint(1, hi), rng.randint(1, hi)
            prompt, sentence, answer = _add_story(rng, x, y), rf"{x} + {y} = \square", x + y
        elif kind == 1:
            x = rng.randint(5, hi)
            y = rng.randint(1, x - 1)
            prompt, sentence, answer = _sub_story(rng, x, y), rf"{x} - {y} = \square", x - y
        else:
            prompt, answer, sentence, _ = _missing_part_story(rng, hi)
            nums = [int(n) for n in sentence.replace("\\square", "").split()
                    if n.isdigit()]
            x, y = nums
        wrongs = [w for w in _sentence_distractors(rng, x, y, answer) if w != sentence]
        return GeneratedQuestion(
            stem=[text(prompt), text("ประโยคสัญลักษณ์ใดตรงกับโจทย์นี้")],
            correct=[content_math(sentence)],
            distractors=fixed(*[[content_math(w)] for w in wrongs]),
            topic=self.topic,
        )


@question_type("math.missing_part_word_problem",
               display_name={"th": "โจทย์ปัญหา: หาจำนวนเดิมหรือจำนวนที่เปลี่ยนไป"},
               level=LEVEL, topic="โจทย์ปัญหา")
class MissingPartWordProblem(WordProblem):
    def expr(self, rng: Random, hi: int = 99):
        prompt, answer, _, flipped = _missing_part_story(rng, max(10, min(int(hi), 100)))
        return MathDraw("", str(answer), prompt=prompt,
                        distractors=_story.keep(flipped, answer + 1, answer - 1,
                                                answer + 10, answer=answer, lo=1))


# ── More word problems (2026-11): money left, how many more are needed, ages, bundles of ten, and a place
# in a line ──


@question_type("math.money_left_p1", display_name={"th": "โจทย์ปัญหาเงินที่เหลือ"},
               level=LEVEL, topic="โจทย์ปัญหา")
class MoneyLeftP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        have = rng.choice((20, 50, 100))
        cost = rng.randint(5, have - 3)
        right = have - cost
        snack = rng.choice(_story.SNACKS)
        prompt = f"{p}มีเงิน {have} บาท ซื้อ{snack}ราคา {cost} บาท {p}เหลือเงินกี่บาท"
        # Added instead; the digits taken smaller from larger; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(have + cost, _no_borrow_diff(have, cost), right + 1, right - 1,
                                                answer=right, lo=1))


@question_type("math.more_needed_p1", display_name={"th": "โจทย์ปัญหาต้องหามาเพิ่มอีกเท่าใด"},
               level=LEVEL, topic="โจทย์ปัญหา")
class MoreNeededP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        t = rng.choice(_story.THINGS)
        want = rng.randint(12, 60)
        have = rng.randint(3, want - 2)
        right = want - have
        prompt = (f"{p}ต้องการ{t.noun} {want} {t.cl} ตอนนี้มีอยู่ {have} {t.cl} "
                  f"{p}ต้องหามาเพิ่มอีกกี่{t.cl}")
        # Added instead; what is already there; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(want + have, have, right + 1, right - 1, answer=right, lo=1))


@question_type("math.age_word_p1", display_name={"th": "โจทย์ปัญหาเรื่องอายุ"},
               level=LEVEL, topic="โจทย์ปัญหา")
class AgeWordP1(WordProblem):
    def expr(self, rng: Random):
        p, q = _story.names(rng)
        age = rng.randint(5, 9)
        gap = rng.randint(2, 6)
        kind = rng.randrange(3)
        if kind == 0:
            right = age + gap
            prompt = f"ปีนี้{p}อายุ {age} ปี อีก {gap} ปี {p}จะอายุกี่ปี"
            wrong = age - gap
        elif kind == 1:
            right = age + gap
            prompt = f"{p}อายุ {age} ปี {q}อายุมากกว่า{p} {gap} ปี {q}อายุกี่ปี"
            wrong = age - gap
        else:
            right = age - gap if age > gap else age + gap
            if age > gap:
                prompt = f"{p}อายุ {age} ปี {q}อายุน้อยกว่า{p} {gap} ปี {q}อายุกี่ปี"
                wrong = age + gap
            else:
                prompt = f"{p}อายุ {age} ปี {q}อายุมากกว่า{p} {gap} ปี {q}อายุกี่ปี"
                wrong = age - gap
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(wrong, age, gap, right + 1, answer=right, lo=1))


@question_type("math.tens_bundles_word_p1", display_name={"th": "โจทย์ปัญหากล่องละสิบ"},
               level=LEVEL, topic="โจทย์ปัญหา")
class TensBundlesWordP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        thing, box, cl = rng.choice((("ดินสอ", "กล่อง", "แท่ง"), ("ไข่ไก่", "แผง", "ฟอง"),
                                     ("ลูกอม", "ถุง", "เม็ด"), ("สีเทียน", "กล่อง", "แท่ง")))
        tens = rng.randint(2, 9)
        ones = rng.randint(1, 9)
        right = 10 * tens + ones
        prompt = (f"{p}มี{thing} {tens} {box} {box}ละ 10 {cl} และมีอีก {ones} {cl} "
                  f"{p}มี{thing}ทั้งหมดกี่{cl}")
        # The counts added as they stand; tens and ones swapped; the boxes only.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(tens + ones, 10 * ones + tens, 10 * tens, tens + 10 + ones,
                                                answer=right, lo=1))


@question_type("math.line_position_p1", display_name={"th": "โจทย์ปัญหาลำดับที่ในแถว"},
               level=LEVEL, topic="โจทย์ปัญหา")
class LinePositionP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        place = rng.randint(2, 9)
        behind = rng.randint(2, 9)
        right = place + behind
        prompt = (f"นักเรียนเข้าแถวตอนเรียงหนึ่ง {p}อยู่ลำดับที่ {place} นับจากหัวแถว "
                  f"ข้างหลัง{p}มีนักเรียนอีก {behind} คน แถวนี้มีนักเรียนทั้งหมดกี่คน")
        # Forgetting the child counted; counting them twice; only those behind.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right - 1, right + 1, behind, place, answer=right, lo=1))

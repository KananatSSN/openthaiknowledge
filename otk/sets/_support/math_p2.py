"""ป.2 sets that the สสวท. books teach and the catalog did not have.

The grade had no การหาร at all (ค 1.1 ป.2/6), no แบบรูป (ค 1.2 ป.2/1), no
บวก ลบ คูณ หารระคน, no hours-and-minutes, and one sentence per word problem.
This module adds them in book order. Numbers stay within the grade's 0–1,000,
products and dividends within what ป.2 multiplies and divides (one digit by at
most two digits; a one-digit quotient).
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType
from otk.kit import story as _story

LEVEL = {"th": "ป.2"}


def _texts(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Thai-text choices, the wrongs offered in the order given."""
    return GeneratedQuestion(stem=stem, correct=[text(correct)],
                             distractors=fixed(*[[text(w)] for w in wrongs]),
                             topic=topic)


def _maths(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """TeX choices, the wrongs offered in the order given."""
    return GeneratedQuestion(stem=stem, correct=[content_math(correct)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]),
                             topic=topic)


# ── การนับ ค่าประจำหลัก การเปรียบเทียบ (ค 1.1 ป.2/1–4) ────────────────────────

def _near_numbers(n: int, hi: int) -> list[int]:
    """Numbers a learner confuses with n: two digits swapped, one place off,
    and the zero dropped (305 read as 35)."""
    s = str(n)
    out = []
    for i in range(len(s) - 1):
        swapped = s[:i] + s[i + 1] + s[i] + s[i + 2:]
        if swapped[0] != "0":
            out.append(int(swapped))
    if "0" in s[1:]:
        out.append(int(s.replace("0", "")))
    for place in (10 ** k for k in range(len(s) - 1, -1, -1)):
        out += [n + place, n - place]
    return [m for m in dict.fromkeys(out) if 0 <= m <= hi and m != n]


def _misreadings(n: int) -> list[str]:
    """Readings a learner writes: หนึ่ง for เอ็ด, สองสิบ for ยี่สิบ."""
    right = _story.thai_words(n)
    out = []
    if right.endswith("เอ็ด"):
        out.append(right.removesuffix("เอ็ด") + "หนึ่ง")
    if "ยี่สิบ" in right:
        out.append(right.replace("ยี่สิบ", "สองสิบ"))
    return out


class NumberReadingType(QuestionType):
    """Read and write a number four ways: word ↔ digits, ตัวเลขไทย ↔ digits."""

    LO, HI = 100, 1000

    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.randint(self.LO, self.HI)
        # Numbers with a zero inside are the ones worth reading.
        if rng.random() < 0.4:
            s = list(str(n))
            s[rng.randrange(1, len(s))] = "0"
            n = int("".join(s))
        near = _near_numbers(n, self.HI)
        kind = rng.randrange(4)
        if kind == 0:
            wrongs = _misreadings(n) + [_story.thai_words(m) for m in near]
            return _texts([text("จำนวนนี้อ่านว่าอย่างไร"), content_math(str(n))],
                          _story.thai_words(n), list(dict.fromkeys(wrongs)), self.topic)
        if kind == 1:
            return _maths([text(f"“{_story.thai_words(n)}” เขียนเป็นตัวเลขฮินดูอารบิกได้อย่างไร")],
                          str(n), [str(m) for m in near], self.topic)
        if kind == 2:
            return _texts([text("เขียนเป็นตัวเลขไทยได้อย่างไร"), content_math(str(n))],
                          _story.thai_numeral(n), [_story.thai_numeral(m) for m in near],
                          self.topic)
        return _maths([text(f"{_story.thai_numeral(n)} เขียนเป็นตัวเลขฮินดูอารบิกได้อย่างไร")],
                      str(n), [str(m) for m in near], self.topic)


# ── การคูณ (ค 1.1 ป.2/5) ────────────────────────────────────────────────────


# (animal, legs) and (vehicle, wheels) for counting-by-groups stories.
_LEGS = (("ไก่", 2), ("เป็ด", 2), ("สุนัข", 4), ("วัว", 4), ("แมงมุม", 8), ("มด", 6),
         ("ผีเสื้อ", 6))


# ── การหาร (ค 1.1 ป.2/6) ─────────────────────────────────────────────────────


# ── บวก ลบ คูณ หารระคน (ค 1.1 ป.2/7) ─────────────────────────────────────────


def evaluate(tex: str) -> float:
    """The value of a sentence side written with + − × ÷ and brackets."""
    # Only ever this module's own authored sentences.
    return eval(tex.replace(r"\times", "*").replace(r"\div", "/"))  # otk: allow eval


# ── โจทย์ปัญหาระคน: บวกลบสองขั้นตอน (ค 1.1 ป.2/8) ─────────────────────────────

def two_step_add_sub_story(rng: Random, hi: int):
    """``(story, answer, the first step alone, both steps the same way)``."""
    p, q = _story.names(rng)
    kind = rng.randrange(5)
    if kind == 0:
        boys, girls = rng.randint(hi // 10, hi // 3), rng.randint(hi // 10, hi // 3)
        gone = rng.randint(10, boys + girls - 10)
        return (f"โรงเรียนแห่งหนึ่งมีนักเรียนชาย {boys} คน นักเรียนหญิง {girls} คน "
                f"ไปทัศนศึกษา {gone} คน อยู่ที่โรงเรียนกี่คน",
                boys + girls - gone, boys + girls, boys + girls + gone)
    if kind == 1:
        shirt, pants = rng.randint(hi // 10, hi // 3), rng.randint(hi // 10, hi // 3)
        note = (shirt + pants) // 500 * 500 + 500
        return (f"{p}ซื้อเสื้อราคา {shirt} บาท และกางเกงราคา {pants} บาท "
                f"จ่ายเงินไป {note} บาท ได้เงินทอนกี่บาท",
                note - shirt - pants, shirt + pants, note - shirt + pants)
    if kind == 2:
        stock = rng.randint(hi // 3, hi - 100)
        sold = rng.randint(20, stock - 10)
        more = rng.randint(20, 100)
        return (f"ร้านหนังสือมีหนังสือ {stock} เล่ม ขายไป {sold} เล่ม "
                f"แล้วสั่งมาเพิ่มอีก {more} เล่ม ร้านมีหนังสือกี่เล่ม",
                stock - sold + more, stock - sold, stock - sold - more)
    if kind == 3:
        a = rng.randint(50, hi // 3)
        b = a + rng.randint(10, 80)
        return (f"{p}เก็บขวดพลาสติกได้ {a} ใบ {q}เก็บได้มากกว่า{p} {b - a} ใบ "
                f"ทั้งสองคนเก็บขวดได้รวมกันกี่ใบ", a + b, b, 2 * a)
    have = rng.randint(hi // 4, hi // 2)
    got = rng.randint(50, hi // 4)
    spent = rng.randint(20, have + got - 10)
    return (f"{p}มีเงิน {have} บาท แม่ให้อีก {got} บาท {p}ซื้อรองเท้าไป {spent} บาท "
            f"{p}เหลือเงินกี่บาท", have + got - spent, have + got, have + got + spent)


# ── แบบรูป (ค 1.2 ป.2/1) ─────────────────────────────────────────────────────


# ── เวลา (ค 2.1 ป.2/1) ───────────────────────────────────────────────────────

def clock(h: int, m: int) -> str:
    """8, 5 -> 8.05 น."""
    return f"{h}.{m:02d} น."


# ── ความยาวและน้ำหนัก (ค 2.1 ป.2/2–5) ────────────────────────────────────────


# ── แผนภูมิรูปภาพ (ค 3.1 ป.2/1) — 1 รูปแทน 2, 5, 10 ─────────────────────────



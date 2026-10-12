"""Secondary sets for indicators the 2560 book lists but no set taught.

From the 2026-09 content audit: factorising degree-2 polynomials at ม.2
(ค 1.2 ม.2/2) and degree-3 ones at ม.3 (ม.3/1); the core track's counting
and probability at ม.4 (ค 3.2 ม.4/1–2), real numbers as radicals and powers
(ค 1.1 ม.5/1), functions describing situations (ค 1.2 ม.5/1) and interest
and the value of money (ค 1.3 ม.5/1) at ม.5; the additional course's
rational equations and inequalities (จำนวนและพีชคณิต ม.4) and the uniform
distribution (สถิติและความน่าจะเป็น ม.6).
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import combine, fixed, label_pool
from otk.core.question import GeneratedQuestion
from otk.kit.math_problems import poly_tex


def _choices(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    return GeneratedQuestion(
        stem=stem, correct=[text(correct)],
        distractors=combine(fixed(*[[text(w)] for w in wrongs]), label_pool(wrongs)),
        topic=topic,
    )


def _lin(a: int, b: int) -> str:
    """ax + b with unit coefficients and signs written the book's way."""
    return poly_tex((a, "x"), (b, ""))


def _quad(a: int, b: int, c: int) -> str:
    return poly_tex((a, "x^{2}"), (b, "x"), (c, ""))


def _nz(rng: Random, lo: int, hi: int) -> int:
    return rng.choice([n for n in range(lo, hi + 1) if n])


def _num(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def _distinct(right: str, *wrongs: str) -> list[str]:
    return [w for w in dict.fromkeys(wrongs) if w != right]


# ── ม.2 การแยกตัวประกอบของพหุนามดีกรีสอง (ค 1.2 ม.2/2) ───────────────────────


# ── ม.3 แยกตัวประกอบพหุนามดีกรีสาม (ค 1.2 ม.3/1) ─────────────────────────────


# ── ม.4 พื้นฐาน หลักการนับเบื้องต้น และความน่าจะเป็น (ค 3.2 ม.4/1–2) ─────────


# ── ม.5 พื้นฐาน จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง (ค 1.1 ม.5/1) ──────────────


# ── ม.5 พื้นฐาน ฟังก์ชันในชีวิตจริง (ค 1.2 ม.5/1) ──────────────────────────────


# ── ม.5 พื้นฐาน ดอกเบี้ยและมูลค่าของเงิน (ค 1.3 ม.5/1) ─────────────────────────


# ── ม.4 เพิ่มเติม สมการและอสมการเศษส่วนของพหุนาม (จำนวนและพีชคณิต ม.4) ──────


# ── ม.6 เพิ่มเติม การแจกแจงเอกรูป (สถิติและความน่าจะเป็น ม.6/1) ───────────────


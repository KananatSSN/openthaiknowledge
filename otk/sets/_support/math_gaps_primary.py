"""Primary sets for indicators the 2560 book lists but no set taught.

Found by the 2026-09 content audit (docs/for_admin/MATH_CONTENT_AUDIT.md):
litres at ป.2 (ค 2.1 ป.2/6); estimating, choosing a measuring tool and tonnes
at ป.3 (ป.3/3–4, 7–12); adding and subtracting large numbers at ป.3 and ป.4
(ค 1.1 ป.3/5, ป.4/8); ordering fractions whose denominators are multiples
(ป.4/4); matching a story to a number sentence (ป.4/12); and length and
weight written as decimals at ป.5 (ค 2.1 ป.5/1–2).
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import combine, fixed, label_pool
from otk.core.question import GeneratedQuestion
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem


def _c(n: int) -> str:
    """12345 -> 12{,}345 in TeX."""
    return f"{int(n):,}".replace(",", "{,}")


def _cs(*values: int, answer: int, lo: int = 1) -> list[str]:
    """Distinct, in-range distractors formatted for TeX, most diagnostic first."""
    return [_c(v) for v in _story.keep(*values, answer=answer, lo=lo)]


def _choices(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """A question whose choices are Thai text, hand-picked wrongs first."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    return GeneratedQuestion(
        stem=stem, correct=[text(correct)],
        distractors=combine(fixed(*[[text(w)] for w in wrongs]), label_pool(wrongs)),
        topic=topic,
    )


# ── ป.2 การวัด: ปริมาตรและความจุเป็นลิตร (ค 2.1 ป.2/6) ──────────────────────


# ── ป.3 การวัด: คาดคะเน เลือกเครื่องมือ และเมตริกตัน ────────────────────────


# ── ป.3 และ ป.4 การบวกและการลบ จำนวนมาก (ค 1.1 ป.3/5, ป.4/8) ────────────────

def _digits(n: int, width: int) -> list[int]:
    return [(n // 10 ** k) % 10 for k in reversed(range(width))]


def _sum_pair(rng: Random, lo: int, hi: int) -> tuple[int, int]:
    """Two addends within ``lo``..``hi``/2 whose sum makes at least one carry."""
    while True:
        a, b = rng.randint(lo, hi // 2), rng.randint(lo, hi // 2)
        width = len(str(a + b))
        if any(x + y >= 10 for x, y in zip(_digits(a, width), _digits(b, width))):
            return a, b


class _AddSubLarge(WordProblem):
    lo, hi = 1_000, 100_000

    def expr(self, rng: Random):
        a, b = _sum_pair(rng, self.lo, self.hi)
        s = a + b
        width = len(str(s))
        if rng.random() < 0.5:
            # Adding each column without carrying.
            no_carry = int("".join(str((x + y) % 10) for x, y in
                                   zip(_digits(a, width), _digits(b, width))))
            return MathDraw(rf"{_c(a)} + {_c(b)}", _c(s), prompt="จงหาผลบวก",
                            distractors=_cs(no_carry, s + 10, s - 100, answer=s))
        # Taking the smaller digit from the larger in each column.
        smaller_from_larger = int("".join(str(abs(x - y)) for x, y in
                                          zip(_digits(s, width), _digits(b, width))))
        return MathDraw(rf"{_c(s)} - {_c(b)}", _c(a), prompt="จงหาผลลบ",
                        distractors=_cs(smaller_from_larger, a + 10, a - 1000, answer=a))


class _MissingAddSubLarge(WordProblem):
    lo, hi = 1_000, 100_000

    def expr(self, rng: Random):
        a, b = _sum_pair(rng, self.lo, self.hi)
        s = a + b
        sq = r"\square"
        form = rng.randrange(3)
        if form == 0:        # a + □ = s
            return MathDraw(rf"{_c(a)} + {sq} = {_c(s)}", _c(b), prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_cs(s + a, b + 10, b - 100, answer=b))
        if form == 1:        # □ − b = a
            return MathDraw(rf"{sq} - {_c(b)} = {_c(a)}", _c(s), prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_cs(abs(a - b), s - 10, s + 100, answer=s))
        return MathDraw(rf"{_c(s)} - {sq} = {_c(a)}", _c(b), prompt="จงหาจำนวนที่แทนใน □",
                        distractors=_cs(s + a, b + 100, b - 10, answer=b))


class _AddSubWordLarge(WordProblem):
    lo, hi = 1_000, 100_000

    def expr(self, rng: Random):
        a, b = _sum_pair(rng, self.lo, self.hi)
        s = a + b
        kind = rng.randrange(4)
        if kind == 0:
            place = rng.choice(("สวนสัตว์", "พิพิธภัณฑ์", "งานกาชาด", "สวนสนุก"))
            return MathDraw("", _c(s), prompt=(
                f"เดือนแรกมีคนเข้าชม{place} {a:,} คน เดือนที่สองมีคนเข้าชม {b:,} คน "
                f"สองเดือนมีคนเข้าชมทั้งหมดกี่คน"),
                distractors=_cs(abs(a - b), s + 1000, s - 100, answer=s))
        if kind == 1:
            return MathDraw("", _c(a), prompt=(
                f"โรงงานผลิตขวดน้ำได้ {s:,} ขวด ส่งไปขายแล้ว {b:,} ขวด เหลือขวดน้ำกี่ขวด"),
                distractors=_cs(s + b, a + 1000, a - 10, answer=a))
        if kind == 2:
            hi_, lo_ = max(a, b), min(a, b)
            if hi_ == lo_:
                hi_ += self.lo
            return MathDraw("", _c(hi_ - lo_), prompt=(
                f"รถยนต์คันหนึ่งราคา {hi_:,} บาท รถจักรยานยนต์คันหนึ่งราคา {lo_:,} บาท "
                f"รถยนต์ราคาแพงกว่ารถจักรยานยนต์กี่บาท"),
                distractors=_cs(hi_ + lo_, hi_ - lo_ + 1000, hi_ - lo_ - 100, answer=hi_ - lo_))
        # Two steps: saving, then a purchase.
        price = rng.randint(self.lo // 2, s - self.lo // 2)
        left = s - price
        return MathDraw("", _c(left), prompt=(
            f"ครอบครัวหนึ่งเก็บเงินได้ {a:,} บาท แล้วเก็บเพิ่มอีก {b:,} บาท "
            f"นำไปซื้อตู้เย็นราคา {price:,} บาท เหลือเงินกี่บาท"),
            distractors=_cs(abs(a - price), s + price, left + 1000, answer=left))


# ── ป.4 เศษส่วน: เปรียบเทียบเมื่อตัวส่วนเป็นพหุคูณ (ค 1.1 ป.4/4) ───────────────


# ── ป.4 โจทย์ปัญหาระคน: เลือกโจทย์ที่ตรงกับประโยคสัญลักษณ์ (ป.4/12) ─────────────


# ── ป.5 ความยาวและน้ำหนักในรูปทศนิยม (ค 2.1 ป.5/1–2) ────────────────────────



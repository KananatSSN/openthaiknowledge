"""Application sets for topics whose last stage had one or two stem shapes.

From the 2026-09 content audit (MATH_CONTENT_AUDIT.md, section 4): the
Application stage should be the richest, but in these topics it held a bare
computation. Each set here puts the topic's skill into three or more
situations, and is filed in its topic's Application stage.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.content import text
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType
from otk.kit import story as _story
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths


def _n(v: int) -> str:
    return f"{v:,}".replace(",", "{,}")


def _nums(answer: int, *wrongs: int, lo: int = 0) -> list[str]:
    return [_n(int(w)) for w in _story.keep(*wrongs, answer=answer, lo=lo)]


def _surd(k: int, n: int) -> str:
    """k√n, with 1 and √1 left unwritten."""
    if n == 1:
        return str(k)
    return (str(k) if k != 1 else "") + rf"\sqrt{{{n}}}"


def _split_square(n: int) -> tuple[int, int]:
    """n = k²·m with m square-free."""
    k = 1
    for d in range(2, int(math.isqrt(n)) + 1):
        while n % (d * d) == 0:
            n //= d * d
            k *= d
    return k, n


# ── ป.1 การบวก และการลบ ──────────────────────────────────────────────────────

_P1_THINGS = (("ลูกอม", "เม็ด"), ("ดินสอ", "แท่ง"), ("สติกเกอร์", "แผ่น"), ("ลูกแก้ว", "ลูก"), ("ส้ม", "ผล"))


# ── ป.1–ป.2 แบบรูป ────────────────────────────────────────────────────────────


# ── ป.1 เรขาคณิต 3 มิติ ───────────────────────────────────────────────────────


# ── ป.2 เงิน ──────────────────────────────────────────────────────────────────


# ── ป.3–ป.4 ค่าประจำหลัก ──────────────────────────────────────────────────────

_PLACES = ("หลักหน่วย", "หลักสิบ", "หลักร้อย", "หลักพัน", "หลักหมื่น", "หลักแสน", "หลักล้าน")


class _PlaceValueWord(QuestionType):
    lo: int
    hi: int
    sentences: tuple[str, ...]           # a count in a sentence, with {n}
    compare: tuple[str, tuple[str, ...]]  # what is compared, and four places

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            n = rng.randint(self.lo, self.hi)
            digits = str(n)
            i = rng.choice([j for j, d in enumerate(digits) if d != "0" and j < len(digits) - 1])
            d = int(digits[i])
            place = len(digits) - 1 - i
            value = d * 10 ** place
            said = rng.choice(self.sentences).format(n=f"{n:,}")
            return maths([text(f"{said} เลขโดด {d} ใน{_PLACES[place]}มีค่าเท่าใด")], _n(value),
                         _nums(value, d, value * 10, value // 10, lo=1), self.topic)
        if kind == 1:
            size = len(str(self.hi))
            cards = rng.sample(range(10), size)
            biggest = int("".join(map(str, sorted(cards, reverse=True))))
            small_digits = sorted(cards)
            if small_digits[0] == 0:
                first = next(d for d in small_digits if d)
                small_digits.remove(first)
                small_digits = [first] + small_digits
            smallest = int("".join(map(str, small_digits)))
            shown = ", ".join(map(str, cards))
            if rng.random() < 0.5:
                return maths([text(f"มีบัตรตัวเลข {shown} ใช้บัตรทุกใบใบละครั้ง เขียนจำนวนที่มากที่สุดได้เท่าใด")],
                             _n(biggest), _nums(biggest, smallest, int(str(biggest)[::-1]),
                                                int(str(biggest)[:2][::-1] + str(biggest)[2:]), lo=1), self.topic)
            wrong_zero = int("".join(map(str, sorted(cards))))
            return maths([text(f"มีบัตรตัวเลข {shown} ใช้บัตรทุกใบใบละครั้ง เขียนจำนวนที่น้อยที่สุดได้เท่าใด "
                               f"(หลักซ้ายสุดต้องไม่เป็น 0)")],
                         _n(smallest), _nums(smallest, biggest, wrong_zero, smallest + 9, lo=1), self.topic)
        what, names = self.compare
        names = list(names)
        base = rng.randint(self.lo, self.hi - self.hi // 10)
        values = []
        while len(values) < 4:
            # Close numbers that differ in a middle place, so the first digit alone does not decide.
            v = base + rng.randint(0, self.hi // 20)
            if v not in values:
                values.append(v)
        most = rng.random() < 0.5
        pick = max if most else min
        right = names[values.index(pick(values))]
        listed = " ".join(f"{nm} {_n(v).replace('{,}', ',')}" for nm, v in zip(names, values))
        word = "มากที่สุด" if most else "น้อยที่สุด"
        return _choices([text(f"{what}ของแต่ละแห่งเป็นดังนี้: {listed} แห่งใดมี{what}{word}")],
                        right, [nm for nm in names if nm != right], self.topic)


# ── ป.3 รูปสมมาตร ─────────────────────────────────────────────────────────────


# ── ป.6 จำนวนเฉพาะ ────────────────────────────────────────────────────────────


# ── ป.6 พื้นที่รูปสามเหลี่ยม ───────────────────────────────────────────────────


# ── ม.1 แยกตัวประกอบเฉพาะ ─────────────────────────────────────────────────────


# ── ม.4 เพิ่มเติม จัดรูปกรณฑ์ ─────────────────────────────────────────────────


# ── ม.5 จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง ────────────────────────────────────


# ── ม.5 ดอกเบี้ยและมูลค่าของเงิน ─────────────────────────────────────────────


# ── ม.5 เพิ่มเติม ทฤษฎีบททวินาม ───────────────────────────────────────────────


# ── ม.6 ค่ากลางของข้อมูล ──────────────────────────────────────────────────────


# ── ม.6 เพิ่มเติม อนุกรม ──────────────────────────────────────────────────────


# ── ม.1 นิพจน์พีชคณิต ─────────────────────────────────────────────────────────


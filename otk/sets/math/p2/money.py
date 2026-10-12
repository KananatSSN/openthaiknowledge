"""เงิน

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.2/*

Sets moved here from: math_apply_stage, math_chapters, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_chapters import P2, _distinct
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p2 import _texts
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_p2 import MONEY

PROVENANCE = Provenance("original")


def _and(parts: list[str]) -> str:
    """["a", "b", "c"] -> "a b และ c", the way the books list amounts."""
    return parts[0] if len(parts) == 1 else " ".join(parts[:-1]) + " และ" + parts[-1]


_MONEY_TOPIC = "เงิน"


_COINS = {1: "เหรียญหนึ่งบาท", 2: "เหรียญสองบาท", 5: "เหรียญห้าบาท", 10: "เหรียญสิบบาท"}


_NOTES = {20: "ธนบัตรยี่สิบบาท", 50: "ธนบัตรห้าสิบบาท", 100: "ธนบัตรหนึ่งร้อยบาท",
          500: "ธนบัตรห้าร้อยบาท"}


_SATANG = {25: "เหรียญยี่สิบห้าสตางค์", 50: "เหรียญห้าสิบสตางค์"}


def _pieces(value: int, count: int) -> str:
    """10, 3 -> 'เหรียญสิบบาท 3 เหรียญ'; 100, 2 -> 'ธนบัตรหนึ่งร้อยบาท 2 ฉบับ'."""
    if value in _NOTES:
        return f"{_NOTES[value]} {count} ฉบับ"
    return f"{_COINS[value]} {count} เหรียญ"


def _purse(rng: Random, kinds: int, hi: int) -> tuple[dict[int, int], int]:
    while True:
        purse = {v: rng.randint(1, 5) for v in sorted(rng.sample(sorted(_COINS | _NOTES), kinds),
                                                      reverse=True)}
        total = sum(v * n for v, n in purse.items())
        if total <= hi:
            return purse, total


def _baht(satang: int) -> str:
    b, s = divmod(satang, 100)
    if not s:
        return f"{b} บาท"
    return f"{s} สตางค์" if not b else f"{b} บาท {s} สตางค์"


@question_type("math.money_picture_p2", display_name={"th": "นับเงินจากภาพ"},
               level=P2, topic="เงิน")
class MoneyPictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        m = rng.choice(MONEY)
        img = image(m.asset_id, alt="ภาพเหรียญและธนบัตร")
        biggest = m.pieces[0][0]
        # Counting pieces; missing one piece of the largest kind; adding each
        # denomination once.
        wrongs = [m.count, m.total - biggest, m.total + biggest, sum(v for v, _ in m.pieces)]
        return _math_q([text("ในภาพมีเงินรวมกี่บาท"), img],
                       str(m.total), _near(m.total, *wrongs, lo=1), self.topic)


@question_type("math.money_count_p2", display_name={"th": "นับเงินเหรียญและธนบัตร"},
               level=P2, topic=_MONEY_TOPIC)
class MoneyCountP2(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.6:
            purse, total = _purse(rng, 3, 1000)
            p = rng.choice(_story.NAMES)
            listed = _and([_pieces(v, n) for v, n in purse.items()])
            biggest = max(purse)
            return MathDraw("", str(total), prompt=f"{p}มี{listed} {p}มีเงินรวมกี่บาท",
                            # One of each piece, the pieces counted, one piece
                            # too many or too few.
                            distractors=_story.keep(sum(purse), total + biggest, total - biggest,
                                                    sum(purse.values()), answer=total, lo=1))
        a, b = _story.names(rng, 2)
        while True:
            (pa, ta), (pb, tb) = _purse(rng, 2, 500), _purse(rng, 2, 500)
            if ta != tb:
                break
        diff = abs(ta - tb)
        return MathDraw("", str(diff),
                        prompt=(f"{a}มี{_and([_pieces(v, n) for v, n in pa.items()])} "
                                f"{b}มี{_and([_pieces(v, n) for v, n in pb.items()])} "
                                f"สองคนมีเงินต่างกันกี่บาท"),
                        distractors=_story.keep(ta + tb, max(ta, tb), min(ta, tb), diff + 10,
                                                answer=diff, lo=1))


@question_type("math.money_exchange_p2", display_name={"th": "การแลกเงิน"},
               level=P2, topic=_MONEY_TOPIC)
class MoneyExchangeP2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            note = rng.choice((20, 50, 100))
            coin = rng.choice([c for c in _COINS if note % c == 0 and note // c <= 50])
            k = rng.choice([k for k in (1, 2, 3) if k * note // coin <= 100])
            ans = k * note // coin
            return MathDraw("", str(ans),
                            prompt=(f"นำ{_NOTES[note]} {k} ฉบับ ไปแลกเป็น{_COINS[coin]}ทั้งหมด "
                                    f"จะได้{_COINS[coin]}กี่เหรียญ"),
                            # The amount itself, one note only, the wrong way round.
                            distractors=_story.keep(k * note, note // coin, k * coin, ans + k,
                                                    answer=ans, lo=1))
        if kind == 1:
            coin = rng.choice((5, 10))
            note = rng.choice([v for v in (20, 50, 100) if v % coin == 0])
            q = rng.choice([q for q in (1, 2, 3, 4) if q * note // coin <= 40])
            cnt = q * note // coin
            return MathDraw("", str(q),
                            prompt=(f"{rng.choice(_story.NAMES)}มี{_COINS[coin]} {cnt} เหรียญ "
                                    f"นำไปแลกเป็น{_NOTES[note]}ได้กี่ฉบับ"),
                            distractors=_story.keep(cnt * coin, cnt, q + 1, q * 2, answer=q, lo=1))
        if rng.random() < 0.5:
            coin, per = rng.choice(((50, 2), (25, 4)))
            n = per * rng.randint(1, 5)
            ans = n // per
            return MathDraw("", str(ans), prompt=f"{_SATANG[coin]} {n} เหรียญ รวมเป็นเงินกี่บาท",
                            # Counting coins as baht, satang as baht.
                            distractors=_story.keep(n, n * coin, n // 2 if per == 4 else n * 2,
                                                    ans + 1, answer=ans, lo=1))
        baht = rng.randint(2, 10)
        coin, per = rng.choice(((50, 2), (25, 4)))
        ans = baht * per
        return MathDraw("", str(ans),
                        prompt=f"นำเงิน {baht} บาท ไปแลกเป็น{_SATANG[coin]} จะได้กี่เหรียญ",
                        distractors=_story.keep(baht, baht * coin, baht * (6 - per), ans + per,
                                                answer=ans, lo=1))


@question_type("math.money_word_p2", display_name={"th": "โจทย์ปัญหาเกี่ยวกับเงิน (เปรียบเทียบและพอซื้อหรือไม่)"},
               level={"th": "ป.2"}, topic="เงิน")
class MoneyWordP2(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        who, other = _story.names(rng)
        kind = rng.randrange(3)
        if kind == 0:
            tens, fives, ones = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 9)
            mine = 10 * tens + 5 * fives + ones
            notes = rng.randint(1, 4)
            theirs = 20 * notes + rng.choice((0, 5, 10))
            while theirs == mine:
                theirs += 5
            more, less = (who, other) if mine > theirs else (other, who)
            gap = abs(mine - theirs)
            extra = "" if theirs == 20 * notes else f" และเหรียญ 5 บาท {(theirs - 20 * notes) // 5} เหรียญ"
            stem = (f"{who}มีเหรียญ 10 บาท {tens} เหรียญ เหรียญ 5 บาท {fives} เหรียญ และเหรียญ 1 บาท {ones} เหรียญ "
                    f"{other}มีธนบัตร 20 บาท {notes} ใบ{extra} ใครมีเงินมากกว่า และมากกว่ากี่บาท")
            return _choices([text(stem)], f"{more} มากกว่า {gap} บาท",
                            [f"{less} มากกว่า {gap} บาท", f"{more} มากกว่า {gap + 5} บาท",
                             "มีเงินเท่ากัน", f"{more} มากกว่า {gap + 10} บาท"], self.topic)
        if kind == 1:
            price = rng.choice((45, 60, 75, 90, 120, 150))
            have = price - rng.choice((5, 10, 15, 20, 25))
            twenties = have // 20
            rest = have - 20 * twenties
            stem = (f"{who}มีธนบัตร 20 บาท {twenties} ใบ และเหรียญรวมกัน {rest} บาท "
                    f"ต้องการซื้อ{rng.choice(_story.TOYS)}ราคา {price} บาท ต้องมีเงินเพิ่มอีกกี่บาท")
            if rest == 0:
                stem = (f"{who}มีธนบัตร 20 บาท {twenties} ใบ ต้องการซื้อ{rng.choice(_story.TOYS)}ราคา {price} บาท "
                        f"ต้องมีเงินเพิ่มอีกกี่บาท")
            need = price - have
            return maths([text(stem)], str(need), _nums(need, have, price + have, need + 10, lo=1), self.topic)
        fifties, quarters = rng.randint(1, 8), rng.randint(1, 8)
        satang = 50 * fifties + 25 * quarters
        baht, left = divmod(satang, 100)
        right = f"{baht} บาท {left} สตางค์" if left else f"{baht} บาท"
        if baht == 0:
            right = f"{left} สตางค์"
        wrongs = [f"{fifties + quarters} บาท", f"{satang} บาท", f"{baht + 1} บาท {left} สตางค์" if left
                  else f"{baht + 1} บาท", f"{baht} บาท {(left + 25) % 100} สตางค์"]
        return _choices([text(f"{who}มีเหรียญ 50 สตางค์ {fifties} เหรียญ และเหรียญ 25 สตางค์ {quarters} เหรียญ "
                              f"รวมเป็นเงินเท่าใด")], right, wrongs, self.topic)


@question_type("math.baht_satang_p2", display_name={"th": "บอกจำนวนเงินเป็นบาทและสตางค์"},
               level=P2, topic=_MONEY_TOPIC)
class BahtSatangP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        baht = {v: rng.randint(1, 4) for v in sorted(rng.sample(sorted(_COINS), 2), reverse=True)}
        sat = {v: rng.randint(1, 3) for v in (50, 25)}
        whole = sum(v * n for v, n in baht.items())
        loose = sum(v * n for v, n in sat.items())
        total = whole * 100 + loose
        listed = _and([_pieces(v, n) for v, n in baht.items()]
                      + [f"{_SATANG[v]} {n} เหรียญ" for v, n in sat.items()])
        right = _baht(total)
        # The satang left uncarried, each satang coin counted as a baht, and
        # a coin miscounted either way.
        wrongs = _distinct(right,
                           f"{whole} บาท {loose} สตางค์" if loose >= 100 else _baht(total + 100),
                           _baht((whole + sum(sat.values())) * 100),
                           _baht(total - 25), _baht(total + 50), _baht(total - 50))
        return _texts([text(f"{listed} รวมเป็นเงินเท่าใด")], right, wrongs[:3], self.topic)

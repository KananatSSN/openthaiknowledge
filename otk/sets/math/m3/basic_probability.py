"""ความน่าจะเป็นเบื้องต้น

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 3.2 ม.3/1

Sets moved here from: math_m3, math_pictures_extra.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import frac_tex
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_m3 import LEVEL
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_pictures_extra import COLOURS, SPINNERS, _fr

PROVENANCE = Provenance("original")


def _fracs(value: Fraction, wrongs) -> list[str]:
    """Distinct wrong fractions, none equal in value to the answer."""
    out = []
    for w in wrongs:
        w = Fraction(w)
        if w != value and 0 <= w <= 1 and frac_tex(w) not in out:
            out.append(frac_tex(w))
    return out


_PROB_TOPIC = "ความน่าจะเป็นเบื้องต้น"


SPINNER_ALT = "ภาพวงล้อที่แบ่งเป็นช่องขนาดเท่ากัน ระบายหลายสี และมีเข็มชี้"


def _prob(f: Fraction) -> str:
    return "0" if f == 0 else "1" if f == 1 else _fr(f.numerator, f.denominator)


@question_type("math.probability_die_coin_m3",
               display_name={"th": "ความน่าจะเป็น: ลูกเต๋า เหรียญ และวงล้อ"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityDieCoinM3(QuestionType):
    _EVENTS = (("ขึ้นแต้มคู่", lambda n: n % 2 == 0), ("ขึ้นแต้มคี่", lambda n: n % 2),
               ("ขึ้นแต้มมากกว่า 4", lambda n: n > 4), ("ขึ้นแต้มน้อยกว่า 3", lambda n: n < 3),
               ("ขึ้นแต้มที่เป็นจำนวนเฉพาะ", lambda n: n in (2, 3, 5)),
               ("ขึ้นแต้มที่หารด้วย 3 ลงตัว", lambda n: n % 3 == 0),
               ("ขึ้นแต้ม 7", lambda n: n == 7), ("ขึ้นแต้มไม่เกิน 6", lambda n: n <= 6))

    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.7:
            name, test = rng.choice(self._EVENTS)
            fav = sum(1 for n in range(1, 7) if test(n))
            value = Fraction(fav, 6)
            # Favourable over unfavourable, the complement, and the count alone.
            wrongs = [Fraction(fav, 6 - fav) if 0 < fav < 6 else Fraction(1, 6),
                      1 - value, Fraction(1, fav) if fav else Fraction(1, 2), Fraction(fav + 1, 6),
                      Fraction(1, 6), Fraction(5, 6), Fraction(1, 2)]
            stem = f"ทอดลูกเต๋าที่เที่ยงตรง 1 ลูก 1 ครั้ง ความน่าจะเป็นที่จะ{name} เท่ากับเท่าใด"
        else:
            sectors = rng.randint(5, 12)
            red = rng.randint(1, sectors - 2)
            value = Fraction(red, sectors)
            wrongs = [Fraction(red, sectors - red), 1 - value, Fraction(1, sectors),
                      Fraction(red + 1, sectors)]
            stem = (f"วงล้อแบ่งเป็น {sectors} ช่องเท่า ๆ กัน ระบายสีแดง {red} ช่อง ที่เหลือสีขาว "
                    f"หมุนวงล้อ 1 ครั้ง ความน่าจะเป็นที่เข็มจะชี้ช่องสีแดงเท่ากับเท่าใด")
        return _maths([text(stem)], frac_tex(value), _fracs(value, wrongs), self.topic)


@question_type("math.probability_bag_m3",
               display_name={"th": "ความน่าจะเป็น: หยิบลูกบอลและบัตรตัวเลข"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityBagM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.6:
            c1, c2, c3 = rng.sample(_story.COLOURS, 3)
            a, b, c = rng.randint(1, 9), rng.randint(1, 9), rng.randint(1, 9)
            total = a + b + c
            if rng.random() < 0.5:
                value = Fraction(a, total)
                ask = f"ได้ลูกบอล{c1}"
                wrongs = [Fraction(a, b + c), Fraction(1, 3), Fraction(b + c, total),
                          Fraction(a, total - 1), Fraction(a + 1, total), Fraction(1, 2)]
            else:
                value = Fraction(a + c, total)
                ask = f"ไม่ได้ลูกบอล{c2}"
                wrongs = [Fraction(b, total), Fraction(a + c, b) if b > a + c else Fraction(2, 3),
                          Fraction(a, total), Fraction(a + c - 1, total), Fraction(1, 3),
                          Fraction(1, 2)]
            stem = (f"ในถุงมีลูกบอล{c1} {a} ลูก {c2} {b} ลูก และ{c3} {c} ลูก ขนาดเท่ากัน "
                    f"สุ่มหยิบ 1 ลูก ความน่าจะเป็นที่จะ{ask}เท่ากับเท่าใด")
        else:
            n = rng.choice((10, 12, 15, 20, 24, 25, 30))
            k = rng.choice((2, 3, 4, 5))
            fav = n // k
            value = Fraction(fav, n)
            stem = (f"บัตร {n} ใบ เขียนหมายเลข 1 ถึง {n} ใบละหนึ่งหมายเลข สุ่มหยิบ 1 ใบ "
                    f"ความน่าจะเป็นที่จะได้หมายเลขที่หารด้วย {k} ลงตัวเท่ากับเท่าใด")
            wrongs = [Fraction(fav, n - fav), Fraction(1, fav), Fraction(fav + 1, n), Fraction(k, n),
                      Fraction(fav - 1, n), Fraction(fav + 2, n), Fraction(1, 2)]
        return _maths([text(stem)], frac_tex(value), _fracs(value, wrongs), self.topic)


@question_type("math.spinner_probability_m3", display_name={"th": "ความน่าจะเป็นจากวงล้อ"},
               level={"th": "ม.3"}, topic="ความน่าจะเป็นเบื้องต้น")
class SpinnerProbabilityM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SPINNERS)
        n = len(s.sectors)
        present = sorted(set(s.sectors))
        img = image(s.asset_id, alt=SPINNER_ALT)
        if rng.random() < 0.3:
            # "Not this colour": the complement.
            c = rng.choice(present)
            p = Fraction(n - s.count(c), n)
            wrongs = [_prob(Fraction(s.count(c), n)), _prob(Fraction(n - s.count(c), s.count(c))
                                                             if s.count(c) else Fraction(1, n)),
                      _prob(Fraction(1, len(present))), _prob(Fraction(n - s.count(c), n + 1))]
            ask = f"ความน่าจะเป็นที่เข็มจะไม่ชี้ช่อง{COLOURS[c]}"
        else:
            c = rng.choice(present)
            p = Fraction(s.count(c), n)
            other = n - s.count(c)
            # Colours rather than sectors; this colour against the rest; the rest.
            wrongs = [_prob(Fraction(1, len(present))), _prob(Fraction(s.count(c), other))
                      if other else "0", _prob(Fraction(other, n)), _prob(Fraction(s.count(c), n + 1))]
            ask = f"ความน่าจะเป็นที่เข็มจะชี้ช่อง{COLOURS[c]}"
        right = _prob(p)
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
        for extra in (Fraction(1, n), Fraction(1, 2), Fraction(2, n + 1)):
            if len(wrongs) >= 3:
                break
            if _prob(extra) not in (right, *wrongs):
                wrongs.append(_prob(extra))
        return _math_q([text(f"หมุนวงล้อหนึ่งครั้ง (ช่องทุกช่องมีขนาดเท่ากัน และเข็มไม่ชี้บนเส้นแบ่ง) {ask}"),
                        img], right, wrongs, self.topic)


@question_type("math.probability_two_events_m3",
               display_name={"th": "ความน่าจะเป็น: การทดลองสองขั้น (เหรียญสองเหรียญ ลูกเต๋าสองลูก)"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityTwoEventsM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            outcomes = [(a, b) for a in "HT" for b in "HT"]
            name, test = rng.choice((("ออกหัวอย่างน้อย 1 เหรียญ", lambda o: "H" in o),
                                     ("ออกหัวทั้งสองเหรียญ", lambda o: o == ("H", "H")),
                                     ("ออกหัวหนึ่งเหรียญและก้อยหนึ่งเหรียญ", lambda o: len(set(o)) == 2)))
            fav = sum(1 for o in outcomes if test(o))
            value = Fraction(fav, 4)
            # Three outcomes (HH, HT, TT) instead of four is the classic mistake.
            wrongs = [Fraction(fav, 3) if fav < 3 else Fraction(2, 3), 1 - value, Fraction(1, 2),
                      Fraction(1, 3), Fraction(1, 4), Fraction(3, 4)]
            stem = f"โยนเหรียญที่เที่ยงตรง 2 เหรียญพร้อมกัน ความน่าจะเป็นที่จะ{name}เท่ากับเท่าใด"
        elif kind == 1:
            s = rng.randint(3, 11)
            fav = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
            value = Fraction(fav, 36)
            wrongs = [Fraction(1, 11), Fraction(fav, 12), Fraction(fav + 1, 36), Fraction(1, 6)]
            stem = (f"ทอดลูกเต๋าที่เที่ยงตรง 2 ลูกพร้อมกัน ความน่าจะเป็นที่ผลรวมของแต้ม"
                    f"เท่ากับ {s} เท่ากับเท่าใด")
        else:
            value = Fraction(1, 4)
            wrongs = [Fraction(1, 12), Fraction(1, 2), Fraction(1, 8), Fraction(2, 3)]
            want = rng.choice(("ออกหัวและลูกเต๋าขึ้นแต้มคู่", "ออกก้อยและลูกเต๋าขึ้นแต้มคี่"))
            if rng.random() < 0.5:
                value = Fraction(1, 12)
                want = f"ออกหัวและลูกเต๋าขึ้นแต้ม {rng.randint(1, 6)}"
                wrongs = [Fraction(1, 8), Fraction(1, 6), Fraction(1, 2), Fraction(2, 12)]
            stem = f"โยนเหรียญ 1 เหรียญ และทอดลูกเต๋า 1 ลูกพร้อมกัน ความน่าจะเป็นที่จะ{want}เท่ากับเท่าใด"
        return _maths([text(stem)], frac_tex(value), _fracs(value, wrongs), self.topic)


def _card_union_parameters(rng: Random) -> tuple[int, int, int]:
    count = rng.randint(24, 60)
    first, second = rng.sample((2, 3, 4, 5, 6), 2)
    return count, first, second


@question_type("math.probability_number_card_or_m3",
               display_name={"th": "ความน่าจะเป็นของบัตรเลขที่ตรงเงื่อนไขอย่างน้อยหนึ่งข้อ"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityNumberCardOrM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        count, first, second = _card_union_parameters(rng)
        first_count, second_count = count // first, count // second
        overlap = count // math.lcm(first, second)
        hits = first_count + second_count - overlap
        answer = Fraction(hits, count)
        counted_twice = Fraction(first_count + second_count, count)
        wrongs = _fracs(answer, (
            counted_twice, Fraction(overlap, count), 1 - answer,
            Fraction(first_count, count), Fraction(second_count, count),
            Fraction(hits + 1, count), Fraction(1, count),
        ))
        if frac_tex(counted_twice) in wrongs:
            named("probability.double_count_overlap", frac_tex(counted_twice))
        if frac_tex(1 - answer) in wrongs:
            named("part.complement", frac_tex(1 - answer))
        return _maths([text(
            f"บัตร {count} ใบ เขียนหมายเลข 1 ถึง {count} ใบละหนึ่งหมายเลข สุ่มหยิบ 1 ใบ "
            f"ความน่าจะเป็นที่จะได้หมายเลขที่หารด้วย {first} หรือ {second} ลงตัวเท่ากับเท่าใด"
        )], frac_tex(answer), wrongs, self.topic)


def _two_draw_parameters(rng: Random) -> tuple[int, int, bool]:
    return rng.randint(2, 12), rng.randint(2, 12), rng.random() < 0.5


@question_type("math.probability_two_colours_without_replacement_m3",
               display_name={"th": "ความน่าจะเป็นเมื่อหยิบสองครั้งไม่ใส่คืน"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityTwoColoursWithoutReplacementM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        red, blue, same = _two_draw_parameters(rng)
        total = red + blue
        if same:
            hits = red * (red - 1) + blue * (blue - 1)
            with_replacement = Fraction(red * red + blue * blue, total * total)
            one_case = Fraction(red * (red - 1), total * (total - 1))
            event = "ลูกบอลทั้งสองลูกมีสีเดียวกัน"
        else:
            hits = 2 * red * blue
            with_replacement = Fraction(2 * red * blue, total * total)
            one_case = Fraction(red * blue, total * (total - 1))
            event = "ลูกบอลทั้งสองลูกมีสีต่างกัน"
        answer = Fraction(hits, total * (total - 1))
        wrongs = _fracs(answer, (
            with_replacement, one_case,
            Fraction(hits, total * total),
            Fraction(red, total), 1 - answer,
            Fraction(hits + 1, total * (total - 1)),
        ))
        if frac_tex(with_replacement) in wrongs:
            named("probability.with_replacement", frac_tex(with_replacement))
        if frac_tex(one_case) in wrongs:
            named("steps.missed_a_step", frac_tex(one_case))
        return _maths([text(
            f"ถุงมีลูกบอลสีแดง {red} ลูก และสีน้ำเงิน {blue} ลูก ขนาดเท่ากัน "
            f"สุ่มหยิบทีละลูก 2 ครั้งโดยไม่ใส่คืน ความน่าจะเป็นที่{event}เท่ากับเท่าใด"
        )], frac_tex(answer), wrongs, self.topic)


def _target_probability_parameters(rng: Random) -> tuple[int, int, int]:
    return rng.randint(2, 8), rng.randint(3, 10), rng.randint(2, 12)


@question_type("math.probability_add_balls_m3",
               display_name={"th": "เพิ่มลูกบอลให้ได้ความน่าจะเป็นที่กำหนด"},
               level=LEVEL, topic=_PROB_TOPIC)
class ProbabilityAddBallsM3(QuestionType):
    invent_numbers = True

    def build(self, rng: Random) -> GeneratedQuestion:
        red, blue, added = _target_probability_parameters(rng)
        target = Fraction(red + added, red + blue + added)
        wrongs = [
            named("steps.missed_a_step", str(red + added)),
            str(red + blue + added),
            str(added + 1), str(max(1, added - 1)),
            str(added + 2),
        ]
        return _maths([text(
            f"ถุงมีลูกบอลสีแดง {red} ลูก และสีน้ำเงิน {blue} ลูก ขนาดเท่ากัน "
            f"ต้องเพิ่มลูกบอลสีแดงอีกกี่ลูก เพื่อให้ความน่าจะเป็นที่สุ่มหยิบ 1 ลูกแล้วได้สีแดง"
            f"เท่ากับ {target.numerator}/{target.denominator}"
        )], str(added), wrongs, self.topic)


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathDraw, WordProblem  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More probability (2026-11): the complement, the sum of two dice, and the expected count ──


@question_type("math.probability_complement_m3", display_name={"th": "ความน่าจะเป็นที่เหตุการณ์จะไม่เกิดขึ้น"},
               level=LEVEL, topic="ความน่าจะเป็นเบื้องต้น")
class ProbabilityComplementM3(WordProblem):
    def expr(self, rng: Random):
        d = rng.randint(3, 12)
        k = rng.randint(1, d - 1)
        p = Fraction(k, d)
        right = 1 - p
        what = rng.choice(("ฝนจะตก", "ทีมเหย้าจะชนะ", "รถไฟจะมาตรงเวลา", "สุ่มได้บัตรรางวัล"))
        prompt = f"ความน่าจะเป็นที่{what}เท่ากับ {p.numerator}/{p.denominator} ความน่าจะเป็นที่จะไม่เป็นเช่นนั้นเท่ากับเท่าใด"
        # The same chance; one part; one part short; the top over the top and bottom.
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk3(p, Fraction(1, p.denominator), right - Fraction(1, p.denominator),
                                         Fraction(k, d + k), answer=right, lo=Fraction(1, 100)))


@question_type("math.two_dice_sum_m3", display_name={"th": "ความน่าจะเป็นของผลรวมแต้มลูกเต๋าสองลูก"},
               level=LEVEL, topic="ความน่าจะเป็นเบื้องต้น")
class TwoDiceSumM3(WordProblem):
    def expr(self, rng: Random):
        s = rng.randint(3, 11)
        ways = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
        right = Fraction(ways, 36)
        prompt = f"ทอดลูกเต๋าสองลูกพร้อมกัน 1 ครั้ง ความน่าจะเป็นที่ผลรวมของแต้มเท่ากับ {s} เท่ากับเท่าใด"
        # Out of 12 (the sums), out of 11 (the possible totals), or the unordered pairs out of 21.
        pairs = sum(1 for a in range(1, 7) for b in range(a, 7) if a + b == s)
        return MathDraw("", frac_tex(right), prompt=prompt,
                        distractors=_fk3(Fraction(ways, 12), Fraction(1, 11), Fraction(pairs, 21), Fraction(ways + 1, 36),
                                         answer=right, lo=Fraction(0)))


@question_type("math.expected_count_m3", display_name={"th": "คาดว่าจะเกิดเหตุการณ์ประมาณกี่ครั้ง"},
               level=LEVEL, topic="ความน่าจะเป็นเบื้องต้น")
class ExpectedCountM3(WordProblem):
    def expr(self, rng: Random):
        red, blue = rng.randint(1, 6), rng.randint(1, 6)
        total = red + blue
        trials = total * rng.randint(4, 30)
        right = trials * red // total
        prompt = (f"ถุงใบหนึ่งมีลูกบอลสีแดง {red} ลูก สีฟ้า {blue} ลูก สุ่มหยิบ 1 ลูกแล้วใส่คืน ทำซ้ำ {trials} ครั้ง "
                  "คาดว่าจะได้สีแดงประมาณกี่ครั้ง")
        # The blue count; half the trials; the trials over red.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(trials - right, trials // 2, trials // red if red > 1 else trials // 3,
                                                right + total, answer=right, lo=1))

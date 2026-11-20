"""การบวกลบระคน

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/4, ค 1.1 ป.1/5

Sets moved here from: math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, _no_carry_sum
from otk.sets._support.math_p1 import LEVEL

PROVENANCE = Provenance("original")


def _mixed_story(rng: Random, a: int, b: int, c: int, add_first: bool):
    """A two-step story: a, then +b, then −c (or −b then +c)."""
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    sc = rng.choice(_story.SCENES)
    if add_first:
        stories = (
            f"{sc.place}มี{sc.animal} {a} ตัว {sc.animal}{sc.arrive} {b} ตัว "
            f"ต่อมา{sc.leave} {c} ตัว {sc.place}เหลือ{sc.animal}กี่ตัว",
            f"{p}มีเงิน {a} บาท {rng.choice(_story.GIVERS)}ให้เพิ่มอีก {b} บาท "
            f"{p}ซื้อ{rng.choice(_story.SNACKS)}ไป {c} บาท {p}เหลือเงินกี่บาท",
            f"บนรถโดยสารมีผู้โดยสาร {a} คน ถึงป้ายแรกมีคนขึ้นมา {b} คน "
            f"ถึงป้ายที่สองมีคนลงไป {c} คน บนรถมีผู้โดยสารกี่คน",
            f"{p}มี{t.noun} {a} {t.cl} {q}ให้มาอีก {b} {t.cl} "
            f"{p}แบ่งให้น้องไป {c} {t.cl} {p}เหลือ{t.noun}กี่{t.cl}",
            f"{p}มี{t.noun} {a} {t.cl} {q}มี {b} {t.cl} "
            f"ทั้งสองคนนำมารวมกันแล้วแบ่งให้เพื่อน {c} {t.cl} เหลือ{t.noun}กี่{t.cl}",
        )
    else:
        stories = (
            f"ห้องสมุดมีหนังสือนิทาน {a} เล่ม นักเรียนยืมไป {b} เล่ม "
            f"ต่อมานำมาคืน {c} เล่ม ห้องสมุดมีหนังสือนิทานกี่เล่ม",
            f"แม่ค้ามีไข่ไก่ {a} ฟอง ขายไป {b} ฟอง แล้วซื้อมาเพิ่มอีก {c} ฟอง "
            f"แม่ค้ามีไข่ไก่กี่ฟอง",
            f"{p}มีเงิน {a} บาท ซื้อ{rng.choice(_story.SNACKS)}ไป {b} บาท "
            f"แล้ว{rng.choice(_story.GIVERS)}ให้เงินอีก {c} บาท {p}มีเงินกี่บาท",
            f"{sc.place}มี{sc.animal} {a} ตัว {sc.leave} {b} ตัว "
            f"ต่อมา{sc.animal}{sc.arrive} {c} ตัว {sc.place}มี{sc.animal}กี่ตัว",
            f"{p}มี{t.noun} {a} {t.cl} แบ่งให้{q} {b} {t.cl} "
            f"แล้ว{rng.choice(_story.GIVERS)}ให้มาอีก {c} {t.cl} {p}มี{t.noun}กี่{t.cl}",
        )
    return rng.choice(stories)


@question_type("math.add_sub_mixed",
               display_name={"th": "การบวกลบระคน"}, level=LEVEL,
               topic="การบวกลบระคน")
class AddSubMixed(MathType):
    def expr(self, rng: Random, hi: int = 50):
        hi = max(10, min(int(hi), 100))
        while True:
            a, b, c = (rng.randint(1, hi) for _ in range(3))
            form = rng.randrange(4)
            if form == 0:
                tex, steps = rf"{a} + {b} - {c}", (a + b, a + b - c)
                wrong = [a + b + c, a - b - c, a + b - c + 10]
            elif form == 1:
                tex, steps = rf"{a} - {b} + {c}", (a - b, a - b + c)
                # Working right to left: a − (b + c).
                wrong = [a - (b + c), a + b + c, a - b - c]
            elif form == 2:
                tex, steps = rf"{a} - {b} - {c}", (a - b, a - b - c)
                wrong = [a - b + c, a - (b - c), a + b - c]
            else:
                tex, steps = rf"{a} + {b} + {c}", (a + b, a + b + c)
                wrong = [a + b - c, a + b, _no_carry_sum(a + b, c)]
            if all(0 <= s <= 100 for s in steps):
                ans = steps[-1]
                return MathDraw(tex, str(ans), prompt="จงหาผลลัพธ์",
                                distractors=_story.keep(*wrong, ans + 1, answer=ans))


@question_type("math.add_sub_mixed_missing",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคสัญลักษณ์การบวกลบระคน"},
               level=LEVEL, topic="การบวกลบระคน")
class AddSubMixedMissing(MathType):
    def expr(self, rng: Random, hi: int = 40):
        hi = max(10, min(int(hi), 60))
        sq = r"\square"
        while True:
            a, b, c = (rng.randint(1, hi) for _ in range(3))
            form = rng.randrange(4)
            if form == 0:         # a + □ − c = d
                x, d = b, a + b - c
                tex, mids = rf"{a} + {sq} - {c} = {d}", (a + b,)
                wrong = [d + c + a, d - c + a, d + c]
            elif form == 1:       # a − □ + c = d
                x, d = b, a - b + c
                tex, mids = rf"{a} - {sq} + {c} = {d}", (a - b,)
                wrong = [a - c - d, d - a + c, a + c + d]
            elif form == 2:       # □ − b + c = d
                x, d = a, a - b + c
                tex, mids = rf"{sq} - {b} + {c} = {d}", (a - b,)
                wrong = [d - b + c, d + b + c, d - b - c]
            else:                 # a + b − □ = d
                x, d = c, a + b - c
                tex, mids = rf"{a} + {b} - {sq} = {d}", (a + b,)
                wrong = [a + b + d, d - a - b, a - b + d]
            if all(0 <= m <= 100 for m in (*mids, d)):
                return MathDraw(tex, str(x), prompt="จงหาจำนวนที่แทนใน □",
                                distractors=_story.keep(*wrong, x + 1, x - 1,
                                                        answer=x, lo=0))


@question_type("math.add_sub_mixed_word_problem",
               display_name={"th": "โจทย์ปัญหาการบวกลบระคน"}, level=LEVEL,
               topic="การบวกลบระคน")
class AddSubMixedWordProblem(WordProblem):
    def expr(self, rng: Random, hi: int = 40):
        hi = max(10, min(int(hi), 60))
        while True:
            a, b, c = (rng.randint(1, hi) for _ in range(3))
            add_first = rng.random() < 0.5
            mid = a + b if add_first else a - b
            ans = mid - c if add_first else mid + c
            if 0 <= mid <= 100 and 0 <= ans <= 100:
                break
        # Doing both steps the same way is the mistake worth catching.
        wrong = [a + b + c, a - b - c] if add_first else [a - b - c, a + b + c]
        return MathDraw("", str(ans), prompt=_mixed_story(rng, a, b, c, add_first),
                        distractors=_story.keep(*wrong, mid, ans + 1, answer=ans))


# ── More mixed adding and subtracting (2026-11): the true number sentence, hops on a number line, the
# largest result, two people after one gives, four numbers, the starting amount, and change for two items ──

from otk.kit.math_problems import ChoiceType  # noqa: E402


@question_type("math.mixed_true_sentence_p1", display_name={"th": "ประโยคสัญลักษณ์การบวกลบระคนใดถูกต้อง"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedTrueSentenceP1(ChoiceType):
    def compose(self, rng: Random):
        while True:
            a, b, c = rng.randint(10, 50), rng.randint(2, 30), rng.randint(2, 30)
            if a + b <= 100 and a + b - c >= 0:
                break
        r = a + b - c
        right = f"{a} + {b} - {c} = {r}"
        # All three added; one off; the last step done as an addition.
        wrongs = [f"{a} + {b} - {c} = {a + b + c}", f"{a} + {b} - {c} = {r + 1}",
                  f"{a} + {b} - {c} = {r - 1}" if r > 0 else f"{a} + {b} - {c} = {r + 10}"]
        return "ประโยคสัญลักษณ์ใดถูกต้อง", right, wrongs


@question_type("math.mixed_number_line_p1", display_name={"th": "เดินหน้าและถอยหลังบนเส้นจำนวน"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedNumberLineP1(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(5, 40)
        fwd = rng.randint(3, 20)
        back = rng.randint(2, start + fwd - 1)
        right = start + fwd - back
        prompt = (f"บนเส้นจำนวน เริ่มที่ {start} นับเดินหน้าไป {fwd} ช่อง "
                  f"แล้วนับถอยหลัง {back} ช่อง จะอยู่ที่จำนวนใด")
        # Both hops forward; only the first hop; the hops swapped in direction.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(start + fwd + back, start + fwd, start - fwd + back,
                                                right + 1, answer=right, lo=0))


@question_type("math.mixed_largest_p1", display_name={"th": "ผลลัพธ์ใดมากที่สุด"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedLargestP1(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                a, b, c = rng.randint(10, 40), rng.randint(2, 20), rng.randint(2, 20)
                if rng.random() < 0.5:
                    exprs[f"{a} + {b} - {c}"] = a + b - c
                else:
                    exprs[f"{a} - {c} + {b}"] = a - c + b
            values = list(exprs.values())
            if len(exprs) == 4 and len(set(values)) == 4:
                break
        right = max(exprs, key=exprs.get)
        return "ผลลัพธ์ของข้อใดมากที่สุด", right, [e for e in exprs if e != right]


@question_type("math.mixed_give_compare_p1", display_name={"th": "แบ่งให้กันแล้วใครมีมากกว่ากี่"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedGiveCompareP1(WordProblem):
    def expr(self, rng: Random):
        p, q = _story.names(rng)
        t = rng.choice(_story.THINGS)
        give = rng.randint(1, 5)
        b = rng.randint(3, 20)
        a = b + 2 * give + rng.randint(1, 10)
        right = (a - give) - (b + give)
        prompt = (f"{p}มี{t.noun} {a} {t.cl} {q}มี {b} {t.cl} {p}ให้{q}ไป {give} {t.cl} "
                  f"ตอนนี้{p}มี{t.noun}มากกว่า{q}กี่{t.cl}")
        # The gap before giving; only one side changed; the gap plus what was given.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a - b, a - b - give, a - b + give, right + 1, answer=right, lo=1))


@question_type("math.mixed_four_terms_p1", display_name={"th": "การบวกลบระคนสี่จำนวน"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedFourTermsP1(MathType):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = rng.randint(10, 40), rng.randint(2, 30), rng.randint(2, 30), rng.randint(2, 30)
            steps = (a + b, a + b - c, a + b - c + d)
            if all(0 <= s <= 100 for s in steps):
                break
        right = steps[-1]
        # The subtraction taken as addition; the last number subtracted; one off.
        return MathDraw(f"{a} + {b} - {c} + {d}", str(right), prompt="จงหาผลลัพธ์",
                        distractors=_story.keep(a + b + c + d, a + b - c - d, right + 1, right - 1,
                                                answer=right, lo=0))


@question_type("math.mixed_start_amount_p1", display_name={"th": "โจทย์ปัญหาหาจำนวนเริ่มต้น"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedStartAmountP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        t = rng.choice(_story.THINGS)
        got = rng.randint(2, 15)
        used = rng.randint(2, 15)
        left = rng.randint(5, 30)
        right = left - got + used
        if right < 1:
            right, left = right + 10, left + 10
        prompt = (f"{p}มี{t.noun}อยู่จำนวนหนึ่ง ได้มาเพิ่มอีก {got} {t.cl} แล้วแบ่งให้เพื่อนไป {used} {t.cl} "
                  f"ตอนนี้เหลือ {left} {t.cl} เดิม{p}มี{t.noun}กี่{t.cl}")
        # Working forward instead of back; ignoring one step each way.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(left + got - used, left + used, left - got, left + got + used,
                                                answer=right, lo=1))


@question_type("math.mixed_change_p1", display_name={"th": "ซื้อของสองอย่างแล้วได้เงินทอน"},
               level=LEVEL, topic="การบวกลบระคน")
class MixedChangeP1(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        x, y = rng.sample(_story.SNACKS, 2)
        a, b = rng.randint(5, 30), rng.randint(5, 30)
        paid = 50 if a + b < 50 else 100
        right = paid - a - b
        prompt = (f"{p}ซื้อ{x}ราคา {a} บาท และ{y}ราคา {b} บาท จ่ายเงิน {paid} บาท "
                  f"{p}จะได้รับเงินทอนกี่บาท")
        # Only one item taken off; the cost of the two; the second item added back.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(paid - a, paid - b, a + b, paid - a + b, answer=right, lo=1))

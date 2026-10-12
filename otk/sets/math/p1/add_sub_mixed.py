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

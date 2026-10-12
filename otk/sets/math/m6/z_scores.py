"""ค่ามาตรฐาน

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data, math_m6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem
from otk.sets._support.math_m6 import M6

PROVENANCE = Provenance("original")


@question_type("math.z_score",
               display_name={"th": "คะแนนมาตรฐาน (Z-score)"}, level={"th": "ม.6"},
               topic="ค่ามาตรฐาน")
class ZScore(WordProblem):
    def expr(self, rng: Random):
        mu = rng.randint(40, 70)
        sigma = rng.choice([2, 4, 5, 10])
        z = rng.choice([n for n in range(-3, 4) if n])
        x = mu + z * sigma
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"ถ้า x = {x}, μ = {mu}, σ = {sigma} แล้ว Z-score เท่ากับเท่าใด?",
            f"คะแนนสอบวิชาหนึ่งมีค่าเฉลี่ย {mu} คะแนน ส่วนเบี่ยงเบนมาตรฐาน {sigma} คะแนน "
            f"{p}สอบได้ {x} คะแนน ค่ามาตรฐานของคะแนน{p}เท่ากับเท่าใด",
            f"น้ำหนักของนักเรียนชั้นหนึ่งมีค่าเฉลี่ย {mu} กิโลกรัม ส่วนเบี่ยงเบนมาตรฐาน {sigma} กิโลกรัม "
            f"{p}หนัก {x} กิโลกรัม ค่ามาตรฐานของน้ำหนัก{p}เท่ากับเท่าใด",
        ))
        return MathDraw("", str(z), prompt=prompt,
                        distractors=[str(-z), str(z * sigma * sigma),
                                     str((x - mu) * sigma)])


@question_type("math.z_score_from_value", display_name={"th": "หาค่าข้อมูลจากคะแนนมาตรฐาน"},
               level={"th": "ม.6"}, topic="ค่ามาตรฐาน")
class ZScoreFromValue(MathType):
    """Run the standardization backwards: x = μ + zσ."""

    def expr(self, rng: Random, mean_hi: int = 80, sd_hi: int = 12):
        mean = rng.randrange(20, mean_hi, 5)
        sd = rng.randint(2, sd_hi)
        z = rng.choice([-2, -1, 1, 2, 3])
        return MathDraw(
            rf"\mu = {mean}, \quad \sigma = {sd}, \quad z = {z}",
            str(mean + z * sd), prompt="จงหาค่าข้อมูล x ที่มีคะแนนมาตรฐานนี้",
            distractors=[str(mean - z * sd), str(mean + z), str(z * sd)])


@question_type("math.z_score_compare", display_name={"th": "เปรียบเทียบด้วยคะแนนมาตรฐาน"},
               level={"th": "ม.6"}, topic="ค่ามาตรฐาน")
class ZScoreCompare(ChoiceType):
    """The whole point of a z-score: comparing scores from different tests."""

    _PAIRS = (("วิชาคณิตศาสตร์", "วิชาภาษาอังกฤษ"), ("การวิ่ง 100 เมตร", "การกระโดดไกล"),
              ("การสอบกลางภาค", "การสอบปลายภาค"), ("วิชาฟิสิกส์", "วิชาเคมี"))

    def compose(self, rng: Random):
        m1, s1 = rng.randrange(50, 80, 5), rng.choice([2, 4, 5, 10])
        m2, s2 = rng.randrange(50, 80, 5), rng.choice([2, 4, 5, 10])
        z1 = rng.choice([1, 2, 3])
        z2 = rng.choice([z for z in (1, 2, 3) if z != z1])
        # The raw scores are arranged to point the other way whenever they can.
        x1, x2 = m1 + z1 * s1, m2 + z2 * s2
        a, b = rng.choice(self._PAIRS)
        better = a if z1 > z2 else b
        stem = (f"นักเรียนคนหนึ่งได้คะแนน{a} {x1} คะแนน "
                f"(ค่าเฉลี่ย {m1} ส่วนเบี่ยงเบนมาตรฐาน {s1}) "
                f"และคะแนน{b} {x2} คะแนน "
                f"(ค่าเฉลี่ย {m2} ส่วนเบี่ยงเบนมาตรฐาน {s2}) "
                "เมื่อเทียบกับกลุ่ม นักเรียนทำได้ดีกว่าในด้านใด")
        other = b if better == a else a
        return stem, better, [other, "ทั้งสองด้านเท่ากัน", "เปรียบเทียบไม่ได้"]


@question_type("math.z_score_word_m6", display_name={"th": "โจทย์ปัญหาค่ามาตรฐาน"},
               level=M6, topic="ค่ามาตรฐาน")
class ZScoreWordM6(WordProblem):
    def expr(self, rng: Random):
        mean, sd = rng.randrange(40, 80, 5), rng.choice((4, 5, 8, 10, 12))
        z = rng.choice((-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5))
        x = mean + z * sd
        if x != int(x):
            z = int(z) or 1
            x = mean + z * sd
        x = int(x)
        p = rng.choice(_story.NAMES)
        if rng.random() < 0.5:
            return MathDraw("", str(x),
                            prompt=(f"คะแนนสอบมีค่าเฉลี่ย {mean} และส่วนเบี่ยงเบนมาตรฐาน {sd} ถ้า{p}ได้ค่ามาตรฐาน "
                                    f"{z:g} {p}ได้คะแนนเท่าใด"),
                            # z · s alone, and mean − z · s.
                            distractors=_story.keep(int(z * sd), int(mean - z * sd), mean + int(z),
                                                    answer=x, lo=-999))
        return MathDraw("", str(sd),
                        prompt=(f"คะแนนสอบมีค่าเฉลี่ย {mean} {p}ได้ {x} คะแนน คิดเป็นค่ามาตรฐาน {z:g} "
                                f"ส่วนเบี่ยงเบนมาตรฐานของคะแนนเท่ากับเท่าใด"),
                        distractors=_story.keep(abs(x - mean), int(abs(x - mean) * abs(z)) or sd + 1, sd * 2,
                                                answer=sd, lo=1))

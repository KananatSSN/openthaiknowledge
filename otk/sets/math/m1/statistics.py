"""สถิติ

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.1/1

Sets moved here from: math, math_data, math_m1, math_pictures_hi.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_data import _seq
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_m1 import LEVEL, NL
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_hi import DOUBLE_BARS

PROVENANCE = Provenance("original")


_STAT_TOPIC = "สถิติ"


_LETTERS = "ABCDE"


_DB_CONTEXTS = (
    ("จำนวนนักเรียนที่ชอบกีฬาแต่ละชนิด", "นักเรียนชาย", "นักเรียนหญิง",
     ("ฟุตบอล", "วอลเลย์บอล", "แบดมินตัน", "ว่ายน้ำ", "บาสเกตบอล"), "คน"),
    ("จำนวนหนังสือที่ห้องสมุดให้ยืมในแต่ละวัน", "สัปดาห์ที่ 1", "สัปดาห์ที่ 2",
     ("วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์"), "เล่ม"),
    ("ยอดขายไอศกรีมแต่ละรส", "เดือนมีนาคม", "เดือนเมษายน",
     ("วานิลลา", "ช็อกโกแลต", "สตรอว์เบอร์รี", "มะพร้าว", "ชาไทย"), "ถ้วย"),
)


DB_ALT = "แผนภูมิแท่งเปรียบเทียบ แต่ละกลุ่มมีแท่งสีฟ้าและแท่งสีส้ม"


@question_type("math.mode_from_data",
               display_name={"th": "ฐานนิยมจากชุดข้อมูล"}, level={"th": "ม.1"},
               topic="สถิติ")
class ModeFromData(WordProblem):
    def expr(self, rng: Random):
        v = rng.randint(1, 9)
        others = rng.sample([x for x in range(1, 10) if x != v], 3)
        data = [v, v] + others
        rng.shuffle(data)
        listed = ", ".join(map(str, data))
        prompt = rng.choice((
            f"จากข้อมูล {listed} ค่าที่พบบ่อยที่สุด (ฐานนิยม) คือเท่าใด?",
            f"คะแนนสอบย่อย (เต็ม 10) ของนักเรียน 5 คน คือ {listed} ฐานนิยมของคะแนนคือเท่าใด",
            f"จำนวนแก้วน้ำที่นักเรียน 5 คนดื่มในวันหนึ่ง คือ {listed} แก้ว ฐานนิยมคือเท่าใด",
            f"จำนวนหนังสือที่นักเรียน 5 คนอ่านในเดือนนี้ คือ {listed} เล่ม ฐานนิยมคือเท่าใด",
        ))
        return MathDraw("", str(v), prompt=prompt,
                        distractors=[str(max(data)), str(min(data)),
                                     str(sorted(others)[1])])


@question_type("math.frequency_table_m1",
               display_name={"th": "อ่านตารางแจกแจงความถี่"},
               level=LEVEL, topic=_STAT_TOPIC)
class FrequencyTableM1(WordProblem):
    def expr(self, rng: Random):
        scores = sorted(rng.sample(range(4, 11), 5))
        freq = [rng.randint(1, 12) for _ in scores]
        while freq.count(max(freq)) > 1:
            freq = [rng.randint(1, 12) for _ in scores]
        lines = ["ตารางแจกแจงความถี่ของคะแนนสอบย่อย (เต็ม 10 คะแนน)", "คะแนน | จำนวนนักเรียน (ความถี่)"]
        lines += [f"{s} | {f}" for s, f in zip(scores, freq)]
        table = NL.join(lines)
        kind = rng.randrange(3)
        if kind == 0:
            mode = scores[freq.index(max(freq))]
            return MathDraw("", str(mode), prompt=f"{table}{NL}ฐานนิยมของคะแนนคือเท่าใด",
                            # The largest frequency instead of its score.
                            distractors=_story.keep(max(freq), max(scores), scores[len(scores) // 2],
                                                    answer=mode, lo=0))
        if kind == 1:
            return MathDraw("", str(sum(freq)), prompt=f"{table}{NL}มีนักเรียนทั้งหมดกี่คน",
                            distractors=_story.keep(sum(scores), len(scores), sum(freq) + 1,
                                                    answer=sum(freq), lo=1))
        cut = scores[2]
        ans = sum(f for s, f in zip(scores, freq) if s >= cut)
        return MathDraw("", str(ans),
                        prompt=f"{table}{NL}นักเรียนที่ได้คะแนนตั้งแต่ {cut} คะแนนขึ้นไปมีกี่คน",
                        distractors=_story.keep(sum(f for s, f in zip(scores, freq) if s > cut),
                                                sum(freq) - ans, ans + 1, answer=ans, lo=0))


@question_type("math.double_bar_chart_m1", display_name={"th": "อ่านแผนภูมิแท่งเปรียบเทียบ"},
               level={"th": "ม.1"}, topic="สถิติ")
class DoubleBarChartM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(DOUBLE_BARS)
        title, blue, orange, cats, unit = rng.choice(_DB_CONTEXTS)
        n = len(c.first)
        names = cats[:n]
        key = " ".join(f"{_LETTERS[i]} = {names[i]}" for i in range(n))
        lead = text(f"แผนภูมิแท่งแสดง{title} (แท่งสีฟ้า = {blue} แท่งสีส้ม = {orange}; {key})")
        img = image(c.asset_id, alt=DB_ALT)
        ask = rng.randrange(3)
        if ask == 0:
            i = rng.randrange(n)
            series, values, other = ((blue, c.first, c.second) if rng.random() < 0.5
                                     else (orange, c.second, c.first))
            v = values[i]
            return _math_q([lead, text(f"{series}ของ{names[i]}มีกี่{unit}"), img], str(v),
                           _near(v, other[i], v + 5, v - 5, values[i] + other[i], lo=1), self.topic)
        if ask == 1:
            i = rng.randrange(n)
            diff = abs(c.first[i] - c.second[i])
            if diff == 0:
                i = max(range(n), key=lambda j: abs(c.first[j] - c.second[j]))
                diff = abs(c.first[i] - c.second[i])
            return _math_q([lead, text(f"ใน{names[i]} {blue}กับ{orange}ต่างกันกี่{unit}"), img],
                           str(diff), _near(diff, c.first[i] + c.second[i], c.first[i], c.second[i],
                                            diff + 5, lo=1), self.topic)
        totals = [a + b for a, b in zip(c.first, c.second)]
        best = max(range(n), key=lambda j: totals[j])
        if totals.count(totals[best]) > 1:
            return _math_q([lead, text(f"{blue}รวมทุกกลุ่มมีกี่{unit}"), img], str(sum(c.first)),
                           _near(sum(c.first), sum(c.second), sum(totals), max(c.first), lo=1),
                           self.topic)
        # The tallest single bar rather than the tallest pair.
        tallest = max(range(n), key=lambda j: max(c.first[j], c.second[j]))
        wrongs = [names[tallest]] + [names[j] for j in range(n) if j not in (best, tallest)]
        return _text_q([lead, text(f"{blue}และ{orange}รวมกันแล้ว กลุ่มใดมีจำนวนมากที่สุด"), img],
                       names[best], [w for w in dict.fromkeys(wrongs) if w != names[best]]
                       + ["มีเท่ากันทุกกลุ่ม"], self.topic)


@question_type("math.mean_from_data", display_name={"th": "ค่าเฉลี่ยเลขคณิต"},
               level={"th": "ม.1"}, topic="สถิติ")
class MeanFromData(MathType):
    def expr(self, rng: Random, count_lo: int = 4, count_hi: int = 8,
             value_hi: int = 40):
        n = rng.randint(count_lo, count_hi)
        # Build around a whole mean so the answer is not a repeating decimal.
        mean = rng.randint(5, value_hi)
        deltas = [rng.randint(-6, 6) for _ in range(n - 1)]
        data = [mean + d for d in deltas] + [mean - sum(deltas)]
        rng.shuffle(data)
        return MathDraw(
            _seq(data), str(mean), prompt="จงหาค่าเฉลี่ยเลขคณิตของข้อมูลชุดนี้",
            distractors=[str(sum(data)), str(sorted(data)[n // 2]),
                         str(mean + 1)])


@question_type("math.mean_missing_value_m1",
               display_name={"th": "หาข้อมูลที่หายไปจากค่าเฉลี่ย"},
               level=LEVEL, topic=_STAT_TOPIC)
class MeanMissingValueM1(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 7)
        mean = rng.randint(40, 90)
        data = [mean + rng.randint(-15, 15) for _ in range(n - 1)]
        missing = n * mean - sum(data)
        if not 0 <= missing <= 100:
            return self.expr(rng)
        p = rng.choice(_story.NAMES)
        return MathDraw("", str(missing),
                        prompt=(f"{p}สอบ {n} วิชา ได้คะแนนเฉลี่ย {mean} คะแนน คะแนน {n - 1} วิชาแรกคือ "
                                f"{', '.join(map(str, data))} วิชาสุดท้ายได้กี่คะแนน"),
                        # Averaging what is known, or dividing the total by n − 1.
                        distractors=_story.keep(round(sum(data) / (n - 1)), mean,
                                                n * mean - sum(data[:-1]), missing + n,
                                                answer=missing, lo=0))

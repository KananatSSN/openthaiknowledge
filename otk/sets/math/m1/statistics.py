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


# ── More statistics (2026-11): pie charts, a line of values over time, statistical questions, kinds of data
# and the chart that suits them, and pictographs ──

from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402


@question_type("math.pie_chart_m1", display_name={"th": "แผนภูมิวงกลม"},
               level=LEVEL, topic=_STAT_TOPIC)
class PieChartM1(WordProblem):
    """A share p% of the whole is p% of 360° and p% of the total."""

    def expr(self, rng: Random):
        pct = rng.choice((5, 10, 15, 20, 25, 30, 35, 40, 45, 50))
        kind = rng.randrange(3)
        if kind == 0:
            right = pct * 360 // 100
            return MathDraw("", str(right), prompt=(f"ในแผนภูมิวงกลม นักเรียนที่ชอบกีฬาฟุตบอลคิดเป็นร้อยละ {pct} "
                                                   f"ส่วนนี้มีมุมที่จุดศูนย์กลางกี่องศา"),
                            distractors=_story.keep(pct, 360 - right, pct * 180 // 100, right + 10, answer=right, lo=1))
        if kind == 1:
            angle = pct * 360 // 100
            return MathDraw("", str(pct), prompt=(f"ในแผนภูมิวงกลม ส่วนที่แทนนักเรียนที่ชอบว่ายน้ำมีมุมที่จุดศูนย์กลาง "
                                                 f"{angle} องศา คิดเป็นร้อยละเท่าใด"),
                            distractors=_story.keep(angle, 100 - pct, angle // 2, pct + 5, answer=pct, lo=1, hi=100))
        total = rng.choice((200, 400, 500, 600, 800, 1000))
        right = total * pct // 100
        return MathDraw("", str(right), prompt=(f"นักเรียน {total} คน ในแผนภูมิวงกลมส่วนที่ชอบวิชาคณิตศาสตร์คิดเป็น"
                                               f"ร้อยละ {pct} มีนักเรียนที่ชอบวิชาคณิตศาสตร์กี่คน"),
                        distractors=_story.keep(pct, total - right, total * pct // 360 if total * pct % 360 == 0 else right + 10,
                                                right * 2, answer=right, lo=1))


@question_type("math.monthly_values_m1", display_name={"th": "อ่านข้อมูลที่เปลี่ยนแปลงตามเวลา"},
               level=LEVEL, topic=_STAT_TOPIC)
class MonthlyValuesM1(WordProblem):
    """Changes between neighbouring months, as a line graph shows them."""

    _MONTHS = ("ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.")

    def expr(self, rng: Random):
        while True:
            values = [rng.randint(10, 60) for _ in range(5)]
            changes = [b - a for a, b in zip(values, values[1:])]
            if len(set(changes)) == 4 and max(changes) > 0:
                break
        listed = ", ".join(f"{m} {v}" for m, v in zip(self._MONTHS, values))
        if rng.random() < 0.5:
            right = max(changes)
            prompt = f"ยอดขายรายเดือน (ชิ้น): {listed} ยอดขายเพิ่มขึ้นมากที่สุดระหว่างสองเดือนติดกันกี่ชิ้น"
            # The whole spread; the largest value; the biggest drop.
            return MathDraw("", str(right), prompt=prompt,
                            distractors=_story.keep(max(values) - min(values), max(values), abs(min(changes)),
                                                    right + 2, answer=right, lo=1))
        a, b = sorted(rng.sample(range(5), 2))
        while values[a] == values[b]:
            a, b = sorted(rng.sample(range(5), 2))
        right = abs(values[b] - values[a])
        more = "มากกว่า" if values[b] > values[a] else "น้อยกว่า"
        prompt = (f"ยอดขายรายเดือน (ชิ้น): {listed} ยอดขายเดือน {self._MONTHS[b]}{more}เดือน "
                  f"{self._MONTHS[a]} กี่ชิ้น")
        # The two added; one month's value; the change from the month before.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(values[a] + values[b], values[b], abs(changes[b - 1]), right + 5,
                                                answer=right, lo=1))


@question_type("math.statistical_question_m1", display_name={"th": "คำถามทางสถิติ"},
               level=LEVEL, topic=_STAT_TOPIC)
class StatisticalQuestionM1(ConceptBankType):
    """A statistical question expects answers that vary, so data must be collected."""

    ITEMS = [
        Concept("ข้อใดเป็นคำถามทางสถิติ", "นักเรียนห้อง ม.1/1 แต่ละคนสูงเท่าใด",
                ("ตอนนี้ฉันสูงกี่เซนติเมตรเมื่อวัดด้วยตลับเมตร", "โรงเรียนของเราตั้งอยู่ที่จังหวัดใดของประเทศไทย",
                 "วันนี้เป็นวันที่เท่าใดของเดือนพฤศจิกายน")),
        Concept("คำถามใดต่อไปนี้ต้องเก็บข้อมูลจากหลายคนจึงจะตอบได้", "นักเรียนในโรงเรียนใช้เวลาเดินทางมาโรงเรียนกี่นาที",
                ("ครูประจำชั้นของห้อง ม.1/1 ชื่ออะไรและสอนวิชาใด", "ห้องเรียนของเรามีประตูและหน้าต่างอย่างละกี่บาน",
                 "เมื่อวานนี้ที่โรงเรียนของเรามีฝนตกหรือไม่")),
        Concept("ข้อใดไม่เป็นคำถามทางสถิติ", "พ่อของฉันอายุเท่าใดในปีนี้",
                ("ผู้ปกครองของนักเรียนในห้องอายุเท่าใดบ้าง", "นักเรียนแต่ละคนชอบผลไม้ชนิดใด",
                 "แต่ละครอบครัวในหมู่บ้านมีสมาชิกกี่คน")),
        Concept("คำถามทางสถิติแตกต่างจากคำถามทั่วไปอย่างไร", "คาดว่าคำตอบจะแตกต่างกันจึงต้องเก็บรวบรวมข้อมูล",
                ("มีคำตอบที่ถูกต้องเพียงคำตอบเดียวเสมอไม่ว่าจะถามใคร", "ต้องถามเป็นตัวเลขเท่านั้นและห้ามถามเป็นข้อความ",
                 "ตอบได้ทันทีจากความรู้ของตนเองโดยไม่ต้องเก็บข้อมูล")),
    ]


@question_type("math.data_display_m1", display_name={"th": "ชนิดของข้อมูลและการนำเสนอที่เหมาะสม"},
               level=LEVEL, topic=_STAT_TOPIC)
class DataDisplayM1(ConceptBankType):
    ITEMS = [
        Concept("ข้อมูลอุณหภูมิในแต่ละวันตลอดหนึ่งเดือน ควรนำเสนอด้วยวิธีใด", "กราฟเส้น",
                ("แผนภูมิวงกลม", "แผนภูมิรูปภาพ", "ตารางคำศัพท์")),
        Concept("ข้อมูลร้อยละของค่าใช้จ่ายแต่ละประเภทในหนึ่งเดือน ควรนำเสนอด้วยวิธีใด", "แผนภูมิวงกลม",
                ("กราฟเส้น", "แผนภาพจุด", "แผนภาพต้น-ใบ")),
        Concept("ข้อมูลจำนวนนักเรียนชายและหญิงของแต่ละห้อง ควรนำเสนอด้วยวิธีใด", "แผนภูมิแท่งเปรียบเทียบ",
                ("กราฟเส้น", "แผนภูมิวงกลม", "แผนภาพจุด")),
        Concept("ข้อมูลใดเป็นข้อมูลเชิงคุณภาพ", "สีที่นักเรียนชอบ",
                ("ความสูงของนักเรียน", "จำนวนพี่น้องของนักเรียน", "คะแนนสอบของนักเรียน")),
        Concept("ข้อมูลใดเป็นข้อมูลเชิงปริมาณ", "น้ำหนักของนักเรียน",
                ("กรุ๊ปเลือดของนักเรียน", "กีฬาที่นักเรียนชอบ", "จังหวัดที่นักเรียนเกิด")),
    ]


@question_type("math.pictograph_m1", display_name={"th": "แผนภูมิรูปภาพ"},
               level=LEVEL, topic=_STAT_TOPIC)
class PictographM1(WordProblem):
    """One picture stands for k; half a picture for k/2."""

    def expr(self, rng: Random):
        k = rng.choice((2, 4, 6, 10, 20, 50))  # even, so half a picture is a whole number of people
        whole = rng.randint(2, 9)
        half = rng.random() < 0.5
        right = whole * k + (k // 2 if half else 0)
        pictures = f"{whole} รูปครึ่ง" if half else f"{whole} รูป"
        prompt = (f"ในแผนภูมิรูปภาพ รูป 1 รูปแทนนักเรียน {k} คน ถ้าห้อง ก มีรูปทั้งหมด {pictures} "
                  f"ห้อง ก มีนักเรียนกี่คน")
        # The pictures counted as people; the half counted as a whole; the half left out.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(whole, (whole + 1) * k, whole * k, right + k, answer=right, lo=1))

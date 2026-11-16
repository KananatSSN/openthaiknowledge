"""การวัด

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.2/*

Sets moved here from: math, math_gaps_primary, math_measure_pictures, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_measure_pictures import SCALES
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


SCALE_ALT = "ภาพหน้าปัดเครื่องชั่งสปริง มีเข็มชี้"


def _kg_khit(kg: int, khit: int) -> str:
    if kg == 0:
        return f"{khit} ขีด"
    return f"{kg} กิโลกรัม {khit} ขีด" if khit else f"{kg} กิโลกรัม"


@question_type("math.convert_length_p2",
               display_name={"th": "แปลงเมตรเป็นเซนติเมตร"}, level={"th": "ป.2"}, topic="การวัด")
class ConvertLengthP2(WordProblem):
    def expr(self, rng: Random):
        m = rng.randint(1, 9)
        cm = rng.choice([0, 0, rng.randint(5, 95)])
        ans = 100 * m + cm
        said = f"{m} เมตร" + (f" {cm} เซนติเมตร" if cm else "")
        thing = rng.choice(("", "ผ้าผืนหนึ่งยาว ", "เชือกเส้นหนึ่งยาว ", "โต๊ะตัวหนึ่งยาว ",
                            "ต้นไม้ต้นหนึ่งสูง "))
        prompt = (f"{thing}{said} คิดเป็นกี่เซนติเมตร?" if thing
                  else f"{said} เท่ากับกี่เซนติเมตร?")
        # Treating a metre as 10 cm, and writing the parts side by side.
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(10 * m + cm, 1000 * m + cm, m + cm,
                                                int(f"{m}{cm}") if cm else 100 * m + 100,
                                                answer=ans))


@question_type("math.scale_picture_p2", display_name={"th": "อ่านน้ำหนักจากหน้าปัดเครื่องชั่ง"},
               level={"th": "ป.2"}, topic="การวัด")
class ScalePictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SCALES)
        right = _kg_khit(s.kg, s.khit)
        # The next kilogram mark; one small mark off either way; ขีด read as kilograms.
        wrongs = [_kg_khit(s.kg + 1, s.khit), _kg_khit(s.kg, (s.khit + 1) % 10),
                  _kg_khit(s.kg, (s.khit - 1) % 10), _kg_khit(s.khit, s.kg), _kg_khit(s.kg + 1, 0)]
        return _text_q([text("เครื่องชั่งอ่านน้ำหนักได้เท่าใด (1 กิโลกรัม มี 10 ขีด)"),
                        image(s.asset_id, alt=SCALE_ALT)],
                       right, [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.convert_weight_p2",
               display_name={"th": "แปลงกิโลกรัมเป็นขีด"}, level={"th": "ป.2"}, topic="การวัด")
class ConvertWeightP2(WordProblem):
    def expr(self, rng: Random):
        kg = rng.randint(1, 9)
        khit = rng.choice([0, rng.randint(1, 9)])
        ans = 10 * kg + khit
        said = f"{kg} กิโลกรัม" + (f" {khit} ขีด" if khit else "")
        thing = rng.choice(("", "ส้มหนัก ", "เนื้อหมูหนัก ", "ข้าวสารหนัก ", "แตงโมหนัก "))
        prompt = (f"{thing}{said} คิดเป็นกี่ขีด?" if thing
                  else f"{said} เท่ากับกี่ขีด?")
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(100 * kg + khit, kg + khit, 1000 * kg + khit,
                                                10 * kg + 10, answer=ans))


@question_type("math.capacity_litre_p2",
               display_name={"th": "ปริมาตรและความจุเป็นลิตร"},
               level={"th": "ป.2"}, topic="การวัด")
class CapacityLitreP2(WordProblem):
    _BIG = ("ถังน้ำ", "หม้อ", "โอ่ง", "กะละมัง", "ตู้ปลา")
    _SMALL = ("ขวด", "เหยือก", "กระติก", "แก้วตวง")

    def expr(self, rng: Random):
        big, small = rng.choice(self._BIG), rng.choice(self._SMALL)
        kind = rng.randrange(4)
        if kind == 0:
            a, b = rng.randint(12, 60), rng.randint(2, 9)
            return MathDraw("", str(a - b), prompt=(
                f"{big}ใบหนึ่งจุน้ำได้ {a} ลิตร {small}ใบหนึ่งจุน้ำได้ {b} ลิตร "
                f"{big}จุน้ำได้มากกว่า{small}กี่ลิตร"),
                distractors=_story.keep(a + b, a - b + 1, a, answer=a - b, lo=1))
        if kind == 1:
            each, n = rng.randint(2, 5), rng.randint(3, 9)
            return MathDraw("", str(each * n), prompt=(
                f"เทน้ำจาก{small}ที่มีน้ำเต็ม {n} ใบ ใบละ {each} ลิตร ลงใน{big} "
                f"{big}มีน้ำกี่ลิตร"),
                distractors=_story.keep(each + n, each * (n - 1), each * n + each,
                                        answer=each * n, lo=1))
        if kind == 2:
            each, n = rng.randint(2, 5), rng.randint(3, 9)
            total = each * n
            return MathDraw("", str(n), prompt=(
                f"{big}จุน้ำได้ {total} ลิตร ใช้{small}ที่จุ {each} ลิตร ตักน้ำใส่ "
                f"ต้องตักกี่ครั้ง{big}จึงจะเต็มพอดี"),
                distractors=_story.keep(total - each, n + 1, each, total, answer=n, lo=1))
        full, used, more = rng.randint(10, 40), rng.randint(2, 9), rng.randint(2, 9)
        left = full - used + more
        return MathDraw("", str(left), prompt=(
            f"{big}มีน้ำ {full} ลิตร ใช้ไป {used} ลิตร แล้วเติมน้ำเพิ่มอีก {more} ลิตร "
            f"ตอนนี้{big}มีน้ำกี่ลิตร"),
            distractors=_story.keep(full - used - more, full + used + more, full - used,
                                    answer=left, lo=1))


@question_type("math.length_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาความยาว (เมตร เซนติเมตร)"},
               level=LEVEL, topic="การวัด")
class LengthWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        p, q = _story.names(rng)
        m1, c1 = rng.randint(1, 4), rng.randint(5, 95)
        m2, c2 = rng.randint(1, 4), rng.randint(5, 95)
        x, y = 100 * m1 + c1, 100 * m2 + c2
        kind = rng.randrange(6)
        if kind == 3:
            more = rng.randint(5, 60)
            return MathDraw("", str(x + more),
                            prompt=(f"{p}กระโดดไกลได้ {m1} เมตร {c1} เซนติเมตร {q}กระโดดได้ไกลกว่า{p} "
                                    f"{more} เซนติเมตร {q}กระโดดได้ไกลกี่เซนติเมตร"),
                            distractors=_story.keep(x - more, m1 + c1 + more, x + more + 100,
                                                    answer=x + more, lo=1))
        if kind == 4:
            n, each = rng.randint(2, 5), rng.randint(20, 95)
            return MathDraw("", str(n * each),
                            prompt=(f"{p}ต่อริบบิ้น {n} เส้น ยาวเส้นละ {each} เซนติเมตร โดยไม่ซ้อนกัน "
                                    f"ได้ริบบิ้นยาวกี่เซนติเมตร"),
                            distractors=_story.keep(n + each, each * (n - 1), n * each + 10,
                                                    answer=n * each, lo=1))
        if kind == 5:
            whole = rng.randint(2, 9)
            walked = rng.randint(30, 100 * whole - 10)
            return MathDraw("", str(100 * whole - walked),
                            prompt=(f"ทางเดินไปห้องสมุดยาว {whole} เมตร {p}เดินไปแล้ว {walked} เซนติเมตร "
                                    f"ต้องเดินอีกกี่เซนติเมตรจึงจะถึง"),
                            distractors=_story.keep(100 * whole + walked, abs(whole - walked),
                                                    100 * whole - walked + 100,
                                                    answer=100 * whole - walked, lo=1))
        if kind == 0:
            ans = x + y
            return MathDraw("", str(ans),
                            prompt=(f"ผ้าผืนแรกยาว {m1} เมตร {c1} เซนติเมตร ผืนที่สองยาว {m2} "
                                    f"เมตร {c2} เซนติเมตร ผ้าสองผืนยาวรวมกันกี่เซนติเมตร"),
                            distractors=_story.keep(10 * (m1 + m2) + c1 + c2, ans - 100,
                                                    ans + 100, abs(x - y), answer=ans))
        if kind == 1:
            # Children's heights: a little over a metre.
            big = rng.randint(115, 160)
            small = rng.randint(100, big - 3)
            hb, hs = divmod(big, 100)
            return MathDraw("", str(big - small),
                            prompt=(f"{p}สูง {hb} เมตร {hs} เซนติเมตร {q}สูง {small} "
                                    f"เซนติเมตร {p}สูงกว่า{q}กี่เซนติเมตร"),
                            distractors=_story.keep(abs(10 * hb + hs - small), big + small,
                                                    big - small + 100, answer=big - small, lo=1))
        whole = rng.randint(3, 9)
        cut = rng.randint(60, 100 * whole - 20)
        return MathDraw("", str(100 * whole - cut),
                        prompt=(f"เชือกยาว {whole} เมตร ตัดออกไป {cut} เซนติเมตร "
                                f"เหลือเชือกยาวกี่เซนติเมตร"),
                        distractors=_story.keep(abs(whole - cut), 10 * whole - cut if 10 * whole > cut
                                                else 100 * whole + cut, 100 * whole - cut + 100,
                                                answer=100 * whole - cut, lo=1))


@question_type("math.weight_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาน้ำหนัก (กิโลกรัม กรัม ขีด)"},
               level=LEVEL, topic="การวัด")
class WeightWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            kg, g = rng.randint(1, 5), rng.choice(range(50, 1000, 50))
            ans = 1000 * kg + g
            return MathDraw("", str(ans), prompt=f"{kg} กิโลกรัม {g} กรัม เท่ากับกี่กรัม",
                            distractors=_story.keep(100 * kg + g, kg + g, 1000 * kg + 10 * g,
                                                    answer=ans))
        if kind == 1:
            k = rng.randint(2, 9)
            return MathDraw("", str(100 * k),
                            prompt=f"{k} ขีด เท่ากับกี่กรัม (1 ขีด เท่ากับ 100 กรัม)",
                            distractors=_story.keep(10 * k, 1000 * k, k, answer=100 * k))
        if kind == 2:
            a, b = rng.sample(range(2, 10), 2)
            meat, veg = rng.sample(("เนื้อหมู", "เนื้อไก่", "กุ้ง", "ผักบุ้ง", "ถั่วฝักยาว"), 2)
            return MathDraw("", str(100 * (a + b)),
                            prompt=(f"แม่ซื้อ{meat} {a} ขีด และ{veg} {b} ขีด "
                                    f"รวมหนักกี่กรัม"),
                            distractors=_story.keep(a + b, 10 * (a + b), 1000 * (a + b),
                                                    100 * abs(a - b), answer=100 * (a + b)))
        bag = rng.randint(2, 5)
        used = rng.choice(range(100, 1000 * bag, 50))
        ans = 1000 * bag - used
        return MathDraw("", str(ans),
                        prompt=(f"{p}มีแป้ง {bag} กิโลกรัม ใช้ทำขนมไป {used} กรัม "
                                f"เหลือแป้งกี่กรัม"),
                        distractors=_story.keep(100 * bag - used if 100 * bag > used else used - bag,
                                                1000 * bag + used, ans + 100, answer=ans, lo=1))


# ── More measuring (2026-11): centimetres as metres and centimetres, the longest of lengths written two ways,
# kilograms and grams as grams, and how much longer across the two units ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402


def _m_cm(cm: int) -> str:
    m, r = divmod(cm, 100)
    return f"{m} เมตร {r} เซนติเมตร" if r else f"{m} เมตร"


@question_type("math.cm_to_m_cm_p2", display_name={"th": "เขียนเซนติเมตรเป็นเมตรและเซนติเมตร"},
               level=LEVEL, topic="การวัด")
class CmToMCmP2(ChoiceType):
    def compose(self, rng: Random):
        m = rng.randint(1, 9)
        r = rng.choice([v for v in range(11, 100) if v % 10 and v % 10 != v // 10])
        cm = 100 * m + r
        right = f"{m} เมตร {r} เซนติเมตร"
        # Split one place off; the centimetres' digits swapped; all of it called metres.
        wrongs = [f"{cm // 10} เมตร {cm % 10} เซนติเมตร", f"{m} เมตร {r % 10}{r // 10} เซนติเมตร", f"{cm} เมตร"]
        return f"{cm} เซนติเมตร เท่ากับเท่าใด", right, wrongs


@question_type("math.longest_mixed_units_p2", display_name={"th": "ความยาวใดยาวที่สุดหรือสั้นที่สุด"},
               level=LEVEL, topic="การวัด")
class LongestMixedUnitsP2(ChoiceType):
    def compose(self, rng: Random):
        values = rng.sample(range(105, 300), 4)
        texts = []
        for v in values:
            texts.append(_m_cm(v) if rng.random() < 0.5 else f"{v} เซนติเมตร")
        most = rng.random() < 0.5
        pick = (max if most else min)(range(4), key=lambda i: values[i])
        return (f"ความยาวใด{'ยาวที่สุด' if most else 'สั้นที่สุด'}", texts[pick],
                [t for i, t in enumerate(texts) if i != pick])


@question_type("math.kg_g_to_g_p2", display_name={"th": "เปลี่ยนกิโลกรัมและกรัมเป็นกรัม"},
               level=LEVEL, topic="การวัด")
class KgGToGP2(WordProblem):
    def expr(self, rng: Random):
        kg = rng.randint(1, 9)
        g = rng.choice((50, 100, 200, 250, 300, 400, 500, 600, 750, 800))
        right = 1000 * kg + g
        # A kilogram taken as 100 grams; the numbers side by side as hundreds; the grams left out.
        return MathDraw("", str(right), prompt=f"{kg} กิโลกรัม {g} กรัม เท่ากับกี่กรัม",
                        distractors=_story.keep(100 * kg + g, kg + g, 1000 * kg, 10 * kg + g, answer=right, lo=1))


@question_type("math.length_compare_mixed_p2", display_name={"th": "ยาวกว่ากันกี่เซนติเมตร (เมตรและเซนติเมตร)"},
               level=LEVEL, topic="การวัด")
class LengthCompareMixedP2(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(150, 400)
        b = rng.randint(100, a - 10)
        right = a - b
        x, y = rng.sample(("ริบบิ้น", "เชือก", "ไม้ไผ่", "ผ้า"), 2)
        prompt = (f"{x}ยาว {_m_cm(a)} {y}ยาว {b} เซนติเมตร {x}ยาวกว่า{y}กี่เซนติเมตร")
        # The metres taken as ten centimetres; added; the metres ignored.
        m, r = divmod(a, 100)
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(10 * m + r - b), a + b, abs(r - b), right + 10,
                                                answer=right, lo=1))


@question_type("math.mixed_length_statement_p2", display_name={"th": "เลือกข้อความเปรียบเทียบความยาวต่างหน่วย"},
               level=LEVEL, topic="การวัด")
class MixedLengthStatementP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-2/4176-2-2567-2-2.pdf, ข้อ 2, 4, 7, 10",))

    def compose(self, rng: Random):
        a, b = rng.sample(range(101, 501), 2)
        m, cm = divmod(a, 100)
        x, y = ("ริบบิ้นสีแดง", "ริบบิ้นสีฟ้า") if a > b else ("ริบบิ้นสีฟ้า", "ริบบิ้นสีแดง")
        gap = abs(a - b)
        return (f"ริบบิ้นสีแดงยาว {m} เมตร {cm} เซนติเมตร ริบบิ้นสีฟ้ายาว {b} เซนติเมตร ข้อใดถูกต้อง",
                f"{x}ยาวกว่า{y} {gap} เซนติเมตร",
                [f"{y}ยาวกว่า{x} {gap} เซนติเมตร", f"{x}ยาวกว่า{y} {a + b} เซนติเมตร",
                 f"{x}ยาวกว่า{y} {gap + 100} เซนติเมตร"])


@question_type("math.capacity_litre_ml_comparison_p2", display_name={"th": "เปรียบเทียบความจุลิตรกับมิลลิลิตร"},
               level=LEVEL, topic="การวัด")
class CapacityLitreMlComparisonP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-2/4176-2-2567-2-2.pdf, ข้อ 15",))

    def compose(self, rng: Random):
        litres = rng.randint(1, 9)
        ml = 1000 * litres + rng.choice((-500, 0, 500))
        delta = ml - 1000 * litres
        labels = ["ขวดสีแดงจุได้มากกว่า", "ขวดสีฟ้าจุได้มากกว่า", "ทั้งสองขวดจุได้เท่ากัน", "ยังเปรียบเทียบไม่ได้แม้ทราบหน่วย"]
        index = 0 if delta < 0 else 1 if delta > 0 else 2
        return (f"ขวดสีแดงจุ {litres} ลิตร ขวดสีฟ้าจุ {ml} มิลลิลิตร ข้อใดถูกต้อง "
                "(1 ลิตร เท่ากับ 1000 มิลลิลิตร)", labels[index],
                [label for i, label in enumerate(labels) if i != index])


@question_type("math.round_trip_metres_p2", display_name={"th": "หาระยะทางไปกลับจากระยะทางขาเดียว"}, level={"th": "ป.2"}, topic="การวัด")
class RoundTripMetresP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 9",))

    def compose(self,rng: Random):
        distance=rng.randint(251,999)
        return (f"บ้านถึงโรงเรียนมีระยะทาง {distance} เมตร เดินไปโรงเรียนแล้วกลับบ้านตามทางเดิม "
                "เดินรวมทั้งหมดกี่เมตร",str(2*distance),
                [str(distance),str(3*distance),str(2*distance+100)])


@question_type("math.volume_comparison_statement_p2", display_name={"th": "ตรวจข้อความเปรียบเทียบปริมาตร"}, level={"th": "ป.2"}, topic="การวัด")
class VolumeComparisonStatementP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 11",))

    def compose(self,rng: Random):
        relations=rng.sample(("มากกว่า","น้อยกว่า","เท่ากับ"),2)*2
        rng.shuffle(relations)
        bad=rng.randrange(4)
        rows=[]
        used=set()
        for i,relation in enumerate(relations):
            while True:
                a,b=rng.randint(2,15),rng.randint(2,15)
                truth=(a>b if relation=="มากกว่า" else a<b if relation=="น้อยกว่า" else a==b)
                unit=rng.choice(("ลิตร","ถ้วยตวง","ช้อนตวง"))
                label=f"{a} {unit} {relation} {b} {unit}"
                if truth==(i!=bad) and label not in used:
                    break
            used.add(label)
            rows.append(label)
        return ("ข้อใดเปรียบเทียบปริมาตรไม่ถูกต้อง ถ้วยตวงและช้อนตวงแต่ละชนิดมีขนาดเท่ากันทุกครั้ง",
                rows[bad],[label for i,label in enumerate(rows) if i!=bad])


@question_type("math.container_equivalence_p2", display_name={"th": "เปรียบเทียบความจุจากภาชนะที่ตวงได้เท่ากัน"}, level={"th": "ป.2"}, topic="การวัด")
class ContainerEquivalenceP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 12",))

    def compose(self,rng: Random):
        bottles,jug=rng.randint(2,5),rng.randint(2,5)
        count=rng.choice((bottles-1,bottles,bottles+1))
        right="น้อยกว่า" if count<bottles else "เท่ากับ" if count==bottles else "มากกว่า"
        def model(n,relation):
            return f"ขวด {n} ใบ จุ{relation}เหยือก 1 ใบ"
        wrongs=[model(count,r) for r in ("น้อยกว่า","เท่ากับ","มากกว่า") if r!=right]
        # A wrong comparison from inverting bottles per jug.
        wrongs.append(f"ขวด {count} ใบ จุเท่ากับเหยือก {bottles*count} ใบ")
        return (f"ขวดทุกใบจุเท่ากัน ขวด {bottles} ใบจุรวมเท่ากับเหยือก 1 ใบ เหยือกจุ {jug*bottles} ลิตร "
                f"ข้อความใดถูกต้องเมื่อเปรียบเทียบขวด {count} ใบกับเหยือก",model(count,right),wrongs)


@question_type("math.dry_measure_method_p2", display_name={"th": "เลือกวิธีตวงให้ตรงลักษณะของแห้ง"}, level={"th": "ป.2"}, topic="การวัด")
class DryMeasureMethodP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 13,15",))

    def compose(self,rng: Random):
        coarse=rng.choice((False,True))
        kind="ถ่านชิ้นใหญ่" if coarse else "แป้งละเอียด"
        answer="ตวงให้พูนเหนือขอบ" if coarse else "ตวงเสมอขอบแล้วปาดเรียบ"
        other="ตวงเสมอขอบแล้วปาดเรียบ" if coarse else "ตวงให้พูนเหนือขอบ"
        # Explicit classroom convention avoids treating it as a universal measurement standard.
        prompt=("กิจกรรมนี้กำหนดให้ของแห้งละเอียดตวงเสมอขอบแล้วปาดเรียบ "
                "ส่วนของแห้งหยาบชิ้นใหญ่ตวงให้พูนเหนือขอบ "
                f"หากตวง{kind}ต้องใช้วิธีใด")
        return prompt,answer,[other,"ตวงเพียงครึ่งภาชนะ","ใส่เท่าใดก็ได้โดยไม่ตรวจขอบ"]


@question_type("math.half_metre_p2", display_name={"th": "เขียนเมตรครึ่งเป็นเมตรและเซนติเมตร"}, level=LEVEL, topic="การวัด")
class HalfMetreP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 2',))

    def compose(self, rng: Random):
        whole = rng.randint(1, 9)
        if rng.choice((False, True)):
            return (f"ริบบิ้นยาว {whole} เมตรครึ่ง เท่ากับกี่เซนติเมตร", str(whole * 100 + 50),
                    [str(whole * 100 + 5), str(whole * 100 + 500), str(whole * 100)])
        return (f"เชือกยาว {whole} เมตรครึ่ง เขียนเป็นเมตรและเซนติเมตรได้อย่างไร",
                f"{whole} เมตร 50 เซนติเมตร",
                [f"{whole} เมตร 5 เซนติเมตร", f"{whole} เมตร 500 เซนติเมตร", f"{whole} เมตร 0 เซนติเมตร"])


@question_type("math.unit_quantity_p2", display_name={"th": "ระบุปริมาณที่หน่วยวัดใช้บอก"}, level=LEVEL, topic="การวัด")
class UnitQuantityP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 11',))

    def compose(self, rng: Random):
        unit, right = rng.choice((("ลิตร", "ปริมาตร"), ("มิลลิลิตร", "ปริมาตร"),
                                 ("เมตร", "ความยาว"), ("เซนติเมตร", "ความยาว"),
                                 ("กรัม", "น้ำหนัก"), ("กิโลกรัม", "น้ำหนัก"),
                                 ("นาที", "เวลา"), ("ชั่วโมง", "เวลา")))
        return (f"{unit}เป็นหน่วยที่ใช้บอกปริมาณชนิดใด", right,
                [x for x in ("ปริมาตร", "ความยาว", "น้ำหนัก", "เวลา") if x != right])


@question_type("math.calibrated_volume_tools_p2", display_name={"th": "แยกเครื่องตวงที่มีความจุกำกับออกจากเครื่องมือชนิดอื่น"}, level=LEVEL, topic="การวัด")
class CalibratedVolumeToolsP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 13',))

    def compose(self, rng: Random):
        calibrated = ("กระบอกตวงมีขีดมิลลิลิตร", "ช้อนตวงระบุความจุมิลลิลิตร", "ถ้วยตวงมีขีดมิลลิลิตร", "เหยือกตวงมีขีดลิตร")
        other = ("แก้วไม่ระบุความจุ", "ขวดไม่ระบุความจุ", "เครื่องชั่งมีขีดกรัม", "ไม้บรรทัดมีขีดเซนติเมตร")
        good = rng.sample(calibrated, 3)
        wrongs = []
        for bad in rng.sample(other, 3):
            group = rng.sample(calibrated, 2) + [bad]
            rng.shuffle(group)
            wrongs.append(" · ".join(group))
        return ("กลุ่มใดเป็นเครื่องตวงที่มีหน่วยความจุกำกับทุกชิ้น", " · ".join(good), wrongs)


@question_type("math.weighing_tool_precision_p2", display_name={"th": "เลือกเครื่องชั่งจากพิกัดและขีดแบ่งที่กำหนด"}, level=LEVEL, topic="การวัด")
class WeighingToolPrecisionP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 16',))

    def compose(self, rng: Random):
        mass = rng.randint(3, 15)
        step = rng.choice((1, 2, 5))
        labels = rng.sample(("ก", "ข", "ค", "ง"), 4)
        profiles = ((mass + 5, step), (mass - 1, step),
                    (mass + 10, step * 10), (mass + 20, step * 5))
        rows = [(f"เครื่องชั่ง{label}", capacity, division)
                for label, (capacity, division) in zip(labels, profiles)]
        rng.shuffle(rows)
        data = " · ".join(f"{label} ชั่งได้ไม่เกิน {cap} กรัม ขีดแบ่ง {div} กรัม" for label, cap, div in rows)
        right = next(label for label, cap, div in rows if cap >= mass and div <= step)
        return (f"ต้องชั่งของประมาณ {mass} กรัม โดยใช้ขีดแบ่งไม่เกิน {step} กรัม "
                f"ข้อมูลเครื่องชั่ง: {data} ควรเลือกเครื่องใด", right,
                [label for label, _, _ in rows if label != right])


@question_type("math.weight_threshold_p2", display_name={"th": "เลือกน้ำหนักที่เกินหรือต่ำกว่าเกณฑ์ต่างหน่วย"}, level=LEVEL, topic="การวัด")
class WeightThresholdP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 18',))

    def compose(self, rng: Random):
        threshold = 100 * rng.randint(2, 9)
        more = rng.choice((False, True))
        # Two exactly equal alternatives expose > versus >= without a second answer.
        equal = [f"{threshold // 100} ขีด", f"{threshold} กรัม"]
        high, low = threshold + rng.choice((100, 200, 500)), threshold - 100
        right = f"{high if more else low} กรัม"
        wrong = f"{low if more else high} กรัม"
        return (f"กำหนดให้ 1 ขีด เท่ากับ 100 กรัม น้ำหนักใด{'หนักกว่า' if more else 'เบากว่า'} {threshold} กรัม",
                right, equal + [wrong])


@question_type("math.weight_extreme_p2", display_name={"th": "หาน้ำหนักมากที่สุดหรือน้อยที่สุดจากกรัมขีดและกิโลกรัมครึ่ง"}, level=LEVEL, topic="การวัด")
class WeightExtremeP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/mathematics/level/primary-2/4167-2-2565-2-2.pdf, ข้อ 19–20',))

    def compose(self, rng: Random):
        half_kg = rng.randint(1, 4)
        values = rng.sample([n for n in range(1, 60) if n != 10 * half_kg + 5], 3)
        amounts = [100 * n for n in values] + [1000 * half_kg + 500]
        labels = [f"{values[0] * 100} กรัม", f"{values[1]} ขีด",
                  f"{values[2] // 10} กิโลกรัม {values[2] % 10 * 100} กรัม", f"{half_kg} กิโลกรัมครึ่ง"]
        maximum = rng.choice((False, True))
        pick = (max if maximum else min)(range(4), key=lambda i: amounts[i])
        return (f"น้ำหนักใด{'หนักที่สุด' if maximum else 'เบาที่สุด'} (1 ขีด เท่ากับ 100 กรัม)",
                labels[pick], [label for i, label in enumerate(labels) if i != pick])

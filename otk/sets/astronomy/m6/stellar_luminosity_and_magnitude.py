"""ความส่องสว่างและโชติมาตรของดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/5

Sets moved here from: science_wave_c7, science_wave_f83.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled as _labelled_science_wave_c7
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c7 import LUMINOSITY_FACTS, LUMINOSITY_SCENARIOS
from otk.sets._support.science_wave_f83 import NAMES

PROVENANCE = Provenance("original")


LUMINOSITY_TOPIC = "ความส่องสว่างและโชติมาตรของดาวฤกษ์"


class Star(NamedTuple):
    """A measured star: how bright it looks, and how bright it really is."""
    name: str
    apparent: float
    absolute: float


# Every value distinct, so "which looks brightest" and "which really is
# brightest" each have one answer, and the two questions have different ones.
STARS = (
    Star("ดาว ก", -1.5, 1.4),
    Star("ดาว ข", 0.1, -5.1),
    Star("ดาว ค", 1.2, 2.7),
    Star("ดาว ง", 2.9, -0.3),
)


FIVE_STEPS = 100


EQUAL_BRIGHTNESS = "ทุกดวงสว่างเท่ากัน"


TOPIC_MAG = "ความส่องสว่างและโชติมาตรของดาวฤกษ์"


MAG_FACTS = (
    ("ความส่องสว่าง (luminosity) ของดาวฤกษ์ขึ้นกับปัจจัยใด", "ขนาด (รัศมี) และอุณหภูมิผิวของดาว",
     ("ระยะห่างจากโลกเพียงอย่างเดียว", "สีของท้องฟ้าบนโลก", "จำนวนดาวเคราะห์ที่โคจรรอบ", "ตำแหน่งของดวงจันทร์")),
    ("ความสว่างปรากฏของดาวฤกษ์ที่เห็นจากโลกขึ้นกับปัจจัยใด", "ความส่องสว่างของดาวและระยะห่างจากโลก",
     ("อุณหภูมิของโลก", "ขนาดของกล้องที่ใช้ดูเพียงอย่างเดียว", "เวลาที่ดาวขึ้น", "ชื่อของกลุ่มดาว")),
    ("โชติมาตรปรากฏมีค่าน้อยลงหมายความว่าอย่างไร", "ดาวปรากฏสว่างมากขึ้น",
     ("ดาวปรากฏสว่างน้อยลง", "ดาวอยู่ไกลขึ้นเสมอ", "ดาวมีอุณหภูมิต่ำลงเสมอ", "ดาวมีขนาดเล็กลงเสมอ")),
    ("โชติมาตรสัมบูรณ์คืออะไร", "โชติมาตรของดาวเมื่อสมมติให้อยู่ห่างจากโลก 10 พาร์เซก",
     ("โชติมาตรที่วัดได้จริงจากโลก", "โชติมาตรเมื่อดาวอยู่ห่าง 1 ปีแสง", "โชติมาตรของดวงอาทิตย์", "โชติมาตรเฉลี่ยของทุกดาว")),
    ("ดาวสองดวงมีโชติมาตรต่างกัน 5 จะมีความสว่างต่างกันกี่เท่า", "100 เท่า",
     ("5 เท่า", "25 เท่า", "10 เท่า", "1,000 เท่า")),
    ("เหตุใดดาวที่มีความส่องสว่างมากจึงอาจปรากฏสว่างน้อยกว่าดาวที่ส่องสว่างน้อย", "เพราะอยู่ไกลจากโลกมากกว่า",
     ("เพราะมีอุณหภูมิผิวสูงกว่า", "เพราะอยู่ใกล้โลกมากกว่า", "เพราะมีขนาดใหญ่กว่า", "เพราะเป็นดาวคู่")),
    ("ดาวฤกษ์สองดวงมีอุณหภูมิผิวเท่ากัน ดวงใดส่องสว่างมากกว่า", "ดวงที่มีรัศมีใหญ่กว่า",
     ("ดวงที่มีรัศมีเล็กกว่า", "ดวงที่อยู่ใกล้โลกมากกว่า", "ส่องสว่างเท่ากันเสมอ", "ดวงที่มีสีแดงกว่า")),
    ("ดาวที่มีโชติมาตรปรากฏเป็นลบ เช่น ดาวซีรีอัส มีความหมายว่าอย่างไร", "ปรากฏสว่างมากกว่าดาวโชติมาตร 0",
     ("ปรากฏสว่างน้อยกว่าดาวโชติมาตร 0", "มองไม่เห็นด้วยตาเปล่า", "เป็นดาวที่ดับไปแล้ว", "อยู่ห่างจากโลกเป็นระยะลบ")),
)


MAG_HINT = ("ความส่องสว่างขึ้นกับรัศมีและอุณหภูมิ (L ∝ R²T⁴) ความสว่างปรากฏลดลงตามระยะทางยกกำลังสอง "
            "โชติมาตรน้อยยิ่งสว่าง ต่างกัน 5 โชติมาตรสว่างต่างกัน 100 เท่า โชติมาตรสัมบูรณ์คือโชติมาตรที่ระยะ 10 พาร์เซก")


@question_type(
    "astro.star_luminosity_foundation",
    display_name={"th": "ปัจจัยที่ส่งผลต่อความส่องสว่าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=LUMINOSITY_TOPIC,
)
class StarLuminosityFoundation(QuestionType):
    """Name what luminosity depends on — the indicator's first free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LUMINOSITY_FACTS,
            hint="ความส่องสว่างขึ้นกับพื้นที่ผิวและอุณหภูมิผิว ส่วนความสว่างที่เห็นยังขึ้นกับระยะทาง",
        ), LUMINOSITY_TOPIC)


@question_type(
    "astro.magnitude_scale_foundation",
    display_name={"th": "ปัจจัยที่มีผลต่อความส่องสว่างและความหมายของโชติมาตร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class MagnitudeScaleFoundation(QuestionType):
    """Luminosity, apparent brightness, apparent and absolute magnitude."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(MAG_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_MAG, hint=MAG_HINT)


@question_type(
    "astro.star_luminosity_fluency",
    display_name={"th": "ความสัมพันธ์ระหว่างความส่องสว่างกับโชติมาตร"},
    level=UPPER_SIX, subject=SUBJECT, topic=LUMINOSITY_TOPIC,
)
class StarLuminosityFluency(QuestionType):
    """Read magnitudes and say what they mean — the indicator's second free verb.

    Magnitude runs backwards, so the answer to "which is brightest" is the
    smallest number in the table, and a difference of five is a factor of a
    hundred. Both are read off the values in the stem.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        table = " / ".join(
            f"{star.name}: โชติมาตรปรากฏ {star.apparent} "
            f"โชติมาตรสัมบูรณ์ {star.absolute}" for star in STARS)
        stem = f"ตารางโชติมาตรของดาวฤกษ์สี่ดวงเป็นดังนี้ {table} "
        draw = rng.random()
        if draw < 0.25:
            brightest = min(STARS, key=lambda star: star.apparent)
            return _labelled_science_wave_c7(
                stem=stem + "จากข้อมูลนี้ ดาวดวงใดปรากฏสว่างที่สุดเมื่อมองจากโลก",
                correct=brightest.name,
                wrongs=tuple([star.name for star in STARS if star.name != brightest.name]
                                        + [EQUAL_BRIGHTNESS]),
                hint="โชติมาตรยิ่งน้อยยิ่งสว่าง ค่าติดลบจึงสว่างที่สุด",
                topic=LUMINOSITY_TOPIC,
            )
        if draw < 0.5:
            luminous = min(STARS, key=lambda star: star.absolute)
            return _labelled_science_wave_c7(
                stem=stem + "จากข้อมูลนี้ ดาวดวงใดมีความส่องสว่างที่แท้จริงมากที่สุด",
                correct=luminous.name,
                wrongs=tuple([star.name for star in STARS if star.name != luminous.name]
                                        + [EQUAL_BRIGHTNESS]),
                hint="ความส่องสว่างที่แท้จริงอ่านจากโชติมาตรสัมบูรณ์ "
                     "และยิ่งน้อยยิ่งสว่าง",
                topic=LUMINOSITY_TOPIC,
            )
        if draw < 0.75:
            return _labelled_science_wave_c7(
                stem="ดาวฤกษ์สองดวงมีโชติมาตรต่างกัน 5 "
                     "ดวงที่โชติมาตรน้อยกว่าสว่างกว่าอีกดวงกี่เท่า",
                correct=f"ประมาณ {FIVE_STEPS} เท่า",
                wrongs=tuple(("ประมาณ 5 เท่า", "ประมาณ 10 เท่า", "ประมาณ 25 เท่า",
                                         "ประมาณ 2.5 เท่า", "ประมาณ 500 เท่า", "ประมาณ 1,000 เท่า")),
                hint="โชติมาตรต่างกัน 5 หมายถึงความสว่างต่างกันหนึ่งร้อยเท่าตามนิยาม",
                topic=LUMINOSITY_TOPIC,
            )
        star = min(STARS, key=lambda one: one.apparent)
        return _labelled_science_wave_c7(
            stem=stem + f"จากข้อมูลนี้ “{star.name}” มีโชติมาตรปรากฏน้อยแต่โชติมาตร"
                        "สัมบูรณ์มากกว่าดาวดวงอื่นบางดวง ข้อใดอธิบายได้ถูกต้อง",
            correct="ดาวดวงนี้ดูสว่างเพราะอยู่ใกล้โลก แต่ความส่องสว่างที่แท้จริง"
                    "ไม่ได้มากที่สุดในกลุ่ม",
            wrongs=tuple((
                "ดาวดวงนี้ดูสว่างเพราะมีความส่องสว่างที่แท้จริงมากที่สุดในกลุ่ม",
                "ดาวดวงนี้ดูสลัวเพราะอยู่ไกลที่สุดในกลุ่ม",
                "ค่าทั้งสองขัดแย้งกัน จึงต้องมีค่าหนึ่งที่วัดผิด",
                "ดาวดวงนี้ดูสว่างเพราะมีรัศมีใหญ่ที่สุดในกลุ่ม",
                "ดาวดวงนี้ดูสว่างเพราะมีอุณหภูมิผิวสูงที่สุดในกลุ่ม",
            )),
            hint="โชติมาตรปรากฏขึ้นกับระยะทางด้วย ส่วนโชติมาตรสัมบูรณ์ตัดระยะทางออกไปแล้ว",
            topic=LUMINOSITY_TOPIC,
        )


@question_type(
    "astro.magnitude_scale_fluency",
    display_name={"th": "เปรียบเทียบความสว่างของดาวจากโชติมาตร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class MagnitudeScaleFluency(QuestionType):
    """Smaller magnitude is brighter; absolute magnitude compares true output."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        mags = [Fraction(n, 10) for n in rng.sample(range(-15, 61), 4)]
        if rng.random() < 0.5:
            bright = rng.random() < 0.5
            pick = mags.index(min(mags) if bright else max(mags))
            table = " ".join(f"{n} โชติมาตรปรากฏ {show(m)}" for n, m in zip(NAMES, mags))
            return _labelled(stem=f"{table} ดาวใดปรากฏ{'สว่างที่สุด' if bright else 'สว่างน้อยที่สุด'}บนท้องฟ้า", correct=NAMES[pick],
                             wrongs=tuple(n for n in NAMES if n != NAMES[pick]), topic=TOPIC_MAG, hint=MAG_HINT)
        absolute = [Fraction(n, 10) for n in rng.sample(range(-80, 151), 4)]
        pick = absolute.index(min(absolute))
        table = " ".join(f"{n} โชติมาตรปรากฏ {show(m)} โชติมาตรสัมบูรณ์ {show(a)}" for n, m, a in zip(NAMES, mags, absolute))
        return _labelled(stem=f"{table} ดาวใดมีความส่องสว่างจริงมากที่สุด", correct=NAMES[pick],
                         wrongs=tuple(n for n in NAMES if n != NAMES[pick]), topic=TOPIC_MAG,
                         hint=MAG_HINT + " เปรียบเทียบความส่องสว่างจริงด้วยโชติมาตรสัมบูรณ์")


@question_type(
    "astro.star_luminosity_application",
    display_name={"th": "วิเคราะห์ความสว่างของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=LUMINOSITY_TOPIC,
)
class StarLuminosityApplication(QuestionType):
    """Separate looking bright from being bright, and size from temperature."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LUMINOSITY_SCENARIOS,
            hint="แยกให้ชัดระหว่างความสว่างที่เห็นจากโลกกับความส่องสว่างที่แท้จริง",
        ), LUMINOSITY_TOPIC)


@question_type(
    "astro.magnitude_scale_application",
    display_name={"th": "คำนวณอัตราส่วนความสว่างและความส่องสว่าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG,
)
class MagnitudeScaleApplication(QuestionType):
    """Five magnitudes is 100 times; inverse square; L ∝ R²T⁴; distance modulus."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            k = rng.randint(1, 3)
            a = Fraction(rng.randint(-10, 20), 10)
            b = a + 5 * k
            return numeric(stem=f"ดาว ก มีโชติมาตรปรากฏ {show(a)} ดาว ข มีโชติมาตรปรากฏ {show(b)} (ต่างกัน 5 โชติมาตร สว่างต่างกัน 100 เท่า) "
                                f"ดาว ก ปรากฏสว่างกว่าดาว ข กี่เท่า", answer=100 ** k,
                           wrongs=[5 * k, 10 ** k, 100 * k], unit="เท่า", topic=TOPIC_MAG, hint="ทุก ๆ 5 โชติมาตร ความสว่างต่างกัน 100 เท่า")
        if roll < 0.55:
            k = rng.choice((2, 3, 4, 5, 10))
            nearer = rng.random() < 0.5
            return numeric(stem=f"ถ้าดาวดวงหนึ่ง{'เคลื่อนเข้าใกล้' if nearer else 'อยู่ห่างออกไป'}จนระยะห่าง{'ลดลงเหลือ 1/' + str(k) + ' ' if nearer else 'เพิ่มเป็น ' + str(k) + ' เท่า'}ของเดิม "
                                f"ความสว่างปรากฏจะ{'เพิ่มขึ้น' if nearer else 'ลดลง'}กี่เท่า", answer=k * k,
                           wrongs=[k, 2 * k, k ** 3], unit="เท่า", topic=TOPIC_MAG, hint="ความสว่างปรากฏแปรผกผันกับระยะทางยกกำลังสอง")
        if roll < 0.8:
            r = rng.choice((1, 2, 3, 4, 5, 10))
            t = rng.choice((1, 2, 3)) if r <= 5 else 1
            if r == 1 and t == 1:
                r = 2
            return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งมีรัศมี {r} เท่า และอุณหภูมิผิว {t} เท่าของดวงอาทิตย์ (L ∝ R²T⁴) "
                                f"มีความส่องสว่างกี่เท่าของดวงอาทิตย์", answer=r ** 2 * t ** 4,
                           wrongs=[r * t, r ** 2 * t ** 2, r ** 4 * t ** 2], unit="เท่า", topic=TOPIC_MAG, hint="L ∝ R² × T⁴")
        n = rng.randint(0, 4)
        d = 10 ** n
        m_abs = Fraction(rng.randint(-50, 100), 10)
        modulus = 5 * (n - 1)
        return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งอยู่ห่าง {show(d)} พาร์เซก มีโชติมาตรสัมบูรณ์ {show(m_abs)} (m − M = 5 log(d/10)) "
                            f"โชติมาตรปรากฏเป็นเท่าใด", answer=m_abs + modulus,
                       wrongs=[m_abs - modulus if modulus else m_abs + 5, m_abs + n, m_abs + 10 * (n - 1) if n != 1 else m_abs - 5],
                       unit="", topic=TOPIC_MAG, hint="m = M + 5 log(d/10) ดาวที่ไกลกว่า 10 พาร์เซกจะปรากฏสว่างน้อยกว่าโชติมาตรสัมบูรณ์",
                       allow_negative=True)

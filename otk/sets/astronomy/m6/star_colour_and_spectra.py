"""สี อุณหภูมิผิว และสเปกตรัมของดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/6

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
from otk.sets._support.science_wave_c7 import SPECTRUM_FACTS, SPECTRUM_SCENARIOS

PROVENANCE = Provenance("original")


SPECTRUM_TOPIC = "สี อุณหภูมิผิว และสเปกตรัมของดาวฤกษ์"


class Spectral(NamedTuple):
    """One spectral class, with all three things the indicator names."""
    kind: str
    colour: str
    temperature: str
    kelvin: int
    lines: str


# Hottest first. Every row carries colour, surface temperature and spectrum, so
# a single answer can reach all three, which is what ``ม.6/6`` asks for.
SPECTRAL = (
    Spectral("O", "น้ำเงิน", "ประมาณ 30,000 เคลวินขึ้นไป", 30000,
             "เส้นของฮีเลียมที่แตกตัวเป็นไอออน และเส้นไฮโดรเจนที่จางมาก"),
    Spectral("B", "น้ำเงินขาว", "ประมาณ 20,000 เคลวิน", 20000,
             "เส้นของฮีเลียมที่เป็นกลาง และเส้นไฮโดรเจนที่เริ่มเด่นขึ้น"),
    Spectral("A", "ขาว", "ประมาณ 10,000 เคลวิน", 10000,
             "เส้นไฮโดรเจนเด่นที่สุดในบรรดาดาวฤกษ์ทุกชนิด"),
    Spectral("G", "เหลือง", "ประมาณ 6,000 เคลวิน", 6000,
             "เส้นของโลหะที่แตกตัวเป็นไอออน เช่น แคลเซียม เด่นขึ้นมา"),
    Spectral("K", "ส้ม", "ประมาณ 4,500 เคลวิน", 4500,
             "เส้นของโลหะที่เป็นกลางจำนวนมาก และเส้นไฮโดรเจนจางลง"),
    Spectral("M", "แดง", "ประมาณ 3,000 เคลวิน", 3000,
             "แถบของโมเลกุล เช่น ไทเทเนียมออกไซด์ ซึ่งพบได้เฉพาะในดาวที่เย็นพอ"),
)


def _spans_three(item: Spectral) -> str:
    return (f"ดาวสี{item.colour} มีอุณหภูมิผิว{item.temperature} "
            f"และสเปกตรัมชนิด {item.kind} ซึ่งเห็น{item.lines}")


TOPIC_COLOR = "สี อุณหภูมิผิว และสเปกตรัมของดาวฤกษ์"


COLORS = (("สีน้ำเงิน", 30000), ("สีขาวแกมน้ำเงิน", 15000), ("สีขาว", 9000), ("สีเหลือง", 5800), ("สีส้ม", 4500), ("สีแดง", 3200))


CLASSES = (("O", 30000, 50000), ("B", 10000, 30000), ("A", 7500, 10000), ("F", 6000, 7500), ("G", 5200, 6000), ("K", 3700, 5200), ("M", 2400, 3700))


COLOR_FACTS = (
    ("ดาวฤกษ์สีใดมีอุณหภูมิผิวสูงที่สุด", "สีน้ำเงิน", ("สีแดง", "สีส้ม", "สีเหลือง", "สีน้ำตาล")),
    ("ดาวฤกษ์สีใดมีอุณหภูมิผิวต่ำที่สุด", "สีแดง", ("สีน้ำเงิน", "สีขาว", "สีเหลือง", "สีขาวแกมน้ำเงิน")),
    ("ดวงอาทิตย์เป็นดาวฤกษ์ชนิดสเปกตรัมใด", "ชนิด G สีเหลือง อุณหภูมิผิวประมาณ 5,800 K",
     ("ชนิด O สีน้ำเงิน อุณหภูมิผิวประมาณ 40,000 K", "ชนิด M สีแดง อุณหภูมิผิวประมาณ 3,000 K", "ชนิด A สีขาว อุณหภูมิผิวประมาณ 9,000 K", "ชนิด B สีขาวแกมน้ำเงิน อุณหภูมิผิวประมาณ 20,000 K")),
    ("เส้นมืดในสเปกตรัมของดาวฤกษ์ (เส้นดูดกลืน) บอกข้อมูลใด", "ธาตุที่เป็นองค์ประกอบในบรรยากาศของดาว",
     ("อายุของเอกภพ", "จำนวนดาวเคราะห์รอบดาว", "ทิศที่ดาวขึ้น", "ความหนาของบรรยากาศโลก")),
    ("เมื่ออุณหภูมิผิวของดาวสูงขึ้น ความยาวคลื่นที่ดาวแผ่รังสีออกมามากที่สุดเปลี่ยนไปอย่างไร", "สั้นลง ดาวจึงดูเป็นสีน้ำเงินมากขึ้น",
     ("ยาวขึ้น ดาวจึงดูแดงขึ้น", "ไม่เปลี่ยนแปลง", "ยาวขึ้นจนเป็นคลื่นวิทยุเท่านั้น", "หายไปทั้งหมด")),
    ("การเรียงลำดับชนิดสเปกตรัม O B A F G K M เรียงตามสมบัติใด", "อุณหภูมิผิวจากสูงไปต่ำ",
     ("ขนาดจากเล็กไปใหญ่", "ระยะทางจากใกล้ไปไกล", "อายุจากน้อยไปมาก", "มวลจากน้อยไปมาก")),
    ("ดาวบีเทลจุสในกลุ่มดาวนายพรานมีสีแดง ส่วนดาวไรเจลมีสีขาวแกมน้ำเงิน ข้อใดถูกต้อง", "ไรเจลมีอุณหภูมิผิวสูงกว่าบีเทลจุส",
     ("บีเทลจุสมีอุณหภูมิผิวสูงกว่าไรเจล", "ทั้งสองดวงมีอุณหภูมิผิวเท่ากัน", "สีของดาวไม่เกี่ยวกับอุณหภูมิ", "ไรเจลอยู่ใกล้โลกกว่าจึงเป็นสีน้ำเงิน")),
    ("นักดาราศาสตร์ใช้อุปกรณ์ใดแยกแสงดาวเพื่อศึกษาสเปกตรัม", "สเปกโทรสโคปหรือเกรตติง",
     ("เทอร์โมมิเตอร์", "บารอมิเตอร์", "ไซสโมกราฟ", "ไฮโกรมิเตอร์")),
)


COLOR_HINT = ("ดาวร้อนมากเป็นสีน้ำเงิน ร้อนน้อยเป็นสีแดง ชนิดสเปกตรัม O B A F G K M เรียงจากร้อนไปเย็น "
              "กฎของวีน λmax = 2,900,000 ÷ T (λ เป็น nm, T เป็น K) อุณหภูมิสูง ความยาวคลื่นสูงสุดสั้นลง")


WIEN = ((100, 29000), (145, 20000), (200, 14500), (290, 10000), (400, 7250), (500, 5800), (580, 5000), (725, 4000), (800, 3625), (1000, 2900))


@question_type(
    "astro.star_spectrum_foundation",
    display_name={"th": "สีกับอุณหภูมิผิวของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=SPECTRUM_TOPIC,
)
class StarSpectrumFoundation(QuestionType):
    """Know which colours are hot and why colour reports temperature at all."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SPECTRUM_FACTS,
            hint="นึกถึงโลหะที่ถูกเผา: ร้อนน้อยเป็นสีแดง ร้อนมากเป็นสีขาวอมน้ำเงิน",
        ), SPECTRUM_TOPIC)


@question_type(
    "astro.star_color_foundation",
    display_name={"th": "สี อุณหภูมิผิว และชนิดสเปกตรัมของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COLOR,
)
class StarColorFoundation(QuestionType):
    """Hot is blue, cool is red; spectral classes; absorption lines."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(COLOR_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_COLOR, hint=COLOR_HINT)


@question_type(
    "astro.star_spectrum_fluency",
    display_name={"th": "เชื่อมโยงสี อุณหภูมิผิว และสเปกตรัม"},
    level=UPPER_SIX, subject=SUBJECT, topic=SPECTRUM_TOPIC,
)
class StarSpectrumFluency(QuestionType):
    """Reach colour, surface temperature and spectrum in one answer.

    ``ม.6/6`` names all three under a single verb, so by the multi-object rule
    only an answer holding all three is a defensible match.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SPECTRAL)
        others = [other for other in SPECTRAL if other.kind != item.kind]
        rng.shuffle(others)
        draw = rng.random()
        if draw < 0.4:
            return _labelled_science_wave_c7(
                stem=f"ดาวฤกษ์ที่จัดอยู่ในสเปกตรัมชนิด {item.kind} "
                     "มีสี อุณหภูมิผิว และลักษณะสเปกตรัมอย่างไร",
                correct=_spans_three(item),
                wrongs=tuple(_spans_three(other) for other in others[:3]),
                hint="ตอบให้ครบทั้งสามเรื่อง แล้วตรวจว่าสีกับอุณหภูมิเข้าคู่กันถูกต้อง",
                topic=SPECTRUM_TOPIC,
            )
        if draw < 0.7:
            return _labelled_science_wave_c7(
                stem=f"ดาวฤกษ์ที่เห็น{item.lines} ในสเปกตรัม "
                     "มีสีและอุณหภูมิผิวอย่างไร",
                correct=f"สี{item.colour} อุณหภูมิผิว{item.temperature}",
                wrongs=tuple(f"สี{other.colour} อุณหภูมิผิว{other.temperature}"
                             for other in others[:3]),
                hint="เส้นในสเปกตรัมบอกว่าผิวดาวร้อนพอจะทำให้ธาตุอยู่ในสภาพใด",
                topic=SPECTRUM_TOPIC,
            )
        return _labelled_science_wave_c7(
            stem=f"ดาวฤกษ์สี{item.colour}จัดอยู่ในสเปกตรัมชนิดใด "
                 "และมีอุณหภูมิผิวประมาณเท่าใด",
            correct=f"ชนิด {item.kind} อุณหภูมิผิว{item.temperature}",
            wrongs=tuple(f"ชนิด {other.kind} อุณหภูมิผิว{other.temperature}"
                         for other in others[:3]),
            hint="ไล่ลำดับ O B A F G K M จากร้อนที่สุดไปเย็นที่สุด",
            topic=SPECTRUM_TOPIC,
        )


@question_type(
    "astro.star_color_fluency",
    display_name={"th": "ระบุสีและชนิดสเปกตรัมจากอุณหภูมิผิว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COLOR,
)
class StarColorFluency(QuestionType):
    """Class from a temperature; hottest or coolest from colours."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            letter, lo, hi = rng.choice(CLASSES)
            temp = rng.randrange(lo + 100, hi - 99, 100)
            others = [c[0] for c in CLASSES if c[0] != letter]
            return _labelled(stem=f"ดาวฤกษ์อุณหภูมิผิวประมาณ {show(temp)} K เป็นชนิดสเปกตรัมใด "
                                  f"(O > 30,000 K, B 10,000-30,000, A 7,500-10,000, F 6,000-7,500, G 5,200-6,000, K 3,700-5,200, M < 3,700)",
                             correct=letter, wrongs=tuple(others), topic=TOPIC_COLOR, hint=COLOR_HINT)
        picked = rng.sample(COLORS, 4)
        hot = rng.random() < 0.5
        right = (max if hot else min)(picked, key=lambda c: c[1])[0]
        return _labelled(stem=f"ดาวฤกษ์ใดน่าจะมีอุณหภูมิผิว{'สูง' if hot else 'ต่ำ'}ที่สุด", correct=f"ดาว{right}",
                         wrongs=tuple(f"ดาว{c[0]}" for c in picked if c[0] != right), topic=TOPIC_COLOR, hint=COLOR_HINT)


@question_type(
    "astro.star_spectrum_application",
    display_name={"th": "วิเคราะห์สเปกตรัมของดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=SPECTRUM_TOPIC,
)
class StarSpectrumApplication(QuestionType):
    """Read a spectrum back to a temperature, and account for reddening."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SPECTRUM_SCENARIOS,
            hint="ร้อนกว่าคือน้ำเงินกว่า และเส้นในสเปกตรัมบอกสภาพของธาตุที่ผิวดาว",
        ), SPECTRUM_TOPIC)


@question_type(
    "astro.star_color_application",
    display_name={"th": "คำนวณด้วยกฎของวีน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COLOR,
)
class StarColorApplication(QuestionType):
    """λmax = 2,900,000 / T in nm and K, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        lam, temp = rng.choice(WIEN)
        name = rng.choice(("ดาวฤกษ์ดวงหนึ่ง", "ดาวในกลุ่มดาวนายพราน", "ดาวในกลุ่มดาวแมงป่อง", "ดาวในกระจุกดาวลูกไก่"))
        if rng.random() < 0.5:
            return numeric(stem=f"{name}มีอุณหภูมิผิว {show(temp)} K (λmax = 2,900,000 ÷ T โดย λ เป็น nm และ T เป็น K) "
                                f"แผ่รังสีมากที่สุดที่ความยาวคลื่นกี่ nm", answer=lam,
                           wrongs=[lam * 10, lam + 100, Fraction(temp, 10)], unit="nm", topic=TOPIC_COLOR, hint="λmax = 2,900,000 ÷ T")
        return numeric(stem=f"{name}แผ่รังสีมากที่สุดที่ความยาวคลื่น {lam} nm (λmax = 2,900,000 ÷ T โดย λ เป็น nm และ T เป็น K) "
                            f"มีอุณหภูมิผิวกี่ K", answer=temp,
                       wrongs=[temp * 10, temp + 1000, Fraction(temp, 2)], unit="K", topic=TOPIC_COLOR, hint="T = 2,900,000 ÷ λmax")

"""สภาพละลายได้ของสาร

เคมี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.2/4

Sets moved here from: science_wave_d9.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d9 import SECONDARY_TWO

PROVENANCE = Provenance("original")


SOLUBILITY_TOPIC = "สภาพละลายได้ของสาร"


class Pressure(NamedTuple):
    case: str
    answer: str
    wrongs: tuple[str, ...]


PRESSURES = (
    Pressure("เมื่อเปิดฝาขวดน้ำอัดลม มีฟองแก๊สผุดขึ้นมาจำนวนมาก",
             "ความดันเหนือน้ำอัดลมลดลง แก๊สคาร์บอนไดออกไซด์ละลายได้น้อยลงจึงแยกออกมาเป็นฟอง",
             ("ความดันเหนือน้ำอัดลมเพิ่มขึ้น แก๊สจึงละลายได้มากขึ้นและเกิดฟองขึ้นมาที่ผิว",
              "ความดันไม่มีผลต่อการละลายของแก๊ส ฟองเกิดจากน้ำเดือด",
              "ความดันลดลง แก๊สจึงละลายได้มากขึ้น",
              "ฟองเกิดจากน้ำตาลในน้ำอัดลมกลายเป็นแก๊ส",
              "ความดันเหนือน้ำอัดลมไม่เปลี่ยน แต่แก๊สถูกดูดออกโดยอากาศ")),
    Pressure("โรงงานผลิตน้ำอัดลมอัดแก๊สคาร์บอนไดออกไซด์ลงในเครื่องดื่มภายใต้ความดันสูงแล้วปิดฝาให้แน่น",
             "ความดันสูงทำให้แก๊สละลายในเครื่องดื่มได้มากขึ้น ปิดฝาแน่นจึงช่วยเก็บแก๊สไว้",
             ("ความดันสูงทำให้แก๊สละลายได้น้อยลง จึงต้องอัดแก๊สเพิ่มและปิดฝาให้แน่น",
              "ความดันมีผลเฉพาะกับของแข็ง ไม่เกี่ยวกับแก๊ส",
              "ปิดฝาแน่นเพื่อให้ความดันในขวดลดลง",
              "ความดันสูงทำให้แก๊สกลายเป็นของเหลวทั้งหมด",
              "ปิดฝาแน่นเพื่อไม่ให้อากาศภายนอกละลายเข้าไปแทน")),
    Pressure("นักดำน้ำลึกที่ขึ้นสู่ผิวน้ำเร็วเกินไปอาจเกิดฟองแก๊สไนโตรเจนในเลือด",
             "ที่ความลึกความดันสูง แก๊สละลายในเลือดได้มาก เมื่อขึ้นเร็วความดันลดลงทันที แก๊สละลายได้น้อยลงจึงแยกเป็นฟอง",
             ("ที่ความลึกความดันต่ำ แก๊สจึงละลายในเลือดได้น้อย",
              "ความดันที่ลดลงทำให้แก๊สละลายในเลือดได้มากขึ้น",
              "ฟองแก๊สเกิดจากเลือดเดือดเพราะน้ำทะเลร้อน",
              "ไนโตรเจนในเลือดทำปฏิกิริยากลายเป็นแก๊สใหม่เมื่อขึ้นเร็ว",
              "ความดันไม่มีผลต่อแก๊สในเลือด ฟองเกิดจากการว่ายน้ำเร็ว")),
    Pressure("เครื่องดื่มอัดแก๊สที่เปิดฝาทิ้งไว้นาน รสซ่าจะค่อย ๆ หายไป",
             "เมื่อเปิดฝา ความดันเหนือเครื่องดื่มลดลง แก๊สละลายได้น้อยลงจึงแยกออกจนหมดซ่า",
             ("เมื่อเปิดฝา ความดันเพิ่มขึ้น แก๊สจึงละลายได้มากขึ้นจนไม่ซ่า",
              "รสซ่าหายเพราะน้ำตาลตกตะกอน ไม่เกี่ยวกับแก๊สที่ละลายอยู่",
              "ความดันไม่มีผล แก๊สหายไปเพราะแสงไฟในห้อง",
              "แก๊สละลายได้มากขึ้นเมื่อความดันลดลง จึงไม่เห็นฟองและรสซ่าค่อย ๆ หายไป",
              "อากาศภายนอกดันแก๊สให้ละลายกลับลงไปจนหมด")),
    Pressure("ขวดน้ำอัดลมที่เปิดบนยอดเขาสูงมีฟองพุ่งออกมามากกว่าขวดแบบเดียวกันที่เปิดบนพื้นราบ",
             "บนยอดเขาความดันอากาศต่ำกว่า เมื่อเปิดฝาแก๊สจึงละลายได้น้อยลงและแยกออกเป็นฟองมาก",
             ("บนยอดเขาความดันอากาศสูงกว่า แก๊สจึงละลายได้มากขึ้นและพุ่งออกมาเป็นฟองมาก",
              "บนยอดเขาน้ำอัดลมเดือดเพราะอากาศร้อนกว่า",
              "ความดันไม่มีผล ฟองมากเพราะขวดถูกเขย่าระหว่างเดินทางเท่านั้น",
              "บนยอดเขาความดันต่ำ แก๊สจึงละลายได้มากขึ้น",
              "บนยอดเขามีออกซิเจนน้อย แก๊สคาร์บอนไดออกไซด์จึงกลายเป็นออกซิเจน")),
)


# (solute, grams per 100 g water at 25 °C) pairs that differ plainly.
SOLUTE_PAIRS = (
    (("น้ำตาลทราย", 204), ("เกลือแกง", 36)),
    (("น้ำตาลทราย", 204), ("โพแทสเซียมไนเตรต", 38)),
    (("เกลือแกง", 36), ("ปูนขาว", 0.2)),
)


# (solute, (solvent, grams per 100 g), (solvent, grams per 100 g))
SOLVENT_CASES = (
    ("ไอโอดีน", ("เอทานอล", 21), ("น้ำ", 0.03)),
    ("เกลือแกง", ("น้ำ", 36), ("เอทานอล", 0.07)),
)


# (solute, (°C, grams per 100 g water), (°C, grams per 100 g water))
TEMPERATURE_CASES = (
    ("โพแทสเซียมไนเตรต", (20, 32), (60, 110)),
    ("น้ำตาลทราย", (20, 200), (80, 362)),
    ("จุนสี", (20, 32), (60, 62)),
)


def _n(value: float) -> str:
    return f"{value:g}"


def solubility_parts(solutes, solvent, temperature) -> tuple[Part, ...]:
    (a, qa), (b, qb) = solutes
    more, less = (a, b) if qa > qb else (b, a)
    solute, (s1, q1), (s2, q2) = solvent
    good, poor = (s1, s2) if q1 > q2 else (s2, s1)
    warm_solute, (t1, w1), (t2, w2) = temperature
    rises = (w2 > w1) == (t2 > t1)
    return (
        Part("ชนิดตัวละลาย", f"ในน้ำปริมาณเท่ากัน {more}ละลายได้มากกว่า{less}",
             f"ในน้ำปริมาณเท่ากัน {less}ละลายได้มากกว่า{more}"),
        Part("ชนิดตัวทำละลาย", f"{solute}ละลายใน{good}ได้มากกว่าใน{poor}",
             f"{solute}ละลายใน{poor}ได้มากกว่าใน{good}"),
        Part("อุณหภูมิ",
             f"{warm_solute}ละลายน้ำได้{'มากขึ้น' if rises else 'น้อยลง'}เมื่ออุณหภูมิสูงขึ้น",
             f"{warm_solute}ละลายน้ำได้{'น้อยลง' if rises else 'มากขึ้น'}เมื่ออุณหภูมิสูงขึ้น"),
    )


SOLUBILITY_SCENARIOS = (
    ("นักเรียนต้องการทดลองว่าอุณหภูมิมีผลต่อสภาพละลายได้ของน้ำตาลหรือไม่ ข้อใดเป็นการออกแบบการทดลองที่ถูกต้อง",
     "ใช้น้ำปริมาณเท่ากันและน้ำตาลชนิดเดียวกัน เปลี่ยนเฉพาะอุณหภูมิของน้ำ แล้ววัดปริมาณน้ำตาลที่ละลายได้จนอิ่มตัว",
     ("ใช้น้ำร้อนปริมาณมากกว่าน้ำเย็น เพื่อให้เห็นผลชัดขึ้น",
      "ใช้น้ำตาลต่างชนิดกันในน้ำแต่ละอุณหภูมิ",
      "คนน้ำร้อนแต่ไม่คนน้ำเย็น",
      "เปลี่ยนทั้งอุณหภูมิและชนิดของน้ำตาลพร้อมกัน",
      "วัดเฉพาะเวลาที่น้ำตาลละลายหมดในน้ำร้อนเพียงแก้วเดียว")),
    ("ปลาในบ่อมักลอยขึ้นมาหายใจที่ผิวน้ำในวันที่อากาศร้อนจัด ข้อใดอธิบายได้สอดคล้องกับสภาพละลายได้ของแก๊ส",
     "น้ำที่อุ่นขึ้นละลายแก๊สออกซิเจนได้น้อยลง ออกซิเจนในน้ำจึงไม่พอ",
     ("น้ำที่อุ่นขึ้นละลายแก๊สออกซิเจนได้มากขึ้น",
      "ปลาต้องการแสงแดดมากขึ้นในวันที่ร้อน",
      "ความดันอากาศสูงขึ้นมากในวันที่ร้อน",
      "น้ำอุ่นทำให้ปลาไม่ต้องใช้ออกซิเจน",
      "ออกซิเจนละลายในน้ำได้มากที่สุดเมื่อน้ำร้อนจัด")),
    ("ที่ 60 องศาเซลเซียส โพแทสเซียมไนเตรตละลายในน้ำ 100 กรัมได้ 110 กรัม และที่ 20 องศาเซลเซียสได้ 32 กรัม ถ้าทำสารละลายอิ่มตัวในน้ำ 100 กรัมที่ 60 องศาเซลเซียส แล้วทำให้เย็นลงเหลือ 20 องศาเซลเซียส จะมีผลึกแยกออกมากี่กรัม",
     "78 กรัม",
     ("32 กรัม", "110 กรัม", "142 กรัม", "39 กรัม", "156 กรัม")),
)


# โพแทสเซียมไนเตรต: grams that dissolve in 100 g of water at each temperature (°C).
KNO3_SOLUBILITY = {20: 32, 40: 64, 60: 110, 80: 169}


def crystals_on_cooling(rng: Random) -> GeneratedQuestion:
    """A saturated solution cooled; the mass of crystals that separate."""
    # Not 20 → 40 °C: 64 g is exactly twice 32 g, so the crystals would equal what stays dissolved.
    low, high = rng.choice([(lo, hi) for lo in KNO3_SOLUBILITY for hi in KNO3_SOLUBILITY
                            if lo < hi and KNO3_SOLUBILITY[hi] != 2 * KNO3_SOLUBILITY[lo]])
    water = rng.choice((50, 100, 200))
    scale = Decimal(water) / 100
    hot, cold = KNO3_SOLUBILITY[high] * scale, KNO3_SOLUBILITY[low] * scale
    answer = hot - cold
    pool = (cold, hot, hot + cold, answer * 2, Decimal(KNO3_SOLUBILITY[high] - KNO3_SOLUBILITY[low]),
            Decimal(KNO3_SOLUBILITY[high]), Decimal(KNO3_SOLUBILITY[low]), answer * 3)
    fmt_g = lambda value: f"{value.normalize():f} กรัม"
    return _labelled(
        stem=(f"โพแทสเซียมไนเตรตละลายในน้ำ 100 กรัมได้ {KNO3_SOLUBILITY[high]} กรัมที่ {high} องศาเซลเซียส "
              f"และได้ {KNO3_SOLUBILITY[low]} กรัมที่ {low} องศาเซลเซียส ถ้าทำสารละลายอิ่มตัวในน้ำ {water} กรัมที่ "
              f"{high} องศาเซลเซียส แล้วทำให้เย็นลงเหลือ {low} องศาเซลเซียส จะมีผลึกแยกออกมากี่กรัม"),
        correct=fmt_g(answer),
        wrongs=tuple(dict.fromkeys(fmt_g(w) for w in pool if w != answer)),
        hint="ปรับค่าสภาพละลายได้ตามมวลน้ำก่อน แล้วผลึกที่แยกออก = ปริมาณที่ละลายได้ที่อุณหภูมิสูง − ที่อุณหภูมิต่ำ",
        topic=SOLUBILITY_TOPIC,
    )


@question_type(
    "chem.solubility_factor_foundation",
    display_name={"th": "อธิบายผลของความดันต่อสภาพละลายได้ของแก๊สจากสารสนเทศ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SOLUBILITY_TOPIC,
)
class SolubilityFactorFoundation(QuestionType):
    """A case about a dissolved gas; how pressure explains it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(PRESSURES)
        return _labelled(
            stem=f"ข้อมูลจากแหล่งสารสนเทศ: {case.case} ข้อใดอธิบายผลของความดันได้ถูกต้อง",
            correct=case.answer,
            wrongs=case.wrongs,
            hint="แก๊สละลายในของเหลวได้มากขึ้นเมื่อความดันสูงขึ้น และน้อยลงเมื่อความดันลดลง",
            topic=SOLUBILITY_TOPIC,
        )


@question_type(
    "chem.solubility_factor_fluency",
    display_name={"th": "อธิบายผลของชนิดตัวละลาย ตัวทำละลาย และอุณหภูมิต่อสภาพละลายได้จากผลการทดลอง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SOLUBILITY_TOPIC,
)
class SolubilityFactorFluency(QuestionType):
    """Three experiments, each varying one factor; explain all three effects."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        solutes = list(rng.choice(SOLUTE_PAIRS))
        rng.shuffle(solutes)
        solute, *solvents = rng.choice(SOLVENT_CASES)
        rng.shuffle(solvents)
        warm_solute, *temps = rng.choice(TEMPERATURE_CASES)
        rng.shuffle(temps)
        (a, qa), (b, qb) = solutes
        (s1, q1), (s2, q2) = solvents
        (t1, w1), (t2, w2) = temps
        record = (f"การทดลองที่ 1 (น้ำ 100 กรัม ที่ 25 องศาเซลเซียส): {a} ละลายได้ {_n(qa)} กรัม, {b} ละลายได้ {_n(qb)} กรัม / "
                  f"การทดลองที่ 2 (ตัวทำละลาย 100 กรัม ที่ 25 องศาเซลเซียส): {solute}ละลายใน{s1}ได้ {_n(q1)} กรัม, ใน{s2}ได้ {_n(q2)} กรัม / "
                  f"การทดลองที่ 3 (น้ำ 100 กรัม): {warm_solute}ละลายได้ {_n(w1)} กรัมที่ {t1} องศาเซลเซียส และ {_n(w2)} กรัมที่ {t2} องศาเซลเซียส")
        return parts_item(
            rng, solubility_parts(solutes, (solute, *solvents), (warm_solute, *temps)),
            stem=(f"นักเรียนออกแบบการทดลอง 3 ชุด โดยแต่ละชุดเปลี่ยนเพียงปัจจัยเดียว ได้ผลดังนี้ — {record} "
                  "จากผลการทดลอง ข้อใดอธิบายผลของปัจจัยทั้งสามต่อสภาพละลายได้ถูกต้องทั้งหมด"),
            hint="อ่านทีละการทดลอง เทียบปริมาณที่ละลายได้เมื่อเปลี่ยนปัจจัยนั้น ข้อที่ผิดจะผิดอย่างน้อยหนึ่งปัจจัย",
            topic=SOLUBILITY_TOPIC,
        )


@question_type(
    "chem.solubility_factor_application",
    display_name={"th": "ออกแบบการทดลองและใช้สภาพละลายได้แก้ปัญหา"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=SOLUBILITY_TOPIC,
)
class SolubilityFactorApplication(QuestionType):
    """A fair temperature test, fish gasping on hot days, and crystals from cooling."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return crystals_on_cooling(rng)
        return _retopic(scenario_question(
            rng, SOLUBILITY_SCENARIOS,
            hint="เปลี่ยนตัวแปรต้นเพียงตัวเดียว และใช้ข้อมูลสภาพละลายได้คำนวณหรืออธิบายผล",
        ), SOLUBILITY_TOPIC)

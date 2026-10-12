"""การสะสมสารพิษในโซ่อาหาร

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.3/5

Sets moved here from: science_wave_b.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import (
    Concept,
    ConceptBankType,
    contextual_scenario_question,
    widen,
)
from otk.sets._support.science_wave_b import LEVEL, SUBJECT, TOPIC, TOXIN_SCENARIOS, _labelled

PROVENANCE = Provenance("original")


class ToxinCase(NamedTuple):
    """One measured chain: the toxin, where it entered, and what was found in each.

    ``levels`` runs from the producer upward and ``readings`` runs beside it, both
    in ส่วนในพันล้านส่วน. Only the readings are stored; every ratio the questions
    ask for is computed, so a stated multiple cannot drift from the table.
    """
    habitat: str
    toxin: str
    source: str
    source_reading: int
    levels: tuple[str, ...]
    readings: tuple[int, ...]


TOXIN_CASES = (
    ToxinCase("นาข้าว", "สารกำจัดแมลงชนิดสลายตัวช้า", "น้ำในนา", 2,
              ("ต้นข้าว", "ตั๊กแตน", "กบ", "งู"), (20, 200, 2_000, 20_000)),
    ToxinCase("ทะเลสาบ", "สารปรอท", "น้ำในทะเลสาบ", 5,
              ("แพลงก์ตอนพืช", "ไรน้ำ", "ปลาเล็ก", "ปลาใหญ่"),
              (100, 500, 2_500, 12_500)),
    ToxinCase("อ่าวชายฝั่ง", "สารดีดีที", "น้ำทะเลบริเวณอ่าว", 3,
              ("แพลงก์ตอนพืช", "หอยสองฝา", "ปลาทู", "นกนางนวล"),
              (60, 240, 960, 3_840)),
    ToxinCase("บึงน้ำจืด", "สารกำจัดวัชพืชตกค้าง", "น้ำในบึง", 4,
              ("สาหร่าย", "หอยขม", "ปลาช่อน", "นกกระยาง"),
              (40, 200, 1_000, 5_000)),
    ToxinCase("แม่น้ำท้ายเหมือง", "สารตะกั่ว", "น้ำในแม่น้ำ", 2,
              ("สาหร่าย", "ลูกกุ้ง", "ปลาซิว", "ปลากราย"), (10, 30, 90, 270)),
    ToxinCase("ป่าชายเลน", "สารแคดเมียม", "น้ำในป่าชายเลน", 3,
              ("แพลงก์ตอนพืช", "หอยแครง", "ปูแสม", "นกยาง"), (12, 48, 192, 768)),
    ToxinCase("อ่างเก็บน้ำ", "สารพีซีบี", "น้ำในอ่างเก็บน้ำ", 1,
              ("สาหร่าย", "ไรน้ำ", "ปลาตะเพียน", "นาก"), (5, 25, 125, 625)),
    ToxinCase("ทุ่งหญ้า", "สารกำจัดหนูชนิดสลายตัวช้า", "ดินในทุ่งหญ้า", 4,
              ("หญ้า", "ตั๊กแตน", "จิ้งจก", "เหยี่ยว"), (8, 32, 128, 512)),
    ToxinCase("คลองข้างโรงงาน", "สารโครเมียม", "น้ำในคลอง", 5,
              ("สาหร่าย", "หอยขม", "ปลานิล", "นกกาน้ำ"), (15, 45, 135, 405)),
    ToxinCase("ทะเลนอกชายฝั่ง", "สารดีบุกอินทรีย์", "น้ำทะเลนอกชายฝั่ง", 2,
              ("แพลงก์ตอนพืช", "กุ้งเคย", "ปลากะตัก", "ปลาเก๋า"), (6, 24, 96, 384)),
)


def magnification_factor(case: ToxinCase) -> int:
    """The constant step between consecutive levels of one case."""
    return case.readings[1] // case.readings[0]


def _distinct_labels(correct: str, candidates: tuple[str, ...],
                     want: int = 3) -> tuple[str, ...]:
    """`want` labels that differ from each other and from the answer.

    Two diagnostic miscalculations can coincide for a particular row — dividing
    by the producer reading and dividing the true ratio by ten give the same
    number whenever the producer sits exactly ten times above the source — and a
    duplicate would silently cost a choice. More candidates are offered than are
    needed so the shortfall cannot happen.
    """
    out: list[str] = []
    for value in candidates:
        if value != correct and value not in out:
            out.append(value)
        if len(out) == want:
            break
    assert len(out) == want, (correct, candidates)
    return tuple(out)


@question_type(
    "ecology.biomagnification_foundation",
    display_name={"th": "การสะสมสารพิษในสิ่งมีชีวิตในโซ่อาหาร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BiomagnificationFoundation(ConceptBankType):
    """Why a toxin concentrates upward, and which toxins do it at all.

    The measurement set that follows is only readable once the learner knows that
    the pattern comes from a toxin the body cannot break down or excrete. Without
    that, a rising column of numbers is just a rising column of numbers.
    """

    ITEMS = widen([
        Concept(
            "การสะสมสารพิษในโซ่อาหารหมายถึงอะไร",
            "สารพิษในผู้ถูกกินถูกส่งต่อไปยังผู้กิน ความเข้มข้นจึงสูงขึ้นตามลำดับขั้น",
            ("สารพิษเจือจางลงเรื่อย ๆ เมื่อถ่ายทอดไปตามลำดับขั้นที่สูงขึ้นในโซ่อาหาร",
             "สิ่งมีชีวิตทุกลำดับขั้นมีสารพิษเข้มข้นเท่ากันหมด เพราะอยู่ในแหล่งเดียวกัน",
             "สารพิษสะสมอยู่ในผู้ผลิตเท่านั้น เพราะผู้ผลิตเป็นผู้รับสารพิษจากน้ำโดยตรง"),
        ),
        Concept(
            "สารพิษชนิดใดสะสมในโซ่อาหารได้มากที่สุด",
            "สารที่สลายตัวช้าและละลายได้ดีในไขมัน จึงถูกเก็บไว้ในร่างกายไม่ถูกขับออก",
            ("สารที่สลายตัวเร็วและละลายน้ำได้ดี จึงกระจายไปทั่วร่างกายอย่างรวดเร็ว",
             "สารที่มีความเป็นพิษสูงมาก จนทำให้สิ่งมีชีวิตตายทันทีที่ได้รับสารเข้าไป",
             "สารที่มีสีเข้มจนมองเห็นได้ในเนื้อเยื่อของสิ่งมีชีวิต"),
        ),
        Concept(
            "เหตุใดผู้บริโภคลำดับสูงสุดจึงมีสารพิษสะสมมากที่สุด",
            "เพราะกินเหยื่อจำนวนมากตลอดชีวิต และสารพิษจากเหยื่อทุกตัวสะสมรวมกันอยู่ในตัวมัน",
            ("เพราะร่างกายของผู้บริโภคลำดับสูงสร้างสารพิษขึ้นเองได้",
             "เพราะผู้บริโภคลำดับสูงอาศัยอยู่ใกล้แหล่งที่ปล่อยสารพิษมากที่สุด",
             "เพราะผู้บริโภคลำดับสูงมีขนาดร่างกายใหญ่ จึงดูดซับสารพิษจากน้ำได้มากกว่า"),
        ),
        Concept(
            "ความเข้มข้นของสารพิษในน้ำต่ำมากจนวัดได้ยาก แต่พบในนกกินปลาสูงมาก ข้อใดอธิบายได้ถูกต้อง",
            "สารพิษสะสมและส่งต่อขึ้นไปตามโซ่อาหาร ความเข้มข้นในนกจึงสูงกว่าในน้ำ",
            ("การวัดในน้ำผิดพลาด เพราะความเข้มข้นในน้ำต้องสูงกว่าในสิ่งมีชีวิตเสมอ",
             "นกสร้างสารพิษชนิดนั้นขึ้นเองเมื่ออาศัยอยู่ในบริเวณที่มีมลพิษ",
             "สารพิษระเหยออกจากน้ำแล้วนกหายใจเอาสารพิษเข้าไปโดยตรง"),
        ),
        Concept(
            "ข้อใดเป็นผลของการสะสมสารพิษในโซ่อาหารต่อมนุษย์",
            "มนุษย์ที่กินปลาผู้ล่าขนาดใหญ่ได้รับสารพิษเข้มข้นกว่าผู้ที่กินสิ่งมีชีวิตลำดับขั้นต่ำ",
            ("มนุษย์ไม่ได้รับผลกระทบ เพราะไม่ได้อยู่ในโซ่อาหารของระบบนิเวศ",
             "มนุษย์ได้รับสารพิษมากที่สุดจากการดื่มน้ำในแหล่งนั้นโดยตรง ไม่ใช่จากการกินปลาหรือผัก",
             "มนุษย์ย่อยสลายสารพิษที่สะสมมาได้หมดในกระเพาะอาหาร"),
        ),
        Concept(
            "แนวทางใดลดการสะสมสารพิษในโซ่อาหารได้ตรงจุดที่สุด",
            "ลดการปล่อยสารที่สลายตัวช้าลงสู่แหล่งน้ำและดินตั้งแต่ต้นทาง",
            ("จับผู้บริโภคลำดับสูงออกจากระบบนิเวศให้หมด",
             "เติมน้ำสะอาดลงในแหล่งน้ำเพื่อเจือจางสารพิษในสิ่งมีชีวิต",
             "เปลี่ยนไปกินสิ่งมีชีวิตลำดับขั้นสูงแทนลำดับขั้นต่ำ"),
        ),
        Concept(
            "เหตุใดสารพิษที่สลายตัวเร็วจึงไม่ค่อยเกิดการสะสมในโซ่อาหาร",
            "เพราะสารสลายตัวไปก่อนที่จะถูกส่งต่อขึ้นไปหลายลำดับขั้น จึงไม่สะสม",
            ("เพราะสารที่สลายตัวเร็วไม่เป็นพิษต่อสิ่งมีชีวิตใดเลย",
             "เพราะสารที่สลายตัวเร็วถูกผู้ผลิตดูดซับไว้จนหมดก่อนถึงผู้บริโภค",
             "เพราะสารที่สลายตัวเร็วละลายในไขมันได้ดี จึงถูกขับออกจากร่างกายทันที"),
        ),
    ], (
        ("สารพิษถูกผู้บริโภคลำดับสูงสร้างขึ้นเอง แล้วส่งลงไปยังผู้ผลิต",
         "สารพิษหายไปทั้งหมดเมื่อถูกส่งต่อจากผู้ผลิตไปยังผู้บริโภค"),
        ("สารที่มีกลิ่นแรงจนสัตว์หลีกเลี่ยงไม่กินสิ่งที่มีสารนั้น",
         "สารที่ถูกขับออกทางปัสสาวะได้หมดภายในวันเดียว"),
        ("เพราะผู้บริโภคลำดับสูงกินอาหารน้อยที่สุดในโซ่อาหาร",
         "เพราะผู้บริโภคลำดับสูงดื่มน้ำมากกว่าสิ่งมีชีวิตอื่น"),
        ("ปลาในน้ำขับสารพิษออกมาทางเหงือก แล้วนกได้รับสารนั้นโดยตรงทางน้ำ",
         "สารพิษในน้ำเข้มข้นกว่าในนก แต่นกไวต่อสารมากกว่า"),
        ("มนุษย์ที่กินผักได้รับสารพิษเข้มข้นกว่าผู้ที่กินปลาผู้ล่าขนาดใหญ่หลายเท่า",
         "มนุษย์ได้รับสารพิษเฉพาะเมื่อว่ายน้ำในแหล่งน้ำที่มีสารพิษ"),
        ("ปล่อยสัตว์ต่างถิ่นลงไปกินสิ่งมีชีวิตที่มีสารพิษ",
         "ย้ายแหล่งปล่อยสารพิษไปยังแหล่งน้ำอื่นที่ไกลออกไป"),
        ("เพราะสารที่สลายตัวเร็วถูกผู้บริโภคลำดับสูงดักจับไว้ก่อน",
         "เพราะสารที่สลายตัวเร็วมีโมเลกุลใหญ่เกินกว่าจะเข้าสู่สิ่งมีชีวิตได้"),
    ))


@question_type(
    "ecology.biomagnification_fluency",
    display_name={"th": "อ่านผลการวัดสารพิษตามลำดับขั้นของโซ่อาหาร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BiomagnificationFluency(QuestionType):
    """Read a measured column of concentrations and use the pattern in it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(TOXIN_CASES)
        table = "\n".join(
            f"{name}: {reading:,} ส่วนในพันล้านส่วน"
            for name, reading in zip(case.levels, case.readings)
        )
        preamble = (f"ตรวจวัด{case.toxin}ใน{case.habitat} พบใน{case.source} "
                    f"{case.source_reading:,} ส่วนในพันล้านส่วน และในสิ่งมีชีวิตดังนี้\n"
                    f"{table}\n")
        which = rng.randrange(3)
        if which == 0:
            return _labelled(
                stem=preamble + "สิ่งมีชีวิตใดมีสารพิษสะสมเข้มข้นที่สุด",
                correct=case.levels[-1],
                wrongs=tuple(reversed(case.levels[:-1]))[:3],
                hint="เทียบตัวเลขในตาราง แล้วดูว่าสิ่งมีชีวิตนั้นอยู่ลำดับขั้นใดของโซ่อาหาร",
            )
        if which == 1:
            times = case.readings[-1] // case.source_reading
            factor = magnification_factor(case)
            return _labelled(
                stem=preamble + f"สารพิษใน{case.levels[-1]}เข้มข้นเป็นกี่เท่าของใน{case.source}",
                correct=f"{times:,} เท่า",
                # เทียบกับผู้ผลิตแทนแหล่งที่มา, ใช้อัตราของขั้นเดียว, หรือวางจุดผิดหลัก
                wrongs=_distinct_labels(
                    f"{times:,} เท่า",
                    (f"{case.readings[-1] // case.readings[0]:,} เท่า",
                     f"{factor:,} เท่า",
                     f"{times * 10:,} เท่า",
                     f"{max(times // 10, 1):,} เท่า")),
                hint="หารความเข้มข้นในสิ่งมีชีวิตด้วยความเข้มข้นในแหล่งที่สารพิษเข้ามา",
            )
        factor = magnification_factor(case)
        predicted = case.readings[-1] * factor
        return _labelled(
            stem=preamble + f"ถ้ามีสัตว์อีกชนิดหนึ่งที่กิน{case.levels[-1]}เป็นอาหาร "
                            "และสารพิษยังสะสมด้วยอัตราเดิม สัตว์ชนิดนั้นน่าจะมีสารพิษ"
                            "ประมาณเท่าใด (ส่วนในพันล้านส่วน)",
            correct=f"{predicted:,}",
            # ไม่เพิ่มเลย, ถอยลงหนึ่งขั้น, หรือเพิ่มเป็นสองเท่าแทนอัตราที่อ่านได้
            wrongs=_distinct_labels(
                f"{predicted:,}",
                (f"{case.readings[-1]:,}",
                 f"{case.readings[-1] // factor:,}",
                 f"{case.readings[-1] * 2:,}",
                 f"{predicted * factor:,}")),
            hint="หาว่าตัวเลขเพิ่มขึ้นกี่เท่าในแต่ละขั้น แล้วใช้อัตราเดิมต่อไปอีกหนึ่งขั้น",
        )


@question_type(
    "ecology.biomagnification_application",
    display_name={"th": "วิเคราะห์การสะสมสารพิษและเสนอแนวทางจัดการ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BiomagnificationApplication(QuestionType):
    """Judge a real case of accumulation and what to do about it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, TOXIN_SCENARIOS,
            hint="เทียบความเข้มข้นตามลำดับขั้นก่อน แล้วจึงถามว่าสารเข้าสู่ระบบนิเวศ"
                 "ที่จุดใดและควรหยุดที่จุดใด",
            topic=TOPIC,
        )

"""ยีนบนโครโมโซมเพศและมัลติเปิลแอลลีล

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/2

Sets moved here from: science_wave_b29.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b29 import LINKAGE_SCENARIOS

PROVENANCE = Provenance("original")


LINKAGE_TOPIC = "การถ่ายทอดยีนบนโครโมโซมเพศและมัลติเปิลแอลลีล"


LINKAGE_FACTS = (
    Fact("โครโมโซมเพศของมนุษย์เป็นอย่างไร",
         "เพศหญิงมีโครโมโซมเพศเป็น XX ส่วนเพศชายเป็น XY "
         "โดยโครโมโซม Y สั้นกว่าและมียีนน้อยกว่า X มาก"),
    Fact("ยีนที่อยู่บนโครโมโซม X ถ่ายทอดอย่างไร",
         "ลูกชายได้รับโครโมโซม X จากแม่เพียงแท่งเดียว "
         "ส่วนลูกสาวได้รับ X จากทั้งพ่อและแม่อย่างละแท่ง"),
    Fact("เหตุใดลักษณะด้อยที่ควบคุมด้วยยีนบนโครโมโซม X จึงพบในเพศชายมากกว่า",
         "เพราะเพศชายมีโครโมโซม X เพียงแท่งเดียว จึงแสดงลักษณะทันทีเมื่อได้รับ"
         "แอลลีลด้อยมา ส่วนเพศหญิงต้องได้รับแอลลีลด้อยทั้งสองแท่ง"),
    Fact("มัลติเปิลแอลลีลหมายถึงอะไร",
         "การที่ยีนหนึ่งยีนมีแอลลีลมากกว่าสองแบบอยู่ในประชากร "
         "แม้แต่ละคนจะมีได้เพียงสองแอลลีลก็ตาม"),
    Fact("หมู่เลือดระบบ ABO ถูกควบคุมด้วยแอลลีลกี่แบบ",
         "สามแบบ คือ IA IB และ i โดย IA และ IB ข่ม i ได้ "
         "แต่ IA และ IB ไม่ข่มกันเอง"),
    Fact("ผู้ที่มีหมู่เลือด AB มีจีโนไทป์อย่างไร และเพราะเหตุใด",
         "มีจีโนไทป์ IAIB เพราะ IA และ IB ไม่ข่มกัน จึงแสดงออกทั้งคู่พร้อมกัน"),
    Fact("ผู้ที่มีหมู่เลือด O มีจีโนไทป์อย่างไร",
         "มีจีโนไทป์ ii เท่านั้น เพราะ i เป็นแอลลีลด้อยต่อทั้ง IA และ IB"),
)


# Each blood genotype as the pair of alleles it holds.
BLOOD_GENOTYPES = (
    ("IA", "IA"), ("IA", "IB"), ("IA", "i"),
    ("IB", "IB"), ("IB", "i"), ("i", "i"),
)


def _blood_group(alleles: tuple[str, str]) -> str:
    if "IA" in alleles and "IB" in alleles:
        return "AB"
    if "IA" in alleles:
        return "A"
    if "IB" in alleles:
        return "B"
    return "O"


def _possible_groups(first: tuple[str, str], second: tuple[str, str]) -> str:
    groups = {_blood_group((one, two)) for one in first for two in second}
    order = [group for group in ("A", "B", "AB", "O") if group in groups]
    return "ลูกอาจมีหมู่เลือด " + " หรือ ".join(order) + " เท่านั้น"


class SexCross(NamedTuple):
    """A cross for a recessive gene on the X chromosome, and its outcome."""
    parents: str
    outcome: str


SEX_CROSSES = (
    SexCross("แม่เป็นพาหะของตาบอดสีและพ่อสายตาปกติ",
             "ลูกสาวทุกคนสายตาปกติ โดยครึ่งหนึ่งเป็นพาหะ "
             "ส่วนลูกชายมีโอกาสตาบอดสีครึ่งหนึ่ง"),
    SexCross("แม่สายตาปกติและไม่เป็นพาหะ ส่วนพ่อตาบอดสี",
             "ลูกทุกคนสายตาปกติ โดยลูกสาวทุกคนเป็นพาหะ "
             "ส่วนลูกชายไม่ได้รับแอลลีลด้อยนี้เลย"),
    SexCross("แม่ตาบอดสีและพ่อสายตาปกติ",
             "ลูกชายทุกคนตาบอดสี ส่วนลูกสาวทุกคนสายตาปกติแต่เป็นพาหะ"),
    SexCross("แม่เป็นพาหะและพ่อตาบอดสี",
             "ลูกสาวมีโอกาสตาบอดสีครึ่งหนึ่งและเป็นพาหะอีกครึ่งหนึ่ง "
             "ส่วนลูกชายมีโอกาสตาบอดสีครึ่งหนึ่ง"),
    SexCross("ทั้งแม่และพ่อตาบอดสี",
             "ลูกทุกคนทั้งชายและหญิงตาบอดสี"),
)


@question_type(
    "life.sex_linkage_foundation",
    display_name={"th": "ยีนบนโครโมโซมเพศและมัลติเปิลแอลลีล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=LINKAGE_TOPIC,
)
class SexLinkageFoundation(QuestionType):
    """Both mechanisms the indicator names, side by side."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, LINKAGE_FACTS, topic=LINKAGE_TOPIC,
            hint="สำหรับยีนบนโครโมโซมเพศ ให้ดูว่าใครมี X กี่แท่ง "
                 "สำหรับหมู่เลือด ให้จำว่า IA กับ IB ไม่ข่มกัน",
        )


@question_type(
    "life.sex_linkage_fluency",
    display_name={"th": "ผลการถ่ายทอดยีนบนโครโมโซมเพศและหมู่เลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=LINKAGE_TOPIC,
)
class SexLinkageFluency(QuestionType):
    """Work out one cross of each kind the indicator names."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            item = rng.choice(SEX_CROSSES)
            others = [other.outcome for other in SEX_CROSSES
                      if other.outcome != item.outcome]
            rng.shuffle(others)
            return _labelled(
                stem=f"ตาบอดสีถูกควบคุมด้วยแอลลีลด้อยบนโครโมโซม X "
                     f"ถ้า{item.parents} ลูกที่เกิดมาจะเป็นอย่างไร",
                correct=item.outcome, wrongs=tuple(others[:3]),
                hint="เขียนโครโมโซมเพศของพ่อแม่ออกมาก่อน "
                     "แล้วจำไว้ว่าลูกชายได้รับ X จากแม่เท่านั้น",
                topic=LINKAGE_TOPIC,
            )
        first, second = rng.choice(BLOOD_GENOTYPES), rng.choice(BLOOD_GENOTYPES)
        correct = _possible_groups(first, second)
        others = []
        for left in BLOOD_GENOTYPES:
            for right in BLOOD_GENOTYPES:
                value = _possible_groups(left, right)
                if value != correct and value not in others:
                    others.append(value)
        rng.shuffle(others)
        return _labelled(
            stem=f"หมู่เลือดระบบ ABO ควบคุมด้วยแอลลีล IA IB และ i "
                 f"ถ้าพ่อมีจีโนไทป์ {''.join(first)} และแม่มีจีโนไทป์ "
                 f"{''.join(second)} ลูกที่เกิดมาจะมีหมู่เลือดใดได้บ้าง",
            correct=correct, wrongs=tuple(others[:3]),
            hint="จับคู่แอลลีลจากพ่อกับแอลลีลจากแม่ให้ครบทุกแบบ "
                 "แล้วจึงแปลงแต่ละคู่เป็นหมู่เลือด",
            topic=LINKAGE_TOPIC,
        )


@question_type(
    "life.sex_linkage_application",
    display_name={"th": "วิเคราะห์การถ่ายทอดยีนบนโครโมโซมเพศและหมู่เลือด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=LINKAGE_TOPIC,
)
class SexLinkageApplication(QuestionType):
    """Reason backwards from children's phenotypes to the parents' alleles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, LINKAGE_SCENARIOS,
            hint="ลูกชายได้รับ X จากแม่เท่านั้น และลูกหมู่เลือด O "
                 "ต้องได้รับแอลลีล i จากทั้งพ่อและแม่",
        ), LINKAGE_TOPIC)

"""ยีนบนออโตโซมและโครโมโซมเพศ

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/5

Sets moved here from: science_wave_f49.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f48 import frac_text
from otk.sets._support.science_wave_f49 import SUBJECT, UPPER_FOUR, _frac_wrongs

PROVENANCE = Provenance("original")


TOPIC_CHROM = "ยีนบนออโตโซมและโครโมโซมเพศ"


LOCATIONS = {
    "ออโตโซม": ("ความสามารถในการห่อลิ้น", "การมีลักยิ้ม", "หมู่เลือดระบบ ABO", "ผิวเผือก", "ธาลัสซีเมีย", "การมีนิ้วเกิน"),
    "โครโมโซม X": ("ตาบอดสีแดงเขียว", "ฮีโมฟีเลีย", "ภาวะพร่องเอนไซม์ G-6-PD", "กล้ามเนื้อแขนขาลีบแบบดูเชนน์"),
    "โครโมโซม Y": ("การมีขนที่ใบหู", "การกำหนดให้เอ็มบริโอพัฒนาเป็นเพศชาย (ยีน SRY)"),
}


CHROM_FACTS = (
    ("โรคที่ควบคุมด้วยแอลลีลด้อยบนโครโมโซม X พบในเพศใดมากกว่า", "เพศชาย เพราะมีโครโมโซม X เพียงแท่งเดียว",
     ("เพศหญิง เพราะมีโครโมโซม X สองแท่ง", "พบเท่ากันทั้งสองเพศ", "พบเฉพาะเพศหญิง")),
    ("ลักษณะที่ควบคุมด้วยยีนบนโครโมโซม Y ถ่ายทอดอย่างไร", "จากพ่อไปยังลูกชายทุกคน",
     ("จากแม่ไปยังลูกชายทุกคน", "จากพ่อไปยังลูกสาวทุกคน", "ถ่ายทอดให้ลูกทุกคนไม่ว่าเพศใด")),
    ("ชายที่เป็นตาบอดสีได้รับแอลลีลตาบอดสีมาจากใคร", "แม่", ("พ่อ", "ทั้งพ่อและแม่", "ปู่ฝ่ายพ่อ")),
    ("ลักษณะที่ควบคุมด้วยยีนบนออโตโซมมีลักษณะการถ่ายทอดอย่างไร", "พบในเพศชายและเพศหญิงในโอกาสใกล้เคียงกัน",
     ("พบเฉพาะในเพศชาย", "ถ่ายทอดจากพ่อสู่ลูกชายเท่านั้น", "พบในเพศชายมากกว่าเพศหญิงเสมอ")),
    ("ในเซลล์ร่างกายของคนมีออโตโซมกี่แท่ง", "44 แท่ง (22 คู่)", ("46 แท่ง (23 คู่)", "22 แท่ง", "23 แท่ง")),
)


LOC_HINT = "ยีนบนออโตโซมพบในทั้งสองเพศพอ ๆ กัน ยีนด้อยบน X พบในชายมากกว่า ยีนบน Y ถ่ายทอดจากพ่อสู่ลูกชายเท่านั้น"


X_LINKED = ("ตาบอดสีแดงเขียว", "ฮีโมฟีเลีย", "ภาวะพร่องเอนไซม์ G-6-PD")


MOTHERS = ("XᴴXᴴ", "XᴴXʰ", "XʰXʰ")


FATHERS = ("XᴴY", "XʰY")


def x_children(mother: str, father: str) -> list[tuple[str, str]]:
    """Four equally likely children as (sex, genotype)."""
    m = [mother[:2], mother[2:]]
    f = [father[:2], father[2:]]
    kids = []
    for a, b in product(m, f):
        if b == "Y":
            kids.append(("son", a + "Y"))
        else:
            kids.append(("daughter", "".join(sorted((a, b), key=lambda x: x[1] != "ᴴ"))))
    return kids


def x_affected(genotype: str) -> bool:
    return "Xᴴ" not in genotype


def x_carrier(genotype: str) -> bool:
    return genotype == "XᴴXʰ"


AUTOSOMAL = ("ผิวเผือก", "ธาลัสซีเมีย", "ฟีนิลคีโตนูเรีย")


def pedigree_cases(x: str, a: str):
    return (
        (f"หญิงปกติที่มีพ่อเป็น{x}แต่งงานกับชายปกติ ถ้าได้ลูกชาย โอกาสที่ลูกชายเป็น{x}", Fraction(1, 2)),
        (f"หญิงปกติที่มีพ่อเป็น{x}แต่งงานกับชายปกติ ถ้าได้ลูกสาว โอกาสที่ลูกสาวเป็นพาหะ", Fraction(1, 2)),
        (f"หญิงปกติที่มีพ่อเป็น{x}แต่งงานกับชายที่เป็น{x} ถ้าได้ลูกสาว โอกาสที่ลูกสาวเป็น{x}", Fraction(1, 2)),
        (f"สามีภรรยาปกติมีลูกชายคนแรกเป็น{x} ถ้าลูกคนต่อไปเป็นชาย โอกาสที่เป็น{x}", Fraction(1, 2)),
        (f"สามีภรรยาปกติมีลูกชายคนแรกเป็น{x} ถ้าลูกคนต่อไปเป็นหญิง โอกาสที่เป็น{x}", Fraction(0)),
        (f"ชายที่เป็น{x}แต่งงานกับหญิงปกติที่ไม่มีแอลลีลนี้ ถ้าได้ลูกชาย โอกาสที่ลูกชายเป็น{x}", Fraction(0)),
        (f"ชายที่เป็น{x}แต่งงานกับหญิงปกติที่ไม่มีแอลลีลนี้ ถ้าได้ลูกสาว โอกาสที่ลูกสาวเป็นพาหะ", Fraction(1)),
        (f"ชายที่เป็น{x}แต่งงานกับหญิงปกติที่ไม่มีแอลลีลนี้ ลูกสาวของทั้งคู่แต่งงานกับชายปกติ ถ้าลูกสาวมีลูกชาย "
         f"โอกาสที่หลานชายเป็น{x}", Fraction(1, 2)),
        (f"สามีภรรยาปกติมีลูกคนแรกเป็น{a} โอกาสที่ลูกคนต่อไปเป็น{a}", Fraction(1, 4)),
        (f"สามีภรรยาปกติมีลูกคนแรกเป็น{a} โอกาสที่ลูกคนต่อไปเป็นพาหะ", Fraction(1, 2)),
        (f"สามีภรรยาปกติมีลูกคนแรกเป็น{a} ลูกคนที่สองมีฟีโนไทป์ปกติ โอกาสที่ลูกคนที่สองเป็นพาหะ", Fraction(2, 3)),
        (f"สามีภรรยาปกติมีลูกคนแรกเป็น{a} ถ้าลูกคนต่อไปเป็นชาย โอกาสที่เป็น{a}", Fraction(1, 4)),
        (f"คนที่เป็น{a}แต่งงานกับคนปกติที่เป็นพาหะ โอกาสที่ลูกเป็น{a}", Fraction(1, 2)),
        (f"คนที่เป็น{a}แต่งงานกับคนปกติที่ไม่มีแอลลีลนี้ โอกาสที่ลูกเป็นพาหะ", Fraction(1)),
    )


@question_type(
    "biology.chromosome_inheritance_foundation",
    display_name={"th": "ลักษณะที่ควบคุมด้วยยีนบนออโตโซมและโครโมโซมเพศ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CHROM,
)
class ChromosomeInheritanceFoundation(QuestionType):
    """Which chromosome a trait's gene sits on, and what that means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            where = rng.choice(sorted(LOCATIONS))
            wrongs = [t for w, ts in LOCATIONS.items() if w != where for t in ts]
            return _labelled(stem=f"ลักษณะใดถูกควบคุมด้วยยีนบน{where}", correct=rng.choice(LOCATIONS[where]),
                             wrongs=tuple(wrongs), topic=TOPIC_CHROM, hint=LOC_HINT)
        if roll < 0.7:
            where = rng.choice(sorted(LOCATIONS))
            trait = rng.choice(LOCATIONS[where])
            return _labelled(stem=f"{trait}ถูกควบคุมด้วยยีนบนโครโมโซมใด", correct=where,
                             wrongs=tuple([w for w in LOCATIONS if w != where] + ["DNA ในไมโทคอนเดรีย"]), topic=TOPIC_CHROM,
                             hint=LOC_HINT)
        stem, right, wrongs = rng.choice(CHROM_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_CHROM, hint=LOC_HINT)


@question_type(
    "biology.chromosome_inheritance_fluency",
    display_name={"th": "โอกาสเกิดลักษณะที่ควบคุมด้วยยีนบนโครโมโซม X"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CHROM,
)
class ChromosomeInheritanceFluency(QuestionType):
    """Sons take their X from the mother; daughters take one X from each parent."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        disease = rng.choice(X_LINKED)
        mother, father = rng.choice(MOTHERS), rng.choice(FATHERS)
        kids = x_children(mother, father)
        sons = [g for s, g in kids if s == "son"]
        daughters = [g for s, g in kids if s == "daughter"]
        asks = (
            ("ลูกที่เกิดมาเป็น" + disease, Fraction(sum(x_affected(g) for _, g in kids), 4)),
            ("ลูกที่เกิดมาเป็นลูกชายที่เป็น" + disease, Fraction(sum(x_affected(g) for g in sons), 4)),
            ("ถ้าได้ลูกชาย ลูกชายคนนั้นเป็น" + disease, Fraction(sum(x_affected(g) for g in sons), 2)),
            ("ถ้าได้ลูกสาว ลูกสาวคนนั้นเป็น" + disease, Fraction(sum(x_affected(g) for g in daughters), 2)),
            ("ถ้าได้ลูกสาว ลูกสาวคนนั้นเป็นพาหะ", Fraction(sum(x_carrier(g) for g in daughters), 2)),
        )
        ask, right = rng.choice(asks)
        if rng.random() < 0.5:
            mom = {"XᴴXᴴ": "หญิงปกติที่ไม่มีแอลลีลนี้", "XᴴXʰ": "หญิงปกติที่เป็นพาหะ", "XʰXʰ": f"หญิงที่เป็น{disease}"}[mother]
            dad = {"XᴴY": "ชายปกติ", "XʰY": f"ชายที่เป็น{disease}"}[father]
            parents = f"{dad}แต่งงานกับ{mom}"
        else:
            parents = f"แม่มีจีโนไทป์ {mother} พ่อมีจีโนไทป์ {father}"
        return _labelled(stem=f"ให้ Xʰ เป็นแอลลีลด้อยที่ทำให้เกิด{disease} {parents} โอกาสที่{ask}เท่ากับเท่าใด",
                         correct=frac_text(right), wrongs=_frac_wrongs(rng, right), topic=TOPIC_CHROM,
                         hint="ลูกชายได้ X จากแม่และ Y จากพ่อ ลูกสาวได้ X จากทั้งพ่อและแม่ เขียนตารางแล้วนับ")


@question_type(
    "biology.chromosome_inheritance_application",
    display_name={"th": "วิเคราะห์การถ่ายทอดโรคทางพันธุกรรมในครอบครัว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CHROM,
)
class ChromosomeInheritanceApplication(QuestionType):
    """Work out the parents' genotypes from the family first, then the chance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        x, a = rng.choice(X_LINKED), rng.choice(AUTOSOMAL)
        stem, right = rng.choice(pedigree_cases(x, a))
        return _labelled(stem=f"{x}ควบคุมด้วยแอลลีลด้อยบนโครโมโซม X ส่วน{a}ควบคุมด้วยแอลลีลด้อยบนออโตโซม {stem}เท่ากับเท่าใด",
                         correct=frac_text(right), wrongs=_frac_wrongs(rng, right), topic=TOPIC_CHROM,
                         hint="หาจีโนไทป์ของพ่อแม่จากข้อมูลครอบครัวก่อน ยีนบน X ลูกชายได้จากแม่ ยีนบนออโตโซมไม่ขึ้นกับเพศ")

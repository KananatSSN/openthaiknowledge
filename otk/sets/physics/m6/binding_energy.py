"""แรงนิวเคลียร์ เสถียรภาพของนิวเคลียส และพลังงานยึดเหนี่ยว

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/15

Sets moved here from: science_wave_f18.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f18 import SUBJECT, U_MEV, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_BINDING = "แรงนิวเคลียร์ เสถียรภาพของนิวเคลียส และพลังงานยึดเหนี่ยว"


BINDING_FACTS = (
    ("แรงนิวเคลียร์มีลักษณะอย่างไร", "เป็นแรงดึงดูดที่มีค่ามากมากแต่กระทำในระยะสั้นมากระหว่างนิวคลีออน",
     ("เป็นแรงผลักระหว่างโปรตอนเท่านั้น", "กระทำในระยะไกลเหมือนแรงโน้มถ่วง", "อ่อนกว่าแรงไฟฟ้าเสมอ")),
    ("มวลของนิวเคลียสน้อยกว่าผลรวมมวลของนิวคลีออนที่แยกกันอยู่ ผลต่างนี้เรียกว่าอะไร", "มวลพร่อง",
     ("มวลอะตอม", "เลขมวล", "มวลโมเลกุล")),
    ("พลังงานยึดเหนี่ยวต่อนิวคลีออนที่มากหมายความว่าอย่างไร", "นิวเคลียสมีเสถียรภาพมาก แยกนิวคลีออนออกได้ยาก",
     ("นิวเคลียสไม่เสถียร สลายง่าย", "นิวเคลียสมีมวลน้อยที่สุด", "นิวเคลียสไม่มีนิวตรอน")),
    ("นิวเคลียสใดมีพลังงานยึดเหนี่ยวต่อนิวคลีออนสูงที่สุดโดยประมาณ", "เหล็ก-56",
     ("ยูเรเนียม-238", "ไฮโดรเจน-1", "ฮีเลียม-3")),
    ("นิวเคลียสหนักที่มีโปรตอนมากต้องมีนิวตรอนมากกว่าโปรตอนจึงจะเสถียร เพราะเหตุใด", "นิวตรอนเพิ่มแรงนิวเคลียร์โดยไม่เพิ่มแรงผลักทางไฟฟ้า",
     ("นิวตรอนมีประจุลบหักล้างโปรตอน", "นิวตรอนมีมวลน้อยกว่า", "นิวตรอนผลักโปรตอนออก")),
)


NUCLEI = (("ฮีเลียม-4", 4, Fraction(2832, 100)), ("ลิเทียม-7", 7, Fraction(392, 10)), ("คาร์บอน-12", 12, Fraction(9216, 100)),
          ("ออกซิเจน-16", 16, Fraction(12768, 100)), ("เหล็ก-56", 56, Fraction(49224, 100)),
          ("ยูเรเนียม-238", 238, Fraction(180166, 100)))


@question_type(
    "phys.binding_energy_foundation",
    display_name={"th": "แรงนิวเคลียร์ มวลพร่อง และเสถียรภาพของนิวเคลียส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BINDING,
)
class BindingEnergyFoundation(QuestionType):
    """What holds a nucleus together, and E = Δm × 931 MeV."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(BINDING_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_BINDING,
                             hint="มวลพร่องเปลี่ยนเป็นพลังงานยึดเหนี่ยว E = Δm × 931 MeV ยิ่งพลังงานต่อนิวคลีออนมาก ยิ่งเสถียร")
        dm = Fraction(rng.randint(1, 250), 100)
        return numeric(
            stem=f"นิวเคลียสหนึ่งมีมวลพร่อง {show(dm)} u มีพลังงานยึดเหนี่ยวกี่เมกะอิเล็กตรอนโวลต์ (1 u = 931 MeV)",
            answer=dm * U_MEV, wrongs=[dm * U_MEV * 10, Fraction(U_MEV) / dm if dm >= 1 else dm * 93, dm * U_MEV / 2],
            unit="MeV", topic=TOPIC_BINDING, hint="E = Δm × 931 MeV")


@question_type(
    "phys.binding_energy_fluency",
    display_name={"th": "คำนวณพลังงานยึดเหนี่ยวต่อนิวคลีออน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BINDING,
)
class BindingEnergyFluency(QuestionType):
    """Binding energy per nucleon = E/A, and E back from it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, a, total = rng.choice(NUCLEI)
        else:
            a = rng.randint(10, 240)
            total = a * Fraction(rng.randint(60, 88), 10)
            name = f" X (เลขมวล {a})"
        per = total / a
        if rng.random() < 0.55:
            return numeric(
                stem=f"นิวเคลียส{name}มีพลังงานยึดเหนี่ยว {show(total)} MeV มีพลังงานยึดเหนี่ยวต่อนิวคลีออนเท่าใด",
                answer=per, wrongs=[total, per * 2, total / (a // 2 or 1)], unit="MeV", topic=TOPIC_BINDING,
                hint="พลังงานยึดเหนี่ยวต่อนิวคลีออน = พลังงานยึดเหนี่ยว ÷ เลขมวล")
        return numeric(
            stem=f"นิวเคลียส{name} (เลขมวล {a}) มีพลังงานยึดเหนี่ยวต่อนิวคลีออน {show(per)} MeV มีพลังงานยึดเหนี่ยวทั้งหมดเท่าใด",
            answer=total, wrongs=[per, total / 2, total * 2], unit="MeV", topic=TOPIC_BINDING,
            hint="พลังงานยึดเหนี่ยว = ต่อนิวคลีออน × เลขมวล")


@question_type(
    "phys.binding_energy_application",
    display_name={"th": "เปรียบเทียบเสถียรภาพของนิวเคลียสจากพลังงานยึดเหนี่ยว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BINDING,
)
class BindingEnergyApplication(QuestionType):
    """The larger energy per nucleon is the more stable nucleus, not the larger total."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            items = []
            for label in ("X", "Y", "Z"):
                a = rng.randint(4, 240)
                per = Fraction(rng.randint(50, 88), 10)
                items.append((label, a, per))
            if len({p for _, _, p in items}) == 3:
                break
        best = max(items, key=lambda t: t[2])[0]
        listed = " ".join(f"{ell} มีเลขมวล {a} และพลังงานยึดเหนี่ยว {show(a * p)} MeV" for ell, a, p in items)
        return _labelled(
            stem=f"นิวเคลียส {listed} นิวเคลียสใดเสถียรที่สุด",
            correct=f"นิวเคลียส {best}",
            wrongs=tuple(f"นิวเคลียส {ell}" for ell, _, _ in items if ell != best) + ("เสถียรเท่ากันทั้งสาม",),
            topic=TOPIC_BINDING, hint="เทียบพลังงานยึดเหนี่ยวต่อนิวคลีออน (หารด้วยเลขมวล) ไม่ใช่พลังงานยึดเหนี่ยวรวม")

"""สูตรโครงสร้างลิวอิส สูตรโครงสร้างแบบย่อ และสูตรโครงสร้างแบบเส้น

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/2

Sets moved here from: science_wave_f26.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f26 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_FORMULA = "สูตรโครงสร้างลิวอิส สูตรโครงสร้างแบบย่อ และสูตรโครงสร้างแบบเส้น"


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


END_GROUPS = {None: (0, {}), "OH": (1, {"O": 1}), "Cl": (0, {"Cl": 1}), "Br": (0, {"Br": 1}), "NH₂": (2, {"N": 1})}


def chain(n: int, branch: int | None = None, end: str | None = None, double: bool = False):
    """A carbon chain as (condensed formula, compressed formula, atoms).

    ``branch`` puts a methyl on that carbon; ``end`` replaces an H on the last
    carbon; ``double`` makes C1=C2.
    """
    hydrogens = [3] + [2] * (n - 2) + [3] if n > 1 else [4]
    if branch:
        hydrogens[branch - 1] -= 1
    if end:
        hydrogens[-1] -= 1
    if double:
        hydrogens[0] -= 1
        hydrogens[1] -= 1
    parts = []
    for i, h in enumerate(hydrogens):
        part = "C" + ("H" + (str(h).translate(SUB) if h > 1 else "") if h else "")
        if branch == i + 1:
            part += "(CH₃)"
        parts.append(part)
    body = [p + ("=" if double and i == 0 else "") for i, p in enumerate(parts)]
    condensed = "".join(body) + (end or "")
    # Compress runs of two or more CH₂ that sit between other carbons.
    compressed, run = "", 0
    for p in body:
        if p == "CH₂":
            run += 1
            continue
        if run:
            compressed += "CH₂" if run == 1 else f"(CH₂){str(run).translate(SUB)}"
            run = 0
        compressed += p
    if run:
        compressed += "CH₂" if run == 1 else f"(CH₂){str(run).translate(SUB)}"
    compressed += end or ""
    extra_h, others = END_GROUPS[end]
    atoms = {"C": n + (1 if branch else 0), "H": sum(hydrogens) + (3 if branch else 0) + extra_h, **others}
    return condensed, compressed, atoms


def molecular(atoms: dict) -> str:
    order = ["C", "H"] + sorted(k for k in atoms if k not in ("C", "H"))
    return "".join(k + (str(atoms[k]).translate(SUB) if atoms[k] > 1 else "") for k in order if atoms.get(k))


def random_chain(rng: Random):
    n = rng.randint(2, 7)
    branch = rng.randint(2, n - 1) if n >= 4 and rng.random() < 0.4 else None
    end = rng.choice((None, None, "OH", "Cl", "Br", "NH₂"))
    double = n >= 3 and not branch and rng.random() < 0.25
    return n, branch, end, double


@question_type(
    "chem.structural_formula_foundation",
    display_name={"th": "สูตรโมเลกุลจากสูตรโครงสร้างแบบย่อ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class StructuralFormulaFoundation(QuestionType):
    """Count every atom in the condensed formula, branches included."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n, branch, end, double = random_chain(rng)
        condensed, _, atoms = chain(n, branch, end, double)
        right = molecular(atoms)
        pool = set()
        for dh in (-2, -1, 1, 2):
            if atoms["H"] + dh > 0:
                pool.add(molecular({**atoms, "H": atoms["H"] + dh}))
        pool.add(molecular({**atoms, "C": atoms["C"] + 1}))
        if atoms["C"] > 1:
            pool.add(molecular({**atoms, "C": atoms["C"] - 1}))
        pool.discard(right)
        return _labelled(stem=f"สารที่มีสูตรโครงสร้างแบบย่อ {condensed} มีสูตรโมเลกุลใด", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_FORMULA,
                         hint="นับ C และ H ของทุกหน่วยในสูตร รวมกิ่งในวงเล็บและหมู่ที่ปลายสาย")


@question_type(
    "chem.structural_formula_fluency",
    display_name={"th": "เขียนสูตรโครงสร้างแบบย่อให้สั้นลงและนับพันธะในสูตรลิวอิส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class StructuralFormulaFluency(QuestionType):
    """(CH₂)ₙ shortens a run; a Lewis structure shows every C–H bond."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            n = rng.randint(5, 9)
            end = rng.choice((None, "OH", "Cl", "NH₂"))
            condensed, compressed, _ = chain(n, None, end)
            run = n - 1 if end else n - 2
            wrong = {compressed.replace(f"(CH₂){str(run).translate(SUB)}", f"(CH₂){str(k).translate(SUB)}")
                     for k in (run - 1, run + 1, run + 2)}
            wrong.discard(compressed)
            return _labelled(stem=f"{condensed} เขียนเป็นสูตรโครงสร้างแบบย่อที่สั้นลงได้อย่างไร", correct=compressed,
                             wrongs=tuple(sorted(wrong))[:3], topic=TOPIC_FORMULA,
                             hint="นับ CH₂ ที่ต่อกันตรงกลางสาย แล้วเขียนเป็น (CH₂)ₙ")
        n, branch, end, double = random_chain(rng)
        condensed, _, atoms = chain(n, branch, end, double)
        c_h = atoms["H"] - END_GROUPS[end][0]
        return numeric(stem=f"ถ้าเขียนสูตรโครงสร้างลิวอิสของ {condensed} จะมีพันธะ C–H ทั้งหมดกี่พันธะ", answer=c_h,
                       wrongs=[atoms["H"] + 1 if atoms["H"] != c_h else c_h + 1, c_h - 1, atoms["C"]], unit="พันธะ",
                       topic=TOPIC_FORMULA, hint="H แต่ละอะตอมที่ต่อกับ C คือ 1 พันธะ C–H (H ใน OH และ NH₂ ไม่นับ)")


@question_type(
    "chem.structural_formula_application",
    display_name={"th": "สูตรโครงสร้างแบบเส้น"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class StructuralFormulaApplication(QuestionType):
    """In a line formula every end and corner is a carbon, and its H are left out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randint(3, 8)
        kind = rng.randrange(3)
        hint = ("ในสูตรแบบเส้น จุดปลายและจุดหักมุมแต่ละจุดคือ C หนึ่งอะตอม ไม่เขียน H ที่ต่อกับ C "
                "แต่ต้องเขียนอะตอมอื่นเช่น O N Cl")
        if kind == 0:
            end = rng.choice((None, "OH", "Cl"))
            condensed, _, _ = chain(n, None, end)
            return numeric(stem=f"สูตรโครงสร้างแบบเส้นของ {condensed} มีจุดปลายและจุดหักมุมที่แทนอะตอมคาร์บอนกี่จุด",
                           answer=n, wrongs=[n + 1, n - 1, n + (1 if end else 2)], unit="จุด", topic=TOPIC_FORMULA,
                           hint=hint)
        if kind == 1:
            double = rng.random() < 0.4
            end = rng.choice((None, "OH")) if not double else None
            _, _, atoms = chain(n, None, end, double)
            words = f"เส้นซิกแซกที่มีจุดปลายและจุดหักมุมรวม {n} จุด ไม่มีกิ่ง"
            if double:
                words += " มีเส้นคู่ระหว่างจุดที่ 1 และ 2"
            if end:
                words += " และมี OH ที่ปลายด้านหนึ่ง"
            right = molecular(atoms)
            pool = {molecular({**atoms, "H": atoms["H"] + d}) for d in (-2, 2, 4)}
            pool |= {molecular({**atoms, "C": atoms["C"] + 1})}
            pool.discard(right)
            return _labelled(stem=f"สูตรโครงสร้างแบบเส้นเป็น{words} สารนี้มีสูตรโมเลกุลใด", correct=right,
                             wrongs=tuple(sorted(pool)), topic=TOPIC_FORMULA, hint=hint)
        facts = (
            ("ในสูตรโครงสร้างแบบเส้น อะตอมใดที่ไม่ต้องเขียนสัญลักษณ์", "C และ H ที่ต่อกับ C",
             ("O และ N", "ทุกอะตอมยกเว้น C", "เฉพาะ H ใน OH")),
            ("สูตรโครงสร้างแบบใดแสดงอิเล็กตรอนคู่โดดเดี่ยวได้ครบ", "สูตรโครงสร้างลิวอิส",
             ("สูตรโครงสร้างแบบย่อ", "สูตรโครงสร้างแบบเส้น", "สูตรโมเลกุล")),
            ("ในสูตรโครงสร้างแบบเส้น เส้นคู่แทนอะไร", "พันธะคู่ระหว่างอะตอมคาร์บอน",
             ("คาร์บอนสองอะตอมซ้อนกัน", "หมู่ CH₂ สองหมู่", "พันธะไฮโดรเจน")),
            ("สูตรโครงสร้างแบบเส้นของเฮกเซนไม่มีกิ่งมีจุดปลายและจุดหักมุมกี่จุด", "6 จุด", ("5 จุด", "7 จุด", "14 จุด")),
        )
        stem, right, wrongs = rng.choice(facts)
        if rng.random() < 0.6:
            condensed, _, atoms = chain(n, rng.randint(2, n - 1) if n >= 4 else None)
            return _labelled(stem=f"สาร {condensed} มีสูตรโครงสร้างแบบเส้นเป็นเส้นซิกแซกที่มีกิ่งหรือไม่ และมีคาร์บอนกี่อะตอม",
                             correct=f"{'มีกิ่ง 1 กิ่ง' if '(' in condensed else 'ไม่มีกิ่ง'} คาร์บอน {atoms['C']} อะตอม",
                             wrongs=tuple(rng.sample([f"{b} คาร์บอน {c} อะตอม" for b in ("มีกิ่ง 1 กิ่ง", "ไม่มีกิ่ง")
                                                      for c in (atoms['C'] - 1, atoms['C'], atoms['C'] + 1)
                                                      if (b == "มีกิ่ง 1 กิ่ง") != ('(' in condensed) or c != atoms['C']], 3)),
                             topic=TOPIC_FORMULA, hint=hint)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_FORMULA, hint=hint)

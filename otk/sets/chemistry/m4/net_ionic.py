"""สมการไอออนิกและสมการไอออนิกสุทธิ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/13

Sets moved here from: science_wave_f21.
"""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f21 import ANIONS, CATIONS, SUBJECT, UPPER_FOUR, formula, ion

PROVENANCE = Provenance("original")


TOPIC_NET = "สมการไอออนิกและสมการไอออนิกสุทธิ"


# Soluble sources: (cation entry, partner anion for its soluble salt) and (anion entry, partner cation).
CATION_SOURCES = (("Ag", "NO₃"), ("Ba", "Cl"), ("Ba", "NO₃"), ("Pb", "NO₃"), ("Ca", "Cl"), ("Ca", "NO₃"), ("Cu", "SO₄"),
                  ("Cu", "NO₃"), ("Fe", "Cl"), ("Mg", "Cl"), ("Mg", "NO₃"), ("Zn", "NO₃"), ("Zn", "SO₄"), ("Al", "Cl"))


ANION_SOURCES = (("Cl", "Na"), ("SO₄", "Na"), ("SO₄", "K"), ("CO₃", "Na"), ("CO₃", "K"), ("OH", "Na"), ("OH", "K"),
                 ("I", "K"), ("Br", "K"), ("PO₄", "Na"), ("S", "Na"))


def _find_cation(symbol: str, charge: int | None = None):
    return next(c for c in CATIONS if c[0] == symbol and (charge is None or c[2] == charge))


def _find_anion(symbol: str):
    return next(a for a in ANIONS if a[0] == symbol)


def insoluble(cation, anion) -> bool:
    c, a = cation[0], anion[0]
    if c in ("Na", "K", "Li", "NH₄") or a == "NO₃":
        return False
    if a in ("Cl", "Br", "I"):
        return c in ("Ag", "Pb")
    if a == "SO₄":
        return c in ("Ba", "Pb")
    if a == "OH":
        # Ba(OH)₂ dissolves and Ca(OH)₂ only slightly; silver gives an oxide instead.
        return c in ("Mg", "Fe", "Cu", "Zn", "Al", "Pb")
    return a in ("CO₃", "PO₄", "S")


def _reaction(rng: Random):
    while True:
        csym, cpartner = rng.choice(CATION_SOURCES)
        cation = _find_cation(csym, 3 if csym == "Fe" else (2 if csym in ("Cu", "Pb") else None))
        asym, apartner = rng.choice(ANION_SOURCES)
        anion = _find_anion(asym)
        salt1 = formula(cation, _find_anion(cpartner))
        salt2 = formula(_find_cation(apartner), anion)
        # Al³⁺ and Fe³⁺ with carbonate or sulfide hydrolyse or react on instead of giving that salt.
        awkward = cation[0] in ("Al", "Fe") and anion[0] in ("CO₃", "S")
        if insoluble(cation, anion) and not insoluble(cation, _find_anion(cpartner)) and cpartner != asym and not awkward:
            return cation, anion, salt1, salt2, _find_anion(cpartner), _find_cation(apartner)


def net_ionic(cation, anion) -> str:
    p, q = cation[2], anion[2]
    k = gcd(p, q)
    nc, na = q // k, p // k
    lead = lambda n: "" if n == 1 else f"{n}"
    return f"{lead(nc)}{ion(cation, 1)}(aq) + {lead(na)}{ion(anion, -1)}(aq) → {formula(cation, anion)}(s)"


@question_type(
    "chem.net_ionic_foundation",
    display_name={"th": "ระบุตะกอนจากการผสมสารละลายไอออนิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NET,
)
class NetIonicFoundation(QuestionType):
    """Which product falls out of solution, by the solubility rules."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion, salt1, salt2, partner_a, partner_c = _reaction(rng)
        right = formula(cation, anion)
        pool = {formula(partner_c, partner_a), salt1, salt2}
        pool.discard(right)
        while len(pool) < 3:
            pool.add("ไม่เกิดตะกอน")
        return _labelled(stem=f"ผสมสารละลาย {salt1} กับสารละลาย {salt2} ตะกอนที่เกิดขึ้นคือสารใด", correct=right,
                         wrongs=tuple(sorted(pool))[:3], topic=TOPIC_NET,
                         hint="สารประกอบของ Na⁺ K⁺ NH₄⁺ และ NO₃⁻ ละลายน้ำทั้งหมด AgCl PbCl₂ BaSO₄ และคาร์บอเนตหรือไฮดรอกไซด์ของโลหะอื่นเป็นตะกอน")


@question_type(
    "chem.net_ionic_fluency",
    display_name={"th": "เขียนสมการไอออนิกสุทธิของปฏิกิริยาการเกิดตะกอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NET,
)
class NetIonicFluency(QuestionType):
    """Only the ions that form the precipitate appear, balanced for charge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion, salt1, salt2, partner_a, partner_c = _reaction(rng)
        right = net_ionic(cation, anion)
        pool = {
            f"{ion(cation, 1)}(aq) + {ion(anion, -1)}(aq) → {formula(cation, anion)}(s)",
            f"{ion(partner_c, 1)}(aq) + {ion(partner_a, -1)}(aq) → {formula(partner_c, partner_a)}(s)",
            f"{salt1}(aq) + {salt2}(aq) → {formula(cation, anion)}(s)",
            f"{ion(cation, 1)}(aq) + {ion(anion, -1)}(aq) → {formula(cation, anion)}(aq)",
        }
        pool.discard(right)
        return _labelled(stem=f"ผสมสารละลาย {salt1} กับ {salt2} สมการไอออนิกสุทธิคือข้อใด", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_NET,
                         hint="เขียนเฉพาะไอออนที่รวมกันเป็นตะกอน ตัดไอออนที่ไม่เปลี่ยนแปลงออก แล้วดุลประจุ")


@question_type(
    "chem.net_ionic_application",
    display_name={"th": "ไอออนที่ไม่เปลี่ยนแปลงในปฏิกิริยา (spectator ions)"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NET,
)
class NetIonicApplication(QuestionType):
    """The ions left in solution on both sides are the spectators."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cation, anion, salt1, salt2, partner_a, partner_c = _reaction(rng)
        right = f"{ion(partner_c, 1)} และ {ion(partner_a, -1)}"
        pool = {f"{ion(cation, 1)} และ {ion(anion, -1)}", f"{ion(cation, 1)} และ {ion(partner_a, -1)}",
                f"{ion(partner_c, 1)} และ {ion(anion, -1)}"}
        pool.discard(right)
        return _labelled(stem=f"ผสมสารละลาย {salt1} กับ {salt2} ไอออนใดไม่เปลี่ยนแปลง (spectator ions)", correct=right,
                         wrongs=tuple(sorted(pool)), topic=TOPIC_NET,
                         hint="ไอออนที่รวมกันเป็นตะกอนเปลี่ยนแปลง ไอออนที่ยังอยู่ในสารละลายทั้งก่อนและหลังคือ spectator ions")

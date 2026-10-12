"""ส่วนขยายของพันธุศาสตร์เมนเดล

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/3

Sets moved here from: science_wave_f49.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f48 import frac_text, offspring
from otk.sets._support.science_wave_f49 import SUBJECT, UPPER_FOUR, _frac_wrongs

PROVENANCE = Provenance("original")


TOPIC_EXT = "ส่วนขยายของพันธุศาสตร์เมนเดล"


PATTERNS = {
    "ลักษณะเด่นไม่สมบูรณ์": (
        "ดอกลิ้นมังกรสีแดงพันธุ์แท้ผสมกับสีขาวพันธุ์แท้ ได้ลูกสีชมพูทั้งหมด",
        "ดอกบานเย็นสีแดงพันธุ์แท้ผสมกับสีขาวพันธุ์แท้ ได้ F₂ สีแดง : ชมพู : ขาว = 1 : 2 : 1",
        "คนผมหยิกแต่งงานกับคนผมเหยียดตรง ได้ลูกผมหยักศก",
        "ไก่อันดาลูเชียนขนดำพันธุ์แท้ผสมกับขนขาวพันธุ์แท้ ได้ลูกขนสีเทาอมฟ้าทั้งหมด",
    ),
    "การข่มร่วมกัน": (
        "คนที่มีจีโนไทป์ IᴬIᴮ มีแอนติเจน A และแอนติเจน B บนเซลล์เม็ดเลือดแดงพร้อมกัน",
        "วัวขนแดงพันธุ์แท้ผสมกับวัวขนขาวพันธุ์แท้ ได้ลูกที่มีทั้งขนสีแดงและขนสีขาวแซมกัน",
        "คนหมู่เลือด MN มีทั้งแอนติเจน M และแอนติเจน N บนเซลล์เม็ดเลือดแดง",
    ),
    "มัลติเปิลแอลลีล": (
        "หมู่เลือดระบบ ABO ถูกควบคุมด้วยยีนตำแหน่งเดียวที่มีแอลลีล Iᴬ Iᴮ และ i",
        "สีขนกระต่ายถูกควบคุมด้วยยีนตำแหน่งเดียวที่มีแอลลีล 4 แบบ",
        "ยีนตำแหน่งหนึ่งในประชากรมีแอลลีลมากกว่า 2 แบบ แต่แต่ละคนมีได้เพียง 2 แอลลีล",
    ),
    "พอลิยีน": (
        "สีผิวของคนถูกควบคุมด้วยยีนหลายคู่ ทำให้มีสีผิวหลายระดับ",
        "ความสูงของคนถูกควบคุมด้วยยีนหลายคู่ร่วมกับสิ่งแวดล้อม",
        "สีเมล็ดข้าวสาลีมีตั้งแต่สีแดงเข้มจนถึงสีขาว ตามจำนวนแอลลีลที่ทำให้เกิดสี",
    ),
    "ยีนที่ควบคุมหลายลักษณะ (พลีโอโทรปี)": (
        "แอลลีลของโรคโลหิตจางชนิดเซลล์รูปเคียวทำให้ทั้งโลหิตจาง ปวดข้อ และอวัยวะหลายแห่งเสียหาย",
        "ยีนเดียวที่ผิดปกติในกลุ่มอาการมาร์แฟนส่งผลต่อทั้งกระดูก ตา และหลอดเลือด",
    ),
}


PATTERN_HINT = ("เด่นไม่สมบูรณ์ได้ลักษณะกึ่งกลาง ข่มร่วมกันแสดงทั้งสองแบบพร้อมกัน มัลติเปิลแอลลีลมีมากกว่า 2 แอลลีล "
                "พอลิยีนคือยีนหลายคู่ควบคุมลักษณะเดียว พลีโอโทรปีคือยีนเดียวส่งผลหลายลักษณะ")


INCOMPLETE = (
    ("ดอกลิ้นมังกร", "ต้น", "ดอกสีแดง", "ดอกสีชมพู", "ดอกสีขาว"),
    ("ดอกบานเย็น", "ต้น", "ดอกสีแดง", "ดอกสีชมพู", "ดอกสีขาว"),
    ("ไก่อันดาลูเชียน", "ตัว", "ขนสีดำ", "ขนสีเทาอมฟ้า", "ขนสีขาว"),
)


BLOOD = {"A": "Iᴬ", "B": "Iᴮ", "O": "i"}


BLOOD_GENOTYPES = (("A", "A"), ("A", "O"), ("B", "B"), ("B", "O"), ("A", "B"), ("O", "O"))


def blood_group(pair) -> str:
    s = set(pair)
    return "AB" if s == {"A", "B"} else ("A" if "A" in s else ("B" if "B" in s else "O"))


def blood_text(pair) -> str:
    return "".join(BLOOD[a] for a in pair)


def blood_children(p1, p2) -> dict[str, Fraction]:
    out: dict[str, Fraction] = {}
    for a, b in product(p1, p2):
        g = blood_group((a, b))
        out[g] = out.get(g, 0) + Fraction(1, 4)
    return out


def possible_groups(phenotype1: str, phenotype2: str) -> frozenset[str]:
    groups = set()
    for g1 in BLOOD_GENOTYPES:
        for g2 in BLOOD_GENOTYPES:
            if blood_group(g1) == phenotype1 and blood_group(g2) == phenotype2:
                groups |= set(blood_children(g1, g2))
    return frozenset(groups)


def groups_text(groups) -> str:
    order = [g for g in ("A", "B", "AB", "O") if g in groups]
    return "หมู่ " + " หรือ ".join(order)


@question_type(
    "biology.mendel_extension_foundation",
    display_name={"th": "รูปแบบการถ่ายทอดที่ขยายจากกฎของเมนเดล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXT,
)
class MendelExtensionFoundation(QuestionType):
    """Name the pattern from an example, or pick the example of a pattern."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pattern = rng.choice(sorted(PATTERNS))
        example = rng.choice(PATTERNS[pattern])
        others = [p for p in PATTERNS if p != pattern]
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{example}\" เป็นการถ่ายทอดลักษณะแบบใด", correct=pattern,
                             wrongs=tuple(others), topic=TOPIC_EXT, hint=PATTERN_HINT)
        wrongs = [rng.choice(PATTERNS[p]) for p in rng.sample(others, 3)]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{pattern}", correct=example, wrongs=tuple(wrongs), topic=TOPIC_EXT,
                         hint=PATTERN_HINT)


@question_type(
    "biology.mendel_extension_fluency",
    display_name={"th": "จำนวนลูกแต่ละลักษณะเมื่อข่มไม่สมบูรณ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXT,
)
class MendelExtensionFluency(QuestionType):
    """With incomplete dominance each genotype shows its own phenotype: 1 : 2 : 1."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        organism, unit, red, mid, white = rng.choice(INCOMPLETE)
        names = {"RR": red, "Rr": mid, "rr": white}
        p1, p2 = rng.choice(("RR", "Rr", "rr")), rng.choice(("Rr", "Rr", "rr", "RR"))
        kids = offspring(p1, p2)
        target = rng.choice(sorted(names))
        total = rng.randrange(40, 1001, 4)
        answer = total * kids.get(target, Fraction(0))
        if answer == 0:
            target = max(kids, key=lambda k: kids[k])
            answer = total * kids[target]
        described = rng.random() < 0.5
        left = names[p1] if described else f"จีโนไทป์ {p1} ({names[p1]})"
        right = names[p2] if described else f"จีโนไทป์ {p2} ({names[p2]})"
        return numeric(stem=f"{organism}{red}พันธุ์แท้ผสมกับ{white}พันธุ์แท้ ได้ลูก{mid}ทั้งหมด (ลักษณะเด่นไม่สมบูรณ์) "
                            f"ถ้าผสม{organism}{left} กับ{right} ได้ลูก {total} {unit} คาดว่าจะมี{names[target]}กี่{unit}",
                       answer=answer, wrongs=[total * Fraction(3, 4), Fraction(total, 4) if answer != Fraction(total, 4) else Fraction(total, 2), total - answer],
                       unit=unit, topic=TOPIC_EXT,
                       hint="เมื่อข่มไม่สมบูรณ์ แต่ละจีโนไทป์มีฟีโนไทป์ของตัวเอง ลูก Rr × Rr ได้ RR : Rr : rr = 1 : 2 : 1")


@question_type(
    "biology.mendel_extension_application",
    display_name={"th": "การถ่ายทอดหมู่เลือดระบบ ABO"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXT,
)
class MendelExtensionApplication(QuestionType):
    """Iᴬ and Iᴮ are codominant, both dominant over i; three alleles, six genotypes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "Iᴬ และ Iᴮ ข่มร่วมกัน ทั้งสองข่ม i หมู่ A คือ IᴬIᴬ หรือ Iᴬi หมู่ B คือ IᴮIᴮ หรือ Iᴮi หมู่ AB คือ IᴬIᴮ หมู่ O คือ ii"
        if rng.random() < 0.55:
            g1, g2 = rng.choice(BLOOD_GENOTYPES), rng.choice(BLOOD_GENOTYPES)
            kids = blood_children(g1, g2)
            target = rng.choice(("A", "B", "AB", "O"))
            if target not in kids and rng.random() < 0.6:
                target = rng.choice(sorted(kids))
            right = kids.get(target, Fraction(0))
            return _labelled(stem=f"พ่อมีจีโนไทป์ {blood_text(g1)} แม่มีจีโนไทป์ {blood_text(g2)} โอกาสที่ลูกมีหมู่เลือด {target} เท่ากับเท่าใด",
                             correct=frac_text(right), wrongs=_frac_wrongs(rng, right), topic=TOPIC_EXT, hint=hint)
        phenotypes = ("A", "B", "AB", "O")
        f, m = rng.choice(phenotypes), rng.choice(phenotypes)
        groups = possible_groups(f, m)
        subsets = {frozenset(c) for n in range(1, 5) for c in combinations(phenotypes, n)} - {groups}
        near = sorted(subsets, key=lambda s: (len(s ^ groups), sorted(s)))[:6]
        return _labelled(stem=f"พ่อมีหมู่เลือด {f} แม่มีหมู่เลือด {m} (ไม่ทราบจีโนไทป์) ลูกอาจมีหมู่เลือดใดได้บ้าง",
                         correct=groups_text(groups), wrongs=tuple(groups_text(s) for s in rng.sample(near, 3)),
                         topic=TOPIC_EXT, hint=hint + " ให้พิจารณาทุกจีโนไทป์ที่พ่อแม่เป็นได้")

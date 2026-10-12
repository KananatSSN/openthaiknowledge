"""กฎแห่งการแยกและกฎแห่งการรวมกลุ่มอย่างอิสระ

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/2

Sets moved here from: science_wave_f48.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f48 import SUBJECT, UPPER_FOUR, frac_text, gametes, offspring

PROVENANCE = Provenance("original")


TOPIC_LAWS = "กฎแห่งการแยกและกฎแห่งการรวมกลุ่มอย่างอิสระ"


GENES = (("A", "a"), ("B", "b"))


def phenotype(genotype: str) -> str:
    pairs = [genotype[i:i + 2] for i in range(0, len(genotype), 2)]
    return "".join(p[0].upper() if any(ch.isupper() for ch in p) else p[0].lower() for p in pairs)


def random_genotype(rng: Random, genes: int) -> str:
    out = ""
    for big, small in GENES[:genes]:
        out += rng.choice((big + big, big + small, small + small))
    return out


def _fraction_wrongs(rng: Random, right: Fraction, denominators=(4, 8, 16)) -> tuple[str, ...]:
    pool = sorted(({Fraction(n, d) for d in denominators for n in range(1, d)} | {Fraction(1)}) - {right})
    near = sorted(pool, key=lambda x: abs(x - right))[:6]
    return tuple(frac_text(x) for x in rng.sample(near, 3))


@question_type(
    "biology.mendel_law_foundation",
    display_name={"th": "กฎแห่งการแยกและเซลล์สืบพันธุ์ที่สร้างได้"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LAWS,
)
class MendelLawFoundation(QuestionType):
    """Alleles separate into gametes; independent genes combine every way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        genes = rng.choice((1, 2, 2))
        genotype = random_genotype(rng, genes)
        kinds = sorted(set(gametes(genotype)))
        if rng.random() < 0.5:
            return numeric(stem=f"ต้นถั่วจีโนไทป์ {genotype} (ยีนแต่ละคู่อยู่บนโครโมโซมต่างคู่กัน) สร้างเซลล์สืบพันธุ์ได้กี่แบบ",
                           answer=len(kinds), wrongs=[len(kinds) * 2, 2 ** (2 * genes) if 2 ** (2 * genes) != len(kinds) else len(kinds) + 1,
                                                      len(kinds) + 1], unit="แบบ", topic=TOPIC_LAWS,
                           hint="แต่ละคู่ยีนแยกให้เซลล์สืบพันธุ์ละ 1 ตัว คู่ที่เป็นพันธุ์ทางให้ 2 แบบ จำนวนแบบ = 2 ยกกำลังจำนวนคู่ที่เป็นพันธุ์ทาง")
        right = ", ".join(kinds)
        # Other genotypes' gamete sets are the natural slips; the genotype itself is the classic one.
        others = {", ".join(sorted(set(gametes("".join(pair))))) for pair in product(*[(b + b, b + s, s + s) for b, s in GENES[:genes]])}
        pool = sorted(others - {right}) + [genotype]
        wrongs = [genotype] + rng.sample([p for p in pool if p != genotype], min(2, len(pool) - 1))
        return _labelled(stem=f"ต้นถั่วจีโนไทป์ {genotype} (ยีนแต่ละคู่อยู่บนโครโมโซมต่างคู่กัน) สร้างเซลล์สืบพันธุ์แบบใดได้บ้าง",
                         correct=right, wrongs=tuple(wrongs), topic=TOPIC_LAWS,
                         hint="เซลล์สืบพันธุ์ได้ยีนละ 1 ตัวจากแต่ละคู่ แล้วรวมกันทุกแบบที่เป็นไปได้")


@question_type(
    "biology.mendel_law_fluency",
    display_name={"th": "โอกาสเกิดจีโนไทป์และฟีโนไทป์ในการผสมยีนหนึ่งคู่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LAWS,
)
class MendelLawFluency(QuestionType):
    """Punnett square for one gene."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p1, p2 = random_genotype(rng, 1), random_genotype(rng, 1)
        kids = offspring(p1, p2)
        if rng.random() < 0.5:
            target = rng.choice(("AA", "Aa", "aa"))
            right = kids.get(target, Fraction(0))
            return _labelled(stem=f"ผสม {p1} × {p2} โอกาสที่ลูกมีจีโนไทป์ {target} เท่ากับเท่าใด", correct=frac_text(right),
                             wrongs=tuple(frac_text(x) for x in rng.sample(
                                 [o for o in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)) if o != right], 3)),
                             topic=TOPIC_LAWS, hint="เขียนตารางพันเนตต์ของเซลล์สืบพันธุ์จากพ่อและแม่ แล้วนับช่องที่ตรงกับจีโนไทป์ที่ถาม")
        dominant = sum(v for k, v in kids.items() if phenotype(k).isupper())
        want_dominant = rng.random() < 0.5
        right = dominant if want_dominant else 1 - dominant
        options = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
        return _labelled(stem=f"ให้ A ข่ม a สมบูรณ์ ผสม {p1} × {p2} โอกาสที่ลูกแสดงลักษณะ{'เด่น' if want_dominant else 'ด้อย'}เท่ากับเท่าใด",
                         correct=frac_text(right), wrongs=tuple(frac_text(x) for x in rng.sample([o for o in options if o != right], 3)),
                         topic=TOPIC_LAWS, hint="ลูกที่มี A อย่างน้อยหนึ่งตัวแสดงลักษณะเด่น (AA และ Aa) aa แสดงลักษณะด้อย")


@question_type(
    "biology.mendel_law_application",
    display_name={"th": "โอกาสเกิดลักษณะในการผสมยีนสองคู่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LAWS,
)
class MendelLawApplication(QuestionType):
    """Independent genes: multiply the chances for each gene."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p1, p2 = random_genotype(rng, 2), random_genotype(rng, 2)
        kids = offspring(p1, p2)
        hint = "ยีนสองคู่แยกกันอย่างอิสระ หาความน่าจะเป็นของแต่ละคู่แล้วคูณกัน"
        if rng.random() < 0.5:
            target = rng.choice(("AB", "Ab", "aB", "ab"))
            names = {"AB": "เด่นทั้งสองลักษณะ", "Ab": "เด่นลักษณะแรก ด้อยลักษณะที่สอง", "aB": "ด้อยลักษณะแรก เด่นลักษณะที่สอง",
                     "ab": "ด้อยทั้งสองลักษณะ"}
            right = sum(v for k, v in kids.items() if phenotype(k) == target)
            return _labelled(stem=f"ให้ A ข่ม a และ B ข่ม b สมบูรณ์ และยีนอยู่คนละโครโมโซม ผสม {p1} × {p2} "
                                  f"โอกาสที่ลูกมีฟีโนไทป์{names[target]}เท่ากับเท่าใด",
                             correct=frac_text(right), wrongs=_fraction_wrongs(rng, right), topic=TOPIC_LAWS, hint=hint)
        genotype = rng.choice(sorted(kids)) if rng.random() < 0.7 else random_genotype(rng, 2)
        right = kids.get(genotype, Fraction(0))
        return _labelled(stem=f"ยีนสองคู่อยู่คนละโครโมโซม ผสม {p1} × {p2} โอกาสที่ลูกมีจีโนไทป์ {genotype} เท่ากับเท่าใด",
                         correct=frac_text(right), wrongs=_fraction_wrongs(rng, right) if right else
                         tuple(frac_text(x) for x in rng.sample([Fraction(1, 16), Fraction(1, 8), Fraction(1, 4), Fraction(3, 16)], 3)),
                         topic=TOPIC_LAWS, hint=hint)

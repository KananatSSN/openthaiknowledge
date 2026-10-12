"""กรดนิวคลีอิก

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/7

Sets moved here from: science_wave_f45.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f45 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_NUCLEIC = "กรดนิวคลีอิก"


COMPARE = (
    ("น้ำตาลในนิวคลีโอไทด์", "น้ำตาลดีออกซีไรโบส", "น้ำตาลไรโบส"),
    ("เบสที่พบ", "เบส A T C และ G", "เบส A U C และ G"),
    ("จำนวนสาย", "โดยทั่วไปเป็นสายคู่บิดเป็นเกลียว", "โดยทั่วไปเป็นสายเดี่ยว"),
    ("หน้าที่หลัก", "เก็บและถ่ายทอดข้อมูลทางพันธุกรรม", "นำข้อมูลจาก DNA ไปใช้สังเคราะห์โปรตีน"),
)


#: Plausible wrong answers for each feature, so a question about strands is
#: not answered by "the sugar is ribose" from another row.
FEATURE_WRONGS = {
    "น้ำตาลในนิวคลีโอไทด์": ("น้ำตาลกลูโคส", "น้ำตาลฟรักโทส"),
    "เบสที่พบ": ("เบสเพียงสองชนิด คือ A และ T", "เบสครบทั้งห้าชนิด คือ A T U C และ G"),
    "จำนวนสาย": ("สามสายพันกันเป็นเชือก", "ไม่มีสาย เป็นก้อนกลมอยู่ในนิวเคลียส"),
    "หน้าที่หลัก": ("เร่งปฏิกิริยาย่อยอาหารในเซลล์", "เก็บพลังงานสำรองไว้ให้เซลล์ใช้"),
}


PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}


RNA_PAIR = {"A": "U", "T": "A", "C": "G", "G": "C"}


@question_type(
    "biology.nucleic_acid_foundation",
    display_name={"th": "โครงสร้างและชนิดของกรดนิวคลีอิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEIC,
)
class NucleicAcidFoundation(QuestionType):
    """A nucleotide is a sugar, a phosphate and a base; DNA and RNA differ in sugar, base and strands."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        feature, dna, rna = rng.choice(COMPARE)
        which = rng.choice(("DNA", "RNA"))
        right = dna if which == "DNA" else rna
        other = rna if which == "DNA" else dna
        if rng.random() < 0.3:
            return _labelled(stem="นิวคลีโอไทด์หนึ่งหน่วยประกอบด้วยอะไร", correct="น้ำตาลเพนโทส หมู่ฟอสเฟต และเบสไนโตรจีนัส",
                             wrongs=("กรดอะมิโน หมู่ฟอสเฟต และเบสไนโตรจีนัส", "น้ำตาลเพนโทส กลีเซอรอล และกรดไขมัน", "น้ำตาลเฮกโซส หมู่ฟอสเฟต และกรดอะมิโน"),
                             topic=TOPIC_NUCLEIC, hint="นิวคลีโอไทด์ = น้ำตาลคาร์บอน 5 อะตอม + ฟอสเฟต + เบส")
        return _labelled(stem=f"{feature}ของ {which} คือข้อใด", correct=right, wrongs=(other, *FEATURE_WRONGS[feature]),
                         topic=TOPIC_NUCLEIC, hint="DNA: ดีออกซีไรโบส เบส T สายคู่ RNA: ไรโบส เบส U สายเดี่ยว")


@question_type(
    "biology.nucleic_acid_fluency",
    display_name={"th": "การจับคู่เบสใน DNA และ RNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEIC,
)
class NucleicAcidFluency(QuestionType):
    """A pairs with T (or U in RNA), C pairs with G."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        strand = "".join(rng.choice("ATCG") for _ in range(rng.randint(5, 9)))
        to_rna = rng.random() < 0.4
        table = RNA_PAIR if to_rna else PAIR
        right = "".join(table[b] for b in strand)
        same = strand
        swapped = "".join({"A": "G", "T": "C", "C": "T", "G": "A"}[b] for b in strand)
        wrong_u = "".join(PAIR[b] for b in strand) if to_rna else "".join(RNA_PAIR[b] for b in strand)
        # One base wrong, as a near miss when the other slips coincide.
        slip = right[:-1] + {"A": "G", "T": "C", "U": "C", "C": "A", "G": "T"}[right[-1]]
        wrongs = [w for w in dict.fromkeys((same, swapped, wrong_u, right[::-1], slip)) if w != right][:3]
        target = "สาย RNA ที่ถอดรหัสจาก" if to_rna else "สาย DNA ที่เป็นคู่สมกับ"
        return _labelled(stem=f"{target}สาย DNA 5′-{strand}-3′ มีลำดับเบสอย่างไร (อ่านเทียบตำแหน่งต่อตำแหน่ง)",
                         correct=right, wrongs=tuple(wrongs), topic=TOPIC_NUCLEIC,
                         hint="DNA: A คู่ T และ C คู่ G ใน RNA ใช้ U แทน T")


@question_type(
    "biology.nucleic_acid_application",
    display_name={"th": "สัดส่วนเบสใน DNA ตามกฎของชาร์กาฟฟ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEIC,
)
class NucleicAcidApplication(QuestionType):
    """In double-stranded DNA A = T and C = G, so the four percentages add to 100."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a = rng.randrange(10, 41)
        c = 50 - a
        given, want = rng.choice((("A", "C"), ("A", "G"), ("A", "T"), ("C", "A"), ("G", "T"), ("T", "C")))
        value = {"A": a, "T": a, "C": c, "G": c}
        if rng.random() < 0.7:
            return numeric(stem=f"DNA สายคู่ของสิ่งมีชีวิตชนิดหนึ่งมีเบส {given} อยู่ร้อยละ {value[given]} มีเบส {want} อยู่ร้อยละเท่าใด",
                           answer=value[want], wrongs=[100 - value[given] if 100 - value[given] != value[want] else value[want] + 10,
                                                       value[given] if value[given] != value[want] else 50 - value[want] + 5,
                                                       value[want] + 5], unit="%", topic=TOPIC_NUCLEIC,
                           hint="A = T และ C = G และ A + T + C + G = 100% ดังนั้น A + C = 50%")
        pairs = rng.randrange(100, 2001, 100)
        at = rng.randrange(10, 91, 10)
        gc_bonds = (100 - at) * pairs // 100 * 3 + at * pairs // 100 * 2
        return numeric(stem=f"DNA สายคู่ยาว {pairs} คู่เบส มีคู่ A-T ร้อยละ {at} ของคู่เบสทั้งหมด มีพันธะไฮโดรเจนระหว่างเบสทั้งหมดกี่พันธะ",
                       answer=gc_bonds, wrongs=[pairs * 2, pairs * 3, gc_bonds + pairs], unit="พันธะ", topic=TOPIC_NUCLEIC,
                       hint="คู่ A-T ยึดด้วยพันธะไฮโดรเจน 2 พันธะ คู่ C-G ยึดด้วย 3 พันธะ")

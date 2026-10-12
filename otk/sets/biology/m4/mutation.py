"""มิวเทชัน

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/9

Sets moved here from: science_wave_f50.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f50 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MUT = "มิวเทชัน"


DISORDERS = (
    ("กลุ่มอาการดาวน์", "มีโครโมโซมคู่ที่ 21 เกินมา 1 แท่ง", "ระดับโครโมโซม"),
    ("กลุ่มอาการเอ็ดเวิร์ด", "มีโครโมโซมคู่ที่ 18 เกินมา 1 แท่ง", "ระดับโครโมโซม"),
    ("กลุ่มอาการพาทัว", "มีโครโมโซมคู่ที่ 13 เกินมา 1 แท่ง", "ระดับโครโมโซม"),
    ("กลุ่มอาการเทอร์เนอร์", "เพศหญิงมีโครโมโซม X เพียงแท่งเดียว (45,X)", "ระดับโครโมโซม"),
    ("กลุ่มอาการไคลน์เฟลเตอร์", "เพศชายมีโครโมโซม X เกิน (47,XXY)", "ระดับโครโมโซม"),
    ("กลุ่มอาการคริดูชา", "แขนข้างสั้นของโครโมโซมคู่ที่ 5 ขาดหายไปบางส่วน", "ระดับโครโมโซม"),
    ("มะเร็งเม็ดเลือดขาวชนิดเรื้อรัง (CML)", "โครโมโซมคู่ที่ 9 และ 22 ย้ายสลับส่วนกัน", "ระดับโครโมโซม"),
    ("โลหิตจางชนิดเซลล์รูปเคียว", "คู่เบสในยีนสร้างสายโกลบินถูกแทนที่ 1 ตำแหน่ง", "ระดับยีน"),
)


MUTAGENS = ("รังสีเอกซ์", "รังสีแกมมา", "รังสีอัลตราไวโอเลต", "สารเบนโซไพรีนในควันบุหรี่", "สารอะฟลาทอกซินจากเชื้อราในถั่วลิสงขึ้นรา",
            "ไวรัสบางชนิด")


NOT_MUTAGENS = ("การออกกำลังกายสม่ำเสมอ", "การดื่มน้ำสะอาด", "การนอนหลับพักผ่อน", "การได้รับแสงสว่างจากหลอด LED",
                "การรับประทานผักและผลไม้")


LEVEL_EVENTS = {
    "ระดับยีน": ("เบสหนึ่งคู่ถูกแทนที่ด้วยเบสคู่อื่น", "นิวคลีโอไทด์เพิ่มเข้ามา 1 ตัวในยีน", "นิวคลีโอไทด์หายไป 2 ตัวในยีน"),
    "ระดับโครโมโซม": ("ส่วนของโครโมโซมขาดหายไป", "ส่วนของโครโมโซมกลับทิศ", "โครโมโซมต่างคู่ย้ายสลับส่วนกัน",
                      "จำนวนโครโมโซมเพิ่มขึ้นเป็นชุด (พอลิพลอยดี)", "โครโมโซมคู่หนึ่งไม่แยกจากกันระหว่างแบ่งเซลล์"),
}


MUT_HINT = ("มิวเทชันระดับยีนคือการแทนที่ เพิ่ม หรือขาดของนิวคลีโอไทด์ ระดับโครโมโซมคือการเปลี่ยนโครงสร้างหรือจำนวนโครโมโซม "
            "สาเหตุ เช่น รังสี สารเคมีบางชนิด และความผิดพลาดในการจำลอง DNA หรือการแบ่งเซลล์")


GENE_KINDS = ("การแทนที่คู่เบส", "การเพิ่มขึ้นของนิวคลีโอไทด์", "การขาดหายไปของนิวคลีโอไทด์")


CHROM_KINDS = ("การขาดหายไปของส่วนโครโมโซม (deletion)", "การเพิ่มซ้ำของส่วนโครโมโซม (duplication)",
               "การกลับทิศของส่วนโครโมโซม (inversion)", "การย้ายสลับส่วนระหว่างโครโมโซมต่างคู่ (translocation)")


def gene_mutation(rng: Random) -> tuple[str, str, str]:
    dna = "".join(rng.choice("ATCG") for _ in range(rng.randint(12, 18)))
    pos = rng.randrange(2, len(dna) - 2)
    kind = rng.randrange(3)
    if kind == 0:
        new = dna[:pos] + rng.choice([b for b in "ATCG" if b != dna[pos]]) + dna[pos + 1:]
    elif kind == 1:
        new = dna[:pos] + rng.choice("ATCG") + dna[pos:]
    else:
        new = dna[:pos] + dna[pos + 1:]
    return dna, new, GENE_KINDS[kind]


def chromosome_mutation(rng: Random) -> tuple[str, str, str]:
    genes = "ABCDEFGH"[:rng.randint(6, 8)]
    kind = rng.randrange(4)
    i = rng.randrange(1, len(genes) - 3)
    j = i + rng.randint(2, 3)
    if kind == 0:
        new = genes[:i] + genes[j:]
    elif kind == 1:
        new = genes[:j] + genes[i:j] + genes[j:]
    elif kind == 2:
        new = genes[:i] + genes[i:j][::-1] + genes[j:]
    else:
        new = genes[:i] + "RST"[:j - i] + genes[j:]
    return genes, new, CHROM_KINDS[kind]


SPECIES = (("มนุษย์", 46), ("ข้าว", 24), ("ข้าวโพด", 20), ("แมลงหวี่", 8), ("ถั่วลันเตา", 14), ("หอมหัวใหญ่", 16),
           ("มะเขือเทศ", 24), ("แมว", 38), ("สุนัข", 78), ("กล้วยป่า", 22))


CONDITIONS = (("ไทรโซมี", lambda d: d + 1), ("โมโนโซมี", lambda d: d - 1), ("นัลลิโซมี", lambda d: d - 2),
              ("ทริปพลอยดี (3n)", lambda d: d // 2 * 3), ("เททระพลอยดี (4n)", lambda d: d * 2))


SYNDROME_COUNTS = (("กลุ่มอาการดาวน์", 47), ("กลุ่มอาการเอ็ดเวิร์ด", 47), ("กลุ่มอาการพาทัว", 47), ("กลุ่มอาการเทอร์เนอร์", 45),
                   ("กลุ่มอาการไคลน์เฟลเตอร์", 47))


@question_type(
    "biology.mutation_foundation",
    display_name={"th": "ชนิด สาเหตุ และโรคที่เกิดจากมิวเทชัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MUT,
)
class MutationFoundation(QuestionType):
    """Syndromes and their causes, gene against chromosome level, and mutagens."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.45:
            name, cause, _ = rng.choice(DISORDERS)
            others = rng.sample([d for d in DISORDERS if d[0] != name], 3)
            if rng.random() < 0.5:
                return _labelled(stem=f"{name}เกิดจากความผิดปกติใด", correct=cause, wrongs=tuple(d[1] for d in others),
                                 topic=TOPIC_MUT, hint=MUT_HINT)
            return _labelled(stem=f"ผู้ที่{cause} จะมีความผิดปกติใด", correct=name, wrongs=tuple(d[0] for d in others),
                             topic=TOPIC_MUT, hint=MUT_HINT)
        if roll < 0.75:
            level = rng.choice(sorted(LEVEL_EVENTS))
            other = [e for lv, es in LEVEL_EVENTS.items() if lv != level for e in es]
            if len(LEVEL_EVENTS[level]) >= 3 and rng.random() < 0.5:
                return _labelled(stem=f"ข้อใดไม่ใช่มิวเทชัน{level}", correct=rng.choice(other),
                                 wrongs=tuple(LEVEL_EVENTS[level]), topic=TOPIC_MUT, hint=MUT_HINT)
            return _labelled(stem=f"ข้อใดเป็นมิวเทชัน{level}", correct=rng.choice(LEVEL_EVENTS[level]),
                             wrongs=tuple(other), topic=TOPIC_MUT, hint=MUT_HINT)
        if rng.random() < 0.5:
            return _labelled(stem="ข้อใดเป็นสิ่งก่อกลายพันธุ์ (มิวทาเจน)", correct=rng.choice(MUTAGENS),
                             wrongs=tuple(NOT_MUTAGENS), topic=TOPIC_MUT, hint=MUT_HINT)
        return _labelled(stem="ข้อใดไม่ใช่สิ่งก่อกลายพันธุ์ (มิวทาเจน)", correct=rng.choice(NOT_MUTAGENS),
                         wrongs=tuple(MUTAGENS), topic=TOPIC_MUT, hint=MUT_HINT)


@question_type(
    "biology.mutation_fluency",
    display_name={"th": "ระบุชนิดของมิวเทชันจากลำดับเบสหรือลำดับยีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MUT,
)
class MutationFluency(QuestionType):
    """Compare before and after, base by base or gene by gene."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            old, new, kind = gene_mutation(rng)
            return _labelled(stem=f"ลำดับเบสในยีนเดิมเป็น 5′-{old}-3′ เปลี่ยนเป็น 5′-{new}-3′ เป็นมิวเทชันแบบใด", correct=kind,
                             wrongs=tuple(k for k in GENE_KINDS if k != kind) + (CHROM_KINDS[2],), topic=TOPIC_MUT,
                             hint="เทียบทีละตำแหน่ง ความยาวเท่าเดิมแต่เบสเปลี่ยนคือการแทนที่ ยาวขึ้นคือการเพิ่ม สั้นลงคือการขาดหาย")
        old, new, kind = chromosome_mutation(rng)
        return _labelled(stem=f"ลำดับยีนบนโครโมโซมเดิมเป็น {old} (โครโมโซมต่างคู่มีลำดับยีน QRSTUV) เปลี่ยนเป็น {new} "
                              f"เป็นมิวเทชันแบบใด", correct=kind, wrongs=tuple(k for k in CHROM_KINDS if k != kind), topic=TOPIC_MUT,
                         hint="ยีนหายไปคือขาดหาย ยีนซ้ำคือเพิ่มซ้ำ ลำดับย้อนกลับคือกลับทิศ มียีนจากโครโมโซมอื่นเข้ามาคือย้ายสลับ")


@question_type(
    "biology.mutation_application",
    display_name={"th": "จำนวนโครโมโซมเมื่อเกิดมิวเทชันระดับโครโมโซม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MUT,
)
class MutationApplication(QuestionType):
    """Aneuploidy adds or loses single chromosomes; polyploidy adds whole sets."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ไทรโซมี 2n + 1 โมโนโซมี 2n − 1 นัลลิโซมี 2n − 2 ทริปพลอยดี 3n เททระพลอยดี 4n"
        roll = rng.random()
        if roll < 0.2:
            name, count = rng.choice(SYNDROME_COUNTS)
            return numeric(stem=f"เซลล์ร่างกายของผู้ที่มี{name}มีโครโมโซมกี่แท่ง", answer=count,
                           wrongs=[46, 48 if count == 47 else 47, 44 if count != 45 else 23], unit="แท่ง", topic=TOPIC_MUT,
                           hint="เซลล์ร่างกายปกติมี 46 แท่ง ไทรโซมี (ดาวน์ เอ็ดเวิร์ด พาทัว ไคลน์เฟลเตอร์) มี 47 เทอร์เนอร์มี 45")
        species, diploid = rng.choice(SPECIES)
        if roll < 0.4:
            extra = rng.random() < 0.5
            return numeric(stem=f"{species}มีโครโมโซม 2n = {diploid} ถ้าระหว่างไมโอซิสโครโมโซมคู่หนึ่งไม่แยกจากกัน เซลล์สืบพันธุ์ที่"
                                + ("ได้โครโมโซมคู่นั้นไปทั้งสองแท่ง" if extra else "ไม่ได้รับโครโมโซมคู่นั้นเลย") + "มีโครโมโซมกี่แท่ง",
                           answer=diploid // 2 + (1 if extra else -1),
                           wrongs=[diploid + (1 if extra else -1), diploid // 2, diploid // 2 + (-1 if extra else 1)], unit="แท่ง",
                           topic=TOPIC_MUT, hint="เซลล์สืบพันธุ์ปกติมี n แท่ง ถ้าได้โครโมโซมเกินมา 1 แท่งเป็น n + 1 ถ้าขาดไป 1 แท่งเป็น n − 1")
        name, rule = rng.choice(CONDITIONS)
        answer = rule(diploid)
        return numeric(stem=f"{species}มีโครโมโซม 2n = {diploid} ถ้าเกิด{name} เซลล์ร่างกายจะมีโครโมโซมกี่แท่ง", answer=answer,
                       wrongs=[diploid, diploid // 2 * 3 if answer != diploid // 2 * 3 else diploid + 1, diploid + 2], unit="แท่ง",
                       topic=TOPIC_MUT, hint=hint)

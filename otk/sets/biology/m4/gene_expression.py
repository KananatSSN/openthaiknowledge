"""การสังเคราะห์โปรตีน

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/7

Sets moved here from: science_wave_f50.
"""

from __future__ import annotations

from itertools import product
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f50 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_EXPR = "การสังเคราะห์โปรตีน"


RNA_ROLES = (
    ("DNA", "เป็นแม่แบบในการสร้าง RNA ในขั้นทรานสคริปชัน"),
    ("mRNA", "นำรหัสพันธุกรรมจาก DNA ไปยังไรโบโซม โดยเบสทุก 3 ตัวเป็น 1 โคดอน"),
    ("tRNA", "นำกรดอะมิโนมายังไรโบโซม โดยใช้แอนติโคดอนจับคู่กับโคดอน"),
    ("rRNA", "เป็นองค์ประกอบของไรโบโซมร่วมกับโปรตีน"),
)


EXPR_FACTS = (
    ("ทรานสคริปชันในเซลล์ยูแคริโอตเกิดขึ้นที่ใด", "นิวเคลียส", ("ไรโบโซมในไซโทพลาซึม", "กอลจิคอมเพล็กซ์", "ไลโซโซม", "แวคิวโอล")),
    ("ทรานสเลชันเกิดขึ้นที่ใด", "ไรโบโซม", ("นิวคลีโอลัส", "เยื่อหุ้มนิวเคลียส", "ไลโซโซม", "เซนทริโอล")),
    ("เอนไซม์ใดสร้าง mRNA จากสายแม่แบบ DNA", "RNA พอลิเมอเรส", ("DNA ไลเกส", "เฮลิเคส", "เพปซิน", "DNA พอลิเมอเรส")),
    ("โคดอนเริ่มต้นของการแปลรหัสคือข้อใด", "AUG", ("UAA", "UAG", "UGA", "GUA")),
    ("ข้อใดเป็นโคดอนหยุด (stop codon) ทั้งหมด", "UAA UAG และ UGA", ("AUG UAA และ UAG", "AUG GUG และ UUG", "UAA UGG และ AGA")),
    ("ในเซลล์ยูแคริโอต ก่อน mRNA ออกจากนิวเคลียสต้องผ่านการเปลี่ยนแปลงใด", "ตัดอินทรอนออกแล้วต่อเอกซอนเข้าด้วยกัน",
     ("ตัดเอกซอนออกแล้วต่ออินทรอนเข้าด้วยกัน", "เปลี่ยนเบส U ทั้งหมดเป็น T", "จับกับกรดอะมิโนตัวแรกทันที")),
    ("พันธะที่เกิดระหว่างกรดอะมิโนที่อยู่ติดกันในการแปลรหัสคือพันธะใด", "พันธะเพปไทด์",
     ("พันธะไฮโดรเจน", "พันธะฟอสโฟไดเอสเทอร์", "พันธะไกลโคซิดิก", "พันธะไดซัลไฟด์")),
    ("ลำดับขั้นของการแสดงออกของยีนข้อใดถูกต้อง", "DNA → (ทรานสคริปชัน) mRNA → (ทรานสเลชัน) โปรตีน",
     ("DNA → (ทรานสเลชัน) mRNA → (ทรานสคริปชัน) โปรตีน", "mRNA → (ทรานสคริปชัน) DNA → โปรตีน",
      "โปรตีน → (ทรานสเลชัน) mRNA → DNA")),
)


EXPR_HINT = ("ทรานสคริปชันในนิวเคลียสใช้ RNA พอลิเมอเรสสร้าง mRNA จาก DNA ทรานสเลชันที่ไรโบโซม tRNA นำกรดอะมิโนมาจับตามโคดอน "
             "เริ่มที่ AUG และหยุดที่ UAA UAG หรือ UGA")


STOPS = ("UAA", "UAG", "UGA")


SENSE = tuple("".join(c) for c in product("UCAG", repeat=3) if "".join(c) not in STOPS)


RNA_PAIR = {"A": "U", "U": "A", "C": "G", "G": "C"}


def reading(mrna: str) -> int:
    """Amino acids made reading in frame from the first AUG to the first stop."""
    start = mrna.index("AUG")
    count = 0
    for i in range(start, len(mrna) - 2, 3):
        if mrna[i:i + 3] in STOPS:
            return count
        count += 1
    raise ValueError("no stop codon")


def planted_mrna(rng: Random) -> tuple[str, int]:
    while True:
        leader = "".join(rng.choice("UCAG") for _ in range(rng.randint(0, 5)))
        middle = [rng.choice(SENSE) for _ in range(rng.randint(2, 7))]
        trailer = "".join(rng.choice("UCAG") for _ in range(rng.randint(0, 4)))
        mrna = leader + "AUG" + "".join(middle) + rng.choice(STOPS) + trailer
        if mrna.index("AUG") == len(leader):
            return mrna, len(middle) + 1


@question_type(
    "biology.gene_expression_foundation",
    display_name={"th": "หน้าที่ของ DNA และ RNA แต่ละชนิดในการสังเคราะห์โปรตีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXPR,
)
class GeneExpressionFoundation(QuestionType):
    """What each nucleic acid does, and where each step happens."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            name, role = rng.choice(RNA_ROLES)
            others = [r for r in RNA_ROLES if r[0] != name]
            if rng.random() < 0.5:
                roles = [r[1] for r in others] + ["ตัดอินทรอนออกจาก DNA ในนิวเคลียส", "เชื่อมชิ้นส่วนโอคาซากิระหว่างการจำลอง DNA"]
                return _labelled(stem=f"ในการสังเคราะห์โปรตีน {name} มีหน้าที่อย่างไร", correct=role,
                                 wrongs=tuple(roles), topic=TOPIC_EXPR, hint=EXPR_HINT)
            names = [r[0] for r in others] + ["RNA พอลิเมอเรส", "DNA ไลเกส"]
            return _labelled(stem=f"สารใดทำหน้าที่{role}", correct=name, wrongs=tuple(names),
                             topic=TOPIC_EXPR, hint=EXPR_HINT)
        stem, right, wrongs = rng.choice(EXPR_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_EXPR, hint=EXPR_HINT)


@question_type(
    "biology.gene_expression_fluency",
    display_name={"th": "อ่านรหัสบน mRNA โคดอนและแอนติโคดอน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXPR,
)
class GeneExpressionFluency(QuestionType):
    """Read from the first AUG to a stop codon; an anticodon pairs antiparallel with its codon."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            mrna, amino = planted_mrna(rng)
            assert reading(mrna) == amino
            return numeric(stem=f"mRNA มีลำดับเบส 5′-{mrna}-3′ เมื่อแปลรหัสเริ่มที่ AUG ตัวแรกจนถึงโคดอนหยุด "
                                f"จะได้พอลิเพปไทด์ที่มีกรดอะมิโนกี่ตัว",
                           answer=amino, wrongs=[amino + 1, amino - 1 or amino + 2, len(mrna) // 3], unit="ตัว",
                           topic=TOPIC_EXPR, hint="เริ่มอ่านที่ AUG ทีละ 3 เบส AUG ให้เมไทโอนีน นับจนถึงโคดอนหยุด (UAA UAG UGA) ซึ่งไม่ให้กรดอะมิโน")
        codon = rng.choice(SENSE)
        anti = "".join(RNA_PAIR[b] for b in codon)
        dna_like = anti.replace("U", "T")
        slips = list(dict.fromkeys(w for w in (f"3′-{codon}-5′", f"3′-{dna_like}-5′", f"5′-{anti}-3′", f"3′-{anti[::-1]}-5′",
                                               f"3′-{codon.replace('U', 'T')}-5′", f"3′-{anti[:2]}{codon[2]}-5′",
                                               f"3′-{codon[0]}{anti[1:]}-5′") if w != f"3′-{anti}-5′"))
        if rng.random() < 0.5:
            return _labelled(stem=f"โคดอนบน mRNA คือ 5′-{codon}-3′ แอนติโคดอนของ tRNA ที่จับคู่กันคือข้อใด", correct=f"3′-{anti}-5′",
                             wrongs=tuple(slips),
                             topic=TOPIC_EXPR, hint="แอนติโคดอนเข้าคู่กับโคดอนแบบสวนทาง A คู่ U และ C คู่ G")
        template = "".join({"A": "T", "U": "A", "C": "G", "G": "C"}[b] for b in codon)
        return _labelled(stem=f"สายแม่แบบของ DNA มีลำดับเบส 3′-{template}-5′ โคดอนบน mRNA ที่ถอดรหัสได้คือข้อใด", correct=f"5′-{codon}-3′",
                         wrongs=tuple(list(dict.fromkeys(
                             w for w in (f"5′-{template}-3′", f"5′-{anti}-3′", f"5′-{codon.replace('U', 'T')}-3′", f"3′-{codon}-5′",
                                         f"5′-{codon[::-1]}-3′", f"5′-{codon[:2]}{RNA_PAIR[codon[2]]}-3′",
                                         f"5′-{RNA_PAIR[codon[0]]}{codon[1:]}-3′") if w != f"5′-{codon}-3′"))),
                         topic=TOPIC_EXPR, hint="mRNA เข้าคู่กับสายแม่แบบแบบสวนทาง ใช้ U แทน T")


@question_type(
    "biology.gene_expression_application",
    display_name={"th": "คำนวณจำนวนเบส โคดอน และพันธะเพปไทด์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EXPR,
)
class GeneExpressionApplication(QuestionType):
    """Three bases per amino acid, one stop codon, n - 1 peptide bonds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randrange(20, 601)
        hint = "กรดอะมิโน 1 ตัวใช้ 1 โคดอน (3 เบส) และต้องมีโคดอนหยุดอีก 1 โคดอน กรดอะมิโน n ตัวเชื่อมด้วยพันธะเพปไทด์ n − 1 พันธะ"
        protein = f"พอลิเพปไทด์ที่มีกรดอะมิโน {n} ตัว"
        cases = (
            (f"{protein} ถูกแปลรหัสจากส่วนของ mRNA ตั้งแต่โคดอนเริ่มต้นถึงโคดอนหยุด ส่วนนี้มีเบสอย่างน้อยกี่เบส", 3 * n + 3,
             [3 * n, n, 6 * n + 6], "เบส"),
            (f"ยีนที่กำหนด{protein} (นับเฉพาะส่วนตั้งแต่โคดอนเริ่มต้นถึงโคดอนหยุด ไม่มีอินทรอน) มีกี่คู่เบส", 3 * n + 3,
             [3 * n, 6 * n + 6, n + 1], "คู่เบส"),
            (f"{protein} มีพันธะเพปไทด์กี่พันธะ", n - 1, [n, n + 1, 3 * n], "พันธะ"),
            (f"การสร้าง{protein} ปล่อยน้ำออกมากี่โมเลกุล", n - 1, [n, n + 1, 2 * n], "โมเลกุล"),
            (f"การสร้าง{protein} ต้องมี tRNA นำกรดอะมิโนมาที่ไรโบโซมกี่ครั้ง", n, [n - 1, n + 1, 3 * n], "ครั้ง"),
            (f"ส่วนของ mRNA ตั้งแต่โคดอนเริ่มต้นถึงโคดอนหยุดยาว {3 * n + 3} เบส แปลรหัสได้กรดอะมิโนกี่ตัว", n,
             [n + 1, 3 * n + 3, n - 1], "ตัว"),
        )
        stem, answer, wrongs, unit = rng.choice(cases)
        return numeric(stem=stem, answer=answer, wrongs=wrongs, unit=unit, topic=TOPIC_EXPR, hint=hint)

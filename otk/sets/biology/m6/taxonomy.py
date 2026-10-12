"""ลำดับขั้นการจำแนกและชื่อวิทยาศาสตร์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.6/4

Sets moved here from: science_wave_f53.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f53 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_TAXON = "ลำดับขั้นการจำแนกและชื่อวิทยาศาสตร์"


RANKS = ("โดเมน", "อาณาจักร", "ไฟลัม", "คลาส", "ออร์เดอร์", "แฟมิลี", "จีนัส", "สปีชีส์")


RANK_HINT = "โดเมน > อาณาจักร > ไฟลัม > คลาส > ออร์เดอร์ > แฟมิลี > จีนัส > สปีชีส์ ยิ่งลำดับขั้นย่อย สมาชิกยิ่งมีลักษณะร่วมกันมาก"


SPECIES = (("คน", "Homo", "sapiens"), ("ข้าว", "Oryza", "sativa"), ("มะม่วง", "Mangifera", "indica"), ("ช้างเอเชีย", "Elephas", "maximus"),
           ("สิงโต", "Panthera", "leo"), ("เสือโคร่ง", "Panthera", "tigris"), ("แมวบ้าน", "Felis", "catus"), ("มะขาม", "Tamarindus", "indica"),
           ("ยุงลาย", "Aedes", "aegypti"), ("แมลงหวี่", "Drosophila", "melanogaster"), ("ปลากัด", "Betta", "splendens"))


# Order, family and genus of each animal (all in Animalia, Chordata, Mammalia).
LINEAGE = {"สิงโต": ("Carnivora", "Felidae", "Panthera"), "เสือโคร่ง": ("Carnivora", "Felidae", "Panthera"),
           "เสือดาว": ("Carnivora", "Felidae", "Panthera"), "แมวบ้าน": ("Carnivora", "Felidae", "Felis"),
           "หมาป่า": ("Carnivora", "Canidae", "Canis"), "หมาจิ้งจอก": ("Carnivora", "Canidae", "Vulpes"),
           "คน": ("Primates", "Hominidae", "Homo"), "ชิมแปนซี": ("Primates", "Hominidae", "Pan"),
           "ลิงแสม": ("Primates", "Cercopithecidae", "Macaca"), "ช้างเอเชีย": ("Proboscidea", "Elephantidae", "Elephas")}


def shared(a: str, b: str) -> int:
    n = 0
    for x, y in zip(LINEAGE[a], LINEAGE[b]):
        if x != y:
            break
        n += 1
    return n


@question_type(
    "biology.taxonomy_foundation",
    display_name={"th": "ลำดับขั้นของการจัดจำแนกสิ่งมีชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TAXON,
)
class TaxonomyFoundation(QuestionType):
    """Domain down to species, in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.5:
            i = rng.randrange(len(RANKS) - 1)
            below = rng.random() < 0.5 or i == 0
            if not below:
                i = rng.randrange(1, len(RANKS))
            target = RANKS[i + 1] if below else RANKS[i - 1]
            pool = [r for r in RANKS if r not in (RANKS[i], target)]
            return _labelled(stem=f"ลำดับขั้นใดอยู่{'ถัดลงมาจาก' if below else 'ถัดขึ้นไปจาก'}{RANKS[i]}", correct=target,
                             wrongs=tuple(pool), topic=TOPIC_TAXON, hint=RANK_HINT)
        if roll < 0.75:
            chosen = sorted(rng.sample(range(len(RANKS)), 4))
            right = " > ".join(RANKS[k] for k in chosen)
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                order = chosen[:]
                rng.shuffle(order)
                if order != chosen:
                    wrongs[" > ".join(RANKS[k] for k in order)] = None
            return _labelled(stem="ข้อใดเรียงลำดับขั้นการจัดจำแนกจากใหญ่ไปย่อยได้ถูกต้อง", correct=right, wrongs=tuple(wrongs),
                             topic=TOPIC_TAXON, hint=RANK_HINT)
        many = rng.random() < 0.5
        return _labelled(stem=f"สมาชิกในลำดับขั้นใดมีลักษณะร่วมกัน{'มากที่สุด' if many else 'น้อยที่สุด'}",
                         correct="สปีชีส์" if many else "โดเมน",
                         wrongs=tuple(rng.sample([r for r in RANKS if r not in ("สปีชีส์", "โดเมน")], 2)) + ("โดเมน" if many else "สปีชีส์",),
                         topic=TOPIC_TAXON, hint=RANK_HINT)


@question_type(
    "biology.taxonomy_fluency",
    display_name={"th": "การเขียนชื่อวิทยาศาสตร์แบบทวินาม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TAXON,
)
class TaxonomyFluency(QuestionType):
    """Genus capitalised, then the specific epithet in lower case, both in Latin."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        common, genus, epithet = rng.choice(SPECIES)
        hint = "ชื่อวิทยาศาสตร์มี 2 คำ คำแรกเป็นชื่อจีนัสขึ้นต้นด้วยอักษรตัวใหญ่ คำหลังเป็นคำระบุชนิดตัวเล็กทั้งหมด เขียนตัวเอนหรือขีดเส้นใต้แยกกัน"
        roll = rng.random()
        if roll < 0.5:
            return _labelled(stem=f"ชื่อวิทยาศาสตร์ของ{common}ข้อใดเขียนตามหลักการตั้งชื่อแบบทวินามได้ถูกต้อง (ไม่คำนึงถึงตัวเอน)",
                             correct=f"{genus} {epithet}",
                             wrongs=(f"{genus.lower()} {epithet}", f"{genus} {epithet.capitalize()}", f"{epithet} {genus}"),
                             topic=TOPIC_TAXON, hint=hint)
        if roll < 0.8:
            part = rng.random() < 0.5
            return _labelled(stem=f"ชื่อวิทยาศาสตร์ของ{common}คือ {genus} {epithet} คำว่า {genus if part else epithet} คืออะไร",
                             correct="ชื่อจีนัส" if part else "คำระบุชนิด (specific epithet)",
                             wrongs=("คำระบุชนิด (specific epithet)" if part else "ชื่อจีนัส", "ชื่อแฟมิลี", "ชื่อผู้ตั้งชื่อ"),
                             topic=TOPIC_TAXON, hint=hint)
        facts = (("ระบบการตั้งชื่อวิทยาศาสตร์แบบทวินามเสนอโดยใคร", "คาโรลัส ลินเนียส", ("ชาลส์ ดาร์วิน", "เกรเกอร์ เมนเดล", "ฌอง ลามาร์ก")),
                 ("ชื่อวิทยาศาสตร์เขียนเป็นภาษาใด", "ภาษาละตินหรือคำที่ทำให้เป็นภาษาละติน", ("ภาษาอังกฤษ", "ภาษาของประเทศที่ค้นพบ", "ภาษาใดก็ได้")),
                 ("ประโยชน์สำคัญของชื่อวิทยาศาสตร์คือข้อใด", "ใช้เรียกสิ่งมีชีวิตชนิดเดียวกันได้ตรงกันทั่วโลก",
                  ("ทำให้ชื่อสั้นและจำง่ายกว่าชื่อสามัญ", "บอกขนาดตัวของสิ่งมีชีวิต", "บอกอายุของสิ่งมีชีวิต")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_TAXON, hint=hint)


@question_type(
    "biology.taxonomy_application",
    display_name={"th": "หาความสัมพันธ์ใกล้ชิดจากลำดับขั้นการจำแนก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TAXON,
)
class TaxonomyApplication(QuestionType):
    """The lower the rank two organisms share, the closer they are."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            ref = rng.choice(sorted(LINEAGE))
            cands = rng.sample([a for a in LINEAGE if a != ref], 4)
            scores = [shared(ref, c) for c in cands]
            if scores.count(max(scores)) == 1:
                break
        right = cands[scores.index(max(scores))]
        table = " ".join(f"{a} (ออร์เดอร์ {LINEAGE[a][0]} แฟมิลี {LINEAGE[a][1]} จีนัส {LINEAGE[a][2]})" for a in [ref, *cands])
        return _labelled(stem=f"สัตว์เลี้ยงลูกด้วยน้ำนมต่อไปนี้ {table} สัตว์ใดมีความสัมพันธ์ใกล้ชิดกับ{ref}มากที่สุด", correct=right,
                         wrongs=tuple(c for c in cands if c != right), topic=TOPIC_TAXON,
                         hint="หาลำดับขั้นที่ย่อยที่สุดที่อยู่ร่วมกัน ร่วมจีนัสใกล้ชิดกว่าร่วมแฟมิลี ร่วมแฟมิลีใกล้ชิดกว่าร่วมออร์เดอร์")

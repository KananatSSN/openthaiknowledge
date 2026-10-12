"""ดีเอ็นเอรีคอมบิแนนท์และสิ่งมีชีวิตดัดแปรพันธุกรรม

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/10

Sets moved here from: science_wave_f51.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f51 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_RDNA = "ดีเอ็นเอรีคอมบิแนนท์และสิ่งมีชีวิตดัดแปรพันธุกรรม"


TOOLS = (
    ("เอนไซม์ตัดจำเพาะ", "ตัด DNA ตรงลำดับเบสที่จำเพาะ"),
    ("DNA ไลเกส", "เชื่อมชิ้น DNA ที่มีปลายเข้าคู่กันให้ต่อเป็นสายเดียว"),
    ("พลาสมิด", "เป็นพาหะนำยีนที่ต้องการเข้าสู่เซลล์เจ้าบ้าน"),
    ("แบคทีเรียเจ้าบ้าน", "รับ DNA รีคอมบิแนนท์แล้วเพิ่มจำนวนพร้อมสร้างผลผลิตของยีน"),
    ("ยีนต้านยาปฏิชีวนะบนพลาสมิด", "ใช้คัดเลือกเซลล์ที่ได้รับพลาสมิด"),
)


RDNA_STEPS = ("ตัด DNA ที่มียีนที่ต้องการและพลาสมิดด้วยเอนไซม์ตัดจำเพาะชนิดเดียวกัน",
              "เชื่อมยีนเข้ากับพลาสมิดด้วย DNA ไลเกส",
              "นำพลาสมิดรีคอมบิแนนท์เข้าสู่แบคทีเรีย",
              "คัดเลือกแบคทีเรียที่ได้รับพลาสมิดแล้วเลี้ยงให้เพิ่มจำนวน")


RDNA_HINT = ("ตัดยีนและพลาสมิดด้วยเอนไซม์ตัดจำเพาะชนิดเดียวกันให้ได้ปลายเข้าคู่กัน เชื่อมด้วย DNA ไลเกส "
             "นำเข้าแบคทีเรีย แล้วคัดเลือกด้วยยาปฏิชีวนะ")


RESTRICTION = (("EcoRI", "GAATTC", "AATT"), ("BamHI", "GGATCC", "GATC"), ("HindIII", "AAGCTT", "AGCT"),
               ("SmaI", "CCCGGG", ""))


def count_sites(seq: str, site: str, circular: bool) -> int:
    text = seq + seq[:len(site) - 1] if circular else seq
    return sum(text.startswith(site, i) for i in range(len(seq) if circular else len(seq) - len(site) + 1))


def planted_dna(rng: Random, site: str, sites: int, circular: bool) -> str:
    while True:
        parts = ["".join(rng.choice("ATCG") for _ in range(rng.randint(3, 9))) for _ in range(sites + 1)]
        seq = parts[0] + "".join(site + p for p in parts[1:])
        if count_sites(seq, site, circular) == sites:
            return seq


@question_type(
    "biology.recombinant_dna_foundation",
    display_name={"th": "เครื่องมือและขั้นตอนการสร้างดีเอ็นเอรีคอมบิแนนท์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RDNA,
)
class RecombinantDnaFoundation(QuestionType):
    """What each tool does, and the order of the steps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            k = rng.randrange(4)
            ordinals = ("แรก", "ที่สอง", "ที่สาม", "สุดท้าย")
            return _labelled(stem=f"ขั้นตอน{ordinals[k]}ของการสร้างแบคทีเรียดัดแปรพันธุกรรมด้วยดีเอ็นเอรีคอมบิแนนท์คือข้อใด",
                             correct=RDNA_STEPS[k], wrongs=tuple(s for i, s in enumerate(RDNA_STEPS) if i != k), topic=TOPIC_RDNA,
                             hint=RDNA_HINT)
        name, role = rng.choice(TOOLS)
        others = rng.sample([t for t in TOOLS if t[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ในการสร้างดีเอ็นเอรีคอมบิแนนท์ {name}มีหน้าที่อย่างไร", correct=role,
                             wrongs=tuple(t[1] for t in others), topic=TOPIC_RDNA, hint=RDNA_HINT)
        return _labelled(stem=f"ในการสร้างดีเอ็นเอรีคอมบิแนนท์ สิ่งใด{role}", correct=name, wrongs=tuple(t[0] for t in others),
                         topic=TOPIC_RDNA, hint=RDNA_HINT)


@question_type(
    "biology.recombinant_dna_fluency",
    display_name={"th": "หาตำแหน่งตัดของเอนไซม์ตัดจำเพาะและจำนวนชิ้น DNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RDNA,
)
class RecombinantDnaFluency(QuestionType):
    """A linear strand cut n times gives n + 1 pieces; a ring gives n."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, site, _ = rng.choice(RESTRICTION)
        sites = rng.randint(1, 4)
        circular = rng.random() < 0.4
        seq = planted_dna(rng, site, sites, circular)
        pieces = sites if circular else sites + 1
        shape = "พลาสมิด (DNA วงกลม) ที่เขียนตัดเป็นเส้นตรง" if circular else "DNA เส้นตรง"
        ask = rng.random() < 0.5
        return numeric(stem=f"{name} ตัด DNA ที่ลำดับ 5′-{site}-3′ {shape}สายหนึ่งมีลำดับเบส 5′-{seq}-3′ "
                            + ("มีตำแหน่งตัดของเอนไซม์นี้กี่ตำแหน่ง" if ask else "เมื่อตัดด้วยเอนไซม์นี้จนครบทุกตำแหน่งจะได้ DNA กี่ชิ้น"),
                       answer=sites if ask else pieces,
                       wrongs=[pieces if ask else sites, sites + 1 if ask else pieces + 1, max(sites - 1, 0) or sites + 2], unit="ตำแหน่ง" if ask else "ชิ้น",
                       topic=TOPIC_RDNA, hint="หาลำดับเบสที่เอนไซม์จดจำทุกตำแหน่ง DNA เส้นตรงถูกตัด n ตำแหน่งได้ n + 1 ชิ้น DNA วงกลมได้ n ชิ้น")


@question_type(
    "biology.recombinant_dna_application",
    display_name={"th": "ปลายเหนียว ขนาดชิ้น DNA และการคัดเลือกเซลล์ที่ได้รับยีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RDNA,
)
class RecombinantDnaApplication(QuestionType):
    """Fragment sizes from cut positions, sticky ends, and antibiotic selection."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.55:
            length = rng.randrange(2000, 10001, 100)
            cuts = sorted(rng.sample(range(100, length, 50), rng.randint(2, 4)))
            circular = rng.random() < 0.4
            if circular:
                pieces = [b - a for a, b in zip(cuts, cuts[1:])] + [length - cuts[-1] + cuts[0]]
                shape = "พลาสมิดวงกลมขนาด"
            else:
                edges = [0, *cuts, length]
                pieces = [b - a for a, b in zip(edges, edges[1:])]
                shape = "DNA เส้นตรงยาว"
            where = ", ".join(str(c) for c in cuts)
            longest = rng.random() < 0.5
            answer = max(pieces) if longest else min(pieces)
            return numeric(stem=f"{shape} {length} คู่เบส ถูกเอนไซม์ตัดจำเพาะตัดที่ตำแหน่งคู่เบสที่ {where} "
                                f"ชิ้น DNA ที่{'ยาวที่สุด' if longest else 'สั้นที่สุด'}ยาวกี่คู่เบส",
                           answer=answer, wrongs=[min(pieces) if longest else max(pieces), cuts[0], length - cuts[-1]],
                           unit="คู่เบส", topic=TOPIC_RDNA,
                           hint="ความยาวแต่ละชิ้นคือระยะระหว่างตำแหน่งตัดที่อยู่ติดกัน DNA วงกลมต้องนับชิ้นที่ต่อผ่านจุดเริ่มต้นด้วย")
        if roll < 0.8:
            name, site, overhang = rng.choice(RESTRICTION)
            answers = [f"5′-{o}" if o else "ไม่มีปลายยื่น (ปลายทู่)" for _, _, o in RESTRICTION]
            right = answers[[r[0] for r in RESTRICTION].index(name)]
            return _labelled(stem=f"{name} จดจำลำดับ 5′-{site}-3′ ตัดแล้วได้ปลาย DNA แบบใด", correct=right,
                             wrongs=tuple(a for a in answers if a != right), topic=TOPIC_RDNA,
                             hint="EcoRI ตัด G^AATTC ได้ปลายเหนียว AATT BamHI ตัด G^GATCC ได้ GATC HindIII ตัด A^AGCTT ได้ AGCT SmaI ตัดกลางได้ปลายทู่")
        cases = (
            ("เลี้ยงแบคทีเรียหลังใส่พลาสมิดที่มียีนต้านแอมพิซิลลินบนอาหารที่มีแอมพิซิลลิน โคโลนีที่เจริญได้คือข้อใด",
             "แบคทีเรียที่ได้รับพลาสมิด", ("แบคทีเรียที่ไม่ได้รับพลาสมิด", "แบคทีเรียทุกเซลล์เจริญได้เท่ากัน", "ไม่มีแบคทีเรียเจริญได้เลย")),
            ("เหตุใดต้องตัดยีนที่ต้องการและพลาสมิดด้วยเอนไซม์ตัดจำเพาะชนิดเดียวกัน", "เพื่อให้ได้ปลายเหนียวที่เข้าคู่กันได้",
             ("เพื่อให้ DNA ยาวขึ้น", "เพื่อฆ่าแบคทีเรียที่ไม่ต้องการ", "เพื่อเปลี่ยน DNA เป็น RNA")),
            ("การผลิตอินซูลินของคนด้วยแบคทีเรียอาศัยหลักการใด", "นำยีนอินซูลินของคนใส่พลาสมิดแล้วให้แบคทีเรียสร้างอินซูลิน",
             ("ฉีดอินซูลินเข้าไปในแบคทีเรียให้เพิ่มจำนวน", "ผสมพันธุ์แบคทีเรียกับเซลล์ตับอ่อน", "สกัดอินซูลินจากแบคทีเรียทั่วไปโดยตรง")),
        )
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_RDNA, hint=RDNA_HINT)

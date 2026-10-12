"""หลักฐานการเกิดวิวัฒนาการ

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/12

Sets moved here from: science_wave_f51.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f51 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_EVID = "หลักฐานการเกิดวิวัฒนาการ"


EVIDENCE = {
    "หลักฐานจากซากดึกดำบรรพ์": ("ซากดึกดำบรรพ์ในชั้นหินที่อยู่ลึกกว่ามีโครงสร้างไม่ซับซ้อนเท่าชั้นบน",
                                "พบซากดึกดำบรรพ์ของม้าที่มีขนาดตัวและจำนวนนิ้วเปลี่ยนไปตามอายุของชั้นหิน",
                                "พบซากอาร์คีออปเทอริกซ์ที่มีทั้งขนนกและฟันแบบสัตว์เลื้อยคลาน"),
    "หลักฐานจากกายวิภาคเปรียบเทียบ": ("แขนคน ครีบวาฬ และปีกค้างคาวมีกระดูกเรียงแบบเดียวกัน",
                                      "งูเหลือมมีกระดูกขาหลังที่ลดรูปอยู่ภายในลำตัว"),
    "หลักฐานจากวิทยาเอ็มบริโอเปรียบเทียบ": ("เอ็มบริโอของปลา ไก่ และคนระยะแรกมีช่องเหงือกและหางเหมือนกัน",
                                            "เอ็มบริโอของสัตว์มีกระดูกสันหลังระยะแรกมีรูปร่างคล้ายกันมาก"),
    "หลักฐานจากชีวภูมิศาสตร์": ("สัตว์มีถุงหน้าท้องพบมากในทวีปออสเตรเลียที่แยกตัวจากทวีปอื่นมานาน",
                               "นกฟินช์บนหมู่เกาะกาลาปากอสแต่ละเกาะมีจะงอยปากต่างกันแต่คล้ายนกบนทวีปใกล้เคียง"),
    "หลักฐานจากชีววิทยาระดับโมเลกุล": ("ลำดับกรดอะมิโนในไซโทโครมซีของคนและชิมแปนซีเหมือนกันเกือบทั้งหมด",
                                       "สิ่งมีชีวิตทุกชนิดใช้รหัสพันธุกรรมชุดเดียวกันในการสร้างโปรตีน"),
}


EVID_HINT = "ซากดึกดำบรรพ์ กายวิภาคเปรียบเทียบ เอ็มบริโอ ชีวภูมิศาสตร์ และโมเลกุล ต่างบอกว่าสิ่งมีชีวิตมีบรรพบุรุษร่วมกัน"


STRUCTURES = {
    "โครงสร้างกำเนิดเดียวกัน (homologous)": ("แขนคนกับครีบวาฬ", "ปีกค้างคาวกับขาหน้าแมว", "ปีกนกกับแขนคน", "ขาหน้าม้ากับครีบโลมา"),
    "โครงสร้างทำหน้าที่เหมือนกัน (analogous)": ("ปีกนกกับปีกผีเสื้อ", "ปีกค้างคาวกับปีกแมลง", "ตาของหมึกกับตาของคน",
                                              "ครีบของฉลามกับครีบของโลมา"),
    "โครงสร้างที่ลดรูป (vestigial)": ("ไส้ติ่งของคน", "กระดูกก้นกบของคน", "กระดูกเชิงกรานของวาฬ", "ปีกของนกกีวี"),
}


# Amino-acid differences from human cytochrome c (textbook values).
CYTOCHROME_C = {"ชิมแปนซี": 0, "ลิงรีซัส": 1, "สุนัข": 11, "ม้า": 12, "ไก่": 13, "กบ": 18, "ปลาทูน่า": 21,
                "ผีเสื้อกลางคืน": 24, "ยีสต์": 44}


@question_type(
    "biology.evolution_evidence_foundation",
    display_name={"th": "ประเภทของหลักฐานการเกิดวิวัฒนาการ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EVID,
)
class EvolutionEvidenceFoundation(QuestionType):
    """Name the kind of evidence from an example, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(EVIDENCE))
        example = rng.choice(EVIDENCE[kind])
        others = [k for k in EVIDENCE if k != kind]
        if rng.random() < 0.55:
            return _labelled(stem=f"\"{example}\" เป็นหลักฐานการเกิดวิวัฒนาการประเภทใด", correct=kind,
                             wrongs=tuple(others), topic=TOPIC_EVID, hint=EVID_HINT)
        return _labelled(stem=f"ข้อใดเป็น{kind}", correct=example,
                         wrongs=tuple(rng.choice(EVIDENCE[k]) for k in rng.sample(others, 3)), topic=TOPIC_EVID, hint=EVID_HINT)


@question_type(
    "biology.evolution_evidence_fluency",
    display_name={"th": "โครงสร้างกำเนิดเดียวกัน ทำหน้าที่เหมือนกัน และลดรูป"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EVID,
)
class EvolutionEvidenceFluency(QuestionType):
    """Same origin, same job, or left over."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(STRUCTURES))
        example = rng.choice(STRUCTURES[kind])
        hint = ("กำเนิดเดียวกัน: โครงสร้างพื้นฐานเหมือนกันแต่ทำหน้าที่ต่างกัน ทำหน้าที่เหมือนกัน: หน้าที่เหมือนแต่กำเนิดต่างกัน "
                "ลดรูป: เหลืออยู่แต่ไม่ได้ใช้ทำหน้าที่เดิม")
        if rng.random() < 0.5:
            return _labelled(stem=f"{example} จัดเป็นโครงสร้างแบบใด", correct=kind,
                             wrongs=tuple([k for k in STRUCTURES if k != kind] + ["โครงสร้างที่เกิดจากสิ่งแวดล้อมเท่านั้น"]),
                             topic=TOPIC_EVID, hint=hint)
        others = [e for k, es in STRUCTURES.items() if k != kind for e in es]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{kind}", correct=example, wrongs=tuple(others),
                         topic=TOPIC_EVID, hint=hint)


@question_type(
    "biology.evolution_evidence_application",
    display_name={"th": "วิเคราะห์ข้อมูลโมเลกุล ชั้นหิน และอายุซากดึกดำบรรพ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EVID,
)
class EvolutionEvidenceApplication(QuestionType):
    """Fewer amino-acid differences mean a closer relative; deeper rock is older; half-lives date fossils."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            picked = sorted(rng.sample(sorted(CYTOCHROME_C), 4), key=CYTOCHROME_C.get)
            data = {a: CYTOCHROME_C[a] for a in picked}
            closest = rng.random() < 0.5
            right = picked[0] if closest else picked[-1]
            table = " ".join(f"{a} {d} ตำแหน่ง" for a, d in sorted(data.items(), key=lambda x: rng.random()))
            return _labelled(stem=f"จำนวนกรดอะมิโนในไซโทโครมซีที่ต่างจากของคน: {table} สิ่งมีชีวิตใดมีความสัมพันธ์ทางวิวัฒนาการกับคน"
                                  f"{'ใกล้ชิดที่สุด' if closest else 'ห่างที่สุด'}", correct=right,
                             wrongs=tuple(a for a in picked if a != right), topic=TOPIC_EVID,
                             hint="ลำดับกรดอะมิโนต่างกันน้อย แสดงว่าแยกสายวิวัฒนาการจากกันไม่นาน จึงมีความสัมพันธ์ใกล้ชิดกว่า")
        if roll < 0.7:
            half = rng.choice((5730, 1250_000_000, 704_000_000, 4_470_000_000))
            name = {5730: "คาร์บอน-14", 1250_000_000: "โพแทสเซียม-40", 704_000_000: "ยูเรเนียม-235",
                    4_470_000_000: "ยูเรเนียม-238"}[half]
            n = rng.randint(1, 5)
            remain = Fraction(1, 2 ** n)
            shown = f"1/{2 ** n}" if rng.random() < 0.6 else f"ร้อยละ {float(remain * 100):g}"
            return numeric(stem=f"ซากดึกดำบรรพ์มี{name} เหลืออยู่ {shown} ของปริมาณเริ่มต้น ถ้าครึ่งชีวิตของ{name}เท่ากับ "
                                f"{half:,} ปี ซากนี้มีอายุประมาณกี่ปี", answer=n * half,
                           wrongs=[(n + 1) * half, max(n - 1, 1) * half if n > 1 else half // 2, half * 2 ** n], unit="ปี",
                           topic=TOPIC_EVID, hint="เหลือ 1/2 ยกกำลัง n แปลว่าผ่านไป n ครึ่งชีวิต อายุ = n × ครึ่งชีวิต")
        fossils = rng.sample(("ซาก A", "ซาก B", "ซาก C", "ซาก D", "ซาก E"), 4)
        order = " ".join(f"ชั้นที่ {i + 1} พบ{f}" for i, f in enumerate(fossils))
        oldest = rng.random() < 0.5
        right = fossils[-1] if oldest else fossils[0]
        return _labelled(stem=f"ชั้นหินที่ไม่ถูกรบกวนเรียงจากบนลงล่าง: {order} ซากใด{'มีอายุมากที่สุด' if oldest else 'มีอายุน้อยที่สุด'}",
                         correct=right, wrongs=tuple(f for f in fossils if f != right), topic=TOPIC_EVID,
                         hint="ชั้นหินที่ไม่ถูกรบกวน ชั้นล่างเกิดก่อนจึงมีอายุมากกว่าชั้นบน")

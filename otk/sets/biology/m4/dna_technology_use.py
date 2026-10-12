"""การประยุกต์ใช้เทคโนโลยีทางดีเอ็นเอ

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/11

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


TOPIC_TECH = "การประยุกต์ใช้เทคโนโลยีทางดีเอ็นเอ"


FIELDS = {
    "ด้านสิ่งแวดล้อม": ("ใช้จุลินทรีย์ดัดแปรพันธุกรรมย่อยสลายคราบน้ำมันที่รั่วไหลในทะเล",
                        "ใช้แบคทีเรียดัดแปรพันธุกรรมกำจัดสารพิษและโลหะหนักในดิน"),
    "ด้านนิติวิทยาศาสตร์": ("ตรวจลายพิมพ์ DNA จากคราบเลือดในที่เกิดเหตุเพื่อระบุตัวผู้ต้องสงสัย",
                           "พิสูจน์ความสัมพันธ์พ่อแม่ลูกด้วยลายพิมพ์ DNA", "พิสูจน์เอกลักษณ์บุคคลจากซากร่างผู้เสียชีวิตในภัยพิบัติ"),
    "ด้านการแพทย์": ("ผลิตอินซูลินของคนจากแบคทีเรียดัดแปรพันธุกรรม", "ตรวจหายีนที่ทำให้เกิดโรคธาลัสซีเมียในคู่สมรส",
                     "ยีนบำบัดโดยใส่ยีนปกติเข้าสู่เซลล์ของผู้ป่วย", "ผลิตวัคซีนตับอักเสบบีจากยีสต์ดัดแปรพันธุกรรม"),
    "ด้านการเกษตร": ("ฝ้ายและข้าวโพดบีทีที่สร้างโปรตีนฆ่าหนอนแมลงได้เอง", "ข้าวสีทองที่สร้างสารตั้งต้นของวิตามินเอ",
                     "มะละกอดัดแปรพันธุกรรมที่ต้านทานไวรัสใบด่างจุดวงแหวน"),
    "ด้านอุตสาหกรรม": ("ผลิตเอนไซม์ย่อยโปรตีนผสมในผงซักฟอกด้วยจุลินทรีย์ดัดแปรพันธุกรรม",
                       "ผลิตเอนไซม์ไคโมซินสำหรับทำเนยแข็งจากจุลินทรีย์ดัดแปรพันธุกรรม"),
}


ETHICS = (
    ("ข้อใดเป็นข้อควรคำนึงด้านชีวจริยธรรมของการใช้เทคโนโลยีทางดีเอ็นเอ",
     ("ข้อมูลพันธุกรรมส่วนบุคคลอาจถูกนำไปใช้เลือกปฏิบัติ", "ยีนจากพืช GMO อาจถ่ายทอดไปยังพืชป่าและกระทบระบบนิเวศ",
      "ผู้บริโภคควรมีสิทธิ์รับรู้ว่าอาหารมีส่วนผสมจาก GMO"),
     ("DNA ทุกชนิดเป็นพิษต่อมนุษย์", "เทคโนโลยีทางดีเอ็นเอไม่มีประโยชน์ใดเลย", "ลายพิมพ์ DNA ของคนสองคนเหมือนกันเสมอ",
      "การผลิตอินซูลินจากแบคทีเรียทำให้คนไข้กลายพันธุ์")),
)


TECH_HINT = "ดูว่าผลที่ได้ใช้ประโยชน์เรื่องใด สิ่งแวดล้อม นิติวิทยาศาสตร์ การแพทย์ การเกษตร หรืออุตสาหกรรม"


TECH_FACTS = (
    ("PCR ใช้ทำอะไร", "เพิ่มจำนวนชิ้น DNA ที่ต้องการให้มากขึ้นในหลอดทดลอง",
     ("ตัด DNA ตรงตำแหน่งลำดับเบสจำเพาะให้เป็นชิ้นสั้น ๆ", "แยกชิ้น DNA ตามขนาด", "เชื่อมยีนที่ต้องการเข้ากับพลาสมิดของแบคทีเรีย", "แปลรหัส mRNA เป็นโปรตีน")),
    ("DNA พอลิเมอเรสที่ใช้ใน PCR ต้องมีสมบัติใด", "ทนความร้อนสูงได้", ("ทำงานได้ที่ 0 °C เท่านั้น", "ตัด DNA ได้",
                                                                  "สร้าง RNA แทน DNA", "ทำงานได้เฉพาะในเซลล์")),
    ("ขั้นแรกของแต่ละรอบ PCR ที่อุณหภูมิประมาณ 95 °C เกิดอะไรขึ้น", "DNA สายคู่แยกออกเป็นสายเดี่ยว",
     ("ไพรเมอร์เข้าจับกับสาย DNA แม่แบบ", "DNA พอลิเมอเรสต่อสายใหม่", "DNA ถูกตัดเป็นชิ้นเล็ก ๆ", "DNA ถูกแปลรหัสเป็นโปรตีน")),
    ("ในเจลอิเล็กโทรโฟรีซิส ชิ้น DNA เคลื่อนที่ไปทางขั้วใด เพราะเหตุใด", "ขั้วบวก เพราะ DNA มีประจุลบจากหมู่ฟอสเฟต",
     ("ขั้วลบ เพราะ DNA มีประจุบวก", "ขั้วลบ เพราะ DNA มีประจุลบ", "ไม่เคลื่อนที่ เพราะ DNA ไม่มีประจุ",
      "ขั้วบวก เพราะ DNA มีประจุบวก")),
    ("ในเจลอิเล็กโทรโฟรีซิส ชิ้น DNA ใดเคลื่อนที่ได้ไกลที่สุด", "ชิ้นที่สั้นที่สุด",
     ("ชิ้นที่ยาวที่สุด", "ชิ้นที่มีเบส G มากที่สุด", "ทุกชิ้นเคลื่อนที่ได้ระยะเท่ากัน", "ชิ้นที่มีขนาดปานกลาง")),
    ("ขั้นที่สองของแต่ละรอบ PCR เมื่อลดอุณหภูมิลงประมาณ 50-65 °C เกิดอะไรขึ้น", "ไพรเมอร์เข้าจับกับสาย DNA แม่แบบ",
     ("DNA สายคู่แยกออกเป็นสายเดี่ยว", "DNA ถูกตัดเป็นชิ้นเล็ก ๆ", "เอนไซม์ถูกทำลายจนหมด", "DNA ถูกแปลรหัสเป็นโปรตีน")),
    ("ขั้นที่สามของแต่ละรอบ PCR ที่อุณหภูมิประมาณ 72 °C เกิดอะไรขึ้น", "DNA พอลิเมอเรสต่อนิวคลีโอไทด์สร้างสายใหม่",
     ("DNA สายคู่แยกออกเป็นสายเดี่ยว", "ไพรเมอร์หลุดออกจากสายแม่แบบทั้งหมด", "DNA ถูกตัดด้วยเอนไซม์ตัดจำเพาะ", "DNA ถูกย้อมสี")),
    ("สารใดไม่จำเป็นต้องใส่ในหลอดทำ PCR", "เอนไซม์ตัดจำเพาะ",
     ("DNA แม่แบบ", "ไพรเมอร์", "นิวคลีโอไทด์ทั้ง 4 ชนิด", "DNA พอลิเมอเรสที่ทนความร้อน")),
    ("ในเจลอิเล็กโทรโฟรีซิส เจลทำหน้าที่อะไร", "เป็นร่างแหที่ชิ้น DNA ขนาดเล็กเคลื่อนผ่านได้เร็วกว่า",
     ("ให้ประจุลบแก่ DNA ทุกชิ้นเพื่อให้เคลื่อนที่ไปขั้วบวก", "ตัด DNA เป็นชิ้นขนาดต่าง ๆ ขณะเคลื่อนที่ผ่านเจล", "เพิ่มจำนวน DNA", "เชื่อมชิ้น DNA ขนาดต่างกันเข้าด้วยกันเป็นสายยาว")),
    ("ลายพิมพ์ DNA ใช้ระบุตัวบุคคลได้เพราะเหตุใด", "จำนวนซ้ำของลำดับเบสสั้น ๆ บางตำแหน่งแตกต่างกันมากในแต่ละคน",
     ("ทุกคนมี DNA เหมือนกันทุกตำแหน่ง", "DNA ของคนเปลี่ยนไปทุกวัน", "ลายพิมพ์ DNA ได้จากลายนิ้วมือโดยตรง จึงต่างกันในแต่ละคน",
      "แต่ละคนมีจำนวนโครโมโซมไม่เท่ากัน ลายแถบ DNA จึงต่างกัน")),
    ("ฝาแฝดคู่ใดมีลายพิมพ์ DNA เหมือนกันทุกแถบ", "แฝดร่วมไข่ (แฝดแท้)",
     ("แฝดต่างไข่เพศเดียวกัน", "แฝดต่างไข่ต่างเพศ", "พี่น้องที่เกิดห่างกันหนึ่งปี", "พ่อกับลูกชาย")),
)


def _bands(rng: Random, n: int, avoid=()) -> list[int]:
    pool = [b for b in range(200, 3001, 50) if b not in avoid]
    return sorted(rng.sample(pool, n))


@question_type(
    "biology.dna_technology_use_foundation",
    display_name={"th": "ตัวอย่างการใช้เทคโนโลยีทางดีเอ็นเอในด้านต่าง ๆ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TECH,
)
class DnaTechnologyUseFoundation(QuestionType):
    """Sort each use into its field, and weigh the ethics."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            stem, rights, wrongs = ETHICS[0]
            return _labelled(stem=stem, correct=rng.choice(rights), wrongs=tuple(wrongs), topic=TOPIC_TECH,
                             hint="ชีวจริยธรรมคำนึงถึงความเป็นส่วนตัว ความปลอดภัยต่อผู้บริโภคและสิ่งแวดล้อม และสิทธิ์ที่จะรับรู้")
        field = rng.choice(sorted(FIELDS))
        use = rng.choice(FIELDS[field])
        others = [f for f in FIELDS if f != field]
        if roll < 0.6:
            return _labelled(stem=f"\"{use}\" เป็นการใช้เทคโนโลยีทางดีเอ็นเอด้านใด", correct=field,
                             wrongs=tuple(others), topic=TOPIC_TECH, hint=TECH_HINT)
        return _labelled(stem=f"ข้อใดเป็นการใช้เทคโนโลยีทางดีเอ็นเอ{field}", correct=use,
                         wrongs=tuple(rng.choice(FIELDS[f]) for f in rng.sample(others, 3)), topic=TOPIC_TECH, hint=TECH_HINT)


@question_type(
    "biology.dna_technology_use_fluency",
    display_name={"th": "PCR เจลอิเล็กโทรโฟรีซิส และลายพิมพ์ DNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TECH,
)
class DnaTechnologyUseFluency(QuestionType):
    """How PCR, gels and fingerprints work."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(TECH_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TECH,
                         hint="PCR เพิ่มจำนวน DNA รอบละ 2 เท่า เจลแยก DNA ตามขนาด ชิ้นสั้นเคลื่อนไปทางขั้วบวกได้ไกลกว่า")


@question_type(
    "biology.dna_technology_use_application",
    display_name={"th": "อ่านลายพิมพ์ DNA และคำนวณจำนวน DNA จาก PCR"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TECH,
)
class DnaTechnologyUseApplication(QuestionType):
    """A child's bands come from the mother or the father; PCR doubles each cycle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            start = rng.choice((1, 2, 3, 5, 10, 20, 50))
            cycles = rng.randint(3, 20)
            return numeric(stem=f"เริ่ม PCR ด้วย DNA แม่แบบ {start} โมเลกุล ทำ PCR {cycles} รอบ (แต่ละรอบเพิ่มเป็น 2 เท่า) จะได้ DNA กี่โมเลกุล",
                           answer=start * 2 ** cycles, wrongs=[start * 2 * cycles, start * 2 ** (cycles - 1), 2 ** cycles if start > 1 else 2 ** (cycles + 1)],
                           unit="โมเลกุล", topic=TOPIC_TECH, hint="จำนวน DNA หลัง PCR = จำนวนเริ่มต้น × 2 ยกกำลังจำนวนรอบ")
        labels = ("ก", "ข", "ค", "ง")
        if roll < 0.7:
            mother = _bands(rng, 6)
            father = _bands(rng, 6, avoid=mother)
            child = sorted(rng.sample(mother, 3) + rng.sample(father, 3))
            from_father = [b for b in child if b not in mother]
            candidates = [father]
            while len(candidates) < 4:
                fake = _bands(rng, 6, avoid=mother)
                if not set(from_father) <= set(fake) and fake not in candidates:
                    candidates.append(fake)
            rng.shuffle(candidates)
            right = labels[candidates.index(father)]
            listing = " ".join(f"ชาย{ell}: {', '.join(map(str, c))}" for ell, c in zip(labels, candidates))
            return _labelled(stem=f"แถบลายพิมพ์ DNA (คู่เบส) ของแม่: {', '.join(map(str, mother))} ลูก: {', '.join(map(str, child))} "
                                  f"{listing} ชายคนใดอาจเป็นพ่อของเด็ก", correct=f"ชาย{right}",
                             wrongs=tuple(f"ชาย{ell}" for ell in labels if ell != right), topic=TOPIC_TECH,
                             hint="ทุกแถบของลูกต้องมาจากแม่หรือพ่อ แถบของลูกที่แม่ไม่มีต้องพบในพ่อทุกแถบ")
        scene = _bands(rng, 5)
        suspects = [scene]
        while len(suspects) < 4:
            fake = sorted(rng.sample(scene, rng.randint(2, 4)) + _bands(rng, 1, avoid=scene))
            fake = sorted(set(fake))
            if fake != scene and fake not in suspects:
                suspects.append(fake)
        rng.shuffle(suspects)
        right = labels[suspects.index(scene)]
        listing = " ".join(f"ผู้ต้องสงสัย{ell}: {', '.join(map(str, c))}" for ell, c in zip(labels, suspects))
        return _labelled(stem=f"แถบลายพิมพ์ DNA (คู่เบส) จากคราบเลือดในที่เกิดเหตุ: {', '.join(map(str, scene))} {listing} "
                              f"คราบเลือดตรงกับผู้ต้องสงสัยคนใด", correct=f"ผู้ต้องสงสัย{right}",
                         wrongs=tuple(f"ผู้ต้องสงสัย{ell}" for ell in labels if ell != right), topic=TOPIC_TECH,
                         hint="ตัวอย่างจากบุคคลเดียวกันต้องมีแถบตรงกันทุกแถบ ไม่ขาดและไม่เกิน")

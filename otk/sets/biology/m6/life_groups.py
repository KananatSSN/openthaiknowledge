"""ลักษณะของสิ่งมีชีวิตกลุ่มต่าง ๆ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.6/3

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


TOPIC_GROUPS = "ลักษณะของสิ่งมีชีวิตกลุ่มต่าง ๆ"


GROUPS = {
    "แบคทีเรีย": (("อีโคไล", "ไซยาโนแบคทีเรีย", "แล็กโทบาซิลลัสในนมเปรี้ยว", "แบคทีเรียก่อโรคอหิวาตกโรค"),
                  ("เป็นเซลล์โพรแคริโอต ไม่มีเยื่อหุ้มนิวเคลียส", "DNA อยู่ในไซโทพลาซึมบริเวณนิวคลีออยด์")),
    "โพรทิสต์": (("อะมีบา", "พารามีเซียม", "ยูกลีนา", "พลาสโมเดียม", "ราเมือก"),
                 ("เป็นยูแคริโอตที่ส่วนใหญ่เป็นเซลล์เดียว และไม่จัดเป็นพืช ฟังไจ หรือสัตว์", "บางชนิดเคลื่อนที่ด้วยแฟลเจลลัม ซิเลีย หรือเท้าเทียม")),
    "พืช": (("มอส", "เฟิร์น", "สน", "มะม่วง", "ข้าว"),
            ("เป็นยูแคริโอตหลายเซลล์ มีผนังเซลล์เป็นเซลลูโลสและสังเคราะห์ด้วยแสงได้", "มีเอ็มบริโอที่ได้รับอาหารจากต้นแม่")),
    "ฟังไจ": (("เห็ดฟาง", "ยีสต์", "ราขนมปัง", "ราเพนิซิลเลียม"),
              ("ผนังเซลล์มีไคทิน และได้อาหารโดยปล่อยเอนไซม์ย่อยแล้วดูดซึม", "สร้างอาหารเองไม่ได้ และส่วนใหญ่มีเส้นใยเรียกว่าไฮฟา")),
    "สัตว์": (("ฟองน้ำ", "ไฮดรา", "ไส้เดือนดิน", "แมงมุม", "ปลาทู"),
              ("เป็นยูแคริโอตหลายเซลล์ ไม่มีผนังเซลล์ และกินสิ่งมีชีวิตอื่นเป็นอาหาร", "ส่วนใหญ่เคลื่อนที่ได้ในบางช่วงของชีวิต")),
}


GROUP_HINT = ("แบคทีเรียเป็นโพรแคริโอต โพรทิสต์ส่วนใหญ่เซลล์เดียว พืชมีเซลลูโลสและสังเคราะห์ด้วยแสง "
              "ฟังไจมีไคทินและดูดซึมอาหาร สัตว์ไม่มีผนังเซลล์และกินสิ่งมีชีวิตอื่น")


SUBGROUPS = (
    ("พืชไม่มีท่อลำเลียง", "มอสขึ้นบนก้อนหินชื้น ไม่มีราก ลำต้น และใบที่แท้จริง", "พืช"),
    ("พืชมีท่อลำเลียงที่ไม่มีเมล็ด", "เฟิร์นมีท่อลำเลียง สืบพันธุ์ด้วยสปอร์ที่อยู่ใต้ใบ", "พืช"),
    ("พืชเมล็ดเปลือย", "สนมีเมล็ดติดอยู่บนแผ่นของโคน ไม่มีรังไข่หุ้ม", "พืช"),
    ("พืชดอก", "มะม่วงมีดอก และมีผลห่อหุ้มเมล็ด", "พืช"),
    ("ฟองน้ำ (ไฟลัมพอริเฟอรา)", "ลำตัวมีรูพรุนจำนวนมาก ไม่มีเนื้อเยื่อที่แท้จริง", "สัตว์"),
    ("ไนดาเรีย", "ไฮดรามีหนวดรอบปาก และมีเซลล์เข็มพิษ", "สัตว์"),
    ("หนอนตัวแบน", "พยาธิใบไม้มีลำตัวแบนบาง ทางเดินอาหารมีช่องเปิดทางเดียว", "สัตว์"),
    ("หนอนตัวกลม", "พยาธิไส้เดือนลำตัวกลมยาวไม่มีปล้อง ทางเดินอาหารสมบูรณ์", "สัตว์"),
    ("แอนเนลิด", "ไส้เดือนดินลำตัวเป็นปล้องชัดเจนทั้งภายนอกและภายใน", "สัตว์"),
    ("มอลลัสก์", "หอยทากมีลำตัวนิ่ม มีแมนเทิลสร้างเปลือกหุ้ม", "สัตว์"),
    ("อาร์โทรพอด", "แมงมุมมีขาเป็นข้อปล้อง และมีโครงร่างแข็งภายนอก", "สัตว์"),
    ("เอไคโนเดิร์ม", "ดาวทะเลผิวขรุขระมีหนาม และเคลื่อนที่ด้วยระบบท่อน้ำ", "สัตว์"),
    ("คอร์เดต", "ปลาทูมีโนโทคอร์ดในระยะเอ็มบริโอ และมีเส้นประสาทกลวงด้านหลัง", "สัตว์"),
)


@question_type(
    "biology.life_groups_foundation",
    display_name={"th": "ตัวอย่างสิ่งมีชีวิตกลุ่มแบคทีเรีย โพรทิสต์ พืช ฟังไจ และสัตว์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUPS,
)
class LifeGroupsFoundation(QuestionType):
    """Which group an organism belongs to, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        group = rng.choice(sorted(GROUPS))
        example = rng.choice(GROUPS[group][0])
        others = [g for g in GROUPS if g != group]
        if rng.random() < 0.55:
            return _labelled(stem=f"{example}จัดอยู่ในสิ่งมีชีวิตกลุ่มใด", correct=group, wrongs=tuple(others),
                             topic=TOPIC_GROUPS, hint=GROUP_HINT)
        return _labelled(stem=f"ข้อใดเป็นสิ่งมีชีวิตกลุ่ม{group}", correct=example,
                         wrongs=tuple(rng.choice(GROUPS[g][0]) for g in rng.sample(others, 3)), topic=TOPIC_GROUPS, hint=GROUP_HINT)


@question_type(
    "biology.life_groups_fluency",
    display_name={"th": "ลักษณะสำคัญของสิ่งมีชีวิตแต่ละกลุ่ม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUPS,
)
class LifeGroupsFluency(QuestionType):
    """The defining traits of each group."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        group = rng.choice(sorted(GROUPS))
        trait = rng.choice(GROUPS[group][1])
        others = [g for g in GROUPS if g != group]
        if rng.random() < 0.5:
            return _labelled(stem=f"สิ่งมีชีวิตที่ \"{trait}\" จัดอยู่ในกลุ่มใด", correct=group, wrongs=tuple(others),
                             topic=TOPIC_GROUPS, hint=GROUP_HINT)
        return _labelled(stem=f"ข้อใดเป็นลักษณะของสิ่งมีชีวิตกลุ่ม{group}", correct=trait,
                         wrongs=tuple(rng.choice(GROUPS[g][1]) for g in rng.sample(others, 3)), topic=TOPIC_GROUPS, hint=GROUP_HINT)


@question_type(
    "biology.life_groups_application",
    display_name={"th": "จัดกลุ่มย่อยของพืชและสัตว์จากลักษณะที่สังเกตได้"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROUPS,
)
class LifeGroupsApplication(QuestionType):
    """Place an organism in its plant or animal subgroup from what it looks like."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, description, kingdom = rng.choice(SUBGROUPS)
        same = [s for s in SUBGROUPS if s[2] == kingdom and s[0] != name]
        others = rng.sample(same, 3)
        if rng.random() < 0.6:
            return _labelled(stem=f"\"{description}\" จัดอยู่ในกลุ่มใด", correct=name, wrongs=tuple(s[0] for s in others),
                             topic=TOPIC_GROUPS, hint="พืชแบ่งตามการมีท่อลำเลียง เมล็ด และดอก สัตว์แบ่งตามเนื้อเยื่อ สมมาตร ช่องลำตัว ปล้อง และโครงร่าง")
        return _labelled(stem=f"ข้อใดเป็นลักษณะของสิ่งมีชีวิตกลุ่ม{name}", correct=description, wrongs=tuple(s[1] for s in others),
                         topic=TOPIC_GROUPS, hint="พืชแบ่งตามการมีท่อลำเลียง เมล็ด และดอก สัตว์แบ่งตามเนื้อเยื่อ สมมาตร ช่องลำตัว ปล้อง และโครงร่าง")

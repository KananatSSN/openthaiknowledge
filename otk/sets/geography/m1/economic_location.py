"""ทำเลที่ตั้งของกิจกรรมทางเศรษฐกิจ

ภูมิศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ส 5.2 ม.1/1, ส 5.2 ม.1/2
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import M1, SUBJECT, scenario, stage

PROVENANCE = Provenance("original")


TOPIC = "ทำเลที่ตั้งของกิจกรรมทางเศรษฐกิจ"


@question_type(
    "geog.economic_sector_m1",
    display_name={"th": "จำแนกกิจกรรมทางเศรษฐกิจขั้นปฐมภูมิ ทุติยภูมิ และตติยภูมิ"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class EconomicSector(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็น{category}"
    CATEGORIES = [
        Category("กิจกรรมขั้นปฐมภูมิ (ได้ผลผลิตจากธรรมชาติโดยตรง)",
                 ("การทำนาข้าว", "การประมงทะเล", "การทำเหมืองถ่านหิน", "การเลี้ยงโคนม",
                  "การทำป่าไม้")),
        Category("กิจกรรมขั้นทุติยภูมิ (แปรรูปหรือผลิตสินค้า)",
                 ("โรงงานผลิตรถยนต์", "โรงสีข้าว", "โรงงานทำปลากระป๋อง", "โรงกลั่นน้ำมัน",
                  "โรงงานทอผ้า")),
        Category("กิจกรรมขั้นตติยภูมิ (บริการ)",
                 ("ธนาคาร", "โรงพยาบาล", "การท่องเที่ยว", "บริษัทขนส่งสินค้า", "ร้านค้าปลีก")),
    ]


@question_type(
    "geog.location_factor_m1",
    display_name={"th": "แยกปัจจัยทางกายภาพและปัจจัยทางสังคมที่มีผลต่อทำเลที่ตั้ง"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class LocationFactor(ClassifyType):
    ASKS = ("pick",)           # two groups: a classify question would offer two choices
    PICK_STEM = "ข้อใดเป็น{category}ที่มีผลต่อทำเลที่ตั้งของกิจกรรมทางเศรษฐกิจ"
    CATEGORIES = [
        Category("ปัจจัยทางกายภาพ",
                 ("ลักษณะภูมิประเทศ", "ภูมิอากาศ", "ความอุดมสมบูรณ์ของดิน", "แหล่งน้ำ",
                  "แหล่งแร่และทรัพยากร")),
        Category("ปัจจัยทางสังคม",
                 ("จำนวนแรงงาน", "ตลาดรับซื้อสินค้า", "เส้นทางคมนาคม", "นโยบายของรัฐบาล",
                  "เงินทุนและเทคโนโลยี")),
    ]


SITES = (
    ("บริษัทจะตั้งโรงงานทำปลากระป๋อง",
     "ใกล้ท่าเรือประมง ได้วัตถุดิบสดและขนส่งสะดวก", ()),
    ("บริษัทจะตั้งโรงงานน้ำตาลทราย",
     "ใกล้ไร่อ้อย เพราะอ้อยหนักและเสียง่ายหลังตัด", ()),
    ("บริษัทจะตั้งศูนย์กระจายสินค้าทั่วประเทศ",
     "ใกล้ทางหลวงสายหลักและชุมทางขนส่ง", ()),
    ("บริษัทจะเปิดห้างสรรพสินค้าขนาดใหญ่",
     "ในเมืองที่ประชากรหนาแน่นและมีกำลังซื้อสูง", ()),
    ("บริษัทจะเปิดรีสอร์ตสำหรับนักดำน้ำ",
     "ใกล้แนวปะการังที่น้ำทะเลใส", ()),
    ("บริษัทจะตั้งโรงงานชิ้นส่วนอิเล็กทรอนิกส์เพื่อส่งออก",
     "ในนิคมอุตสาหกรรมใกล้ท่าเรือน้ำลึก", ()),
)


@question_type(
    "geog.choose_location_m1",
    display_name={"th": "เลือกทำเลที่ตั้งที่เหมาะกับกิจกรรมทางเศรษฐกิจ"},
    level=M1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class ChooseLocation(QuestionType):
    def build(self, rng: Random, **params):
        return scenario(rng, SITES, ask="ทำเลใดเหมาะสมที่สุด",
                        hint="ถามว่ากิจกรรมนี้ต้องการอะไรมากที่สุด วัตถุดิบ ตลาด แรงงาน หรือการขนส่ง แล้วเลือกทำเลที่ให้สิ่งนั้น",
                        topic=TOPIC)

# More rows and items: these tables held five or six, so a learner met them
# all in a few tries. Each added situation is one no other row answers.
SITES += (
    ('บริษัทจะตั้งโรงงานแปรรูปน้ำยางพารา',
     'ใกล้สวนยางในภาคใต้ เพื่อลดค่าขนส่งน้ำยาง', ()),
    ('บริษัทจะสร้างโรงไฟฟ้าพลังน้ำ',
     'หุบเขาที่มีแม่น้ำไหลแรงและสร้างเขื่อนได้', ()),
    ('บริษัทจะเปิดโรงเรียนสอนพิเศษ',
     'ใกล้โรงเรียนและชุมชนที่มีนักเรียนจำนวนมาก', ()),
    ('บริษัทจะตั้งฟาร์มกังหันลมผลิตไฟฟ้า',
     'ชายฝั่งหรือที่สูงที่มีลมพัดแรงสม่ำเสมอ', ()),
    ('บริษัทจะตั้งโรงงานปูนซีเมนต์',
     'ใกล้ภูเขาหินปูนซึ่งเป็นวัตถุดิบหลัก', ()),
    ('รัฐบาลจะสร้างสนามบินแห่งใหม่',
     'ที่ราบกว้างนอกเมืองที่ไม่มีภูเขาขวางเส้นทางบิน', ()),
)

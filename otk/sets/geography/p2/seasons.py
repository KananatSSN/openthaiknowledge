"""ฤดูกาลกับการดำเนินชีวิต

ภูมิศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ส 5.2 ป.2/3
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.sets._support.geography import P2, SUBJECT, stage

PROVENANCE = Provenance("original")


TOPIC = "ฤดูกาลกับการดำเนินชีวิต"


@question_type(
    "geog.season_month_p2",
    display_name={"th": "บอกเดือนที่อยู่ในฤดูร้อน ฤดูฝน และฤดูหนาวของประเทศไทย"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class SeasonMonth(ClassifyType):
    # The seasons turn mid-month (กรมอุตุนิยมวิทยา: ร้อน mid-Feb to mid-May,
    # ฝน mid-May to mid-Oct, หนาว mid-Oct to mid-Feb), so February, May and
    # October belong to two seasons and are left out.
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็นเดือนใน{category}ของประเทศไทย"
    CATEGORIES = [
        Category("ฤดูร้อน", ("มีนาคม", "เมษายน")),
        Category("ฤดูฝน", ("มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน")),
        Category("ฤดูหนาว", ("พฤศจิกายน", "ธันวาคม", "มกราคม")),
    ]


@question_type(
    "geog.season_life_p2",
    display_name={"th": "เชื่อมโยงฤดูกาลกับการดำเนินชีวิตของคนไทย"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class SeasonLife(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็นการดำเนินชีวิตที่เหมาะกับ{category}"
    CATEGORIES = [
        Category("ฤดูร้อน", ("ดื่มน้ำมาก ๆ และหลบแดดช่วงบ่าย", "เล่นน้ำในวันสงกรานต์",
                             "สวมเสื้อผ้าบางที่ระบายความร้อนได้ดี")),
        Category("ฤดูฝน", ("ชาวนาไถนาและหว่านข้าว", "พกร่มหรือเสื้อกันฝนเมื่อออกจากบ้าน",
                           "ระวังถนนลื่นและน้ำท่วมขัง")),
        Category("ฤดูหนาว", ("สวมเสื้อกันหนาวในตอนเช้า", "ชาวนาเกี่ยวข้าวที่สุกเต็มทุ่ง",
                             "ขึ้นดอยไปชมทะเลหมอกยามเช้า")),
    ]


@question_type(
    "geog.season_plan_p2",
    display_name={"th": "วางแผนกิจกรรมให้เหมาะกับฤดูกาล"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class SeasonPlan(ConceptBankType):
    ITEMS = [
        Concept("ครอบครัวอยากขึ้นดอยไปชมทะเลหมอก ควรไปเที่ยวในเดือนใด", "ธันวาคม",
                ("เมษายน", "กรกฎาคม", "สิงหาคม")),
        Concept("ร้านค้าควรนำร่มและเสื้อกันฝนมาวางขายให้มากในเดือนใด", "สิงหาคม",
                ("มกราคม", "มีนาคม", "ธันวาคม")),
        Concept("ร้านค้าควรเตรียมพัดลมและน้ำแข็งไว้ขายให้มากในเดือนใด", "เมษายน",
                ("ธันวาคม", "สิงหาคม", "กรกฎาคม")),
        Concept("ชาวนาเริ่มไถนาและหว่านข้าวนาปีเมื่อฝนเริ่มตก ราวเดือนใด", "มิถุนายน",
                ("ธันวาคม", "มีนาคม", "มกราคม")),
        Concept("ชาวนาเกี่ยวข้าวนาปีที่สุกเต็มทุ่ง ราวเดือนใด", "พฤศจิกายน",
                ("มิถุนายน", "เมษายน", "กรกฎาคม")),
        Concept("โรงเรียนจะจัดค่ายพักแรมกลางแจ้ง ไม่อยากให้ฝนตกและไม่อยากให้ร้อนจัด ควรจัดเดือนใด",
                "ธันวาคม", ("กรกฎาคม", "เมษายน", "กันยายน")),
    ]

# More rows and items: these tables held five or six, so a learner met them
# all in a few tries. Each added situation is one no other row answers.
SeasonPlan.ITEMS = [*SeasonPlan.ITEMS,
    Concept('ชาวสวนผลไม้ภาคตะวันออกเก็บทุเรียนและมังคุดได้มากราวเดือนใด',
            'พฤษภาคม',
            ('ธันวาคม', 'กันยายน', 'มกราคม', 'ตุลาคม')),
    Concept('เทศกาลสงกรานต์ซึ่งอยู่ในฤดูร้อน ตรงกับเดือนใด',
            'เมษายน',
            ('ธันวาคม', 'สิงหาคม', 'ตุลาคม', 'มิถุนายน')),
    Concept('ประเพณีลอยกระทงซึ่งน้ำในแม่น้ำลำคลองเต็มตลิ่ง ตรงกับราวเดือนใด',
            'พฤศจิกายน',
            ('เมษายน', 'มีนาคม', 'มิถุนายน', 'กุมภาพันธ์')),
    Concept('สตรอว์เบอร์รีบนดอยทางภาคเหนือออกผลมากในช่วงอากาศหนาว ราวเดือนใด',
            'มกราคม',
            ('พฤษภาคม', 'กรกฎาคม', 'กันยายน', 'เมษายน')),
]

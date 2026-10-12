"""การใช้ประโยชน์สารประกอบอินทรีย์ในชีวิตประจำวันและอุตสาหกรรม

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/10

Sets moved here from: science_wave_f28.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f28 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_USE = "การใช้ประโยชน์สารประกอบอินทรีย์ในชีวิตประจำวันและอุตสาหกรรม"


# (compound, class, use)
ORGANIC_USES = (
    ("เอทานอล", "แอลกอฮอล์", "ผสมกับน้ำมันเบนซินเป็นแก๊สโซฮอล์"),
    ("เอทิลีนไกลคอล (เอทาน-1,2-ไดออล)", "แอลกอฮอล์", "สารป้องกันการเยือกแข็งในหม้อน้ำรถยนต์"),
    ("กลีเซอรอล", "แอลกอฮอล์", "สารให้ความชุ่มชื้นในเครื่องสำอาง"),
    ("โพรพาโนน (แอซีโตน)", "คีโตน", "น้ำยาล้างเล็บและตัวทำละลาย"),
    ("เมทานาล (ฟอร์มาลดีไฮด์)", "แอลดีไฮด์", "สารละลายฟอร์มาลินสำหรับรักษาสภาพตัวอย่างสิ่งมีชีวิต"),
    ("กรดเอทาโนอิก", "กรดคาร์บอกซิลิก", "น้ำส้มสายชูสำหรับปรุงอาหาร"),
    ("กรดซิทริก", "กรดคาร์บอกซิลิก", "ให้รสเปรี้ยวและช่วยถนอมเครื่องดื่ม"),
    ("3-เมทิลบิวทิลเอทาโนเอต", "เอสเทอร์", "สารแต่งกลิ่นกล้วย"),
    ("เอทิลบิวทาโนเอต", "เอสเทอร์", "สารแต่งกลิ่นสับปะรด"),
    ("เมทิลซาลิซิเลต", "เอสเทอร์", "น้ำมันระกำในยาทาแก้ปวดเมื่อย"),
    ("ไบโอดีเซล (เมทิลเอสเทอร์ของกรดไขมัน)", "เอสเทอร์", "เชื้อเพลิงเครื่องยนต์ดีเซล"),
    ("ยูเรีย", "เอไมด์", "ปุ๋ยให้ธาตุไนโตรเจน"),
    ("พาราเซตามอล", "เอไมด์", "ยาลดไข้และบรรเทาปวด"),
    ("อีทอกซีอีเทน (ไดเอทิลอีเทอร์)", "อีเทอร์", "ตัวทำละลายในห้องปฏิบัติการ และเคยใช้เป็นยาสลบ"),
    ("โพรเพนและบิวเทน", "แอลเคน", "แก๊สหุงต้ม"),
    ("อีทีน (เอทิลีน)", "แอลคีน", "เร่งการสุกของผลไม้"),
    ("เอไทน์ (แอซีทิลีน)", "แอลไคน์", "เชื้อเพลิงในการเชื่อมและตัดโลหะ"),
    ("เมทิลเบนซีน (โทลูอีน)", "อะโรมาติกไฮโดรคาร์บอน", "ตัวทำละลายในทินเนอร์"),
)


# (ester, smell, acid, alcohol)
FLAVOURS = (
    ("3-เมทิลบิวทิลเอทาโนเอต", "กล้วย", "กรดเอทาโนอิก", "3-เมทิลบิวทาน-1-ออล"),
    ("เอทิลบิวทาโนเอต", "สับปะรด", "กรดบิวทาโนอิก", "เอทานอล"),
    ("ออกทิลเอทาโนเอต", "ส้ม", "กรดเอทาโนอิก", "ออกทาน-1-ออล"),
    ("เมทิลบิวทาโนเอต", "แอปเปิล", "กรดบิวทาโนอิก", "เมทานอล"),
    ("เมทิลซาลิซิเลต", "น้ำมันระกำ", "กรดซาลิซิลิก", "เมทานอล"),
)


MISUSES = (
    ("แช่อาหารทะเลในฟอร์มาลินให้ดูสด", ("ใช้น้ำส้มสายชูปรุงรสอาหาร", "ใช้แอซีโตนล้างยาทาเล็บ",
                                          "ใช้เอทานอลเช็ดทำความสะอาดแผลรอบนอก")),
    ("ผสมเมทานอลในเครื่องดื่มแทนเอทานอล", ("ใช้แก๊สโซฮอล์เติมรถยนต์", "ใช้กลีเซอรอลในโลชัน",
                                            "ใช้ยูเรียเป็นปุ๋ย")),
    ("ใช้ทินเนอร์ที่มีโทลูอีนในห้องปิดโดยไม่ระบายอากาศ", ("ใช้แก๊สเอทิลีนบ่มผลไม้ในห้องบ่ม",
                                                        "ใช้เอทิลีนไกลคอลในหม้อน้ำรถยนต์",
                                                        "ใช้น้ำมันระกำทาแก้ปวดเมื่อยภายนอก")),
)


@question_type(
    "chem.organic_use_foundation",
    display_name={"th": "สารประกอบอินทรีย์กับการใช้ประโยชน์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_USE,
)
class OrganicUseFoundation(QuestionType):
    """Match a use to its compound."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, use = rng.choice(ORGANIC_USES)
        others = [u[0] for u in ORGANIC_USES if u[0] != name]
        return _labelled(stem=f"สารใดใช้เป็น{use}", correct=name, wrongs=tuple(others), topic=TOPIC_USE,
                         hint="นึกถึงสมบัติของสาร: ระเหยง่าย มีกลิ่น ละลายน้ำ เผาไหม้ได้ หรือฆ่าเชื้อ")


@question_type(
    "chem.organic_use_fluency",
    display_name={"th": "ประเภทของสารอินทรีย์ที่ใช้ในชีวิตประจำวัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_USE,
)
class OrganicUseFluency(QuestionType):
    """Name the class of the compound behind a use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, cls, use = rng.choice(ORGANIC_USES)
        right = f"{name} ซึ่งเป็น{cls}"
        wrong_classes = sorted({u[1] for u in ORGANIC_USES} - {cls})
        others = [f"{u[0]} ซึ่งเป็น{u[1]}" for u in ORGANIC_USES if u[0] != name]
        wrongs = (f"{name} ซึ่งเป็น{rng.choice(wrong_classes)}", *rng.sample(others, 2))
        return _labelled(stem=f"สารที่ใช้เป็น{use} คือสารใดและจัดเป็นสารประเภทใด", correct=right, wrongs=wrongs,
                         topic=TOPIC_USE, hint="ระบุสารก่อน แล้วดูหมู่ฟังก์ชันในโครงสร้างของสารนั้น")


@question_type(
    "chem.organic_use_application",
    display_name={"th": "สังเคราะห์สารแต่งกลิ่นและใช้สารอินทรีย์อย่างปลอดภัย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_USE,
)
class OrganicUseApplication(QuestionType):
    """Which acid and alcohol make a flavour ester, and which use is unsafe."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            ester_name, smell, acid, alcohol = rng.choice(FLAVOURS)
            right = f"{acid} กับ {alcohol}"
            acids = sorted({f[2] for f in FLAVOURS})
            alcohols = sorted({f[3] for f in FLAVOURS})
            pool = [f"{a} กับ {b}" for a in acids for b in alcohols if f"{a} กับ {b}" != right]
            return _labelled(stem=f"ต้องการสังเคราะห์{ester_name} ซึ่งให้กลิ่น{smell} ต้องใช้กรดและแอลกอฮอล์คู่ใด",
                             correct=right, wrongs=tuple(pool), topic=TOPIC_USE,
                             hint="ส่วนหน้าของชื่อเอสเทอร์มาจากแอลกอฮอล์ ส่วน -โอเอต มาจากกรด")
        bad, fine = rng.choice(MISUSES)
        others = [f for _, fs in MISUSES for f in fs]
        return _labelled(stem="ข้อใดเป็นการใช้สารประกอบอินทรีย์ที่ไม่เหมาะสมและเป็นอันตราย", correct=bad,
                         wrongs=tuple(others), topic=TOPIC_USE,
                         hint="ฟอร์มาลินและเมทานอลเป็นพิษเมื่อเข้าสู่ร่างกาย ไอของตัวทำละลายอินทรีย์เป็นอันตรายเมื่อสูดดม")

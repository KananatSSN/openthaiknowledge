"""ลิพิด

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/6

Sets moved here from: science_wave_f45.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f45 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_LIPID = "ลิพิด"


LIPIDS = (
    ("ไตรกลีเซอไรด์", "กลีเซอรอล 1 โมเลกุลกับกรดไขมัน 3 โมเลกุล", "สะสมพลังงานและเป็นฉนวนรักษาความร้อน"),
    ("ฟอสโฟลิพิด", "กลีเซอรอล กรดไขมัน 2 โมเลกุล และหมู่ฟอสเฟต", "เป็นองค์ประกอบหลักของเยื่อหุ้มเซลล์"),
    ("สเตอรอยด์ (เช่น คอเลสเตอรอล)", "คาร์บอนต่อกันเป็นวง 4 วง", "เป็นองค์ประกอบของเยื่อหุ้มเซลล์สัตว์และสารตั้งต้นของฮอร์โมนเพศ"),
    ("ไข (wax)", "กรดไขมันสายยาวกับแอลกอฮอล์สายยาว", "เคลือบผิวใบพืชและขนนกกันน้ำ"),
)


LIPID_EXAMPLES = (
    ("น้ำมันถั่วเหลือง", "ไตรกลีเซอไรด์"), ("ไขมันหมู", "ไตรกลีเซอไรด์"), ("เนย", "ไตรกลีเซอไรด์"),
    ("เลซิทินในไข่แดง", "ฟอสโฟลิพิด"), ("คอเลสเตอรอล", "สเตอรอยด์ (เช่น คอเลสเตอรอล)"),
    ("ฮอร์โมนเทสโทสเตอโรน", "สเตอรอยด์ (เช่น คอเลสเตอรอล)"), ("ฮอร์โมนเอสโทรเจน", "สเตอรอยด์ (เช่น คอเลสเตอรอล)"),
    ("ไขผึ้ง", "ไข (wax)"), ("สารเคลือบผิวใบบัว", "ไข (wax)"), ("สารที่ต่อมน้ำมันของนกใช้เคลือบขน", "ไข (wax)"),
)


FATS = (
    ("กรดไขมันอิ่มตัว", "มีแต่พันธะเดี่ยวระหว่างคาร์บอน", "มักเป็นของแข็งที่อุณหภูมิห้อง เช่น ไขมันสัตว์"),
    ("กรดไขมันไม่อิ่มตัว", "มีพันธะคู่ระหว่างคาร์บอนอย่างน้อยหนึ่งพันธะ", "มักเป็นของเหลวที่อุณหภูมิห้อง เช่น น้ำมันพืช"),
)


LIPID_FACTS = (
    ("ลิพิดให้พลังงานต่อกรัมเทียบกับคาร์โบไฮเดรตอย่างไร", "มากกว่าประมาณ 2 เท่า (ประมาณ 9 kcal ต่อ 4 kcal ต่อกรัม)",
     ("น้อยกว่าครึ่งหนึ่ง", "เท่ากัน (ประมาณ 4 kcal ต่อกรัม ทั้งไขมันและคาร์โบไฮเดรต)", "มากกว่าประมาณ 10 เท่า (ประมาณ 40 kcal ต่อ 4 kcal ต่อกรัม)")),
    ("เพราะเหตุใดลิพิดจึงไม่ละลายน้ำ", "โมเลกุลส่วนใหญ่ไม่มีขั้ว", ("มีมวลโมเลกุลน้อยเกินไป", "โมเลกุลมีขั้วมากเกินไป",
                                                              "เป็นสารประกอบไอออนิก")),
    ("ฟอสโฟลิพิดเรียงตัวเป็นเยื่อหุ้มเซลล์สองชั้นได้เพราะเหตุใด", "ส่วนหัวมีขั้วชอบน้ำ ส่วนหางไม่มีขั้วไม่ชอบน้ำ",
     ("ส่วนหัวไม่ชอบน้ำ ส่วนหางมีขั้วชอบน้ำ", "ทั้งส่วนหัวและส่วนหางไม่มีขั้วและไม่ชอบน้ำ", "ส่วนหัวไม่มีขั้ว ส่วนหางมีขั้ว")),
    ("การทดสอบลิพิดอย่างง่ายทำได้อย่างไร", "ถูบนกระดาษแล้วเกิดรอยโปร่งแสง", ("หยดสารละลายไอโอดีนแล้วได้สีน้ำเงินเข้ม",
                                                                          "ต้มกับเบเนดิกต์แล้วได้ตะกอนแดงอิฐ",
                                                                          "หยดไบยูเร็ตแล้วได้สีม่วง")),
)


@question_type(
    "biology.lipid_foundation",
    display_name={"th": "ชนิดของลิพิด โครงสร้าง และหน้าที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIPID,
)
class LipidFoundation(QuestionType):
    """Triglycerides store, phospholipids build membranes, steroids signal, waxes waterproof."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, made, role = rng.choice(LIPIDS)
        others = [ell for ell in LIPIDS if ell[0] != name]
        if rng.random() < 0.4:
            example, group = rng.choice(LIPID_EXAMPLES)
            pool = [ell[0] for ell in LIPIDS if ell[0] != group] + ["คาร์โบไฮเดรต", "โปรตีน"]
            return _labelled(stem=f"{example}จัดเป็นสารชนิดใด", correct=group, wrongs=tuple(pool),
                             topic=TOPIC_LIPID, hint="น้ำมันและไขมันเป็นไตรกลีเซอไรด์ ฮอร์โมนเพศและคอเลสเตอรอลเป็นสเตอรอยด์")
        kind = rng.randrange(3)
        if kind == 0:
            return _labelled(stem=f"{name}ประกอบด้วยอะไร", correct=made, wrongs=tuple(ell[1] for ell in others), topic=TOPIC_LIPID,
                             hint="ไตรกลีเซอไรด์ = กลีเซอรอล + กรดไขมัน 3 ฟอสโฟลิพิดมีหมู่ฟอสเฟต สเตอรอยด์เป็นวง 4 วง")
        if kind == 1:
            return _labelled(stem=f"{name}มีหน้าที่ใด", correct=role, wrongs=tuple(ell[2] for ell in others), topic=TOPIC_LIPID,
                             hint="ไตรกลีเซอไรด์สะสมพลังงาน ฟอสโฟลิพิดสร้างเยื่อหุ้มเซลล์ สเตอรอยด์เป็นฮอร์โมน")
        return _labelled(stem=f"ลิพิดใดทำหน้าที่{role}", correct=name, wrongs=tuple(ell[0] for ell in others), topic=TOPIC_LIPID,
                         hint="นึกถึงโครงสร้างที่เหมาะกับหน้าที่ของลิพิดแต่ละชนิด")


@question_type(
    "biology.lipid_fluency",
    display_name={"th": "กรดไขมันอิ่มตัวและไม่อิ่มตัว และการสร้างไตรกลีเซอไรด์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIPID,
)
class LipidFluency(QuestionType):
    """Double bonds kink the chain; three ester bonds release three waters."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            kind, structure, state = rng.choice(FATS)
            other = [f for f in FATS if f[0] != kind][0]
            if rng.random() < 0.5:
                return _labelled(stem=f"{kind}มีโครงสร้างอย่างไร", correct=structure,
                                 wrongs=(other[1], "มีหมู่ฟอสเฟตที่ปลายสาย", "เป็นวงคาร์บอน 4 วง"), topic=TOPIC_LIPID,
                                 hint="อิ่มตัว = มีแต่พันธะเดี่ยว ไม่อิ่มตัว = มีพันธะคู่")
            return _labelled(stem=f"ไขมันที่มี{kind}เป็นส่วนใหญ่มีลักษณะอย่างไร", correct=state,
                             wrongs=(other[2], "ละลายน้ำได้ดีทุกอุณหภูมิ", "เป็นแก๊สที่อุณหภูมิห้อง"), topic=TOPIC_LIPID,
                             hint="พันธะคู่ทำให้สายหักงอ เรียงชิดกันไม่ได้ จึงเป็นของเหลวที่อุณหภูมิห้อง")
        n = rng.randint(1, 40)
        what = rng.choice(("โมเลกุลน้ำที่เกิดขึ้น", "กรดไขมันที่ใช้"))
        answer = 3 * n
        return numeric(stem=f"สร้างไตรกลีเซอไรด์ {n} โมเลกุลจากกลีเซอรอลและกรดไขมัน จะมี{what}กี่โมเลกุล", answer=answer,
                       wrongs=[n, 2 * n, 3 * n + 1], unit="โมเลกุล", topic=TOPIC_LIPID,
                       hint="ไตรกลีเซอไรด์ 1 โมเลกุล = กลีเซอรอล 1 + กรดไขมัน 3 และเกิดน้ำ 3 โมเลกุล")


@question_type(
    "biology.lipid_application",
    display_name={"th": "สมบัติและการทดสอบลิพิด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIPID,
)
class LipidApplication(QuestionType):
    """Non-polar, energy-rich, and double-layered in membranes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(LIPID_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LIPID,
                         hint="ลิพิดส่วนใหญ่ไม่มีขั้ว ไม่ละลายน้ำ และให้พลังงานสูง")

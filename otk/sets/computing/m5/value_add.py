"""การใช้ข้อมูลเพิ่มมูลค่าผลิตภัณฑ์และบริการ

วิทยาการคำนวณ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.5/1

Sets moved here from: technology_t3s6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s3 import _bank
from otk.sets._support.technology_t3s6 import M5

PROVENANCE = Provenance("original")


VALUE_TOPIC = "การใช้ข้อมูลเพิ่มมูลค่าผลิตภัณฑ์และบริการ"


#: Each wrong fix is a real change a shop might make, just not one the data
#: points to.
EVIDENCE = (
    ("ข้อมูลการสั่งซื้อของร้านกาแฟพบว่าลูกค้าช่วงเช้ารอคิวนานจนยกเลิกการสั่งบ่อย",
     "เพิ่มระบบสั่งและชำระเงินล่วงหน้าผ่านแอปเพื่อลดเวลารอ",
     ("เพิ่มเมนูของหวานอีก 20 รายการเพื่อดึงลูกค้าช่วงเช้า",
      "ขึ้นราคาทุกเมนูในช่วงเช้าเพื่อลดจำนวนลูกค้าที่มาต่อคิว",
      "เปลี่ยนสีป้ายร้านให้เด่นขึ้นเพื่อให้ลูกค้าหาร้านเจอง่าย",
      "ปิดร้านในช่วงเช้าแล้วเปิดขายเฉพาะช่วงบ่ายที่ลูกค้าน้อย",
      "ย้ายร้านไปเปิดในจังหวัดอื่นที่มีลูกค้าช่วงเช้าน้อยกว่า")),
    ("ข้อมูลการเข้าชมเว็บไซต์ขายผ้าทอพบว่าผู้ชมส่วนใหญ่เปิดจากโทรศัพท์ แต่หน้าเว็บแสดงผลบนโทรศัพท์ไม่ดี",
     "ปรับหน้าเว็บให้แสดงผลได้ดีบนโทรศัพท์",
     ("เพิ่มหน้าเว็บสำหรับคอมพิวเตอร์ตั้งโต๊ะ",
      "ลดจำนวนภาพสินค้าในหน้าเว็บลงทั้งหมด",
      "เปลี่ยนชื่อร้านให้จำง่ายขึ้นกว่าเดิม",
      "เลิกขายออนไลน์แล้วขายเฉพาะที่หน้าร้าน",
      "ขึ้นราคาผ้าทอทุกผืนในหน้าเว็บไซต์")),
    ("ข้อมูลรีวิวของร้านอาหารพบว่าลูกค้าชมรสชาติ แต่ร้องเรียนเรื่องส่งอาหารช้ามากที่สุด",
     "ปรับเส้นทางและรอบการส่งอาหารให้เร็วขึ้น",
     ("เปลี่ยนสูตรอาหารทุกจานให้รสชาติดีขึ้น",
      "ปิดระบบรีวิวไม่ให้ลูกค้าร้องเรียนได้อีก",
      "เปลี่ยนโลโก้และบรรจุภัณฑ์ของร้านใหม่",
      "ลดขนาดจานลงเพื่อให้ทำอาหารได้ถูกลง",
      "เลิกใช้บรรจุภัณฑ์ใส่อาหารที่ส่งให้ลูกค้า")),
    ("ข้อมูลการขายของสหกรณ์โรงเรียนพบว่าสินค้าบางชนิดหมดทุกวันก่อนเที่ยง ส่วนบางชนิดขายไม่ออกเลย",
     "ใช้ข้อมูลยอดขายกำหนดปริมาณสินค้าแต่ละชนิดที่จะสั่งเข้าร้าน",
     ("สั่งสินค้าทุกชนิดเข้าร้านในจำนวนเท่ากันทุกวันเพื่อความยุติธรรม",
      "เลิกขายสินค้าที่หมดเร็ว เพราะทำให้นักเรียนที่มาช้าไม่ได้ซื้อ",
      "ขึ้นราคาสินค้าที่ขายไม่ออก เพื่อให้ได้กำไรเท่ากับสินค้าขายดี",
      "หยุดเก็บข้อมูลการขาย แล้วสั่งสินค้าตามที่ผู้ขายคาดเดาเอาเอง",
      "เปิดร้านเฉพาะช่วงบ่าย เพื่อไม่ให้สินค้าขายดีหมดก่อนเที่ยงอีก")),
    ("ข้อมูลจากแอปสอนภาษาพบว่าผู้ใช้จำนวนมากเลิกใช้หลังบทเรียนแรกซึ่งยาวถึง 40 นาที",
     "แบ่งบทเรียนแรกให้สั้นลงเป็นช่วงย่อย",
     ("เพิ่มความยาวบทเรียนแรกให้ละเอียดขึ้น",
      "เก็บค่าบริการตั้งแต่บทเรียนแรกเลย",
      "เปลี่ยนสีและไอคอนของแอปให้สดใส",
      "ปิดการแจ้งเตือนของแอปทั้งหมด",
      "ลบบทเรียนทั้งหมดแล้วเริ่มสร้างใหม่")),
    ("ข้อมูลการจองคิวของร้านตัดผมพบว่ามีลูกค้าจองแล้วไม่มาบ่อย ทำให้เก้าอี้ว่าง",
     "ส่งข้อความเตือนก่อนถึงเวลานัดและให้ยืนยันคิว",
     ("ยกเลิกระบบจองคิวแล้วรับเฉพาะลูกค้าที่เดินมา",
      "ขึ้นราคาทุกบริการเพื่อชดเชยเก้าอี้ที่ว่างอยู่",
      "ลดจำนวนช่างตัดผมลงครึ่งหนึ่งในทุกช่วงเวลา",
      "เปิดร้านดึกขึ้นเพื่อให้มีเวลารับลูกค้ามากขึ้น",
      "ไม่รับลูกค้าที่ไม่ได้จองคิวไว้ล่วงหน้าเลย")),
)


COMPLAINTS = (
    ("แอปสั่งอาหาร", ("ส่งช้า", "อาหารไม่ตรงกับที่สั่ง", "แอปค้าง", "ค่าส่งแพง")),
    ("ร้านขายเสื้อออนไลน์", ("ไซซ์ไม่ตรง", "สีไม่ตรงกับภาพ", "จัดส่งช้า", "ตอบแชตช้า")),
    ("บริการรถรับส่งนักเรียน", ("มาไม่ตรงเวลา", "รถแน่นเกินไป", "แอร์ไม่เย็น", "ติดต่อคนขับยาก")),
)


@question_type(
    "comp.value_add_foundation",
    display_name={"th": "เลือกการปรับปรุงที่ข้อมูลสนับสนุน"},
    level=M5, subject=SUBJECT, topic=VALUE_TOPIC,
)
class ValueAddFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _bank(rng, EVIDENCE, "{} การปรับปรุงใดสอดคล้องกับข้อมูลมากที่สุด",
                     hint="การเพิ่มมูลค่าที่ดีต้องแก้ปัญหาที่ข้อมูลชี้ให้เห็นโดยตรง ไม่ใช่เปลี่ยนสิ่งที่ข้อมูลไม่ได้กล่าวถึง",
                     topic=VALUE_TOPIC)


@question_type(
    "comp.value_add_fluency",
    display_name={"th": "วิเคราะห์ข้อร้องเรียนเพื่อจัดลำดับการปรับปรุง"},
    level=M5, subject=SUBJECT, topic=VALUE_TOPIC,
)
class ValueAddFluency(QuestionType):
    """Complaint counts: the one to fix first, or its share of all complaints."""

    def build(self, rng: Random, **params):
        service, kinds = rng.choice(COMPLAINTS)
        total = rng.choice((50, 100, 200))
        unit = total // 50
        while True:
            cuts = sorted(rng.sample(range(1, 50), 3))
            counts = [(b - a) * unit for a, b in zip([0] + cuts, cuts + [50])]
            if len(set(counts)) == 4:
                break
        table = " ".join(f"{k} {c} ครั้ง" for k, c in zip(kinds, counts))
        lead = f"{service}รวบรวมข้อร้องเรียน {total} ครั้งในเดือนที่ผ่านมา แยกได้ดังนี้ {table}"
        if rng.random() < 0.5:
            worst = kinds[counts.index(max(counts))]
            return _labelled(stem=f"{lead} ถ้าต้องการลดข้อร้องเรียนให้ได้มากที่สุด ควรปรับปรุงเรื่องใดก่อน",
                             correct=worst, wrongs=tuple(k for k in kinds if k != worst),
                             hint="เรื่องที่ถูกร้องเรียนมากที่สุดคือเรื่องที่แก้แล้วลดข้อร้องเรียนได้มากที่สุด",
                             topic=VALUE_TOPIC)
        k = rng.randrange(4)
        percent = counts[k] * 100 // total
        wrongs = _near(percent, (counts[k], 100 - percent, percent + 10))
        return _labelled(stem=f"{lead} ข้อร้องเรียนเรื่อง{kinds[k]}คิดเป็นร้อยละเท่าใดของข้อร้องเรียนทั้งหมด",
                         correct=f"ร้อยละ {percent}",
                         wrongs=tuple(f"ร้อยละ {w}" for w in rng.sample(wrongs[:4], 3)),
                         hint="ร้อยละ = จำนวนข้อร้องเรียนเรื่องนั้น ÷ จำนวนข้อร้องเรียนทั้งหมด × 100",
                         topic=VALUE_TOPIC)


@question_type(
    "comp.value_add_application",
    display_name={"th": "เปรียบเทียบผลการทดลองสองแบบด้วยอัตราส่วน"},
    level=M5, subject=SUBJECT, topic=VALUE_TOPIC,
)
class ValueAddApplication(QuestionType):
    """Two versions of a page shown to different numbers of visitors: compare purchase rates."""

    def build(self, rng: Random, **params):
        while True:
            seen = rng.sample((100, 200, 250, 400, 500), 2)
            rates = rng.sample(range(4, 25), 2)
            bought = [n * r // 100 for n, r in zip(seen, rates)]
            if all(n * r % 100 == 0 for n, r in zip(seen, rates)):
                break
        # The raw counts should point the other way often enough to matter.
        better = 0 if rates[0] > rates[1] else 1
        gap = abs(rates[0] - rates[1])
        names = ("หน้าเว็บแบบ A", "หน้าเว็บแบบ B")

        def say(i: int, points: int) -> str:
            return f"{names[i]} ดีกว่า เพราะมีอัตราการซื้อสูงกว่า {points} จุดร้อยละ"

        correct = say(better, gap)
        more = 0 if bought[0] > bought[1] else 1
        counts_gap = abs(bought[0] - bought[1])
        wrongs = [say(1 - better, gap),
                  f"{names[more]} ดีกว่า เพราะมีจำนวนผู้ซื้อมากกว่า" if more != better
                  else f"{names[1 - more]} ดีกว่า เพราะมีผู้เข้าชมน้อยกว่า",
                  say(better, counts_gap), say(better, gap + 1), say(1 - better, gap + 1)]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != correct][:4]
        return _labelled(
            stem=(f"ร้านค้าออนไลน์ทดลองหน้าเว็บสองแบบ {names[0]} มีผู้เข้าชม {seen[0]} คน ซื้อสินค้า {bought[0]} คน "
                  f"{names[1]} มีผู้เข้าชม {seen[1]} คน ซื้อสินค้า {bought[1]} คน ข้อใดสรุปได้ถูกต้อง"),
            correct=correct, wrongs=tuple(wrongs),
            hint="จำนวนผู้เข้าชมไม่เท่ากัน จึงต้องเทียบอัตราการซื้อ = ผู้ซื้อ ÷ ผู้เข้าชม × 100 ไม่ใช่จำนวนผู้ซื้อ",
            topic=VALUE_TOPIC)

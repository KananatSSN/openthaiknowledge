"""ฮอร์โมนพืช

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/17

Sets moved here from: science_wave_f58.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f58 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HORMONE = "ฮอร์โมนพืช"


HORMONES = {
    "ออกซิน": ("กระตุ้นการยืดตัวของเซลล์ และทำให้เกิดการข่มของตายอด", "ใช้เร่งการเกิดรากของกิ่งปักชำ",
               "ใช้ชักนำให้เกิดผลแบบไม่มีเมล็ด เช่น แตงโม"),
    "ไซโทไคนิน": ("กระตุ้นการแบ่งเซลล์ และชะลอการเสื่อมสภาพของใบ", "ใช้ชักนำให้เกิดยอดในการเพาะเลี้ยงเนื้อเยื่อ",
                  "ใช้ยืดอายุผักและไม้ตัดดอกให้สดนานขึ้น"),
    "จิบเบอเรลลิน": ("กระตุ้นการยืดยาวของลำต้นและการงอกของเมล็ด", "ใช้ทำให้ผลองุ่นไร้เมล็ดมีขนาดใหญ่ขึ้น",
                    "ใช้กระตุ้นการสร้างอะไมเลสในการผลิตมอลต์จากข้าวบาร์เลย์"),
    "เอทิลีน": ("กระตุ้นการสุกของผล และการหลุดร่วงของใบ", "ใช้เร่งให้ผลไม้ดิบสุกพร้อมกัน",
                "ใช้กระตุ้นการออกดอกของสับปะรด"),
    "กรดแอบไซซิก": ("กระตุ้นการปิดปากใบเมื่อขาดน้ำ และทำให้เมล็ดพักตัว", "ช่วยให้พืชทนแล้งโดยลดการคายน้ำ",
                    "ทำให้ตาของไม้ยืนต้นพักตัวในฤดูหนาว"),
}


HORMONE_HINT = ("ออกซินยืดเซลล์ เกิดราก ข่มตาข้าง ไซโทไคนินแบ่งเซลล์ ชะลอการแก่ จิบเบอเรลลินยืดลำต้น แก้การพักตัว "
                "เอทิลีนเร่งผลสุก กรดแอบไซซิกปิดปากใบและทำให้พักตัว")


HORMONE_EXPERIMENTS = (
    ("ตัดยอดของต้นชบาออก ตาข้างที่อยู่ใต้รอยตัดจะเป็นอย่างไร", "เจริญเป็นกิ่ง เพราะไม่มีออกซินจากยอดมาข่มตาข้าง",
     ("หยุดเจริญ เพราะได้รับออกซินมากขึ้น", "ตาข้างตายทั้งหมด เพราะขาดออกซินจากยอด", "ไม่มีการเปลี่ยนแปลงใด ๆ เพราะตาข้างไม่ต้องใช้ออกซิน")),
    ("ตัดยอดแล้วทาออกซินที่รอยตัด ตาข้างจะเป็นอย่างไร", "ยังไม่เจริญ เพราะออกซินที่ทายังข่มตาข้างอยู่",
     ("เจริญเป็นกิ่งอย่างรวดเร็ว เพราะยอดถูกตัดออกไปแล้ว", "เปลี่ยนเป็นดอก เพราะออกซินกระตุ้นการออกดอก", "เปลี่ยนเป็นราก")),
    ("ในการเพาะเลี้ยงเนื้อเยื่อ ถ้าอาหารมีสัดส่วนออกซินสูงกว่าไซโทไคนินมาก แคลลัสมักเจริญเป็นอะไร", "ราก",
     ("ยอด", "ดอก", "ผล")),
    ("ในการเพาะเลี้ยงเนื้อเยื่อ ถ้าอาหารมีสัดส่วนไซโทไคนินสูงกว่าออกซินมาก แคลลัสมักเจริญเป็นอะไร", "ยอด",
     ("ราก", "เมล็ด", "ผล")),
    ("บ่มกล้วยดิบไว้กับกล้วยสุกในถุงปิด กล้วยดิบสุกเร็วขึ้นเพราะเหตุใด", "กล้วยสุกปล่อยแก๊สเอทิลีนกระตุ้นการสุก",
     ("กล้วยสุกปล่อยออกซิเจน", "กล้วยสุกดูดความชื้นออกจากกล้วยดิบ", "กล้วยสุกปล่อยกรดแอบไซซิก")),
    ("ต้นพืชที่วางไว้ริมหน้าต่างโค้งเข้าหาแสงเพราะเหตุใด", "ออกซินเคลื่อนไปด้านที่ไม่ได้รับแสง เซลล์ด้านนั้นจึงยืดยาวกว่า",
     ("ออกซินสะสมด้านที่ได้รับแสงมากกว่า ลำต้นจึงโค้งหนีแสงแทน", "เอทิลีนยับยั้งการยืดตัวของเซลล์ด้านที่ไม่ได้รับแสง", "จิบเบอเรลลินด้านที่ได้รับแสงถูกทำลายจนเซลล์หยุดแบ่ง")),
)


HORMONE_EXPERIMENTS += (
    ('ฉีดพ่นจิบเบอเรลลินให้ต้นถั่วพันธุ์เตี้ย ลำต้นจะเป็นอย่างไร', 'สูงขึ้นจนใกล้เคียงพันธุ์สูง เพราะจิบเบอเรลลินกระตุ้นการยืดตัวของปล้อง',
     ('เตี้ยลงกว่าเดิม เพราะจิบเบอเรลลินยับยั้งการแบ่งเซลล์', 'ไม่เปลี่ยนแปลง เพราะพันธุกรรมกำหนดความสูงไว้ตายตัวเสมอ', 'ใบร่วงหมด เพราะจิบเบอเรลลินเร่งการหลุดร่วงของใบ')),
    ('แช่เมล็ดข้าวในสารละลายจิบเบอเรลลิน เมล็ดจะเป็นอย่างไร', 'งอกได้เร็วขึ้น เพราะจิบเบอเรลลินกระตุ้นการสร้างเอนไซม์ย่อยแป้งในเมล็ด',
     ('พักตัวนานขึ้น เพราะจิบเบอเรลลินยับยั้งการงอกของเมล็ด', 'เน่าเสีย เพราะจิบเบอเรลลินเป็นอาหารของเชื้อราในเมล็ด', 'งอกเป็นรากอย่างเดียว เพราะจิบเบอเรลลินกระตุ้นเฉพาะการเกิดราก')),
    ('เมื่อพืชขาดน้ำ ใบสร้างกรดแอบไซซิกมากขึ้น ผลที่ตามมาคืออะไร', 'ปากใบปิด ช่วยลดการสูญเสียน้ำ',
     ('ปากใบเปิดกว้าง เพื่อดูดน้ำจากอากาศ', 'ใบยืดยาวขึ้นเพื่อหาแหล่งน้ำ', 'รากหยุดเจริญถาวร')),
    ('ฉีดพ่นไซโทไคนินบนใบที่ตัดออกจากต้น ใบจะเป็นอย่างไรเมื่อเทียบกับใบที่ไม่ได้พ่น', 'เหลืองช้ากว่า เพราะไซโทไคนินชะลอการเสื่อมสภาพของใบ',
     ('เหลืองเร็วกว่า เพราะไซโทไคนินเร่งการสลายคลอโรฟิลล์', 'ออกรากทันที เพราะไซโทไคนินกระตุ้นเฉพาะการเกิดราก', 'ไม่ต่างกัน เพราะใบที่ตัดออกแล้วไม่ตอบสนองต่อฮอร์โมนใด')),
)


@question_type(
    "biology.plant_hormone_foundation",
    display_name={"th": "บทบาทหน้าที่ของฮอร์โมนพืช"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class PlantHormoneFoundation(QuestionType):
    """What each of the five hormones does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name = rng.choice(sorted(HORMONES))
        role = HORMONES[name][0]
        others = [h for h in HORMONES if h != name]
        picked = rng.sample(others, 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ฮอร์โมนใด{role}", correct=name, wrongs=tuple(picked), topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        return _labelled(stem=f"{name}มีบทบาทหลักอย่างไร", correct=role, wrongs=tuple(HORMONES[h][0] for h in picked), topic=TOPIC_HORMONE,
                         hint=HORMONE_HINT)


@question_type(
    "biology.plant_hormone_fluency",
    display_name={"th": "การใช้ฮอร์โมนพืชทางการเกษตร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class PlantHormoneFluency(QuestionType):
    """Name the hormone behind a farm practice, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name = rng.choice(sorted(HORMONES))
        use = rng.choice(HORMONES[name][1:])
        others = [h for h in HORMONES if h != name]
        picked = rng.sample(others, 3)
        if rng.random() < 0.55:
            return _labelled(stem=f"การ{use.removeprefix('ใช้')}ใช้ฮอร์โมนพืชชนิดใด" if use.startswith("ใช้") else f"\"{use}\" เป็นผลของฮอร์โมนใด",
                             correct=name, wrongs=tuple(picked), topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        return _labelled(stem=f"ข้อใดเป็นการใช้ประโยชน์หรือผลของ{name}", correct=use,
                         wrongs=tuple(rng.choice(HORMONES[h][1:]) for h in picked), topic=TOPIC_HORMONE, hint=HORMONE_HINT)


@question_type(
    "biology.plant_hormone_application",
    display_name={"th": "อธิบายผลการทดลองเกี่ยวกับฮอร์โมนพืช"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class PlantHormoneApplication(QuestionType):
    """Predict what cutting, painting or bagging does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(HORMONE_EXPERIMENTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HORMONE, hint=HORMONE_HINT)

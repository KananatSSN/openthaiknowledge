"""การสำรวจอวกาศและเทคโนโลยีอวกาศ

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/18

Sets moved here from: science_wave_f86.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f86 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SPACE = "การสำรวจอวกาศและเทคโนโลยีอวกาศ"


TELESCOPES = (
    ("กล้องโทรทรรศน์อวกาศฮับเบิล", "แสงที่ตามองเห็นและอัลตราไวโอเลต"), ("กล้องโทรทรรศน์อวกาศเจมส์ เวบบ์", "อินฟราเรดใกล้และอินฟราเรดกลาง"),
    ("หอดูดาวรังสีเอกซ์จันทรา (Chandra)", "รังสีเอกซ์ (X-ray)"), ("กล้องโทรทรรศน์วิทยุแห่งชาติ เชียงใหม่", "คลื่นวิทยุช่วงความยาวคลื่นเซนติเมตร"),
    ("กล้องโทรทรรศน์แห่งชาติ บนดอยอินทนนท์", "แสงที่ตามองเห็น"),
)


SATELLITES = (
    ("ดาวเทียมไทยโชต (THEOS)", "สำรวจทรัพยากรและถ่ายภาพพื้นผิวโลก"), ("ดาวเทียมฮิมาวาริ", "ติดตามเมฆและสภาพอากาศ"),
    ("ดาวเทียมไทยคม", "สื่อสารและถ่ายทอดสัญญาณโทรทัศน์"), ("ดาวเทียม GPS", "ระบุตำแหน่งบนพื้นโลก"),
    ("สถานีอวกาศนานาชาติ (ISS)", "ห้องปฏิบัติการทดลองในสภาพไร้น้ำหนัก"),
)


SPINOFFS = ("หมอนและที่นอนเมมโมรีโฟม", "เครื่องกรองน้ำแบบพกพา", "เซนเซอร์กล้องในโทรศัพท์มือถือ", "สว่านไร้สาย", "ระบบนำทางด้วย GPS",
            "อาหารแช่เยือกแข็งแบบแห้ง", "เทอร์โมมิเตอร์วัดไข้ทางหู")


NOT_SPINOFFS = ("กังหันลมวิดน้ำ", "เกวียน", "เตาถ่าน", "ครกหิน", "เรือใบ")


SPACE_HINT = ("บรรยากาศโลกดูดกลืนรังสีเอกซ์ อัลตราไวโอเลต และอินฟราเรดส่วนใหญ่ จึงต้องสังเกตจากอวกาศ ส่วนแสงที่ตามองเห็นและคลื่นวิทยุผ่านได้ "
              "ดาวเทียมมีหน้าที่ต่างกัน เช่น สื่อสาร อุตุนิยมวิทยา สำรวจทรัพยากร นำทาง เทคโนโลยีอวกาศหลายอย่างถูกนำมาใช้ในชีวิตประจำวัน")


@question_type(
    "astro.space_telescope_foundation",
    display_name={"th": "กล้องโทรทรรศน์ในช่วงความยาวคลื่นต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPACE,
)
class SpaceTelescopeFoundation(QuestionType):
    """Which band each telescope observes, and why some must go to space."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            facts = (("เหตุใดกล้องโทรทรรศน์รังสีเอกซ์จึงต้องอยู่ในอวกาศ", "บรรยากาศโลกดูดกลืนรังสีเอกซ์เกือบทั้งหมด",
                      ("รังสีเอกซ์เดินทางช้าลงมากในบรรยากาศ", "อวกาศมีแสงสว่างมากกว่าพื้นโลก", "รังสีเอกซ์ถูกสนามแม่เหล็กโลกขยายจนแรงเกินไป", "เมฆบนโลกสะท้อนรังสีเอกซ์กลับออกไปหมด")),
                     ("ข้อดีของกล้องโทรทรรศน์วิทยุบนพื้นโลกคือข้อใด", "คลื่นวิทยุผ่านบรรยากาศและเมฆได้ จึงสังเกตได้ทั้งกลางวันและกลางคืน",
                      ("ให้ภาพสีเหมือนตามองเห็น จึงไม่ต้องแปลงข้อมูลเป็นภาพ", "ใช้ได้เฉพาะคืนเดือนมืดที่ท้องฟ้าโปร่งไม่มีเมฆ", "ต้องตั้งอยู่เหนือเมฆเสมอ จึงต้องสร้างบนยอดเขาสูง", "ไม่ต้องใช้จานรับสัญญาณ")),
                     ("กล้องอินฟราเรดเหมาะศึกษาวัตถุใด", "ดาวฤกษ์เกิดใหม่ที่ถูกฝุ่นบังและกาแล็กซีที่อยู่ไกลมาก",
                      ("ผิวดวงอาทิตย์ในแสงขาวเท่านั้น", "เมฆฝนและพายุฝนฟ้าคะนองบนโลก", "ภูเขาและหลุมบนดวงจันทร์เท่านั้น", "คลื่นแผ่นดินไหวที่เกิดใต้เปลือกโลก")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SPACE, hint=SPACE_HINT)
        name, band = rng.choice(TELESCOPES)
        picked = rng.sample([t for t in TELESCOPES if t[1] != band], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ใช้สังเกตในช่วงคลื่นใดเป็นหลัก", correct=band, wrongs=tuple(p[1] for p in picked),
                             topic=TOPIC_SPACE, hint=SPACE_HINT)
        return _labelled(stem=f"ถ้าต้องการสังเกตวัตถุท้องฟ้าในช่วง{band} ควรใช้ข้อมูลจากกล้องใด", correct=name,
                         wrongs=tuple(p[0] for p in picked), topic=TOPIC_SPACE, hint=SPACE_HINT)


@question_type(
    "astro.space_telescope_fluency",
    display_name={"th": "หน้าที่ของดาวเทียมและการนำเทคโนโลยีอวกาศมาใช้"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPACE,
)
class SpaceTelescopeFluency(QuestionType):
    """Match satellites to jobs; spot the space spin-offs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            name, job = rng.choice(SATELLITES)
            picked = rng.sample([s for s in SATELLITES if s[0] != name], 3)
            if rng.random() < 0.5:
                return _labelled(stem=f"{name}มีหน้าที่หลักอย่างไร", correct=job, wrongs=tuple(p[1] for p in picked), topic=TOPIC_SPACE, hint=SPACE_HINT)
            return _labelled(stem=f"ถ้าต้องการข้อมูลเพื่อ{job} ควรใช้ข้อมูลจากข้อใด", correct=name, wrongs=tuple(p[0] for p in picked),
                             topic=TOPIC_SPACE, hint=SPACE_HINT)
        return _labelled(stem="ข้อใดเป็นผลิตภัณฑ์หรือเทคโนโลยีที่พัฒนาต่อยอดจากเทคโนโลยีอวกาศ", correct=rng.choice(SPINOFFS),
                         wrongs=tuple(NOT_SPINOFFS), topic=TOPIC_SPACE, hint=SPACE_HINT)


@question_type(
    "astro.space_telescope_application",
    display_name={"th": "คำนวณความสามารถรวมแสง เวลาส่งสัญญาณ และรอบการโคจรของดาวเทียม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPACE,
)
class SpaceTelescopeApplication(QuestionType):
    """Light grasp ∝ D²; delay = d / c; orbits per day = 1,440 / period."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            small = rng.choice((Fraction(1, 2), 1, Fraction(6, 5), 2, Fraction(12, 5)))
            k = rng.randint(2, 6)
            big = Fraction(small) * k
            return numeric(stem=f"กล้องโทรทรรศน์ ก มีกระจกเส้นผ่านศูนย์กลาง {show(big)} m กล้อง ข มีกระจก {show(small)} m "
                                f"กล้อง ก รวมแสงได้มากกว่ากล้อง ข กี่เท่า (ความสามารถรวมแสง ∝ D²)", answer=k * k,
                           wrongs=[k, 2 * k, k ** 3], unit="เท่า", topic=TOPIC_SPACE, hint="อัตราส่วน = (D₁ ÷ D₂)²")
        if roll < 0.65:
            dist = rng.choice((36000, 72000, 384000, 3000, 6000, 30000, 150000, 90000))
            delay = Fraction(dist, 300000)
            what = {36000: "ดาวเทียมค้างฟ้าที่ความสูงประมาณ 36,000 km", 72000: "ดาวเทียมค้างฟ้า ไปและกลับรวม 72,000 km",
                    384000: "ดวงจันทร์ที่ห่างประมาณ 384,000 km"}.get(dist, f"ดาวเทียมที่อยู่ห่าง {show(dist)} km")
            if (delay * 100).denominator != 1:
                dist, delay, what = 30000, Fraction(1, 10), "ดาวเทียมที่อยู่ห่าง 30,000 km"
            return numeric(stem=f"สัญญาณวิทยุเดินทางด้วยอัตราเร็ว 300,000 km/s ส่งถึง{what} ใช้เวลากี่วินาที", answer=delay,
                           wrongs=[delay * 2, delay * 10, Fraction(dist, 3000)], unit="s", topic=TOPIC_SPACE, hint="เวลา = ระยะทาง ÷ อัตราเร็วแสง")
        period = rng.choice((90, 96, 80, 120, 144, 160, 180, 240, 288, 360, 480, 720, 1440))
        return numeric(stem=f"ดาวเทียมดวงหนึ่งโคจรรอบโลกรอบละ {period} นาที ในหนึ่งวัน (1,440 นาที) จะโคจรได้กี่รอบ", answer=Fraction(1440, period),
                       wrongs=[Fraction(1440, period) * 2, Fraction(period, 60), Fraction(1440, period) + 1], unit="รอบ", topic=TOPIC_SPACE,
                       hint="จำนวนรอบ = 1,440 ÷ คาบ (นาที)")

"""คลื่นแม่เหล็กไฟฟ้า ส่วนประกอบ และหลักการทำงานของอุปกรณ์

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/11

Sets moved here from: science_wave_e15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import show
from otk.sets._support.science_wave_e15 import SUBJECT, UPPER_FIVE, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_EM_WAVE = "คลื่นแม่เหล็กไฟฟ้า ส่วนประกอบ และหลักการทำงานของอุปกรณ์"


C_LIGHT = 3 * 10 ** 8


EM_TRUE = (
    "คลื่นแม่เหล็กไฟฟ้าประกอบด้วยสนามไฟฟ้าและสนามแม่เหล็กที่เปลี่ยนแปลงและตั้งฉากกัน",
    "สนามไฟฟ้าและสนามแม่เหล็กของคลื่นแม่เหล็กไฟฟ้าตั้งฉากกับทิศการเคลื่อนที่ของคลื่น จึงเป็นคลื่นตามขวาง",
    "คลื่นแม่เหล็กไฟฟ้าทุกความถี่เคลื่อนที่ในสุญญากาศด้วยอัตราเร็วเท่ากัน คือ 3 × 10⁸ m/s",
    "คลื่นแม่เหล็กไฟฟ้าเคลื่อนที่ผ่านสุญญากาศได้ ไม่ต้องอาศัยตัวกลาง",
    "คลื่นแม่เหล็กไฟฟ้าเกิดจากประจุไฟฟ้าที่มีความเร่ง เช่น อิเล็กตรอนที่สั่นไปมาในสายอากาศ",
    "คลื่นที่มีความถี่สูงกว่ามีความยาวคลื่นสั้นกว่าและมีพลังงานสูงกว่า",
)


EM_FALSE = (
    "คลื่นแม่เหล็กไฟฟ้าต้องอาศัยอากาศเป็นตัวกลางในการเคลื่อนที่",
    "สนามไฟฟ้าและสนามแม่เหล็กของคลื่นแม่เหล็กไฟฟ้าขนานกับทิศการเคลื่อนที่",
    "รังสีเอกซ์เคลื่อนที่ในสุญญากาศเร็วกว่าคลื่นวิทยุ",
    "คลื่นแม่เหล็กไฟฟ้าเป็นคลื่นตามยาวเหมือนคลื่นเสียง",
    "คลื่นที่มีความถี่สูงกว่ามีความยาวคลื่นยาวกว่า",
    "คลื่นแม่เหล็กไฟฟ้าประกอบด้วยสนามไฟฟ้าเพียงอย่างเดียว",
)


DEVICES = (
    ("เตาไมโครเวฟ", "ไมโครเวฟ", "คลื่นไมโครเวฟทำให้โมเลกุลน้ำในอาหารสั่นจนอาหารร้อน"),
    ("รีโมตคอนโทรลโทรทัศน์", "รังสีอินฟราเรด", "ส่งสัญญาณเป็นจังหวะของรังสีอินฟราเรดไปยังตัวรับที่โทรทัศน์"),
    ("กล้องถ่ายภาพความร้อน", "รังสีอินฟราเรด", "ตรวจรับรังสีอินฟราเรดที่วัตถุร้อนแผ่ออกมา แล้วแสดงเป็นภาพ"),
    ("เครื่องถ่ายภาพเอกซเรย์", "รังสีเอกซ์", "รังสีเอกซ์ทะลุผ่านเนื้อเยื่ออ่อนได้มากกว่ากระดูก จึงเกิดภาพเงาของกระดูก"),
    ("หลอดฆ่าเชื้อโรค", "รังสีอัลตราไวโอเลต", "รังสีอัลตราไวโอเลตทำลายสารพันธุกรรมของจุลินทรีย์"),
    ("เรดาร์ตรวจจับอากาศยาน", "ไมโครเวฟ", "ส่งคลื่นไมโครเวฟไปกระทบวัตถุแล้วรับคลื่นสะท้อนกลับมาเพื่อหาตำแหน่ง"),
    ("เครื่องรับวิทยุ", "คลื่นวิทยุ", "สายอากาศรับคลื่นวิทยุแล้วแปลงสัญญาณเป็นเสียง"),
    ("เครื่องฉายรังสีรักษามะเร็ง", "รังสีแกมมา", "รังสีแกมมาพลังงานสูงทำลายเซลล์มะเร็ง"),
)


BANDS = ("คลื่นวิทยุ", "ไมโครเวฟ", "รังสีอินฟราเรด", "แสง", "รังสีอัลตราไวโอเลต", "รังสีเอกซ์", "รังสีแกมมา")


@question_type(
    "phys.em_wave_foundation",
    display_name={"th": "ส่วนประกอบและสมบัติของคลื่นแม่เหล็กไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_WAVE,
)
class EmWaveFoundation(QuestionType):
    """The wave's make-up: one true statement among wrong ones, or which band a device uses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _labelled(
                stem="ข้อใดกล่าวถึงคลื่นแม่เหล็กไฟฟ้าได้ถูกต้อง",
                correct=rng.choice(EM_TRUE), wrongs=tuple(EM_FALSE),
                topic=TOPIC_EM_WAVE,
                hint="คลื่นแม่เหล็กไฟฟ้าคือสนามไฟฟ้าและสนามแม่เหล็กที่ตั้งฉากกันและตั้งฉากกับทิศการเคลื่อนที่ เคลื่อนที่ในสุญญากาศได้ด้วยอัตราเร็วแสง")
        device, band, _ = rng.choice(DEVICES)
        return _labelled(
            stem=f"{device}อาศัยคลื่นแม่เหล็กไฟฟ้าช่วงใด",
            correct=band, wrongs=tuple([b for b in BANDS if b != band]),
            topic=TOPIC_EM_WAVE,
            hint="นึกถึงสิ่งที่อุปกรณ์ทำ: ทำให้น้ำร้อน รับความร้อน ทะลุร่างกาย ฆ่าเชื้อ หรือส่งสัญญาณระยะไกล")


@question_type(
    "phys.em_wave_fluency",
    display_name={"th": "อธิบายหลักการทำงานของอุปกรณ์ที่อาศัยคลื่นแม่เหล็กไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_WAVE,
)
class EmWaveFluency(QuestionType):
    """The indicator: how devices use their band."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        device, _, how = rng.choice(DEVICES)
        return _labelled(
            stem=f"ข้อใดอธิบายหลักการทำงานของ{device}ได้ถูกต้อง",
            correct=how, wrongs=tuple([h for d, _, h in DEVICES if d != device]),
            topic=TOPIC_EM_WAVE,
            hint="แต่ละช่วงคลื่นมีสมบัติต่างกัน: ไมโครเวฟทำให้น้ำสั่น อินฟราเรดคือรังสีความร้อน เอกซ์ทะลุเนื้อเยื่ออ่อน อัลตราไวโอเลตทำลายเชื้อ")


@question_type(
    "phys.em_wave_application",
    display_name={"th": "คำนวณความยาวคลื่นและความถี่ของคลื่นแม่เหล็กไฟฟ้าจาก c = fλ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_WAVE,
)
class EmWaveApplication(QuestionType):
    """c = fλ with real stations and ovens, both ways."""

    SOURCES = (
        # Frequencies whose wavelength is exact, so the reverse question is too.
        ("สถานีวิทยุ FM", "เมกะเฮิรตซ์", 10 ** 6, (75, 100, 120, 150)),
        ("สถานีวิทยุ AM", "กิโลเฮิรตซ์", 10 ** 3, (500, 600, 750, 1000, 1500)),
        ("เตาไมโครเวฟ", "กิกะเฮิรตซ์", 10 ** 9, (1, 2, 3, 5, 6)),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, unit, scale, values = rng.choice(self.SOURCES)
        f = rng.choice(values)
        wavelength = Fraction(C_LIGHT, f * scale)
        if rng.random() < 0.6:
            return _numeric(
                stem=(f"{name}ส่งคลื่นความถี่ {f:,} {unit} คลื่นนี้มีความยาวคลื่นเท่าใด "
                      "(อัตราเร็วแสง 3 × 10⁸ m/s)"),
                answer=wavelength, wrongs=[wavelength * 10, wavelength / 10, Fraction(f * scale, C_LIGHT)],
                unit="เมตร", topic=TOPIC_EM_WAVE,
                hint="λ = c ÷ f และแปลงหน่วยความถี่เป็นเฮิรตซ์ก่อน (เมกะ = 10⁶ กิโล = 10³ กิกะ = 10⁹)")
        return _numeric(
            stem=(f"คลื่นจาก{name}มีความยาวคลื่น {show(wavelength)} เมตร มีความถี่กี่{unit} "
                  "(อัตราเร็วแสง 3 × 10⁸ m/s)"),
            answer=f, wrongs=[f * 10, Fraction(f, 10), f * 3],
            unit=unit, topic=TOPIC_EM_WAVE,
            hint="f = c ÷ λ แล้วแปลงเฮิรตซ์เป็นหน่วยที่โจทย์ถาม")

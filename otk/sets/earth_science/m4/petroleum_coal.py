"""การเกิดและการสำรวจปิโตรเลียมและถ่านหิน

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/10

Sets moved here from: science_wave_f77.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f77 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_FORM = "การเกิดและการสำรวจปิโตรเลียมและถ่านหิน"


ROLES = (
    ("หินต้นกำเนิด (source rock)", "หินดินดานที่มีซากสิ่งมีชีวิตสะสม ถูกความร้อนและความดันจนเกิดปิโตรเลียม"),
    ("หินกักเก็บ (reservoir rock)", "หินที่มีรูพรุนและซึมผ่านได้ เช่น หินทราย ให้ปิโตรเลียมสะสมอยู่"),
    ("หินปิดกั้น (cap rock)", "หินเนื้อแน่นที่ของไหลซึมผ่านไม่ได้ เช่น หินดินดาน กั้นไม่ให้ปิโตรเลียมเล็ดลอด"),
    ("โครงสร้างรูปประทุนหงาย (anticline)", "ชั้นหินโค้งขึ้นเป็นรูปโดม ปิโตรเลียมสะสมที่ส่วนยอด"),
    ("โครงสร้างรอยเลื่อน (fault trap)", "ชั้นหินเลื่อนจนหินกักเก็บไปชนกับหินที่ซึมผ่านไม่ได้"),
)


COAL_RANKS = ("พีต", "ลิกไนต์", "ซับบิทูมินัส", "บิทูมินัส", "แอนทราไซต์")


FORM_HINT = ("ปิโตรเลียมเกิดจากซากสิ่งมีชีวิตในทะเลถูกฝังและได้รับความร้อนความดันนานนับล้านปี สะสมในหินกักเก็บใต้หินปิดกั้น "
             "ถ่านหินเกิดจากซากพืชในที่ลุ่มชื้นแฉะ ยิ่งถูกกดทับนาน ปริมาณคาร์บอนและค่าความร้อนยิ่งสูง: พีต → ลิกไนต์ → ซับบิทูมินัส → บิทูมินัส → แอนทราไซต์")


@question_type(
    "geo.petroleum_coal_foundation",
    display_name={"th": "การเกิดและแหล่งกักเก็บปิโตรเลียม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORM,
)
class PetroleumCoalFoundation(QuestionType):
    """Source, reservoir and cap rock, and traps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            facts = (("ปิโตรเลียมเกิดจากอะไร", "ซากสิ่งมีชีวิตขนาดเล็กในทะเลที่ถูกฝังและได้รับความร้อนและความดันเป็นเวลานาน",
                      ("ลาวาจากภูเขาไฟที่เย็นตัวลงใต้พื้นทะเลเป็นเวลานาน", "ซากไดโนเสาร์บนบกที่ถูกฝังอยู่ใต้ทะเลทราย", "น้ำทะเลที่ระเหยจนเหลือแต่ตะกอนเกลือ", "แร่เหล็กที่ผุพัง")),
                     ("ถ่านหินเกิดจากอะไร", "ซากพืชในแอ่งที่ลุ่มชื้นแฉะถูกทับถมและอัดแน่นเป็นเวลานาน",
                      ("ซากแพลงก์ตอนในทะเลลึกที่ถูกทับถมภายใต้ความดันสูง", "หินปูนที่ถูกความร้อนจากหินหนืดเผาจนกลายเป็นสีดำ", "น้ำมันดิบที่ซึมขึ้นมาแล้วแข็งตัวบนผิวดิน", "ลาวาที่เย็นตัว")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FORM, hint=FORM_HINT)
        name, role = rng.choice(ROLES)
        others = rng.sample([r for r in ROLES if r[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ในระบบปิโตรเลียมมีลักษณะหรือหน้าที่อย่างไร", correct=role, wrongs=tuple(r[1] for r in others),
                             topic=TOPIC_FORM, hint=FORM_HINT)
        return _labelled(stem=f"\"{role}\" คืออะไร", correct=name, wrongs=tuple(r[0] for r in others), topic=TOPIC_FORM, hint=FORM_HINT)


@question_type(
    "geo.petroleum_coal_fluency",
    display_name={"th": "ลำดับชั้นถ่านหินและการสำรวจแหล่งพลังงาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORM,
)
class PetroleumCoalFluency(QuestionType):
    """Coal ranks in order, and survey methods."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            a, b = sorted(rng.sample(range(len(COAL_RANKS)), 2))
            more = rng.random() < 0.5
            right = COAL_RANKS[b] if more else COAL_RANKS[a]
            return _labelled(stem=f"ระหว่าง{COAL_RANKS[a]}กับ{COAL_RANKS[b]} ชนิดใดมีปริมาณคาร์บอนและค่าความร้อน{'สูงกว่า' if more else 'ต่ำกว่า'}",
                             correct=right, wrongs=(COAL_RANKS[a] if more else COAL_RANKS[b], "เท่ากัน", "เปรียบเทียบไม่ได้"),
                             topic=TOPIC_FORM, hint=FORM_HINT)
        if roll < 0.7:
            chunk = [COAL_RANKS[i] for i in sorted(rng.sample(range(len(COAL_RANKS)), 4))]
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                c = chunk[:]
                rng.shuffle(c)
                if c != chunk:
                    wrongs[" → ".join(c)] = None
            return _labelled(stem="ข้อใดเรียงถ่านหินจากคาร์บอนน้อยไปมากได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs), topic=TOPIC_FORM,
                             hint=FORM_HINT)
        facts = (("การสำรวจคลื่นไหวสะเทือนแบบสะท้อนใช้ทำอะไรในการหาแหล่งปิโตรเลียม", "หาตำแหน่งและรูปร่างของชั้นหินและโครงสร้างกักเก็บใต้ดิน",
                  ("วัดปริมาณน้ำมันในถังโดยตรง", "ตรวจหาแร่ทองคำบนผิวดิน", "พยากรณ์อากาศ", "วัดความเค็มของน้ำทะเล")),
                 ("แหล่งถ่านหินลิกไนต์ขนาดใหญ่ของไทยอยู่ที่ใด", "อำเภอแม่เมาะ จังหวัดลำปาง", ("อ่าวไทยตอนกลาง", "เกาะภูเก็ต", "จังหวัดชลบุรี", "ยอดดอยอินทนนท์")),
                 ("แหล่งก๊าซธรรมชาติสำคัญของไทยอยู่ที่ใด", "ใต้พื้นทะเลอ่าวไทย", ("อำเภอแม่เมาะ", "ภูเขาหินปูนภาคใต้", "ที่ราบสูงโคราช", "ทะเลสาบสงขลา")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FORM, hint=FORM_HINT)


@question_type(
    "geo.petroleum_coal_application",
    display_name={"th": "คำนวณความลึกของชั้นหินจากการสำรวจคลื่นไหวสะเทือน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORM,
)
class PetroleumCoalApplication(QuestionType):
    """The wave goes down and back, so depth is half of speed × time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        speed = rng.choice((2000, 2500, 3000, 3500, 4000))
        time = Fraction(rng.randrange(2, 41), 10)
        depth = speed * time / 2
        if rng.random() < 0.6:
            return numeric(stem=f"คลื่นไหวสะเทือนเคลื่อนที่ในชั้นหินด้วยอัตราเร็วเฉลี่ย {speed:,} m/s สะท้อนจากชั้นหินกลับมาถึงผิวดินในเวลา {show(time)} วินาที "
                                f"ชั้นหินนั้นอยู่ลึกกี่เมตร", answer=depth, wrongs=[depth * 2, depth / 2, speed * time * 10], unit="m", topic=TOPIC_FORM,
                           hint="คลื่นเดินทางไปและกลับ ความลึก = อัตราเร็ว × เวลา ÷ 2")
        return numeric(stem=f"ชั้นหินกักเก็บอยู่ลึก {show(depth)} m ถ้าคลื่นไหวสะเทือนเคลื่อนที่ด้วยอัตราเร็ว {speed:,} m/s คลื่นที่สะท้อนกลับจะมาถึงผิวดินในเวลากี่วินาที",
                       answer=time, wrongs=[time / 2, time * 2, time + 1], unit="วินาที", topic=TOPIC_FORM,
                       hint="เวลาไปกลับ = 2 × ความลึก ÷ อัตราเร็ว")

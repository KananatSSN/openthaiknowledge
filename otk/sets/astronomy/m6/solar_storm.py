"""โครงสร้างดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/12

Sets moved here from: science_wave_f84.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f84 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_STORM = "โครงสร้างดวงอาทิตย์ ลมสุริยะ และพายุสุริยะ"


SUN_LAYERS = ("แกน", "เขตการแผ่รังสี", "เขตการพาความร้อน", "โฟโตสเฟียร์", "โครโมสเฟียร์", "คอโรนา")


SUN_FEATURES = (
    ("จุดมืดดวงอาทิตย์", "บริเวณบนโฟโตสเฟียร์ที่อุณหภูมิต่ำกว่ารอบข้าง เกิดจากสนามแม่เหล็กเข้มข้น"),
    ("พวยแก๊ส (prominence)", "แก๊สร้อนพุ่งเป็นวงโค้งตามเส้นสนามแม่เหล็กเหนือผิวดวงอาทิตย์"),
    ("การลุกจ้า (flare)", "การปลดปล่อยพลังงานอย่างรุนแรงในเวลาสั้น ๆ ทำให้บริเวณนั้นสว่างจ้าขึ้นทันที"),
    ("การพ่นมวลคอโรนา (CME)", "การพ่นก้อนพลาสมาปริมาณมหาศาลจากคอโรนาออกสู่อวกาศ"),
    ("ลมสุริยะ", "กระแสอนุภาคมีประจุที่ไหลออกจากคอโรนาอย่างต่อเนื่อง"),
)


STORM_EFFECTS = (
    ("แสงเหนือแสงใต้บริเวณขั้วโลก", True), ("การสื่อสารทางวิทยุคลื่นสั้นขัดข้อง", True),
    ("ดาวเทียมและระบบ GPS ทำงานผิดพลาด", True), ("ระบบสายส่งไฟฟ้าแรงสูงเสียหาย", True), ("นักบินอวกาศได้รับรังสีมากขึ้น", True),
    ("เกิดแผ่นดินไหวรุนแรงหลายแห่ง", False), ("น้ำทะเลขึ้นสูงผิดปกติทั่วโลก", False), ("เกิดพายุไต้ฝุ่นในเขตร้อน", False),
    ("ภูเขาไฟระเบิดพร้อมกันหลายลูก", False),
)


STORM_HINT = ("ดวงอาทิตย์: แกน → เขตการแผ่รังสี → เขตการพาความร้อน → โฟโตสเฟียร์ → โครโมสเฟียร์ → คอโรนา "
              "ลมสุริยะและพายุสุริยะ (การลุกจ้า CME) ทำให้เกิดออโรรา รบกวนวิทยุ ดาวเทียม GPS และระบบไฟฟ้า "
              "จำนวนจุดมืดเปลี่ยนตามวัฏจักรสุริยะประมาณ 11 ปี")


@question_type(
    "astro.solar_storm_foundation",
    display_name={"th": "โครงสร้างดวงอาทิตย์และปรากฏการณ์บนดวงอาทิตย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STORM,
)
class SolarStormFoundation(QuestionType):
    """Layers in order, and sunspots, prominences, flares, CMEs, solar wind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            i = rng.randrange(len(SUN_LAYERS) - 1)
            outward = rng.random() < 0.5 or i == 0
            if outward:
                right, stem = SUN_LAYERS[i + 1], f"ชั้นที่อยู่ถัดออกมาจาก{SUN_LAYERS[i]}ของดวงอาทิตย์คือชั้นใด"
            else:
                right, stem = SUN_LAYERS[i - 1], f"ชั้นที่อยู่ถัดเข้าไปด้านในจาก{SUN_LAYERS[i]}ของดวงอาทิตย์คือชั้นใด"
            pool = [x for x in SUN_LAYERS if x not in (right, SUN_LAYERS[i])]
            return _labelled(stem=stem, correct=right, wrongs=tuple(pool), topic=TOPIC_STORM, hint=STORM_HINT)
        name, what = rng.choice(SUN_FEATURES)
        others = [f for f in SUN_FEATURES if f[0] != name]
        picked = rng.sample(others, 3)
        if roll < 0.65:
            return _labelled(stem=f"{name} คืออะไร", correct=what, wrongs=tuple(p[1] for p in picked), topic=TOPIC_STORM, hint=STORM_HINT)
        return _labelled(stem=f"ปรากฏการณ์ใดคือ{what}", correct=name, wrongs=tuple(p[0] for p in picked), topic=TOPIC_STORM, hint=STORM_HINT)


@question_type(
    "astro.solar_storm_fluency",
    display_name={"th": "ผลของลมสุริยะและพายุสุริยะต่อโลกและประเทศไทย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STORM,
)
class SolarStormFluency(QuestionType):
    """What storms do and do not do; Thailand's case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            is_effect = rng.random() < 0.5
            right = rng.choice([e for e, y in STORM_EFFECTS if y == is_effect])
            wrongs = rng.sample([e for e, y in STORM_EFFECTS if y != is_effect], 3)
            return _labelled(stem=f"ข้อใด{'เป็น' if is_effect else 'ไม่ได้เป็น'}ผลจากพายุสุริยะ", correct=right, wrongs=tuple(wrongs),
                             topic=TOPIC_STORM, hint=STORM_HINT)
        cases = (("เหตุใดคนในประเทศไทยจึงแทบไม่เห็นแสงเหนือแสงใต้ แม้เกิดพายุสุริยะรุนแรง", "ประเทศไทยอยู่ใกล้เส้นศูนย์สูตร อนุภาคถูกสนามแม่เหล็กนำไปลงที่บริเวณขั้วโลก",
                  ("ประเทศไทยไม่ได้รับลมสุริยะเลย", "ประเทศไทยมีเมฆมากตลอดปี", "แสงเหนือเกิดเฉพาะเวลากลางวัน", "ประเทศไทยอยู่ใกล้ขั้วโลกเกินไป")),
                 ("ช่วงพายุสุริยะรุนแรง ผู้ใช้ระบบ GPS ในประเทศไทยอาจพบปัญหาใด", "ตำแหน่งคลาดเคลื่อนเพราะชั้นไอโอโนสเฟียร์ถูกรบกวน",
                  ("GPS แม่นยำขึ้นเป็นพิเศษ เพราะมีอนุภาคช่วยส่งสัญญาณ", "โทรศัพท์ร้อนจนระเบิดเพราะรับรังสีโดยตรง", "แผนที่ในเครื่องถูกลบเพราะคลื่นแม่เหล็ก", "ไม่มีผลใดเลย")),
                 ("เหตุใดหน่วยงานดาวเทียมจึงติดตามจำนวนจุดมืดบนดวงอาทิตย์", "ช่วงที่จุดมืดมากมักเกิดการลุกจ้าและ CME บ่อย ซึ่งอาจทำให้ดาวเทียมเสียหาย",
                  ("จุดมืดทำให้ดวงอาทิตย์ดับ", "จุดมืดบอกเวลาเกิดสุริยุปราคา", "จุดมืดทำให้โลกหยุดหมุน", "จุดมืดบอกตำแหน่งดาวเหนือ")),
                 ("สนามแม่เหล็กโลกช่วยป้องกันพายุสุริยะอย่างไร", "เบี่ยงเบนอนุภาคมีประจุไม่ให้พุ่งตรงสู่ผิวโลก",
                  ("ดูดกลืนแสงอาทิตย์และอนุภาคทั้งหมดไม่ให้ถึงผิวโลก", "ทำให้ลมสุริยะเย็นลงจนหยุดก่อนถึงโลก", "สะท้อนแสงเหนือกลับสู่อวกาศ", "ทำให้ดวงอาทิตย์หยุดพ่นมวลออกมาทางโลก")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_STORM, hint=STORM_HINT)


@question_type(
    "astro.solar_storm_application",
    display_name={"th": "คำนวณเวลาที่ลมสุริยะเดินทางถึงโลกและวัฏจักรจุดมืด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STORM,
)
class SolarStormApplication(QuestionType):
    """Travel time over 150 million km; the 11-year cycle; spot temperature gap."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            speed = rng.choice((400, 500, 600, 750, 800, 1000, 1200, 1250, 1500, 2000, 2500, 3000))
            seconds = Fraction(150_000_000, speed)
            what = rng.choice(("ลมสุริยะ", "ก้อนพลาสมาจาก CME"))
            if rng.random() < 0.5 and (seconds / 60 * 100).denominator == 1:
                return numeric(stem=f"{what} เคลื่อนที่ด้วยอัตราเร็ว {show(speed)} km/s ระยะจากดวงอาทิตย์ถึงโลก 150,000,000 km ใช้เวลากี่นาทีจึงถึงโลก",
                               answer=seconds / 60, wrongs=[seconds, seconds / 3600 * 100 if (seconds / 36).denominator == 1 else seconds / 30, seconds / 60 + 60],
                               unit="นาที", topic=TOPIC_STORM, hint="เวลา (s) = ระยะทาง ÷ อัตราเร็ว แล้วหาร 60 เป็นนาที")
            return numeric(stem=f"{what} เคลื่อนที่ด้วยอัตราเร็ว {show(speed)} km/s ระยะจากดวงอาทิตย์ถึงโลก 150,000,000 km ใช้เวลากี่วินาทีจึงถึงโลก",
                           answer=seconds, wrongs=[seconds * 10, seconds / 10, seconds * 2], unit="s", topic=TOPIC_STORM,
                           hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
        if roll < 0.7:
            year = rng.choice((2001, 2014, 2025))
            cycles = rng.randint(1, 5)
            if rng.random() < 0.5:
                # Years are labels, not quantities: no thousands separator.
                right = year + 11 * cycles
                return _labelled(stem=f"จุดมืดบนดวงอาทิตย์มีจำนวนมากที่สุดในปี ค.ศ. {year} ถ้าวัฏจักรสุริยะยาวประมาณ 11 ปี "
                                      f"ช่วงจุดมืดมากที่สุดครั้งที่ {cycles} ถัดจากนั้นจะเป็นปี ค.ศ. ใด", correct=f"ค.ศ. {right}",
                                 wrongs=(f"ค.ศ. {right + 11}", f"ค.ศ. {year + 10 * cycles}", f"ค.ศ. {year + cycles}"),
                                 topic=TOPIC_STORM, hint="ปีที่จุดมืดมาก = ปีเดิม + 11 × จำนวนรอบ")
            gap = 11 * cycles
            return numeric(stem=f"ช่วงจุดมืดมากที่สุดของดวงอาทิตย์เกิดในปี ค.ศ. {year - gap} และ ค.ศ. {year} ถ้าวัฏจักรหนึ่งยาว 11 ปี "
                                f"ระหว่างสองปีนี้ผ่านไปกี่วัฏจักร", answer=cycles, wrongs=[gap, cycles + 1, cycles * 2 if cycles > 1 else 3], unit="วัฏจักร",
                           topic=TOPIC_STORM, hint="จำนวนวัฏจักร = จำนวนปี ÷ 11")
        photo = rng.randrange(5500, 6001, 100)
        spot = photo - rng.randrange(1200, 2201, 100)
        return numeric(stem=f"โฟโตสเฟียร์บริเวณหนึ่งมีอุณหภูมิ {show(photo)} K จุดมืดที่อยู่ใกล้กันมีอุณหภูมิ {show(spot)} K จุดมืดเย็นกว่ากี่ K",
                       answer=photo - spot, wrongs=[photo + spot, spot, photo - spot + 1000], unit="K", topic=TOPIC_STORM,
                       hint="ผลต่าง = อุณหภูมิโฟโตสเฟียร์ − อุณหภูมิจุดมืด")

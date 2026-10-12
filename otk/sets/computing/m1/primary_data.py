"""ข้อมูลปฐมภูมิและการประมวลผลเพื่อตัดสินใจ

วิทยาการคำนวณ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.1/3

Sets moved here from: technology_t3s6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t1s6 import _pick_one
from otk.sets._support.technology_t3s6 import M1

PROVENANCE = Provenance("original")


PRIMARY_TOPIC = "ข้อมูลปฐมภูมิและการประมวลผลเพื่อตัดสินใจ"


PRIMARY = (
    "จำนวนนักเรียนที่นั่งรถโดยสารมาโรงเรียน ซึ่งนักเรียนสำรวจเองที่หน้าประตูโรงเรียน",
    "อุณหภูมิของน้ำในบ่อที่นักเรียนวัดด้วยเทอร์โมมิเตอร์ทุกเช้า",
    "คำตอบจากแบบสอบถามที่นักเรียนแจกให้เพื่อนในห้อง",
    "จำนวนรถที่ผ่านหน้าโรงเรียนในหนึ่งชั่วโมง ซึ่งนักเรียนนับเอง",
    "คำให้สัมภาษณ์ของเกษตรกรที่นักเรียนไปพูดคุยด้วยตนเอง",
    "ความสูงของต้นถั่วที่นักเรียนปลูกและวัดเองทุกวัน",
)


SECONDARY = (
    "จำนวนประชากรของจังหวัดจากเว็บไซต์ของหน่วยงานรัฐ",
    "ปริมาณน้ำฝนย้อนหลังสิบปีจากรายงานของกรมอุตุนิยมวิทยา",
    "ผลสำรวจการอ่านของคนไทยที่ตีพิมพ์ในหนังสือพิมพ์",
    "สถิติผู้ป่วยไข้เลือดออกจากรายงานประจำปีของกระทรวงสาธารณสุข",
    "ข้อมูลราคาข้าวย้อนหลังจากบทความในวารสาร",
    "ตารางคะแนนเฉลี่ยระดับประเทศที่ดาวน์โหลดจากอินเทอร์เน็ต",
)


MEASURES = (
    ("ชั่วโมงการนอนต่อคืนของเพื่อน 5 คน", "ชั่วโมง", 5, 10),
    ("เวลาที่ใช้เดินทางมาโรงเรียนของเพื่อน 5 คน", "นาที", 5, 40),
    ("จำนวนหนังสือที่เพื่อน 5 คนอ่านในเดือนนี้", "เล่ม", 1, 12),
    ("อุณหภูมิที่วัดได้ตอนเที่ยงวัน 5 วัน", "องศาเซลเซียส", 26, 36),
    ("มวลของขยะพลาสติกที่ห้องเรียน 5 ห้องเก็บได้", "กิโลกรัม", 2, 15),
)


CHOICES = (
    ("เลือกกิจกรรมทัศนศึกษาของห้อง", ("พิพิธภัณฑ์", "สวนสัตว์", "ฟาร์มเกษตร", "ท้องฟ้าจำลอง"),
     ("ความรู้ที่ได้", "ค่าใช้จ่ายที่ประหยัด", "ความปลอดภัย")),
    ("เลือกขนมที่จะขายในงานโรงเรียน", ("ขนมครก", "กล้วยทอด", "ข้าวเกรียบ", "บัวลอย"),
     ("ความนิยมของผู้ซื้อ", "กำไรต่อชิ้น", "ความง่ายในการทำ")),
    ("เลือกวิธีลดขยะในโรงอาหาร", ("แยกขยะ", "ใช้กล่องซ้ำ", "งดหลอดพลาสติก", "ทำปุ๋ยหมัก"),
     ("ลดขยะได้มาก", "ค่าใช้จ่ายน้อย", "ทำได้ทันที")),
    ("เลือกแอปจดการบ้าน", ("แอป A", "แอป B", "แอป C", "แอป D"),
     ("ใช้งานง่าย", "ฟรี", "เตือนความจำได้")),
)


@question_type(
    "comp.primary_data_foundation",
    display_name={"th": "แยกข้อมูลปฐมภูมิกับข้อมูลทุติยภูมิ"},
    level=M1, subject=SUBJECT, topic=PRIMARY_TOPIC,
)
class PrimaryDataFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _pick_one(rng, good=PRIMARY, bad=SECONDARY,
                         good_stem="ข้อใดเป็นข้อมูลปฐมภูมิ",
                         bad_stem="ข้อใดเป็นข้อมูลทุติยภูมิ",
                         hint="ข้อมูลปฐมภูมิคือข้อมูลที่ผู้ใช้เก็บรวบรวมเองจากแหล่งโดยตรง เช่น สังเกต วัด สัมภาษณ์ "
                              "ข้อมูลทุติยภูมิคือข้อมูลที่ผู้อื่นเก็บและเผยแพร่ไว้แล้ว",
                         topic=PRIMARY_TOPIC)


@question_type(
    "comp.primary_data_fluency",
    display_name={"th": "ประมวลผลข้อมูลที่เก็บรวบรวมด้วยค่าเฉลี่ยและพิสัย"},
    level=M1, subject=SUBJECT, topic=PRIMARY_TOPIC,
)
class PrimaryDataFluency(QuestionType):
    """Five collected values: their mean (always whole) or their range."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        what, unit, low, high = rng.choice(MEASURES)
        while True:
            values = [rng.randint(low, high) for _ in range(5)]
            if sum(values) % 5 == 0 and len(set(values)) >= 3:
                break
        listed = " ".join(str(v) for v in values)
        lead = f"นักเรียนเก็บข้อมูล{what} ได้ดังนี้ {listed} {unit}"
        if rng.random() < 0.5:
            mean = sum(values) // 5
            wrongs = _near(mean, (sum(values), sorted(values)[2], max(values) - min(values)))
            return _labelled(stem=f"{lead} ค่าเฉลี่ยของข้อมูลชุดนี้เท่ากับเท่าใด", correct=f"{mean} {unit}",
                             wrongs=tuple(f"{w} {unit}" for w in rng.sample(wrongs[:4], 3)),
                             hint="ค่าเฉลี่ย = ผลรวมของข้อมูลทั้งหมด ÷ จำนวนข้อมูล", topic=PRIMARY_TOPIC)
        spread = max(values) - min(values)
        wrongs = _near(spread, (max(values), min(values), max(values) + min(values)))
        return _labelled(stem=f"{lead} ข้อมูลชุดนี้มีพิสัย (ค่ามากที่สุดลบค่าน้อยที่สุด) เท่าใด",
                         correct=f"{spread} {unit}",
                         wrongs=tuple(f"{w} {unit}" for w in rng.sample(wrongs[:4], 3)),
                         hint="พิสัย = ค่ามากที่สุด − ค่าน้อยที่สุด", topic=PRIMARY_TOPIC)


@question_type(
    "comp.primary_data_application",
    display_name={"th": "ประเมินทางเลือกด้วยตารางคะแนน"},
    level=M1, subject=SUBJECT, topic=PRIMARY_TOPIC,
)
class PrimaryDataApplication(QuestionType):
    """Three alternatives scored 1-5 on three criteria; the highest total wins."""

    def build(self, rng: Random, **params):
        goal, options, criteria = rng.choice(CHOICES)
        picked = rng.sample(options, 3)
        while True:
            scores = [[rng.randint(1, 5) for _ in criteria] for _ in picked]
            totals = [sum(s) for s in scores]
            best = max(totals)
            # One clear winner, and no tie anywhere to argue over.
            if totals.count(best) == 1 and len(set(totals)) == 3:
                break
        winner = picked[totals.index(best)]
        table = " ".join(
            f"{name} ได้ " + " ".join(f"{c} {v}" for c, v in zip(criteria, s)) + " คะแนน;"
            for name, s in zip(picked, scores))
        leftover = next(o for o in options if o not in picked)
        return _labelled(
            stem=(f"นักเรียนต้องการ{goal} จึงให้คะแนนแต่ละทางเลือกตามเกณฑ์ 3 ข้อ ข้อละ 1 ถึง 5 คะแนน "
                  f"ดังนี้ {table.rstrip(';')} ถ้าเลือกทางเลือกที่ได้คะแนนรวมมากที่สุด ควรเลือกข้อใด"),
            correct=winner,
            wrongs=tuple([o for o in picked if o != winner] + [leftover]),
            hint="รวมคะแนนทุกเกณฑ์ของแต่ละทางเลือก แล้วเปรียบเทียบคะแนนรวม ทางเลือกที่ไม่ได้ประเมินเลือกไม่ได้",
            topic=PRIMARY_TOPIC)

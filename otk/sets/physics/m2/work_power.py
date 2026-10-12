"""การคำนวณงานและกำลังโดยใช้สมการ W = Fs และ P = W/t

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.2/1

Sets moved here from: science_wave_d30.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d30 import SECOND_SECONDARY, _facts

PROVENANCE = Provenance("original")


WORK_POWER_TOPIC = "การคำนวณงานและกำลังโดยใช้สมการ W = Fs และ P = W/t"


WORK_CASES = ("ยกกล่องจากพื้นขึ้นไปวางบนโต๊ะ", "ผลักรถเข็นให้เคลื่อนที่ไปข้างหน้า", "ดึงถังน้ำขึ้นจากบ่อ", "เข็นตู้ให้เลื่อนไปตามพื้น",
              "ลากกระเป๋าเดินทางไปตามพื้นในทิศทางที่ดึง", "ยกดัมเบลจากระดับอกขึ้นเหนือศีรษะ", "ดันประตูบานเลื่อนให้เปิดออก",
              "ดึงเชือกรอกยกธงขึ้นสู่ยอดเสา", "เตะลูกฟุตบอลให้พุ่งออกไป")


NO_WORK_CASES = ("ผลักกำแพงเต็มแรงแต่กำแพงไม่ขยับ", "ถือกระเป๋ายืนนิ่งรอรถโดยสาร", "ยกดัมเบลค้างไว้เหนือศีรษะนิ่ง ๆ",
                 "ออกแรงดันรถยนต์ที่ดึงเบรกมือไว้แต่รถไม่ขยับ", "หนังสือวางนิ่งอยู่บนโต๊ะ", "แบกถุงข้าวยืนรอคิวอยู่กับที่",
                 "ดึงเชือกชักเย่อที่สองฝ่ายออกแรงเท่ากันจนเชือกไม่ขยับ")


WORK_FACTS = (
    ("แรงที่กระทำต่อวัตถุกรณีใดถือว่าเกิดงาน (work) ตามหลักฟิสิกส์",
     "แรงที่กระทำทำให้วัตถุเคลื่อนที่ไปในทิศทางของแรง (หรือมีองค์ประกอบในทิศทางนั้น)",
     ("แรงที่กระทำโดยวัตถุไม่เคลื่อนที่เลย เช่น ผลักกำแพงที่ไม่ขยับ", "แรงโน้มถ่วงที่กระทำต่อวัตถุที่วางนิ่งอยู่บนพื้นเสมอ",
      "การออกแรงใด ๆ ก็ตาม ไม่ว่าวัตถุจะเคลื่อนที่หรือไม่", "การที่ผู้ออกแรงรู้สึกเหนื่อย", "แรงที่ตั้งฉากกับทิศการเคลื่อนที่เสมอ")),
    ("งานมีหน่วยเป็นอะไร", "จูล (J) ซึ่งเท่ากับนิวตัน × เมตร",
     ("วัตต์ (W)", "นิวตัน (N)", "เมตรต่อวินาที", "กิโลกรัม", "จูลต่อวินาที")),
    ("กำลัง (power) หมายถึงอะไร", "งานที่ทำได้ในหนึ่งหน่วยเวลา มีหน่วยเป็นวัตต์หรือจูลต่อวินาที",
     ("แรงที่ใช้ในหนึ่งหน่วยเวลา", "ระยะทางที่วัตถุเคลื่อนที่ได้", "งานทั้งหมดโดยไม่เกี่ยวกับเวลา", "มวลของผู้ออกแรง", "พลังงานที่สะสมในวัตถุ")),
    ("ถ้าออกแรงเท่าเดิมแต่วัตถุเคลื่อนที่ได้ระยะทางเป็นสองเท่า งานที่ทำจะเป็นอย่างไร", "เพิ่มเป็นสองเท่า เพราะ W = Fs",
     ("ลดลงครึ่งหนึ่ง", "เท่าเดิม", "เพิ่มเป็นสี่เท่า", "เป็นศูนย์", "ขึ้นกับเวลาที่ใช้เท่านั้น")),
)


WORK_HINT = "งานเกิดขึ้นเมื่อมีทั้งแรงกระทำและการเคลื่อนที่ไปในทิศทางของแรงนั้น W = Fs และกำลัง P = W/t"


WORK_POWER_COMBOS = (
    (20, 8, 5, 32),
    (80, 3, 4, 60),
    (20, 2, 10, 4),
    (40, 2, 10, 8),
    (20, 6, 8, 15),
    (60, 5, 10, 30),
    (60, 2, 8, 15),
    (60, 3, 10, 18),
)


def _power_combo(rng: Random) -> tuple[int, int, int, int | float]:
    """An authored row, or a fresh force, distance and time giving a whole or half watt."""
    if rng.random() < 0.2:
        return rng.choice(WORK_POWER_COMBOS)
    while True:
        force = rng.choice((10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120, 150, 200))
        distance = rng.randint(2, 15)
        time = rng.randint(2, 20)
        power = Fraction(force * distance, time)
        options = {power, force * distance, force * time, distance * time}
        if (power * 2).denominator == 1 and len(options) == 4:
            return force, distance, time, float(power) if power.denominator != 1 else int(power)


WORK_POWER_SCENARIOS = (
    ("คนสองคนยกกล่องน้ำหนักเท่ากันขึ้นไปที่ความสูงเท่ากัน คนแรกใช้เวลา 5 วินาที คนที่สองใช้เวลา 10 วินาที ใครมีกำลังมากกว่า และเพราะเหตุใด",
     "คนแรกมีกำลังมากกว่า เพราะทำงานเท่ากันในเวลาที่น้อยกว่า",
     ("คนที่สองมีกำลังมากกว่า เพราะใช้เวลานานกว่า", "ทั้งสองคนมีกำลังเท่ากันเพราะทำงานเท่ากัน", "กำลังไม่เกี่ยวข้องกับเวลาที่ใช้ในการทำงาน")),
    ("มอเตอร์ตัวหนึ่งยกวัตถุหนักเท่ากับมอเตอร์อีกตัวขึ้นไปสูงเท่ากัน แต่มอเตอร์ตัวแรกใช้เวลาน้อยกว่า ข้อใดสรุปได้ถูกต้อง",
     "มอเตอร์ตัวแรกมีกำลังมากกว่า เพราะทำงานเท่ากันในเวลาที่สั้นกว่า",
     ("มอเตอร์ทั้งสองตัวมีกำลังเท่ากันเสมอถ้างานเท่ากัน", "มอเตอร์ตัวที่ใช้เวลานานกว่ามีกำลังมากกว่า", "งานที่ทำได้ไม่เกี่ยวข้องกับกำลังของมอเตอร์เลย")),
    ("นักเรียนวิ่งขึ้นบันไดชุดเดียวกันสองครั้ง ครั้งแรกวิ่งเร็วใช้เวลา 10 วินาที ครั้งที่สองเดินช้าใช้เวลา 30 วินาที งานและกำลังในการวิ่งขึ้นบันไดทั้งสองครั้งเป็นอย่างไร",
     "งานที่ทำเท่ากันทั้งสองครั้งเพราะยกน้ำหนักตัวขึ้นความสูงเท่ากัน แต่กำลังครั้งแรกมากกว่าเพราะใช้เวลาน้อยกว่า",
     ("งานครั้งแรกมากกว่าเพราะวิ่งเร็วกว่า", "กำลังทั้งสองครั้งเท่ากันเพราะขึ้นบันไดชุดเดียวกัน", "งานและกำลังไม่มีความสัมพันธ์กับเวลาที่ใช้เลย")),
)


PEOPLE = ("นิด", "ต้น", "มายด์", "บอส", "ฟ้า", "เจ", "ปราง", "ภูมิ")


@question_type(
    "phys.work_power_foundation",
    display_name={"th": "วิเคราะห์ว่าแรงที่กระทำต่อวัตถุเกิดงานหรือไม่"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=WORK_POWER_TOPIC,
)
class WorkPowerFoundation(QuestionType):
    """Work is done only when a force causes motion along the force's direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem="สถานการณ์ใดเกิดงานตามหลักฟิสิกส์", correct=rng.choice(WORK_CASES),
                             wrongs=tuple(NO_WORK_CASES), hint=WORK_HINT, topic=WORK_POWER_TOPIC)
        if roll < 0.7:
            return _labelled(stem="สถานการณ์ใดไม่เกิดงานตามหลักฟิสิกส์", correct=rng.choice(NO_WORK_CASES),
                             wrongs=tuple(WORK_CASES), hint=WORK_HINT, topic=WORK_POWER_TOPIC)
        return _facts(rng, WORK_FACTS, hint=WORK_HINT, topic=WORK_POWER_TOPIC)


@question_type(
    "phys.work_power_fluency",
    display_name={"th": "คำนวณกำลังโดยใช้สมการ W = Fs และ P = W/t จากข้อมูลที่รวบรวมได้"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=WORK_POWER_TOPIC,
)
class WorkPowerFluency(QuestionType):
    """Compute power from a stated force, distance, and time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        force, distance, time, power = _power_combo(rng)
        return _labelled(
            stem=(f"แรง {force} นิวตัน กระทำต่อวัตถุจนเคลื่อนที่ไปทางเดียวกับแรงเป็นระยะทาง {distance} เมตร ในเวลา {time} วินาที "
                  "กำลังที่ใช้มีค่าเท่าใด (ใช้ W = Fs และ P = W/t)"),
            correct=f"{power:g} วัตต์",
            wrongs=(f"{force * distance:g} วัตต์", f"{force * time:g} วัตต์", f"{distance * time:g} วัตต์"),
            hint="หางาน W = Fs ก่อน แล้วหากำลัง P = W/t",
            topic=WORK_POWER_TOPIC,
        )


@question_type(
    "phys.work_power_application",
    display_name={"th": "เปรียบเทียบกำลังจากงานและเวลาที่ใช้ในสถานการณ์จริง"},
    level=SECOND_SECONDARY, subject=SUBJECT, topic=WORK_POWER_TOPIC,
)
class WorkPowerApplication(QuestionType):
    """Authored comparisons, two climbers with their own numbers, and a lift's work and power."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            return _retopic(scenario_question(
                rng, WORK_POWER_SCENARIOS,
                hint="กำลังคืองานที่ทำได้ในหนึ่งหน่วยเวลา งานเท่ากันแต่ใช้เวลาน้อยกว่าหมายถึงกำลังมากกว่า",
            ), WORK_POWER_TOPIC)
        if roll < 0.6:
            a, b = rng.sample(PEOPLE, 2)
            while True:
                wa, wb = rng.choice((400, 450, 500, 550, 600)), rng.choice((400, 450, 500, 550, 600))
                h = rng.choice((3, 4, 5, 6, 8, 10))
                ta, tb = rng.randint(4, 20), rng.randint(4, 20)
                pa, pb = Fraction(wa * h, ta), Fraction(wb * h, tb)
                if pa != pb:
                    break
            right = a if pa > pb else b
            return _labelled(stem=f"{a} น้ำหนัก {wa} นิวตัน วิ่งขึ้นบันไดสูง {h} เมตรในเวลา {ta} วินาที ส่วน{b} น้ำหนัก {wb} นิวตัน "
                                  f"วิ่งขึ้นบันไดเดียวกันในเวลา {tb} วินาที ใครมีกำลังมากกว่า",
                             correct=f"{right} เพราะทำงานต่อหนึ่งหน่วยเวลาได้มากกว่า",
                             wrongs=(f"{b if right == a else a} เพราะทำงานต่อหนึ่งหน่วยเวลาได้มากกว่า", "มีกำลังเท่ากันเพราะขึ้นบันไดเดียวกัน",
                                     f"{b if right == a else a} เพราะใช้เวลานานกว่า"),
                             hint="คำนวณกำลังของแต่ละคน P = (น้ำหนัก × ความสูง) ÷ เวลา แล้วเปรียบเทียบ", topic=WORK_POWER_TOPIC)
        weight = rng.choice((500, 800, 1000, 1200, 1500, 2000))
        height = rng.choice((3, 5, 6, 10, 12, 15, 20))
        time = rng.choice((2, 4, 5, 8, 10, 12, 15, 20, 25, 30))
        work = weight * height
        if rng.random() < 0.5 or (Fraction(work, time) * 100).denominator != 1:
            return numeric(stem=f"ลิฟต์ขนของยกสินค้าหนัก {show(weight)} นิวตัน ขึ้นไปสูง {height} เมตร ด้วยอัตราเร็วคงตัว ลิฟต์ทำงานกี่จูล",
                           answer=work, wrongs=[weight + height, Fraction(work, 10), work * 2], unit="จูล", topic=WORK_POWER_TOPIC,
                           hint="W = F × s โดยแรงเท่ากับน้ำหนักของสินค้า")
        return numeric(stem=f"ลิฟต์ขนของยกสินค้าหนัก {show(weight)} นิวตัน ขึ้นไปสูง {height} เมตร ในเวลา {time} วินาที ลิฟต์มีกำลังกี่วัตต์",
                       answer=Fraction(work, time), wrongs=[work, Fraction(weight, time), Fraction(work, time) * 2], unit="วัตต์",
                       topic=WORK_POWER_TOPIC, hint="หางาน W = Fs แล้วหากำลัง P = W/t")

"""หลักฐานสนับสนุนทฤษฎีบิกแบง

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/2

Sets moved here from: science_wave_f82.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f82 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_HUBBLE = "หลักฐานสนับสนุนทฤษฎีบิกแบง"


HUBBLE_FACTS = (
    ("ฮับเบิลพบความสัมพันธ์ใดระหว่างกาแล็กซีกับระยะทาง", "กาแล็กซียิ่งไกลยิ่งเคลื่อนที่ออกห่างจากเราเร็วขึ้น",
     ("กาแล็กซียิ่งไกลยิ่งเคลื่อนเข้าหาเราเร็วขึ้น", "กาแล็กซียิ่งไกลยิ่งเคลื่อนที่ออกห่างจากเราช้าลง", "กาแล็กซียิ่งใกล้ยิ่งเคลื่อนออกเร็วขึ้น", "กาแล็กซีทุกแห่งเคลื่อนที่ออกห่างจากเราด้วยความเร็วเท่ากัน")),
    ("การเลื่อนไปทางแดงของสเปกตรัมกาแล็กซีแสดงว่าอะไร", "กาแล็กซีกำลังเคลื่อนที่ออกห่างจากผู้สังเกต",
     ("กาแล็กซีกำลังเคลื่อนเข้าหาผู้สังเกต", "กาแล็กซีมีอุณหภูมิต่ำมาก แสงจึงเปลี่ยนเป็นสีแดง", "กาแล็กซีหยุดนิ่งอยู่กับที่เมื่อเทียบกับผู้สังเกต", "กาแล็กซีประกอบด้วยเหล็กเป็นส่วนใหญ่")),
    ("ไมโครเวฟพื้นหลังของเอกภพถูกค้นพบโดยใครและเมื่อใด", "เพนเซียสและวิลสัน ปี ค.ศ. 1965",
     ("ฮับเบิล ปี ค.ศ. 1929", "ไอน์สไตน์ ปี ค.ศ. 1905", "อัลเบิร์ต ไอน์สไตน์ ปี ค.ศ. 1915", "เอ็ดวิน ฮับเบิล ปี ค.ศ. 1929")),
    ("ไมโครเวฟพื้นหลังของเอกภพในปัจจุบันมีอุณหภูมิประมาณเท่าใด", "ประมาณ 2.7 K",
     ("ประมาณ 3,000 K", "ประมาณ 273 K", "ประมาณ 5,800 K", "ประมาณ 15 ล้าน K")),
    ("เหตุใดไมโครเวฟพื้นหลังจึงเป็นหลักฐานสนับสนุนทฤษฎีบิกแบง", "เป็นรังสีที่หลงเหลือจากเอกภพยุคแรกที่ร้อน ซึ่งเย็นลงเมื่อเอกภพขยายตัว",
     ("เป็นรังสีจากดวงอาทิตย์ที่สะท้อนจากดวงจันทร์", "เป็นคลื่นวิทยุจากเครื่องส่งบนโลกที่สะท้อนกลับจากชั้นบรรยากาศทุกทิศ", "เป็นรังสีจากแกนโลกที่ร้อน ซึ่งแผ่ออกมาในทุกทิศทางอย่างสม่ำเสมอ", "เป็นแสงจากดาวฤกษ์ใกล้เคียงที่ถูกฝุ่นในกาแล็กซีกระเจิงจนสม่ำเสมอ")),
    ("ไมโครเวฟพื้นหลังมีลักษณะการกระจายอย่างไร", "มาจากทุกทิศทางเกือบเท่ากัน",
     ("มาจากทิศของดวงอาทิตย์เท่านั้น", "มาจากใจกลางทางช้างเผือกเท่านั้น", "มาเฉพาะเวลากลางคืน", "มาจากดวงจันทร์")),
    ("ค่าคงที่ฮับเบิลใช้ประมาณค่าใดของเอกภพได้", "อายุของเอกภพ เพราะ 1/H₀ ใกล้เคียงเวลาที่เอกภพขยายตัวมา",
     ("มวลรวมของเอกภพ เพราะ 1/H₀ บอกปริมาณสสารทั้งหมดที่มีอยู่", "ระยะทางถึงขอบเอกภพ เพราะ 1/H₀ มีหน่วยเป็นปีแสงโดยตรง", "ระยะทางจากโลกถึงดวงจันทร์", "จำนวนดาวเคราะห์ในระบบสุริยะ")),
    ("ทำไมไมโครเวฟพื้นหลังซึ่งเดิมเป็นรังสีจากแก๊สร้อนหลายพันเคลวินจึงอยู่ในช่วงคลื่นไมโครเวฟในปัจจุบัน", "เอกภพขยายตัว ความยาวคลื่นจึงยืดออกและอุณหภูมิลดลง",
     ("รังสีถูกดูดกลืนโดยบรรยากาศโลกจนเหลือเพียงไมโครเวฟ", "ดาวฤกษ์ปล่อยไมโครเวฟออกมาเพิ่ม", "เอกภพหดตัว ความยาวคลื่นจึงสั้นลงและอุณหภูมิลดลง", "สนามแม่เหล็กโลกเปลี่ยนความยาวคลื่น")),
)


HUBBLE_HINT = ("กฎของฮับเบิล v = H₀ × d กาแล็กซีที่ไกลกว่าเคลื่อนออกเร็วกว่า สเปกตรัมเลื่อนไปทางแดง แสดงว่าเอกภพขยายตัว "
               "ไมโครเวฟพื้นหลังอุณหภูมิประมาณ 2.7 K มาจากทุกทิศ เป็นรังสีหลงเหลือจากเอกภพยุคแรก")


@question_type(
    "astro.hubble_law_foundation",
    display_name={"th": "หลักฐานการขยายตัวของเอกภพและไมโครเวฟพื้นหลัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HUBBLE,
)
class HubbleLawFoundation(QuestionType):
    """Redshift, Hubble's discovery, the CMB."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(HUBBLE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HUBBLE, hint=HUBBLE_HINT)


@question_type(
    "astro.hubble_law_fluency",
    display_name={"th": "เปรียบเทียบการเคลื่อนที่ของกาแล็กซีจากระยะทางและการเลื่อนของสเปกตรัม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HUBBLE,
)
class HubbleLawFluency(QuestionType):
    """Farther recedes faster; bigger redshift, faster recession."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        names = ("กาแล็กซี ก", "กาแล็กซี ข", "กาแล็กซี ค", "กาแล็กซี ง")
        if rng.random() < 0.5:
            dists = rng.sample(range(20, 801, 10), 4)
            fastest = rng.random() < 0.5
            pick = dists.index(max(dists) if fastest else min(dists))
            table = " ".join(f"{n} ห่าง {d} ล้านพาร์เซก" for n, d in zip(names, dists))
            return _labelled(stem=f"{table} กาแล็กซีใดเคลื่อนที่ออกห่างจากเรา{'เร็วที่สุด' if fastest else 'ช้าที่สุด'}", correct=names[pick],
                             wrongs=tuple(n for n in names if n != names[pick]), topic=TOPIC_HUBBLE, hint=HUBBLE_HINT)
        shifts = rng.sample(range(2, 60), 4)
        farthest = rng.random() < 0.5
        pick = shifts.index(max(shifts) if farthest else min(shifts))
        table = " ".join(f"{n} เส้นสเปกตรัมเลื่อนไปทางแดง {s} nm" for n, s in zip(names, shifts))
        return _labelled(stem=f"เส้นสเปกตรัมเดียวกันจากกาแล็กซีต่าง ๆ: {table} กาแล็กซีใดน่าจะอยู่{'ไกล' if farthest else 'ใกล้'}ที่สุด",
                         correct=names[pick], wrongs=tuple(n for n in names if n != names[pick]), topic=TOPIC_HUBBLE,
                         hint=HUBBLE_HINT + " เลื่อนไปทางแดงมาก เคลื่อนออกเร็ว จึงอยู่ไกล")


@question_type(
    "astro.hubble_law_application",
    display_name={"th": "คำนวณด้วยกฎของฮับเบิลและการเลื่อนไปทางแดง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HUBBLE,
)
class HubbleLawApplication(QuestionType):
    """v = H0 d, d = v / H0, and v = c Δλ / λ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        h0 = rng.choice((70, 72, 68))
        roll = rng.random()
        if roll < 0.35:
            d = rng.randrange(10, 501, 10)
            return numeric(stem=f"กาแล็กซีหนึ่งอยู่ห่าง {d} ล้านพาร์เซก (Mpc) ถ้าค่าคงที่ฮับเบิลเป็น {h0} km/s ต่อ Mpc กาแล็กซีเคลื่อนที่ออกห่างด้วยอัตราเร็วกี่ km/s",
                           answer=h0 * d, wrongs=[h0 + d, Fraction(d, h0) * 1000 if (Fraction(d, h0) * 100000).denominator == 1 else h0 * d * 2, h0 * d + 1000],
                           unit="km/s", topic=TOPIC_HUBBLE, hint="v = H₀ × d")
        if roll < 0.7:
            d = rng.randrange(10, 501, 10)
            return numeric(stem=f"กาแล็กซีหนึ่งเคลื่อนที่ออกห่างด้วยอัตราเร็ว {show(h0 * d)} km/s ถ้าค่าคงที่ฮับเบิลเป็น {h0} km/s ต่อ Mpc กาแล็กซีอยู่ห่างกี่ Mpc",
                           answer=d, wrongs=[d * 2, d + h0, Fraction(d, 10)], unit="Mpc", topic=TOPIC_HUBBLE, hint="d = v ÷ H₀")
        rest = rng.choice((400, 500, 600, 656, 486))
        shift = rng.choice((1, 2, 4, 5, 8, 10, 20))
        v = Fraction(300000 * shift, rest)
        while (v * 100).denominator != 1:
            rest = rng.choice((400, 500, 600))
            v = Fraction(300000 * shift, rest)
        return numeric(stem=f"เส้นสเปกตรัมที่ความยาวคลื่นปกติ {rest} nm จากกาแล็กซีหนึ่งวัดได้ {rest + shift} nm "
                            f"(v = c × Δλ ÷ λ, c = 300,000 km/s) กาแล็กซีเคลื่อนที่ออกห่างด้วยอัตราเร็วกี่ km/s",
                       answer=v, wrongs=[Fraction(300000 * shift, rest + shift) if (Fraction(300000 * shift, rest + shift) * 100).denominator == 1 else v * 2,
                                         300000 * shift, v * 10], unit="km/s", topic=TOPIC_HUBBLE, hint="Δλ = ความยาวคลื่นที่วัดได้ − ความยาวคลื่นปกติ")

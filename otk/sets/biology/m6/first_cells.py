"""การเกิดเซลล์เริ่มแรกและวิวัฒนาการของสิ่งมีชีวิตเซลล์เดียว

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.6/2

Sets moved here from: science_wave_f53.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f53 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ORIGIN = "การเกิดเซลล์เริ่มแรกและวิวัฒนาการของสิ่งมีชีวิตเซลล์เดียว"


ORIGIN_FACTS = (
    ("บรรยากาศของโลกยุคแรกเริ่มแตกต่างจากปัจจุบันอย่างไร", "แทบไม่มีแก๊สออกซิเจนอิสระ",
     ("มีแก๊สออกซิเจนมากกว่าปัจจุบัน", "มีแก๊สโอโซนหนาแน่น", "ประกอบด้วยไนโตรเจนและออกซิเจนเหมือนปัจจุบัน", "ไม่มีไอน้ำเลย")),
    ("การทดลองของมิลเลอร์และยูเรย์แสดงผลอะไร", "สารอินทรีย์ เช่น กรดอะมิโน เกิดจากแก๊สในบรรยากาศยุคแรกได้เมื่อได้รับพลังงาน",
     ("สิ่งมีชีวิตเกิดขึ้นเองจากสิ่งไม่มีชีวิตได้ทันทีโดยไม่ต้องใช้พลังงานใด ๆ", "DNA เป็นสารพันธุกรรมของสิ่งมีชีวิตทุกชนิด", "เซลล์ทุกเซลล์เกิดจากเซลล์เดิม จึงไม่มีสารอินทรีย์เกิดขึ้นใหม่ได้",
      "ออกซิเจนจำเป็นต่อการเกิดสารอินทรีย์")),
    ("เหตุใดนักวิทยาศาสตร์จึงเสนอว่า RNA อาจเป็นสารพันธุกรรมแรกเริ่ม", "RNA บางชนิดเก็บข้อมูลพันธุกรรมและเร่งปฏิกิริยาได้ด้วยตัวเอง",
     ("RNA มีสายคู่ที่เสถียรกว่า DNA", "RNA พบเฉพาะในเซลล์ยูแคริโอตที่เกิดขึ้นก่อนโพรแคริโอต", "RNA สร้างพลังงานให้เซลล์โดยไม่ต้องใช้ไมโทคอนเดรียเลย", "RNA ไม่ต้องใช้นิวคลีโอไทด์ จึงสร้างขึ้นเองได้ง่ายที่สุด")),
    ("เซลล์แรกเริ่มน่าจะมีลักษณะใด", "เซลล์โพรแคริโอตที่ดำรงชีวิตได้โดยไม่ใช้ออกซิเจน",
     ("เซลล์ยูแคริโอตที่มีไมโทคอนเดรียและใช้ออกซิเจน", "เซลล์พืชที่มีคลอโรพลาสต์และสังเคราะห์ด้วยแสง", "สิ่งมีชีวิตหลายเซลล์ที่มีเนื้อเยื่อ")),
    ("แก๊สออกซิเจนในบรรยากาศเพิ่มขึ้นครั้งแรกเพราะสิ่งมีชีวิตกลุ่มใด", "ไซยาโนแบคทีเรียที่สังเคราะห์ด้วยแสง",
     ("ฟังไจที่ย่อยสลายซากสิ่งมีชีวิต", "สัตว์ที่หายใจด้วยเหงือกในทะเลยุคแรก", "พืชดอกที่ขึ้นบนบกยุคแรก", "แบคทีเรียที่ไม่ใช้ออกซิเจน")),
    ("โพรโทเซลล์ (protocell) ที่เสนอว่าเป็นจุดเริ่มต้นของเซลล์คืออะไร", "หยดสารอินทรีย์ที่มีเยื่อลิพิดล้อมรอบและเกิดปฏิกิริยาเคมีภายในได้",
     ("เซลล์แบคทีเรียที่สมบูรณ์", "ไวรัสที่มีสารพันธุกรรมเป็น DNA และมีเยื่อหุ้มแบบเซลล์", "ผลึกเกลือในทะเลที่เติบโตขึ้นเองได้", "ออร์แกเนลล์ที่หลุดออกจากเซลล์ยูแคริโอตแล้วแบ่งตัวเองได้ในทะเล")),
    ("โอพารินและฮาลเดนเสนอแนวคิดเกี่ยวกับการเกิดสิ่งมีชีวิตอย่างไร", "สารอินทรีย์เกิดจากสารอนินทรีย์ในบรรยากาศยุคแรก แล้วสะสมในทะเลจนรวมตัวเป็นโครงสร้างคล้ายเซลล์",
     ("สิ่งมีชีวิตมาจากนอกโลกเท่านั้น", "สิ่งมีชีวิตถูกสร้างขึ้นพร้อมกันทุกชนิดในทะเลยุคแรกโดยไม่ผ่านการเกิดสารอินทรีย์ก่อน", "เซลล์แรกเป็นเซลล์ยูแคริโอตหลายเซลล์",
      "สารอินทรีย์เกิดได้เฉพาะในสิ่งมีชีวิต เซลล์แรกจึงต้องมาจากสิ่งมีชีวิตที่มีอยู่ก่อนแล้ว")),
    ("หินสโตรมาโทไลต์เป็นหลักฐานของอะไร", "ชั้นของไซยาโนแบคทีเรียที่สะสมมาตั้งแต่อดีตกาลอันยาวนาน",
     ("ซากไดโนเสาร์", "ลาวาจากภูเขาไฟยุคใหม่ที่เย็นตัวเป็นชั้น", "ปะการังที่เพิ่งตายในทะเลปัจจุบัน", "รอยเท้าสัตว์เลื้อยคลานยุคไดโนเสาร์ที่ประทับบนหินทราย")),
)


ENDO_EVIDENCE = ("ไมโทคอนเดรียและคลอโรพลาสต์มี DNA เป็นของตนเองซึ่งเป็นวงกลมคล้ายของแบคทีเรีย",
                 "ไมโทคอนเดรียและคลอโรพลาสต์มีเยื่อหุ้มสองชั้น",
                 "ไมโทคอนเดรียและคลอโรพลาสต์มีไรโบโซมขนาดเล็กคล้ายของแบคทีเรีย",
                 "ไมโทคอนเดรียและคลอโรพลาสต์เพิ่มจำนวนด้วยการแบ่งตัวคล้ายแบคทีเรีย")


NOT_ENDO = ("ไมโทคอนเดรียพบได้ทั้งในเซลล์พืชและเซลล์สัตว์", "นิวเคลียสมีเยื่อหุ้มที่มีรูพรุน", "ไรโบโซมพบบนร่างแหเอนโดพลาซึมแบบขรุขระ",
            "แวคิวโอลของเซลล์พืชมีขนาดใหญ่", "ผนังเซลล์พืชประกอบด้วยเซลลูโลส")


ORIGIN_HINT = ("โลกยุคแรกไม่มี O₂ อิสระ สารอินทรีย์เกิดจากพลังงานในบรรยากาศ เซลล์แรกเป็นโพรแคริโอตที่ไม่ใช้ O₂ "
               "ไซยาโนแบคทีเรียปล่อย O₂ ยูแคริโอตเกิดจากการอยู่ร่วมภายในเซลล์ของแบคทีเรีย")


ENDO_FACTS = (
    ("ตามทฤษฎีเอนโดซิมไบโอซิส ไมโทคอนเดรียมีต้นกำเนิดจากอะไร", "แบคทีเรียที่ใช้ออกซิเจน",
     ("ไซยาโนแบคทีเรีย", "นิวเคลียสที่แยกตัวออกมา", "ไวรัส", "เยื่อหุ้มเซลล์ที่พับเข้าไป")),
    ("ตามทฤษฎีเอนโดซิมไบโอซิส คลอโรพลาสต์มีต้นกำเนิดจากอะไร", "ไซยาโนแบคทีเรีย",
     ("แบคทีเรียที่ใช้ออกซิเจน", "ไมโทคอนเดรียที่เปลี่ยนรูป", "ไวรัส", "ฟังไจเซลล์เดียว")),
)


EVENTS = (("โลกเกิดขึ้น", 4600), ("เซลล์โพรแคริโอตแรกเริ่มปรากฏ", 3500), ("ไซยาโนแบคทีเรียเริ่มสร้างหินสโตรมาโทไลต์", 3400),
          ("แก๊สออกซิเจนเริ่มสะสมในบรรยากาศ", 2400), ("เซลล์ยูแคริโอตแรกเริ่มปรากฏ", 1800), ("สิ่งมีชีวิตหลายเซลล์ปรากฏ", 1200),
          ("สัตว์หลากหลายชนิดเกิดขึ้นในยุคแคมเบรียน", 540), ("ไดโนเสาร์สูญพันธุ์", 66))


SCALES = (("เชือกยาว 46 เมตร", "เมตร", 100), ("เชือกยาว 460 เซนติเมตร", "เซนติเมตร", 10), ("นาฬิกา 46 ชั่วโมง", "ชั่วโมง", 100),
          ("ทางเดินยาว 4,600 เมตร", "เมตร", 1))


@question_type(
    "biology.first_cells_foundation",
    display_name={"th": "สภาพโลกยุคแรกและการเกิดเซลล์เริ่มแรก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ORIGIN,
)
class FirstCellsFoundation(QuestionType):
    """Early atmosphere, Miller-Urey, the RNA world, and the first oxygen."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ORIGIN_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ORIGIN, hint=ORIGIN_HINT)


@question_type(
    "biology.first_cells_fluency",
    display_name={"th": "ทฤษฎีเอนโดซิมไบโอซิสและหลักฐานสนับสนุน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ORIGIN,
)
class FirstCellsFluency(QuestionType):
    """Mitochondria and chloroplasts were once free-living bacteria."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ไมโทคอนเดรียมาจากแบคทีเรียที่ใช้ O₂ คลอโรพลาสต์มาจากไซยาโนแบคทีเรีย หลักฐานคือ DNA วงกลม เยื่อสองชั้น ไรโบโซมเล็ก และการแบ่งตัว"
        roll = rng.random()
        if roll < 0.3:
            stem, right, wrongs = rng.choice(ENDO_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ORIGIN, hint=hint)
        if roll < 0.7:
            return _labelled(stem="ข้อใดเป็นหลักฐานสนับสนุนทฤษฎีเอนโดซิมไบโอซิส", correct=rng.choice(ENDO_EVIDENCE),
                             wrongs=tuple(NOT_ENDO), topic=TOPIC_ORIGIN, hint=hint)
        return _labelled(stem="ข้อใดไม่ใช่หลักฐานสนับสนุนทฤษฎีเอนโดซิมไบโอซิส", correct=rng.choice(NOT_ENDO),
                         wrongs=tuple(ENDO_EVIDENCE), topic=TOPIC_ORIGIN, hint=hint)


@question_type(
    "biology.first_cells_application",
    display_name={"th": "ลำดับเหตุการณ์และมาตราส่วนเวลาทางธรณีวิทยา"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ORIGIN,
)
class FirstCellsApplication(QuestionType):
    """Scale Earth's history down, and put events in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            event, ago = rng.choice(EVENTS)
            model, unit, per = rng.choice(SCALES)
            intro = f"ถ้าย่อประวัติโลก 4,600 ล้านปีให้เป็น{model} โดยปลายด้านหนึ่งคือปัจจุบัน ({unit} ละ {per:,} ล้านปี)"
            hint = f"ระยะจากปัจจุบัน = จำนวนล้านปีที่ผ่านมา ÷ {per:,}"
            if rng.random() < 0.6:
                return numeric(stem=f"{intro} เหตุการณ์ \"{event}\" เมื่อประมาณ {ago:,} ล้านปีก่อน อยู่ห่างจากปลายปัจจุบันกี่{unit}",
                               answer=Fraction(ago, per), wrongs=[Fraction(4600 - ago, per), Fraction(ago, per * 10), ago],
                               unit=unit, topic=TOPIC_ORIGIN, hint=hint)
            where = Fraction(ago, per)
            return numeric(stem=f"{intro} เหตุการณ์หนึ่งอยู่ห่างจากปลายปัจจุบัน {show(where)} {unit} เกิดขึ้นเมื่อประมาณกี่ล้านปีก่อน",
                           answer=ago, wrongs=[4600 - ago, ago // 10 or ago * 10, ago * 10], unit="ล้านปี", topic=TOPIC_ORIGIN, hint=hint)
        picked = sorted(rng.sample(EVENTS[1:], 4), key=lambda e: -e[1])
        first = rng.random() < 0.5
        right = picked[0][0] if first else picked[-1][0]
        shuffled = [e[0] for e in picked]
        rng.shuffle(shuffled)
        return _labelled(stem=f"เหตุการณ์ใดเกิดขึ้น{'ก่อน' if first else 'หลัง'}สุด", correct=right,
                         wrongs=tuple(e for e in shuffled if e != right), topic=TOPIC_ORIGIN,
                         hint="โพรแคริโอต → ไซยาโนแบคทีเรีย → ออกซิเจนสะสม → ยูแคริโอต → หลายเซลล์ → สัตว์ยุคแคมเบรียน")

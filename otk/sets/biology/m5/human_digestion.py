"""การย่อยอาหารและการดูดซึมของมนุษย์

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/3

Sets moved here from: science_wave_f59.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f59 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HUMAN = "การย่อยอาหารและการดูดซึมของมนุษย์"


ENZYMES = (
    ("อะไมเลสในน้ำลาย", "ปาก", "แป้งเป็นมอลโทส"),
    ("เพปซิน", "กระเพาะอาหาร", "โปรตีนเป็นพอลิเพปไทด์สายสั้น"),
    ("ทริปซิน", "ลำไส้เล็ก (หลั่งจากตับอ่อน)", "พอลิเพปไทด์เป็นเพปไทด์สายสั้น"),
    ("อะไมเลสจากตับอ่อน", "ลำไส้เล็ก (หลั่งจากตับอ่อน)", "แป้งที่เหลือเป็นมอลโทส"),
    ("ไลเพส", "ลำไส้เล็ก (หลั่งจากตับอ่อน)", "ไขมันเป็นกรดไขมันและกลีเซอรอล"),
    ("มอลเทส", "ลำไส้เล็ก", "มอลโทสเป็นกลูโคส"),
    ("ซูเครส", "ลำไส้เล็ก", "ซูโครสเป็นกลูโคสและฟรักโทส"),
    ("แล็กเทส", "ลำไส้เล็ก", "แล็กโทสเป็นกลูโคสและกาแล็กโทส"),
)


HUMAN_HINT = ("ปากย่อยแป้ง กระเพาะย่อยโปรตีนด้วยเพปซินในกรด ลำไส้เล็กย่อยทุกชนิดด้วยเอนไซม์จากตับอ่อนและผนังลำไส้ "
              "น้ำดีช่วยให้ไขมันแตกตัวแต่ไม่ใช่เอนไซม์ สารอาหารดูดซึมที่วิลลัส")


HUMAN_FACTS = (
    ("น้ำดีช่วยการย่อยอาหารอย่างไร", "ทำให้ไขมันแตกเป็นหยดเล็ก ๆ เพิ่มพื้นที่ให้ไลเพสทำงาน",
     ("ย่อยไขมันเป็นกรดไขมันโดยตรง", "ย่อยโปรตีนในลำไส้เล็ก", "เปลี่ยนแป้งเป็นกลูโคส เพื่อให้ดูดซึมได้ง่ายขึ้นในลำไส้เล็ก", "ย่อยไขมันเป็นกรดไขมันและกลีเซอรอลได้โดยตรงโดยไม่ต้องใช้ไลเพส")),
    ("กลูโคสและกรดอะมิโนที่ดูดซึมที่วิลลัสเข้าสู่ส่วนใดก่อน", "หลอดเลือดฝอยในวิลลัส แล้วไปตับทางเวนตับ",
     ("หลอดน้ำเหลืองแล็กเทียล", "ลำไส้ใหญ่", "หลอดน้ำเหลืองในผนังกระเพาะอาหาร", "กระเพาะอาหาร")),
    ("กรดไขมันและกลีเซอรอลส่วนใหญ่ถูกดูดซึมเข้าสู่ส่วนใด", "หลอดน้ำเหลืองแล็กเทียลในวิลลัส",
     ("หลอดเลือดฝอยแล้วไปตับทันที", "ผนังกระเพาะอาหาร", "ลำไส้ใหญ่", "หลอดเลือดฝอยในวิลลัสแล้วไปหัวใจ")),
    ("ลำไส้ใหญ่มีหน้าที่หลักอย่างไร", "ดูดน้ำและแร่ธาตุบางชนิดกลับ และเก็บกากอาหาร",
     ("ย่อยโปรตีนด้วยเพปซิน", "ดูดซึมกลูโคสส่วนใหญ่", "ดูดซึมกรดอะมิโนส่วนใหญ่เข้าสู่เลือด", "สร้างเอนไซม์ย่อยแป้งและโปรตีนให้ลำไส้เล็ก")),
    ("วิลลัสและไมโครวิลลัสในลำไส้เล็กมีประโยชน์อย่างไร", "เพิ่มพื้นที่ผิวในการดูดซึมสารอาหาร",
     ("หลั่งกรดไฮโดรคลอริก", "บดอาหารให้ละเอียด", "เพิ่มพื้นที่ผิวในการย่อยไขมัน", "สร้างน้ำดี")),
    ("กรดไฮโดรคลอริกในกระเพาะอาหารมีบทบาทอย่างไร", "ทำให้เพปซิโนเจนเปลี่ยนเป็นเพปซินและช่วยฆ่าจุลินทรีย์",
     ("ย่อยแป้งเป็นมอลโทส", "ทำให้ไขมันแตกตัว", "ย่อยแป้งเป็นมอลโทสและช่วยฆ่าจุลินทรีย์", "สร้างน้ำดี")),
    ("น้ำดีสร้างจากอวัยวะใดและเก็บไว้ที่ใด", "สร้างที่ตับ เก็บไว้ที่ถุงน้ำดี",
     ("สร้างที่ถุงน้ำดี เก็บไว้ที่ตับ", "สร้างที่ตับอ่อน เก็บไว้ที่ลำไส้เล็ก", "สร้างที่กระเพาะอาหาร เก็บไว้ที่ตับ", "สร้างที่ม้าม เก็บไว้ที่ตับ")),
    ("เหตุใดเพปซินจึงหยุดทำงานเมื่ออาหารเข้าสู่ลำไส้เล็ก", "ลำไส้เล็กมีสภาพเป็นเบสเล็กน้อยจากโซเดียมไฮโดรเจนคาร์บอเนต",
     ("ลำไส้เล็กเป็นกรดจัดเกินไป", "เพปซินถูกน้ำดีย่อยจนหมดก่อนถึงลำไส้เล็ก", "อุณหภูมิในลำไส้เล็กต่ำเกินไป", "ลำไส้เล็กมีสภาพเป็นกรดจัดจากกรดไฮโดรคลอริกที่ไหลตามมา")),
)


# (enzyme, substrate, best pH label, test and positive result meaning digestion)
TUBE_ENZYMES = (("น้ำลาย", "น้ำแป้ง", "กลาง", "หยดสารละลายไอโอดีนแล้วไม่เปลี่ยนเป็นสีน้ำเงินปนม่วง"),
                ("เพปซิน", "ไข่ขาวต้มสุก", "กรด", "ไข่ขาวถูกย่อยจนใสหรือหายไป"),
                ("ไลเพสจากตับอ่อน", "น้ำมันพืชผสมน้ำ", "เบสเล็กน้อย", "สารผสมมีความเป็นกรดเพิ่มขึ้นจากกรดไขมัน"))


PH_TEXT = {"กรด": "สารละลายกรดไฮโดรคลอริกเจือจาง", "กลาง": "น้ำกลั่น", "เบสเล็กน้อย": "สารละลายโซเดียมไฮโดรเจนคาร์บอเนตเจือจาง"}


@question_type(
    "biology.human_digestion_foundation",
    display_name={"th": "เอนไซม์ย่อยอาหาร แหล่งที่ทำงาน และผลที่ได้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanDigestionFoundation(QuestionType):
    """Enzyme, where it works, and what it makes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, where, does = rng.choice(ENZYMES)
        others = rng.sample([e for e in ENZYMES if e[0] != name and e[2] != does], 3)
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"{name}ย่อยสารใดเป็นสารใด", correct=does, wrongs=tuple(e[2] for e in others), topic=TOPIC_HUMAN,
                             hint=HUMAN_HINT)
        if roll < 0.75:
            return _labelled(stem=f"เอนไซม์ใดย่อย{does}", correct=name, wrongs=tuple(e[0] for e in others), topic=TOPIC_HUMAN, hint=HUMAN_HINT)
        # Both small-intestine labels are true of any small-intestine enzyme, so neither is a wrong answer for one.
        places = sorted(p for p in {e[1] for e in ENZYMES} | {"ลำไส้ใหญ่", "หลอดอาหาร"}
                        if p != where and not (p.startswith("ลำไส้เล็ก") and where.startswith("ลำไส้เล็ก")))
        return _labelled(stem=f"{name}ทำงานที่ใด", correct=where, wrongs=tuple(places), topic=TOPIC_HUMAN, hint=HUMAN_HINT)


@question_type(
    "biology.human_digestion_fluency",
    display_name={"th": "หน้าที่ของอวัยวะย่อยอาหารและการดูดซึม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanDigestionFluency(QuestionType):
    """Bile, villi, lacteals, the large intestine, and pH."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(HUMAN_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HUMAN, hint=HUMAN_HINT)


@question_type(
    "biology.human_digestion_application",
    display_name={"th": "วิเคราะห์ผลการทดลองการทำงานของเอนไซม์ย่อยอาหาร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanDigestionApplication(QuestionType):
    """Only the tube with active enzyme, its substrate, its pH and body heat digests."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        enzyme, substrate, best, sign = rng.choice(TUBE_ENZYMES)
        # Saliva and lipase still work near neutral, so their failing tube is acid; pepsin fails anywhere not acid.
        wrong_ph = "กรด" if best != "กรด" else rng.choice(("กลาง", "เบสเล็กน้อย"))
        tubes = [("ก", f"{substrate} + {enzyme} + {PH_TEXT[best]} ที่ 37 °C", True),
                 ("ข", f"{substrate} + {enzyme}ที่ต้มเดือดแล้ว + {PH_TEXT[best]} ที่ 37 °C", False),
                 ("ค", f"{substrate} + {enzyme} + {PH_TEXT[wrong_ph]} ที่ 37 °C", False),
                 ("ง", f"{substrate} + น้ำกลั่นแทน{enzyme} + {PH_TEXT[best]} ที่ 37 °C", False)]
        contents = [t[1] for t in tubes]
        rng.shuffle(contents)
        labels = ("ก", "ข", "ค", "ง")
        digesting = contents.index(tubes[0][1])
        listing = " ".join(f"หลอด {ell}: {c}" for ell, c in zip(labels, contents))
        return _labelled(stem=f"{listing} หลอดใดจะพบว่า{sign}", correct=f"หลอด {labels[digesting]}",
                         wrongs=tuple(f"หลอด {ell}" for i, ell in enumerate(labels) if i != digesting), topic=TOPIC_HUMAN,
                         hint="เอนไซม์ทำงานได้เมื่อไม่ถูกความร้อนทำลาย อยู่ใน pH ที่เหมาะสม (น้ำลายเป็นกลาง เพปซินเป็นกรด ไลเพสเป็นเบสเล็กน้อย) และอุณหภูมิร่างกาย")

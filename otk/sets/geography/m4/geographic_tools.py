"""เครื่องมือทางภูมิศาสตร์

ภูมิศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ส 5.1 ม.4-6/3
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import Concept, ConceptBankType, widen
from otk.sets._support.geography import M4, SUBJECT, choices, number, stage

PROVENANCE = Provenance("original")


TOPIC = "เครื่องมือทางภูมิศาสตร์"


@question_type(
    "geog.contour_reading_m4",
    display_name={"th": "อ่านลักษณะภูมิประเทศจากเส้นชั้นความสูง"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class ContourReading(ConceptBankType):
    ITEMS = [
        Concept("เส้นชั้นความสูงคืออะไร", "เส้นที่ลากเชื่อมจุดที่มีความสูงเท่ากัน",
                ("เส้นที่ลากเชื่อมจุดที่มีอุณหภูมิเท่ากัน", "เส้นที่ลากเชื่อมจุดที่มีความกดอากาศเท่ากัน",
                 "เส้นที่ลากเชื่อมจุดที่มีปริมาณฝนเท่ากัน")),
        Concept("บริเวณที่เส้นชั้นความสูงอยู่ชิดกันมาก แสดงว่าพื้นที่นั้นเป็นอย่างไร", "เป็นที่ลาดชันมาก",
                ("เป็นที่ราบเรียบ", "เป็นแหล่งน้ำกว้าง", "มีความสูงเท่ากันทั้งบริเวณ")),
        Concept("บริเวณที่เส้นชั้นความสูงอยู่ห่างกันมาก แสดงว่าพื้นที่นั้นเป็นอย่างไร",
                "เป็นที่ลาดเอียงน้อยหรือค่อนข้างราบ",
                ("เป็นหน้าผาที่สูงชันมาก", "เป็นยอดเขาที่สูงที่สุดในแผนที่", "เป็นหุบเขาที่ลึกและแคบ")),
        Concept("เส้นชั้นความสูงเป็นวงปิดซ้อนกัน โดยค่าความสูงเพิ่มขึ้นเข้าหาวงในสุด แสดงลักษณะภูมิประเทศใด",
                "เนินเขาหรือยอดเขา", ("แอ่งหรือหลุมยุบ", "ที่ราบกว้างใหญ่", "ลำน้ำที่ไหลผ่าน")),
        Concept("ค่าความสูงบนแผนที่ภูมิประเทศวัดเทียบกับระดับใด", "ระดับทะเลปานกลาง",
                ("ระดับพื้นดินที่ผู้วัดยืนอยู่", "ระดับยอดเขาที่สูงที่สุด", "ระดับน้ำในแม่น้ำสายหลัก")),
    ]


@question_type(
    "geog.contour_interval_m4",
    display_name={"th": "หาช่วงชั้นความสูงจากเส้นชั้นความสูงหลักและเส้นแทรก"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class ContourInterval(QuestionType):
    def build(self, rng: Random, **params):
        while True:
            interval = rng.choice((5, 10, 20, 25, 50))
            between = rng.randint(2, 4)
            gaps = between + 1
            low = rng.randint(1, 12) * 50
            high = low + interval * gaps
            slip = Fraction(high - low, between)
            if slip.denominator == 1:
                break
        # Only wrong values that come out exact: a rounded one would stand out.
        extra = Fraction(high - low, gaps + 1)
        wrongs = [("count.lines_not_gaps", f"{number(slip)} เมตร")]
        if extra.denominator == 1:
            wrongs.append(f"{number(extra)} เมตร")
        wrongs += [f"{interval * 2} เมตร", f"{number(high - low)} เมตร", f"{interval + 5} เมตร"]
        return choices(
            stem=(f"บนแผนที่ภูมิประเทศ เส้นชั้นความสูงหลัก 2 เส้นที่อยู่ติดกันมีค่า {number(low)} เมตร และ "
                  f"{number(high)} เมตร ระหว่างสองเส้นนี้มีเส้นชั้นความสูงอีก {between} เส้นที่แบ่งช่วงเท่า ๆ กัน "
                  "ช่วงชั้นความสูงเท่ากับกี่เมตร"),
            correct=f"{interval} เมตร",
            wrongs=wrongs,
            hint="นับจำนวนช่วงระหว่างเส้น ไม่ใช่จำนวนเส้น: ถ้ามีเส้นแทรก n เส้น จะมี n + 1 ช่วง",
            topic=TOPIC)


@question_type(
    "geog.contour_height_m4",
    display_name={"th": "หาความสูงของจุดจากเส้นชั้นความสูง"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class ContourHeight(QuestionType):
    def build(self, rng: Random, **params):
        interval = rng.choice((10, 20, 25, 50))
        base = rng.randint(2, 20) * interval
        lines = rng.randint(2, 6)
        up = rng.random() < 0.6
        sign = 1 if up else -1
        word = "สูงกว่า" if up else "ต่ำกว่า"
        return choices(
            stem=(f"แผนที่ภูมิประเทศมีช่วงชั้นความสูง {interval} เมตร จุด ก อยู่บนเส้นชั้นความสูง {number(base)} เมตร "
                  f"จุด ข อยู่บนเส้นชั้นความสูงที่{word}จุด ก ไป {lines} เส้น จุด ข สูงจากระดับทะเลปานกลางกี่เมตร"),
            correct=f"{number(base + sign * lines * interval)} เมตร",
            wrongs=[("operation.reversed", f"{number(base - sign * lines * interval)} เมตร"),
                    ("count.lines_not_gaps", f"{number(base + sign * (lines + 1) * interval)} เมตร"),
                    f"{number(base + sign * (lines - 1) * interval)} เมตร",
                    f"{number(base + sign * lines)} เมตร"],
            hint="เส้นชั้นความสูงที่อยู่ติดกันต่างกันหนึ่งช่วงชั้นความสูง นับจำนวนเส้นแล้วคูณด้วยช่วงชั้นความสูง",
            topic=TOPIC)


@question_type(
    "geog.slope_gradient_m4",
    display_name={"th": "หาความลาดชันจากเส้นชั้นความสูงและมาตราส่วน"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class SlopeGradient(QuestionType):
    def build(self, rng: Random, **params):
        while True:
            rise = rng.choice((20, 25, 40, 50, 100))
            run_per_rise = rng.randint(4, 40)
            scale = rng.choice((10_000, 20_000, 25_000, 50_000))
            ground = rise * run_per_rise              # metres
            cm = Fraction(ground * 100, scale)
            if (cm * 10).denominator == 1 and 1 <= cm <= 15 and run_per_rise % 10:
                break
        low = rng.randint(1, 15) * 50
        return choices(
            stem=(f"แผนที่มาตราส่วน 1 : {number(scale)} จุด ก อยู่บนเส้นชั้นความสูง {number(low)} เมตร จุด ข อยู่บน"
                  f"เส้นชั้นความสูง {number(low + rise)} เมตร ระยะระหว่างจุดทั้งสองบนแผนที่วัดได้ {number(cm)} เซนติเมตร "
                  "ความลาดชันระหว่างจุด ก กับจุด ข เป็นเท่าใด (ระยะดิ่ง : ระยะราบ)"),
            correct=f"1 : {run_per_rise}",
            wrongs=[("units.wrong_conversion", f"1 : {run_per_rise * 10}"),
                    ("units.wrong_conversion", f"1 : {number(Fraction(run_per_rise, 10))}"),
                    f"{run_per_rise} : 1", f"1 : {run_per_rise * 2}"],
            hint="แปลงระยะบนแผนที่เป็นระยะราบจริงด้วยมาตราส่วน (เมตร) แล้วเทียบกับผลต่างของความสูง",
            topic=TOPIC)


@question_type(
    "geog.geoinformatics_m4",
    display_name={"th": "เลือกใช้ภูมิสารสนเทศ: GIS, GNSS และการรับรู้จากระยะไกล"},
    level=M4, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class Geoinformatics(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็นการใช้{category}"
    CATEGORIES = [
        Category("ระบบสารสนเทศภูมิศาสตร์ (GIS)", (
            "ซ้อนชั้นข้อมูลดิน ความลาดชัน และถนน เพื่อหาที่ตั้งโรงเรียนแห่งใหม่",
            "รวมข้อมูลจำนวนประชากรของแต่ละตำบลแล้วแสดงเป็นแผนที่",
            "ซ้อนแผนที่ระดับความสูงกับที่ตั้งบ้านเรือนเพื่อหาบ้านที่เสี่ยงน้ำท่วม",
        )),
        Category("ระบบดาวเทียมนำทาง (GNSS) เช่น GPS", (
            "บอกพิกัดตำแหน่งของผู้ใช้จากสัญญาณดาวเทียมนำทาง",
            "บันทึกพิกัดจุดเก็บตัวอย่างดินระหว่างออกภาคสนาม",
            "ติดตามตำแหน่งของรถส่งพัสดุขณะกำลังวิ่งอยู่บนถนน",
        )),
        Category("การรับรู้จากระยะไกล (Remote Sensing)", (
            "เปรียบเทียบภาพถ่ายดาวเทียมสองปีเพื่อดูพื้นที่ป่าที่ถูกบุกรุก",
            "ตรวจหาจุดความร้อนของไฟป่าจากภาพถ่ายดาวเทียม",
            "ใช้ภาพถ่ายทางอากาศสำรวจขอบเขตน้ำท่วมเป็นบริเวณกว้าง",
        )),
    ]

# More rows and items: these tables held five or six, so a learner met them
# all in a few tries. Each added situation is one no other row answers.
ContourReading.ITEMS = [*ContourReading.ITEMS,
    Concept('เส้นชั้นความสูงเป็นวงปิดซ้อนกัน โดยค่าความสูงลดลงเข้าหาวงในสุด แสดงลักษณะภูมิประเทศใด',
            'แอ่งหรือหลุมยุบ',
            ('เนินเขาหรือยอดเขา', 'ที่ราบกว้างใหญ่', 'สันเขาที่ยาวต่อเนื่อง', 'ลำน้ำที่ไหลผ่าน')),
    Concept('เส้นชั้นความสูงหักเป็นรูปตัววี โดยปลายแหลมชี้ไปทางที่สูงขึ้น มักแสดงลักษณะใด',
            'หุบเขาหรือร่องน้ำ',
            ('สันเขาที่ยาวต่อเนื่อง', 'ยอดเขาที่สูงที่สุด', 'ที่ราบกว้างใหญ่', 'แอ่งหรือหลุมยุบ')),
    Concept('ค่าความสูงที่ต่างกันระหว่างเส้นชั้นความสูงสองเส้นที่อยู่ติดกันเรียกว่าอะไร',
            'ช่วงชั้นความสูง',
            ('มาตราส่วนของแผนที่', 'ทิศเหนือของแผนที่', 'เส้นกริดของแผนที่', 'สัญลักษณ์ของแผนที่')),
    Concept('บนแผนที่ภูมิประเทศ สีน้ำเงินมักใช้แสดงสิ่งใด',
            'แหล่งน้ำ เช่น แม่น้ำ',
            ('ถนนและทางรถไฟสายต่าง ๆ', 'ป่าไม้และพืชพรรณธรรมชาติ', 'อาคารบ้านเรือนและหมู่บ้าน', 'ยอดเขาและเนินเขาที่สูงชัน')),
]

# Longer wrong readings for the original items, so their answers are not the
# longest choice.
ContourReading.ITEMS = widen(ContourReading.ITEMS, (
    ("เส้นที่ลากเชื่อมจุดที่มีความชื้นในดินเท่ากัน", "เส้นที่ลากแบ่งเขตจังหวัดและอำเภอบนแผนที่"),
    ("เป็นหุบเหวลึกที่มีหน้าผาสองข้าง", "เป็นที่ราบกว้างที่ไม่มีความลาดเลย"),
    ("เป็นภูเขาสูงชันที่ไต่ขึ้นได้ยากมาก", "เป็นหน้าผาสูงชันริมทะเลที่ลาดชันมาก"),
    ("สันเขาที่ยาวต่อเนื่องหลายลูก", "หุบเขาลึกที่มีลำน้ำไหลผ่าน"),
    ("ระดับเมฆที่อยู่ต่ำที่สุดบนท้องฟ้า", "ระดับความสูงของอาคารที่สูงที่สุดในเมือง"),
    ("เนินเขาหรือยอดเขาที่สูงชัน", "ที่ราบกว้างใหญ่ไม่มีเนิน"),
    ("ยอดเขาที่สูงที่สุดในแผนที่", "ทางเดินบนสันเขาที่ยาว"),
    ("มาตราส่วนเส้นบรรทัดของแผนที่", "เส้นแบ่งเขตการปกครองบนแผนที่"),
    ("พื้นที่เกษตรกรรมและทุ่งนา", "ทะเลทรายและพื้นที่แห้งแล้ง"),
))

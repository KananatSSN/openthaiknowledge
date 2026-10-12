"""สถิติประยุกต์

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType

PROVENANCE = Provenance("original")


@question_type("math.data_type_classify", display_name={"th": "ข้อมูลเชิงปริมาณหรือคุณภาพ"},
               level={"th": "ม.6"}, topic="สถิติประยุกต์")
class DataTypeClassify(ChoiceType):
    QUANTITATIVE = ["ส่วนสูงของนักเรียน", "จำนวนพี่น้อง", "น้ำหนักกระเป๋า",
                    "คะแนนสอบวิชาคณิตศาสตร์", "อายุของผู้ตอบแบบสอบถาม",
                    "ระยะทางจากบ้านถึงโรงเรียน"]
    QUALITATIVE = ["สีที่ชอบ", "เพศ", "จังหวัดที่เกิด", "ยี่ห้อโทรศัพท์",
                   "ระดับความพึงพอใจ", "อาชีพของผู้ปกครอง"]

    def compose(self, rng: Random):
        if rng.random() < 0.5:
            item, answer = rng.choice(self.QUANTITATIVE), "ข้อมูลเชิงปริมาณ"
        else:
            item, answer = rng.choice(self.QUALITATIVE), "ข้อมูลเชิงคุณภาพ"
        other = ("ข้อมูลเชิงคุณภาพ" if answer == "ข้อมูลเชิงปริมาณ"
                 else "ข้อมูลเชิงปริมาณ")
        return (f"ข้อมูล “{item}” จัดเป็นข้อมูลชนิดใด", answer,
                [other, "ไม่ใช่ข้อมูลทางสถิติ", "เป็นได้ทั้งสองชนิด"])


@question_type("math.classify_data_type",
               display_name={"th": "จำแนกชนิดข้อมูล"}, level={"th": "ม.6"},
               topic="สถิติประยุกต์")
class ClassifyDataType(ChoiceType):
    _CONT, _DISC, _QUAL = ("ข้อมูลเชิงปริมาณแบบต่อเนื่อง",
                           "ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง",
                           "ข้อมูลเชิงคุณภาพ")
    _ATTRS = [("ส่วนสูงของนักเรียน", _CONT), ("น้ำหนักของผลไม้", _CONT),
              ("อุณหภูมิของอากาศในแต่ละวัน", _CONT), ("เวลาที่ใช้วิ่ง 100 เมตร", _CONT),
              ("ปริมาณน้ำฝนในแต่ละเดือน", _CONT), ("ระยะทางจากบ้านถึงโรงเรียน", _CONT),
              ("จำนวนพี่น้อง", _DISC), ("จำนวนนักเรียนในห้อง", _DISC),
              ("จำนวนรถยนต์ที่ผ่านสี่แยกในหนึ่งชั่วโมง", _DISC),
              ("จำนวนหนังสือที่อ่านในหนึ่งเดือน", _DISC), ("จำนวนครั้งที่ขาดเรียนในภาคเรียน", _DISC),
              ("สีที่ชอบ", _QUAL), ("เพศ", _QUAL), ("กรุ๊ปเลือด", _QUAL),
              ("จังหวัดที่เกิด", _QUAL), ("ยี่ห้อโทรศัพท์ที่ใช้", _QUAL),
              ("ระดับความพึงพอใจ (มาก ปานกลาง น้อย)", _QUAL)]

    def compose(self, rng: Random):
        attr, label = rng.choice(self._ATTRS)
        others = [x for x in (self._CONT, self._DISC, self._QUAL) if x != label]
        return f"ข้อมูล “{attr}” เป็นข้อมูลชนิดใด?", label, others


@question_type("math.measurement_scale", display_name={"th": "มาตราการวัดของข้อมูล"},
               level={"th": "ม.6"}, topic="สถิติประยุกต์")
class MeasurementScale(ChoiceType):
    ITEMS = [
        ("หมายเลขเสื้อนักกีฬา", "มาตรานามบัญญัติ"),
        ("อันดับที่ได้จากการแข่งขัน", "มาตราเรียงอันดับ"),
        ("อุณหภูมิเป็นองศาเซลเซียส", "มาตราอันตรภาค"),
        ("น้ำหนักเป็นกิโลกรัม", "มาตราอัตราส่วน"),
        ("เลขประจำตัวนักเรียน", "มาตรานามบัญญัติ"),
        ("ระดับความพึงพอใจ 1–5", "มาตราเรียงอันดับ"),
        ("รหัสไปรษณีย์", "มาตรานามบัญญัติ"),
        ("กรุ๊ปเลือด", "มาตรานามบัญญัติ"),
        ("ระดับการศึกษา (ประถม มัธยม ปริญญาตรี)", "มาตราเรียงอันดับ"),
        ("ขนาดเสื้อ S M L XL", "มาตราเรียงอันดับ"),
        ("อุณหภูมิเป็นองศาฟาเรนไฮต์", "มาตราอันตรภาค"),
        ("ปีพุทธศักราช", "มาตราอันตรภาค"),
        ("ส่วนสูงเป็นเซนติเมตร", "มาตราอัตราส่วน"),
        ("รายได้ต่อเดือนเป็นบาท", "มาตราอัตราส่วน"),
        ("เวลาที่ใช้ทำข้อสอบเป็นนาที", "มาตราอัตราส่วน"),
    ]
    SCALES = ["มาตรานามบัญญัติ", "มาตราเรียงอันดับ", "มาตราอันตรภาค",
              "มาตราอัตราส่วน"]

    def compose(self, rng: Random):
        item, answer = rng.choice(self.ITEMS)
        return (f"ข้อมูล “{item}” อยู่ในมาตราการวัดใด", answer,
                [s for s in self.SCALES if s != answer])

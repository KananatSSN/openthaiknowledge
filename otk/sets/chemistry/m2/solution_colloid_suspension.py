"""สารละลาย คอลลอยด์ และสารแขวนลอย

เคมี · ม.2 · เสริมทักษะ
Indicators: —

Sets moved here from: substances.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.substances import LEVEL, SUBJECT, TOPIC_PURE

PROVENANCE = Provenance("original")


@question_type("chem.solution_colloid_suspension",
               display_name={"th": "สารละลาย คอลลอยด์ และสารแขวนลอย"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_PURE)
class SolutionColloidSuspension(ClassifyType):
    """จำแนกจากขนาดอนุภาค การตกตะกอน การกรอง และการเกิดทินดอล."""

    CLASSIFY_STEM = "“{member}” ตรงกับสารประเภทใด"
    PICK_STEM = "ข้อใดเป็นตัวอย่างหรือลักษณะของ{category}"

    CATEGORIES = [
        Category("สารละลาย (Solution)",
                 ("อนุภาคมีขนาดเล็กที่สุด คือเล็กกว่า 10⁻⁷ เซนติเมตร",
                  "ตั้งทิ้งไว้นานเท่าใดก็ไม่ตกตะกอน",
                  "ผ่านกระดาษกรองได้ทั้งหมด",
                  "ไม่เกิดปรากฏการณ์ทินดอล เพราะอนุภาคเล็กเกินกว่าจะกระเจิงแสง",
                  "น้ำเกลือ น้ำเชื่อม น้ำส้มสายชู")),
        Category("คอลลอยด์ (Colloid)",
                 ("อนุภาคมีขนาดปานกลาง ระหว่าง 10⁻⁷ ถึง 10⁻⁴ เซนติเมตร",
                  "ตั้งทิ้งไว้แล้วไม่ตกตะกอน แต่เนื้อสารขุ่น",
                  "ผ่านกระดาษกรองได้ แต่ผ่านเยื่อกึ่งซึมผ่านไม่ได้",
                  "เกิดปรากฏการณ์ทินดอล มองเห็นลำแสงพาดผ่านเนื้อสาร",
                  "นมสด หมอก ควัน วุ้น เจล")),
        Category("สารแขวนลอย (Suspension)",
                 ("อนุภาคมีขนาดใหญ่ที่สุด คือใหญ่กว่า 10⁻⁴ เซนติเมตร",
                  "ตั้งทิ้งไว้สักครู่แล้วตกตะกอนแยกชั้น",
                  "ถูกกระดาษกรองกั้นไว้ จึงแยกออกได้ด้วยการกรอง",
                  "น้ำโคลน น้ำแป้งดิบ น้ำปูนขาว")),
    ]
